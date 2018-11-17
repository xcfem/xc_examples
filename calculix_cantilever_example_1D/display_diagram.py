execfile('./cantilever_mesh_generation.py')

#Graphic output
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import vtk_FE_graphic
from postprocess.xcVtk import vtk_internal_force_diagram as gde
from postprocess.reports import graphical_reports as gr
from postprocess.xcVtk.FE_model import quick_graphics as qg

lcs= qg.QuickGraphics(feProblem)

loadCaseToDisplay= gr.getRecordLoadCaseDispFromLoadPattern(lp0)
loadCaseToDisplay.cameraParameters= vtk_graphic_base.CameraParameters('Custom')
loadCaseToDisplay.cameraParameters.viewUpVc= [0,1,0]
loadCaseToDisplay.cameraParameters.posCVc= [-100,100,100]

 
#Define the diagram to display:
# scaleFactor, unitConversionFactor, element sets and magnitude to display.
lcs.solve(loadCaseName=loadCaseToDisplay.loadCaseName,loadCaseExpr=loadCaseToDisplay.loadCaseExpr)

#lcs.displayIntForcDiag('N',xcTotalSet,1e-3,1,'(kN)',loadCaseToDisplay.cameraParameters)
lcs.displayIntForcDiag('Mz',xcTotalSet,1e-3,-1.0,'(kN m)',loadCaseToDisplay.cameraParameters)
#lcs.displayIntForcDiag('Qy',xcTotalSet,1e-3,1,'(kN)',loadCaseToDisplay.cameraParameters)
