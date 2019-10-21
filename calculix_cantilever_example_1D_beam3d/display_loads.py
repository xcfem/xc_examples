# -*- coding: utf-8 -*-

from postprocess.reports import graphical_reports as gr
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import quick_graphics as qg

execfile('./cantilever_mesh_generation.py')

#available components: 'axialComponent', 'transComponent', 'transYComponent',
#                      'transZComponent'

rlcd= gr.getRecordLoadCaseDispFromLoadPattern(lp0)
rlcd.cameraParameters= modelSpace.cameraParameters
rlcd.setsToDispLoads=[xcTotalSet]
rlcd.setsToDispBeamLoads=[xcTotalSet]

loadCasesToDisplay=[rlcd]

#End data

for lc in loadCasesToDisplay:
    lc.displayLoadOnSets()
