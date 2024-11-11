# Definition of roadway loads
from actions.roadway_traffic import IAP_load_models as slm
from actions.roadway_traffic import load_model_base as lmb

# import local modules
from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import data_geom as datG
import xc_geom as xcG

# Point loads defined in the object lModel, distributed over the shell 
# elements under the wheels affected by them.

# syntax: VehicleDistrLoad(name,xcSet,loadModel, xCentr,yCentr,hDistr,slopeDistr)
#      name: name identifying the load
#      xcSet: set that contains the shell elements
#      lModel: instance of the class LoadModel with the definition of
#               vehicle of the load model.
#      xCent: global coord. X where to place the centroid of the vehicle
#      yCent: global coord. Y where  to place the centroid of the vehicle
#      hDistr: height considered to distribute each point load with
#               slope slopeDistr 
#      slopeDistr: slope (H/V) through hDistr to distribute the load of 
#               a wheel

vehicleDeck1=lmb.VehicleDistrLoad(name='vehicleDeck1',xcSet=xcG.decklv1,loadModel=slm.IAP_notional_lane3_brake, xCentr=datG.LbeamX/2,yCentr=datG.LbeamY/2.,hDistr=0.25,slopeDistr=1.0)
