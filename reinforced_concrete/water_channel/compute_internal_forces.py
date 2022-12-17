# -*- coding: utf-8 -*-
import sys
from postprocess import limit_state_data as lsd
from postprocess.config import default_config
from misc_utils import log_messages as lmsg

import xc_model # Import finite element model.

lsd.LimitStateData.envConfig= xc_model.cfg

#Set of entities for which checking is going to be performed.
setCalc= xc_model.concreteSet

#Limit states to calculate internal forces for.
limitStates= [lsd.normalStressesResistance, # Normal stresses resistance.
#lsd.shearResistance, # Shear stresses resistance (IS THE SAME AS NORMAL STRESSES, THIS IS WHY IT'S COMMENTED OUT).
lsd.freqLoadsCrackControl, # RC crack control under frequent loads
lsd.quasiPermanentLoadsCrackControl, # RC crack control under quasi-permanent loads
#lsd.fatigueResistance # Fatigue resistance.
]

lmsg.setLevel(lmsg.INFO)
for ls in limitStates:
    lmsg.log(ls.label+'; use Wood-Armer method also for axial forces: '+str(ls.woodArmerAlsoForAxialForces))
    ls.saveAll(xc_model.combContainer,setCalc)
