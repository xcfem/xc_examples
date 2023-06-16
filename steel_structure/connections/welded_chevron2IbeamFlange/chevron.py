# -*- coding: utf-8 -*-
from __future__ import division 
from __future__ import print_function


import geom
import xc
import math

from model import predefined_spaces
from solution import predefined_solutions
from model.geometry import grid_model as gm
from model.mesh import finit_el_model as fem
from model.sets import sets_mng as sets
from materials import typical_materials as tm
from materials.astm_aisc import ASTM_materials
from actions import loads
from actions import load_cases as lcases
from postprocess import limit_state_data as lsd
from materials.sections.structural_shapes import aisc_metric_shapes as lb
from actions import combinations as combs
from materials.astm_aisc import AISC_limit_state_checking as aisc
from connections.steel_connections import cbfem_bolt_weld as sc
from connections.steel_connections import check_report  as checksc

# Default configuration of environment variables.
from postprocess.config import default_config
from postprocess import output_styles as outSty
from postprocess import output_handler as outHndl

# ***Data***
# 
steelW=ASTM_materials.A992   #steel support W shapes
beamShape=ASTM_materials.WShape(steelW,lb.getUSLabel('W250X44.8'))
steelPlate=ASTM_materials.A36   #steel shear plates

gsstThk=16e-3  # thickness of the gusset
gsstH=200e-3  # hight of the gusset
gsstW=150e-3  # half width of the gusset
chmfH=50e-3   # height of the chamfer in the gusset
chmfW=50e-3   # width of the chamfer in the gusset

LtotBeam=4.09 #total legth of beam
Hdiag=14.39-12.14 # projection of diagonal dimension on the axis Z
Lbeam=1.2 # length of beam near de chevron gusset

#weld gusset-lower flange
weldSz=5e-3 # weld size
weldMetal=ASTM_materials.E7018

# loads
N1d= 10e3 # design axial force in left diagonal
N2d= 15e3 # design axial force in right diagonal
lN=0.2 #length to get the load application point

esize=0.05
title='Lime silo - chevron bracing connection'

# *** End data

theta=math.atan(Hdiag/(LtotBeam/2))

unitV_N1=geom.Vector3d(-math.cos(theta),0,-math.sin(theta))
unitV_N2=geom.Vector3d(math.cos(theta),0,-math.sin(theta))

yb=beamShape.b()/2
xb=round(Lbeam/2,1)
xbtot=round(LtotBeam/2,1)
zb=beamShape.h()-beamShape.tf()

xLst_beam=[0,-xbtot,xbtot,-xb,xb] ; xLst_beam.sort()  
yLst_beam=[0,-yb,yb] ; yLst_beam.sort() 
zLst_beam=[0,zb] ; zLst_beam.sort()

xgss=gsstW
xchf=gsstW-chmfW
zgssTop=0
zgssBot=-gsstH
zchf=-(gsstH-chmfH)
xLst_gsst=[0,-xgss,xgss,-xchf,xchf] ; xLst_gsst.sort()  
yLst_gsst=[0] 
zLst_gsst=[zgssTop,zgssBot] ; zLst_gsst.sort()


FEcase= xc.FEProblem()
FEcase.title= title
preprocessor=FEcase.getPreprocessor
prep=preprocessor   #short name
nodes= prep.getNodeHandler
elements= prep.getElementHandler
elements.dimElem= 3
# Problem type
modelSpace= predefined_spaces.StructuralMechanics3D(nodes) #Defines the
# dimension of the space: nodes by three coordinates (x,y,z) and 
# six DOF for each node (Ux,Uy,Uz,thetaX,thetaY,thetaZ)
sty=outSty.OutputStyle() 
out=outHndl.OutputHandler(modelSpace,sty)

gridBeam=gm.GridModel(prep,xLst_beam,yLst_beam,zLst_beam)
gridBeam.generatePoints()

gridGusset=gm.GridModel(prep,xLst_gsst,yLst_gsst,zLst_gsst)
gridGusset.generatePoints()
gridGusset.movePointXYZ((-xgss,0,zgssBot),xc.Vector([0,0,chmfH]))
gridGusset.movePointXYZ((xgss,0,zgssBot),xc.Vector([0,0,chmfH]))

