# -*- coding: utf-8 -*-
'''
Simple continuous beam analysis.
'''

from __future__ import division
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AO_O)"
__copyright__= "Copyright 2021, LCPT and AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es ana.ortega@ciccp.es"

import math
import xc_base
import geom
import xc
from solution import predefined_solutions
from model import predefined_spaces
from materials import typical_materials

feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor   
nodes= preprocessor.getNodeHandler
# Problem type
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)

# Geometry
spans= [3.0,3.0,3.0]

# Materials.
b= 1.0 # section width.
h= 0.15 # section depth.
E= 2.0e10 # Young modulus.

A= b*h # Beam cross-section area.
I= 1/12.0*b*h**3 # Inertia of the beam section.
sry= 5/5.0 # Shear coefficient.
Ay= A/sry
nu= 0.3 # Poisson's ratio.
G= E/(2.0*(1+nu))
scc= typical_materials.defElasticShearSection2d(preprocessor, "scc",A,E,G,I,alpha= Ay/A)


# Loads
vLoad= 10e3+3.75e3 # vertical load

points= preprocessor.getMultiBlockTopology.getPoints
lines= preprocessor.getMultiBlockTopology.getLines
x= 0
pt0= points.newPoint(geom.Pos3d(x,0,0))
beamPoints= []
beamLines= []
beamPoints.append(pt0)
for i, sp in enumerate(spans):
    x+= sp
    pt1= points.newPoint(geom.Pos3d(x,0,0))
    l= lines.newLine(pt0.tag,pt1.tag)
    l.nDiv= 8
    beamLines.append(l)
    beamPoints.append(pt1)
    pt0= pt1

# Mesh generation

## Geometric transformations
lin= modelSpace.newLinearCrdTransf("lin")

## Seed element
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.dimElem= 2 # Bars defined in a two-dimensional space.
seedElemHandler.defaultMaterial= scc.name
seedElemHandler.defaultTransformation= lin.name
beam2d= seedElemHandler.newElement("ElasticBeam2d",xc.ID([0,0]))
beam2d.h= h

xcTotalSet= preprocessor.getSets.getSet("total")
xcTotalSet.genMesh(xc.meshDir.I)

# Constraints
constraints= preprocessor.getBoundaryCondHandler
for p in beamPoints:
    n= p.getNode()
    spc= constraints.newSPConstraint(n.tag,0,0.0) # Node A
    spc= constraints.newSPConstraint(n.tag,1,0.0)
    
# Load definition.
lp0= modelSpace.newLoadPattern(name= '0')

eleLoad= lp0.newElementalLoad("beam2d_uniform_load")
eleLoad.elementTags= xc.ID(xcTotalSet.getElementTags())
eleLoad.transComponent= -vLoad
# We add the load case to domain.
modelSpace.addLoadCaseToDomain(lp0.name)

# Solution
analysis= predefined_solutions.simple_static_linear(feProblem)
result= analysis.analyze(1)

#########################################################
# Graphic stuff.
from postprocess import output_handler
oh= output_handler.OutputHandler(modelSpace)

# oh.displayBlocks()
# oh.displayFEMesh()
# oh.displayLocalAxes()
oh.displayLoads()
oh.displayDispRot('uY', defFScale= 100.0)
oh.displayIntForcDiag(itemToDisp= 'Mz')
oh.displayIntForcDiag(itemToDisp= 'Qy')
oh.displayReactions()
