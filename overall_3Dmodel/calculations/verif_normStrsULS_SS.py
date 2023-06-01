# -*- coding: utf-8 -*-
#Verification of ULS normal-stresses for structural steel

from postprocess import limit_state_data as lsd
from materials.ec3 import EC3_limit_state_checking as EC3lscheck
from postprocess.config import default_config

# local modules
import sys
workingDirectory= default_config.findWorkingDirectory()+'/' #search env_config.py
sys.path.append(workingDirectory)
import env_config as env
import steel_beams_def as sMemb # steel members

#Verification of normal-stresses ULS for structural steel
lsd.LimitStateData.envConfig= env.cfg #configuration defined in script
                                  #env_config.py

setCalc=beamXsteel+columnZsteel
# variables that control the output of the checking (setCalc,
# appendToResFile .py [defaults to 'N'], listFile .tex [defaults to 'N']
outCfg= lsd.VerifOutVars(setCalc=setCalc,appendToResFile='Y',listFile='N',calcMeanCF='Y')

limitState=lsd.normalStressesResistance
outCfg.controller= EC3lscheck.BiaxialBendingNormalStressController(limitState.label)
mean=limitState.runChecking(outCfg)


