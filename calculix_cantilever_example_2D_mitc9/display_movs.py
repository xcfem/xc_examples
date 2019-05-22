# -*- coding: utf-8 -*-

from postprocess.reports import graphical_reports as gr
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import quick_graphics as qg

execfile('./cantilever_mesh_generation.py')

#available components: 'axialComponent', 'transComponent', 'transYComponent',
#                      'transZComponent'

rlcd= gr.getRecordLoadCaseDispFromLoadPattern(lp0)
rlcd.cameraParameters= vtk_graphic_base.CameraParameters('Custom')
rlcd.cameraParameters.viewUpVc= [0,1,0]
rlcd.cameraParameters.posCVc= [-100,100,100]

loadCasesToDisplay=[rlcd]

#End data
for lc in loadCasesToDisplay:
    lc.displayDispRot(fName=None)
