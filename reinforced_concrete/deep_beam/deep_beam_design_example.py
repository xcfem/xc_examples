# -*- coding: utf-8 -*-
''' Design of  deep beam according to ACI 318-11. Example taken from the document:

Design of Deep Beam (Transfer Girder) Using Strut-and-Tie Model (ACI 318-11) from Structure Point (https://structurepoint.org)
'''

from __future__ import division
from __future__ import print_function

import math
import geom
from scipy.constants import g


__author__= "Luis Claudio Pérez Tato (LCPT)"
__copyright__= "Copyright 2023, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

# Units.
psi= 6894.75729 # pascals
lbf= 4.4482216153 # newton
kip= lbf*1e3 # newton
inch= 2.54e-2 # meters
feet= 12*inch

# Design data.

## Materials.
fcp= 4000*psi
fy= 60000*psi
concreteDensity= 150*lbf/feet**3 # kg/m3

## Loads
DL= 180*kip
LL= 250*kip

## Deep beam dimensions.
depth= 60*inch
thickness= 20*inch
width= 176*inch
supportsWidth= 16*inch
span= width-supportsWidth

# Solution

## Factored load and reactions.
Psw= concreteDensity*depth*width*thickness
Pu= 1.2*(Psw+DL)+1.6*LL
Ru= Pu/2.0

# Deep beam check. ACI 318-11 (10.7.1 & 11.7.1)
isDeep= (span/depth<4)
ok= (isDeep==True)

# Maximum Shear Capacity of the Cross Section
Vu= Ru
phiV= 0.75
d= 0.9*depth
phiVn= phiV*10*math.sqrt(fcp/psi)*thickness/inch*d/inch*lbf # ACI 318-11 (11.7.3 & 10.7.2)
phiVnRef= 512.3*kip
ratio1= abs(phiVn-phiVnRef)/phiVnRef
ok= ok and (ratio1<1e-4)

# Stablish strut model.
A= geom.Pos2d(0,0)
C= geom.Pos2d(span/2, depth-2*5*inch)
B= geom.Pos2d(span, 0)

strutAC= geom.Segment2d(A,C)
strucBC= geom.Segment2d(B,C)
tieAC= geom.Segment2d(A,B)

strutLength= strutAC.getLength()
refStrutLength= 94.3*inch
ratio2= abs(strutLength-refStrutLength)/refStrutLength

print('Psw= ', Psw/1e3, ' kN, ', Psw/kip, 'kip')
print('Pu= ', Pu/1e3, ' kN, ', Pu/kip, 'kip')
print('Ru= ', Ru/1e3, ' kN, ', Ru/kip, 'kip')
print('phiVn= ', phiVn/1e3, ' kN, ', phiVn/kip, 'kip')
print('\nTruss model:')
print('  strut length: ',strutLength, ' m, ', strutLength/inch, 'in')


print('test OK:'+str(ok))
