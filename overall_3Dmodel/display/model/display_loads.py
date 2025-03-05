from postprocess.config import default_config
from actions import load_cases as lcases

# import local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import xc_init
import xc_loads as xcL # loads (typical)
import xc_roadway_loads as xcLr # roadway loads
import xc_lcases as xcLC # load cases
import xc_sets as xcS
# Common variables
out=xc_init.out ; modelSpace=xc_init.modelSpace ; prep=xc_init.prep
#
auxLC=lcases.LoadCase(preprocessor=prep,name="GselfWeight",loadPType="default",timeSType="constant_ts")
auxLC.create()

for sl in xcL.lstL+xcLr.lstLr:
    auxLC=lcases.LoadCase(preprocessor=prep,name=sl.name,loadPType="default",timeSType="constant_ts")
    auxLC.create()
    auxLC.addLstLoads([sl])
    modelSpace.addLoadCaseToDomain(auxLC.name)
    out.displayLoads()
    modelSpace.removeLoadCaseFromDomain(auxLC.name)

for lc in xcLC.lstLC:
    modelSpace.addLoadCaseToDomain(lc.name)
    out.displayLoads()
    modelSpace.removeLoadCaseFromDomain(lc.name)
    


