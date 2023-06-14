# -*- coding: utf-8 -*-
from __future__ import division 
from __future__ import print_function

import os
import geom
import xc
import math
from model import predefined_spaces
from model.geometry import grid_model as gm
from model.mesh import finit_el_model as fem
from model.boundary_cond import spring_bound_cond as sprbc
from model.sets import sets_mng as sets
from materials import typical_materials as tm
from model.geometry import geom_utils as gut
from materials.astm_aisc import ASTM_materials as astm
from actions import loads
from actions import load_cases as lcases
from misc_utils import data_struct_utils as dsu

# Default configuration of environment variables.
from postprocess.config import default_config
from postprocess import output_styles as outSty
from postprocess import output_handler as outHndl

# import local modules
import sys
workingDirectory= default_config.findWorkingDirectory()+'/' #search env_config.py
sys.path.append(workingDirectory)
#import env_config as env
import data as dat

sty=outSty.OutputStyle() 

#Data
#             *** GEOMETRIC model (points, lines, surfaces) - SETS ***
FEcase= xc.FEProblem()
preprocessor=FEcase.getPreprocessor
prep=preprocessor   #short name
nodes= prep.getNodeHandler
elements= prep.getElementHandler
elements.dimElem= 3
# Problem type
modelSpace= predefined_spaces.StructuralMechanics3D(nodes) #Defines the
# dimension of the space: nodes by three coordinates (x,y,z) and 
# six DOF for each node (Ux,Uy,Uz,thetaX,thetaY,thetaZ)
out=outHndl.OutputHandler(modelSpace,sty)

#   **** Grid generation ****
# coordinates in global X,Y,Z axes for the grid generation

# grid model definition
gridTank= gm.GridModel(prep,dat.rList,dat.angList,dat.zList,xCentCoo=0,yCentCoo=0)
gridHopper= gm.GridModel(prep,dat.rListHopp,dat.angList,dat.zListHopp,xCentCoo=0,yCentCoo=0)


# Grid geometric entities definition (points, lines, surfaces)
# Points' generation
gridTank.generateCylZPoints()
gridHopper.generateCylZPoints()

#adjust cone radius (tank)
lastAind=gridTank.lastYIndex()
lastZind=gridTank.lastZIndex()
Rind=dsu.get_index_closest_inlist(dat.rList,dat.Rbase)
#gridTank.moveCylPointsRadius(gm.IJKRange((Rind,0,lastZind),(Rind,lastAind,lastZind)),RtopQuencher)

for r in dat.rList:
    Rind=dsu.get_index_closest_inlist(dat.rList,r)
#    for k in range(dsu.get_index_closest_inlist(dat.zList,dat.z_cone[0]),lastZind-1):
    for k in range(dsu.get_index_closest_inlist(dat.zList,dat.z_cone[0]),lastZind+1):
        z=dat.zList[k]
        R=r+dat.slopeCone*(z-dat.z_cone[0])
        gridTank.moveCylPointsRadius(gm.IJKRange((Rind,0,k),(Rind,lastAind,k)),R)
#adjust cone radius (hopper)
gridHopper.moveCylPointsRadius(gm.IJKRange((0,0,1),(0,lastAind,1)),dat.r_hopper_up)

#  **** Geometry *****
#Surfaces generation
tankLow_z0=gridTank.genSurfMultiXYZRegion(lstXYZRange=[
    ((dat.Rbase,0,0),(dat.Rbase,dat.angList[-1],dat.z_stiff_200x25[0]))],
    setName='tankLow_z0',closeCyl='Y')

tankLow_z1=gridTank.genSurfMultiXYZRegion(lstXYZRange=[
    ((dat.Rbase,dat.angCooHole1[0],dat.z_stiff_200x25[0]),(dat.Rbase,dat.angCooHole0[0],dat.z_holes[0])),
    ((dat.Rbase,dat.angCooHole0[1],dat.z_stiff_200x25[0]),(dat.Rbase,dat.angCooHole1[1],dat.z_holes[0]))],
    setName='tankLow_z1',closeCyl='N')

