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

# import local modules
import sys
sys.path.insert(0, '../local_modules')
import steel_connection_models as sbcm

#  **** Data
steelW=ASTM_materials.A992   #steel support W shapes
steelPlate=ASTM_materials.A36   #steel shear plates
steelBolt=ASTM_materials.A325   
fiBolt=16e-3 # diameter of the bolts
boltFastener=ASTM_materials.BoltFastener(fiBolt,steelBolt)

columnShape=ASTM_materials.WShape(steelW,lb.getUSLabel('W360X110'))
col1_L=1  # lenght of beam to modelize
col1_vOrig=xc.Vector([0,0,0]) # global coordinates of the start point in the beam axis 
col1_angX=0  # angle of the beam axis with the global XZ plane
col1_angY=-90
col1_esize=0.015  # size of the elements
col1_idName='col1_' # id for naming sets

col2_L=0.5  # lenght of beam to modelize
col2_vOrig=xc.Vector([0,0,0]) # global coordinates of the start point in the beam axis 
col2_angX=0  # angle of the beam axis with the global XZ plane
col2_angY=90
col2_esize=0.015  # size of the elements
col2_idName='col2_' # id for naming sets

# Flange plates
flgPthk=16e-3  #thickness
flgP_W=210e-3   # width (horizontal)
flgP_H=470e-3  #height (vertical)
xCentflgP1=columnShape.h()/2+flgPthk/2 # global x-coordinate of the center (aux)
yCentflgP=0
zCentflgP=0
flgP1_vCentr=xc.Vector([xCentflgP1,yCentflgP,zCentflgP]) #center of end-plate 1 in global coordinates
xCentflgP2=-xCentflgP1
flgP2_vCentr=xc.Vector([xCentflgP2,yCentflgP,zCentflgP]) 
flgP_angX=90  # angle of the end-plates with the global XZ plane
flgP_esize=0.02 # size of the elements
flgP1_idName='ep1_'  # id for naming sets
flgP2_idName='ep2_'  # id for naming sets

# Web plate
webPthk=10e-3  #thickness
webP_W=170e-3   # width (horizontal)
webP_H=320e-3  #height (vertical)
webP_angX=0  #height (vertical)
xCentwebP=0 # global x-coordinate of the center (aux)
yCentwebP=columnShape.tw()/2+webPthk/2
zCentwebP=0
webP_vCentr=xc.Vector([xCentwebP,yCentwebP,zCentwebP]) #center of end-plate 1 in global coordinates
webP_idName='wp_'  # id for naming sets
webP_esize=0.02 # size of the elements

#Bolts flanges
dh_flB=75e-3 #distance between bolts in height direction
dw_flB=140e-3 #distance between bolts in width direction
d2midp=45e-3  # distance from the first row of bolts to the mid-plane

col1_flange_bolts=list()
for x in [-dw_flB/2,dw_flB/2]:
    for z in [-d2midp,-d2midp-dh_flB,-d2midp-2*dh_flB]:
        col1_flange_bolts.append([x,z])
col2_flange_bolts=list()
for x in [-dw_flB/2,dw_flB/2]:
    for z in [d2midp,d2midp+dh_flB,d2midp+2*dh_flB]:
        col2_flange_bolts.append([x,z])

flange_bolts=col1_flange_bolts+col2_flange_bolts

#Bolts web
dh_flB=75e-3 #distance between bolts in height direction
dw_flB=100e-3 #distance between bolts in width direction
d2midp=45e-3  # distance from the first row of bolts to the mid-plane

col1_web_bolts=list()
for x in [-dw_flB/2,dw_flB/2]:
    for z in [-d2midp,-d2midp-dh_flB]:
        col1_web_bolts.append([x,z])
col2_web_bolts=list()
for x in [-dw_flB/2,dw_flB/2]:
    for z in [d2midp,d2midp+dh_flB]:
        col2_web_bolts.append([x,z])

