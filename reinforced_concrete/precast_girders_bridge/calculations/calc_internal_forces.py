# -*- coding: utf-8 -*-
from postprocess import limit_state_data as lsd
from postprocess.config import default_config

exec(default_config.compileCode('../xc_model.py'))
print('model built')
# Load combinations
exec(cfg.compileCode('load_combinations.py'))

concreteAge= 1e4 # Concrete age in days at the moment considered.
deckConcreteAgeAtLoading= 28 # Age of the deck concrete in days at loading.
girdersConcreteAgeAtLoading= deckConcreteAgeAtLoading+28 # Age of the girders concrete in days at loading.
HR= 0.25 # Ambient relative humidity
exec(cfg.compileCode('loads.py'))

lsd.LimitStateData.setEnvConfig(cfg)

#Set of entities for which checking is going to be performed.
setCalc= concreteSet

#Limit states to calculate internal forces for.
limitStates= [lsd.normalStressesResistance, # Normal stresses resistance.
#lsd.shearResistance, # Shear stresses resistance (IS THE SAME AS NORMAL STRESSES, THIS IS WHY IT'S COMMENTED OUT).
lsd.freqLoadsCrackControl, # RC crack control under frequent loads
lsd.quasiPermanentLoadsCrackControl, # RC crack control under quasi-permanent loads
#lsd.fatigueResistance # Fatigue resistance.
]

initStateStorage= InitialStateStorage()
lsd.normalStressesResistance.woodArmerAlsoForAxialForces= True
for ls in limitStates:
    lmsg.log(ls.label+'; use Wood-Armer method also for axial forces: '+str(ls.woodArmerAlsoForAxialForces))
    initStateStorage.computeResponses(combContainer, displayFunction= None, limitState= ls, setCalc= setCalc)

