# -*- coding: utf-8 -*-
import geom
import xc
from postprocess.config import default_config
from actions import loads
from actions import load_cases as lcases
from actions.wind import base_wind as bw

# import local modules
import sys
workingDirectory= default_config.findWorkingDirectory()+'/' #search env_config.py
sys.path.append(workingDirectory)
#import env_config as env
import data as dat
import mesh_gen as msh

#                       ***ACTIONS***
def LoadsCollar(nodLst,loadLst):
    for i in range(len(nodLst)):
        n=nodLst[i]
        l=loadLst[i]
        n.newLoad(xc.Vector(l))
        
#Inertial load (density*acceleration) applied to the elements in a set
grav=10 #Gravity acceleration (m/s2)
selfWeight=loads.InertialLoad(name='selfWeight', lstSets=msh.gravitySets, vAccel=xc.Vector( [0.0,0.0,-dat.coefSelfweigth*dat.grav]))
# dead load platform

# thermal insulation
tInsul=loads.UniformLoadOnSurfaces(name='tInsul', xcSet=msh.internalTank, loadVector=xc.Vector([0,0,-dat.insulW,0,0,0]), refSystem='Global')

platfD=loads.SlidingVectorLoad(name='platfD', nodes=msh.platform.nodes, pntCoord=dat.O_platform,loadVector=-dat.Mass_platform*dat.grav*dat.zUnitF)

# Live loads
platfL=loads.SlidingVectorLoad(name='platfL', nodes=msh.platform.nodes, pntCoord=dat.O_platform,loadVector=-dat.platf_live*dat.zUnitF)
dustL=loads.SlidingVectorLoad(name='dustL', nodes=msh.dustSet.nodes, pntCoord=dat.O_dust,loadVector=-dat.dust_live*dat.zUnitF)

# Wind load
def windLoad(tankWindDef):
    for e in msh.openTank.elements:
        vCoo=e.getCooCentroid(0)
        pres=dat.coeffWindCylOpen*dat.Gf*tankWindDef.getWindPress(vCoo[0],vCoo[1],vCoo[2])
        loadVector=xc.Vector([0,0,-pres])
        e.vector3dUniformLoadLocal(loadVector)
    for e in msh.closedTank.elements:
        vCoo=e.getCooCentroid(0)
        pres=dat.Gf*tankWindDef.getWindPress(vCoo[0],vCoo[1],vCoo[2])
        loadVector=xc.Vector([0,0,-pres])
        e.vector3dUniformLoadLocal(loadVector)
    for e in msh.stiffWind.elements:
        vCoo=e.getCooCentroid(0)
        pres=dat.Gf*dat.Cp_stiffeners*dat.windParams.qz(vCoo[2])
        loadVector=xc.Vector([0,0,pres])
        e.vector3dUniformLoadLocal(loadVector)
    
# Earthquake loads
tankEX=loads.InertialLoad(name='tankEX', lstSets=msh.gravitySets, vAccel=xc.Vector( [dat.accelEarthq,0.0,0]))
tankEXneg=loads.InertialLoad(name='tankEXneg', lstSets=msh.gravitySets, vAccel=xc.Vector( [-dat.accelEarthq,0.0,0]))
tankEY=loads.InertialLoad(name='tankEY', lstSets=msh.gravitySets, vAccel=xc.Vector( [0,dat.accelEarthq,0]))
tankEYneg=loads.InertialLoad(name='tankEYneg', lstSets=msh.gravitySets, vAccel=xc.Vector( [0,-dat.accelEarthq,0]))

# Thermal
# Thermal work (+400ºC)
thermWorkTang_tankwall=loads.StrainLoadOnShells(name='thermWorkTang_tankwall', xcSet=msh.thermalIntTank, DOFstrain=0, strain=dat.tempWork*dat.AISI_alpha)

thermWorkTang_stiff=loads.StrainLoadOnShells(name='thermWorkTang_stiff', xcSet=msh.stiffWorkTemp, DOFstrain=1, strain=dat.tempWork*dat.AISI_alpha)
thermWorkTang_stiffVertCond=loads.StrainLoadOnShells(name='thermWorkTang_stiffVertCond', xcSet=msh.stiffVertCond, DOFstrain=1, strain=dat.tempWork*dat.AISI_alpha)

