# -*- coding: utf-8 -*-
from postprocess import limit_state_data as lsd
from materials.astm_aisc import AISC_limit_state_checking as aisc
from postprocess.config import default_config
from actions import combinations as combs

#Verification of Von Mises stresses

workingDirectory= default_config.setWorkingDirectory()
import model_gen_imperf #FE model generation

for e in tank.elements: e.setProp('yieldStress', AISI_fy)

setCalc=tank


lsd.LimitStateData.setEnvConfig(cfg_imperf)

limitState= lsd.vonMisesStressResistance
limitState.vonMisesStressId= 'avg_von_mises_stress'
### Check material resistance.
outCfg= lsd.VerifOutVars(setCalc=setCalc, appendToResFile='N', listFile='N', calcMeanCF='Y')
outCfg.controller= aisc.VonMisesStressController(limitState.label)
average= limitState.runChecking(outCfg)

'''
from postprocess import output_handler
oh= output_handler.OutputHandler(modelSpace)
#oh.displayFEMesh()
oh.displayField(limitStateLabel= limitState.label, section= None, argument= 'CF', component= None, setToDisplay= None, fileName= None)
'''
#oh.displayLoads()
#oh.displayDispRot('uY')
#oh.displayStrains('epsilon_xx')
#oh.displayStresses('sigma_11')
#oh.displayVonMisesStresses(vMisesCode= 'max_von_mises_stress')
