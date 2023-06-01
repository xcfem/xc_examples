# -*- coding: utf-8 -*-
from postprocess import limit_state_data as lsd
from postprocess.config import default_config
from postprocess import RC_material_distribution

from materials.sia262 import SIA262_limit_state_checking as lscheck  #Checking material for cracking limit state according to SIA262

exec(default_config.compileCode('../xc_model.py'))
print('model built')
lsd.LimitStateData.envConfig=cfg
#
#
#
#Reinforced concrete sections on each element.
reinfConcreteSections= RC_material_distribution.loadRCMaterialDistribution()

#stcalc=modelSpace.setSum('stCalc',[setArmadosEstr,pilesAbut])
#stcalc= bridgeDeckSet
#stcalc= concreteSet
#stcalc= girderBottomFlanges
stcalc= girderWebs

# variables that control the output of the checking (setCalc,
# appendToResFile .py [defaults to 'N'], listFile .tex [defaults to 'N']
outCfg= lsd.VerifOutVars(setCalc=stcalc,appendToResFile='N',listFile='N',calcMeanCF='N')

#Checking material for limit state.
limitStress= 350e6 #XXX
limitState= lsd.freqLoadsCrackControl
outCfg.controller= lscheck.CrackControlSIA262PlanB(limitState.label,limitStress)
lsd.freqLoadsCrackControl.check(reinfConcreteSections,outCfg)

