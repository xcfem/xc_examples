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

# import local modules
import sys
sys.path.insert(0, '../local_modules')
import steel_connection_models as sbcm


# Connection beam to beam with shear-plate and double end-plate
# Axis of the main beam (supporting beam) remains at global Z=0 

#  **** Data
weldMetal=ASTM_materials.E7018
steelW=ASTM_materials.A992   #steel support W shapes
steelPlate=ASTM_materials.A36   #steel shear plates
steelBolt=ASTM_materials.A325   
fiBolt=16e-3 # diameter of the bolts

boltFastener=ASTM_materials.BoltFastener(fiBolt,steelBolt)
#supporting beam data
mainBshape=ASTM_materials.WShape(steelW,lb.getUSLabel('W200X46.1'))
mainB_L=2  # lenght of beam to modelize
mainB_vOrig=xc.Vector([-mainB_L/2,0,0]) # global coordinates of the start point in the beam axis 
mainB_angX=0  # angle of the beam axis with the global XZ plane
mainB_esize=0.025  # size of the elements
mainB_idName='mb_' # id for naming sets

# End-plates data (end-plate 1 welded to shear-plate, end-plate 1 welded to supported beam)
endPthk=9e-3  #thickness
endP_W=0.15   # width (horizontal)
endP_H=mainBshape.h()  #height (vertical)
xCent=0 # global x-coordinate of the center (aux)
yCentEndP1=mainBshape.b()/2+endPthk/2 # global y-coordinate of the center (end-plate 1)
yCentEndP2=mainBshape.b()/2+3*endPthk/2# global y-coordinate of the center (end-plate 2)
zCent=0 # global y-coordinate of the center
endP1_vCentr=xc.Vector([xCent,yCentEndP1,zCent]) #center of end-plate 1 in global coordinates
endP2_vCentr=xc.Vector([xCent,yCentEndP2,zCent]) #center of end-plate 2 in global coordinates
endP_angX=0  # angle of the end-plates with the global XZ plane
endP_esize=0.025 # size of the elements
endP1_idName='ep1_'  # id for naming sets
endP2_idName='ep2_'  # id for naming sets

# secondary beam data
secBshape=ASTM_materials.WShape(steelW,lb.getUSLabel('W150X13.5'))
secB_L=0.1  # lenght of beam to modelize (small in order to apply loads at extremity)
ySecB=mainBshape.b()/2+2*endPthk
zSecB=mainBshape.h()/2-secBshape.h()/2 # z coordinate of the axis of the secondary beam. Top of beams flange in the same plan
secB_vOrig=xc.Vector([0,ySecB,zSecB]) # global coordinates of the start point in the beam axis 
secB_angX=90  # angle of the beam axis with the global XZ plane
secB_esize=0.025  # size of the elements
secB_idName='sb_' # id for naming sets

# Array of bolts in end-plates
boltDistX=100e-3  #aux
boltDistZ=60e-3 #aux
relZaxSecB=endP_H/2-secBshape.h()/2  # height of the center of the secondary beam relative to the center of the end-plate
# boltCoord: coordinates of the bolts in a relative coordinate system centered in
# the center of the base plate with 1st coord. horizontal and 2nd coord. vertical
boltCoord=[[-boltDistX/2,relZaxSecB+boltDistZ/2],
           [boltDistX/2,relZaxSecB+boltDistZ/2],
           [boltDistX/2,relZaxSecB-boltDistZ/2],
           [-boltDistX/2,relZaxSecB-boltDistZ/2]]
# Shear plate data
shPthk=10e-3 #thickness
shP_W=(mainBshape.b()-mainBshape.tw())/2 #width (horizontal)
shP_H=mainBshape.h()-2*mainBshape.tf() #height (vertical)
xCent=0 #aux
yCent=mainBshape.tw()/2+shP_W/2 #aux
zCent=0  #aux
shP_vCentr=xc.Vector([xCent,yCent,zCent]) #center of shear-plate 1 in global coordinates
shP_angX=90 # angle of the shear-plates with the global XZ plane
shP_esize=0.025 # size of the elements
shP_idName='sp_'  # id for naming sets
# Stiffener
stiff=True  # True if stiffener in prolongation of the shear plate
# Stiffener
stiff=True  # True if stiffener in prolongation of the shear plate
stfPthk=shPthk #thickness
stfP_W=shP_W #width (horizontal)
stfP_H=shP_H #height (vertical)
xCent=0 #aux
yCent=-mainBshape.tw()/2-stfP_W/2 #aux
zCent=0  #aux
stfP_vCentr=xc.Vector([xCent,yCent,zCent]) #center of shear-plate 1 in global coordinates
stfP_angX=-90 # angle of the shear-plates with the global XZ plane
stfP_esize=0.02 # size of the elements
stfP_idName='stf_'  # id for naming sets
#
N=17.6e3  #design axial force in the supported beam (+ tension)
V=21.3e3  #shear force
Mz=2e3     #bending moment around strong axis
My=0 # bending moment around weak axis

