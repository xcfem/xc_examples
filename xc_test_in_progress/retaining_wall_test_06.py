# -*- coding: utf-8 -*-
''' Retaining wall calculation verification test. Inspired on the "A.4 worked example to accompany Chapter 4" of the publication: Eurocode 7: Geotechnical Design Worked examples. Worked examples presented at the Workshop “Eurocode 7: Geotechnical Design” Dublin, 13-14 June, 2013.

https://publications.jrc.ec.europa.eu/repository/handle/JRC85029
'''

from __future__ import division
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2023, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

import os
import math
import geom
import xc
from scipy.constants import g
from rough_calculations import ng_retaining_wall
from materials.ec2 import EC2_materials
from materials.ec2 import EC2_limit_state_checking
from actions import load_cases
from actions import combinations
from geotechnics import earth_pressure as ep
from geotechnics import frictional_cohesive_soil as fcs
from actions.earth_pressure import earth_pressure
from misc_utils import log_messages as lmsg

#     __      __    _ _                          _            
#     \ \    / /_ _| | |  __ _ ___ ___ _ __  ___| |_ _ _ _  _ 
#      \ \/\/ / _` | | | / _` / -_) _ \ '  \/ -_)  _| '_| || |
#       \_/\_/\__,_|_|_| \__, \___\___/_|_|_\___|\__|_|  \_, |
#                        |___/                           |__/ 
#                              +
#                             /|
#                           /  | V
#                         /    | i
#     Backfill slope -> /      | r            
#                     /        | t
#      zTopWall --- /          | u
#               |  |           | a
#               |  |           | l
#               |  | step      |
#               |  |__         | b
#               |     |        | a
#               |     |        | c
#               |     |        | k
#          +----      ---------+    <- zTopFooting
#          |Toe          Heel  |
#          +-------------------+
#

# Wall geometry
retainedHeight= 8.35
zTopWall= retainedHeight

## Stem
stemTopWidth= 0.55 # width of the wall at its top.
stemBottomWidth= 0.85 # width of the wall at its bottom.
stemBackSteps= [(4.0, stemBottomWidth-stemTopWidth)] # step on the stem back.

## Foundation.
bToe= 1.4 # width of the toe.
bHeel= 2.55
footingWidth= bToe+stemBottomWidth+bHeel # overall breadth of the base.
footingThickness= 1.1 # thickness of the footing.

#  __  __      _           _      _    
# |  \/  |__ _| |_ ___ _ _(_)__ _| |___
# | |\/| / _` |  _/ -_) '_| / _` | (_-<
# |_|  |_\__,_|\__\___|_| |_\__,_|_/__/

# Partial factors (M1)
gammaMPhiM1= 1.0

# Granular fill.
slopeOfBackfillSurface= 0.0
## Design approach 2 (A1+M1+R2).
granularFillM1= ep.RankineSoil(phi= math.radians(30), rho= 2000, gammaMPhi= gammaMPhiM1, beta= slopeOfBackfillSurface) 

# Wall materials.
concrete= EC2_materials.C25
steel= EC2_materials.S500B
cover= 45e-3
reinf_types= EC2_limit_state_checking.define_rebar_families(steel= steel, cover= cover)

#  __      __    _ _        _     _        _   
# \ \    / /_ _| | |   ___| |__ (_)___ __| |_ 
# \ \/\/ / _` | | |  / _ \ '_ \| / -_) _|  _|
# \_/\_/\__,_|_|_|  \___/_.__// \___\__|\__|
#                            |__/            

wall= ng_retaining_wall.RetainingWall(name= 'Retaining_wall_test_05', stemHeight= retainedHeight, stemBottomWidth= stemBottomWidth, stemTopWidth= stemTopWidth, stemBackSlope= 0.0, footingThickness= footingThickness, bToe= bToe, bHeel= bHeel, concrete= concrete, steel= steel)
wall.setStemBackSteps(stemBackSteps)

# Check area.
wallArea= wall.getArea()
refWallArea= footingWidth*footingThickness+stemTopWidth*retainedHeight+(retainedHeight-stemBackSteps[0][0])*stemBackSteps[0][1]
ratioWallArea= abs(wallArea-refWallArea)/refWallArea

