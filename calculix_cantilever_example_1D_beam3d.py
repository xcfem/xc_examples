# -*- coding: utf-8 -*-
'''Example from http://feacluster.com/CalculiX/ccx_2.13/doc/ccx/node7.html#beam5'''

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
from materials.sections import section_properties
from postprocess.xcVtk import vtk_graphic_base
from postprocess import output_handler


#########################################################
# Problem definition.
feProblem= xc.FEProblem()
preprocessor= feProblem.getPreprocessor
modelSpace= predefined_spaces.StructuralMechanics3D(preprocessor.getNodeHandler)

# Problem geometry (only geometry, no mesh yet).
points= preprocessor.getMultiBlockTopology.getPoints  # Point container.
# Position of the left end of the beam:
pt0= points.newPntFromPos3d(geom.Pos3d(0.0,0.0,0.0)) 
# Position of the right end of the beam:
pt1= points.newPntFromPos3d(geom.Pos3d(0.0,0.0,8.0))  # Right end

lines= preprocessor.getMultiBlockTopology.getLines  # Line container.
ln= lines.newLine(pt0.tag,pt1.tag)  # From pt0 to pt1.

# Ascii art:
#
#    ^ y
#    |            ln
#    +-----------------------------+ ---> z
#   pt0                           pt1
#
# We have finished with the definition of the geometry.

# Material definition.
# We need a material to assign to the elements that we create
# with the mesh generation.
# Material properties
EL= typical_materials.MaterialData(name= 'EL',E=210000.0e6,nu=0.3,rho=0.0)

# Cross section properties (1x1 m square section)
crossSection= section_properties.RectangularSection("SQ_1x1",b=1.0,h=1.0)
beamSection= crossSection.defElasticShearSection3d(preprocessor,EL)


#########################################################
# Mesh generation.

# Definition of the "seed element": the element that will copied into each
# mesh cell.

# Orientation of the element axis:
lin= modelSpace.newLinearCrdTransf("lin",xc.Vector([1,0,0]))

seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultTransformation= lin.getName()  # Orientation of the element axis.
seedElemHandler.defaultMaterial= beamSection.name  # Material name.
beam3d= seedElemHandler.newElement("ElasticBeam3d",xc.ID([0,0]));

# We tell the line the size of the elements we want.
ln.setElemSize(1.0)  # 1 m so 8 elements along the line.

# Mesh generation.
ln.genMesh(xc.meshDir.I)  # Now we have a finite element mesh.


#########################################################
# Boundary conditions.
modelSpace.fixNode000_000(pt0.getNode().tag)  # Fix all the 6 DOF of the node
                                              # at pt0.


#########################################################
# Load
lp0= modelSpace.newLoadPattern(name= '0')
lp0.newNodalLoad(pt1.getNode().tag,xc.Vector([0.0,9.0e6,0.0,0.0,0.0,0.0]))
# We add the load case to domain.
modelSpace.addLoadCaseToDomain(lp0.getName())



#########################################################
# Convenience set (all the nodes, all the elements, all the points,
# all the surfaces,...).
xcTotalSet= preprocessor.getSets.getSet("total")


#########################################################
# Solution
result= modelSpace.analyze(calculateNodalReactions= False)

deltaY= pt1.getNode().getDisp[1]  # y displacement of node at point pt1.

print('deltaY= ', deltaY)
#########################################################
# Graphic stuff.
oh= output_handler.OutputHandler(modelSpace)
oh.outputStyle.cameraParameters= vtk_graphic_base.CameraParameters('Custom')
oh.outputStyle.cameraParameters.viewUpVc= [0,1,0]
oh.outputStyle.cameraParameters.posCVc= [-100,100,100]

## Uncomment to display blocks
#oh.displayBlocks()

## Uncomment to display local axes
#oh.displayLocalAxes()

## Uncomment to display strong and weak axes
#oh.displayStrongWeakAxis()

## Uncomment to display the mesh
#oh.displayFEMesh()

## Uncomment to display the vertical displacement
#oh. displayDispRot(itemToDisp='uY')

## Uncomment to display the reactions
#oh.displayReactions()

## Uncomment to display the reactions
#oh.displayIntForcDiag('Mz')

## Uncomment to display the reactions
oh.displayLoads()
