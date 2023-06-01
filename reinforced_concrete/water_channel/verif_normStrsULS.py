# -*- coding: utf-8 -*-
import sys
import math
from postprocess import limit_state_data as lsd
from postprocess.config import default_config
from postprocess import RC_material_distribution

from materials.ec2 import EC2_limit_state_checking as lscheck
from materials.ec2 import EC2_materials


import xc_model # Import finite element model.

lsd.LimitStateData.envConfig= xc_model.cfg

#Reinforced concrete sections on each element.
reinfConcreteSections= RC_material_distribution.loadRCMaterialDistribution()

#Set of entities for which checking is going to be performed.
setCalc= xc_model.concreteSet

# variables that control the output of the checking (setCalc,
# appendToResFile .py [defaults to 'N'], listFile .tex [defaults to 'N']
outCfg= lsd.VerifOutVars(setCalc=setCalc,appendToResFile='N',listFile='N',calcMeanCF='N')
limitState=lsd.normalStressesResistance
outCfg.controller= lscheck.BiaxialBendingNormalStressController(limitState.label)
lsd.normalStressesResistance.check(reinfConcreteSections,outCfg)