loadTriples=[[N,V,Mz,My]] # maximum 4 load cases

# Welds data
weld_mainBfl_shP=sc.WeldTyp(6e-3,weldMetal) # weld flanges of main-beam to shear-plate
weld_mainBwb_shP=sc.WeldTyp(6e-3,weldMetal) # weld web of main-beam to shear-plate
weld_shP_endP=sc.WeldTyp(6e-3,weldMetal) # weld shear-plate to end-plate
weld_secBtopfl_endP=sc.WeldTyp(6e-3,weldMetal) # weld top-flange of second-beam to end-plate
weld_secBbotfl_endP=sc.WeldTyp(6e-3,weldMetal) # weld bottom-flange of second-beam to end-plate
weld_secBwb_endP=sc.WeldTyp(6e-3,weldMetal) # weld web of second-beam to end-plate
weldShP2bottomFl=True # True if shear plate is welded to the bottom flange of the main beam
weldUpFlang2endPBoth=False # True if top flange of the beam is welded to the end plate also in the upper side
#  ****  end data ***


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

mainBeam=sbcm.Ibeam(mainBshape,mainB_L,mainB_vOrig,mainB_angX,mainB_idName)
mainBeam.genSurfaces(modelSpace)
secondBeam=sbcm.Ibeam(secBshape,secB_L,secB_vOrig,secB_angX,secB_idName)
secondBeam.genSurfaces(modelSpace)
shearPlate=sbcm.rectWeldPlate(shP_W,shP_H,shP_vCentr,shP_angX,shP_idName)
shearPlate.genSurfaces(modelSpace)
endPlate1=sbcm.rectFakeBoltedPlate(endP_W,endP_H,endP1_vCentr,endP_angX,endP1_idName,boltCoord)
endPlate1.genSurfaces(modelSpace)
endPlate2=sbcm.rectFakeBoltedPlate(endP_W,endP_H,endP2_vCentr,endP_angX,endP2_idName,boltCoord)
endPlate2.genSurfaces(modelSpace)
if stiff:
    stiffPlate=sbcm.rectWeldPlate(stfP_W,stfP_H,stfP_vCentr,stfP_angX,stfP_idName)
    stiffPlate.genSurfaces(modelSpace)


#out.displayBlocks()#mainBeam.web)

# Materials for linear analysis vonmises verification
ndWsteel=tm.defElasticIsotropic3d(preprocessor=prep, name='ndWsteel', E=steelW.E, nu=steelW.nu, rho=steelW.rho)
ndPlateSteel=tm.defElasticIsotropic3d(preprocessor=prep, name='ndPlateSteel', E=steelPlate.E, nu=steelPlate.nu, rho=steelPlate.rho)


mainBflangeMat=tm.defMembranePlateFiberSection(prep,name='mainBflangeMat',h=mainBshape.tf(),nDMaterial=ndWsteel)
mainBwebMat=tm.defMembranePlateFiberSection(prep,name='mainBwebMat',h=mainBshape.tw(),nDMaterial=ndWsteel)

secBflangeMat=tm.defMembranePlateFiberSection(prep,name='secBflangeMat',h=secBshape.tf(),nDMaterial=ndWsteel)
secBwebMat=tm.defMembranePlateFiberSection(prep,name='secBwebMat',h=secBshape.tw(),nDMaterial=ndWsteel)
shearPmat=tm.defMembranePlateFiberSection(prep,name='shearPmat',h=shPthk,nDMaterial=ndPlateSteel)
endPmat=tm.defMembranePlateFiberSection(prep,name='endPmat',h=endPthk,nDMaterial=ndPlateSteel)

