# -*- coding: utf-8 -*-
from __future__ import division 
from __future__ import print_function


import geom
import xc

from model import predefined_spaces
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

# Default configuration of environment variables.
from postprocess.config import default_config
from postprocess import output_styles as outSty
from postprocess import output_handler as outHndl

# ***Data***
# 

steelW=ASTM_materials.A992   #steel support W shapes
beamShape=ASTM_materials.WShape(steelW,lb.getUSLabel('W460X158'))
steelPlate=ASTM_materials.A36   #steel shear plates

cntPlateThk=22e-3 # thickness of the cantilever plate
cntPlateW=0.13  # width of the cantilever plate (perpendicular to beam)

shPlateThk=14e-3 # thickness of the shear plates
shPlateDist=0.185 # distance between shear plates
shPlateChanf=70e-3 # vertical length of the shear plates

distBoltsPar=0.22 # distance between bolts in direction parallel to beam
distBoltsPerp=0.22 # distance between bolts in direction perpendicular to beam
distBoltsEdge=97e-3 # distance from the bolts to the edge of the plate perpendicular to beam

LtotBeam=4.2 #total legth of beam
Lbeam=0.8 # length of beam to calculate von mises stresses
esize=0.025

# Loads (obtained as Qz in elements of supports set in the residues-silo model
# (with display_weight_cell_intForces.py module)
D=75.4e3 #total dead load over the support
H=375e3 # bulk material
WX=188e3 # wind +X
EX=51e3  # earthquake +X
EfillX=165e3 # earthquake over fill material
# Vertical total forces ultimate limit states
F_ULS01=1.2*D+1.6*H
F_ULS02=1.2*D+1.6*WX
F_ULS03=0.9*D+1.0*EX+1.0*EfillX+1.6*H

Fd=max(F_ULS01,F_ULS02,F_ULS03)

backPlate=True # True if we put stiffener in the back half of the beam
bkPlateThk=14e-3
#*** end data

yb=beamShape.b()/2
yCp=yb+cntPlateW
y2Bl=yCp-distBoltsEdge
y1Bl=y2Bl-distBoltsPerp
xb=round(Lbeam/2,1)
xbtot=round(LtotBeam/2,1)
xBl=distBoltsPar/2
xSp=shPlateDist
zb=beamShape.h()-beamShape.tf()
zSp=zb-shPlateChanf

xLst=[0,-xbtot,xbtot,-xb,xb,-xBl,xBl,-xSp,xSp] ; xLst.sort()  
#xLst=[0,-xb,xb,-xSp,xSp] ; xLst.sort()  
yLst=[0,-yb,yb,yCp,y2Bl,y1Bl] ; yLst.sort() 
#yLst=[0,-yb,yb,yCp] ; yLst.sort() 
zLst=[0,zSp,zb] ; zLst.sort() 

FEcase= xc.FEProblem()
FEcase.title= 'Lime silo'
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

grid=gm.GridModel(prep,xLst,yLst,zLst)
grid.generatePoints()

grid.scaleCoorYPointsXYZrange(XYZrange=((-xbtot,0,0),(xbtot,yCp,0)),yOrig=0,scale=yb/yCp)

upFlange=grid.genSurfOneXYZRegion(((-xb,-yb,zb),(xb,yb,zb)),'upFlange')
lowFlange=grid.genSurfOneXYZRegion(((-xb,-yb,0),(xb,yCp,0)),'lowFlange')
web=grid.genSurfOneXYZRegion(((-xb,0,0),(xb,0,zb)),'web')
cPlate=grid.genSurfOneXYZRegion(((-xSp,yb,zb),(xSp,yCp,zb)),'cPlate')
sPlate=grid.genSurfMultiXYZRegion([[(-xSp,0,0),(-xSp,yCp,zb)],
                                   [(0,0,0),(0,yCp,zb)],
                                   [(xSp,0,0),(xSp,yCp,zb)]],'sPlate')

upFlangeOut=grid.genSurfMultiXYZRegion([[(-xbtot,-yb,zb),(-xb,yb,zb)],
                                        [(xb,-yb,zb),(xbtot,yb,zb)]],
                                       'upFlangeOut')
lowFlangeOut=grid.genSurfMultiXYZRegion([[(-xbtot,-yb,0),(-xb,yCp,0)],
                                        [(xb,-yb,0),(xbtot,yCp,0)]],
                                       'lowFlangeOut')
webOut=grid.genSurfMultiXYZRegion([[(-xbtot,0,0),(-xb,0,zb)],
                                   [(xb,0,0),(xbtot,0,zb)]],
                                  'webOut')
if backPlate:
    bPlate=grid.genSurfOneXYZRegion(((-xb,-yb,0),(xb,-yb,zb)),'bPlate')

#    bPlate=grid.genSurfMultiXYZRegion([[(-xSp,-yb,0),(-xSp,0,zb)],[(0,-yb,0),(0,0,zb)],[(xSp,-yb,0),(xSp,0,zb)]],'bPlate')

#out.displayBlocks()

# Materials for linear analysis vonmises verification
ndWsteel=tm.defElasticIsotropic3d(preprocessor=prep, name='ndWsteel', E=steelW.E, nu=steelW.nu, rho=steelW.rho)
ndPlateSteel=tm.defElasticIsotropic3d(preprocessor=prep, name='ndPlateSteel', E=steelPlate.E, nu=steelPlate.nu, rho=steelPlate.rho)


