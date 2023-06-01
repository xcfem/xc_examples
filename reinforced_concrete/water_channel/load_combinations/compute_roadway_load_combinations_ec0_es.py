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

lcg= ec0_es.combGenerator
# Permanent load.
G= lcg.newPermanentAction(actionName=  'G', actionDescription= 'Peso propio.')
# Earth pressure.
E= lcg.newPermanentAction(actionName=  'E', actionDescription= 'Empuje de tierras.')
# Hidrostatic pressure.
W= lcg.newHydrostaticPressureAction(actionName= 'W', actionDescription= 'Presión hidrostática', context= 'road_bridge')
# Uniform traffic load.
T= lcg.newUniformLoadAction(actionName= 'T', actionDescription= 'Carga de tráfico.')

# Write the combinations to a file.
lcg.computeCombinations()
combContainer= lcg.getCombContainer()
outputFileName= 'channel_load_combinations.py'
with open(outputFileName,'w') as outputFile:
    combContainer.writePythonScript(containerName= 'combContainer', os= outputFile)

