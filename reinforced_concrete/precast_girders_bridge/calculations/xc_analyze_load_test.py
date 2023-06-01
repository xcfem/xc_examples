# -*- coding: utf-8 -*-
''' Analyze simple load cases.'''
from postprocess.config import default_config

exec(default_config.compileCode('../xc_model.py'))
print('model built')
import csv

def displayResults():
    ''' Display some analysis results.'''
    oh.displayLoads()
    oh.displayReactions(reactionCheckTolerance= reactionCheckTol)
    oh.displayDispRot(itemToDisp='uZ')
    #oh.displayDispRot(itemToDisp='uX')
    #oh.displayDispRot(itemToDisp='uY')
    #oh.displayIntForc(itemToDisp= 'N1', setToDisplay= concreteSet)
    #oh.displayIntForc(itemToDisp= 'N2', setToDisplay= concreteSet)
    #oh.displayLocalAxes(setToDisplay= concreteSet)

concreteAge= 1e4 # Concrete age in days at the moment considered.
deckConcreteAgeAtLoading= 28 # Age of the deck concrete in days at loading.
girdersConcreteAgeAtLoading= deckConcreteAgeAtLoading+28 # Age of the girders concrete in days at loading.
HR= 0.25 # Ambient relative humidity
exec(default_config.compileCode('../loads.py'))

## Display loads.
loadCasesToAnalyze= ['Q1b1','LTPh1','Q1b2','LTPh2']
for lcName in loadCasesToAnalyze:
    modelSpace.addLoadCaseToDomain(lcName)
    oh.displayLoads()
    modelSpace.removeLoadCaseFromDomain(lcName)

## Compute and save initial state.
initStateStorage= InitialStateStorage()
initStateComb= "1.00*G1 + 1.00*G2 + 1.00*G3 + 1.00*P1"
initStateStorage.solve('initComb', initStateComb)
displayResults()

loadCasesToAnalyze= ['Q1b1','LTPh1','Q1b2','LTPh2']
for lcName in loadCasesToAnalyze:
    combName= lcName+'cmb'
    combExpr= initStateComb+'+1.00*'+lcName
    print(combExpr)
    result= initStateStorage.solve(combName, combExpr)
    if(result!= 0):
        lmsg.error('Error when solving for: '+lcName+'(analOk='+str(result)+')')
        quit()
    displayResults()
    modelSpace.removeAllLoadPatternsFromDomain()

