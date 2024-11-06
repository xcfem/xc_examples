# Generation of the finite element model
import sys
import xc
from model.mesh import finit_el_model as fem

# import local modules
from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
sys.path.append(workingDirectory)
import data_geom as datG
import xc_init
import xc_geom_cart as xcG
import xc_materials as xcM
# Common variables
prep=xc_init.prep
out=xc_init.out
#                         ***FE model - MESH***
# IMPORTANT: it's convenient to generate the mesh of surfaces before meshing
# the lines, otherwise, sets of shells can take also beam elements touched by
# them

beamXconcr_mesh=fem.LinSetToMesh(linSet=xcG.beamXconcr,matSect=xcM.beamXconcr_mat,elemSize=datG.eSize,vDirLAxZ=xc.Vector([0,1,0]),elemType='ElasticBeam3d',dimElemSpace=3,coordTransfType='linear')
beamY_mesh=fem.LinSetToMesh(linSet=xcG.beamY,matSect=xcM.beamY_mat,elemSize=datG.eSize,vDirLAxZ=xc.Vector([1,0,0]),elemType='ElasticBeam3d',coordTransfType='linear')
columnZconcr_mesh=fem.LinSetToMesh(linSet=xcG.columnZconcr,matSect=xcM.columnZconcr_mat,elemSize=datG.eSize,vDirLAxZ=xc.Vector([1,0,0]),elemType='ElasticBeam3d',coordTransfType='linear')
decklv1_mesh=fem.SurfSetToMesh(surfSet=xcG.decklv1,matSect=xcM.deck_mat,elemSize=datG.eSize,elemType='ShellMITC4')
decklv1_mesh.generateMesh(prep)     #mesh the set of surfaces
decklv2_mesh=fem.SurfSetToMesh(surfSet=xcG.decklv2,matSect=xcM.deck_mat,elemSize=datG.eSize,elemType='ShellMITC4')
decklv2_mesh.generateMesh(prep)     #mesh the set of surfaces
wall_mesh=fem.SurfSetToMesh(surfSet=xcG.wall,matSect=xcM.wall_mat,elemSize=datG.eSize,elemType='ShellMITC4')
wall_mesh.generateMesh(prep) 
foot_mesh=fem.SurfSetToMesh(surfSet=xcG.foot,matSect=xcM.foot_mat,elemSize=datG.eSize,elemType='ShellMITC4')
foot_mesh.generateMesh(prep)

#Steel elements: local Z-axis corresponds to weak axis of the steel shape
beamXsteel_mesh=fem.LinSetToMesh(linSet=xcG.beamXsteel,matSect=xcM.beamXsteel_mat,elemSize=datG.eSize,vDirLAxZ=xc.Vector([0,-1,0]),elemType='ElasticBeam3d',dimElemSpace=3,coordTransfType='linear')
columnZsteel_mesh=fem.LinSetToMesh(linSet=xcG.columnZsteel,matSect=xcM.columnZsteel_mat,elemSize=datG.eSize,vDirLAxZ=xc.Vector([-1,0,0]),elemType='ElasticBeam3d',coordTransfType='linear')

fem.multi_mesh(preprocessor=prep,lstMeshSets=[beamXconcr_mesh,beamXsteel_mesh,beamY_mesh,columnZconcr_mesh,columnZsteel_mesh])     #mesh these sets

# out.displayFEMesh()
# out.displayFEMesh([xcG.beamXconcr,xcG.beamY,xcG.columnZconcr,xcG.decklv1,xcG.decklv2,xcG.wall,xcG.foot])
# out.displayFEMesh([xcG.beamXconcr,xcG.beamXsteel])
# out.displayFEMesh([xcG.columnZconcr,xcG.columnZsteel])
# out.displayLocalAxes()
# out.displayStrongWeakAxis(xcG.beams)
