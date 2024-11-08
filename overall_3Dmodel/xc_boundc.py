# Definition of boundary conditions
import geom
from model.boundary_cond import spring_bound_cond as sprbc

# import local modules
from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import xc_init
import data_geom as datG
import data_materials as datM
import xc_geom as xcG

# Common variables
nodes=xc_init.nodes
modelSpace=xc_init.modelSpace
#                       ***BOUNDARY CONDITIONS***
# Regions resting on springs (Winkler elastic foundation)
#       wModulus: Winkler modulus of the foundation (springs in Z direction)
#       cRoz:     fraction of the Winkler modulus to apply for friction in
#                 the contact plane (springs in X, Y directions)
foot_wink=sprbc.ElasticFoundation(wModulus=datM.wModulus,cRoz=datM.cRoz)
foot_wink.generateSprings(xcSet=xcG.foot)
#out.displayFEMesh()

# Springs (defined by Kx,Ky,Kz) to apply on nodes, points, 3Dpos, ...
# Default values for Kx, Ky, Kz are 0, which means that no spring is
# created in the corresponding direction
# spring_col=sprbc.SpringBC(name='spring_col',modelSpace=modelSpace,Kx=10e3,Ky=50e3,Kz=30e3)
# a=spring_col.applyOnNodesIn3Dpos(lst3DPos=[geom.Pos3d(0,datG.LbeamY,0)])

#fixed DOF (ux:'0FF_FFF', uy:'F0F_FFF', uz:'FF0_FFF',
#           rx:'FFF_0FF', ry:'FFF_F0F', rz:'FFF_FF0')
### se puede poner de la forma: set.nodes.getNearestNode(geom.Pos3d(0,datG.LbeamY,0))
n_col1=nodes.getDomain.getMesh.getNearestNode(geom.Pos3d(0,datG.LbeamY,0))
modelSpace.fixNode('000_FFF',n_col1.tag)
n_col2=nodes.getDomain.getMesh.getNearestNode(geom.Pos3d(datG.LbeamX,datG.LbeamY,0))
modelSpace.fixNode('000_FFF',n_col2.tag)
n_col3=nodes.getDomain.getMesh.getNearestNode(geom.Pos3d(datG.LbeamX/2.,datG.LbeamY,0))
modelSpace.fixNode('FF0_000',n_col3.tag)
#out.displayFEMesh()
