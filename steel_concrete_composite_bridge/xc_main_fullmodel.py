# Main module. Full FE model
# import local modules
from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import xc_init
# Common variables
out=xc_init.out


import xc_geom as xcG # Geometry and sets
import xc_materials as xcM # Materials
import xc_fem_beam as xcFn # FE beam model 
import xc_fem_slab as xcFs # FE slab model 
import xc_boundc_beam as xcBb # Boundary conditions
import xc_loads as xcL # loads 
 # load cases
#import xc_combinations as xcC # SLS and ULS combinations

