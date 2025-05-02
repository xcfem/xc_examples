# Definition of boundary conditions
import geom
from model.boundary_cond import spring_bound_cond as sprbc

# import local modules
from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import xc_init
import xc_geom as xcG
import xc_fem_beam as xcFb
import xc_fem_slab as xcRs
import xc_sets as xcS
# Common variables
nodes=xc_init.nodes
out=xc_init.out
modelSpace=xc_init.modelSpace
x=xcG.xSlab[-1]
for n in xcG.slab.nodes:
    if abs(n.getCoo[0]-x)<1e-2:
        modelSpace.fixNode('0FF_FFF',n.tag)
