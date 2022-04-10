# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT) , Ana Ortega (AO_O) "
__copyright__= "Copyright 2022, LCPT, AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es, ana.ortega@ciccp.es "

import math
import yaml
import geom
import xc
from materials.sections import section_properties
from materials.awc_nds import AWCNDS_materials
from materials.awc_nds import AWCNDS_limit_state_checking
from materials.awc_nds import dimensional_lumber
from actions import combinations as combs
from misc_utils import units_utils

class StudArrangement(AWCNDS_limit_state_checking.StudArrangement):
    

    def printCombResults(self, combResults):
          N= combResults['N']
          M= combResults['M']
          fc= combResults['fc']
          CP= combResults['CP']
          CD= combResults['CD']
          FcE1= combResults['FcE1']
          FcE2= combResults['FcE2']
          RB= combResults['RB']
          FbE= combResults['FbE=']
          CF= combResults['CF']


          print('axial load:', N/1e3, ' kN')
          print('load duration factor: ', CD)
          print('bending moment:', M/1e3, ' kN m')
          print ('compression stress: ', fc/1e6, ' MPa')
          print('unbraced length x:', self.stud.unbracedLengthY, ' m')
          print('unbraced length y:', self.stud.unbracedLengthZ, ' m')
          # print('Fc\'= ', Fc_adj/1e6,' MPa')
          # print('Fb\'= ', Fb_adj/1e6,' MPa')
          # print('E\'= ', E_adj/1e9,' GPa')
          print('stud stability factor Cp= ', CP)
          print('FcE1= ', FcE1/1e6,' MPa')
          print('FcE2= ', FcE2/1e6,' MPa')
          print('RB= ', RB,' m')
          print('FbE= ', FbE/1e6,' MPa')
          print('capacity factor CF= ', CF[0])
        
        
    def printResults(self, results, worstCase):

        if(worstCase):
            print('*************** worst case: ', worstCase)
            self.printCombResults(results[worstCase])
        else:
            for key in results:
                print('*************** comb: ', key)
                self.printCombResults(results[key])
       
    def printReport(self, results, worstCase):
        print('***** ', self.name ,' ******')
        print('wall height= ',self.wallHeight, ' m')
        print('stud height= ',self.studHeight, ' m')
        print('stud spacing= ',self.studSpacing, ' m')
        print('sections dimensions: ', str(self.stud.crossSection.b*1e3)+'x'+str(self.stud.crossSection.h*1e3), ' mm')
        self.printResults(results, worstCase)

def getLoadCombDurationFactor(loadComb):
    ll= ('liveLoad' in loadComb)
    dl= ('deadLoad' in loadComb)
    sl= ('snowLoad' in loadComb)
    wl= ('windLoad' in loadComb)
    return AWCNDS_materials.getLoadCombinationDurationFactor(deadLoad= dl, liveLoad= ll, snowLoad= sl, windLoad= wl)

# Read data.
fName= './bearing_wall_data.yaml'
with open(fName) as file:
    try:
        wallData= yaml.safe_load(file)
    except yaml.YAMLError as exception:
        print(exception)

# Geometry
wallHeight= eval(wallData['wallHeight'])
studSpacing= eval(wallData['studSpacing'])

# Materials
wood= eval(wallData['wood'])
studSection= AWCNDS_materials.DimensionLumberSection(name= wallData['studSection'], woodMaterial= wood)

#Loads
## Wind loads
windWallPressure= wallData['windWallPressure'] 
windStudPressure= windWallPressure*studSpacing # N/m

print('wind load:', windStudPressure/1e3, ' kN/m')

title= wallData['title']
# Actions
## Reduction in uniform live loads.
liveLoadReductionFactor= wallData['liveLoadReductionFactor'] 
print('Live load reduction factor: ', liveLoadReductionFactor)

## Load definition (values from truss_AB_reactions.ods)
deadLoad= xc.Vector([0.0,15.25e3]) # kN/m
liveLoad= liveLoadReductionFactor*xc.Vector([0.0,26.17e3]) # kN/m
snowLoad= xc.Vector([0.0,11.28e3]) # kN/m
windLoad= xc.Vector([windStudPressure,-7.13e3]) # kN/m

# Load combination definition
combContainer= combs.CombContainer()
combData= wallData['loadCombinations']        
for combName in combData:
    combExpr= combData[combName]
    combContainer.SLS.qp.add(combName,combExpr)

studObj= StudArrangement(name= title, studSection= studSection, studSpacing= studSpacing, wallHeight= wallHeight, loadCombDurationFactorFunction= getLoadCombDurationFactor);

results, worstCase= studObj.check(deadLoad, liveLoad, snowLoad, windLoad, loadCombinations= combContainer.SLS.qp)

studObj.printReport(results= results, worstCase= worstCase)
