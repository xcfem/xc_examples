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
rlcd.setsToDispLoads=[xcTotalSet]
rlcd.setsToDispBeamLoads=[xcTotalSet]

loadCasesToDisplay=[rlcd]

#End data

lcs=qg.LoadCaseResults(feProblem=feProblem,loadCaseName='lp0',loadCaseExpr='1.2*lp0')
lcs.solve()
lcs.displayReactions(setToDisplay=xcTotalSet,fConvUnits=1.0,scaleFactor=1.0,unitDescription= '[m,kN]',viewDef= rlcd.cameraParameters,fileName=None,defFScale=0.0)
