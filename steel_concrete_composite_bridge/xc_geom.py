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

# Local variables
zBF=0 # Z-coo of bottom flange
datST1=datG.sbeam_st1
datST2=datG.sbeam_st2
datST3=datG.sbeam_st3
zTF=datST3['bf_t']/2+datST3['w_h']+datST3['tf_t']/2
zSlab=zTF+datST3['tf_t']/2+datG.slabTh/2
xSlab=[-datG.slabW/2,datG.slabW/2]
xShrC=[-datG.b_0/2,datG.b_0/2]
xWeb=0
xBFst1=[-datST1['bf_w']/2,datST1['bf_w']/2]
xBFst2=[-datST2['bf_w']/2,datST2['bf_w']/2]
xBFst3=[-datST3['bf_w']/2,datST3['bf_w']/2]
xTFst1=[-datST1['tf_w']/2,datST1['tf_w']/2]
xTFst2=[-datST2['tf_w']/2,datST2['tf_w']/2]
xTFst3=[-datST3['tf_w']/2,datST3['tf_w']/2]

yAbut=[0,datG.Lbeam]
yPier=[datG.spansL[0],datG.spansL[0]+datG.spansL[1]]
#
xList=xSlab+xShrC+[xWeb]+xBFst1+xBFst2+xBFst3
xList.sort(); xList=dsu.remove_duplicates_list(xList)
yList=yAbut+yPier
for yl in datST1['yCoord']+datST2['yCoord']+datST3['yCoord']:
    yList+=yl
yList.sort(); yList=dsu.remove_duplicates_list(yList)
zList=[zBF,zTF,zSlab]; zList.sort(); zList=dsu.remove_duplicates_list(zList)
gridGeom= gm.GridModel(prep,xList,yList,zList)
gridGeom.generatePoints()

# Section type 1
dat=datG.sbeam_st1
yCoo=dat['yCoord']
lstXYZRange=list()
## Bottom flange
xmin=xBFst1[0]; xmax=xBFst1[-1]
z=zBF
for yl in yCoo:
    lstXYZRange.append([[xmin,yl[0],z],[xmax,yl[-1],z]])
bfST1=gridGeom.genSurfMultiXYZRegion(lstXYZRange=lstXYZRange,setName='bfST1')
## Top flange
xmin=xTFst1[0]; xmax=xTFst1[-1]
z=zTF
for yl in yCoo:
    lstXYZRange.append([[xmin,yl[0],z],[xmax,yl[-1],z]])
tfST1=gridGeom.genSurfMultiXYZRegion(lstXYZRange=lstXYZRange,setName='tfST1')
## Web
x=0
zmin=zBF
zmax=zTF
for yl in yCoo:
    lstXYZRange.append([[x,yl[0],zmin],[x,yl[-1],zmax]])
wST1=gridGeom.genSurfMultiXYZRegion(lstXYZRange=lstXYZRange,setName='wST1')

# Section type 2
dat=datG.sbeam_st2
yCoo=dat['yCoord']
lstXYZRange=list()
## Bottom flange
xmin=xBFst2[0]; xmax=xBFst2[-1]
z=zBF
for yl in yCoo:
    lstXYZRange.append([[xmin,yl[0],z],[xmax,yl[-1],z]])
bfST2=gridGeom.genSurfMultiXYZRegion(lstXYZRange=lstXYZRange,setName='bfST2')
## Top flange
xmin=xTFst2[0]; xmax=xTFst2[-1]
z=zTF
for yl in yCoo:
    lstXYZRange.append([[xmin,yl[0],z],[xmax,yl[-1],z]])
tfST2=gridGeom.genSurfMultiXYZRegion(lstXYZRange=lstXYZRange,setName='tfST2')
## Web
x=0
zmin=zBF
zmax=zTF
for yl in yCoo:
    lstXYZRange.append([[x,yl[0],zmin],[x,yl[-1],zmax]])
wST2=gridGeom.genSurfMultiXYZRegion(lstXYZRange=lstXYZRange,setName='wST2')

# Section type 3
dat=datG.sbeam_st3
yCoo=dat['yCoord']
lstXYZRange=list()
## Bottom flange
xmin=xBFst3[0]; xmax=xBFst3[-1]
z=zBF
for yl in yCoo:
    lstXYZRange.append([[xmin,yl[0],z],[xmax,yl[-1],z]])
bfST3=gridGeom.genSurfMultiXYZRegion(lstXYZRange=lstXYZRange,setName='bfST3')
## Top flange
xmin=xTFst3[0]; xmax=xTFst3[-1]
z=zTF
for yl in yCoo:
    lstXYZRange.append([[xmin,yl[0],z],[xmax,yl[-1],z]])
tfST3=gridGeom.genSurfMultiXYZRegion(lstXYZRange=lstXYZRange,setName='tfST3')
## Web
x=0
zmin=zBF
zmax=zTF
for yl in yCoo:
    lstXYZRange.append([[x,yl[0],zmin],[x,yl[-1],zmax]])
wST3=gridGeom.genSurfMultiXYZRegion(lstXYZRange=lstXYZRange,setName='wST3')

# slab
slab=gridGeom.genSurfOneXYZRegion(
    xyzRange=[[xSlab[0],0,zSlab],[xSlab[-1],datG.Lbeam,zSlab]],
    setName='slab'
    )

beamSets=[bfST1,tfST1,wST1,
          bfST2,tfST2,wST2,
          bfST3,tfST3,wST3]
slabSets=[slab]
allSets=beamSets+slabSets
#out.displayBlocks()  
