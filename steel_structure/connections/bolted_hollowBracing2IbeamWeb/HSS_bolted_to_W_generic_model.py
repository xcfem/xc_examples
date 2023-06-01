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
steelHSS=ASTM_materials.A500
steelPlate=ASTM_materials.A36   #steel shear plates
steelBolt=ASTM_materials.A325   
fiBolt=30e-3 # diameter of the bolts

boltFastener=ASTM_materials.BoltFastener(fiBolt,steelBolt)
#supporting beam data
mainBshape=ASTM_materials.WShape(steelW,lb.getUSLabel('W360X216'))
mainB_L=2  # lenght of beam to modelize
mainB_vOrig=xc.Vector([-mainB_L/2,0,0]) # global coordinates of the start point in the beam axis 
mainB_angX=0  # angle of the beam axis with the global XZ plane
mainB_esize=0.02  # size of the elements
mainB_idName='mb_' # id for naming sets

# End-plate data 
endPthk=30e-3  #thickness
#endP_W=0.19   # width (horizontal)
endP_W=580e-3   # width (horizontal)

endP_H=180e-3  #height (vertical)
xCent=0 # global x-coordinate of the center (aux)
yCentEndP=mainBshape.tw()/2+endPthk/2 # global y-coordinate of the center (end-plate 1)
zCent=0 # global y-coordinate of the center
endP_vCentr=xc.Vector([xCent,yCentEndP,zCent]) #center of end-plate in global coordinates
endP_angX=0  # angle of the end-plates with the global XZ plane
endP_esize=0.02 # size of the elements
endP_idName='ep_'  # id for naming sets

# diagonal data
diagshape=ASTM_materials.HSSShape(steelHSS,lb.getUSLabel('HSS101.6X101.6X7.9'))
diag_L=0.4  # lenght of beam to modelize (small in order to apply loads at extremity)
ySecB=mainBshape.tw()/2+endPthk
zSecB=0 # z coordinate of the axis of the secondary beam. Top of beams flange in the same plan
diag_vOrig=xc.Vector([0,ySecB,zSecB]) # global coordinates of the start point in the beam axis 
diag_angX=29  # angle of the beam axis with the global XZ plane
diag_esize=0.02  # size of the elements
diag_idName='sb_' # id for naming sets

# Array of bolts in end-plate
#boltDistX=140e-3  #aux
boltDistX1=250e-3 #distance to center
boltDistX2=150e-3  #aux
boltDistX3=240e-3  #aux

#boltDistZ=90e-3 #aux
boltDistZ=50e-3
relZaxSecB=0  # height of the center of the secondary beam relative to the center of the end-plate
# boltCoord: coordinates of the bolts in a relative coordinate system centered in
# the center of the base plate with 1st coord. horizontal and 2nd coord. vertical
boltCoord=[[-boltDistX1,relZaxSecB+boltDistZ],
           [-boltDistX1,relZaxSecB-boltDistZ],
           [-boltDistX2,relZaxSecB+boltDistZ],
           [-boltDistX2,relZaxSecB-boltDistZ],
           [boltDistX3,relZaxSecB+boltDistZ],
           [boltDistX3,relZaxSecB-boltDistZ]
]
# boltCoordMbeam= coordinates of the bolts in the beam relative coordinate
# system with origin in the start of the beam, 1st coordinate horizontal 
# and 2nd coord. vertical
boltCoordMbeam=list()
for b in boltCoord:
    boltCoordMbeam.append([b[0]+mainB_L/2,0,b[1]])
#
N=591e3  #design axial force in the diagonal

# Welds data
weld_diag_endP=sc.WeldTyp(10e-3,weldMetal) # weld HSS to end-plate


#  ****  end data ***
gf.print_bolt_dim(fiBolt,steelBolt)

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

mainBeam=sbcm.Ibeam(mainBshape,mainB_L,mainB_vOrig,mainB_angX,mainB_idName,lstXYZBoltCoord=boltCoordMbeam)
mainBeam.genSurfaces(modelSpace)
diagonal=sbcm.HSSmember(diagshape,diag_L,diag_vOrig,diag_angX,diag_idName,bevelWidth=True)
diagonal.genSurfaces(modelSpace)
endPlate=sbcm.rectFakeBoltedPlate(endP_W,endP_H,endP_vCentr,endP_angX,endP_idName,boltCoord)
endPlate.genSurfaces(modelSpace)


#out.displayBlocks()#mainBeam.web)

# Materials for linear analysis vonmises verification
ndWsteel=tm.defElasticIsotropic3d(preprocessor=prep, name='ndWsteel', E=steelW.E, nu=steelW.nu, rho=steelW.rho)
ndHSSsteel=tm.defElasticIsotropic3d(preprocessor=prep, name='ndHSSsteel', E=steelHSS.E, nu=steelHSS.nu, rho=steelHSS.rho)
ndPlateSteel=tm.defElasticIsotropic3d(preprocessor=prep, name='ndPlateSteel', E=steelPlate.E, nu=steelPlate.nu, rho=steelPlate.rho)

