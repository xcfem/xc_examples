# -*- coding: utf-8 -*-
''' Test calculation of anchorage lengths according to clause
    8.4.4 of EC2:2004. Home made test.'''

from __future__ import division
from __future__ import print_function

import os
import math
import sys
from materials.ec2 import EC2_materials
from materials.ec2 import EC2_limit_state_checking
from misc_utils import log_messages as lmsg

__author__= "Luis Claudio Pérez Tato (LCPT)"
__copyright__= "Copyright 2022, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

# Check if silent execution has been requested.
argv= sys.argv
silent= False
if(len(argv)>1):
    if 'silent' in argv[1:]:
        silent= True

diameters= [8e-3, 10e-3, 12e-3, 16e-3, 20e-3, 25e-3, 32e-3, 40e-3]
#diameters= [12e-3]

# Define rebar controllers.
rebarControllerGood= EC2_limit_state_checking.RebarController(concreteCover= 25e-3, spacing= 150e-3, alphaCoefs=(1.0, None, 1.0, 1.0, 1.0), eta1= 1.0, compression= False)
rebarControllerPoor= EC2_limit_state_checking.RebarController(concreteCover= 25e-3, spacing= 150e-3,alphaCoefs=(1.0, None, 1.0, 1.0, 1.0), eta1= 0.7, compression= False)

# Materials
concrete= EC2_materials.C25
steel= EC2_materials.S500C

lbd_straight_good_cond= ['good', 'straight']
lbd_straight_poor_cond= ['poor', 'straight']
lbd_bent_good_cond= ['good', 'bent']
lbd_bent_poor_cond= ['poor', 'bent']
for d in diameters:
    tmp= rebarControllerGood.getDesignAnchorageLength(concrete, rebarDiameter= d, steel= steel, steelEfficiency= 1.0, barShape= 'straight')
    tmp= math.ceil(tmp*1e2)*10
    lbd_straight_good_cond.append(tmp)
    tmp= rebarControllerPoor.getDesignAnchorageLength(concrete, rebarDiameter= d, steel= steel, steelEfficiency= 1.0, barShape= 'straight')
    tmp= math.ceil(tmp*1e2)*10
    lbd_straight_poor_cond.append(tmp)
    tmp= rebarControllerGood.getDesignAnchorageLength(concrete, rebarDiameter= d, steel= steel, steelEfficiency= 1.0, barShape= 'bent')
    tmp= math.ceil(tmp*1e2)*10
    lbd_bent_good_cond.append(tmp)
    tmp= rebarControllerPoor.getDesignAnchorageLength(concrete, rebarDiameter= d, steel= steel, steelEfficiency= 1.0, barShape= 'bent')
    tmp= math.ceil(tmp*1e2)*10
    lbd_bent_poor_cond.append(tmp)

values= [lbd_straight_good_cond, lbd_straight_poor_cond,lbd_bent_good_cond,lbd_bent_poor_cond]
refValues= [['good', 'straight', 230, 320, 410, 600, 780, 1010, 1300, 1760], ['poor', 'straight', 330, 450, 580, 850, 1110, 1450, 1850, 2510], ['good', 'bent', 320, 410, 490, 650, 810, 1010, 1300, 1760], ['poor', 'bent', 460, 580, 700, 930, 1160, 1450, 1850, 2510]]

err= 0.0 

for row1, row2 in zip(values, refValues):
    for v1, v2 in zip(row1[2:], row2[2:]):
        err+=(v1-v2)**2
err= math.sqrt(err)


if not silent:
    print(values)
    print(err)
    # Tabular output
    numDiameters= len(diameters)
    diametersCaption= ['']*numDiameters
    diametersCaption[0]= 'Reinforcement in tension, bar diameter (mm)'
    diametersHeader= ['']*numDiameters
    for i, d in enumerate(diameters):
        diametersHeader[i]= str(int(d*1e3))

    header2= ['bar', 'bond', 'concrete', 'steel']+diametersCaption
    header3= ['type', 'condition', 'type', 'type',]+diametersHeader
    headers= [header2, header3]

    results= headers
    results.append(['']*len(header2))
    for row in values:
        resultRow= [row[1], row[0], concrete.materialName, steel.materialName]
        resultRow.extend(row[2:])
        results.append(resultRow)

    from tabulate import tabulate
    print(tabulate(results))

    # Write csv file.
    import csv
    fileName= concrete.materialName+'_'+steel.materialName+'_anchorage_lengths.csv'
    with open(fileName, 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in results:
            writer.writerow(row)


import os
from misc_utils import log_messages as lmsg
fname= os.path.basename(__file__)
if(err<1e-8):
    print("test "+fname+": ok.")
else:
    lmsg.error(fname+' ERROR.')





