# -*- coding: utf-8 -*-
from postprocess import limit_state_data as lsd
from postprocess import RC_material_distribution
from solution import predefined_solutions
from materials.ehe import EHE_limit_state_checking as lschck  #Checking material for shear limit state according to EHE08
#from materials.sia262 import SIA262_limit_state_checking as lschck  #Checking material for shear limit state according to SIA262
from postprocess.config import default_config

#   *** Verificacion of shear ULS for reinf. concrete elements ***

# local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import env_config as env
import xc_model as model

# Verificacion of shear ULS for reinf. concrete elements
lsd.LimitStateData.envConfig= env.cfg #configuration defined in script
                                  #env_config.py

#Reinforced concrete sections on each element.
reinfConcreteSections= RC_material_distribution.loadRCMaterialDistribution()

# variables that control the output of the checking (setCalc,
# appendToResFile .py [defaults to 'N'], listFile .tex [defaults to 'N']
setCalc=model.allConcrete

class CustomSolver(predefined_solutions.PlainNewtonRaphsonMUMPS):

    def __init__(self, prb):
        super(CustomSolver,self).__init__(prb= prb, name= 'test', maxNumIter= 20, printFlag= 1, convergenceTestTol= 1e-3)

limitState= lsd.shearResistance
# create limit state controller.
controller= lschck.ShearController(limitState.label, solutionProcedureType= CustomSolver)
# Check limit state.
# variables that control the output of the checking (setCalc,
# appendToResFile .py [defaults to 'N'], listFile .tex [defaults to 'N']
limitState.check(crossSections= reinfConcreteSections,setCalc=setCalc,appendToResFile='N',listFile='N', controller= controller)








