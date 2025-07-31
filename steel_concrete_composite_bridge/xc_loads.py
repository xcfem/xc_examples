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
qUnif=slabSWpm/wTF # [N/m2]
slabSWst1=loads.UniformLoadOnSurfaces(name= 'slabSWst1',xcSet=xcG.tfST1,loadVector=xc.Vector([0,0,-qUnif,0,0,0]),refSystem='Global')
## uniform load on top flange of section type 2
wTF=datG.sbeam_st2['tf_w']
qUnif=slabSWpm/wTF # [N/m2]
slabSWst2=loads.UniformLoadOnSurfaces(name= 'slabSWst3',xcSet=xcG.tfST2,loadVector=xc.Vector([0,0,-qUnif,0,0,0]),refSystem='Global')
## uniform load on top flange of section type 3
wTF=datG.sbeam_st3['tf_w']
qUnif=slabSWpm/wTF # [N/m2]
slabSWst3=loads.UniformLoadOnSurfaces(name= 'slabSWst3',xcSet=xcG.tfST3,loadVector=xc.Vector([0,0,-qUnif,0,0,0]),refSystem='Global')

# shrinkage t=15
shrink0_15=loads.StrainLoadOnShells(name='shrink15',xcSet=xcG.slab,DOFstrain=[0,1],strain=datL.epsShrinkage_15)

# dead load
qDL=loads.UniformLoadOnSurfaces(name= 'qDL',xcSet=xcG.slab,loadVector=xc.Vector([0,0,-datL.deadL,0,0,0]),refSystem='Global')

# shrinkage t= 15 to infinite days
shrink15_inf=loads.StrainLoadOnShells(name='shrink15',xcSet=xcG.slab,DOFstrain=[0,1],strain=datL.epsShrinkage_inf-datL.epsShrinkage_15)

# traffic unif. load
qUnifTrf=loads.UniformLoadOnSurfaces(name= 'qUnifTrf',xcSet=xcG.slab,loadVector=xc.Vector([0,0,-datL.qUnifTraffic,0,0,0]),refSystem='Global')

# traffic concentrated load
from actions.roadway_traffic import load_model_base as lmb
xCentCV1=0
yCentCV1=datG.Lbeam/2
truckLoad=lmb.VehicleDistrLoad(
    name='truckLoad',
    xcSet=xcG.slab,
    loadModel=datL.truck3axes,
    xCentr=xCentCV1,
    yCentr=yCentCV1,
    hDistr=0.1,
    slopeDistr=1,
    vehicleRot=0)
# Thermal
## heating
heating=loads.StrainLoadOnShells(name='heating',xcSet=xcS.beam,DOFstrain=[0,1,2],strain=datL.TempIncr*datM.strSteel.alpha)

## cooling
cooling=loads.StrainLoadOnShells(name='cooling',xcSet=xcS.beam,DOFstrain=[0,1,2],strain=datL.TempDecr*datM.strSteel.alpha)