upFlange=gridBeam.genSurfOneXYZRegion(((-xb,-yb,zb),(xb,yb,zb)),'upFlange')
lowFlange=gridBeam.genSurfOneXYZRegion(((-xb,-yb,0),(xb,yb,0)),'lowFlange')
web=gridBeam.genSurfOneXYZRegion(((-xb,0,0),(xb,0,zb)),'web')

gusset=gridGusset.genSurfOneXYZRegion(((-xgss,0,zgssBot),(xgss,0,zgssTop)),'gusset')

upFlangeOut=gridBeam.genSurfMultiXYZRegion([[(-xbtot,-yb,zb),(-xb,yb,zb)],
                                        [(xb,-yb,zb),(xbtot,yb,zb)]],
                                       'upFlangeOut')
lowFlangeOut=gridBeam.genSurfMultiXYZRegion([[(-xbtot,-yb,0),(-xb,yb,0)],
                                        [(xb,-yb,0),(xbtot,yb,0)]],
                                       'lowFlangeOut')
webOut=gridBeam.genSurfMultiXYZRegion([[(-xbtot,0,0),(-xb,0,zb)],
                                   [(xb,0,0),(xbtot,0,zb)]],
                                  'webOut')


# Materials for linear analysis vonmises verification
ndWsteel=tm.defElasticIsotropic3d(preprocessor=prep, name='ndWsteel', E=steelW.E, nu=steelW.nu, rho=steelW.rho)
ndPlateSteel=tm.defElasticIsotropic3d(preprocessor=prep, name='ndPlateSteel', E=steelPlate.E, nu=steelPlate.nu, rho=steelPlate.rho)


flange_mat=tm.defMembranePlateFiberSection(prep,name='flange_mat',h=beamShape.tf(),nDMaterial=ndWsteel)
web_mat=tm.defMembranePlateFiberSection(prep,name='web_mat',h=beamShape.tw(),nDMaterial=ndWsteel)
gusset_mat=tm.defMembranePlateFiberSection(prep,name='cPlate_mat',h=gsstThk,nDMaterial=ndPlateSteel)
    
upFlange_mesh=fem.SurfSetToMesh(surfSet=upFlange,matSect=flange_mat,elemSize=esize,elemType='ShellMITC4')
upFlangeOut_mesh=fem.SurfSetToMesh(surfSet=upFlangeOut,matSect=flange_mat,elemSize=esize,elemType='ShellMITC4')
lowFlange_mesh=fem.SurfSetToMesh(surfSet=lowFlange,matSect=flange_mat,elemSize=esize,elemType='ShellMITC4')
lowFlangeOut_mesh=fem.SurfSetToMesh(surfSet=lowFlangeOut,matSect=flange_mat,elemSize=esize,elemType='ShellMITC4')
web_mesh=fem.SurfSetToMesh(surfSet=web,matSect=web_mat,elemSize=esize,elemType='ShellMITC4')
webOut_mesh=fem.SurfSetToMesh(surfSet=webOut,matSect=web_mat,elemSize=esize,elemType='ShellMITC4')
gusset_mesh=fem.SurfSetToMesh(surfSet=gusset,matSect=gusset_mat,elemSize=esize,elemType='ShellMITC4')
lst_mesh=[upFlange_mesh,upFlangeOut_mesh,lowFlange_mesh,lowFlangeOut_mesh,web_mesh,webOut_mesh,gusset_mesh]
fem.multi_mesh(prep,lst_mesh)

#boundary conditions
beamSet=modelSpace.setSum('beamSet',[upFlange,lowFlange,web,upFlangeOut,lowFlangeOut,webOut])
beamSet.fillDownwards()
bound1=sets.get_set_nodes_plane_YZ('bound1',beamSet,-xbtot)
bound2=sets.get_set_nodes_plane_YZ('bound2',beamSet,xbtot)
for n in bound1.nodes:
    modelSpace.fixNode000_FFF(n.tag)
for n in bound2.nodes:
    modelSpace.fixNode000_FFF(n.tag)

# Welds
weld_t=sc.WeldTyp(weldSz,weldMetal)
l=geom.Segment3d(geom.Pos3d(-xgss,0,0),geom.Pos3d(xgss,0,0))
WFlgGsst=sc.MultiFilletWeld(weld_t,gusset,lowFlange,[l],'WFlgGsst','weld chevron-gusset with flange beam')
WFlgGsst.generateWeld(nDiv=15,WS2sign=-1,bothSidesOfWS1=True)
welds2check=[WFlgGsst]
out.displayFEMesh()

