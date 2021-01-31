preprocessor= FEcase.getPreprocessor
nodes= preprocessor.getNodeHandler
elements= preprocessor.getElementHandler
points= preprocessor.getMultiBlockTopology.getPoints
lines= preprocessor.getMultiBlockTopology.getLines
surfaces= preprocessor.getMultiBlockTopology.getSurfaces
groups= preprocessor.getSets
# imported from file: ./freecad_import_test.FCStd on 2020-12-21 16:31:36.877020
pt0= points.newPntIDPos3d(0,geom.Pos3d(0.0,0.0,0.0)); pt0.setProp("labels",[u'Rectangle', u'Rectangle', u'Line'])
pt1= points.newPntIDPos3d(1,geom.Pos3d(1.0,0.0,0.0)); pt1.setProp("labels",[u'Rectangle', u'Rectangle'])
pt2= points.newPntIDPos3d(2,geom.Pos3d(1.0,1.0,0.0)); pt2.setProp("labels",[u'Rectangle', u'Rectangle'])
pt3= points.newPntIDPos3d(3,geom.Pos3d(0.0,1.0,0.0)); pt3.setProp("labels",[u'Rectangle', u'Rectangle'])
pt4= points.newPntIDPos3d(4,geom.Pos3d(-1.0,-1.0,0.0)); pt4.setProp("labels",[u'Line', u'Line', u'Line001', u'Extrude'])
pt5= points.newPntIDPos3d(5,geom.Pos3d(1.0,-1.0,0.0)); pt5.setProp("labels",[u'Line001', u'Line001', u'Extrude'])
pt6= points.newPntIDPos3d(6,geom.Pos3d(-1.0,-1.0,1.0)); pt6.setProp("labels",[u'Extrude', u'Extrude'])
pt7= points.newPntIDPos3d(7,geom.Pos3d(1.0,-1.0,1.0)); pt7.setProp("labels",[u'Extrude', u'Extrude'])
pt8= points.newPntIDPos3d(8,geom.Pos3d(1.0,-0.5,0.0)); pt8.setProp("labels",[u'Pt1', u'Pt1'])

xcPointsDict= {0:pt0,1:pt1,2:pt2,3:pt3,4:pt4,5:pt5,6:pt6,7:pt7,8:pt8}

l0= lines.newLine(4, 0); l0.setProp("labels",[u'Line']); l0.setProp("attributes",{'matId': None}); l0.setProp("thickness",0.0)
l1= lines.newLine(4, 5); l1.setProp("labels",[u'Line001']); l1.setProp("attributes",{'matId': None}); l1.setProp("thickness",0.0)
f2= surfaces.newQuadSurfacePts(0, 1, 2, 3); f2.setProp("labels",[u'Rectangle']); f2.setProp("attributes",{'matId': None}); f2.setProp("thickness",0.0)
f3= surfaces.newQuadSurfacePts(4, 6, 7, 5); f3.setProp("labels",[u'Extrude']); f3.setProp("attributes",{'matId': None}); f3.setProp("thickness",0.0)

xcBlocksDict= {0:l0,1:l1,2:f2,3:f3}

