# -*- coding: utf-8 -*-
from postprocess import limit_state_data as lsd
from postprocess.config import default_config
from postprocess import RC_material_distribution

from materials.ehe import EHE_limit_state_checking as lscheck

exec(default_config.compileCode('../xc_model.py'))
print('model built')
lsd.LimitStateData.setEnvConfig(cfg)
#
from shutil import copyfile
internalForcesPath= cfg.projectDirTree.getInternalForcesResultsPath()

copyfile(internalForcesPath+'intForce_ULS_normalStressesResistance.json', internalForcesPath+'intForce_ULS_shearResistance.json')

#
#
#Reinforced concrete sections on each element.
reinfConcreteSections= RC_material_distribution.loadRCMaterialDistribution()

#stcalc=modelSpace.setSum('stCalc',[setArmadosEstr,pilesAbut])
#stcalc= bridgeDeckSet
stcalc= concreteSet

# variables that control the output of the checking (setCalc,
# appendToResFile .py [defaults to 'N'], listFile .tex [defaults to 'N']
outCfg= lsd.VerifOutVars(setCalc=stcalc,appendToResFile='N',listFile='N',calcMeanCF='N')

limitState=lsd.shearResistance
outCfg.controller= lscheck.ShearController(limitState.label)
lsd.shearResistance.check(reinfConcreteSections,outCfg)

