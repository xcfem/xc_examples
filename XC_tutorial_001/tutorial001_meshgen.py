# -*- coding: utf-8 -*-
'''
tutorial 1 from www.xcengineering.xyz
to fit with the line numbers of the tutorial no comments are added and the file header is at file end
'''

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2015, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

import xc_base
import geom
import xc
from model import predefined_spaces
from materials import typical_materials
from solution import predefined_solutions
L = 1.0  # Bar length (m)
E = 210e9  # Elastic modulus (Pa)
alpha = 1.2e-5  # Thermal expansion coefficient of the steel
A = 4e-4  # bar area expressed in square meters
AT = 10  # Temperature increment (Celsius degrees)
feProblem = xc.FEProblem ()
preprocessor = feProblem.getPreprocessor
nodes = preprocessor.getNodeHandler
modelSpace = predefined_spaces.SolidMechanics2D(nodes)
nod1 = nodes.newNodeXY(0.0 ,0.0)
nod2 = nodes.newNodeXY(L ,0.0)
elast = typical_materials.defElasticMaterial(preprocessor, "elast", E)
elements = preprocessor.getElementHandler
elements.defaultMaterial = "elast"
elements.dimElem = 2  # Dimension of element space
elements.defaultTag = 1  # Tag for the next element.
truss = elements.newElement("Truss", xc.ID([nod1.tag, nod2.tag]))
truss.area = A
constraints = preprocessor.getBoundaryCondHandler
spc1 = constraints.newSPConstraint(nod1.tag, 0, 0.0)
spc2 = constraints.newSPConstraint(nod1.tag, 1, 0.0)
spc3 = constraints.newSPConstraint(nod2.tag, 0, 0.0)
spc4 = constraints.newSPConstraint(nod2.tag, 1, 0.0)
loadHandler = preprocessor.getLoadHandler
lPatterns = loadHandler.getLoadPatterns
ts = lPatterns.newTimeSeries("linear_ts", "ts")
lPatterns.currentTimeSeries = "ts"
lp0 = lPatterns.newLoadPattern("default", "0")
eleLoad = lp0.newElementalLoad("truss_temp_load")
eleLoad.elementTags = xc.ID([1])
eleLoad.eps1 = alpha * AT
eleLoad.eps2 = alpha * AT
lPatterns.addToDomain("0")
analisis = predefined_solutions.simple_static_linear(feProblem)
result = analisis.analyze(1)
elem1 = elements.getElement(1)
elem1.getResistingForce()
N = elem1.getN()
print('N = ', N)


