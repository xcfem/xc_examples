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
steelPlate=ASTM_materials.A36   #steel shear plates
steelHSS=ASTM_materials.A500
steelBolt=ASTM_materials.A325   
fiBolt=24e-3 # diameter of the bolts

boltFastener=ASTM_materials.BoltFastener(fiBolt,steelBolt)
beamshape=ASTM_materials.WShape(steelW,lb.getUSLabel('W310X97'))
endPthk=25e-3  #end-plate thickness

#supporting beam data
gap_col_to_weld=0.02
colLowshape=ASTM_materials.HSSShape(steelHSS,lb.getUSLabel('HSS304.8X304.8X12.7'))
colUpshape=ASTM_materials.HSSShape(steelHSS,lb.getUSLabel('HSS304.8X304.8X19'))
colLow_L=2  # lenght of column to modelize
colLow_zCent=-beamshape.h()/2-2*endPthk-gap_col_to_weld
colLow_vOrig=xc.Vector([0,0,colLow_zCent]) # global coordinates of the start point in the column
col_angX=0  # angle of the beam axis with the global XZ plane
col_esize=0.02  # size of the elements
colLow_idName='colLow_' # id for naming sets
colUp_L=beamshape.h()+2*gap_col_to_weld
colUp_vOrig=xc.Vector([0,0,colUp_L/2]) # global coordinates of the start poi
colUp_idName='colUp_' # id for naming sets
# End-plate data 
#endPthk=10e-3  #thickness
#endP_W=0.19   # width (horizontal)
endP_W=0.48   # width (horizontal)
endP_H=0.48  #height (vertical)
endPlow_zCent=colLow_zCent+0.5*endPthk
endPlow_vCentr=xc.Vector([0,0,endPlow_zCent]) #center of end-plate 1 in global coordinates
endPup_zCent=colLow_zCent+1.5*endPthk
endPup_vCentr=xc.Vector([0,0,endPup_zCent]) #center of end-plate 1 in global coordinates
endP_angX=0  # angle of the end-plates with the global XZ plane
endP_esize=0.02 # size of the elements
endPup_idName='epUp_'  # id for naming sets
endPlow_idName='epLow_'  # id for naming sets

# beams
beam_L=0.4  # lenght of beam to modelize (small in order to apply loads at extremity)
xbeamX=colUpshape.h()/2
beamX_vOrig=xc.Vector([xbeamX,0,0]) # global coordinates of the start point in the beam axis
ybeamY=colUpshape.h()/2
beamY_vOrig=xc.Vector([0,ybeamY,0]) # global coordinates of the start point in the beam axis 

beamX_angX=0  # angle of the beam axis with the global XZ plane
beamY_angX=90  # angle of the beam axis with the global XZ plane

beam_esize=0.02  # size of the elements
beamX_idName='bmx_' # id for naming sets
beamY_idName='bmy_' # id for naming sets

#Top-plate
topPthk=16e-3  #end-plate thickness
topP_W=0.325   # width (horizontal)
topP_H=0.325  #height (vertical)
topP_zCent=beamshape.h()/2+endPthk-gap_col_to_weld
topP_vCentr=xc.Vector([0,0,topP_zCent]) #center of end-plate 1 in global coordinates
topP_angX=0  # angle of the end-plates with the global XZ plane
topP_esize=0.02 # size of the elements
topP_idName='tpp_'  # id for naming sets

# Array of bolts in end-plate
#boltDistX=140e-3  #aux
boltCoord=list()
distBolts=0.2
for x in [-distBolts,distBolts]:
    for y in [-distBolts,distBolts]:
        if [x,y] != [0,0]:
            boltCoord.append([x,y])
for x in [-0.05,0.05]:
    for y in [-distBolts,distBolts]:
        boltCoord.append([x,y])
for x in [-distBolts,distBolts]:
    for y in [-0.05,0.05]:
        boltCoord.append([x,y])


