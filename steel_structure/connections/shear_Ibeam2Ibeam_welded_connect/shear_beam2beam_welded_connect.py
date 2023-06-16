# -*- coding: utf-8 -*-
from __future__ import division 
from __future__ import print_function


import geom
import xc
import math

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
mainBshape=ASTM_materials.WShape(steelW,lb.getUSLabel('W310X97'))
mainB_L=2  # lenght of beam to modelize
mainB_vOrig=xc.Vector([-mainB_L/2,0,0]) # global coordinates of the start point in the beam axis 
mainB_angX=0  # angle of the beam axis with the global XZ plane
mainB_esize=0.025  # size of the elements
mainB_idName='mb_' # id for naming sets


# secondary beam data
secBshape=ASTM_materials.WShape(steelW,lb.getUSLabel('W310X97'))
secB_L=0.6  # lenght of beam to modelize (small in order to apply loads at extremity)
ySecB=mainBshape.tw()/2
zSecB=mainBshape.h()/2-secBshape.h()/2 # z coordinate of the axis of the secondary beam. Top of beams flange in the same plan
secB_vOrig=xc.Vector([0,ySecB,zSecB]) # global coordinates of the start point in the beam axis 
secB_angX=90  # angle of the beam axis with the global XZ plane
secB_esize=0.025  # size of the elements
secB_idName='sb_' # id for naming sets


# Welds data
weld_web2web=sc.WeldTyp(6e-3,weldMetal) # weld flanges of main-beam to shear-plate

stiff=False
# Loads in global coordinate system
N=-14e3
V=-100e3
M=-V*secB_L
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
secondBeam=sbcm.Ibeam(secBshape,secB_L,secB_vOrig,secB_angX,secB_idName,topNotch=True,bottNotch=True,notchDim=[.168,.036])
secondBeam.genSurfaces(modelSpace)
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

mainBeam.genMesh(modelSpace,mainBflangeMat,mainBwebMat,mainB_esize)
mainBeam.fixBothExtr(modelSpace)
secondBeam.genMesh(modelSpace,secBflangeMat,secBwebMat,secB_esize)
if stiff:
    stiffPmat=tm.defMembranePlateFiberSection(prep,name='stiffPmat',h=stfPthk,nDMaterial=ndPlateSteel)
    stiffPlate.genMesh(modelSpace,stiffPmat,stfP_esize)

out.displayFEMesh()

W1=secondBeam.genWeldWebInitExtr(weldType=weld_web2web,toSet=mainBeam.web,weldSetName='W1',toSetSign=1,bothSides=True,weldDescrip='Weld web to web')

lstWelds2check=[W1]
if stiff:
    W8=stiffPlate.genWeldTopEdge(weldType=weld_mainBfl_shP,toSet=mainBeam.topFlange,weldSetName='W8',toSetSign=-1,bothSides=True,weldDescrip='Weld stiffener to main beam top flange')
    W9=stiffPlate.genWeldLeftEdge(weldType=weld_mainBwb_shP,toSet=mainBeam.web,weldSetName='W9',toSetSign=-1,bothSides=True,weldDescrip='Weld stiffener to main beam web')
    lstWelds2check+=[W8,W9]
    if weldShP2bottomFl:
        W10=stiffPlate.genWeldBottomEdge(weldType=weld_mainBfl_shP,toSet=mainBeam.bottFlange,weldSetName='W10',toSetSign=1,bothSides=True,weldDescrip='Weld stiffener to main beam bottom flange')
        lstWelds2check+=[W10]
out.displayFEMesh()#endPlate1.plate)


pnt2load=secondBeam.grid.getPntXYZ((mainB_L,0,0))
node2load=pnt2load.getNode()

load1=loads.NodalLoad('load1',[node2load],xc.Vector([0,N,V,M,0,0]))
LC1=lcases.LoadCase(preprocessor=prep,name="LC1",loadPType="default",timeSType="constant_ts")
LC1.create()
LC1.addLstLoads([load1])

modelSpace.addLoadCaseToDomain('LC1')                                   
out.displayLoads()
modelSpace.analyze()
out.displayDispRot('uZ')
modelSpace.removeAllLoadPatternsFromDomain()
ULSs=['LC1']

from solution import predefined_solutions

checksc.aisc_check_bolts_welds(modelSpace, ULSs=ULSs, boltSets2Check=[], welds2Check=lstWelds2check, baseMetal=steelPlate,meanShearProc=True, resFile='check', solutionProcedureType= predefined_solutions.SimpleStaticLinearUMF, reactionCheckTolerance=1e-3,warningsFile='warnings.tex')#foundSprings=No

# Von mises
combContainer= combs.CombContainer()
for ULSnm in ULSs:
    combContainer.ULS.perm.add(str(ULSnm),'1.0*'+str(ULSnm))
combContainer.dumpCombinations(prep)

lstBeams=[mainBeam.beam,secondBeam.beam]
lstPlates=[]
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

