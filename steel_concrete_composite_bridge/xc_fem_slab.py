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
import xc_fem_beam as xcFb
import xc_sets as xcS
# Common variables
prep=xc_init.prep
out=xc_init.out; modelSpace=xc_init.modelSpace

#Put the slab surface parallel to the top flange
incrZ=datG.slabTh/2
for p in xcG.slab.points:
    n=xcS.topFlange.getNearestNode(p.getPos)
    zn=n.getCurrentPos3d(1)[2]
    p.pos.z=zn+incrZ
    
#                         ***FE model - MESH***

slab_mesh=fem.SurfSetToMesh(surfSet=xcG.slab,matSect=xcM.slab_mat,elemSize=datG.eSize,elemType='ShellMITC4')
slab_mesh.generateMesh(prep)
xcG.slab.fillDownwards()

shearC_mesh=fem.LinSetToMesh(
    linSet=xcG.shearC,
    matSect=xcM.shearC_mat,
    elemSize=datG.eSize,
    vDirLAxZ=xc.Vector([0,10,0]),
    elemType='ElasticBeam3d',
    dimElemSpace=3,
    coordTransfType='linear',
    )
shearC_mesh.generateMesh(prep)

#out.displayFEMesh()
'''
# Nodes in top flange with shear connectors
ySC=[i*datG.SCdisY for i in range(int(datG.Lbeam/datG.SCdisY))] # Y-coord shear connections
topFlange=xcS.topFlange
zTF=xcG.zTF
nTagShearC=list()
for y in ySC:
    for x in xcG.xShrC:
        topFlange.getNearestNode(geom.Pos3d(x,y,zTF))
        nTagShearC.append(n.tag)
    
# Vertical springs to define rigid-contact between the top flange of the beam and the slab
nodesTF=xcS.topFlange.nodes
import data_geom as datG
import data_materials as datM
topFlange.resetTributaries()
topFlange.computeTributaryAreas(False)
Econcr=datM.concrete.Ecm()
hSpring=datG.slabTh/2
zSlab=xcG.zSlab
for n in nodesTF:
    A=n.getTributaryArea()
    kVertSpring=A*E/hSpring # Vertical springs to define rigid-contact between the top flange of the beam and the slab
    v=n.get3dCoo
    p=geom.Pos3d(v[0],v[1],zSlab)
    nSlab=xcG.slab.getNearestNode(p)
'''    


#out.displayFEMesh(xcG.allSets)
