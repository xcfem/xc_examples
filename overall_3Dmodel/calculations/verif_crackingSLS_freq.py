# -*- coding: utf-8 -*-
from postprocess import limit_state_data as lsd
from postprocess import RC_material_distribution
from materials.sia262 import SIA262_limit_state_checking as lscheck  #Checking material for cracking limit state according to SIA262
from postprocess.config import default_config

# local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import env_config as env
import xc_model as model #FE model generation


# Verificacion of cracking SLS under frequent loads for reinf. concrete elements
lsd.LimitStateData.envConfig= env.cfg #configuration defined in script
                                  #env_config.py


# variables that control the output of the checking (setCalc,
# appendToResFile .py [defaults to 'N'], listFile .tex [defaults to 'N']
setCalc=model.allConcrete
outCfg= lsd.VerifOutVars(setCalc=setCalc,appendToResFile='N',listFile='N',calcMeanCF='N')

#Reinforced concrete sections on each element.
reinfConcreteSections= RC_material_distribution.loadRCMaterialDistribution()

#Checking material for limit state.
limitStress= 350e6 #XXX
limitState= lsd.freqLoadsCrackControl
outCfg.controller= lscheck.CrackControlSIA262PlanB(limitState.label,limitStress)
lsd.freqLoadsCrackControl.check(reinfConcreteSections,outCfg)