web_bolts=col1_web_bolts+col2_web_bolts

#loads in combination 0.9D+1.6Wy
Nax=69e3 # axial force  (Fz)
Mweak=9.1e3 # bending moment around weak axis (Mx) 
Mstrong=49e3 # bending moment around strong axis (My)
Qweb=18.2  # shear in web direction (Fx)
Qflang=10e3 #shear in flange direction (Fy)

#End data

#area_flange_plate=columnShape.getFlangeGrossArea()*steelW.fy/steelPlate.fy
#b_flange_plate=0.250
#thk_flange_plate=area_flange_plate/b_flange_plate

FEcase= xc.FEProblem()
#FEcase.title= title
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

column1=sbcm.Ibeam(columnShape,col1_L,col1_vOrig,col1_angX,col1_idName,rotY=col1_angY)
column1.genSurfaces(modelSpace)
column2=sbcm.Ibeam(columnShape,col2_L,col2_vOrig,col2_angX,col2_idName,rotY=col2_angY)
column2.genSurfaces(modelSpace)
flangePlate1=sbcm.rectFakeBoltedPlate(flgP_W,flgP_H,flgP1_vCentr,flgP_angX,flgP1_idName,lstXZBoltCoord=flange_bolts)#,boltCoord)
flangePlate1.genSurfaces(modelSpace)
flangePlate2=sbcm.rectFakeBoltedPlate(flgP_W,flgP_H,flgP2_vCentr,flgP_angX,flgP2_idName,lstXZBoltCoord=flange_bolts)#,boltCoord)                                 
flangePlate2.genSurfaces(modelSpace)
webPlate=sbcm.rectFakeBoltedPlate(webP_W,webP_H,webP_vCentr,webP_angX,webP_idName,lstXZBoltCoord=web_bolts)
webPlate.genSurfaces(modelSpace)
#out.displayBlocks()

# Materials for linear analysis vonmises verification
ndWsteel=tm.defElasticIsotropic3d(preprocessor=prep, name='ndWsteel', E=steelW.E, nu=steelW.nu, rho=steelW.rho)
ndPlateSteel=tm.defElasticIsotropic3d(preprocessor=prep, name='ndPlateSteel', E=steelPlate.E, nu=steelPlate.nu, rho=steelPlate.rho)


colFlangeMat=tm.defMembranePlateFiberSection(prep,name='colFlangeMat',h=columnShape.tf(),nDMaterial=ndWsteel)
colWebMat=tm.defMembranePlateFiberSection(prep,name='colWebMat',h=columnShape.tw(),nDMaterial=ndWsteel)
flgPmat=tm.defMembranePlateFiberSection(prep,name='flgPmat',h=flgPthk,nDMaterial=ndPlateSteel)
webPmat=tm.defMembranePlateFiberSection(prep,name='webPmat',h=webPthk,nDMaterial=ndPlateSteel)


column1.genMesh(modelSpace,colFlangeMat,colWebMat,col1_esize)
column1.fixEndExtr(modelSpace)
column2.genMesh(modelSpace,colFlangeMat,colWebMat,col2_esize)
flangePlate1.genMesh(modelSpace,flgPmat,flgP_esize)
flangePlate2.genMesh(modelSpace,flgPmat,flgP_esize)
webPlate.genMesh(modelSpace,webPmat,webP_esize)

#out.displayFEMesh()#setsToDisplay=[column1,column2])

col1Flanges=modelSpace.setSum('col1Flanges',[column1.bottFlange,column1.topFlange])
col2Flanges=modelSpace.setSum('col2Flanges',[column2.bottFlange,column2.topFlange])

setBolts=prep.getSets.defSet('setBolts')
bolt=sc.Bolt(fiBolt,steelBolt)

