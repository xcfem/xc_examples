# -*- coding: utf-8 -*-
from postprocess import limit_state_data as lsd
from materials.ec3 import EC3_limit_state_checking as EC3lscheck
from postprocess.config import default_config
from postprocess.config import default_config

#  *** Verificacion of shear ULS for structural steel ***

# local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import env_config as env
import xc_model as model
import steel_beams_def as sMemb # steel members

# Verificacion of shear ULS for structural steel
lsd.LimitStateData.envConfig= env.cfg

setCalc=model.allSteel
# variables that control the output of the checking (setCalc,
# appendToResFile .py [defaults to 'N'], listFile .tex [defaults to 'N']
outCfg= lsd.VerifOutVars(setCalc=setCalc,appendToResFile='Y',listFile='N',calcMeanCF='Y')

limitState=lsd.shearResistance
outCfg.controller= EC3lscheck.ShearController(limitState.label)
a=limitState.runChecking(outCfg)


