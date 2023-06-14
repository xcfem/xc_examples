# -*- coding: utf-8 -*-
from __future__ import division 
from __future__ import print_function

import os
import geom
import xc
import math
from misc_utils import data_struct_utils as dsu
from materials.astm_aisc import ASTM_materials as astm
from actions.wind import base_wind as bw

#units
kmh2ms=1/3.6

# ** Geometry data **
#Z coordinates
# dist_stiff_80x10=[0.35+5.5+0.3+1.95,1.95,2*1.95]+4*[1.95]+[2.25+1.965]+2*[1.95] # 24/11/2020 changed for thicken stiffeners near conduit support
z_max=[12+12+12.085]

dist_stiff_80x10=[0.35+5.5+0.3+1.95,1.95,2*1.95]+2*[1.95]+[2*1.95+2.25+1.965]+2*[1.95]
z_stiff_80x10=[sum(dist_stiff_80x10[0:i]) for i in range(1,len(dist_stiff_80x10)+1)]
z_stiff_80x10.append(22.4)
z_stiff_80x10.sort()
z_stiff_80x12=[z_max[0]]
z_stiff_cond=[20,21]
z_stiff_175x25=[0]
z_stiff_200x25=[0.3]
z_stiff_120x20=[0.35+5.5,0.3+5.5+0.3]
z_stiff_120x40=[12]  #change in thickness
z_stiff_100x30=[12+12]  
z_cone=[12+12-1.4,z_max[0]]
z_holes=[0.35+1.012,0.35+4.8]
bStiff=[80e-3,175e-3,200e-3,120e-3,100e-3]
z_platf=[z_stiff_100x30[0]+5.07+2.5]
zList=z_stiff_80x10+z_stiff_175x25+z_stiff_200x25+z_stiff_120x20+z_stiff_120x40+z_stiff_100x30+z_cone+z_max+z_holes+z_platf+z_stiff_cond
zList=dsu.remove_duplicates_list(zList)
zList.sort()
#Thickness
tWebStiffCond=25e-3 # thickness of the web of stiffeners near conduit
wWebStiffCond=0.15 # width of the web of sstiffeners near conduit
tFlgStiffCond=20e-3 # thickness of the flanges of stiffeners near conduit
wFlgStiffCond=0.15 # width of the flange of stiffeners near conduit

if tFlgStiffCond > 0:
    zFlgStiffCond=[z_stiff_cond[0]-wFlgStiffCond/2,
                   z_stiff_cond[0]+wFlgStiffCond/2,
                   z_stiff_cond[1]-wFlgStiffCond/2,
                   z_stiff_cond[1]+wFlgStiffCond/2
    ]
    zList=zList+zFlgStiffCond
    zList=dsu.remove_duplicates_list(zList)
    zList.sort()

tBase=12e-3
tMidd=8e-3
tUp=6e-3
tPlatenBase=20e-3 # thicknes of the vertical stiffeners between
                  # ring stiffeners in the base
tPlatenUp=10e-3   # thickness of the vertical stiffeners between
                  # the annular stiffeners over the main opening
#Radial coordinate
Rbase=round((4598e-3+2*tBase)/2,3)
RtopCone=round((1908e-3+2*tUp)/2,3)
rList=[Rbase]+[round(Rbase+b,3) for b in bStiff]
rList=dsu.remove_duplicates_list(rList)
rList.sort()
Ranchors=2.41
#Angular coordinate
# angAnchors =[i*11.25+2.113 for i in range(32)]#angular coordinates of anchors (true angular coordinates, we'll not use them. Instead we'll use fictitious coordinates to catch all the points in the circumference.
angAnchors=[i*6 for i in range(60)]
#angular coordinates of platens between ring stiffeners in base
angPlaten1=[i*11.25 for i in range(32)] 
angPlaten2=[i*11.25+2*2.113 for i in range(32)]

#angList=angAnchors+angPlaten1+angPlaten2
angList=angPlaten1+angPlaten2
angList.sort()

'''
ang=11.25/2
ndiv=int(360/ang)
angList=[i*ang for i in range(ndiv)] 
'''
angHole0=(0.8/Rbase)*180/math.pi
angHole1=(2.57/Rbase)*180/math.pi

