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
# shrinkage t=0 to 15 days
G4shrink_0_15=lcases.LoadCase(preprocessor=prep,name="G4shrink-0-15",loadPType="default",timeSType="constant_ts")
G4shrink_0_15.create()
modelSpace.setCurrentLoadPattern(G4shrink_0_15.name)
G4shrink_0_15.addLstLoads([xcL.shrink0_15])

# dead load
G3deadL=lcases.LoadCase(preprocessor=prep,name="G3deadL",loadPType="default",timeSType="constant_ts")
G3deadL.create()
G3deadL.addLstLoads([xcL.qDL])

# # shrinkage t=15 to infinite days
G4shrink_15_inf=lcases.LoadCase(preprocessor=prep,name="G4shrink-15-inf",loadPType="default",timeSType="constant_ts")
G4shrink_15_inf.create()
modelSpace.setCurrentLoadPattern(G4shrink_15_inf.name)
G4shrink_15_inf.addLstLoads([xcL.shrink15_inf])

# traffic unif. load
Q1TraffUnif=lcases.LoadCase(preprocessor=prep,name="Q1TraffUnif",loadPType="default",timeSType="constant_ts")
Q1TraffUnif.create()
Q1TraffUnif.addLstLoads([xcL.qUnifTrf])
# traffic concentrated load
Q2TraffConc=lcases.LoadCase(preprocessor=prep,name="Q2TraffConc",loadPType="default",timeSType="constant_ts")
Q2TraffConc.create()
Q2TraffConc.addLstLoads([xcL.truckLoad])

# Thermal
## heating
Q3heating=lcases.LoadCase(preprocessor=prep,name="Q3heating",loadPType="default",timeSType="constant_ts")
Q3heating.create()
modelSpace.setCurrentLoadPattern(Q3heating.name)
Q3heating.addLstLoads([xcL.heating])
## cooling
Q4cooling=lcases.LoadCase(preprocessor=prep,name="Q4cooling",loadPType="default",timeSType="constant_ts")
Q4cooling.create()
modelSpace.setCurrentLoadPattern(Q4cooling.name)
Q4cooling.addLstLoads([xcL.cooling])



lstLCnm=[G3deadL.name,Q1TraffUnif.name,Q2TraffConc.name,Q3heating.name,Q4cooling.name]

