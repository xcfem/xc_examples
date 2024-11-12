# -*- coding: utf-8 -*-
''' Verification test for SoilLayers class inspired in the example 12.1 of the book "Principles of Foundation Engineering" of Braja M. Das. Eight Edition. CENGAGE Learning. 2016.'''

import math
from geotechnics import earth_pressure
from scipy.constants import g
import excavation_process as ep

# Materials definition
## Soil materials
soil= earth_pressure.RankineSoil(phi= math.radians(30), rho= 16.5e3/g, rhoSat= 19.3e3/g)
### Soil strata.
L1= 2.5 # Water table depth (m).
L2= L1+2.5 # Todal depth (m).
soilLayersDepths= [0.0, L2]
soilLayers= [soil, soil]
soilStrata= ep.SoilLayers(depths= soilLayersDepths, soils= soilLayers, waterTableDepth= L1)

p0= soilStrata.getAtRestPressureAtDepth(depth= 0.0)
err= p0**2
p1= soilStrata.getAtRestPressureAtDepth(depth= L1)
p1Ref= 0.5*16.5*2.5e3
err+= (p1-p1Ref)**2
p2= soilStrata.getAtRestPressureAtDepth(depth= L2)
p2Ref= 0.5*((16.5+19.3-g)*2.5e3)
err+= (p2-p2Ref)**2

u0= soilStrata.getHydrostaticPressureAtDepth(depth= 0.0)
err+= u0**2
u1= soilStrata.getHydrostaticPressureAtDepth(depth= L1)
err+= u1**2
u2= soilStrata.getHydrostaticPressureAtDepth(depth= L2)
u2Ref= g*2.5e3
err+= (u2-u2Ref)**2

err= math.sqrt(err)

'''
print(p0/1e3)
print(p1/1e3)
print(p2/1e3)

print(u0/1e3)
print(u1/1e3)
print(u2/1e3)

print(err)
'''

import os
from misc_utils import log_messages as lmsg
fname= os.path.basename(__file__)
if abs(err)<1e-8:
    print('test: '+fname+': ok.')
else:
    lmsg.error('test: '+fname+' ERROR.')
