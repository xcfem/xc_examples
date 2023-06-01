# -*- coding: utf-8 -*-
from postprocess.config import default_config

exec(default_config.compileCode('../xc_model.py'))

setsToDisplay= girderSets+bridgeDeckSets


oh.displayFEMesh(setsToDisplay= setsToDisplay)

# for s in setsToDisplay:
#     oh.displayFEMesh(setsToDisplay= [s])

#oh.displayFEMesh(setsToDisplay= [bridgeDeckSet])