for coo in col1_flange_bolts:
    x=coo[0]
    z=coo[1]
    endA=flangePlate1.grid.getPntXYZ((x,0,z))
    endB=col1Flanges.nodes.getNearestNode(endA.pos)
    bolt.createBolt([endA,endB],'setBolts')
    endA=flangePlate2.grid.getPntXYZ((x,0,z))
    endB=col1Flanges.nodes.getNearestNode(endA.pos)
    bolt.createBolt([endA,endB],'setBolts')
    

for coo in col2_flange_bolts:
    x=coo[0]
    z=coo[1]
    endA=flangePlate1.grid.getPntXYZ((x,0,z))
    endB=col2Flanges.nodes.getNearestNode(endA.pos)
    bolt.createBolt([endA,endB],'setBolts')
    endA=flangePlate2.grid.getPntXYZ((x,0,z))
    endB=col2Flanges.nodes.getNearestNode(endA.pos)
    bolt.createBolt([endA,endB],'setBolts')

for coo in col1_web_bolts:
    x=coo[0]
    z=coo[1]
    endA=webPlate.grid.getPntXYZ((x,0,z))
    endB=column1.web.nodes.getNearestNode(endA.pos)
    bolt.createBolt([endA,endB],'setBolts')

for coo in col2_web_bolts:
    x=coo[0]
    z=coo[1]
    endA=webPlate.grid.getPntXYZ((x,0,z))
    endB=column2.web.nodes.getNearestNode(endA.pos)
    bolt.createBolt([endA,endB],'setBolts')

#out.displayFEMesh(setBolts)

pnt2load=column2.grid.getPntXYZ((col2_L,0,0))
node2load=pnt2load.getNode()
load1=loads.NodalLoad('load1',[node2load],xc.Vector([Qweb,Qflang,Nax,Mweak,Mstrong,0]))
LC1=lcases.LoadCase(preprocessor=prep,name="LC1",loadPType="default",timeSType="constant_ts")
LC1.create()
LC1.addLstLoads([load1])

modelSpace.addLoadCaseToDomain('LC1')                                   
out.displayLoads()
modelSpace.analyze()
out.displayDispRot('uZ')
out.displayDispRot('uX')
out.displayDispRot('uY')
ULSs=['LC1']

checksc.aisc_check_bolts_welds(modelSpace, ULSs=ULSs, boltSets2Check=[[setBolts,boltFastener]], welds2Check=[], baseMetal=steelPlate,meanShearProc=True, resFile='check', solutionProcedureType= predefined_solutions.SimpleStaticLinearUMF, warningsFile='warnings.tex')#foundSprings=No

# Von mises
combContainer= combs.CombContainer()
for ULSnm in ULSs:
    combContainer.ULS.perm.add(str(ULSnm),'1.0*'+str(ULSnm))
combContainer.dumpCombinations(prep)

column1.beam.description='Column low '+columnShape.getMetricName()
column2.beam.description='Column up '+columnShape.getMetricName()
flangePlate1.plate.description='Flange plate 1 '+ str(round(flgP_H*1000,0)) + 'x' +str(round(flgP_W*1000,0)) +  'x' +str(round(flgPthk*1000,0))
flangePlate2.plate.description='Flange plate 2 '+ str(round(flgP_H*1000,0)) + 'x' +str(round(flgP_W*1000,0)) +  'x' +str(round(flgPthk*1000,0))

webPlate.plate.description='Shear plate '+ str(round(webP_H*1000,0)) + 'x' +str(round(webP_W*1000,0)) +  'x' +str(round(webPthk*1000,0))
lstBeams=[column1.beam,column2.beam]
lstPlates=[flangePlate1.plate,flangePlate2.plate,webPlate.plate]

for st in lstBeams:
    for e in st.elements: e.setProp('yieldStress', steelW.fy)
for st in lstPlates:
    for e in st.elements: e.setProp('yieldStress', steelPlate.fy)


lstAllShells=lstBeams+lstPlates
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
for st in lstAllShells:
    out.displayField(limitStateLabel= limitState.label, section= None, argument= 'CF', component= None, setToDisplay= st, fileName= None)