N_beamX=5e3  #design axial force in the supported beam (+ tension)
V_beamX=-87e3  #shear force
M_beamX=100e3-V_beamX*beam_L    #bending moment (vertical)
N_beamY=14.4e3  #design axial force in the supported beam (+ tension)
V_beamY=-87e3  #shear force
M_beamY=-160e3-V_beamY*beam_L#-V*beam_L    #bending moment (vertical)

# Welds data
weld_column_topP=sc.WeldTyp(10e-3,weldMetal) # weld top-flange of second-beam to end-plate
weld_column_endP=sc.WeldTyp(12e-3,weldMetal) # weld top-flange of second-beam to end-plate
weld_beam_column=sc.WeldTyp(10e-3,weldMetal) # weld beams to column
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

colLow=sbcm.HSSmember(colLowshape,colLow_L,colLow_vOrig,col_angX,colLow_idName,rotY=-90)
colLow.genSurfaces(modelSpace)
colUp=sbcm.HSSmember(colUpshape,colUp_L,colUp_vOrig,col_angX,colUp_idName,rotY=-90)
colUp.genSurfaces(modelSpace)

beamX=sbcm.Ibeam(beamshape,beam_L,beamX_vOrig,beamX_angX,beamX_idName)
beamX.genSurfaces(modelSpace)
beamY=sbcm.Ibeam(beamshape,beam_L,beamY_vOrig,beamY_angX,beamY_idName)
beamY.genSurfaces(modelSpace)

endPlateUp=sbcm.rectFakeBoltedPlate(endP_W,endP_H,endPup_vCentr,endP_angX,endPup_idName,boltCoord,rotX=90)
endPlateUp.genSurfaces(modelSpace)
endPlateLow=sbcm.rectFakeBoltedPlate(endP_W,endP_H,endPlow_vCentr,endP_angX,endPlow_idName,boltCoord,rotX=90)
endPlateLow.genSurfaces(modelSpace)
topPlate=sbcm.rectWeldPlate(topP_W,topP_H,topP_vCentr,topP_angX,topP_idName,rotX=90)
topPlate.genSurfaces(modelSpace)


out.displayBlocks()#coleam.web)

# Materials for linear analysis vonmises verification
ndWsteel=tm.defElasticIsotropic3d(preprocessor=prep, name='ndWsteel', E=steelW.E, nu=steelW.nu, rho=steelW.rho)
ndHSSsteel=tm.defElasticIsotropic3d(preprocessor=prep, name='ndHSSsteel', E=steelHSS.E, nu=steelHSS.nu, rho=steelHSS.rho)
ndPlateSteel=tm.defElasticIsotropic3d(preprocessor=prep, name='ndPlateSteel', E=steelPlate.E, nu=steelPlate.nu, rho=steelPlate.rho)

colUpMat=tm.defMembranePlateFiberSection(prep,name='colUpMat',h=colUpshape.t(),nDMaterial=ndHSSsteel)
colLowMat=tm.defMembranePlateFiberSection(prep,name='colLowMat',h=colLowshape.t(),nDMaterial=ndHSSsteel)
beamflangeMat=tm.defMembranePlateFiberSection(prep,name='beamflangeMat',h=beamshape.tf(),nDMaterial=ndWsteel)
beamwebMat=tm.defMembranePlateFiberSection(prep,name='beamwebMat',h=beamshape.tw(),nDMaterial=ndWsteel)
endPmat=tm.defMembranePlateFiberSection(prep,name='endPmat',h=endPthk,nDMaterial=ndPlateSteel)
topPmat=tm.defMembranePlateFiberSection(prep,name='topPmat',h=topPthk,nDMaterial=ndPlateSteel)

colLow.genMesh(modelSpace,colLowMat,col_esize)
colUp.genMesh(modelSpace,colUpMat,col_esize)
colLow.fixEndExtr(modelSpace)
beamX.genMesh(modelSpace,beamflangeMat,beamwebMat,beam_esize)
beamY.genMesh(modelSpace,beamflangeMat,beamwebMat,beam_esize)