tankLow_z2=gridTank.genSurfMultiXYZRegion(lstXYZRange=[
    ((dat.Rbase,dat.angCooHole1[0],dat.z_holes[0]),(dat.Rbase,dat.angCooHole1[1],dat.z_holes[1]))],
    setName='tankLow_z2',closeCyl='N')
                                          
tankLow_z3=gridTank.genSurfMultiXYZRegion(lstXYZRange=[
    ((dat.Rbase,0,dat.z_holes[-1]),(dat.Rbase,dat.angList[-1],dat.z_stiff_80x10[0]))],
    setName='tankLow_z3',closeCyl='Y')

tankLow_z4=gridTank.genSurfMultiXYZRegion(lstXYZRange=[
    ((dat.Rbase,0,dat.z_stiff_80x10[0]),(dat.Rbase,dat.angList[-1],dat.z_stiff_120x40[0]))],
    setName='tankLow_z4',closeCyl='Y')

tankLow=modelSpace.setSum('tankLow',[ tankLow_z0,tankLow_z1,tankLow_z2,tankLow_z3,tankLow_z4])
tankLow.description='Quencher, lower part'

tankMid=gridTank.genSurfMultiXYZRegion(lstXYZRange=[
    ((dat.Rbase,0,dat.z_stiff_120x40[0]),(dat.Rbase,dat.angList[-1],dat.z_stiff_100x30[0]))],
    setName='tankMid',closeCyl='Y')
tankMid.description='Quencher, middle part'
    
tankUp=gridTank.genSurfMultiXYZRegion(lstXYZRange=[
    ((dat.Rbase,0,dat.z_stiff_100x30[0]),(dat.Rbase,dat.angList[-1],dat.z_max[0]))],
    setName='tankUp',closeCyl='Y')
tankUp.description='Quencher, upper part'

#   stiffeners
# stiffeners 80x10
lstXYZRange=list()
for zs in dat.z_stiff_80x10:
    lstXYZRange.append([(dat.Rbase,0,zs),(dat.Rbase+0.08,dat.angList[-1],zs)])
stiff80x10=gridTank.genSurfMultiXYZRegion(lstXYZRange,'stiff80x10','Y')
stiff80x10.description='Stiffeners 80x10'

# stiffeners 80x12
lstXYZRange=list()
for zs in dat.z_stiff_80x12:
    lstXYZRange.append([(dat.Rbase,0,zs),(dat.Rbase+0.08,dat.angList[-1],zs)])
stiff80x12=gridTank.genSurfMultiXYZRegion(lstXYZRange,'stiff80x12','Y')
stiff80x12.description='Stiffeners 80x12'

#stiffeners 175x25
lstXYZRange=list()
for zs in dat.z_stiff_175x25:
    lstXYZRange.append([(dat.Rbase,0,zs),(dat.Rbase+0.175,dat.angList[-1],zs)])
stiff175x25=gridTank.genSurfMultiXYZRegion(lstXYZRange,'stiff175x25','Y')
stiff175x25.description='Stiffeners 175x25'

#stiffeners 200x25
lstXYZRange=list()
for zs in dat.z_stiff_200x25:
    lstXYZRange.append([(dat.Rbase,0,zs),(dat.Rbase+0.2,dat.angList[-1],zs)])
stiff200x25=gridTank.genSurfMultiXYZRegion(lstXYZRange,'stiff200x25','Y')
stiff200x25.description='Stiffeners 200x25'

#stiffeners 120x20
lstXYZRange=list()
for zs in dat.z_stiff_120x20:
    lstXYZRange.append([(dat.Rbase,0,zs),(dat.Rbase+0.12,dat.angList[-1],zs)])
stiff120x20=gridTank.genSurfMultiXYZRegion(lstXYZRange,'stiff120x20','Y')
stiff120x20.description='Stiffeners 120x20'

#stiffeners 120x40
lstXYZRange=list()
for zs in dat.z_stiff_120x40:
    lstXYZRange.append([(dat.Rbase,0,zs),(dat.Rbase+0.12,dat.angList[-1],zs)])
stiff120x40=gridTank.genSurfMultiXYZRegion(lstXYZRange,'stiff120x40','Y')
stiff120x40.description='Stiffeners 120x40'

