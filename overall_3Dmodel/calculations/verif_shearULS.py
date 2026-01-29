# -*- coding: utf-8 -*-
from postprocess import limit_state_data as lsd
from postprocess import RC_material_distribution
from solution import predefined_solutions
from materials.ehe import EHE_limit_state_checking as lschck  
#from materials.sia262 import SIA262_limit_state_checking as lschck  
from postprocess.config import default_config
from misc_utils import log_messages as lmsg
# local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import env_config as env
import xc_sets as xcS
import shutil
shutil.copyfile(env.cfg.projectDirTree.getInternalForcesResultsPath()+'intForce_ULS_normalStressesResistance.json', env.cfg.projectDirTree.getInternalForcesResultsPath()+'intForce_ULS_shearResistance.json')
import RC_sections_def
if  RC_sections_def.plotSection:
    lmsg.error('You must disable RC-section plotting before running check')
    quit()

#   *** Verificacion of shear ULS for reinf. concrete elements ***

lsd.LimitStateData.setEnvConfig(env.cfg)
reinfConcreteSections= RC_sections_def.reinfConcreteSectionDistribution

setCalc=xcS.mixSet

class CustomSolver(predefined_solutions.PlainNewtonRaphsonMUMPS):
    def __init__(self, prb):
        super(CustomSolver,self).__init__(prb= prb, name= 'test', maxNumIter= 20, printFlag= 1, convergenceTestTol= 1e-3)

limitState= lsd.shearResistance
controller= lschck.ShearController(limitState.label, solutionProcedureType= CustomSolver)
limitState.check(crossSections= reinfConcreteSections,setCalc=setCalc,appendToResFile='N',listFile='N', controller= controller)








