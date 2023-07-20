# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import math
from rough_calculations import ng_retaining_wall
import geom
import xc
from materials.sia262 import SIA262_materials
from materials.sia262 import SIA262_limit_state_checking
from materials.ehe import EHE_materials
from materials.ehe import EHE_limit_state_checking
from materials import typical_materials
from geotechnics import earth_pressure as ep
from geotechnics import frictional_cohesive_soil as fcs
from actions import load_cases
from actions import combinations
from actions.earth_pressure import earth_pressure
from postprocess.reports import common_formats as fmt
from postprocess import output_handler

#Geometry
zTopWall= 6.0 # z coordinate of the wall top.
zTopFooting= 0.0 # z coordinate of the footing upper surface.

stemSlope= 1/10.0 # H/V
b= 1.0   #length of wall to analyze
stemTopWidth= 0.40 # width of the wall at its top.
stemHeight= zTopWall-zTopFooting # height of the stem.
stemBottomWidth= stemTopWidth+stemSlope*stemHeight # width of the wall at its bottom.
bToe= 1.25 # width of the toe.
bHeel= 3.5-stemBottomWidth # width of the heel.
footingThickness= 1.1 # thickness of the footing.
cover= 60e-3 # rebars cover.

#Backfill soil properties
kS= 15e6 # Winkler modulus.
phiS= 30  # internal frictional angle
rhoS= 2000  # density (kg/m3)
backfillDelta= math.radians(18.4)
frontFillDepth= 0.5
zGroundBackfill= -0.2 # back fill

# Foundation stratified soil properties
hi=[1,3,5,8,100]  #cuaternario (QG), QT3L, QT3G,formación  Dueñas
rhoi= [2000,1910,1690,2100,1950]
phii= [math.radians(30),math.radians(25),math.radians(32),math.radians(35),math.radians(24)]
ci=[20e3,2.5e3,5e3,30e3,50e3]

#Loads
gravity=9.81 # Gravity acceleration (m/s2)
HwaterAcc= 1.5

#Materials
concrete= SIA262_materials.c30_37
#concrete= EHE_materials.HA30
reinfSteel= EHE_materials.B500S
exec(open("./rebar_types.py")).read())

sectionName= "mur6m"
wall= ng_retaining_wall.RetainingWall(sectionName,cover,stemBottomWidth,stemTopWidth, stemBackSlope= 1/10.0, footingThickness= footingThickness, concrete= concrete, steel= reinfSteel)
wall.stemHeight= stemHeight
wall.bToe= bToe
wall.bHeel= bHeel
wall.concrete= concrete
#wall.exigeanceFisuration= 'A'
wall.stemReinforcement.setReinforcement(1,A20_10.getCopy('A'))  # vert. trasdós (esperas)
wall.stemReinforcement.setReinforcement(2,A20_20.getCopy('A')) # vert. trasdós (contacto terreno)
wall.stemReinforcement.setReinforcement(11,A16_20.getCopy('A')) #horiz. trasdós

wall.stemReinforcement.setReinforcement(4,A16_20.getCopy('A')) # vert. intradós (esperas)
wall.stemReinforcement.setReinforcement(5,A16_20.getCopy('A')) # vert. intradós (exterior)
wall.stemReinforcement.setReinforcement(12,A16_20.getCopy('A')) #horiz. intradós

wall.footingReinforcement.setReinforcement(3,A20_10.getCopy('A')) #tr. sup. zapata
wall.footingReinforcement.setReinforcement(9,A16_10.getCopy('A')) # ln. sup. zapata
wall.footingReinforcement.setReinforcement(7,A20_10.getCopy('A')) # tr. inf. zapata
wall.footingReinforcement.setReinforcement(8,A16_20.getCopy('A')) # ln. inf. zapata

wall.stemReinforcement.setReinforcement(6,A12_20.getCopy('A'))  #coronación

