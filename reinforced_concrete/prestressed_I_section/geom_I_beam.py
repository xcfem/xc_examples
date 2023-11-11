## -*- coding: utf-8 -*-
import math
import geom
from materials.ehe import EHE_materials




def gmSecHP_viga_jabali(preprocessor, nmbGeomSecc,concrDiagName,reinfSteelDiagramName,prestressingSteelDiagramName,concreteLstWidthHeight,activeReinLayers,passiveReinLayers,zStart):
    # Concrete
    # Hbeam=0
    # for wh in concreteLstWidthHeight:
    #     Hbeam+=wh[1]
    # zStart=-Hbeam/2
    geomSecc= preprocessor.getMaterialHandler.newSectionGeometry(nmbGeomSecc)
    regions= geomSecc.getRegions
    startW=concreteLstWidthHeight[0][0] #start width
    for wh in concreteLstWidthHeight[1:]:
        endW=wh[0]
        horm= regions.newQuadRegion(concrDiagName)
        horm.nDivIJ= 50
        horm.nDivJK= 50
        pt1= geom.Pos2d(-startW/2,zStart)
        pt2= geom.Pos2d(+startW/2,zStart)
        zStart=zStart+wh[1]
        pt3= geom.Pos2d(+endW/2,zStart)
        pt4= geom.Pos2d(-endW/2,zStart)
        horm.setQuad(geom.Quadrilateral2d(pt1,pt2,pt3,pt4))
        startW=endW

    # Reinforcement layers
    ## Active reinforcement
    reinforcement= geomSecc.getReinfLayers
    for arl in activeReinLayers.keys():
        rebarLayer= reinforcement.newStraightReinfLayer(prestressingSteelDiagramName)
        rebarLayer.barArea=math.pi*activeReinLayers[arl]['fi']**2/4.
        rebarLayer.numReinfBars=activeReinLayers[arl]['nBars']
        rebarLayer.p1=activeReinLayers[arl]['p1']
        rebarLayer.p2=activeReinLayers[arl]['p2']
    for prl in passiveReinLayers.keys():
        rebarLayer= reinforcement.newStraightReinfLayer(reinfSteelDiagramName)
        rebarLayer.barArea=math.pi*passiveReinLayers[prl]['fi']**2/4.
        rebarLayer.numReinfBars=passiveReinLayers[prl]['nBars']
        rebarLayer.p1=passiveReinLayers[prl]['p1']
        rebarLayer.p2=passiveReinLayers[prl]['p2']

    return geomSecc
