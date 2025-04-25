# Definition of loads (typical)
from scipy.constants import g
import xc
import geom
from scipy.constants import g
from model.sets import sets_mng as setMng
from model.geometry import geom_utils as gut
from actions import loads
from actions.earth_pressure import earth_pressure as ep

# import local modules
from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import xc_init
import data_geom as datG
import data_materials as datM
import data_loads as datL
import xc_geom as xcG
import xc_sets as xcS
# Common variables
prep=xc_init.prep

# beam self-weight
beamSW=loads.InertialLoad(name='beamSW', lstSets=[xcS.beam], vAccel=xc.Vector( [0.0,0.0,-g]))
# slab weight on top of flanges
slabSWpm=datG.slabTh*datG.slabW*datM.concrete.density()*g
## uniform load on top flange of section type 1
wTF=datG.sbeam_st1['tf_w']
qUnifTBst1=slabSWpm/wTF # [N/m2]
