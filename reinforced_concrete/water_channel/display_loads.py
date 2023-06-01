# -*- coding: utf-8 -*-
import sys
from postprocess.config import default_config
from misc_utils import log_messages as lmsg

import xc_model # Import finite element model.

loadCasesToDisplay= xc_model.loadCaseNames
setsToDisplay= [xc_model.xcTotalSet]

xc_model.modelSpace.displayLoads(oh= xc_model.oh, loadCasesToDisplay= loadCasesToDisplay, setsToDisplay= setsToDisplay)
