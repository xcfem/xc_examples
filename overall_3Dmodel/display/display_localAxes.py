# -*- coding: utf-8 -*-
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import quick_graphics as qg
from postprocess.config import default_config

# local modules
import sys
workingDirectory= default_config.findWorkingDirectory()+'/' #search env_config.py
sys.path.append(workingDirectory)
import env_config as env
import model_gen as model #FE model generation

setToDisp=model.allBeams
model.out.displayLocalAxes(setToDisplay=setToDisp,caption=None,fileName=None,defFScale=0.0)





