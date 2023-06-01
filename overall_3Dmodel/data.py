# -*- coding: utf-8 -*-
import math
from materials.ehe import EHE_materials
#from materials.sia262 import SIA262_materials
from materials.ec3 import EC3_materials

 #Geometry
LbeamX=5
LbeamY=6
LcolumnZ=6
Wfoot=2.0
hbeamX=0.5
hbeamY=0.3
hcolumnZ=0.40
wbeamX=0.35
wbeamY=0.5
wcolumnZ=0.40
deckTh=0.20
wallTh=0.5
footTh=0.7

 #Actions
qdeck1=1e3  #N/m2
qdeck2=2e3   #N/m2
Qbeam=3e3  #N/m
qunifBeam=5e3
qLinDeck2=30 #N/m
Qwheel=5e3  #N
firad=math.radians(31)  #internal friction angle (radians)                   
KearthPress=(1-math.sin(firad))/(1+math.sin(firad))     #Active coefficient of p
densSoil=800       #mass density of the soil (kg/m3)
densWater=1000      #mass density of the water (kg/m3)


#Materials
concrete=EHE_materials.HA30
reinfSteel=EHE_materials.B500S
S235JR= EC3_materials.S235JR
S235JR.gammaM= 1.00

eSize= 0.35     #length of elements
