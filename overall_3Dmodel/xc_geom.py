# Geometry definition in cartesian coordinates 
from model.geometry import grid_model as gm
from misc_utils import data_struct_utils as dsu
from model.geometry import geom_utils as gut

# import local modules
from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import env_config as env
import xc_init
import data_geom as datG # geometry data

# Common variables
out=xc_init.out ; modelSpace=xc_init.modelSpace ; prep=xc_init.prep
#
# coordinates in global X,Y,Z axes for the grid generation
xList=[0,datG.LbeamX/2.0,datG.LbeamX]; xList.sort(); xList=dsu.remove_duplicates_list(xList)
yList=[-datG.Wfoot/2.,0,datG.Wfoot/2.,datG.LbeamY]; yList.sort(); yList=dsu.remove_duplicates_list(yList)
zList=[0,datG.LcolumnZ/2.0,datG.LcolumnZ]; zList.sort(); zList=dsu.remove_duplicates_list(zList)
#auxiliary data
lastXpos=len(xList)-1
lastYpos=len(yList)-1
lastZpos=len(zList)-1

# grid model definition
gridGeom= gm.GridModel(prep,xList,yList,zList)

# Grid geometric entities definition (points, lines, surfaces)
# Points' generation
gridGeom.generatePoints()

#Displacements of the grid points in a range
#syntax: movePointsRange(ijkRange,vDisp)
#        ijkRange: range for the search
#        vDisp: xc vector displacement
# for i in range(1,len(xList)):
#     r= gm.IJKRange((i,0,lastZpos),(i,lastYpos,lastZpos))
#     gridGeom.movePointsRange(r,xc.Vector([0.0,0.0,-trSlope*xList[i]]))
#     gridGeom.slopePointsXYZrange....


#Slope (in X direction, Y direction or both) the grid points in a range
#syntax: slopePointsRange(ijkRange,slopeX,xZeroSlope,slopeY,yZeroSlope)
#     ijkRange: range for the search.
#     slopeX: slope in X direction, expressed as deltaZ/deltaX 
#                       (defaults to 0 = no slope applied)
#     xZeroSlope: coordinate X of the "rotation axis".
#     slopeY: slope in Y direction, expressed as deltaZ/deltaY)
#                       (defaults to 0 = no slope applied)
#     yZeroSlope: coordinate Y of the "rotation axis".

#Scale in X with origin xOrig (fixed axis: X=xOrig) to the points in a range
#Only X coordinate of points is modified in the following way:
#       x_scaled=xOrig+scale*(x_inic-xOrig)
#syntax: scaleCoorXPointsRange(ijkRange,xOrig,scale)
#     ijkRange: range for the search.
#     xOrig: origin X to apply scale (point in axis X=xOrig)
#            are not affected by the transformation 
#     scale: scale to apply to X coordinate

#Scale in Y with origin yOrig (fixed axis: Y=yOrig) to the points in a range
#Only Y coordinate of points is modified in the following way:
#       y_scaled=yOrig+scale*(y_inic-yOrig)
#syntax: scaleCoorYPointsRange(ijkRange,yOrig,scale)
#     ijkRange: range for the search.
#     yOrig: origin Y to apply scale (point in axis Y=yOrig)
#            are not affected by the transformation 
#     scale: scale to apply to Y coordinate

#Scale in Z with origin zOrig (fixed axis: Z=zOrig) to the points in a range
#Only Z coordinate of points is modified in the following way:
#       z_scaled=zOrig+scale*(z_inic-zOrig)
#syntax: scaleCoorZPointsRange(ijkRange,zOrig,scale)
#     ijkRange: range for the search.
#     zOrig: origin Z to apply scale (point in axis Z=zOrig)
#            are not affected by the transformation 
#     scale: scale to apply to Z coordinate

#Ranges for lines and surfaces
# extractIncludedIJranges(step): subranges index K=constant (default step=1)
# extractIncludedIKranges((step): subranges index J=constant (default step=1)
# extractIncludedJKranges((step): subranges index I=constant (default step=1)
# extractIncludedIranges(stepJ,stepK): subranges indexes J,K=constant (default
#                                      stpes= 1)
# idem for J and K ranges
beamXconcr_rg=gm.IJKRange((0,1,lastZpos),(lastXpos,lastYpos,lastZpos)).extractIncludedIranges(stepJ=2,stepK=1)
beamY_rg=gm.IJKRange((0,1,lastZpos),(lastXpos,lastYpos,lastZpos)).extractIncludedJranges(stepI=2,stepK=1)
columnZconcr_rg=gm.IJKRange((0,1,0),(lastXpos,1,lastZpos)).extractIncludedKranges(stepI=2)
columnZsteel_rg=gm.IJKRange((0,lastYpos,0),(lastXpos,lastYpos,lastZpos)).extractIncludedJKranges(step=2)+[gm.IJKRange((1,lastYpos,0),(1,lastYpos,1))]
decklv1_rg=gm.IJKRange((0,1,1),(lastXpos,lastYpos,lastZpos)).extractIncludedIJranges(step=2)
foot_rg=[gut.def_rg_cooLim(XYZLists=(xList,yList,zList),Xcoo=(0,datG.LbeamX),Ycoo=(-datG.Wfoot/2.,datG.Wfoot/2.),Zcoo=(0,0))]
beamXsteel_rg=gm.IJKRange((0,2,lastZpos),(lastXpos,2,lastZpos))
#Lines generation
beamXconcr=gridGeom.genLinMultiRegion(lstIJKRange=beamXconcr_rg,setName='beamXconcr')
beamXsteel=gridGeom.genLinOneRegion(ijkRange=beamXsteel_rg,setName='beamXsteel')
beamY=gridGeom.genLinMultiRegion(lstIJKRange=beamY_rg,setName='beamY')
columnZconcr=gridGeom.genLinMultiRegion(lstIJKRange=columnZconcr_rg,setName='columnZconcr')
columnZsteel=gridGeom.genLinMultiRegion(lstIJKRange=columnZsteel_rg,setName='columnZsteel')

#out.displayBlocks()

#Surfaces generation
decklv1=gridGeom.genSurfMultiRegion(lstIJKRange=decklv1_rg,setName='decklv1')
decklv2=gridGeom.genSurfOneXYZRegion(xyzRange=((0,datG.Wfoot/2.,datG.LcolumnZ),(datG.LbeamX/2.0,datG.LbeamY,datG.LcolumnZ)),setName='decklv2')
wall=gridGeom.genSurfOneXYZRegion(xyzRange=((0,0,0),(datG.LbeamX,0,datG.LcolumnZ)),setName='wall')
foot=gridGeom.genSurfMultiRegion(lstIJKRange=foot_rg,setName='foot')

