# -*- coding: utf-8 -*-
from postprocess.xcVtk.FE_model import vtk_FE_graphic
from postprocess.config import default_config

# import local modules
import sys
workingDirectory= default_config.findWorkingDirectory()+'/' #search env_config.py
sys.path.append(workingDirectory)
import model_gen as model #FE model generation

setsTodisp=[model.decklv1,model.decklv2,model.foot,model.wall,model.columnZconcr,model.columnZsteel,model.beamY,model.beamXconcr,model.beamXsteel]

model.out.displayFEMesh(setsToDisplay=setsTodisp,caption=None,fileName=None,defFScale=0.0)

