# -*- coding: utf-8 -*-
''' Analyze simple load cases.'''
from postprocess.config import default_config

exec(default_config.compileCode('../xc_model.py'))
print('model built')
import csv

def displayResults():
    ''' Display some analysis results.'''
    #oh.displayLoads()
    oh.displayReactions(reactionCheckTolerance= reactionCheckTol)
    #oh.displayDispRot(itemToDisp='uZ')
    oh.displayDispRot(itemToDisp='uX')
    #oh.displayDispRot(itemToDisp='uY')
    #oh.displayIntForc(itemToDisp= 'N1', setToDisplay= girderWebs)
    #oh.displayIntForc(itemToDisp= 'N2', setToDisplay= girderWebs)
    #oh.displayLocalAxes(setToDisplay= concreteSet)

concreteAge= 1e4 # Concrete age in days at the moment considered.
deckConcreteAgeAtLoading= 28 # Age of the deck concrete in days at loading.
girdersConcreteAgeAtLoading= deckConcreteAgeAtLoading+28 # Age of the girders concrete in days at loading.
HR= 0.25 # Ambient relative humidity
exec(cfg.compileCode('loads.py'))

#loadCasesToAnalyze= ['G2', 'Q1a1', 'Q1a2', 'Q1b1', 'Q1b2', 'Q1b1F', 'Q1b2F', 'Q21', 'Q22', 'Q31', 'Q31neopr', 'Q32', 'Q32neopr']
loadCasesToAnalyze= ['Q31', 'Q32']

initStateStorage= InitialStateStorage()

f= open('reactions.csv', 'w')
writer= csv.writer(f)


# Initial state
## Solve for initial state.
initialReactions= dict()

## Compute and save initial state.
initStateComb= "1.00*G1 + 1.00*G2 + 1.00*G3 + 1.00*P1"
initStateStorage.solve('initComb', initStateComb)

for n in fixedNodeSet.nodes:
    Rx= n.getReaction[0]
    Ry= n.getReaction[1]
    Rz= n.getReaction[2]
    writer.writerow(['init', n.tag, round(Rx/1e3,2), round(Ry/1e3,2), round(Rz/1e3,2)])
    initialReactions[n.tag]= [Rx,Ry,Rz]

for lcName in loadCasesToAnalyze:
    combName= lcName+'cmb'
    combExpr= initStateComb+'+1.00*'+lcName
    print(combExpr)
    result= initStateStorage.solve(combName, combExpr)
    if(result!= 0):
        lmsg.error('Error when solving for: '+lcName+'(analOk='+str(result)+')')
        quit()
    displayResults()
    for n in fixedNodeSet.nodes:
        R0= initialReactions[n.tag]
        Rx= n.getReaction[0]-R0[0]
        Ry= n.getReaction[1]-R0[1]
        Rz= n.getReaction[2]-R0[2]
        writer.writerow([lcName, n.tag, round(Rx/1e3,2), round(Ry/1e3,2), round(Rz/1e3,2)])
    modelSpace.removeAllLoadPatternsFromDomain()
f.close()
