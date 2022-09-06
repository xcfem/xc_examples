# -*- coding: utf-8 -*-
''' Based on the example 13.18 from https://faculty.ksu.edu.sa/sites/default/files/ce_481_lateral_earth_pressure_0.pdf
'''

import math
from geotechnics import frictional_cohesive_soil as fcs
from scipy.constants import g


wallHeight= 4.0 #m
soilGamma= 15e3 # N/m3
soilRho= soilGamma/g
fi= math.radians(26)
cohesion= 8e3 # N/m2

q= 10e3 # surface load

soil= fcs.FrictionalCohesiveSoil(phi= fi, c= cohesion, rho= soilRho)

crackDepth= soil.getCoulombTensionCrackDepth(sg_v=q, a= 0, b= 0)

sigma_a= soil.eah_coulomb(sg_v= q, a= 0, b= 0)
sigma_0= soil.eah_coulomb(sg_v=crackDepth*soil.gamma()+q, a= 0, b= 0)
sigma_b= soil.eah_coulomb(sg_v=wallHeight*soil.gamma()+q, a= 0, b= 0)
earthPressureForce= sigma_b*(wallHeight-crackDepth)/2.0
earthPressureLeverArm= (wallHeight-crackDepth)/3.0

print('horizontal pressure at the top of the wall sigma_a= ',sigma_a/1e3, ' kN/m2') 
print('horizontal pressure at crack depth sigma_0= ',sigma_0/1e3, ' kN/m2') 
print('horizontal pressure at the bottom of the wall sigma_b= ',sigma_b/1e3, ' kN/m2') 
print('earth pressure force P= ',earthPressureForce/1e3, ' kN/m')
print('earth pressure lever arm h= ', earthPressureLeverArm, 'm')
