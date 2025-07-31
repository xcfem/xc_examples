# Generation of the finite element model
import xc
from model.mesh import finit_el_model as fem

# import local modules
from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import data_geom as datG
import xc_init
import xc_geom as xcG
import data_materials as datM
import xc_materials as xcM
# Common variables
prep=xc_init.prep
out=xc_init.out
modelSpace=xc_init.modelSpace
#                         ***FE model - MESH***


## Section type 1
bfST1_mesh=fem.SurfSetToMesh(surfSet=xcG.bfST1,matSect=xcM.bfST1_mat,elemSize=datG.eSize,elemType='ShellMITC4')
tfST1_mesh=fem.SurfSetToMesh(surfSet=xcG.tfST1,matSect=xcM.tfST1_mat,elemSize=datG.eSize,elemType='ShellMITC4')
wST1_mesh=fem.SurfSetToMesh(surfSet=xcG.wST1,matSect=xcM.wST1_mat,elemSize=datG.eSize,elemType='ShellMITC4')
## Section type 2
bfST2_mesh=fem.SurfSetToMesh(surfSet=xcG.bfST2,matSect=xcM.bfST2_mat,elemSize=datG.eSize,elemType='ShellMITC4')
tfST2_mesh=fem.SurfSetToMesh(surfSet=xcG.tfST2,matSect=xcM.tfST2_mat,elemSize=datG.eSize,elemType='ShellMITC4')
wST2_mesh=fem.SurfSetToMesh(surfSet=xcG.wST2,matSect=xcM.wST2_mat,elemSize=datG.eSize,elemType='ShellMITC4')
## Section type 3
bfST3_mesh=fem.SurfSetToMesh(surfSet=xcG.bfST3,matSect=xcM.bfST3_mat,elemSize=datG.eSize,elemType='ShellMITC4')
tfST3_mesh=fem.SurfSetToMesh(surfSet=xcG.tfST3,matSect=xcM.tfST3_mat,elemSize=datG.eSize,elemType='ShellMITC4')
wST3_mesh=fem.SurfSetToMesh(surfSet=xcG.wST3,matSect=xcM.wST3_mat,elemSize=datG.eSize,elemType='ShellMITC4')
## Transverse stiffeners
Tstiff_mesh=fem.SurfSetToMesh(surfSet=xcG.Tstiff,matSect=xcM.Tstiff_mat,elemSize=datG.eSize,elemType='ShellMITC4')
#Tstiff_mesh.generateMesh(prep)
#xcG.Tstiff.fillDownwards()
#out.displayBlocks()
#out.displayFEMesh(xcG.Tstiff)

fem.multi_mesh(preprocessor=prep,
               lstMeshSets=[bfST1_mesh,tfST1_mesh,wST1_mesh,
                            bfST2_mesh,tfST2_mesh,wST2_mesh,
                            bfST3_mesh,tfST3_mesh,wST3_mesh,
                            Tstiff_mesh,
                            ])

for st in xcG.beamSets:
    for e in st.elements: e.setProp('yieldStress',datM.strSteel.fy)

out.displayFEMesh(xcG.beamSets)

