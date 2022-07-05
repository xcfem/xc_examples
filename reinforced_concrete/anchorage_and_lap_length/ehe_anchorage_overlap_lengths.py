# -*- coding: utf-8 -*-
''' Test calculation of anchorage lengths according to EHE.
    Home made test.'''

from __future__ import division
from __future__ import print_function

import math
import os
from materials.ehe import EHE_materials
from materials.ehe import EHE_limit_state_checking
from misc_utils import log_messages as lmsg
from collections import OrderedDict
from pyexcel_ods import save_data

__author__= "Luis Claudio Pérez Tato (LCPT"
__copyright__= "Copyright 2020, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

# Materials
concreteList= [EHE_materials.HA30]# , EHE_materials.HP50]
steel= EHE_materials.B500S
diameters= [8e-3, 10e-3, 12e-3, 16e-3, 20e-3, 25e-3]
spacing= [0.10] #[0.1,0.2]
cCover= .035

# Rebar controller.
rebarControllerPosI= EHE_limit_state_checking.RebarController(concreteCover= cCover, pos= 'I', compression= True)
rebarControllerPosII= EHE_limit_state_checking.RebarController(concreteCover= cCover, pos= 'II', compression= True)

rows= list([[u'Hormigón', u'Diámetro', u'Separación', 'LsI', 'LsII', 'LnI', 'LnII'], ['','(mm)', '(cm)', '(cm)', '(cm)', '(cm)', '(cm)']])

fmt= '{:.0f}'

def to5cm(value):
    return (math.ceil(value/.05)*.05)*100

#  length.
for c in concreteList:
    for diam in diameters:
        for s in spacing:
            lsI= rebarControllerPosI.getLapLength(c,diam,steel, distBetweenNearestSplices= s, steelEfficiency= 1.0, ratioOfOverlapedTensionBars= 1.0)
            lsII= rebarControllerPosII.getLapLength(c,diam,steel, distBetweenNearestSplices= s, steelEfficiency= 1.0, ratioOfOverlapedTensionBars= 1.0)
            lbI= rebarControllerPosI.getNetAnchorageLength(c, diam, steel, steelEfficiency= 1.0, barShape= 'straight')
            lbII= rebarControllerPosII.getNetAnchorageLength(c, diam, steel, steelEfficiency= 1.0, barShape= 'straight')
            prevRow= rows[-1]
            row= [str(c), diam*1e3, fmt.format(s*100), to5cm(lsI), to5cm(lsII), to5cm(lbI), to5cm(lbII)]
            if((row[3]!= prevRow[3]) or (row[4]!= prevRow[4]) or (row[5]!= prevRow[5]) or (row[6]!= prevRow[6])):
                if(row[1]==prevRow[1]):
                    row[1]= ''
                rows.append(row)
            else:
                prevRow[2]= '-'


data= OrderedDict()
data.update({'sheet1':rows})
save_data('ehe_anchorage_overlap_lengths.ods', data)