mainBeam.genMesh(modelSpace,mainBflangeMat,mainBwebMat,mainB_esize)
mainBeam.fixBothExtr(modelSpace)
secondBeam.genMesh(modelSpace,secBflangeMat,secBwebMat,secB_esize)
shearPlate.genMesh(modelSpace,shearPmat,shP_esize)
endPlate1.genMesh(modelSpace,endPmat,endP_esize)
endPlate2.genMesh(modelSpace,endPmat,endP_esize)
if stiff:
    stiffPmat=tm.defMembranePlateFiberSection(prep,name='stiffPmat',h=stfPthk,nDMaterial=ndPlateSteel)
    stiffPlate.genMesh(modelSpace,stiffPmat,stfP_esize)
out.displayFEMesh()#endPlate1.plate)

W1=shearPlate.genWeldTopEdge(weldType=weld_mainBfl_shP,toSet=mainBeam.topFlange,weldSetName='W1',toSetSign=-1,bothSides=True,weldDescrip='Weld shear plate to main beam top flange')
W3=shearPlate.genWeldLeftEdge(weldType=weld_mainBwb_shP,toSet=mainBeam.web,weldSetName='W3',toSetSign=1,bothSides=True,weldDescrip='Weld shear plate to main beam web')
W4=shearPlate.genWeldRightEdge(weldType=weld_shP_endP,toSet=endPlate1.plate,weldSetName='W4',toSetSign=-1,bothSides=True,weldDescrip='Weld shear plate to end plate')
W5=secondBeam.genWeldTopFlangeInitExtr(weldType=weld_secBtopfl_endP,toSet=endPlate2.plate,weldSetName='W5',toSetSign=1,bothSides=weldUpFlang2endPBoth,weldDescrip='Weld supported beam top flange to end plate',plateSign=-1)
W6=secondBeam.genWeldBottFlangeInitExtr(weldType=weld_secBbotfl_endP,toSet=endPlate2.plate,weldSetName='W6',toSetSign=1,bothSides=True,weldDescrip='Weld supported beam bottom flange to end plate')
W7=secondBeam.genWeldWebInitExtr(weldType=weld_secBwb_endP,toSet=endPlate2.plate,weldSetName='W7',toSetSign=1,bothSides=True,weldDescrip='Weld supported beam web to end plate')

lstWelds2check=[W1,W3,W4,W5,W6,W7]
if weldShP2bottomFl:
    W2=shearPlate.genWeldBottomEdge(weldType=weld_mainBfl_shP,toSet=mainBeam.bottFlange,weldSetName='W2',toSetSign=1,bothSides=True,weldDescrip='Weld shear plate to main beam bottom flange')
    lstWelds2check.insert(1,W2)
if stiff:
    W8=stiffPlate.genWeldTopEdge(weldType=weld_mainBfl_shP,toSet=mainBeam.topFlange,weldSetName='W8',toSetSign=-1,bothSides=True,weldDescrip='Weld stiffener to main beam top flange')
    W9=stiffPlate.genWeldLeftEdge(weldType=weld_mainBwb_shP,toSet=mainBeam.web,weldSetName='W9',toSetSign=-1,bothSides=True,weldDescrip='Weld stiffener to main beam web')
    lstWelds2check+=[W8,W9]
    if weldShP2bottomFl:
        W10=stiffPlate.genWeldBottomEdge(weldType=weld_mainBfl_shP,toSet=mainBeam.bottFlange,weldSetName='W10',toSetSign=1,bothSides=True,weldDescrip='Weld stiffener to main beam bottom flange')
        lstWelds2check+=[W10]
    
out.displayFEMesh()#endPlate1.plate)

#Bolts
setBolts=prep.getSets.defSet('setBolts')
bolt=sc.Bolt(fiBolt,steelBolt)
for coo in boltCoord:
    x=coo[0]
    z=coo[1]
    endA=endPlate1.grid.getPntXYZ((x,0,z))
    endB=endPlate2.grid.getPntXYZ((x,0,z))
    bolt.createBolt([endA,endB],'setBolts')

#out.displayFEMesh()

pnt2load=secondBeam.grid.getPntXYZ((mainB_L,0,0))
node2load=pnt2load.getNode()

