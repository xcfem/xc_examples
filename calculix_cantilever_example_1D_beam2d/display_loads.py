# -*- coding: utf-8 -*-

from postprocess.reports import graphical_reports as gr

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
