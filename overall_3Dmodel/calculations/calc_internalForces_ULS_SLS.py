# -*- coding: utf-8 -*-
from postprocess import limit_state_data as lsd
from postprocess.config import default_config
from actions import combinations as cc

# local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import env_config as env
#import steel_beams_def as sMemb # steel members
import xc_init
import xc_main_fullmodel
import xc_sets as xcS
import xc_combinations as xcC
# Common variables
modelSpace=xc_init.modelSpace ; prep=xc_init.prep ; out=xc_init.out

lsd.LimitStateData.envConfig= env.cfg

#Reinforced concrete sections on each element.
#reinfConcreteSections= RC_material_distribution.loadRCMaterialDistribution()

#Set of entities for which checking is going to be performed.
setCalc=xcS.allConcreteSet

#setCalc=model.overallSet
loadCombinations= prep.getLoadHandler.getLoadCombinations

# Limit states to calculate internal forces for.
# REINFORCED CONCRETE
limitStates= [lsd.normalStressesResistance, 
              lsd.steelShearResistance, 
              lsd.freqLoadsCrackControl,
              lsd.rareLoadsCrackControl,
              lsd.quasiPermanentLoadsCrackControl, 
              lsd.fatigueResistance,
              lsd.torsionResistance,
              ]
# STEEL
'''
limitStates= [lsd.steelNormalStressesResistance,
              lsd.steelShearResistance,
              lsd.vonMisesStressResistance
              ]
'''
# WOOD
'''
limitStates= [lsd.woodNormalStressesResistance,
              ]
'''

for ls in limitStates:
    ls.saveAll(combContainer=xcC.combContainer,setCalc=setCalc,bucklingMembers=None)
    print('combinations for ', ls.label, ': ', loadCombinations.getKeys())



# add the effect of the in-plane Vxy forces to the axial internal forces 
#lsd.normalStressesResistance.woodArmerAlsoForAxialForces= True

# for ls in limitStates:
#     ls.saveAll(
#         combContainer=model.combContainer,
#         setCalc=setCalc,bucklingMembers=[sMemb.col01a,sMemb.col01b,sMemb.col02a,sMemb.col02b,sMemb.col03,sMemb.beam01]
#     )
#     print('combinations for ', ls.label, ': ', loadCombinations.getKeys())
