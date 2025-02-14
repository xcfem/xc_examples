# -*- coding: utf-8 -*-

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AO_O)"
__copyright__= "Copyright 2022, LCPT and AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es ana.ortega@ciccp.es"

import math
import loadCombinations
from actions.load_combination_utils import ec0_es # Eurocode 0 Spanish annex.
# from actions.load_combination_utils import utils
# from misc_utils import log_messages as lmsg

frameCombinations= True # Compute combinations for frame structures.

lcg= ec0_es.bridgeCombGenerator
safetyFactorSet= 'B' # Table A2.4(B)
# Permanent load.
G= lcg.newSelfWeightAction(actionName=  'G', actionDescription= 'Peso propio.', safetyFactorSet= safetyFactorSet)
# Earth pressure.
E= lcg.newEarthPressureAction(actionName=  'E', actionDescription= 'Empuje de tierras.', safetyFactorSet= safetyFactorSet)
# Hidrostatic pressure.
W= lcg.newHydrostaticPressureAction(actionName= 'W', actionDescription= 'Presión hidrostática', context= 'road_bridge', safetyFactorSet= safetyFactorSet)
# Uniform traffic load.
T= lcg.newUniformLoadAction(actionName= 'T', actionDescription= 'Carga de tráfico.', safetyFactorSet= safetyFactorSet)

# Write the combinations to a file.
lcg.computeCombinations()
combContainer= lcg.getCombContainer()
outputFileName= 'channel_load_combinations.py'
with open(outputFileName,'w') as outputFile:
    combContainer.writePythonScript(containerName= 'combContainer', os= outputFile)

