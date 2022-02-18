# -*- coding: utf-8 -*-

exec(open("./xc_model.py").read()) #FE model generation
from postprocess.config import default_config
from postprocess import limit_state_data as lsd

# Compute internal forces.

## Set combinations to compute.
loadCombinations= preprocessor.getLoadHandler.getLoadCombinations

## Limit states to calculate internal forces for.
limitStates= [lsd.normalStressesResistance, # Normal stresses resistance.
lsd.shearResistance, ]

# calcSet= modelSpace.defSet('calcSet')
# for l in xcTotalSet.getLines:
#     for e in l.elements:
#         calcSet.elements.append(e)
 
## Compute internal forces for each combination
for ls in limitStates:
    ls.saveAll(combContainer, ndsCalcSet)
outCfg= lsd.VerifOutVars(setCalc= ndsCalcSet, appendToResFile='Y', listFile='N', calcMeanCF='Y')
limitState= lsd.normalStressesResistance
outCfg.controller= nds.BiaxialBendingNormalStressController(limitState.label)
average= limitState.runChecking(outCfg)

#########################################################
# Graphic stuff.
from postprocess import output_handler
oh= output_handler.OutputHandler(modelSpace)

#oh.displayElementValueDiagram('chiLT', setToDisplay= ndsCalcSet)

oh.displayBeamResult(attributeName=lsd.normalStressesResistance.label, itemToDisp='CF', beamSetDispRes=ndsCalcSet, setToDisplay=xcTotalSet)
