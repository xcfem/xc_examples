# -*- coding: utf-8 -*-

from postprocess.reports import graphical_reports as gr
from postprocess.xcVtk import vtk_graphic_base

execfile('./xc_model.py')

#available components: 'axialComponent', 'transComponent', 'transYComponent',
#                      'transZComponent'

rlcd= gr.getRecordLoadCaseDispFromLoadPattern(lp0)
rlcd.cameraParameters= vtk_graphic_base.CameraParameters('Custom')
rlcd.cameraParameters.viewUpVc= [0,0,1]
rlcd.cameraParameters.posCVc= [0,-100,0]
rlcd.setsToDispLoads=[xcTotalSet]
rlcd.setsToDispBeamLoads=[xcTotalSet]

loadCasesToDisplay=[rlcd]

#End data

for lc in loadCasesToDisplay:
    lc.displayLoadOnSets()