endPlateUp.genMesh(modelSpace,endPmat,endP_esize)
endPlateLow.genMesh(modelSpace,endPmat,endP_esize)
topPlate.genMesh(modelSpace,topPmat,endP_esize)

lstWelds2check=list()
Wupcol_topP=colUp.genWeldContourInitExtr(weld_column_topP,topPlate.plate,-1,'Weld column to top plate')
lstWelds2check+=Wupcol_topP
Wupcol_endP=colUp.genWeldContourEndExtr(weld_column_endP,endPlateUp.plate,1,'Weld upper column to end plate')
lstWelds2check+=Wupcol_endP
Wlowcol_endP=colLow.genWeldContourInitExtr(weld_column_endP,endPlateLow.plate,-1,'Weld lower column to end plate')
lstWelds2check+=Wlowcol_endP
WbeamX_column=beamX.genWeldContourInitExtr(weld_beam_column,colUp.member,1,'Weld X-beam to column')
lstWelds2check+=WbeamX_column
WbeamY_column=beamY.genWeldContourInitExtr(weld_beam_column,colUp.member,1,'Weld X-beam to column')
lstWelds2check+=WbeamY_column

out.displayFEMesh()

#Bolts

setBolts=prep.getSets.defSet('setBolts')
bolt=sc.Bolt(fiBolt,steelBolt)
matchCoor=zip(boltCoord,boltCoord)
for coo in list(matchCoor):
    x=coo[0][0] ; z=coo[0][1]
    print('x1=',x,'z1=',z)
    endA=endPlateUp.grid.getPntXYZ((x,0,z))
    x=coo[1][0] ; z=coo[1][1]
    print('x2=',x,'z2=',z)
    endB=endPlateLow.grid.getPntXYZ((x,0,z))
    bolt.createBolt([endA,endB],'setBolts')

out.displayFEMesh()

node_beamX_load=beamX.grid.getPntXYZ((beam_L,0,0)).getNode()
node_beamY_load=beamY.grid.getPntXYZ((beam_L,0,0)).getNode()

load_beamX=loads.NodalLoad('load_beamX',[node_beamX_load],xc.Vector([N_beamX,0,V_beamX,0,M_beamX,0]))
load_beamY=loads.NodalLoad('load_beamY',[node_beamY_load],xc.Vector([0,N_beamY,V_beamY,M_beamY,0,0]))

LC1=lcases.LoadCase(preprocessor=prep,name="LC1",loadPType="default",timeSType="constant_ts")
LC1.create()
LC1.addLstLoads([load_beamX,load_beamY])

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

colUp.member.description='Column '+colUpshape.getMetricName()
topPlate.plate.description='Top plate '+ str(round(topP_H*1000,0)) + 'x' +str(round(topP_W*1000,0)) +  'x' +str(round(topPthk*1000,0))
endPlateUp.plate.description='Top splice-plate '+ str(round(endP_H*1000,0)) + 'x' +str(round(endP_W*1000,0)) +  'x' +str(round(endPthk*1000,0))
endPlateLow.plate.description='Bottom splice-plate '+ str(round(endP_H*1000,0)) + 'x' +str(round(endP_W*1000,0)) +  'x' +str(round(endPthk*1000,0))


lstBeams=[beamX.beam,beamY.beam]
lstHSS=[colUp.member,colLow.member]
lstPlates=[topPlate.plate,endPlateUp.plate,endPlateLow.plate]

for st in lstHSS:
    for e in st.elements: e.setProp('yieldStress', steelHSS.fy)
for st in lstBeams:
    for e in st.elements: e.setProp('yieldStress', steelW.fy)
for st in lstPlates:
    for e in st.elements: e.setProp('yieldStress', steelPlate.fy)

lstAllShells=lstBeams+lstPlates+lstHSS
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

