# -*- coding: utf-8 -*-
from solution import predefined_solutions
from postprocess import limit_state_data as lsd
from postprocess import RC_material_distribution
from materials.ehe import EHE_limit_state_checking as lschck
#from materials.ec2 import EC2_limit_state_checking
from postprocess.config import default_config

# local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import env_config as env

import model_gen as model #FE model generation

# Verificacion of cracking SLS under frequent loads for reinf. concrete
# elements, taking account of tension-stiffening

lsd.LimitStateData.envConfig= env.cfg #configuration defined in script
                                  #env_config.py

# variables that control the output of the checking (setCalc,
# appendToResFile .py [defaults to 'N'], listFile .tex [defaults to 'N']
outCfg= lsd.VerifOutVars(setCalc=beamX,appendToResFile='N',listFile='N')

#Reinforced concrete sections on each element.
#reinfConcreteSections=RC_material_distribution.RCMaterialDistribution()
reinfConcreteSections=RC_material_distribution.loadRCMaterialDistribution()
reinfConcreteSections.mapSectionsFileName='./mapSectionsReinforcementTenStiff.pkl'
#Checking material for limit state.
limitStateLabel= lsd.freqLoadsCrackControl.label
outCfg.controller= lschck.CrackStraightController(limitStateLabel= lsd.freqLoadsCrackControl.label)
outCfg.controller.solutionProcedureType= predefined_solutions.PlainStaticModifiedNewton
meanFCs= lsd.freqLoadsCrackControl.check(reinfConcreteSections,outCf)