flange_mat=tm.defMembranePlateFiberSection(prep,name='flange_mat',h=beamShape.tf(),nDMaterial=ndWsteel)
web_mat=tm.defMembranePlateFiberSection(prep,name='web_mat',h=beamShape.tw(),nDMaterial=ndWsteel)
cPlate_mat=tm.defMembranePlateFiberSection(prep,name='cPlate_mat',h=cntPlateThk,nDMaterial=ndPlateSteel)
sPlate_mat=tm.defMembranePlateFiberSection(prep,name='sPlate_mat',h=shPlateThk,nDMaterial=ndPlateSteel)
if backPlate: bPlate_mat=tm.defMembranePlateFiberSection(prep,name='bPlate_mat',h=bkPlateThk,nDMaterial=ndPlateSteel)
    
upFlange_mesh=fem.SurfSetToMesh(surfSet=upFlange,matSect=flange_mat,elemSize=esize,elemType='ShellMITC4')
upFlangeOut_mesh=fem.SurfSetToMesh(surfSet=upFlangeOut,matSect=flange_mat,elemSize=esize,elemType='ShellMITC4')
lowFlange_mesh=fem.SurfSetToMesh(surfSet=lowFlange,matSect=flange_mat,elemSize=esize,elemType='ShellMITC4')
lowFlangeOut_mesh=fem.SurfSetToMesh(surfSet=lowFlangeOut,matSect=flange_mat,elemSize=esize,elemType='ShellMITC4')
web_mesh=fem.SurfSetToMesh(surfSet=web,matSect=web_mat,elemSize=esize,elemType='ShellMITC4')
webOut_mesh=fem.SurfSetToMesh(surfSet=webOut,matSect=web_mat,elemSize=esize,elemType='ShellMITC4')
cPlate_mesh=fem.SurfSetToMesh(surfSet=cPlate,matSect=cPlate_mat,elemSize=None,elemType='ShellMITC4')
sPlate_mesh=fem.SurfSetToMesh(surfSet=sPlate,matSect=sPlate_mat,elemSize=None,elemType='ShellMITC4')
lst_mesh=[upFlange_mesh,upFlangeOut_mesh,lowFlange_mesh,lowFlangeOut_mesh,web_mesh,webOut_mesh,cPlate_mesh,sPlate_mesh]
if backPlate:
    bPlate_mesh=fem.SurfSetToMesh(surfSet=bPlate,matSect=bPlate_mat,elemSize=None,elemType='ShellMITC4')
    lst_mesh.append(bPlate_mesh)
fem.multi_mesh(prep,lst_mesh)
#out.displayFEMesh(sPlate)

#boundary conditions
beamSet=modelSpace.setSum('beamSet',[upFlange,lowFlange,web,upFlangeOut,lowFlangeOut,webOut])
beamSet.fillDownwards()
bound1=sets.get_set_nodes_plane_YZ('bound1',beamSet,-xbtot)
bound2=sets.get_set_nodes_plane_YZ('bound2',beamSet,xbtot)
for n in bound1.nodes:
    modelSpace.fixNode000_FFF(n.tag)
for n in bound2.nodes:
    modelSpace.fixNode000_FFF(n.tag)
out.displayFEMesh()

'''
# Nodes bolts
pBolts=[grid.getPntXYZ([-xBl,y1Bl,zb]),
        grid.getPntXYZ([-xBl,y2Bl,zb]),
        grid.getPntXYZ([xBl,y1Bl,zb]),
        grid.getPntXYZ([xBl,y2Bl,zb])]
nBolts=[p.getNode() for p in pBolts]

#Loads (point loads on nodes of bolts)
designLoad=loads.NodalLoad('designLoad',nBolts,xc.Vector([0,0,-Fd/len(nBolts),0,0,0]))
'''
# load distributed in the weighing cell baseplate surface
surfLoaded=grid.getSetSurfOneXYZRegion(((-xBl,y1Bl,zb),(xBl,yCp,zb)),'surfLoaded')
areaLoaded=0
for s in surfLoaded.surfaces: areaLoaded+=s.getArea()
designLoad=loads.UniformLoadOnSurfaces('designLoad',surfLoaded,xc.Vector([0,0,-Fd/areaLoaded,0,0,0]))

LC1=lcases.LoadCase(preprocessor=prep,name="LC1",loadPType="default",timeSType="constant_ts")
LC1.create()
LC1.addLstLoads([designLoad])

modelSpace.addLoadCaseToDomain('LC1')                                   
out.displayLoads()
modelSpace.analyze()
out.displayDispRot('uZ')
modelSpace.removeAllLoadPatternsFromDomain()

ULSs=['LC1']

# Von mises verification

combContainer= combs.CombContainer()
for ULSnm in ULSs:
    combContainer.ULS.perm.add(str(ULSnm),'1.0*'+str(ULSnm))
combContainer.dumpCombinations(prep)

for e in beamSet.elements: e.setProp('yieldStress', steelW.fy)
for e in cPlate.elements: e.setProp('yieldStress', steelPlate.fy)
for e in sPlate.elements: e.setProp('yieldStress', steelPlate.fy)
if backPlate:
    for e in bPlate.elements: e.setProp('yieldStress', steelPlate.fy)
lstCenterShells=[upFlange,lowFlange,web,cPlate,sPlate]
if backPlate: lstCenterShells.append(bPlate)
centerShells=modelSpace.setSum('centerShells',lstCenterShells)
lstAllShells=lstCenterShells+[upFlangeOut,lowFlangeOut,webOut]
allShells=modelSpace.setSum('allShells',lstAllShells)
setCalc=allShells

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

out.displayField(limitStateLabel= limitState.label, section= None, argument= 'CF', component= None, setToDisplay= allShells, fileName= None)
out.displayField(limitStateLabel= limitState.label, section= None, argument= 'CF', component= None, setToDisplay= centerShells, fileName= None)
for st in lstAllShells:
    out.displayField(limitStateLabel= limitState.label, section= None, argument= 'CF', component= None, setToDisplay= st, fileName= None)