#    ___     _       __                              _   
#   | _ \___(_)_ _  / _|___ _ _ __ ___ _ __  ___ _ _| |_ 
#   |   / -_) | ' \|  _/ _ \ '_/ _/ -_) '  \/ -_) ' \  _|
#   |_|_\___|_|_||_|_| \___/_| \__\___|_|_|_\___|_||_\__|
#                                                      
wall.stemReinforcement.setReinforcement(1, reinf_types['A20_10'].getCopy())  # vert. trasdós (esperas)
wall.stemReinforcement.setReinforcement(2, reinf_types['A20_10'].getCopy()) # vert. trasdós (contacto terreno)
wall.stemReinforcement.setReinforcement(6, reinf_types['A10_10'].getCopy())  # coronación
wall.stemReinforcement.setReinforcement(11, reinf_types['A16_10'].getCopy()) # horiz. trasdós

wall.stemReinforcement.setReinforcement(4, reinf_types['A10_10'].getCopy()) # vert. intradós (esperas)
wall.stemReinforcement.setReinforcement(5, reinf_types['A10_10'].getCopy()) # vert. intradós (exterior)
wall.stemReinforcement.setReinforcement(12, reinf_types['A16_10'].getCopy()) # horiz. intradós

wall.footingReinforcement.setReinforcement(3, reinf_types['A20_10'].getCopy()) # tr. sup. zapata
wall.footingReinforcement.setReinforcement(9, reinf_types['A20_10'].getCopy()) # ln. sup. zapata
wall.footingReinforcement.setReinforcement(7, reinf_types['A10_10'].getCopy()) # tr. inf. zapata
wall.footingReinforcement.setReinforcement(8, reinf_types['A20_10'].getCopy()) # ln. inf. zapata

wall.footingReinforcement.setReinforcement(10, reinf_types['A12_15'].getCopy()) # lateral zapata

# Next step reinforcement.
wall.stemReinforcement.setReinforcement(102, reinf_types['A16_20'].getCopy()) # vert. trasdós (contacto terreno)
wall.stemReinforcement.setReinforcement(105, reinf_types['A10_10'].getCopy()) # vert. intradós (exterior)
wall.stemReinforcement.setReinforcement(111, reinf_types['A16_10'].getCopy()) # horiz. trasdós
wall.stemReinforcement.setReinforcement(112, reinf_types['A16_10'].getCopy()) # horiz. intradós


# Create wall FE model.
wallFEModel= wall.createLinearElasticFEModel(prbName= 'Retaining wall '+wall.name, kS= 15e6) # assumed value for subgrade reaction modulus.

#    _      _   _             
#   /_\  __| |_(_)___ _ _  ___
#  / _ \/ _|  _| / _ \ ' \(_-<
# /_/ \_\__|\__|_\___/_||_/__/
                             
#Actions.
preprocessor= wallFEModel.getPreprocessor
loadCaseManager= load_cases.LoadCaseManager(preprocessor)
loadCaseNames= ['selfWeight','earthPress','liveLoad']
loadCaseManager.defineSimpleLoadCases(loadCaseNames)

### Partial safety factors on actions (A).
gammaGA1= 1.35 # Set A1.
gammaQA1= 1.5 # Set A1.



#        ___                                 _             _   _             
#       | _ \___ _ _ _ __  __ _ _ _  ___ _ _| |_   __ _ __| |_(_)___ _ _  ___
#       |  _/ -_) '_| '  \/ _` | ' \/ -_) ' \  _| / _` / _|  _| / _ \ ' \(_-<
#       |_| \___|_| |_|_|_\__,_|_||_\___|_||_\__| \__,_\__|\__|_\___/_||_/__/
#                                                                          
## Self weight of the wall.
selfWeight= loadCaseManager.setCurrentLoadCase('selfWeight')
Wselfk= wall.createSelfWeightLoads(rho= concrete.density(),grav= g)

## Dead load on the heel.
heelFillDepth= wall.getBackfillAvobeHeelAvgHeight(beta= granularFillM1.beta, zGround= 0.0)
Wfillk= wall.createDeadLoad(heelFillDepth= heelFillDepth, toeFillDepth= 0.0, rho= granularFillM1.rho, grav= g)

## Earth pressure.
### Backfill soil properties
KaM1= granularFillM1.Ka()
gSoil= granularFillM1.rho*g
zBottomSoils=[-1e3]
KSoils= [KaM1]
gammaSoils= [gSoil]
zWater= -1e3
gammaWater= 1000*g
### Set current load case.
earthPress= loadCaseManager.setCurrentLoadCase('earthPress')

