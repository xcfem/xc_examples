# -*- coding: utf-8 -*-
from postprocess.config import default_config

# local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import xc_init
import xc_geom as xcG #FE model generation
import xc_materials as xcM # Materials
import xc_fem as xcF # FE model

out=xc_init.out

setToDisp=xcG.allBeams
out.displayLocalAxes(setToDisplay=setToDisp,caption=None,fileName=None,defFScale=0.0)





