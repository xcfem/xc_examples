execfile('./cantilever_mesh_generation.py')

#Graphic output
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import vtk_FE_graphic
from postprocess.xcVtk import vtk_internal_force_diagram as gde
from postprocess.reports import graphical_reports as gr
from postprocess.xcVtk.FE_model import quick_graphics as qg



loadCaseToDisplay= gr.getRecordLoadCaseDispFromLoadPattern(lp0)
loadCaseToDisplay.setsToDispIntForc=[xcTotalSet]
loadCaseToDisplay.unitsForc='[kN]'
loadCaseToDisplay.unitsMom='[kN.m]'
loadCaseToDisplay.cameraParameters= modelSpace.cameraParameters

lcs= qg.LoadCaseResults(feProblem,loadCaseName=loadCaseToDisplay.loadCaseName,loadCaseExpr=loadCaseToDisplay.loadCaseExpr)
 
#Define the diagram to display:
# scaleFactor, unitConversionFactor, element sets and magnitude to display.
lcs.solve()

loadCaseToDisplay.displayIntForcDiag('Mz')

