# -*- coding: utf-8 -*-
from postprocess.xcVtk.FE_model import vtk_FE_graphic
from postprocess.config import default_config

# import local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import xc_init
import xc_geom as xcG #FE model generation
import xc_materials as xcM # Materials
import xc_fem as xcF # FE model

out=xc_init.out

setsTodisp=[xcG.decklv1,xcG.decklv2,xcG.foot,xcG.wall,xcG.columnZconcr,xcG.columnZsteel,xcG.beamY,xcG.beamXconcr,xcG.beamXsteel]

out.displayFEMesh(setsToDisplay=setsTodisp,caption=None,fileName=None,defFScale=0.0)