#stiffeners 100x30
lstXYZRange=list()
for zs in dat.z_stiff_100x30:
    lstXYZRange.append([(dat.Rbase,0,zs),(dat.Rbase+0.1,dat.angList[-1],zs)])
stiff100x30=gridTank.genSurfMultiXYZRegion(lstXYZRange,'stiff100x30','Y')
stiff100x30.description='Stiffeners 100x30'

#stiffeners conduit (Web)
lstXYZRange=list()
for zs in dat.z_stiff_cond:
    lstXYZRange.append([(dat.Rbase,0,zs),(dat.Rbase+dat.wWebStiffCond,dat.angList[-1],zs)])
stiffWebCond=gridTank.genSurfMultiXYZRegion(lstXYZRange,'stiffWebCond','Y')
stiffWebCond.description='Web stiffeners conduit'

lstXYZRange=list()
if dat.tFlgStiffCond > 0:
    lstXYZRange.append([(dat.Rbase+dat.wWebStiffCond,0,dat.zFlgStiffCond[0]),(dat.Rbase+dat.wWebStiffCond,dat.angList[-1],dat.zFlgStiffCond[1])])
    lstXYZRange.append([(dat.Rbase+dat.wWebStiffCond,0,dat.zFlgStiffCond[2]),(dat.Rbase+dat.wWebStiffCond,dat.angList[-1],dat.zFlgStiffCond[3])])
    stiffFlgCond=gridTank.genSurfMultiXYZRegion(lstXYZRange,'stiffFlgCond','Y')
    stiffFlgCond.description='Flange stiffeners conduit'
# vertical stiffener conduit
lstXYZRange=list()
for ang in dat.ang_vstiff_cond:
    lstXYZRange.append([(dat.Rbase,ang,dat.zFlgStiffCond[0]),(dat.Rbase+dat.wWebStiffCond,ang,dat.zFlgStiffCond[1])])
    lstXYZRange.append([(dat.Rbase,ang,dat.zFlgStiffCond[2]),(dat.Rbase+dat.wWebStiffCond,ang,dat.zFlgStiffCond[3])])
stiffVertCond=gridTank.genSurfMultiXYZRegion(lstXYZRange,'stiffVertCond','N')
stiffWebCond.description='Vertical stiffeners conduit'
    
# Platens base
lstXYZRange=list()
z1=dat.z_stiff_175x25[0]
z2=dat.z_stiff_200x25[0]
for ang in dat.angPlaten1:
    lstXYZRange.append([(dat.Rbase,ang,z1),(dat.Rbase+0.175,ang,z2)])
for ang in dat.angPlaten2:
    lstXYZRange.append([(dat.Rbase,ang,z1),(dat.Rbase+0.175,ang,z2)])
platenBase=gridTank.genSurfMultiXYZRegion(lstXYZRange,'platenBase','N')
platenBase.description='Vertical stiffeners t=20mm'

# Platens over main opening
lstXYZRange=list()
z1=dat.z_stiff_120x20[0]
z2=dat.z_stiff_120x20[1]
for ang in dat.angPlaten1:
    lstXYZRange.append([(dat.Rbase,ang,z1),(dat.Rbase+0.1,ang,z2)])
platenUp=gridTank.genSurfMultiXYZRegion(lstXYZRange,'platenUp','N')
platenUp.description='Vertical stiffeners t=10mm'
lstXYZRange=[[(dat.Rbase+0.1,0,z1),(dat.Rbase+0.1,dat.angList[-1],z2)]]
ringPlatenUp=gridTank.genSurfMultiXYZRegion(lstXYZRange,'ringPlatenUp','Y')

hopper=gridHopper.genSurfOneXYZRegion([(dat.r_hopper_down,0,dat.z_hopper_down),(dat.r_hopper_down,dat.angList[-1],dat.z_hopper_up)],'hopper','Y')
hopper.description='Hopper'

#out.displayBlocks()

# Columns HEB-200 (W8x48)
lstXYZRange=list()
angs=[45+i*90 for i in range(4)]
for ang in angs:
    lstXYZRange.append([(dat.Rbase,ang,0),(dat.Rbase,ang,dat.z_stiff_120x20[0])])
