# Main module. Full FE model

import sys

# import local modules
from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
sys.path.append(workingDirectory)
import xc_init
import xc_geom_cart as xcG
# Common variables
out=xc_init.out


import xc_geom_cart as xcG # Geometry and sets
import xc_materials as xcM # Materials
import xc_fem as xcF # FE model
import xc_boundc as xcB # Boundary conditions
import xc_loads as xcL # loads (typical)
import xc_roadway_loads as xcLr # roadway loads
import xc_lcases as xcLC # load cases
import xc_combinations as xcC # SLS and ULS combinations

out.displayFEMesh(xcG.lstSets)