wallFEModel= wall.createFEProblem('Retaining wall '+sectionName)
preprocessor= wallFEModel.getPreprocessor
nodes= preprocessor.getNodeHandler

#Soils
kX= typical_materials.defElasticMaterial(preprocessor, "kX",kS/10.0)
kY= typical_materials.defElasticMaterial(preprocessor, "kY",kS)
#kY= typical_materials.defElastNoTensMaterial(preprocessor, "kY",kS)
#Backfill soil properties
backfillSoilModel= ep.RankineSoil(phi= math.radians(phiS),rho= rhoS) #Characteristic values.
#Foundation stratified soil properties
stratifiedSoil= fcs.StratifiedSoil(hi,rhoi,phii,ci)

foundationSoilModel= stratifiedSoil.getEquivalentSoil(Beff= 5,gMPhi= 1.2,gMc= 1.5) #Design values.

#Mesh.
wall.genMesh(nodes,[kX,kY])

#Sets.
totalSet= preprocessor.getSets.getSet("total")


#Actions.
loadCaseManager= load_cases.LoadCaseManager(preprocessor)
loadCaseNames= ['selfWeight','earthPress','earthPressAcc']
loadCaseManager.defineSimpleLoadCases(loadCaseNames)

#Self weight.
selfWeight= loadCaseManager.setCurrentLoadCase('selfWeight')
wall.createSelfWeightLoads(rho= concrete.density(),grav= gravity)

# Earth pressure. (drainage ok)
gSoil= backfillSoilModel.rho*gravity
earthPress= loadCaseManager.setCurrentLoadCase('earthPress')
wall.createDeadLoad(heelFillDepth= wall.stemHeight,toeFillDepth= frontFillDepth,rho= backfillSoilModel.rho, grav= gravity)
Ka= backfillSoilModel.Ka()
backfillPressureModel=  earth_pressure.EarthPressureModel(zGround= zGroundBackfill, zBottomSoils=[-1e3],KSoils= [Ka], gammaSoils= [gSoil], zWater= -1e3, gammaWater= 1000*gravity,qUnif=0)
wall.createBackfillPressures(backfillPressureModel, Delta= backfillDelta)
zGroundFrontFill= zGroundBackfill-wall.stemHeight+frontFillDepth #Front fill
frontFillPressureModel=  earth_pressure.EarthPressureModel(zGround= zGroundFrontFill, zBottomSoils=[-1e3],KSoils= [Ka], gammaSoils= [gSoil], zWater= -1e3, gammaWater= 1000*gravity,qUnif=0)
wall.createFrontFillPressures(frontFillPressureModel)

#Accidental: earth pressure failure drainage system.
gSoil= backfillSoilModel.rho*gravity
earthPressAcc= loadCaseManager.setCurrentLoadCase('earthPressAcc')
wall.createDeadLoad(heelFillDepth= wall.stemHeight,toeFillDepth= frontFillDepth,rho= backfillSoilModel.rho, grav= gravity)
Ka= backfillSoilModel.Ka()
backfillPressureModelAcc=  earth_pressure.EarthPressureModel(zGround= zGroundBackfill, zBottomSoils=[-1e3],KSoils= [Ka], gammaSoils= [gSoil], zWater=zGroundBackfill-stemHeight+HwaterAcc, gammaWater= 1000*gravity,qUnif=0)
wall.createBackfillPressures(backfillPressureModelAcc, Delta= backfillDelta)
zGroundFrontFill= zGroundBackfill-wall.stemHeight+frontFillDepth #Front fill
frontFillPressureModel=  earth_pressure.EarthPressureModel(zGround= zGroundFrontFill, zBottomSoils=[-1e3],KSoils= [Ka], gammaSoils= [gSoil], zWater= -1e3, gammaWater= 1000*gravity,qUnif=0)
wall.createFrontFillPressures(frontFillPressureModel)


#Load combinations
combContainer= combinations.CombContainer()

