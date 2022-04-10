# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import math
import yaml
import geom
import xc
from model import predefined_spaces
from materials.awc_nds import AWCNDS_materials
from materials.awc_nds import AWCNDS_limit_state_checking
from materials.awc_nds import dimensional_lumber
from actions import combinations as combs
from misc_utils import units_utils

OKGREEN= '\033[92m'
WARNING= '\033[93m'
FAIL= '\033[91m'
ENDC = '\033[0m'

def getLoadCombDurationFactor(loadComb):
    ll= ('liveLoad' in loadComb)
    dl= ('deadLoad' in loadComb)
    sl= ('snowLoad' in loadComb)
    wl= ('windLoad' in loadComb)
    return AWCNDS_materials.getLoadCombinationDurationFactor(deadLoad= dl, liveLoad= ll, snowLoad= sl, windLoad= wl)

class DoublePlate(AWCNDS_limit_state_checking.WallTopPlates):
        

    def reportComb(self, combName, combResults):
        
        uYMax= combResults['uYMax']
        r= self.studSpacing/uYMax
        loadDurationFactor= combResults['CD']
        sgMax= combResults['sgMax']
        Fb_adj= combResults['Fb_adj']
        FbCF= combResults['bendingCF']
        tauMax= combResults['tauMax']
        Fv_adj= combResults['Fv_adj']
        FvCF= combResults['shearCF']
        RMax= combResults['RMax']
        sgMax= combResults['sgMax']
        Fc_perp= combResults['Fc_perp']
        Fc_perpCF= combResults['Fc_perpCF']
        
        ## Bending stiffness
        print('**** uYMax('+combName+')= ', uYMax*1e3, ' mm (L/'+str(r)+')\n')

        ## Bending strength
        print('load duration factor: ', loadDurationFactor)
        print('sgMax= ', sgMax/1e6,' MPa')
        print('Fb_adj= ', Fb_adj/1e6,' MPa')
        if(Fb_adj>sgMax):
            print('**** CF= ', FbCF,'OK\n')
        else:
            print(FAIL+'**** CF= '+str(FbCF)+' KO\n'+ENDC)

        ## Shear strength
        print('tauMax= ', tauMax/1e6,' MPa')
        print('Fv_adj= ', Fv_adj/1e6,' MPa')
        if(Fv_adj>tauMax):
            print('**** CF= ', FvCF,'OK\n')
        else:
            print(FAIL+'**** CF= '+str(FvCF)+' KO\n'+ENDC)

        ## Compression perpendicular to grain
        print('RMax= ', RMax/1e3, ' kN')
        print('sgMax= ', sgMax/1e6, ' MPa / ', sgMax/AWCNDS_materials.psi2Pa,'psi')
        print('Fc_perp= ', Fc_perp/1e6, ' MPa / ', Fc_perp/AWCNDS_materials.psi2Pa,'psi')
        if(Fc_perp>sgMax):
            print('**** CF= ', Fc_perpCF,'OK\n')
        else:
            print(FAIL+'**** CF= '+str(Fc_perpCF)+' KO\n'+ENDC)
            

    
    def printResults(self, combContainer, results):
        # Data
        print('Wood plate material: ', self.plateSection.wood.name,' grade:', self.plateSection.wood.grade)
        print('plate thickness= ', self.plateSection.h*1e3, ' mm')
        print('stud spacing= ', self.studSpacing, ' m')
        print('truss spacing= ', self.trussSpacing, ' m\n')
        for comb in combContainer.SLS.qp:
            print('********** combination: '+comb)
            combResults= results[comb]
            self.reportComb(combName= comb, combResults= combResults)
            
# Read data.
fName= './bearing_wall_data.yaml'
with open(fName) as file:
    try:
        wallData= yaml.safe_load(file)
    except yaml.YAMLError as exception:
        print(exception)

title= wallData['title']
studSpacing= eval(wallData['studSpacing'])
trussSpacing= eval(wallData['trussSpacing'])
# Materials
wood= eval(wallData['wood'])
xc_material= wood.defXCMaterial()
plateSection= AWCNDS_materials.CustomLumberSection(name= wallData['plateSection'], b= 5.5*units_utils.inchToMeter, h= 1.5*units_utils.inchToMeter, woodMaterial= wood)


# Reduction in uniform live loads.
liveLoadReductionFactor= wallData['liveLoadReductionFactor'] 

# Actions
## Load definition (values from truss_AB_reactions.ods)
deadLoad= 4.65e3 # kN/truss
liveLoad= liveLoadReductionFactor*7.98e3 # kN/truss
snowLoad= 3.44e3 # kN/truss
windLoad= -2.17e3 # kN/truss
loadDict= {'deadLoad':deadLoad, 'liveLoad':liveLoad, 'snowLoad':snowLoad, 'windLoad':windLoad}

# Load combination definition
combContainer= combs.CombContainer()
combData= wallData['loadCombinations']                
for combName in combData:
    combExpr= combData[combName]
    combContainer.SLS.qp.add(combName,combExpr)


doublePlate= DoublePlate(title= title, plateSection= plateSection, studSpacing= studSpacing, trussSpacing= trussSpacing, pointLoadFactor= 1.0/3.0, loadCombDurationFactorFunction= getLoadCombDurationFactor);

results, worstResults= doublePlate.check(loadDict, combContainer)

# worst cases.
worstDeflectionCase= worstResults['worstDeflectionCase']
worstDeflectionValue= worstResults['worstDeflectionValue']
worstBendingCase= worstResults['worstBendingCase']
worstBendingCF= worstResults['worstBendingCF']
worstShearCase= worstResults['worstShearCase']
worstShearCF= worstResults['worstShearCF']
worstPerpComprCase= worstResults['worstPerpComprCase']
worstPerpComprCF= worstResults['worstPerpComprCF']

worstCasesOk= (worstDeflectionCase=='EQ1611')
worstCasesOk= worstCasesOk and (worstBendingCase=='EQ1611')
worstCasesOk= worstCasesOk and (worstShearCase=='EQ1611')
worstCasesOk= worstCasesOk and (worstPerpComprCase=='EQ1611')

ratio1= abs(worstDeflectionValue-0.0006571529990458183)/0.0006571529990458183
ratio2= abs(worstBendingCF-0.8454475777931175)/0.8454475777931175
ratio3= abs(worstShearCF-0.6582678785975511)/0.6582678785975511
ratio4= abs(worstPerpComprCF-1.0306325564675434)/1.0306325564675434

doublePlate.printResults(combContainer, results)
print('worstDeflectionCase=', worstDeflectionCase)
print('worstDeflectionValue=', worstDeflectionValue)
print('worstBendingCase=', worstBendingCase)
print('worstBendingCF=', worstBendingCF)
print('worstShearCase=', worstShearCase)
print('worstShearCF=', worstShearCF)
print('worstPerpComprCase=', worstPerpComprCase)
print('worstPerpComprCF=', worstPerpComprCF)


