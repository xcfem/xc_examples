# -*- coding: utf-8 -*-
'''
Example from http://feacluster.com/CalculiX/ccx_2.13/doc/ccx/node7.html#beam5
done with 2D shell elements
'''

__author__= "Bernd Hahnebach"
__copyright__= "Copyright 2015, Bernd Hahnebach"
__license__= "GPL"
__version__= "3.0"
__email__= "bernd@bimstatik.org"


import xc_base
import geom
import xc
from model import predefined_spaces
from model.mesh import finit_el_model
from materials import typical_materials
from materials.sections import section_properties
from postprocess.xcVtk import vtk_graphic_base
from postprocess import output_handler

# *********Problem definition*********
feProblem = xc.FEProblem()
preprocessor = feProblem.getPreprocessor
modelSpace = predefined_spaces.StructuralMechanics3D(preprocessor.getNodeHandler)


# *********geometry*********
L= 8.0 #8.0
inPlane= True #False
points = preprocessor.getMultiBlockTopology.getPoints  # Point container.
if(inPlane):
  pt0 = points.newPntFromPos3d(geom.Pos3d(0.0,0.0,0.0)) 
  pt1 = points.newPntFromPos3d(geom.Pos3d(0.0,1.0,0.0)) 
  pt2 = points.newPntFromPos3d(geom.Pos3d(0.0,1.0,L)) 
  pt3 = points.newPntFromPos3d(geom.Pos3d(0.0,0.0,L))  # Right end
else:
  pt0 = points.newPntFromPos3d(geom.Pos3d(0.0,0.0,0.0)) 
  pt1 = points.newPntFromPos3d(geom.Pos3d(1.0,0.0,0.0)) 
  pt2 = points.newPntFromPos3d(geom.Pos3d(1.0,0.0,L)) 
  pt3 = points.newPntFromPos3d(geom.Pos3d(0.0,0.0,L))  # Right end

surfaces = preprocessor.getMultiBlockTopology.getSurfaces  # Face container.
face0 = surfaces.newQuadSurfacePts(pt0.tag, pt1.tag, pt2.tag, pt3.tag)
#face0.setElemSizeIJ(0.5,0.25) #Element size in (pt0->pt1,pt1->pt2) directions 
face0.setElemSizeIJ(0.5,0.5) #Element size in (pt0->pt1,pt1->pt2) directions 

# Ascii art:
#
#    ^ y (inPlane==True) or x (inPlane==False)
#    |
#    |
#
#   pt1                           pt2
#    +-----------------------------+
#    |                             |
#    |                             |
#    |                             |
#    +-----------------------------+ ---> z
#   pt0                           pt3
#
# We have finished with the definition of the geometry.


# *********Material*********
width_cantilever = 1.0
E= 210000.0e6
I= 1/12.0*width_cantilever**4
canti_mat = typical_materials.defElasticMembranePlateSection(preprocessor, "canti_mat", E, 0.3, 0.0, width_cantilever)


# *********Elements: MITC9 *********
# Nine node element (quadratic interpolation):
#
#   4      7      3
#    +-----+-----+
#    |           |
#    |           |
#  8 +   9 +     + 6
#    |           |
#    |           |
#    +-----+-----+
#   1      5      2
#
seedElemHandler = preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial = "canti_mat"
elem = seedElemHandler.newElement("ShellMITC9", xc.ID([0,0,0,0,0,0,0,0,0]))


# *********Mesh*********
f1 = preprocessor.getSets.getSet(face0.name)
f1.genMesh(xc.meshDir.I)


# *********Boundary conditions*********
# Fix all the 6 displacement and rotation DOFs
# for all the nodes on the line between pt0 and pt1.
#   We ask for the line to fix:
lineToFix= preprocessor.getMultiBlockTopology.getLineWithEndPoints(pt0.tag,pt1.tag)
#   We ask for the nodes on this line
nodesToFix= lineToFix.nodes
#   We fix them
for n in nodesToFix:
    modelSpace.fixNode000_000(n.tag) # node fixed.


# *********Load*********
# Load pattern definition
lp0= modelSpace.newLoadPattern(name= '0')

# Nodes to load.
#   We ask for the line to load:
lineToLoad= preprocessor.getMultiBlockTopology.getLineWithEndPoints(pt3.tag,pt2.tag)
#   We ask for the nodes on this line
nodesToLoad= lineToLoad.nodes
P= 9e6
loadForEachNode= P/len(nodesToLoad)
#   We load them
for n in nodesToLoad:
    lp0.newNodalLoad(n.tag,xc.Vector([0.0,loadForEachNode,0.0,0.0,0.0,0.0]))

# We add the load case to domain.
modelSpace.addLoadCaseToDomain(lp0.getName())


# *********xcTotalSet*********
# Convenience set (all the nodes, all the elements, all the points,
# all the surfaces,...).
xcTotalSet = preprocessor.getSets.getSet("total")

# *********Solution*********
result= modelSpace.analyze(calculateNodalReactions= False)

f= P*L**3/3.0/E/I 

deltaYpt2 = pt2.getNode().getDisp[1]  # y displacement of node at point pt2.
deltaYpt3 = pt3.getNode().getDisp[1]  # y displacement of node at point pt3.

error= ((deltaYpt2+deltaYpt3)/2.0-f)/f
print 'deltaYpt2= ', deltaYpt2, f
print 'deltaYpt3= ', deltaYpt3, f
print 'error= ', error*100, ' %'

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

## Uncomment to display the mesh
#oh.displayFEMesh()

## Uncomment to display the vertical displacement
#oh.displayDispRot(itemToDisp='uY')

## Uncomment to display the reactions
#oh.displayReactions()

## Uncomment to display the reactions
#oh.displayIntForc('M2')

## Uncomment to display the reactions
oh.displayLoads()
