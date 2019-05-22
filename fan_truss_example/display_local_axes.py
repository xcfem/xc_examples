# -*- coding: utf-8 -*-

execfile('./xc_model.py')
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import vtk_FE_graphic

defDisplay= vtk_FE_graphic.RecordDefDisplayEF()
defDisplay.cameraParameters= vtk_graphic_base.CameraParameters('Custom')
defDisplay.cameraParameters.viewUpVc= [0,0,1]
defDisplay.cameraParameters.posCVc= [0,-100,0]
setToDisplay= xcTotalSet #totalSet

defDisplay.displayLocalAxes(xcSet= xcTotalSet, caption= 'local axes',vectorScale=0.3)


