# -*- coding: utf-8 -*-
from postprocess import limit_state_data as lsd
from postprocess.config import default_config
from postprocess import RC_material_distribution

from materials.ehe import EHE_limit_state_checking as lscheck

exec(default_config.compileCode('../xc_model.py'))
print('model built')
lsd.LimitStateData.envConfig=cfg

#
#
#Reinforced concrete sections on each element.
reinfConcreteSections= RC_material_distribution.loadRCMaterialDistribution()

#stcalc=modelSpace.setSum('stCalc',[setArmadosEstr,pilesAbut])
#stcalc= bridgeDeckSet
stcalc= concreteSet
#stcalc= websLowerEdge
#stcalc= girderWebs

# variables that control the output of the checking (setCalc,
# appendToResFile .py [defaults to 'N'], listFile .tex [defaults to 'N']
outCfg= lsd.VerifOutVars(setCalc=stcalc,appendToResFile='N',listFile='N',calcMeanCF='N')

limitState=lsd.normalStressesResistance
outCfg.controller= lscheck.BiaxialBendingNormalStressController(limitState.label)
lsd.normalStressesResistance.check(reinfConcreteSections,outCfg)