angCooHole1=[angHole1/2,360-angHole1/2]
angCooHole0=[180-32-angHole0/2,180-32+angHole0/2]

# Hopper geometry
z_hopper_down=z_holes[1]
z_hopper_up=z_stiff_80x10[0]
r_hopper_down=1.45/2
r_hopper_up=Rbase
rListHopp=[r_hopper_down]
zListHopp=[z_hopper_down,z_hopper_up]

tHopper=6e-3  #hopper thickness
slopeCone=(RtopCone-Rbase)/(z_cone[1]-z_cone[0])

steel_W=astm.A36
#Material AISI 304L (shells and rolled shapes)
#Properties of AISI 304L at 400ºC
AISI_alpha=1.8e-5  # thermal expansion coefficient of steel
AISI_E=172e9
AISI_fy=150e6
AISI_fu=400e6



##Loads
# Self-weight
coefSelfweigth=500/437. #Corrección de la gravedad para que salga
                        #el peso indicado en el plano **COMPROBAR**
# thickness platform elements (added mass of platform)
Mass_platform=2730+1780  #mass of the platform [kg]
sPlatf=9.0 # surface platform [m2]
thick_platf=0.08 #platform thickness [m] **COMPROBAR**
# data to apply loads on platform using sliding vectors
O_platform=(0,0,z_platf[0]) #point coord. of sliding vector
O_dust=(0,0,z_stiff_80x10[0]) #point coord. of sliding vector
zUnitF=xc.Vector([0,0,1,0,0,0])
# Thermal insulation
insulW=1.4e3*0.1 # (N/m2) weigth of 100 mm of thermal insulation (1.4 kN/m3)
            

# Dust weight
#dust_live=11.4e3  #dust weight [N]  #annulled on 23/11/2020
dustV=1.9   # Volumen of dust (m3)
dustEspW=11e3  # dust especific weigth (N/m3)
dust_live=dustV*dustEspW

# Platform
platf_live=3e3*sPlatf # 4000  #platform live load [N]


#Wind data
v=155*kmh2ms #basic speed wind [m/s]
Kd=0.95      #wind directionality factor
Kzt=1.0      #topographic factor
I=1.15       #importance factor
alpha=9.5    #terrain exposure constant (exposure C)
zg=275       #terrain exposure constant (exposure C)
Gf=0.87      #gust effect factor

Cp_stiffeners=1.6 #net pressure coefficient stiffeners

#Wind action definition
windParams=bw.windParams(v,Kd,Kzt,I,alpha,zg)
tankWindX=bw.cylindrWind(diam=2*Rbase,height=z_max[0],windParams=windParams,windComp=[1,0],zGround=0,xCent=0,yCent=0)
tankWindXneg=bw.cylindrWind(diam=2*Rbase,height=z_max[0],windParams=windParams,windComp=[-1,0],zGround=0,xCent=0,yCent=0)
tankWindY=bw.cylindrWind(diam=2*Rbase,height=z_max[0],windParams=windParams,windComp=[0,1],zGround=0,xCent=0,yCent=0)
tankWindYneg=bw.cylindrWind(diam=2*Rbase,height=z_max[0],windParams=windParams,windComp=[0,-1],zGround=0,xCent=0,yCent=0)

coeffWindCylOpen=1.6 #coefficient that multiplies pressures in open surfaces

#Thermal data
tempRise=30    #temperature rise (ºC)
tempFall=-30   #temperature fall (ºC)
tempWork=400   # thermal work load (ºC)

# tempWork=25  #limit convergence
#Seismic acceleration
grav=9.81
T=0.3
Sa=0.0907*grav  # m/s2
Iocc=1.25  #occupancy factor
accelEarthq=coefSelfweigth*Sa*Iocc  # **COMPROBAR** cuando se ajuste el peso
#FseismPipe=3.19e3 #seisme resultant over upper half pipe [N]  (see model conduct)

