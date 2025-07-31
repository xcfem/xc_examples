from actions import load_cases as lcases

# import local modules
from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import xc_init
import xc_geom as xcG
import xc_loads as xcL
import xc_sets

# Common variables
out=xc_init.out ; modelSpace=xc_init.modelSpace ; prep=xc_init.prep
# beam self-weight
G1beamSW=lcases.LoadCase(preprocessor=prep,name="G1beamSW",loadPType="default",timeSType="constant_ts")
G1beamSW.create()
G1beamSW.addLstLoads([xcL.beamSW])
# slab weight on top of flanges
G2slabSW=lcases.LoadCase(preprocessor=prep,name="G2slabSW",loadPType="default",timeSType="constant_ts")
G2slabSW.create()
G2slabSW.addLstLoads([xcL.slabSWst1,xcL.slabSWst2,xcL.slabSWst3])

lstLCnm=[G1beamSW.name,G2slabSW.name]

