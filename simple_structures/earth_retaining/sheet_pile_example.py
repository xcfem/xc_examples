# -*- coding: utf-8 -*-
''' Sheet-piles according to chapter 14 of the book "Principles of Foundation 
Engineering" of Braja M. Das. Eight Edition. CENGAGE Learning. 2016.

Example 14.1
'''

from __future__ import division
from __future__ import print_function

import sys
import math
from geotechnics import earth_pressure
from geotechnics.earth_retaining import sheet_pile
from scipy.constants import g

# Check if silent execution has been requested.
argv= sys.argv
silent= False
if(len(argv)>1):
    if 'silent' in argv[1:]:
        silent= True

soil= earth_pressure.RankineSoil(phi= math.radians(32), rho= 15.90e3/g, rhoSat= 19.33e3/g)
L1= 2.0 # m
L2= 3.0 # m

# Sheet-pile object.
sheetPile= sheet_pile.CantileverSheetPile(soil= soil, waterTableDepth= L1, excavationDepth= L1+L2)
    
# Theoretical depth
D= sheetPile.getDepth(depthSafetyFactor= 1.0)
# Total length
L= sheetPile.getTotalLength(depthSafetyFactor= 1.3)

# Maximum bending moment.
Mmax= sheetPile.getMaxBendingMoment()
ratioMmax= abs(Mmax-209.57330322152927e3)/209.57330322152927e3

if not silent:
    print('D= ', D, 'm')
    print('L= ', L, 'm')
    print('Mmax= ', Mmax/1e3,'kN.m/m')
    print('ratioMmax= ', ratioMmax)


import os
from misc_utils import log_messages as lmsg
fname= os.path.basename(__file__)
if abs(ratioMmax)<1e-10:
    print('test: '+fname+': ok.')
else:
    lmsg.error('test: '+fname+' ERROR.')
