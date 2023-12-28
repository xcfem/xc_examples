# -*- coding: utf-8 -*-
''' Non-linear analysis. Steel must be previously set J2PlateFibre and
shell elements as MembranePlateFiberSection.
'''

from postprocess import limit_state_data as lsd
from postprocess.config import default_config

workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import env_config as env
import mesh_gen as msh
import limit_states_def as lstts

lsd.LimitStateData.envConfig= env.cfg

#Reinforced concrete sections on each element.
#reinfConcreteSections= RC_material_distribution.loadRCMaterialDistribution()

#Set of entities for which checking is going to be performed.
setCalc= msh.tank

loadCombinations= msh.prep.getLoadHandler.getLoadCombinations

#Limit states to calculate internal forces for.
von_mises_limit_state=lsd.vonMisesStressResistance
von_mises_limit_state.vonMisesStressId= 'avg_von_mises_stress'
limitStates= [von_mises_limit_state,
#lsd.normalStressesResistance, # Normal stresses resistance.
#lsd.shearResistance, # Shear stresses resistance (IS THE SAME AS NORMAL STRESSES, THIS IS WHY IT'S COMMENTED OUT).
#lsd.freqLoadsCrackControl, # RC crack control under frequent loads
#lsd.quasiPermanentLoadsCrackControl, # RC crack control under quasi-permanent loads
#lsd.fatigueResistance # Fatigue resistance.
] 

#limitStates= [lsd.freqLoadsCrackControl]

# Nonlinear analysis
from solution import predefined_solutions
class CustomPenaltyModifiedNewton(predefined_solutions.PenaltyModifiedNewton):
    def __init__(self, prb):
        super(CustomPenaltyModifiedNewton, self).__init__(prb, maxNumIter=100, convergenceTestTol= 1.0e-2, printFlag= 2)

### Compute internal forces for each combination
for ls in limitStates:
    ls.saveAll(lstts.combContainer,setCalc,solutionProcedureType= CustomPenaltyModifiedNewton)
    print ('combinations for ', ls.label, ': ', loadCombinations.getKeys())

