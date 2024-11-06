# -*- coding: utf-8 -*-
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import quick_graphics as qg
from postprocess.config import default_config

# local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import env_config as env
import xc_model as model #FE model generation

setToDisp=model.allBeams
model.out.displayLocalAxes(setToDisplay=setToDisp,caption=None,fileName=None,defFScale=0.0)