mainBflangeMat=tm.defMembranePlateFiberSection(prep,name='mainBflangeMat',h=mainBshape.tf(),nDMaterial=ndWsteel)
mainBwebMat=tm.defMembranePlateFiberSection(prep,name='mainBwebMat',h=mainBshape.tw(),nDMaterial=ndWsteel)
diagMat=tm.defMembranePlateFiberSection(prep,name='diagMat',h=diagshape.t(),nDMaterial=ndHSSsteel)
endPmat=tm.defMembranePlateFiberSection(prep,name='endPmat',h=endPthk,nDMaterial=ndPlateSteel)

mainBeam.genMesh(modelSpace,mainBflangeMat,mainBwebMat,mainB_esize)
mainBeam.fixBothExtr(modelSpace)
diagonal.genMesh(modelSpace,diagMat,diag_esize)
endPlate.genMesh(modelSpace,endPmat,endP_esize)

W1=diagonal.genWeldTopInitExtr(weldType=weld_diag_endP,toSet=endPlate.plate,weldSetName='W1',toSetSign=1,weldDescrip='Weld top edge of diagonal to end plate')
W2=diagonal.genWeldBottInitExtr(weldType=weld_diag_endP,toSet=endPlate.plate,weldSetName='W2',toSetSign=1,weldDescrip='Weld bottom edge of diagonal to end plate')
W3=diagonal.genWeldLeftInitExtr(weldType=weld_diag_endP,toSet=endPlate.plate,weldSetName='W3',toSetSign=1,weldDescrip='Weld left edge of diagonal to end plate')
W4=diagonal.genWeldRightInitExtr(weldType=weld_diag_endP,toSet=endPlate.plate,weldSetName='W4',toSetSign=1,weldDescrip='Weld right edge of diagonal to end plate')

out.displayFEMesh([mainBeam.beam,diagonal.member])

lstWelds2check=[W1,W2,W3,W4]

#Bolts

setBolts=prep.getSets.defSet('setBolts')
bolt=sc.Bolt(fiBolt,steelBolt)
for l in boltCoord:
    l.insert(1,0) 
matchCoor=zip(boltCoord,boltCoordMbeam)
for coo in list(matchCoor):
    x=coo[0][0] ;  z=coo[0][2]
    print('x1=',x,'z1=',z)
    endA=endPlate.grid.getPntXYZ((x,0,z))
    x=coo[1][0] ; z=coo[1][2]
    print('x2=',x,'z2=',z)
    endB=mainBeam.grid.getPntXYZ((x,0,z))
    bolt.createBolt([endA,endB],'setBolts')

out.displayFEMesh()
out.displayFEMesh(setBolts)

pntsload=[diagonal.grid.getPntXYZ((mainB_L,-diagshape.b()/2,-diagshape.h()/2)),
          diagonal.grid.getPntXYZ((mainB_L,-diagshape.b()/2,diagshape.h()/2)),
          diagonal.grid.getPntXYZ((mainB_L,diagshape.b()/2,-diagshape.h()/2)),
          diagonal.grid.getPntXYZ((mainB_L,diagshape.b()/2,diagshape.h()/2)),
]
nodesload=[p.getNode() for p in pntsload]
nn=len(nodesload)
alpha=math.radians(diag_angX)
load=loads.NodalLoad('load1',nodesload,xc.Vector([N*math.cos(alpha)/nn,N*math.sin(alpha)/nn,0,0,0,0]))
LC1=lcases.LoadCase(preprocessor=prep,name="LC1",loadPType="default",timeSType="constant_ts")
LC1.create()
LC1.addLstLoads([load])

modelSpace.addLoadCaseToDomain('LC1')                                   
out.displayLoads()
modelSpace.analyze()
out.displayDispRot('uZ')
modelSpace.removeAllLoadPatternsFromDomain()
ULSs=['LC1']

    
checksc.aisc_check_bolts_welds(modelSpace, ULSs=ULSs, boltSets2Check=[[setBolts,boltFastener]], welds2Check=lstWelds2check, baseMetal=steelPlate,meanShearProc=True, resFile='check', solutionProcedureType= predefined_solutions.SimpleStaticLinearUMF, warningsFile='warnings.tex')#foundSprings=No

# Von mises
combContainer= combs.CombContainer()
for ULSnm in ULSs:
    combContainer.ULS.perm.add(str(ULSnm),'1.0*'+str(ULSnm))
combContainer.dumpCombinations(prep)
mainBeam.beam.description='Main beam '+mainBshape.getMetricName()
diagonal.member.description='Diagonal '+diagshape.getMetricName()
endPlate.plate.description='End plate welded to diagonal '+ str(round(endP_H*1000,0)) + 'x' +str(round(endP_W*1000,0)) +  'x' +str(round(endPthk*1000,0))

lstBeams=[mainBeam.beam]
lstDiag=[diagonal.member]
lstPlates=[endPlate.plate]
for st in lstBeams:
    for e in st.elements: e.setProp('yieldStress', steelW.fy)
for st in lstDiag:
    for e in st.elements: e.setProp('yieldStress', steelHSS.fy)
for st in lstPlates:
    for e in st.elements: e.setProp('yieldStress', steelPlate.fy)

lstAllShells=lstBeams+lstDiag+lstPlates
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

