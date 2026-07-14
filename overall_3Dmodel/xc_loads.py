# Definition of loads (typical)
import xc
import geom
from scipy.constants import g
from model.sets import sets_mng as setMng
from actions import loads
from actions.earth_pressure import earth_pressure as ep

# import local modules
from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import xc_init
import data_geom as datG
import data_loads as datL
import xc_geom as xcG
import xc_sets as xcS
# Common variables
prep=xc_init.prep

#Inertial load (density*acceleration) applied to the elements in a set
#selfWeight=loads.InertialLoad(name='selfWeight', lstSets=[beamXconcr,beamY,columnZconcr,deck,wall,foot], vAccel=xc.Vector( [0.0,0.0,-g]))
selfWeight=loads.InertialLoad(name='selfWeight', lstSets=[xcS.beamXconcrSet,xcS.beamYSet,xcS.columnZconcrSet,xcS.decklv1Set,xcS.decklv2Set], vAccel=xc.Vector( [0.0,0.0,-g]))

# Point load acting on one or several nodes
#     name:       name identifying the load
#     lstNod:     list of nodes  on which the load is applied
#     loadVector: xc.Vector with the six components of the load: 
#                 xc.Vector([Fx,Fy,Fz,Mx,My,Mz]).

nodPLoad=setMng.get_lstNod_from_lst3DPos(preprocessor=prep,lst3DPos=[geom.Pos3d(0,xcG.yList[-1]/2.0,xcG.zList[-1]),geom.Pos3d(xcG.xList[-1],xcG.yList[-1]/2.0,xcG.zList[-1])])
QpuntBeams=loads.NodalLoad(name='QpuntBeams',lstNod=nodPLoad,loadVector=xc.Vector([0,0,-datL.Qbeam,0,0,0]))

# Uniform loads applied on shell elements
#    name:       name identifying the load
#    xcSet:     set that contains the surfaces
#    loadVector: xc.Vector with the six components of the load: 
#                xc.Vector([Fx,Fy,Fz,Mx,My,Mz]).
#    refSystem: reference system in which loadVector is defined:
#               'Local': element local coordinate system
#               'Global': global coordinate system (defaults to 'Global)

unifLoadDeck1= loads.UniformLoadOnSurfaces(name= 'unifLoadDeck1',xcSet=xcS.decklv1Set,loadVector=xc.Vector([0,0,-datL.qdeck1,0,0,0]),refSystem='Global')
unifLoadDeck2= loads.UniformLoadOnSurfaces(name= 'unifLoadDeck2',xcSet=xcS.decklv2Set,loadVector=xc.Vector([0,0,-datL.qdeck2,0,0,0]),refSystem='Global')

# Earth pressure applied to shell or 2D-beam elements
#     Attributes:
#     name:       name identifying the load
#     xcSet:      set that contains the elements to be loaded
#     soilData: instance of the class EarthPressureModel, with 
#               the following attributes:
#                 zGround: global Z coordinate of ground level
#                 zBottomSoils: list of global Z coordinates of the bottom level
#                   for each soil (from top to bottom)
#                 KSoils: list of pressure coefficients for each soil (from top 
#                   to bottom)
#                 gammaSoils: list of weight density for each soil (from top to
#                   bottom)
#                 zWater: global Z coordinate of groundwater level 
#                   (if zGroundwater<minimum z of model => there is no groundwater)
#                 gammaWater: weight density of water
#                 qUnif: uniform load over the backfill surface (defaults to 0)
#     vDir: unit xc vector defining pressures direction

soil01=ep.EarthPressureModel( zGround=xcG.zList[-1]-3, zBottomSoils=[-10],KSoils=[datL.KearthPress],gammaSoils=[datL.densSoil*g], zWater=0, gammaWater=datL.densWater*g,qUnif=datL.qBackfill)
earthPressLoadWall= loads.EarthPressLoad(name= 'earthPressLoadWall', xcSet=xcG.wall,soilData=soil01, vDir=xc.Vector([0,1,0]))

soil02=ep.EarthPressureModel(zGround=xcG.zList[-1],zBottomSoils=[-10],KSoils=[0.001],  gammaSoils=[datL.densSoil*g], zWater=0.05, gammaWater=datL.densWater*g)
stripL01=ep.StripLoadOnBackfill(qLoad=2e5, zLoad=xcG.zList[-1],distWall=1.5, stripWidth=1.2)
earthPWallStrL= loads.EarthPressLoad(name= 'earthPWallStrL', xcSet=xcG.wall,soilData=None, vDir=xc.Vector([0,1,0]))
earthPWallStrL.stripLoads=[stripL01]