# loads
O=geom.Vector3d(0,0,beamShape.h()/2) 
gc_N1=O+lN*unitV_N1
node_N1=gusset.nodes.getNearestNode(geom.Pos3d(gc_N1.x,gc_N1.y,gc_N1.z))
gc_N2=O+lN*unitV_N2
node_N2=gusset.nodes.getNearestNode(geom.Pos3d(gc_N2.x,gc_N2.y,gc_N2.z))
load_N1=N1d*unitV_N1
load_N2=N2d*unitV_N2

loadLeftDiag=loads.NodalLoad('loadLeftDiag',[node_N1],xc.Vector([load_N1.x,load_N1.y,load_N1.z,0,0,0]))
loadRightDiag=loads.NodalLoad('loadRightDiag',[node_N2],xc.Vector([load_N2.x,load_N2.y,load_N2.z,0,0,0]))


LC1=lcases.LoadCase(preprocessor=prep,name="LC1",loadPType="default",timeSType="constant_ts")
LC1.create()
LC1.addLstLoads([loadLeftDiag,loadRightDiag])

LC2=lcases.LoadCase(preprocessor=prep,name="LC2",loadPType="default",timeSType="constant_ts")
LC2.create()
LC2.addLstLoads([loadLeftDiag])

modelSpace.addLoadCaseToDomain('LC1')                                   
out.displayLoads()
modelSpace.analyze()
out.displayDispRot('uZ')
modelSpace.removeAllLoadPatternsFromDomain()

ULSs=['LC1','LC2']
checksc.aisc_check_bolts_welds(modelSpace, ULSs=ULSs, boltSets2Check=[], welds2Check=welds2check, baseMetal=steelPlate,meanShearProc=True, resFile='welds_check', solutionProcedureType= predefined_solutions.SimpleStaticLinearUMF, reactionCheckTolerance=1e-3,warningsFile='warnings.tex')#foundSprings=No

# Von mises verification

combContainer= combs.CombContainer()
for ULSnm in ULSs:
    combContainer.ULS.perm.add(str(ULSnm),'1.0*'+str(ULSnm))
combContainer.dumpCombinations(prep)

beamSet=modelSpace.setSum('beamSet',[upFlange,lowFlange,web,upFlangeOut,lowFlangeOut,webOut]) 
for e in beamSet.elements: e.setProp('yieldStress', steelW.fy)
for e in gusset.elements: e.setProp('yieldStress', steelPlate.fy)

lstCenterShells=[upFlange,lowFlange,web,gusset]
centerShells=modelSpace.setSum('centerShells',lstCenterShells)
centerShells.description='Beam and chevron gusset'
lstAllShells=lstCenterShells+[upFlangeOut,lowFlangeOut,webOut]
allShells=modelSpace.setSum('allShells',lstAllShells)
setCalc=centerShells

cfg= default_config.EnvConfig(language='en', resultsPath= 'tmp_results/', intForcPath= 'internalForces/',verifPath= 'verifications/',reportPath='./',reportResultsPath= 'annex/',grWidth='120mm')
cfg.projectDirTree.workingDirectory='./'
lsd.LimitStateData.envConfig= cfg
### Set combinations to compute.
loadCombinations= prep.getLoadHandler.getLoadCombinations

### Limit states to calculate internal forces for.
limitState= lsd.vonMisesStressResistance
limitState.vonMisesStressId= 'avg_von_mises_stress'
limitStates= [limitState]

### Compute internal forces for each combination
for ls in limitStates:
    ls.saveAll(combContainer,setCalc)
### Check material resistance.
outCfg= lsd.VerifOutVars(setCalc=setCalc, appendToResFile='N', listFile='N', calcMeanCF='Y')
outCfg.controller= aisc.VonMisesStressController(limitState.label)
average= limitState.runChecking(outCfg)

#out.displayField(limitStateLabel= limitState.label, section= None, argument= 'CF', component= None, setToDisplay= allShells, fileName= None)
out.displayField(limitStateLabel= limitState.label, section= None, argument= 'CF', component= None, setToDisplay= centerShells, fileName= None)
for st in lstCenterShells:
    out.displayField(limitStateLabel= limitState.label, section= None, argument= 'CF', component= None, setToDisplay= st, fileName= None)

