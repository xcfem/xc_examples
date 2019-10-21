# -*- coding: utf-8 -*-
execfile('./xc_model.py')

#Graphic output
from postprocess.xcVtk import vtk_graphic_base
from postprocess.reports import graphical_reports as gr

loadCaseToDisplay= gr.getRecordLoadCaseDispFromLoadPattern(lp0)
loadCaseToDisplay.setsToDispIntForc=[xcTotalSet]
loadCaseToDisplay.unitsForc='[kN]'
loadCaseToDisplay.unitsMom='[kN.m]'
loadCaseToDisplay.cameraParameters= modelSpace.cameraParameters

 
#Define the diagram to display:
# scaleFactor, unitConversionFactor, element sets and magnitude to display.

loadCaseToDisplay.displayIntForcDiag(itemToDisp='N')
