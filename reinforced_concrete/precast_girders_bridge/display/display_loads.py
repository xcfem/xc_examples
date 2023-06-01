# -*- coding: utf-8 -*-
from postprocess.config import default_config

exec(default_config.compileCode('../xc_model.py'))

from solution import predefined_solutions
exec(cfg.compileCode('loads.py'))

#loadCasesToDisplay= ['Q1a1','Q1a2','Q1b1','Q1b2','Q1b1F','Q1b2F']
loadCasesToDisplay= loadCaseNames

for l in loadCasesToDisplay:
    modelSpace.removeAllLoadPatternsFromDomain()
    modelSpace.revertToStart()
    lp= modelSpace.addLoadCaseToDomain(l)
    oh.displayLoadVectors() #setToDisplay= purlinSet)
    oh.displayLoads() #setToDisplay= purlinSet)