## Define virtual back.
virtualBack= wall.getVirtualBack(beta= granularFillM1.beta)

### Earth pressure on back of wall stem.
backfillPressureModel= earth_pressure.EarthPressureModel(zGround= virtualBack.getFromPoint().y, zBottomSoils= zBottomSoils, KSoils= KSoils, gammaSoils= gammaSoils, zWater= zWater, gammaWater= gammaWater,qUnif=0)
EaGk= wall.createBackfillPressures(backfillPressureModel, Delta= granularFillM1.beta, beta= granularFillM1.beta)



#     __   __        _      _    _               _   _             
#     \ \ / /_ _ _ _(_)__ _| |__| |___   __ _ __| |_(_)___ _ _  ___
#      \ V / _` | '_| / _` | '_ \ / -_) / _` / _|  _| / _ \ ' \(_-<
#       \_/\__,_|_| |_\__,_|_.__/_\___| \__,_\__|\__|_\___/_||_/__/
#                                                                  
### Set current load case.
earthPress= loadCaseManager.setCurrentLoadCase('liveLoad')
### Uniform load on the backfill surface.
qUnif= 10e3
unifLoadPressure= earth_pressure.UniformPressureOnBackfill(zGround= virtualBack.getFromPoint().y, zBottomSoils= zBottomSoils, KSoils= KSoils, qUnif= qUnif)
EaQk= wall.createBackfillPressures(pressureModel= unifLoadPressure, Delta= granularFillM1.beta, beta= granularFillM1.beta)

#   ___           _    _           _   _             
#  / __|___ _ __ | |__(_)_ _  __ _| |_(_)___ _ _  ___
# | (__/ _ \ '  \| '_ \ | ' \/ _` |  _| / _ \ ' \(_-<
# \___\___/_|_|_|_.__/_|_||_\__,_|\__|_\___/_||_/__/
# Define combinations.
combDict= dict()
combDict['ULS01']= '1.35*selfWeight+1.35*earthPress'
combDict['ULS02']= '1.35*selfWeight+1.35*earthPress+1.5*liveLoad'
combDict['SLS01']= '1.0*selfWeight+1.0*earthPress'

# Put them in the combination container.
combContainer= combinations.CombContainer()
for key in combDict:
    combExpr= combDict[key]
    if(key.startswith('ULS')):
        combContainer.ULS.perm.add(key, combExpr)
    elif(key.startswith('SLS')):
        combContainer.SLS.qp.add(key, combExpr)
    else:
        lmsg.error('unknown combination type: '+str(key))
        
# Dump them into the XC model.
combContainer.dumpCombinations(preprocessor)


# Limit state checking

#    ___ ___ ___                _  __ _         _   _             
#   / __| __/ _ \  __ _____ _ _(_)/ _(_)__ __ _| |_(_)___ _ _  ___
#  | (_ | _| (_) | \ V / -_) '_| |  _| / _/ _` |  _| / _ \ ' \(_-<
#  \___|___\___/   \_/\___|_| |_|_| |_\__\__,_|\__|_\___/_||_/__/
#                                                                
geoULSCombinations= ['ULS01','ULS02']

gammaR2Sliding= 1.1
gammaR2Bearing= 1.4

## Critical state (constant volume) angle of shearing resistance of the soil.
## See clause 6.5.3 (10) of Eurocode 7 part 1. 
phi_cv= math.radians(30)
foundationSoilModel= fcs.FrictionalCohesiveSoil(phi= granularFillM1.phi, c= 0.0, rho= granularFillM1.rho, phi_cv= phi_cv, gammaMPhi= gammaMPhiM1)
## Perform GEO verifications.
sr= wall.performGEOVerifications(geoULSCombinations, foundationSoilModel= foundationSoilModel, toeFillDepth= wall.footingThickness, gammaRSliding= gammaR2Sliding, gammaRBearing= gammaR2Bearing, sg_adm=3.75*9.81/1e-4)

