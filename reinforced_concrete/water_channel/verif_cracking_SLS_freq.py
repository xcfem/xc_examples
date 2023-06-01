# -*- coding: utf-8 -*-
import sys
from postprocess.config import default_config
from postprocess import limit_state_data as lsd
from postprocess import RC_material_distribution

from materials.sia262 import SIA262_limit_state_checking as lscheck  #Checking material for cracking limit state according to SIA262

import xc_model # Import finite element model.

lsd.LimitStateData.envConfig= xc_model.cfg

#Reinforced concrete sections on each element.
reinfConcreteSections= RC_material_distribution.loadRCMaterialDistribution()

#Set of entities for which checking is going to be performed.
setCalc= xc_model.concreteSet

# variables that control the output of the checking (setCalc,
# appendToResFile .py [defaults to 'N'], listFile .tex [defaults to 'N']
outCfg= lsd.VerifOutVars(setCalc=setCalc,appendToResFile='N',listFile='N',calcMeanCF='N')

#Checking material for limit state.
limitStress= 350e6 #XXX
limitState= lsd.freqLoadsCrackControl
outCfg.controller= lscheck.CrackControlSIA262PlanB(limitState.label,limitStress)
lsd.freqLoadsCrackControl.check(reinfConcreteSections,outCfg)