#rad=dat.Rbase+0.08
rad=dat.Rbase
ang=45
column45=gridTank.genLinOneXYZRegion([(rad,ang,dat.z_stiff_200x25[0]),(rad,ang,dat.z_stiff_120x20[0])],'column45')
ang=135
column135=gridTank.genLinOneXYZRegion([(rad,ang,dat.z_stiff_200x25[0]),(rad,ang,dat.z_stiff_120x20[0])],'column135')
ang=225
column225=gridTank.genLinOneXYZRegion([(rad,ang,dat.z_stiff_200x25[0]),(rad,ang,dat.z_stiff_120x20[0])],'column225')
ang=315
column315=gridTank.genLinOneXYZRegion([(rad,ang,dat.z_stiff_200x25[0]),(rad,ang,dat.z_stiff_120x20[0])],'column315')
 
columns=modelSpace.setSum('columns',[column45,column135,column225,column315])

columns.description='Columns'


#   ***** Steel elastoplastic law  ******
AISI304L= tm.defJ2PlateFibre(preprocessor=preprocessor, name='AISI304L', E=dat.AISI_E, nu=0.3, fy=dat.AISI_fy,alpha=dat.AISI_alpha,rho=7850) #Properties of AISI 304L at 400ºC

#  ***** Material von  mises verification *****
tankLow_mat=tm.defMembranePlateFiberSection(preprocessor,name='tankLow_mat',h=dat.tBase ,nDMaterial= AISI304L)

tankMid_mat=tm.defMembranePlateFiberSection(preprocessor,name='tankMid_mat',h=dat.tMidd ,nDMaterial= AISI304L)

tankUp_mat=tm.defMembranePlateFiberSection(preprocessor,name='tankUp_mat',h=dat.tUp,nDMaterial= AISI304L)

stiff80x10_mat=tm.defMembranePlateFiberSection(preprocessor,name='stiff80x10_mat',h=10e-3 ,nDMaterial= AISI304L)

stiff80x12_mat=tm.defMembranePlateFiberSection(preprocessor,name='stiff80x12_mat',h=12e-3 ,nDMaterial= AISI304L)

stiff175x25_mat=tm.defMembranePlateFiberSection(preprocessor,name='stiff175x25_mat',h=25e-3 ,nDMaterial= AISI304L)

stiff200x25_mat=tm.defMembranePlateFiberSection(preprocessor,name='stiff200x25_mat',h=25e-3 ,nDMaterial= AISI304L)

stiff120x20_mat=tm.defMembranePlateFiberSection(preprocessor,name='stiff120x20_mat',h=20e-3 ,nDMaterial= AISI304L)

stiff120x40_mat=tm.defMembranePlateFiberSection(preprocessor,name='stiff120x40_mat',h=40e-3 ,nDMaterial= AISI304L)

stiff100x30_mat=tm.defMembranePlateFiberSection(preprocessor,name='stiff100x30_mat',h=30e-3 ,nDMaterial= AISI304L)

stiffWebCond_mat=tm.defMembranePlateFiberSection(preprocessor,name='stiffWebCond_mat',h=dat.tWebStiffCond ,nDMaterial= AISI304L)

if dat.tFlgStiffCond > 0:
    stiffFlgCond_mat=tm.defMembranePlateFiberSection(preprocessor,name='stiffFlgCond_mat',h=dat.tFlgStiffCond ,nDMaterial= AISI304L)

stiffVertCond_mat=tm.defMembranePlateFiberSection(preprocessor,name='stiffVertCond_mat',h=dat.tVertStiffCond ,nDMaterial= AISI304L)

platenBase_mat=tm.defMembranePlateFiberSection(preprocessor,name='platenBase_mat',h=dat.tPlatenBase,nDMaterial= AISI304L)

platenUp_mat=tm.defMembranePlateFiberSection(preprocessor,name='platenUp_mat',h=dat.tPlatenUp,nDMaterial= AISI304L)

hopper_mat=tm.defMembranePlateFiberSection(preprocessor,name='hopper_mat',h=dat.tHopper ,nDMaterial= AISI304L)

eType='ShellNLDKGQ' # element large deformation theory


#  **** Mesh *****

