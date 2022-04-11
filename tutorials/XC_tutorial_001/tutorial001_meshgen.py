# -*- coding: utf-8 -*-
'''
tutorial 1 from www.xcengineering.xyz
to fit with the line numbers of the tutorial no comments are added and the file header is at file end
'''

from __future__ import print_function
from __future__ import division

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2015, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

import geom
import xc
from model import predefined_spaces
from materials import typical_materials

# Data
L = 1.0  # Bar length (m)
E = 210e9  # Elastic modulus (Pa)
alpha = 1.2e-5  # Thermal expansion coefficient of the steel
A = 4e-4  # bar area expressed in square meters
AT = 10  # Temperature increment (Celsius degrees)

# Finite element problem
feProblem = xc.FEProblem ()
preprocessor = feProblem.getPreprocessor

## Mesh
nodes = preprocessor.getNodeHandler
modelSpace = predefined_spaces.SolidMechanics2D(nodes)
nod1 = nodes.newNodeXY(0.0 ,0.0)
nod2 = nodes.newNodeXY(L ,0.0)
elast = typical_materials.defElasticMaterial(preprocessor, "elast", E)
elements = preprocessor.getElementHandler
elements.defaultMaterial = "elast"
elements.dimElem = 2  # Dimension of element space
truss = elements.newElement("Truss", xc.ID([nod1.tag, nod2.tag]))
truss.sectionArea= A

## Constraints
constraints = preprocessor.getBoundaryCondHandler
spc1 = constraints.newSPConstraint(nod1.tag, 0, 0.0)
spc2 = constraints.newSPConstraint(nod1.tag, 1, 0.0)
spc3 = constraints.newSPConstraint(nod2.tag, 0, 0.0)
spc4 = constraints.newSPConstraint(nod2.tag, 1, 0.0)

## Loads
loadHandler = preprocessor.getLoadHandler
lPatterns = loadHandler.getLoadPatterns
ts = lPatterns.newTimeSeries("linear_ts", "ts")
lPatterns.currentTimeSeries = "ts"
lp0 = lPatterns.newLoadPattern("default", "0")
eleLoad = lp0.newElementalLoad("truss_strain_load")
eleLoad.elementTags = xc.ID([truss.tag])
eleLoad.eps1 = alpha * AT
eleLoad.eps2 = alpha * AT
lPatterns.addToDomain("0")

# Solution
result= modelSpace.analyze(calculateNodalReactions= False)

# Results
elem1 = elements.getElement(truss.tag)
elem1.getResistingForce()
N = elem1.getN()
print('N= '+str(N))


