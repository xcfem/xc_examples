# -*- coding: utf-8 -*-
from postprocess import limit_state_data as lsd
from postprocess import RC_material_distribution
#from materials.sia262 import SIA262_limit_state_checking as lscheck
from materials.ehe import EHE_limit_state_checking as lscheck
from postprocess.config import default_config
# local modules
workingDirectory= default_config.setWorkingDirectory() 
import env_config as env
import xc_sets as xcS

#   *** Verification of normal-stresses ULS for reinf. concrete elements***

setCalc=xcS.mixSet
lsd.LimitStateData.setEnvConfig(env.cfg) 
reinfConcreteSections= RC_material_distribution.loadRCMaterialDistribution()
limitState=lsd.normalStressesResistance
controller= lscheck.BiaxialBendingNormalStressController(limitState.label)
mean=lsd.normalStressesResistance.check(crossSections= reinfConcreteSections, setCalc=setCalc,appendToResFile='N',listFile='N',calcMeanCF='Y', controller= controller)