lstMeshSurf=[]
tankLow_mesh=fem.SurfSetToMesh(surfSet=tankLow,matSect=tankLow_mat,elemSize=dat.eSize,elemType=eType)
lstMeshSurf.append(tankLow_mesh)

tankMid_mesh=fem.SurfSetToMesh(surfSet=tankMid,matSect=tankMid_mat,elemSize=dat.eSize,elemType=eType)
lstMeshSurf.append(tankMid_mesh)

tankUp_mesh=fem.SurfSetToMesh(surfSet=tankUp,matSect=tankUp_mat,elemSize=dat.eSize,elemType=eType)
lstMeshSurf.append(tankUp_mesh)

stiff80x10_mesh=fem.SurfSetToMesh(surfSet=stiff80x10,matSect=stiff80x10_mat,elemSize=dat.eSize,elemType=eType)
lstMeshSurf.append(stiff80x10_mesh)

stiff80x12_mesh=fem.SurfSetToMesh(surfSet=stiff80x12,matSect=stiff80x12_mat,elemSize=dat.eSize,elemType=eType)
lstMeshSurf.append(stiff80x12_mesh)

stiff175x25_mesh=fem.SurfSetToMesh(surfSet=stiff175x25,matSect=stiff175x25_mat,elemSize=dat.eSize,elemType=eType)
lstMeshSurf.append(stiff175x25_mesh)

stiff200x25_mesh=fem.SurfSetToMesh(surfSet=stiff200x25,matSect=stiff200x25_mat,elemSize=dat.eSize,elemType=eType)
lstMeshSurf.append(stiff200x25_mesh)

stiff120x20_mesh=fem.SurfSetToMesh(surfSet=stiff120x20,matSect=stiff120x20_mat,elemSize=dat.eSize,elemType=eType)
lstMeshSurf.append(stiff120x20_mesh)

stiff120x40_mesh=fem.SurfSetToMesh(surfSet=stiff120x40,matSect=stiff120x40_mat,elemSize=dat.eSize,elemType=eType)
lstMeshSurf.append(stiff120x40_mesh)

stiff100x30_mesh=fem.SurfSetToMesh(surfSet=stiff100x30,matSect=stiff100x30_mat,elemSize=dat.eSize,elemType=eType)
lstMeshSurf.append(stiff100x30_mesh)

stiffWebCond_mesh=fem.SurfSetToMesh(surfSet=stiffWebCond,matSect=stiffWebCond_mat,elemSize=dat.eSize,elemType=eType)
lstMeshSurf.append(stiffWebCond_mesh)

if dat.tFlgStiffCond > 0:
    stiffFlgCond_mesh=fem.SurfSetToMesh(surfSet=stiffFlgCond,matSect=stiffFlgCond_mat,elemSize=dat.eSize,elemType=eType)
    lstMeshSurf.append(stiffFlgCond_mesh)

stiffVertCond_mesh=fem.SurfSetToMesh(surfSet=stiffVertCond,matSect=stiffVertCond_mat,elemSize=dat.eSize,elemType=eType)
lstMeshSurf.append(stiffVertCond_mesh)

platenBase_mesh=fem.SurfSetToMesh(surfSet=platenBase,matSect=platenBase_mat,elemSize=dat.eSize,elemType=eType)
lstMeshSurf.append(platenBase_mesh)

platenUp_mesh=fem.SurfSetToMesh(surfSet=platenUp,matSect=platenUp_mat,elemSize=dat.eSize,elemType=eType)
lstMeshSurf.append(platenUp_mesh)

ringPlatenUp_mesh=fem.SurfSetToMesh(surfSet=ringPlatenUp,matSect=platenUp_mat,elemSize=dat.eSize,elemType=eType)
lstMeshSurf.append(ringPlatenUp_mesh)

hopper_mesh=fem.SurfSetToMesh(surfSet=hopper,matSect=hopper_mat,elemSize=dat.eSize,elemType=eType)
lstMeshSurf.append(hopper_mesh)
fem.multi_mesh(prep,lstMeshSurf)

columns_mat=astm.WShape(dat.steel_W,'W8X48')
columns_mat.defElasticShearSection3d(prep)

