from postprocess.config import default_config

# import local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import xc_init
import xc_geom as xcG # Geometry and sets
import xc_materials as xcM # Materials
import xc_fem as xcF # FE model
import xc_boundc as xcB # Boundary conditions
import xc_loads as xcL # loads (typical)
import xc_roadway_loads as xcLr # roadway loads
import xc_lcases as xcLC # load cases

# Common variables
out=xc_init.out
modelSpace=xc_init.modelSpace
prep=xc_init.prep
#

for lc in xcLC.lstLC:
    modelSpace.addLoadCaseToDomain(lc.name)
    out.displayLoads()
    modelSpace.removeLoadCaseFromDomain(lc.name)
    


