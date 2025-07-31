# -*- coding: utf-8 -*-
from postprocess import limit_state_data as lsd
from postprocess import RC_material_distribution
from solution import predefined_solutions
from materials.ehe import EHE_limit_state_checking as lschck  
#from materials.sia262 import SIA262_limit_state_checking as lschck  
from postprocess.config import default_config
# local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import env_config as env
import xc_sets as xcS

#   *** Verificacion of shear ULS for reinf. concrete elements ***

lsd.LimitStateData.setEnvConfig(env.cfg)
reinfConcreteSections= RC_material_distribution.loadRCMaterialDistribution()
setCalc=xcS.mixSet

class CustomSolver(predefined_solutions.PlainNewtonRaphsonMUMPS):
    def __init__(self, prb):
        super(CustomSolver,self).__init__(prb= prb, name= 'test', maxNumIter= 20, printFlag= 1, convergenceTestTol= 1e-3)

limitState= lsd.shearResistance
controller= lschck.ShearController(limitState.label, solutionProcedureType= CustomSolver)
limitState.check(crossSections= reinfConcreteSections,setCalc=setCalc,appendToResFile='N',listFile='N', controller= controller)








