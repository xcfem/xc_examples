# Definition of boundary conditions
import xc
import geom
from model.boundary_cond import spring_bound_cond as sprbc
# import local modules
from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import xc_init
import data_geom as datG
import data_materials as datM
import xc_geom as xcG
import xc_materials as xcM
import xc_fem_beam as xcFb
import xc_sets as xcS

# Common variables
nodes=xc_init.nodes
out=xc_init.out
modelSpace=xc_init.modelSpace

# abutment 1
y=xcG.yAbut[0]
for n in xcS.bottomFlange.nodes:
    if abs(n.getCoo[1]-y)<1e-2:
        modelSpace.fixNode('000_F00',n.tag)
# piers and abutment 2
for n in xcS.bottomFlange.nodes:
    ynod=n.getCoo[1]
    if abs(ynod-xcG.yAbut[-1])<1e-2 or abs(ynod-xcG.yPier[0])<1e-2 or abs(ynod-xcG.yPier[1])<1e-2:
        modelSpace.fixNode('0F0_F00',n.tag)

# Diaphragms
yDiaphragms=datG.yBearings+datG.yID
zBF=datG.zBF_ID 
zTF=datG.zTF_ID
## diaphragms bottom flange
lstNod_BF_ID=list()
for y in yDiaphragms:
    n=xcS.web.nodes.getNearestNode(geom.Pos3d(0,y,zBF))
    lstNod_BF_ID.append(n)
BF_ID_spring=sprbc.SpringBC(name='BF_ID_spring',modelSpace=modelSpace,Kx=datM.K_BF_ID,Ky=0,Kz=0)
BF_ID_spring.applyOnNodesLst(lstNod_BF_ID)

## diaphragms top flange
lstNod_TF_ID=list()
for y in yDiaphragms:
    n=xcS.web.nodes.getNearestNode(geom.Pos3d(0,y,zTF))
    lstNod_TF_ID.append(n)
TF_ID_spring=sprbc.SpringBC(name='TF_ID_spring',modelSpace=modelSpace,Kx=datM.K_TF_ID,Ky=0,Kz=0)
TF_ID_spring.applyOnNodesLst(lstNod_TF_ID)

#out.displayFEMesh()

        