## Verification of resistance to sliding
slidingResistanceDegreeOfUtilization= sr.getDegreeOfUtilizationForSliding()
ratioSliding= abs(slidingResistanceDegreeOfUtilization-0.9339424062947872)/0.9339424062947872
## Verification of bearing resistance
bearingResistanceDegreeOfUtilization= sr.getDegreeOfUtilizationForBearingResistance()
ratioBearing= abs(bearingResistanceDegreeOfUtilization-2.2375774287878336)/2.2375774287878336
## Verification of admissible pressure
admissiblePressureDegreeOfUtilization= sr.getDegreeOfUtilizationForAdmissiblePressure()
ratioAdmPressure= abs(admissiblePressureDegreeOfUtilization-0.9338748230058515)/0.9338748230058515
## Verification of resistance to toppling
topplingResistanceDegreeOfUtilization= sr.getDegreeOfUtilizationForOverturning()
ratioToppling= abs(topplingResistanceDegreeOfUtilization-0.6341013315905858)/0.6341013315905858

#      ___ _    ___  __   __       _  __ _         _   _             
#     / __| |  / __| \ \ / /__ _ _(_)/ _(_)__ __ _| |_(_)___ _ _  ___
#     \__ \ |__\__ \  \ V / -_) '_| |  _| / _/ _` |  _| / _ \ ' \(_-<
#     |___/____|___/   \_/\___|_| |_|_| |_\__\__,_|\__|_\___/_||_/__/
#
## Serviceability analysis.
slsCombinations= ['SLS01']
wall.modelSpace.removeAllLoadsAndCombinationsFromDomain()
wall.modelSpace.revertToStart()
wall.modelSpace.clearCombinationsFromLoadHandler()
combContainer.dumpCombinations(preprocessor)
sls_results= wall.performSLSAnalysis(slsCombinations)
wall.setSLSInternalForcesEnvelope(sls_results.internalForces)


#     ___ _____ ___                _  __ _         _   _             
#    / __|_   _| _ \  __ _____ _ _(_)/ _(_)__ __ _| |_(_)___ _ _  ___
#    \__ \ | | |   /  \ V / -_) '_| |  _| / _/ _` |  _| / _ \ ' \(_-<
#    |___/ |_| |_|_\   \_/\___|_| |_|_| |_\__\__,_|\__|_\___/_||_/__/
#
# ULS strength analysis.
strULSCombinations= ['ULS01','ULS02']
wall.modelSpace.removeAllLoadsAndCombinationsFromDomain()
wall.modelSpace.revertToStart()
wall.modelSpace.clearCombinationsFromLoadHandler()
## Dump the STR combinations to XC (in this case they are the same than
## the used for the GEO calculations.
combContainer.dumpCombinations(preprocessor)
uls_results= wall.performULSAnalysis(strULSCombinations)
wall.setULSInternalForcesEnvelope(uls_results.internalForces)

pth= "/tmp/tmp_results/"
if not os.path.exists(pth):
    os.makedirs(pth)
wall.writeResult(pth)
wall.drawSchema(pth)

print('wall area: ', wallArea, 'm2')
print('reference wall area: ', refWallArea, 'm2')
print('ratioWallArea= ',ratioWallArea)
print('\nCheck sliding degree of utilization.')
print('sliding degree of utilization: ', slidingResistanceDegreeOfUtilization, ratioSliding)
print('\nCheck bearing degree of utilization.')
print('bearing degree of utilization: ', bearingResistanceDegreeOfUtilization, ratioBearing)
print('\nCheck admissible pressure degree of utilization.')
print('admissible pressure degree of utilization: ', admissiblePressureDegreeOfUtilization, ratioAdmPressure)
print('\nCheck toppling degree of utilization.')
print('toppling degree of utilization: ', topplingResistanceDegreeOfUtilization, ratioToppling)



fname= os.path.basename(__file__)
if(abs(ratioWallArea)<1e-6) and (abs(ratioSliding)<1e-4) and (abs(ratioBearing)<1e-4) and (abs(ratioToppling)<1e-4):
    print('test '+fname+': ok.')
else:
    lmsg.error(fname+' ERROR.')
    
# # Graphic output.
# wall.draw()
    
# # Display loads.
# from postprocess import output_handler
# oh= output_handler.OutputHandler(wall.modelSpace)
# for load in loadCaseNames:
#     wall.modelSpace.addLoadCaseToDomain(load)
#     oh.displayLoads()
#     wall.modelSpace.removeLoadCaseFromDomain(load)

print('Uncomment the following line!')
#os.system("rm -rf "+pth) # Your garbage you clean it
