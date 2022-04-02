# -*- coding: utf-8 -*-
''' output handler setCameraParameters method test.
    Set view point using this method.'''
from __future__ import print_function

import xc_base
import geom
import xc
from model import predefined_spaces
from postprocess.xcVtk import vtk_graphic_base as gb
from postprocess import output_handler

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2014, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor
modelSpace= predefined_spaces.StructuralMechanics3D(preprocessor.getNodeHandler)

points= preprocessor.getMultiBlockTopology.getPoints
pt1= points.newPoint(geom.Pos3d(0,0,0))
pt2= points.newPoint(geom.Pos3d(5,0,0))
pt3= points.newPoint(geom.Pos3d(5,5,0))
pt4= points.newPoint(geom.Pos3d(0,5,0))

lines= preprocessor.getMultiBlockTopology.getLines
l1= lines.newLine(pt2.tag,pt3.tag)
l2= lines.newLine(pt3.tag,pt4.tag)
l3= lines.newLine(pt4.tag,pt1.tag)

oh= output_handler.OutputHandler(modelSpace)
oh.setCameraParameters(gb.CameraParameters('ZPos'))
oh.displayBlocks()


