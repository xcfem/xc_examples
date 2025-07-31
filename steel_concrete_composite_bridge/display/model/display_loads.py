from postprocess.config import default_config
from actions import load_cases as lcases

# import local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import xc_init
import xc_loads as xcL # loads (typical)
import xc_lcases as xcLC # load cases
import xc_sets as xcS
# Common variables
out=xc_init.out ; modelSpace=xc_init.modelSpace ; prep=xc_init.prep
#

for lc in xcLC.lstLC:
    modelSpace.addLoadCaseToDomain(lc.name)
    out.displayLoads()
    modelSpace.removeLoadCaseFromDomain(lc.name)
    