lstMeshLin=list()

ang=math.radians(45)
column45_mesh=fem.LinSetToMesh(linSet=column45, matSect=columns_mat, elemSize=dat.eSize, vDirLAxZ=xc.Vector([-math.cos(ang),math.sin(ang),0]), elemType='ElasticBeam3d', dimElemSpace=3, coordTransfType='corot')
lstMeshLin.append(column45_mesh)

ang=math.radians(135)
column135_mesh=fem.LinSetToMesh(linSet=column135, matSect=columns_mat, elemSize=dat.eSize, vDirLAxZ=xc.Vector([-math.cos(ang),math.sin(ang),0]), elemType='ElasticBeam3d', dimElemSpace=3, coordTransfType='corot')
lstMeshLin.append(column135_mesh)

ang=math.radians(225)
column225_mesh=fem.LinSetToMesh(linSet=column225, matSect=columns_mat, elemSize=dat.eSize, vDirLAxZ=xc.Vector([-math.cos(ang),math.sin(ang),0]), elemType='ElasticBeam3d', dimElemSpace=3, coordTransfType='corot')
lstMeshLin.append(column225_mesh)

ang=math.radians(315)
column315_mesh=fem.LinSetToMesh(linSet=column315, matSect=columns_mat, elemSize=dat.eSize, vDirLAxZ=xc.Vector([-math.cos(ang),math.sin(ang),0]), elemType='ElasticBeam3d', dimElemSpace=3, coordTransfType='corot')
lstMeshLin.append(column315_mesh)

fem.multi_mesh(prep,lstMeshLin)
columns.fillDownwards()
#out.displayLocalAxes(columns)
#out.displayStrongWeakAxis(columns)
out.displayFEMesh()


#  **** Boundary conditions *****
nodAnchor=prep.getSets.defSet('nodAnchor')

z=0
#for ang in dat.angAnchors:
for ang in dat.angPlaten1:
    x=dat.Ranchors*math.cos(math.radians(ang))
    y=dat.Ranchors*math.sin(math.radians(ang))
    n=stiff175x25.nodes.getNearestNode(geom.Pos3d(x,y,z))
    nodAnchor.nodes.append(n)

# for n in nodAnchor.nodes:
#     modelSpace.fixNode('000_FFF',n.tag)
# Springs
nodBase=prep.getSets.defSet('nodBase')
tagIni=prep.getNodeHandler.defaultTag
from model.boundary_cond import spring_bound_cond as sbc
kv=1e10
kh=1e9
springAnchor=sbc.SpringBC(name='springAnchor',modelSpace=modelSpace,Kx=kh,Ky=kh,Kz=kv)
springAnchor.createSpringMaterials()
springAnchor.applyOnNodesInSet(nodAnchor)
tagFin=prep.getNodeHandler.defaultTag

for tag in range(tagIni,tagFin):
    nodBase.nodes.append(nodes.getNode(tag))
    
#out.displayFEMesh(nodBase)

# Glued nodes between hopper and tank
hoppNodGlue=sets.get_set_nodes_plane_XY(setName='hoppNodGlue', setBusq=hopper, zCoord=dat.z_hopper_up, tol=0.0001)
tankNodGlue=sets.get_set_nodes_plane_XY(setName='tankNodGlue', setBusq=tankLow, zCoord=dat.z_hopper_up, tol=0.0001)

for nh in hoppNodGlue.nodes:
    nt=tankNodGlue.getNearestNode(nh.getInitialPos3d)
    modelSpace.newEqualDOF(nh.tag,nt.tag,dofs=xc.ID([0,1,2]))


    #    **** Sets definition ****
    # Auxiliary sets definition

tankLow_z0.fillDownwards()
tankLow_z1.fillDownwards()
tankLow_z2.fillDownwards()
tankLow_z3.fillDownwards()
tankLow_z4.fillDownwards()

openTank=modelSpace.setSum('openTank',[tankLow_z0,tankLow_z1,tankLow_z2,tankLow_z3]); openTank.fillDownwards()

closedTank=modelSpace.setSum('closedTank',[tankLow_z4,tankMid,tankUp]); closedTank.fillDownwards()

