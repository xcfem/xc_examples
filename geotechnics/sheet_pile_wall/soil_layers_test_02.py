# -*- coding: utf-8 -*-
''' Verification test for SoilLayers class inspired in the example 12.3 of the book "Principles of Foundation Engineering" of Braja M. Das. Eight Edition. CENGAGE Learning. 2016.'''

import math
from geotechnics import earth_pressure
from scipy.constants import g
import excavation_process as ep

# Units
ft= 0.3048
lbf= 4.44822

# Materials definition
## Soil materials
drySoil= earth_pressure.RankineSoil(phi= math.radians(30), rho= 102*lbf/ft**3/g, rhoSat= 121*lbf/ft**3/g)
wetSoil= earth_pressure.RankineSoil(phi= math.radians(36), rho= 102*lbf/ft**3/g, rhoSat= 121*lbf/ft**3/g)
### Soil strata.
L1= 10*ft # Water table depth (m).
L2= L1+10*ft # Todal depth (m).
soilLayersDepths= [0.0, L1, L2]
soilLayers= [drySoil, wetSoil, wetSoil]
soilStrata= ep.SoilLayers(depths= soilLayersDepths, soils= soilLayers, waterTableDepth= L1)

p0= soilStrata.getActivePressureAtDepth(depth= 0.0)
err= p0**2
p1minus= soilStrata.getActivePressureAtDepth(depth= L1-1e-3)
p1minusRef= 340*lbf/ft/ft
err+= ((p1minus-p1minusRef)/p1minusRef)**2
p1plus= soilStrata.getActivePressureAtDepth(depth= L1+1e-3)
p1plusRef= 265.2*lbf/ft/ft
err+= ((p1plus-p1plusRef)/p1plusRef)**2
p2= soilStrata.getActivePressureAtDepth(depth= L2)
p2Ref= 417.6*lbf/ft/ft
err+= ((p2-p2Ref)/p2Ref)**2

u0= soilStrata.getHydrostaticPressureAtDepth(depth= 0.0)
err+= u0**2
u1= soilStrata.getHydrostaticPressureAtDepth(depth= L1)
err+= u1**2
u2= soilStrata.getHydrostaticPressureAtDepth(depth= L2)
u2Ref= g*(L2-L1)*1e3
err+= (u2-u2Ref)**2

err= math.sqrt(err)

'''
print(p0/1e3, 'kN/m2')
print(p1minus/1e3, 'kN/m2')
print(p1plus/1e3, 'kN/m2')
print(p2/1e3, 'kN/m2')

print('u0= ', u0/1e3, 'kN/m2')
print('u1= ', u1/1e3, 'kN/m2')
print('u2= ', u2/1e3, 'kN/m2')
print('u2Ref= ', u2Ref/1e3, 'kN/m2')

print('err= ', err)
'''


import os
from misc_utils import log_messages as lmsg
fname= os.path.basename(__file__)
if abs(err)<.01:
    print('test: '+fname+': ok.')
else:
    lmsg.error('test: '+fname+' ERROR.')