load1=loads.NodalLoad('load1',[node2load],xc.Vector([0,loadTriples[0][0],loadTriples[0][1],loadTriples[0][2],0,loadTriples[0][3]]))
LC1=lcases.LoadCase(preprocessor=prep,name="LC1",loadPType="default",timeSType="constant_ts")
LC1.create()
LC1.addLstLoads([load1])

modelSpace.addLoadCaseToDomain('LC1')                                   
out.displayLoads()
modelSpace.analyze()
out.displayDispRot('uZ')
out.displayDispRot('uX')
out.displayDispRot('uY')
modelSpace.removeAllLoadPatternsFromDomain()
ULSs=['LC1']

if len(loadTriples)>1:
    i=1
    load2=loads.NodalLoad('load2',[node2load],xc.Vector([0,loadTriples[i][0],loadTriples[i][1],loadTriples[i][2],0,0]))
    LC2=lcases.LoadCase(preprocessor=prep,name="LC2",loadPType="default",timeSType="constant_ts")
    LC2.create()
    LC2.addLstLoads([load2])
    ULSs.append('LC2')
if len(loadTriples)>2:
    i=2
    load3=loads.NodalLoad('load3',[node2load],xc.Vector([0,loadTriples[i][0],loadTriples[i][1],loadTriples[i][2],0,0]))
    LC3=lcases.LoadCase(preprocessor=prep,name="LC3",loadPType="default",timeSType="constant_ts")
    LC3.create()
    LC3.addLstLoads([load3])
    ULSs.append('LC3')    
if len(loadTriples)>3:
    i=3
    load4=loads.NodalLoad('load4',[node2load],xc.Vector([0,loadTriples[i][0],loadTriples[i][1],loadTriples[i][2],0,0]))
    LC4=lcases.LoadCase(preprocessor=prep,name="LC4",loadPType="default",timeSType="constant_ts")
    LC4.create()
    LC4.addLstLoads([load4])
    ULSs.append('LC4')    


checksc.aisc_check_bolts_welds(modelSpace, ULSs=ULSs, boltSets2Check=[[setBolts,boltFastener]], welds2Check=lstWelds2check, baseMetal=steelPlate,meanShearProc=True, resFile='check', solutionProcedureType= predefined_solutions.SimpleStaticLinearUMF,  reactionCheckTolerance=1e-3,warningsFile='warnings.tex')#foundSprings=No

# Von mises
combContainer= combs.CombContainer()
for ULSnm in ULSs:
    combContainer.ULS.perm.add(str(ULSnm),'1.0*'+str(ULSnm))
combContainer.dumpCombinations(prep)

mainBeam.beam.description='Main beam '+mainBshape.getMetricName()
secondBeam.beam.description= 'Secondary beam '+secBshape.getMetricName()
shearPlate.plate.description='Shear plate '+ str(round(shP_H*1000,0)) + 'x' +str(round(shP_W*1000,0)) +  'x' +str(round(shPthk*1000,0))
endPlate1.plate.description='End plate welded to shear plate '+ str(round(endP_H*1000,0)) + 'x' +str(round(endP_W*1000,0)) +  'x' +str(round(endPthk*1000,0))
endPlate2.plate.description='End plate welded to beam '+ str(round(endP_H*1000,0)) + 'x' +str(round(endP_W*1000,0)) +  'x' +str(round(endPthk*1000,0))
if stiff:
    stiffPlate.plate.description='Stiffener '+ str(round(stfP_H*1000,0)) + 'x' +str(round(stfP_W*1000,0)) +  'x' +str(round(stfPthk*1000,0))
lstBeams=[mainBeam.beam,secondBeam.beam]
lstPlates=[shearPlate.plate,endPlate1.plate,endPlate2.plate]
if stiff: lstPlates.append(stiffPlate.plate)
for st in lstBeams:
    for e in st.elements: e.setProp('yieldStress', steelW.fy)
for st in lstPlates:
    for e in st.elements: e.setProp('yieldStress', steelPlate.fy)

lstAllShells=lstBeams+lstPlates
allShells=modelSpace.setSum('allShells',lstAllShells)
setCalc=allShells

cfg= default_config.EnvConfig(language='en', resultsPath= 'tmp_results/', intForcPath= 'internalForces/',verifPath= 'verifications/',reportPath='./',reportResultsPath= 'annex/',grWidth='120mm')
cfg.projectDirTree.workingDirectory='./'
lsd.LimitStateData.setEnvConfig(cfg)
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

