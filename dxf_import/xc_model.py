# -*- coding: utf-8 -*-
import math
import geom
import xc

test= xc.FEProblem()
exec(open('./xc_model_blocks.py').read())

xcTotalSet= preprocessor.getSets.getSet('total')

