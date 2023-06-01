# -*- coding: utf-8 -*-
from materials.sia262 import SIA262_limit_state_checking
from misc_utils import log_messages as lmsg
from postprocess.config import default_config

# local modules
import sys
workingDirectory= default_config.findWorkingDirectory()+'/' #search env_config.py
sys.path.append(workingDirectory)
import env_config as env

lsd.LimitStateData.envConfig= env.cfg

lmsg.warning('Implementation pending. Do not use.')
quit()
# variables that control the output of the checking (setCalc,
# appendToResFile .py [defaults to 'N'], listFile .tex [defaults to 'N']
outCfg= lsd.VerifOutVars(setCalc=beamX,appendToResFile='N',listFile='N')

#Reinforced concrete sections on each element.
reinfConcreteSections= RC_material_distribution.loadRCMaterialDistribution()

limitStateLabel= lsd.fatigueResistance.label
outCfg.controller= SIA262_limit_state_checking.FatigueController(limitStateLabel)
lsd.fatigueResistance.check(reinfConcreteSections,outCfg)


