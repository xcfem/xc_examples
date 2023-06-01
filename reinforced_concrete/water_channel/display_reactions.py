# -*- coding: utf-8 -*-
import sys

import xc_model # Import finite element model.

setsToDisplay= [xc_model.xcTotalSet]

xc_model.modelSpace.displayReactions(oh= xc_model.oh, setsToDisplay= setsToDisplay, combContainer= xc_model.combContainer)