lineL01=ep.LineVerticalLoadOnBackfill(qLoad=1e5, zLoad=xcG.zList[-1],distWall=1.0)
earthPWallLinL= loads.EarthPressLoad(name= 'earthPWallLinL', xcSet=xcG.wall,soilData=None, vDir=xc.Vector([0,1,0]))
earthPWallLinL.lineLoads=[lineL01]

hrzL01=ep.HorizontalLoadOnBackfill(phi=math.radians(30), qLoad=2e5, zLoad=xcG.zList[-1],distWall=1, loadedAreaWidth= 0.5, loadedAreaLength= 1.5,horDistrAngle= math.radians(45))
earthPWallHrzL=loads.EarthPressLoad(name= 'earthPWallHrzL', xcSet=xcG.wall,soilData=None, vDir=xc.Vector([0,1,0]))
earthPWallHrzL.horzLoads=[hrzL01]

#Uniform load on beams
# syntax: UniformLoadOnBeams(name, xcSet, loadVector,refSystem)
#    name:       name identifying the load
#    xcSet:      set that contains the lines
#    loadVector: xc.Vector with the six components of the load: 
#                xc.Vector([Fx,Fy,Fz,Mx,My,Mz]).
#    refSystem: reference system in which loadVector is defined:
#               'Local': element local coordinate system
#               'Global': global coordinate system (defaults to 'Global)
unifLoadBeamsY=loads.UniformLoadOnBeams(name='unifLoadBeamsY', xcSet=xcS.beamYSet, loadVector=xc.Vector([0,0,-datL.qunifBeam,0,0,0]),refSystem='Global')

# Strain gradient on shell elements
#     name:  name identifying the load
#     xcSet: set that contains the surfaces
#     nabla: strain gradient in the thickness of the elements:
#            nabla=espilon/thickness    

#strGrad=loads.StrainLoadOnShells(name='strGrad', xcSet=deck,epsilon=0.001)

# Uniform load applied to all the lines (not necessarily defined as lines
# for latter generation of beam elements, they can be lines belonging to 
# surfaces for example) found in the xcSet
# The uniform load is introduced as point loads in the nodes
#     name:   name identifying the load
#     xcSet:  set that contains the lines
#     loadVector: xc.Vector with the six components of the load: 
#                 xc.Vector([Fx,Fy,Fz,Mx,My,Mz]).

unifLoadLinDeck2=loads.UniformLoadOnLines(name='unifLoadLinDeck2',xcSet=xcS.decklv2Set,loadVector=xc.Vector([0,datL.qLinDeck2,0,0,0,0]))

# Point load distributed over the shell elements in xcSet whose 
# centroids are inside the prism defined by the 2D polygon prismBase
# and one global axis.
# syntax: PointLoadOverShellElems(name, xcSet, loadVector,prismBase,prismAxis,refSystem):
#    name: name identifying the load
#    xcSet: set that contains the shell elements
#    loadVector: xc vector with the six components of the point load:
#                   xc.Vector([Fx,Fy,Fz,Mx,My,Mz]).
#    prismBase: 2D polygon that defines the n-sided base of the prism.
#                   The vertices of the polygon are defined in global 
#                   coordinates in the following way:
#                      - for X-axis-prism: (y,z)
#                      - for Y-axis-prism: (x,z)
#                      - for Z-axis-prism: (x,y)
#    prismAxis: axis of the prism (can be equal to 'X', 'Y', 'Z')
#                   (defaults to 'Z')
#    refSystem:  reference system in which loadVector is defined:
#                   'Local': element local coordinate system
#                   'Global': global coordinate system (defaults to 'Global')
from model.geometry import geom_utils as gut

prBase=gut.rect2DPolygon(xCent=datG.LbeamX/2.,yCent=datG.LbeamY/2.,Lx=0.5,Ly=1.0)
wheelDeck1=loads.PointLoadOverShellElems(name='wheelDeck1', xcSet=xcS.decklv1Set, loadVector=xc.Vector([0,0,-datL.Qwheel]),prismBase=prBase,prismAxis='Z',refSystem='Global')

lstL=[selfWeight,QpuntBeams,unifLoadDeck1,unifLoadDeck2,earthPressLoadWall,earthPWallStrL,earthPWallLinL,earthPWallHrzL,unifLoadBeamsY,unifLoadLinDeck2,wheelDeck1]

# Vehicle load
from actions.roadway_traffic import load_model_base as lmb
xCentCV1=2
yCentCV1=2
truckLoad=lmb.VehicleDistrLoad(
    name='truckLoad',
    xcSet=xcS.decklv2Set,
    loadModel=datL.truck3axes,
    xCentr=xCentCV1,
    yCentr=yCentCV1,
    hDistr=0.1,
    slopeDistr=1,
    vehicleRot=0)

# Shrinkage
shrinkage=loads.StrainLoadOnShells(name='shrinkage',xcSet=xcS.decklv2Set,DOFstrain=[0,1],strain=datL.epsShrinkage)

