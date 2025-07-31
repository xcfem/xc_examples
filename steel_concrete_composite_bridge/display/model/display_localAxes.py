# -*- coding: utf-8 -*-
from postprocess.config import default_config

# local modules
workingDirectory= default_config.setWorkingDirectory()
import xc_init
import xc_sets as xcS
out=xc_init.out

setToDisp=xcS.allBeamsSet
out.displayLocalAxes(setToDisplay=setToDisp,caption=None,fileName=None,defFScale=0.0)





