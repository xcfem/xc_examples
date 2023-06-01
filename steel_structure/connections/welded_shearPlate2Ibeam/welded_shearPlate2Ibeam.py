# -*- coding: utf-8 -*-
from __future__ import division 
from __future__ import print_function

from materials.astm_aisc import ASTM_materials
import sys
import geom
import xc

from postprocess.config import default_config
from model import predefined_spaces
from solution import predefined_solutions
from postprocess import output_styles as outSty
from postprocess import output_handler as outHndl
from materials.astm_aisc import ASTM_materials as astm
from materials import typical_materials as tm
from model.mesh import finit_el_model as fem
from materials.sections.structural_shapes import aisc_metric_shapes as lb
from model.geometry import grid_model as gm
from connections.steel_connections import cbfem_bolt_weld as sc
from model.sets import sets_mng as sets
from actions import loads
from actions import load_cases as lcases
from connections.steel_connections import check_report  as checksc
from actions import combinations as combs
from postprocess import limit_state_data as lsd
from materials.astm_aisc import AISC_limit_state_checking as aisc

# import local modules
import sys
sys.path.insert(0, '../local_modules')
import steel_connection_models as scm

# Beams than support the grating in levels 1 to 3 of the stair tower.
#Data
steel_W=ASTM_materials.A992   #steel support W shapes
steel_plate=ASTM_materials.A36   #steel shear plates
beam_shape=ASTM_materials.WShape(steel_W,'W6X20')

L_beam=1.0 #length of beam to be modelised

dist_cent_bolts=50e-3 # distance between centers of bolts
dist_edge_bolt=25e-3 # distance between the center of the bolt and the edge

plateThck=8e-3 #plate thickness
weldSz=5e-3 # weld size
weldMetal=astm.E7018

Vd=15e3 #design shear force
# end data

FEcase= xc.FEProblem()
prep=FEcase.getPreprocessor
nodes= prep.getNodeHandler
modelSpace= predefined_spaces.StructuralMechanics3D(nodes) #Defines the
sty=outSty.OutputStyle() 
out=outHndl.OutputHandler(modelSpace,sty)

esize=0.015
beam=scm.Icolumn(height=beam_shape.h(),flWidht=beam_shape.b(),webThick=beam_shape.tw(),flThick=beam_shape.tf(),membL=L_beam,setName='beam')
beam.generateSurfaces(prep)
flangeSet=modelSpace.setSum('flangeSet',[beam.flXnegSet,beam.flXposSet])

#Plate 1
x1=beam_shape.tw()/2
x2=beam_shape.b()/2
xBolt=x2+dist_edge_bolt
x3=xBolt+dist_edge_bolt
xListPlt1=[x1,x2,xBolt,x3]


yEdge=beam_shape.h()/2-beam_shape.tf()
yBolt=dist_cent_bolts/2
yList=[-yEdge,-yBolt,yBolt,yEdge]
zPlt=L_beam/2
zList=[zPlt]

gridPlt1=gm.GridModel(prep,xListPlt1,yList,zList)
gridPlt1.generatePoints()

plate1=gridPlt1.genSurfOneXYZRegion(((x1,-yEdge,zPlt),(x3,yEdge,zPlt)),'plate1')

#Plate 2
xListPlt2=[-x1,-x2,-xBolt,-x3]
xListPlt2.sort()
gridPlt2=gm.GridModel(prep,xListPlt2,yList,zList)
gridPlt2.generatePoints()
plate2=gridPlt2.genSurfOneXYZRegion(((-x3,-yEdge,zPlt),(-x1,yEdge,zPlt)),'plate2')

# Materials for linear analysis vonmises verification
ndWsteel=tm.defElasticIsotropic3d(preprocessor=prep, name='ndWsteel', E=steel_W.E, nu=steel_W.nu, rho=steel_W.rho)
ndPlateSteel=tm.defElasticIsotropic3d(preprocessor=prep, name='ndWsteel', E=steel_plate.E, nu=steel_plate.nu, rho=steel_plate.rho)
plate_mat=tm.defMembranePlateFiberSection(prep,name='plate_mat',h=plateThck,nDMaterial=ndPlateSteel)
bmFlange_mat=tm.defMembranePlateFiberSection(prep,name='bmFlange_mat',h=beam_shape.tf(),nDMaterial=ndWsteel)
bmWeb_mat=tm.defMembranePlateFiberSection(prep,name='bmWeb_mat',h=beam_shape.tw(),nDMaterial=ndWsteel)

#plate_mat=tm.DeckMaterialData(name='plate_mat',thickness=plateThck,material=steel_plate)
#plate_mat.setupElasticSection(prep)

plate1_mesh=fem.SurfSetToMesh(surfSet=plate1,matSect=plate_mat,elemSize=esize,elemType='ShellMITC4')
plate2_mesh=fem.SurfSetToMesh(surfSet=plate2,matSect=plate_mat,elemSize=esize,elemType='ShellMITC4')
bmFlange_mesh=fem.SurfSetToMesh(surfSet=flangeSet,matSect=bmFlange_mat,elemSize=esize,elemType='ShellMITC4')
bmWeb_mesh=fem.SurfSetToMesh(surfSet=beam.webSet,matSect=bmWeb_mat,elemSize=esize,elemType='ShellMITC4')

fem.multi_mesh(prep,[plate1_mesh,plate2_mesh,bmFlange_mesh,bmWeb_mesh])

#boundary conditions
beamSet=modelSpace.setSum('beamSet',[beam.flXnegSet,beam.flXposSet,beam.webSet])
beamSet.fillDownwards()
bound1=sets.get_set_nodes_plane_XY('bound1',beamSet,0)
bound2=sets.get_set_nodes_plane_XY('bound2',beamSet,L_beam)
for n in bound1.nodes:
    modelSpace.fixNode000_FFF(n.tag)
