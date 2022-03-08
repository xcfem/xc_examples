# -*- coding: utf-8 -*-

exec(open("./xc_model.py").read()) #FE model generation

# Install recorder.
for member in ndsMembers:
    member.installULSControlRecorder(recorderType="element_prop_recorder", calcSet= ndsCalcSet)
 

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
limitState= lsd.shearResistance
outCfg.controller= nds.ShearController(limitState.label)
average= limitState.runChecking(outCfg)

#########################################################
# Graphic stuff.
from postprocess import output_handler
oh= output_handler.OutputHandler(modelSpace)

#oh.displayElementValueDiagram('chiLT', setToDisplay= ndsCalcSet)

oh.displayBeamResult(attributeName=lsd.shearResistance.label, itemToDisp='CF', beamSetDispRes=ndsCalcSet, setToDisplay=xcTotalSet)