## vertical
thermWorkVert_tankwall=loads.StrainLoadOnShells(name='thermWorkVert_tankwall', xcSet=msh.thermalIntTank, DOFstrain=1, strain=dat.tempWork*dat.AISI_alpha)

thermWorkRad_stiff=loads.StrainLoadOnShells(name='thermWorkTang_stiff', xcSet=msh.stiffWorkTemp, DOFstrain=0, strain=dat.tempWork*dat.AISI_alpha)
thermWorkVert_stiffVertCond=loads.StrainLoadOnShells(name='thermWorkVert_stiffVertCond', xcSet=msh.stiffVertCond, DOFstrain=0, strain=dat.tempWork*dat.AISI_alpha)


'''
#Thermal expansion
## tangential
thermExpansTang_tankwall=loads.StrainLoadOnShells(name='thermExpansTang_tankwall', xcSet=msh.tankwallPlusHopper, DOFstrain=0, strain=dat.tempRise*dat.AISI_alpha)
thermExpansTang_stiff=loads.StrainLoadOnShells(name='thermExpansTang_stiff', xcSet=msh.stiffeners, DOFstrain=1, strain=dat.tempRise*dat.AISI_alpha)
## vertical
thermExpansVert_tankwall=loads.StrainLoadOnShells(name='thermExpansVert_tankwall', xcSet=msh.tankwallPlusHopper, DOFstrain=1, strain=dat.tempRise*dat.AISI_alpha)
thermExpans_columns=loads.StrainLoadOnBeams(name='thermExpans_columns', xcSet=msh.columns, strain=dat.tempRise*dat.AISI_alpha)
                                      
#Thermal contraction
## tangential
thermContrTang_tankwall=loads.StrainLoadOnShells(name='thermContrTang_tankwall', xcSet=msh.tankwallPlusHopper, DOFstrain=0, strain=dat.tempFall*dat.AISI_alpha)
thermContrTang_stiff=loads.StrainLoadOnShells(name='thermContrTang_stiff', xcSet=msh.stiffeners, DOFstrain=1, strain=dat.tempFall*dat.AISI_alpha)
## vertical
thermContrVert_tankwall=loads.StrainLoadOnShells(name='thermContrVert_tankwall', xcSet=msh.tankwallPlusHopper, DOFstrain=1, strain=dat.tempFall*dat.AISI_alpha)
thermContr_columns=loads.StrainLoadOnBeams(name='thermContr_columns', xcSet=msh.columns, strain=dat.tempFall*dat.AISI_alpha)
'''
# Internal pressure
tankIntPress=loads.UniformLoadOnSurfaces(name='tankIntPress',xcSet=msh.internalTank, loadVector=xc.Vector([0,0,dat.intpress,0,0,0]), refSystem='Local')
#                       ***ACTIONS***
D=lcases.LoadCase(preprocessor=msh.prep,name="D",loadPType="default",timeSType="constant_ts")
D.create()
D.addLstLoads([selfWeight,platfD,tInsul])
LoadsCollar(nodLst=msh.collarNodes,loadLst=dat.condD)

L=lcases.LoadCase(preprocessor=msh.prep,name="L",loadPType="default",timeSType="constant_ts")
L.create()
L.addLstLoads([dustL,platfL])
LoadsCollar(nodLst=msh.collarNodes,loadLst=dat.condL)

WX=lcases.LoadCase(preprocessor=msh.prep,name="WX",loadPType="default",timeSType="constant_ts")
WX.create()
windLoad(dat.tankWindX)
LoadsCollar(nodLst=msh.collarNodes,loadLst=dat.condWX)


WXneg=lcases.LoadCase(preprocessor=msh.prep,name="WXneg",loadPType="default",timeSType="constant_ts")
WXneg.create()
windLoad(dat.tankWindXneg)
LoadsCollar(nodLst=msh.collarNodes,loadLst=dat.condWXneg)

WY=lcases.LoadCase(preprocessor=msh.prep,name="WY",loadPType="default",timeSType="constant_ts")
WY.create()
windLoad(dat.tankWindY)
LoadsCollar(nodLst=msh.collarNodes,loadLst=dat.condWY)


WYneg=lcases.LoadCase(preprocessor=msh.prep,name="WYneg",loadPType="default",timeSType="constant_ts")
WYneg.create()
windLoad(dat.tankWindYneg)
LoadsCollar(nodLst=msh.collarNodes,loadLst=dat.condWYneg)

