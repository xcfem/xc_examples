# -*- coding: utf-8 -*-
''' Analyze simple load cases.'''
from postprocess.config import default_config

exec(default_config.compileCode('../xc_model.py'))
print('model built')
# Load combinations
exec(cfg.compileCode('load_combinations.py'))


def displayResults():
    ''' Display some analysis results.'''
    #oh.displayLoads()
    #oh.displayReactions()
    oh.displayDispRot(itemToDisp='uZ')
    oh.displayDispRot(itemToDisp='uX')
    oh.displayDispRot(itemToDisp='uY')
    #oh.displayIntForc(itemToDisp= 'N1', setToDisplay= concreteSet)
    #oh.displayIntForc(itemToDisp= 'N2', setToDisplay= concreteSet)
    #oh.displayLocalAxes(setToDisplay= concreteSet)

concreteAge= 1e4 # Concrete age in days at the moment considered.
deckConcreteAgeAtLoading= 28 # Age of the deck concrete in days at loading.
girdersConcreteAgeAtLoading= deckConcreteAgeAtLoading+28 # Age of the girders concrete in days at loading.
HR= 0.25 # Ambient relative humidity
exec(cfg.compileCode('loads.py'))


# Initial state
## Solve for initial state.
initialReactions= dict()

## Compute and save initial state.
# result= initial_state()
# db= modelSpace.getNewDatabase('../aux1/initial_state.db')
# modelSpace.save(100)

initStateStorage= InitialStateStorage()

# Compute ELS response
#initStateStorage.computeResponses(combContainer.SLS.qp, displayFunction= displayResults())
initStateStorage.computeResponses(combContainer.SLS.rare, displayFunction= displayResults())
#initStateStorage.computeResponses(combContainer.SLS.freq, displayFunction= displayResults())