stiffWind=modelSpace.setSum('stiffWind',[stiff80x10,stiff80x12,stiff120x20,stiff120x40,stiff100x30,stiffWebCond]); stiffWind.fillDownwards()

stiffBase=modelSpace.setSum('stiffBase',[stiff175x25,stiff200x25]); stiffBase.fillDownwards()

if dat.tFlgStiffCond > 0:
    stiffeners=modelSpace.setSum('stiffeners',[stiffWind,stiffBase,stiffFlgCond]); stiffBase.fillDownwards()
else:
    stiffeners=modelSpace.setSum('stiffeners',[stiffWind,stiffBase]); stiffBase.fillDownwards()


tankWall=modelSpace.setSum('tankWall',[openTank,closedTank]); tankWall.fillDownwards()
if dat.tFlgStiffCond > 0:
    tankwallPlusHopper=modelSpace.setSum('tankWall',[tankWall,hopper,stiffFlgCond]); tankwallPlusHopper.fillDownwards()
else:
    tankwallPlusHopper=modelSpace.setSum('tankWall',[tankWall,hopper]); tankwallPlusHopper.fillDownwards()


platform=sets.get_set_nodes_plane_XY(setName='platform', setBusq=tankUp, zCoord=dat.z_platf[0], tol=0.0001)

dustSet=sets.get_set_nodes_plane_XY(setName='dustSet', setBusq=tankLow, zCoord=dat.z_stiff_80x10[0], tol=0.0001)

collarNodes=[stiffFlgCond.getNodes.getNearestNode(dat.coord_20016),
             stiffFlgCond.getNodes.getNearestNode(dat.coord_20017),
             stiffFlgCond.getNodes.getNearestNode(dat.coord_20018),
             stiffFlgCond.getNodes.getNearestNode(dat.coord_20019)]
#Elements under work thermal load 
#tankLow_endInsul=gridTank.getSetSurfOneXYZRegion(xyzRange=((dat.Rbase,0,dat.z_stiff_120x20[-1]),(dat.Rbase,dat.angList[-1],dat.z_stiff_80x10[0])),setName='tankLow_endInsul',closeCyl='Y')
internalTank=modelSpace.setSum('internalTank',[tankLow_z4,tankMid,tankUp,hopper]) # also under internal negative pressure
if dat.tFlgStiffCond > 0:
    thermalIntTank=modelSpace.setSum('thermalIntTank',[tankLow_z4,tankMid,tankUp,hopper,stiffFlgCond])
else:
    thermalIntTank=modelSpace.setSum('thermalIntTank',[tankLow_z4,tankMid,tankUp,hopper])
    
stiffWorkTemp=modelSpace.setSum('stiffWorkTemp',[stiff80x10,stiff80x12,stiff120x40,stiff100x30,stiffWebCond])

lowerMemb=modelSpace.setSum('lowerMemb',[stiff120x20,stiff200x25,stiff175x25,platenBase,platenUp,columns])

stiffCond=modelSpace.setSum('stiffCond',[stiffWebCond,stiffFlgCond,stiffVertCond]) ; #stiffCond.fillDownwards()
stiffCond.description='Stiffener conduit'

gravitySets=[tankWall,hopper,stiffeners,columns]

tank=modelSpace.setSum('tank',[tankWall,hopper,stiffeners,stiffVertCond,platenBase,platenUp,ringPlatenUp,stiffFlgCond])
tank-=columns
tank.description='Quencher'

openTank.description='Skirt-support shell'

basePlate=modelSpace.setSum('basePlate',[stiffBase,platenBase])
basePlate.description='Base-plate ring'
skirtStiff=modelSpace.setSum('skirtStiff',[stiff120x20,platenUp,ringPlatenUp])
skirtStiff.description='Ring stiffener skirt'

internalTank.description='Quencher shell'
stiff80x10.description='Ring stiffeners 80x10'
stiff80x12.description='Ring stiffeners 80x12'
stiff120x20.description='Ring stiffeners 120x20'
stiff120x40.description='Ring stiffeners 120x40'
stiff100x30.description='Ring stiffeners 100x30'
stiffCond.description='Ring stiffeners conduit'



