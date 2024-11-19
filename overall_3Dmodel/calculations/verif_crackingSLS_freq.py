# -*- coding: utf-8 -*-
from postprocess import limit_state_data as lsd
from postprocess import RC_material_distribution
from materials.ehe import EHE_limit_state_checking as lscheck
#from materials.sia262 import SIA262_limit_state_checking as lscheck  
from solution import predefined_solutions
from postprocess.config import default_config
# local modules
workingDirectory= default_config.setWorkingDirectory() 
import env_config as env
import xc_sets as xcS

# Verificacion of cracking SLS under frequent loads for reinf. concrete elements

lsd.LimitStateData.envConfig= env.cfg 
setCalc=xcS.mixSet
limitState= lsd.freqLoadsCrackControl
# Plan B
'''
limitStress= 350e6 #XXX
controller= lscheck.CrackControlSIA262PlanB(limitState.label,limitStress)
'''
reinfConcreteSections= RC_material_distribution.loadRCMaterialDistribution()

class CustomSolver(predefined_solutions.PlainNewtonRaphsonMUMPS):
    def __init__(self, prb):
        super(CustomSolver,self).__init__(prb= prb, name= 'test', maxNumIter= 20, printFlag= 1, convergenceTestTol= 1e-3)

controller= lscheck.CrackController(limitStateLabel= limitState.label, solutionProcedureType= CustomSolver)
lsd.freqLoadsCrackControl.check(crossSections= reinfConcreteSections,setCalc=setCalc,appendToResFile='N',listFile='N',calcMeanCF='N', controller= controller)

# Plan B
'''
outCfg.controller= lscheck.CrackControlSIA262PlanB(limitState.label,limitStress)
lsd.freqLoadsCrackControl.check(reinfConcreteSections,outCfg)
'''



