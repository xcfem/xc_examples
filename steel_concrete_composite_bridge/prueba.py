# import local modules
from solution import predefined_solutions

from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import xc_init
# Common variables
out=xc_init.out
modelSpace=xc_init.modelSpace
FEcase=xc_init.FEcase
# import xc_geom as xcG # Geometry and sets
# import xc_materials as xcM # Materials
import xc_fem_beam as xcFb # FE model
import xc_boundc_beam as xcBb # Boundary conditions
# import xc_loads as xcL # loads
import xc_sets as xcS # sets
import xc_lcases_beam as xcLCb # load cases


analysis=predefined_solutions.simple_static_linear(FEcase)
# Beam self-weight
modelSpace.addLoadCaseToDomain(xcLCb.G1beamSW.name)
result= analysis.analyze(1)
modelSpace.calculateNodalReactions()

#for e xcS.

