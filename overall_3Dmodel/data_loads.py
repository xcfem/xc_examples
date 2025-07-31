import math

# Loads data
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
# Vehicle concentrated loads
from actions.roadway_traffic import load_model_base as lmb
# wheels
w1=lmb.WheelLoad(pos=geom.Pos2d(-1,-1.79),ld=35e3,lx=0.4,ly=0.4)
w2=lmb.WheelLoad(pos=geom.Pos2d(1,-1.79),ld=35e3,lx=0.4,ly=0.4)
w3=lmb.WheelLoad(pos=geom.Pos2d(-1,-2.99),ld=35e3,lx=0.4,ly=0.4)
w4=lmb.WheelLoad(pos=geom.Pos2d(1,-2.99),ld=35e3,lx=0.4,ly=0.4)
w5=lmb.WheelLoad(pos=geom.Pos2d(-1,-4.19),ld=35e3,lx=0.4,ly=0.4)
w6=lmb.WheelLoad(pos=geom.Pos2d(1,-4.19),ld=35e3,lx=0.4,ly=0.4)

truck3axes=lmb.LoadModel(wLoads=[w1,w2,w3,w4,w5,w6])

# shrinkage
epsShrinkage=350e-6 #shrinkage strain