EX=lcases.LoadCase(preprocessor=msh.prep,name="EX",loadPType="default",timeSType="constant_ts")
EX.create()
EX.addLstLoads([tankEX])
LoadsCollar(nodLst=msh.collarNodes,loadLst=dat.condEX)

EXneg=lcases.LoadCase(preprocessor=msh.prep,name="EXneg",loadPType="default",timeSType="constant_ts")
EXneg.create()
EXneg.addLstLoads([tankEXneg])
LoadsCollar(nodLst=msh.collarNodes,loadLst=dat.condEXneg)

EY=lcases.LoadCase(preprocessor=msh.prep,name="EY",loadPType="default",timeSType="constant_ts")
EY.create()
EY.addLstLoads([tankEY])
LoadsCollar(nodLst=msh.collarNodes,loadLst=dat.condEY)

EYneg=lcases.LoadCase(preprocessor=msh.prep,name="EYneg",loadPType="default",timeSType="constant_ts")
EYneg.create()
EYneg.addLstLoads([tankEYneg])
LoadsCollar(nodLst=msh.collarNodes,loadLst=dat.condEYneg)

T=lcases.LoadCase(preprocessor=msh.prep,name="T",loadPType="default",timeSType="constant_ts")
T.create()
T.addLstLoads([thermWorkTang_tankwall,thermWorkTang_stiff,thermWorkTang_stiffVertCond,thermWorkVert_tankwall,thermWorkRad_stiff,thermWorkVert_stiffVertCond])
LoadsCollar(nodLst=msh.collarNodes,loadLst=dat.condTwork)

#Gradient of temperature: for z=dat.z_hopper_up -> temp=400ºC, for dat.z_stiff_120x20[1] -> temp=0ºC
loadPattern=msh.modelSpace.getCurrentLoadPattern()
z0= dat.z_stiff_120x20[1]
z400=dat.z_hopper_up
gradT=400/(z400-z0)
for e in msh.tankLow_z3.elements:
    z=e.getCooCentroid(True)[2]
    if z>z0:
        temp=(z-z0)*gradT
        strain=temp*dat.AISI_alpha
        eLoad= loadPattern.newElementalLoad("shell_strain_load")
        eLoad.elementTags= xc.ID([e.tag])
        eLoad.setStrainComp(0,0,strain)
        eLoad.setStrainComp(1,0,strain)
        eLoad.setStrainComp(2,0,strain)
        eLoad.setStrainComp(3,0,strain)
        eLoad.setStrainComp(0,1,strain)
        eLoad.setStrainComp(1,1,strain)
        eLoad.setStrainComp(2,1,strain)
        eLoad.setStrainComp(3,1,strain)
for e in msh.columns.elements:
    z=e.getCooCentroid(True)[2]
    if z>z0:
        temp=(z-z0)*gradT
        strain=temp*dat.AISI_alpha
        pDef= xc.DeformationPlane(strain)
        eLoad= loadPattern.newElementalLoad("beam_strain_load")
        eLoad.elementTags= xc.ID([e.tag])
        eLoad.backEndDeformationPlane= pDef
        eLoad.frontEndDeformationPlane= pDef

P=lcases.LoadCase(preprocessor=msh.prep,name="P",loadPType="default",timeSType="constant_ts")
P.create()
P.addLstLoads([tankIntPress])
LoadsCollar(nodLst=msh.collarNodes,loadLst=dat.condP)
'''
Texp=lcases.LoadCase(preprocessor=msh.prep,name="Texp",loadPType="default",timeSType="constant_ts")
Texp.create()
Texp.addLstLoads([thermExpansTang_tankwall,thermExpansTang_stiff,thermExpansVert_tankwall,thermExpans_columns])
LoadsCollar(nodLst=msh.collarNodes,loadLst=dat.condTpos)

Tcontr=lcases.LoadCase(preprocessor=msh.prep,name="Tcontr",loadPType="default",timeSType="constant_ts")
Tcontr.create()
Tcontr.addLstLoads([thermContrTang_tankwall,thermContrTang_stiff,thermContrVert_tankwall,thermContr_columns])
LoadsCollar(nodLst=msh.collarNodes,loadLst=dat.condTneg)
'''
