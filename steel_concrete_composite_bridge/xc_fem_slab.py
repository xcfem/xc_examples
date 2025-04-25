# Generation of the finite element model
import xc
from model.mesh import finit_el_model as fem

# import local modules
from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import data_geom as datG
import xc_init
import xc_geom as xcG
import xc_materials as xcM
# Common variables
prep=xc_init.prep
out=xc_init.out

slab_mesh=fem.SurfSetToMesh(surfSet=xcG.slab,matSect=xcM.slab_mat,elemSize=datG.eSize,elemType='ShellMITC4')
slab_mesh.generateMesh(prep)

#out.displayFEMesh(xcG.slab)