## Quasi-permanent situations.
combContainer.SLS.qp.add('SLS01', '1.0*selfWeight+1.0*earthPress')
slsCombinations= ['SLS01']

## Stability ultimate states. (type 1)
combContainer.ULS.perm.add('ULS01', '0.9*selfWeight+1.00*earthPress')
combContainer.ULS.perm.add('ULS02', '1.1*selfWeight+1.00*earthPress')
combContainer.ULS.perm.add('ULS03', '0.9*selfWeight+1.50*earthPress')
combContainer.ULS.perm.add('ULS04', '1.1*selfWeight+1.50*earthPress')
combContainer.ULS.perm.add('ULS05', '0.9*selfWeight+1.00*earthPressAcc')
combContainer.ULS.perm.add('ULS06', '1.1*selfWeight+1.00*earthPressAcc')
stabilityULSCombinations= ['ULS01','ULS02','ULS03','ULS04','ULS05','ULS06']

## Strength ultimate states. (type 2).
# Earth pressure at rest so 1.35*K0/Ka= 1.35*0.5/0.33= 2.05 -> 2.0
combContainer.ULS.perm.add('ULS07', '1.0*selfWeight+1.00*earthPress')
combContainer.ULS.perm.add('ULS08', '1.35*selfWeight+1.00*earthPress')
combContainer.ULS.perm.add('ULS09', '1.0*selfWeight+1.50*earthPress')
combContainer.ULS.perm.add('ULS10', '1.35*selfWeight+1.50*earthPress')
combContainer.ULS.perm.add('ULS11', '1.0*selfWeight+1.00*earthPressAcc')
combContainer.ULS.perm.add('ULS12', '1.35*selfWeight+1.00*earthPressAcc')
strengthULSCombinations= ['ULS07','ULS08','ULS09','ULS10','ULS11','ULS12']

# Limit state checking
## Serviceability analysis.
combContainer.dumpCombinations(preprocessor)
sls_results= wall.performSLSAnalysis(slsCombinations)
wall.setSLSInternalForcesEnvelope(sls_results.internalForces)

sg_adm= 0.222e6
fill_pressure= (frontFillDepth+footingThickness)*backfillSoilModel.rho*gravity
print('fill pressure: ', fill_pressure/1e6, 'MPa')
print('sg_adm: ', sg_adm/1e6, 'MPa')
sg_adm+= fill_pressure
print('total sg_adm: ', sg_adm/1e6, 'MPa')

## ULS stability analysis.
sr= wall.performStabilityAnalysis(stabilityULSCombinations,foundationSoilModel,sg_adm= sg_adm)

## ULS strength analysis.
uls_results= wall.performULSAnalysis(strengthULSCombinations)
wall.setULSInternalForcesEnvelope(uls_results.internalForces)


pth= "./results/"


print("Overturning: ",sr.Foverturning)
print("Sliding: ",sr.Fsliding)
print("Bearing: ",sr.Fbearing)
print("Allow. press.: ",sr.FadmPressure)

wall.writeResult(pth)
wall.drawSchema(pth)
notes= ["Overturning: "+fmt.Factor.format(sr.Foverturning), "Sliding: "+fmt.Factor.format(sr.Fsliding), "Bearing: "+fmt.Factor.format(sr.Fbearing), "Allow. press.: "+fmt.Factor.format(sr.FadmPressure)] 
wall.draw(notes)

#########################################################
# Graphic stuff.
#oh= output_handler.OutputHandler(wall.modelSpace)

## Uncomment to display blocks
#oh.displayBlocks()
## Uncomment to display the mesh
#oh.displayFEMesh()

## Uncomment to display the loads
#oh.displayLoads()

## Uncomment to display the vertical displacement
#oh.displayDispRot(itemToDisp='uX')
#oh.displayNodeValueDiagram(itemToDisp='uX')

## Uncomment to display the reactions
#oh.displayReactions()

## Uncomment to display the internal force
#oh.displayIntForcDiag('Mz')