#Pressure
intpress=-7845   # internal pressure (-800 mmcda)
# Conduit collar loads on quencher
condD=[[-13770,-400,-3870,0,0,0],	
	[-13650,350,-3870,0,0,0],	
	[16270,110,-3880,0,0,0],	
	[16150,-170,-3880,0,0,0]]
condL=[[-680,-240,-10,0,0,0],	
	[660,-240,10,0,0,0],	
	[710,-320,10,0,0,0],	
	[-720,-280,-10,0,0,0]]
condP=[[6870,-1070,10,0,0,0],	
	[6620,1100,0,0,0,0],	
	[-3860,-1320,-10,0,0,0],	
	[-3590,1390,0,0,0,0]]
condEX=[[4590,-260,10,0,0,0],	
	[4590,260,10,0,0,0],	
	[1530,20,-10,0,0,0],	
	[1530,-20,-10,0,0,0]]
condEY=[[7840,3420,-140,0,0,0],	
	[-7860,3410,140,0,0,0],	
	[-7070,2410,190,0,0,0],	
	[7120,2410,-190,0,0,0]]
condTneg=[[20,0,0,0,0,0],	
	[-10,0,0,0,0,0],	
	[10,10,0,0,0,0],	
	[30,0,0,0,0,0]]
condTpos=[[-20,0,0,0,0,0],	
	[10,0,0,0,0,0],	
	[-10,-10,0,0,0,0],	
	[-30,0,0,0,0,0]]
condTwork=[[-2590,-60280,-8980,0,0,0],	
	[-2660,60290,-8980,0,0,0],	
	[8170,61710,8980,0,0,0],	
	[8250,-61690,8980,0,0,0]]
condWXneg=[[-23720,1160,40,0,0,0],	
	[-22080,-1930,-30,0,0,0],	
	[-8690,-900,-10,0,0,0],	
	[-10070,460,50,0,0,0]]
condWX=[[35260,-1670,110,0,0,0],	
	[33950,2170,120,0,0,0],	
	[10630,230,-60,0,0,0],	
	[12000,270,-70,0,0,0]]
condWYneg=[[-103820,-47980,2260,0,0,0],	
	[109220,-46930,-2330,0,0,0],	
	[95020,-31540,-3000,0,0,0],	
	[-94120,-31670,2980,0,0,0]]
condWY=[[107720,46750,-2310,0,0,0],	
	[-103610,47580,2320,0,0,0],	
	[-92630,31460,3030,0,0,0],	
	[94940,31090,-2970,0,0,0]]
condEXneg=[[-4590,260,-10,0,0,0],	
	[-4590,-260,-10,0,0,0],	
	[-1530,-20,10,0,0,0],	
	[-1530,20,10,0,0,0]]
condEYneg=[[-7840,-3420,140,0,0,0],	
	[7860,-3410,-140,0,0,0],	
	[7070,-2410,-190,0,0,0],	
	[-7120,-2410,190,0,0,0]]


# Coordinates of the conduit collar
ang_reactor=math.radians(32)
xaxis=-Rbase*math.cos(ang_reactor)
yaxis=Rbase*math.sin(ang_reactor)
wCollar=2.245
hCollar=1.0
alpha=math.asin(wCollar/2/Rbase)
x1=xaxis-wCollar/2*math.sin(ang_reactor)
x2=xaxis+wCollar/2*math.sin(ang_reactor)
y1=yaxis-wCollar/2*math.cos(ang_reactor)
y2=yaxis*wCollar/2*math.cos(ang_reactor)
z_1=20
z_2=z_1+hCollar
x=-Rbase*math.cos(alpha)
coord_20016=geom.Pos3d(x2,y2,z_2)
coord_20017=geom.Pos3d(x1,y1,z_2)
coord_20018=geom.Pos3d(x1,y1,z_1)
coord_20019=geom.Pos3d(x2,y2,z_1)

eSize=0.5

#vertical stiffeners in conduit reinforcements
angAux=math.degrees(math.atan((wCollar/2)/Rbase))

angCondAx=180-32
ang_vstiff_cond=[angCondAx-angAux+15,
                 angCondAx-angAux+20,
                 angCondAx+angAux-5,
                 angCondAx+angAux+1]

tVertStiffCond=20e-3 #thickness
