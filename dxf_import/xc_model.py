# -*- coding: utf-8 -*-
import math
import xc_base
import geom
import xc

test= xc.FEProblem()
execfile('./xc_model_blocks.py')

xcTotalSet= preprocessor.getSets.getSet('total')

