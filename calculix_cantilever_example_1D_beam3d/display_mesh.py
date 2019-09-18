# -*- coding: utf-8 -*-

execfile('./cantilever_mesh_generation.py')
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import vtk_FE_graphic


defDisplay= vtk_FE_graphic.RecordDefDisplayEF()
cameraParams= vtk_graphic_base.CameraParameters('Custom')
cameraParams.viewUpVc= [0,1,0]
cameraParams.posCVc= [-100,100,100]
setToDisplay= xcTotalSet #impactOnBody #totalSet

defDisplay.FEmeshGraphic(xcSet= setToDisplay,caption=setToDisplay.name+' set; mesh',cameraParameters= cameraParams)

