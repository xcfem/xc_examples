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
import gen_functions as gf


# Connection beam to beam in angle with end-plate
# Axis of the main beam (supporting beam) remains at global Z=0 

#  **** Data
weldMetal=ASTM_materials.E7018
steelW=ASTM_materials.A992   #steel support W shapes
#column
colshape=ASTM_materials.WShape(steelW,lb.getUSLabel('W200X26.6'))
col_L=2  # lenght of beam to modelize
col_vOrig=xc.Vector([-col_L/2,0,0]) # global coordinates of the start point in the beam axis 
col_angX=0  # angle of the beam axis with the global XZ plane
col_esize=0.02  # size of the elements
col_idName='col_' # id for naming sets

#beam
beamshape=ASTM_materials.WShape(steelW,lb.getUSLabel('W150X13.5'))
beam_L=0.1  # lenght of beam to modelize (small in order to apply loads at extremity)
ySecB=colshape.h()/2
zSecB=0 # z coordinate of the axis of the secondary beam. Top of beams flange in the same plan
beam_vOrig=xc.Vector([0,ySecB,zSecB]) # global coordinates of the start point in the beam axis 
beam_angX=90  # angle of the beam axis with the global XZ plane
beam_esize=0.02  # size of the elements
beam_idName='sb_' # id for naming sets

N=0  #design axial force in the supported beam (+ tension)
V=29.2e3  #shear force
M=-10.4e3#-V*secB_L    #bending moment (vertical)

# Welds data
weld_beam_col=sc.WeldTyp(5e-3,weldMetal) # weld beam to flange of column

#end data
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

column=sbcm.Ibeam(colshape,col_L,col_vOrig,col_angX,col_idName,rotX=90)
column.genSurfaces(modelSpace)
beam=sbcm.Ibeam(beamshape,beam_L,beam_vOrig,beam_angX,beam_idName,rotX=90)
beam.genSurfaces(modelSpace)
# Materials for linear analysis vonmises verification
ndWsteel=tm.defElasticIsotropic3d(preprocessor=prep, name='ndWsteel', E=steelW.E, nu=steelW.nu, rho=steelW.rho)

colflangeMat=tm.defMembranePlateFiberSection(prep,name='colflangeMat',h=colshape.tf(),nDMaterial=ndWsteel)
colwebMat=tm.defMembranePlateFiberSection(prep,name='colwebMat',h=colshape.tw(),nDMaterial=ndWsteel)

beamflangeMat=tm.defMembranePlateFiberSection(prep,name='beamflangeMat',h=beamshape.tf(),nDMaterial=ndWsteel)
beamwebMat=tm.defMembranePlateFiberSection(prep,name='beamwebMat',h=beamshape.tw(),nDMaterial=ndWsteel)

column.genMesh(modelSpace,colflangeMat,colwebMat,col_esize)
column.fixBothExtr(modelSpace)
beam.genMesh(modelSpace,beamflangeMat,beamwebMat,beam_esize)


W1=beam.genWeldTopFlangeInitExtr(weldType=weld_beam_col,toSet=column.bottFlange,weldSetName='W1',toSetSign=-1,bothSides=True,weldDescrip='Weld beam top flange to column')
W2=beam.genWeldBottFlangeInitExtr(weldType=weld_beam_col,toSet=column.bottFlange,weldSetName='W2',toSetSign=1,bothSides=True,weldDescrip='Weld sbeam bottom flange to column')
W3=beam.genWeldWebInitExtr(weldType=weld_beam_col,toSet=column.bottFlange,weldSetName='W3',toSetSign=1,bothSides=True,weldDescrip='Weld beam web to column')

lstWelds2check=[W1,W2,W3]
out.displayFEMesh()

pnt2load=beam.grid.getPntXYZ((beam_L,0,0))
node2load=pnt2load.getNode()
load1=loads.NodalLoad('load1',[node2load],xc.Vector([V,N,0,0,0,M]))
LC1=lcases.LoadCase(preprocessor=prep,name="LC1",loadPType="default",timeSType="constant_ts")
LC1.create()
LC1.addLstLoads([load1])

modelSpace.addLoadCaseToDomain('LC1')                                   
out.displayLoads()
modelSpace.analyze()
out.displayDispRot('uZ')
modelSpace.removeAllLoadPatternsFromDomain()
ULSs=['LC1']
checksc.aisc_check_bolts_welds(modelSpace, ULSs=ULSs, boltSets2Check=[], welds2Check=lstWelds2check, baseMetal=steelW,meanShearProc=True, resFile='check', solutionProcedureType= predefined_solutions.SimpleStaticLinearUMF, reactionCheckTolerance=1e-3,warningsFile='warnings.tex')#foundSprings=No

# Von mises
combContainer= combs.CombContainer()
for ULSnm in ULSs:
    combContainer.ULS.perm.add(str(ULSnm),'1.0*'+str(ULSnm))
combContainer.dumpCombinations(prep)

lstBeams=[column.beam,beam.beam]
for st in lstBeams:
    for e in st.elements: e.setProp('yieldStress', steelW.fy)

lstAllShells=lstBeams
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

