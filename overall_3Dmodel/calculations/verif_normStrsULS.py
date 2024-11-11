# -*- coding: utf-8 -*-
from postprocess import limit_state_data as lsd
from postprocess import RC_material_distribution
from materials.sia262 import SIA262_limit_state_checking as lscheck
from postprocess.config import default_config

#   *** Verification of normal-stresses ULS for reinf. concrete elements***

# local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import env_config as env
import xc_model as model

#Verification of normal-stresses ULS for reinf. concrete elements
lsd.LimitStateData.envConfig= env.cfg  #configuration defined in script
                                   #env_config.py

#Reinforced concrete sections on each element.
reinfConcreteSections= RC_material_distribution.loadRCMaterialDistribution()

# variables that control the output of the checking (setCalc,
# appendToResFile .py [defaults to 'N'], listFile .tex [defaults to 'N']
setCalc=model.allConcrete

outCfg= lsd.VerifOutVars(setCalc=setCalc,appendToResFile='N',listFile='N',calcMeanCF='Y')

limitState=lsd.normalStressesResistance
controller= lscheck.BiaxialBendingNormalStressController(limitState.label)
mean=lsd.normalStressesResistance.check(crossSections= reinfConcreteSections, setCalc=setCalc,appendToResFile='N',listFile='N',calcMeanCF='Y', controller= controller)




