# -*- coding: utf-8 -*-
from postprocess import limit_state_data as lsd
from postprocess.config import default_config

# local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import env_config as env
import model_gen as model
import steel_beams_def as sMemb # steel members

lsd.LimitStateData.envConfig= env.cfg

#Reinforced concrete sections on each element.
#reinfConcreteSections= RC_material_distribution.loadRCMaterialDistribution()

#Set of entities for which checking is going to be performed.
setCalc= model.allConcrete
setCalc=model.overallSet
loadCombinations= model.prep.getLoadHandler.getLoadCombinations

#Limit states to calculate internal forces for.
limitStates= [lsd.steelNormalStressesResistance, # Normal stresses resistance.
lsd.steelShearResistance, # Shear stresses resistance (IS THE SAME AS NORMAL STRESSES, THIS IS WHY IT'S COMMENTED OUT).
lsd.freqLoadsCrackControl, # RC crack control under frequent loads
lsd.quasiPermanentLoadsCrackControl, # RC crack control under quasi-permanent loads
#lsd.fatigueResistance # Fatigue resistance.
] 

# add the effect of the in-plane Vxy forces to the axial internal forces 
#lsd.normalStressesResistance.woodArmerAlsoForAxialForces= True

for ls in limitStates:
    ls.saveAll(
        combContainer=model.combContainer,
        setCalc=setCalc,bucklingMembers=[sMemb.col01a,sMemb.col01b,sMemb.col02a,sMemb.col02b,sMemb.col03,sMemb.beam01]
    )
    print('combinations for ', ls.label, ': ', loadCombinations.getKeys())
