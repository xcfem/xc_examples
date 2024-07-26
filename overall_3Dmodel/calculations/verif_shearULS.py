# -*- coding: utf-8 -*-
from postprocess import limit_state_data as lsd
from postprocess import RC_material_distribution
from materials.ehe import EHE_limit_state_checking as lschck  #Checking material for shear limit state according to EHE08
#from materials.sia262 import SIA262_limit_state_checking as lschck  #Checking material for shear limit state according to SIA262
from postprocess.config import default_config

#   *** Verificacion of shear ULS for reinf. concrete elements ***

# local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import env_config as env
import model_gen as model

# Verificacion of shear ULS for reinf. concrete elements
lsd.LimitStateData.envConfig= env.cfg #configuration defined in script
                                  #env_config.py

#Reinforced concrete sections on each element.
reinfConcreteSections= RC_material_distribution.loadRCMaterialDistribution()

# variables that control the output of the checking (setCalc,
# appendToResFile .py [defaults to 'N'], listFile .tex [defaults to 'N']
setCalc=model.allConcrete
outCfg= lsd.VerifOutVars(setCalc=setCalc,appendToResFile='N',listFile='N')

limitState= lsd.shearResistance
outCfg.controller= lschck.ShearController(limitState.label)
limitState.check(reinfConcreteSections,outCfg)







