# -*- coding: utf-8 -*-

execfile('./cantilever_mesh_generation.py')
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import vtk_FE_graphic


defDisplay= vtk_FE_graphic.RecordDefDisplayEF()
defDisplay.cameraParameters= vtk_graphic_base.CameraParameters('Custom')
defDisplay.cameraParameters.viewUpVc= [0,1,0]
defDisplay.cameraParameters.posCVc= [-100,100,100]
setToDisplay= xcTotalSet

defDisplay.displayStrongWeakAxis(xcSet= setToDisplay,caption= setToDisplay.name + ' set, strong and weak axis')

