# -*- coding: utf-8 -*-
''' Test based on the example 1.2 of the Book: Non-linear Finite Element Analysis of Solids and Structures. Volume 1: Essentials. M. A. Crisfield. April 2000.'''

from __future__ import print_function
from __future__ import division

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2021, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

import math
import xc_base
import geom
import xc
from solution import predefined_solutions
from model import predefined_spaces
from materials import typical_materials
from postprocess import output_handler

feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor
nodes= preprocessor.getNodeHandler

# Problem geometry.
L0= 0.3
z= .04

x2= math.sqrt(L0**2-z**2)

# Problem type
modelSpace= predefined_spaces.SolidMechanics2D(nodes)

# Mesh
nod1= nodes.newNodeXY(0,0)
nod2= nodes.newNodeXY(0,0)

## Constraints
### Zero movement for node 1.
spc1= modelSpace.fixNode('00',nod1.tag)
### Zero x disp. for node 2.
spc2= modelSpace.fixNode('0F',nod2.tag)

### Material
E= 50000000
elast= typical_materials.defElasticMaterial(preprocessor, "elast",E)

### Element.
elements= preprocessor.getElementHandler
elements.dimElem= 2 #Bars defined in a two dimensional space.
elements.defaultMaterial= elast.name
truss= elements.newElement("CorotTruss",xc.ID([nod1.tag,nod2.tag]))
truss.sectionArea= 1

# Loads.
P= -100
## Linear time series
lts= modelSpace.newTimeSeries(name= 'lts', tsType= 'linear_ts')
## Load pattern.
lp= modelSpace.newLoadPattern(name= 'lp')
