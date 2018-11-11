execfile('./cantilever_mesh_generation.py')
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.CAD_model import vtk_CAD_graphic

defDisplay= vtk_CAD_graphic.RecordDefDisplayCAD()
defDisplay.cameraParameters= vtk_graphic_base.CameraParameters('Custom')
defDisplay.cameraParameters.viewUpVc= [0,1,0]
defDisplay.cameraParameters.posCVc= [-100,100,100]
setDisp= xcTotalSet
defDisplay.displayBlocks(setDisp,caption= setDisp.name+' set')
