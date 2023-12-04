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
leverArm= depth-2*5*inch
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
C= geom.Pos2d(span/2, leverArm)
B= geom.Pos2d(span, 0)

strutAC= geom.Segment2d(A,C)
strucBC= geom.Segment2d(B,C)
tieAB= geom.Segment2d(A,B)

strutLength= strutAC.getLength()
refStrutLength= 94.3*inch
ratio2= abs(strutLength-refStrutLength)/refStrutLength
ok= ok and (ratio2<1e-3)

tieLength= tieAB.getLength()
refTieLength= 160*inch
ratio3= abs(tieLength-refTieLength)/refTieLength
ok= ok and (ratio3<1e-4)

strutForce= Ru*strutLength/leverArm
refStrutForce= 603*kip
ratio4= abs(strutForce-refStrutForce)/refStrutForce
ok= ok and (ratio4<1e-2)

tieForce= Ru*(tieLength/2)/leverArm
refTieForce= 512*kip
ratio5= abs(tieForce-refTieForce)/refTieForce
ok= ok and (ratio5<1e-2)

tieStrutAngle= strutAC.getAngle(tieAB) # ACI 318-11 (A.2.5)
refTieStrutAngle= math.radians(32)
ratio6= abs(tieStrutAngle-refTieStrutAngle)/refTieStrutAngle
ok= ok and (ratio6<1e-3)

## Effective Concrete Strength for the Struts ACI 318-11 (A.3.3)
beta= 0.75 # ACI 318-11 (A.3.2.2(a)) with reinforcement satisfying A.3.3
strutStressLimit= 0.85*beta*fcp # ACI 318-11 (Eq. A-3)
strutStressLimitRef= 2550*psi
ratio7= abs(strutStressLimit-strutStressLimit)/strutStressLimit
ok= ok and (ratio7<1e-5)

print('XXX continue here (page 12 of the report).')

requiredTieArea= tieForce/(0.75*fy)

print('Psw= ', Psw/1e3, ' kN, ', Psw/kip, 'kip')
print('Pu= ', Pu/1e3, ' kN, ', Pu/kip, 'kip')
print('Ru= ', Ru/1e3, ' kN, ', Ru/kip, 'kip')
print('phiVn= ', phiVn/1e3, ' kN, ', phiVn/kip, 'kip')
print('\nTruss model:')
print('  strut length: ', strutLength, ' m, ', strutLength/inch, 'in')
print('  tie length: ', tieLength, ' m, ', tieLength/inch, 'in')
print('  force in diagonal struts:, ', strutForce/1e3, ' kN, ', strutForce/kip, 'kip')
print('  force in diagonal tie:, ', tieForce/1e3, ' kN, ', tieForce/kip, 'kip')
print('  angle between the diagonal struts and horizontal tie (must be greater than 25): ', math.degrees(tieStrutAngle), 'º')
print('  limit stress in struts -ACI 318-11 (Eq. A-3)-: ', strutStressLimit/1e6 , 'MPa, ', strutStressLimit/psi, ' psi')
print('XXX continue here (page 12 of the report).')
print('  required reinforcement area: ', requiredTieArea/1e-4 , 'cm2, ', requiredTieArea/inch**2, ' inch2')


print('test OK:'+str(ok))
print(ratio2, ratio3, ratio4, ratio5, ratio6, ratio7)

import os
from misc_utils import log_messages as lmsg
fname= os.path.basename(__file__)
if ok:
    print('test '+fname+': ok.')
else:
    lmsg.error(fname+' ERROR.')