for n in bound2.nodes:
    modelSpace.fixNode000_FFF(n.tag)
out.displayFEMesh()


#Welds plate 1
weld_t=sc.WeldTyp(weldSz,weldMetal)
l1=geom.Segment3d(geom.Pos3d(x1,-yEdge,zPlt),geom.Pos3d(x2,-yEdge,zPlt))
l2=geom.Segment3d(geom.Pos3d(x1,yEdge,zPlt),geom.Pos3d(x2,yEdge,zPlt))
WFlg1Plt1=sc.MultiFilletWeld(weld_t,plate1,flangeSet,[l1],'WFlg1Plt1','welds plate 1 with flange 1')
WFlg1Plt1.generateWeld(nDiv=10,WS2sign=1,bothSidesOfWS1=True)
WFlg2Plt1=sc.MultiFilletWeld(weld_t,plate1,flangeSet,[l2],'WFlg2Plt1','welds plate 1 with flange 2')
WFlg2Plt1.generateWeld(nDiv=10,WS2sign=-1,bothSidesOfWS1=True)

l1=geom.Segment3d(geom.Pos3d(x1,-yEdge,zPlt),geom.Pos3d(x1,yEdge,zPlt))
WWebPlt1=sc.MultiFilletWeld(weld_t,plate1,beam.webSet,[l1],'WWebPlt1','weld plate 1 with web')
WWebPlt1.generateWeld(nDiv=15,WS2sign=1,bothSidesOfWS1=True)
weldsPlate1=[WFlg1Plt1,WFlg2Plt1,WWebPlt1]

#Welds plate 2
weld_t=sc.WeldTyp(weldSz,weldMetal)
l1=geom.Segment3d(geom.Pos3d(-x2,-yEdge,zPlt),geom.Pos3d(-x1,-yEdge,zPlt))
l2=geom.Segment3d(geom.Pos3d(-x2,yEdge,zPlt),geom.Pos3d(-x1,yEdge,zPlt))
WFlg1Plt2=sc.MultiFilletWeld(weld_t,plate2,flangeSet,[l1],'WFlg1Plt2','welds plate 2 with flange 1')
WFlg1Plt2.generateWeld(nDiv=10,WS2sign=1,bothSidesOfWS1=True)
WFlg2Plt2=sc.MultiFilletWeld(weld_t,plate2,flangeSet,[l2],'WFlg2Plt2','welds plate 2 with flange 2')
WFlg2Plt2.generateWeld(nDiv=10,WS2sign=-1,bothSidesOfWS1=True)
l1=geom.Segment3d(geom.Pos3d(-x1,-yEdge,zPlt),geom.Pos3d(-x1,yEdge,zPlt))
WWebPlt2=sc.MultiFilletWeld(weld_t,plate2,beam.webSet,[l1],'WWebPlt2','weld plate 2 with web')
WWebPlt2.generateWeld(nDiv=15,WS2sign=-1,bothSidesOfWS1=True)
out.displayFEMesh()
weldsPlate2=[WFlg1Plt2,WFlg2Plt2,WWebPlt2]

# Nodes bolts
nBoltsPlt1=[plate1.nodes.getNearestNode(geom.Pos3d(xBolt,-yBolt,zPlt)),
            plate1.nodes.getNearestNode(geom.Pos3d(xBolt,yBolt,zPlt))]
nBoltsPlt2=[plate2.nodes.getNearestNode(geom.Pos3d(-xBolt,-yBolt,zPlt)),
            plate2.nodes.getNearestNode(geom.Pos3d(-xBolt,yBolt,zPlt))]

loadPlt1= loads.NodalLoad('loadPlt1', nBoltsPlt1,xc.Vector([0,Vd/2,0,0,0,0]))
loadPlt2= loads.NodalLoad('loadPlt2', nBoltsPlt2,xc.Vector([0,Vd/2,0,0,0,0]))

LC1=lcases.LoadCase(preprocessor=prep,name="LC1",loadPType="default",timeSType="constant_ts")
LC1.create()
LC1.addLstLoads([loadPlt1])

LC2=lcases.LoadCase(preprocessor=prep,name="LC2",loadPType="default",timeSType="constant_ts")
LC2.create()
LC2.addLstLoads([loadPlt1,loadPlt2])

#ULSs=[['ULS01','1.0*LC1'],['ULS02','1.0*LC2']]
ULSs=['LC1','LC2']
welds2Check=weldsPlate1+weldsPlate2
welds2Check=weldsPlate2

#Checking
checksc.aisc_check_bolts_welds(modelSpace, ULSs=ULSs, boltSets2Check=[], welds2Check=welds2Check, baseMetal=steel_plate,meanShearProc=True, resFile='stair_tower_grating_beams_check', solutionProcedureType= predefined_solutions.SimpleStaticLinearUMF, warningsFile='warnings.tex')#foundSprings=None)#found.springs)

# Von mises verification

combContainer= combs.CombContainer()
for ULSnm in ULSs:
    combContainer.ULS.perm.add(str(ULSnm),'1.0*'+str(ULSnm))
combContainer.dumpCombinations(prep)

for e in beamSet.elements: e.setProp('yieldStress', steel_W.fy)
for e in plate1.elements: e.setProp('yieldStress', steel_plate.fy)
for e in plate2.elements: e.setProp('yieldStress', steel_plate.fy)

allShells=modelSpace.setSum('allShells',[beamSet,plate1,plate2])
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

out.displayField(limitStateLabel= limitState.label, section= None, argument= 'CF', component= None, setToDisplay= None, fileName= None)
