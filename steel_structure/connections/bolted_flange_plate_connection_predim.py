# -*- coding: utf-8 -*-
''' Predimensioning of a bolted flange plate connection
    (a plate that is bolted to a beam flange and then
     attached to a column or other structural element).'''

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2015, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

import sys
import xc
from model import predefined_spaces
from materials.astm_aisc import ASTM_materials # steel

# Check if silent execution has been requested.
argv= sys.argv
silent= False
if(len(argv)>1):
    if 'silent' in argv[1:]:
        silent= True

# Problem type
feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor
nodes= preprocessor.getNodeHandler
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)

#Materials
## Steel material
steel= ASTM_materials.A36
steel.gammaM= 1.00
## Profile geometry
shape= ASTM_materials.WShape(steel,'W10X39')
xcSection= shape.defElasticShearSection2d(preprocessor)

# Geometry.
n1= modelSpace.newNodeXY(0.0,0.0)
n2= modelSpace.newNodeXY(1.0,0.0)

# Element defininion
trfs= preprocessor.getTransfCooHandler
lin= trfs.newLinearCrdTransf2d("lin")
elements= preprocessor.getElementHandler
elements.defaultTransformation= lin.name
elements.defaultMaterial= xcSection.name
beam2d= elements.newElement("ElasticBeam2d",xc.ID([n1.tag,n2.tag]))

# Connected member.
beam2d.setProp('crossSection', shape)
member= ASTM_materials.ConnectedMember(beam2d)

# Return a minimal bolted plate for the beam flange. The
# length of the plate is just enough to accomodate the bolts
# and its width is chosen as the maximum of the flange width
# and the bolted plate minimum width.

# :param boltSteel: steel type of the bolts that connect the plate with
#                   the flange.
# :param plateSteel: steel type of the bolted plate.
flangeBoltedPlate= member.getFlangeBoltedPlateCore(boltSteel= ASTM_materials.A490, plateSteel= ASTM_materials.A490)

width= flangeBoltedPlate.getWidth()
ratio1= abs(width-203e-3)/203e-3
length= flangeBoltedPlate.getLength()
ratio2= abs(length-500e-3)/500e-3
thickness= flangeBoltedPlate.getThickness()
ratio3= abs(thickness-5e-3)/5e-3
boltArray= flangeBoltedPlate.boltArray
numberOfBolts= boltArray.getNumberOfBolts()
ratio4= abs(numberOfBolts-8)/8
boltDiameter= boltArray.bolt.diameter
ratio5= abs(boltDiameter-16e-3)/16e-3

if not silent:
    print('plate width: ', width*1e3, ' mm')
    print('plate length: ', length*1e3, ' mm')
    print('plate thickness: ', thickness*1e3, ' mm')
    print('number of bolts: ', numberOfBolts)
    print('bolt diameter: ', boltDiameter)

'''
print('ratio1= ', ratio1)
print('ratio2= ', ratio2)
print('ratio3= ', ratio3)
print('ratio4= ', ratio4)
print('ratio5= ', ratio5)
'''

from misc_utils import log_messages as lmsg
import os
fname= os.path.basename(__file__)
if (abs(ratio1)<1e-9) & (abs(ratio2)<1e-9) & (abs(ratio3)<1e-9) & (abs(ratio4)<1e-9) & (abs(ratio5)<1e-9):
    print('test: '+fname+': ok.')
else:
    lmsg.error(fname+' ERROR.')
