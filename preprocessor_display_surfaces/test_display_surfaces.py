# -*- coding: utf-8 -*-
''' Tiny example to show how to define two simple surfaces and display them.'''

import xc_base
import geom
import xc
import math
import os
import sys
from model import predefined_spaces
from materials import typical_materials

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2014, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

CooMaxX= 2
CooMaxY= 1
old_stderr= sys.stderr

# Problem type
feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor
nodes= preprocessor.getNodeHandler

modelSpace= predefined_spaces.SolidMechanics2D(nodes)# Model space definition

# Definition of points.
points= preprocessor.getMultiBlockTopology.getPoints
pt1= points.newPntFromPos3d(geom.Pos3d(0.0,0.0,0.0))
pt2= points.newPntFromPos3d(geom.Pos3d(CooMaxX/2,0.0,0.0))
pt3= points.newPntFromPos3d(geom.Pos3d(CooMaxX,0.0,0.0))
pt4= points.newPntFromPos3d(geom.Pos3d(0.0,CooMaxY,0.0))
pt5= points.newPntFromPos3d(geom.Pos3d(CooMaxX/2,CooMaxY,0.0))
pt6= points.newPntFromPos3d(geom.Pos3d(CooMaxX,CooMaxY,0.0))

# Definition of quadrilateral surfaces.
surfaces= preprocessor.getMultiBlockTopology.getSurfaces
s1= surfaces.newQuadSurfacePts(pt1.tag,pt2.tag,pt5.tag,pt4.tag)
s2= surfaces.newQuadSurfacePts(pt2.tag,pt3.tag,pt6.tag,pt5.tag)


# Display surfaces.
from postprocess.xcVtk.CAD_model import vtk_CAD_graphic
defDisplay= vtk_CAD_graphic.RecordDefDisplayCAD()
setDisp= feProblem.getPreprocessor.getSets['total']
defDisplay.displayBlocks(setDisp,caption= setDisp.name+' set')
