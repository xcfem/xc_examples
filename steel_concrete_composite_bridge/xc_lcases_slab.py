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
# dead load
G3deadL=lcases.LoadCase(preprocessor=prep,name="G3deadL",loadPType="default",timeSType="constant_ts")
G3deadL.create()
G3deadL.addLstLoads([xcL.qDL])
# traffic unif. load
Q1TraffUnif=lcases.LoadCase(preprocessor=prep,name="Q1TraffUnif",loadPType="default",timeSType="constant_ts")
Q1TraffUnif.create()
Q1TraffUnif.addLstLoads([xcL.qUnifTrf])
# traffic concentrated load
Q2TraffConc=lcases.LoadCase(preprocessor=prep,name="Q2TraffConc",loadPType="default",timeSType="constant_ts")
Q2TraffConc.create()
Q2TraffConc.addLstLoads([xcL.truckLoad])

lstLCnm=[G3deadL.name,Q1TraffUnif.name,Q2TraffConc.name]
