# -*- coding: utf-8 -*-
'''Define reinforcement.'''

# Reinforcement row scheme:
#
#    ----------------------------------------------------   ^
#    |                                                  |   | cover
#    |  o    o    o    o    o    o    o    o    o    o  |   v
#    <->           <-->                               <-> 
#    lateral      spacing                           lateral
#     cover                                          cover
#

# Geometry of the reinforcement.

## Bridge deck reinforcement.
### Transverse top reinforcement.
cover= 40e-3 # Concrete cover
bridgeDeckTransverseTopReinf= def_simple_RC_section.ReinfRow(rebarsDiam= 16e-3, rebarsSpacing= 0.1, width= 1.0, nominalCover= cover+8e-3, nominalLatCover= 0.0)

### Longitudinal top reinforcement.
cover+= bridgeDeckTransverseTopReinf.rebarsDiam
bridgeDeckLongitudinalTopReinf= def_simple_RC_section.ReinfRow(rebarsDiam= 12e-3, rebarsSpacing= 0.2, width= 1.0, nominalCover= cover+6e-3, nominalLatCover= 0.0)
### Transverse bottom reinforcement.
cover= 65e-3 # Concrete cover (thickness of shuttering slab: 65 mm).
bridgeDeckTransverseBottomReinf= def_simple_RC_section.ReinfRow(rebarsDiam= 12e-3, rebarsSpacing= 0.1, width= 1.0, nominalCover= cover+6e-3, nominalLatCover= 0.0)
### Longitudinal bottom reinforcement.
cover+= bridgeDeckTransverseBottomReinf.rebarsDiam
bridgeDeckLongitudinalBottomReinf= def_simple_RC_section.ReinfRow(rebarsDiam= 10e-3, rebarsSpacing= 0.2, width= 1.0, nominalCover= cover+5e-3, nominalLatCover= 0.0)

### Reinforcement on edges.
bridgeDeckEdgeTransverseReinf= def_simple_RC_section.ReinfRow(rebarsDiam= 20e-3, rebarsSpacing= 0.1, width= 1.0, nominalCover= cover+10e-3, nominalLatCover= 0.0)
bridgeDeckEdgeLongitudinalReinf= def_simple_RC_section.ReinfRow(rebarsDiam= 8e-3, rebarsSpacing= 0.2, width= 1.0, nominalCover= cover+4e-3, nominalLatCover= 0.1)
bridgeDeckEdgeShearReinf= def_simple_RC_section.ShearReinforcement(familyName= "shearReinf", nShReinfBranches= 2, areaShReinfBranch= EHE_materials.Fi8, shReinfSpacing= 0.2, angAlphaShReinf= math.pi/2.0)

## Precast beams reinforcement.
### Bottom flange reinforcement.
#### Bottom flange transverse top reinforcement in zone A (11A).
cover= 30e-3
bottomFlangeTransverseTopReinfA= def_simple_RC_section.ReinfRow(rebarsDiam= 12e-3, rebarsSpacing= 0.1, width= 1.0, nominalCover= cover+6e-3, nominalLatCover= 0.0)
#### Bottom flange transverse top reinforcement in zone B (11B).
bottomFlangeTransverseTopReinfB= def_simple_RC_section.ReinfRow(rebarsDiam= 12e-3, rebarsSpacing= 0.1, width= 1.0, nominalCover= cover+5e-3, nominalLatCover= 0.0)
#### Bottom flange transverse top reinforcement in zone C (11C).
bottomFlangeTransverseTopReinfC= def_simple_RC_section.ReinfRow(rebarsDiam= 12e-3, rebarsSpacing= 0.1, width= 1.0, nominalCover= cover+6e-3, nominalLatCover= 0.0)
#### Bottom flange transverse top reinforcement in zone D (11D).
bottomFlangeTransverseTopReinfD= def_simple_RC_section.ReinfRow(rebarsDiam= 12e-3, rebarsSpacing= 0.1, width= 1.0, nominalCover= cover+5e-3, nominalLatCover= 0.0)

#### Bottom flange longitudinal top reinforcement (12a 4fi32/2).
cover+= bottomFlangeTransverseTopReinfA.rebarsDiam
bottomFlangeLongitudinalTopReinf= def_simple_RC_section.ReinfRow(rebarsDiam= 25e-3, rebarsSpacing= 0.2, width= 1.0, nominalCover= cover+12.5e-3, nominalLatCover= 0.0)

#### Bottom flange transverse bottom reinforcement in zone A (2A).
cover= 30e-3
bottomFlangeTransverseBottomReinfA= def_simple_RC_section.ReinfRow(rebarsDiam= 12e-3, rebarsSpacing= 0.1, width= 1.0, nominalCover= cover+6e-3, nominalLatCover= 0.0)
#### Bottom flange transverse bottom reinforcement in zone B (2B).
bottomFlangeTransverseBottomReinfB= def_simple_RC_section.ReinfRow(rebarsDiam= 12e-3, rebarsSpacing= 0.1, width= 1.0, nominalCover= cover+5e-3, nominalLatCover= 0.0)
#### Bottom flange transverse bottom reinforcement in zone C (2C).
bottomFlangeTransverseBottomReinfC= def_simple_RC_section.ReinfRow(rebarsDiam= 12e-3, rebarsSpacing= 0.1, width= 1.0, nominalCover= cover+6e-3, nominalLatCover= 0.0)
#### Bottom flange transverse bottom reinforcement in zone D (2D).
bottomFlangeTransverseBottomReinfD= def_simple_RC_section.ReinfRow(rebarsDiam= 12e-3, rebarsSpacing= 0.1, width= 1.0, nominalCover= cover+5e-3, nominalLatCover= 0.0)

#### Bottom flange longitudinal bottom reinforcement (12b Virtual 4fi32/2).
cover+= bottomFlangeTransverseBottomReinfA.rebarsDiam
bottomFlangeLongitudinalBottomReinf= def_simple_RC_section.ReinfRow(rebarsDiam= 25e-3, rebarsSpacing= 0.2, width= 1.0, nominalCover= cover+12.5e-3, nominalLatCover= 0.0)

### Web reinforcement.
webLowerEdge1= geom.Segment3d(geom.Pos3d(-2.7162302204840053, 8.526485292746998, -1.2500), geom.Pos3d(22.043769779515995, 8.526485292746993, -1.2500000000000018))
webLowerEdge2= geom.Segment3d(geom.Pos3d(-2.189653500592005, 6.873514707339, -1.2500), geom.Pos3d(22.570346499407977, 6.873514707338985, -1.2499999999999982))
webLowerEdge3= geom.Segment3d(geom.Pos3d(-1.3782619328970031, 4.326485292657, -1.2499999999999998), geom.Pos3d(23.38173806710296, 4.326485292656967, -1.2499999999999961))
webLowerEdge4= geom.Segment3d(geom.Pos3d(-0.8516852130050028, 2.673514707249, -1.2499999999999998), geom.Pos3d(23.90831478699495, 2.6735147072489563, -1.249999999999998))

#### Web transverse (vertical) exterior reinforcement in zone A (2A).
cover= 30e-3
webTransverseExteriorReinfA= def_simple_RC_section.ReinfRow(rebarsDiam= 16e-3, rebarsSpacing= 0.1, width= 1.0, nominalCover= cover+8e-3, nominalLatCover= 0.0)

#### Web longitudinal (horizontal) exterior reinforcement
cover+= webTransverseExteriorReinfA.rebarsDiam
webLongitudinalExteriorReinf= def_simple_RC_section.ReinfRow(rebarsDiam= 10e-3, rebarsSpacing= 0.2, width= 1.0, nominalCover= cover+5e-3, nominalLatCover= 0.0)

#### Web transverse (vertical) exterior reinforcement in zone B (2B).
cover= 30e-3
webTransverseExteriorReinfB= def_simple_RC_section.ReinfRow(rebarsDiam= 12e-3, rebarsSpacing= 0.1, width= 1.0, nominalCover= cover+6e-3, nominalLatCover= 0.0)
#### Web transverse (vertical) exterior reinforcement in zone C (2C).
webTransverseExteriorReinfC= def_simple_RC_section.ReinfRow(rebarsDiam= 12e-3, rebarsSpacing= 0.1, width= 1.0, nominalCover= cover+6e-3, nominalLatCover= 0.0)
#### Web transverse (vertical) exterior reinforcement in zone D (2D).
webTransverseExteriorReinfD= def_simple_RC_section.ReinfRow(rebarsDiam= 12e-3, rebarsSpacing= 0.1, width= 1.0, nominalCover= cover+6e-3, nominalLatCover= 0.0)

#### Web transverse (vertical) interior reinforcement in zone A (1A).
cover= 30e-3
webTransverseInteriorReinfA= def_simple_RC_section.ReinfRow(rebarsDiam= 16e-3, rebarsSpacing= 0.1, width= 1.0, nominalCover= cover+8e-3, nominalLatCover= 0.0)

#### Web longitudinal (horizontal) interior reinforcement
cover+= webTransverseInteriorReinfA.rebarsDiam
webLongitudinalInteriorReinf= def_simple_RC_section.ReinfRow(rebarsDiam= 10e-3, rebarsSpacing= 0.2, width= 1.0, nominalCover= cover+5e-3, nominalLatCover= 0.0)

#### Web longitudinal lower edge reinforcement
webLowerEdgeReinf= def_simple_RC_section.ReinfRow(rebarsDiam= 25e-3, rebarsSpacing= 0.2, width= 1.0, nominalCover= .05, nominalLatCover= 0.05)

#### Web transverse (vertical) interior reinforcement in zone B (1B).
cover= 30e-3
webTransverseInteriorReinfB= def_simple_RC_section.ReinfRow(rebarsDiam= 12e-3, rebarsSpacing= 0.1, width= 1.0, nominalCover= cover+6e-3, nominalLatCover= 0.0)
#### Web transverse (vertical) interior reinforcement in zone C (1C).
webTransverseInteriorReinfC= def_simple_RC_section.ReinfRow(rebarsDiam= 12e-3, rebarsSpacing= 0.1, width= 1.0, nominalCover= cover+6e-3, nominalLatCover= 0.0)
#### Web transverse (vertical) interior reinforcement in zone D (1D).
webTransverseInteriorReinfD= def_simple_RC_section.ReinfRow(rebarsDiam= 10e-3, rebarsSpacing= 0.1, width= 1.0, nominalCover= cover+6e-3, nominalLatCover= 0.0)

### Diaphragms reinforcement.
skewVector= geom.Vector3d(-0.3040165214044994, 0.9526667595298514, 0.0)
skewNormalVector=  geom.Vector3d(-skewVector.y, skewVector.x, 0.0)

#### Diaphragm transverse (vertical) exterior reinforcement
cover= 30e-3
diaphragmTransverseExteriorReinf= def_simple_RC_section.ReinfRow(rebarsDiam= 20e-3, rebarsSpacing= 0.15, width= 1.0, nominalCover= cover+5e-3, nominalLatCover= 0.0)

#### Diaphragm longitudinal (horizontal) exterior reinforcement
cover+= diaphragmTransverseExteriorReinf.rebarsDiam
diaphragmLongitudinalExteriorReinf= def_simple_RC_section.ReinfRow(rebarsDiam= 20e-3, rebarsSpacing= 0.15, width= 1.0, nominalCover= cover+4e-3, nominalLatCover= 0.0)

#### Diaphragm transverse (vertical) interior reinforcement
cover= 30e-3
diaphragmTransverseInteriorReinf= def_simple_RC_section.ReinfRow(rebarsDiam= 20e-3, rebarsSpacing= 0.15, width= 1.0, nominalCover= cover+5e-3, nominalLatCover= 0.0)

#### Diaphragm longitudinal (horizontal) interior reinforcement
cover+= diaphragmTransverseInteriorReinf.rebarsDiam
diaphragmLongitudinalInteriorReinf= def_simple_RC_section.ReinfRow(rebarsDiam= 20e-3, rebarsSpacing= 0.15, width= 1.0, nominalCover= cover+4e-3, nominalLatCover= 0.0)

## Store element reinforcement information.
### Bridge deck edges.
edge01= geom.Polygon2d([geom.Pos2d(-3573.9689840088486e-3, 11201.023341485536e-3), geom.Pos2d(0.19395142815073996e-3, 1.019453525535937e-3), geom.Pos2d(1000.1939514281512e-3, 1.019453525535937e-3), geom.Pos2d(-2573.9689840088486e-3, 11201.023341485536e-3)])
edge02= geom.Polygon2d([geom.Pos2d(20272.118314563e-3, 11201.023341485543e-3), geom.Pos2d(23846.281249999996e-3, 1.019453525543213e-3), geom.Pos2d(24846.28125e-3, 1.019453525543213e-3), geom.Pos2d(21272.118314563e-3, 11201.023341485543e-3)])

### Bridge deck.
for setName in bridgeDeckSetsNames:
    xcSet= modelSpace.getSet(setName)
    sectionName= xcSet.getProp('sectionName')
    rcSection= rcSectionDict[sectionName]
    baseSection= rcSection.getTemplateSection(posReb= None,negReb= None,YShReinf= None, ZShReinf= None)
    baseSection.name= setName+'Section'
    for e in xcSet.elements:
        e.setProp("baseSection", baseSection)
        e.setProp("reinforcementUpVector", geom.Vector3d(0,0,1)) # Z+
        e.setProp("reinforcementIVector", geom.Vector3d(1,0,0)) # X+
        elementCenter= e.getPosCentroid(True)
        ePos2d= geom.Pos2d(elementCenter.x, elementCenter.y)            
        bottomReinforcementI= [bridgeDeckLongitudinalBottomReinf]
        topReinforcementI= [bridgeDeckLongitudinalTopReinf]
        bottomReinforcementII= [bridgeDeckTransverseBottomReinf]
        topReinforcementII= [bridgeDeckTransverseTopReinf]
        shearReinforcementI= None
        shearReinforcementII= None
        if(edge01.In(ePos2d,.05) or edge02.In(ePos2d,.05)):
            bottomReinforcementI.append(bridgeDeckEdgeLongitudinalReinf)
            topReinforcementI.append(bridgeDeckEdgeLongitudinalReinf)
            bottomReinforcementII= [bridgeDeckEdgeTransverseReinf]
            topReinforcementII= [bridgeDeckTransverseTopReinf]
            shearReinforcementI= bridgeDeckEdgeShearReinf
            shearReinforcementII= bridgeDeckEdgeShearReinf
        e.setProp("bottomReinforcementI", def_simple_RC_section.LongReinfLayers(bottomReinforcementI))
        e.setProp("topReinforcementI", def_simple_RC_section.LongReinfLayers(topReinforcementI))
        e.setProp("bottomReinforcementII", def_simple_RC_section.LongReinfLayers(bottomReinforcementII))
        e.setProp("topReinforcementII", def_simple_RC_section.LongReinfLayers(topReinforcementII))
        if(shearReinforcementI):
            e.setProp('shearReinforcementI',shearReinforcementI)
        if(shearReinforcementII):
            e.setProp('shearReinforcementII', shearReinforcementII)        

### Bridge girders.
#### Diaphragms.
diaphragmSet= modelSpace.getSet('Diaphragms')
sectionName= diaphragmSet.getProp('sectionName')
rcSection= rcSectionDict[sectionName]
baseSection= rcSection.getTemplateSection(posReb= None,negReb= None,YShReinf= None, ZShReinf= None)
baseSection.name= diaphragmSet.name+'Section'
for e in diaphragmSet.elements:
    e.setProp("baseSection", baseSection)
    e.setProp("reinforcementUpVector", skewNormalVector) # ~X-
    e.setProp("reinforcementIVector", skewVector) # ~Y+
    e.setProp("bottomReinforcementI", def_simple_RC_section.LongReinfLayers([diaphragmLongitudinalInteriorReinf]))
    e.setProp("topReinforcementI", def_simple_RC_section.LongReinfLayers([diaphragmLongitudinalExteriorReinf]))
    e.setProp("bottomReinforcementII", def_simple_RC_section.LongReinfLayers([diaphragmTransverseInteriorReinf]))
    e.setProp("topReinforcementII", def_simple_RC_section.LongReinfLayers([diaphragmTransverseExteriorReinf]))

#### Webs.
##### Web reinforcement zones.
zoneA1= geom.Polygon2d([geom.Pos2d(-852.1007005584597e-3, 11201.023341485536e-3), geom.Pos2d(-3573.9689840088486e-3, 11201.023341485536e-3), geom.Pos2d(0.1939514281511947e-3, 1.019453525535937e-3), geom.Pos2d(2722.06223487854e-3, 1.019453525534118e-3)])
zoneA2= geom.Polygon2d([geom.Pos2d(21278.248046875e-3, 11200.9248046875e-3), geom.Pos2d(18493.986650336545e-3, 11201.023341485536e-3), geom.Pos2d(22068.149585773543e-3, 1.019453525535937e-3), geom.Pos2d(24846.28125e-3, 1.019453525543213e-3)])

zoneB1= geom.Polygon2d([geom.Pos2d(2647.8992994415403e-3, 11201.023341485534e-3), geom.Pos2d(-852.1007005584597e-3, 11201.023341485536e-3), geom.Pos2d(2722.06223487854e-3, 1.019453525534118e-3), geom.Pos2d(6222.06223487854e-3, 1.019453525534118e-3)])
zoneB2= geom.Polygon2d([geom.Pos2d(18493.98665033654e-3, 11201.023341485534e-3), geom.Pos2d(14993.986650336541e-3, 11201.023341485536e-3), geom.Pos2d(18568.149585773543e-3, 1.019453525534118e-3), geom.Pos2d(22068.149585773543e-3, 1.019453525534118e-3)])

zoneC1= geom.Polygon2d([geom.Pos2d(5147.8994140625e-3, 11201.0234375e-3), geom.Pos2d(2647.8992994415403e-3, 11201.023341485534e-3), geom.Pos2d(6222.06223487854e-3, 1.019453525534118e-3), geom.Pos2d(8722.06223487854e-3, 1.019453525534118e-3)])
zoneC2= geom.Polygon2d([geom.Pos2d(14993.986764957503e-3, 11201.0234375e-3), geom.Pos2d(12493.986650336543e-3, 11201.023341485534e-3), geom.Pos2d(16068.149585773543e-3, 1.019453525534118e-3), geom.Pos2d(18568.149585773543e-3, 1.019453525534118e-3)])
                        
zoneD= geom.Polygon2d([geom.Pos2d(12493.986650336543e-3, 11201.023341485536e-3), geom.Pos2d(5147.89929944154e-3, 11201.023341485534e-3), geom.Pos2d(8722.06223487854e-3, 1.019453525534118e-3), geom.Pos2d(16068.149585773543e-3, 1.019453525535937e-3)])

websLowerEdge= modelSpace.defSet('websLowerEdge')


for setName in ['GirderWebs', 'GirderTops']:
    xcSet= modelSpace.getSet(setName)
    sectionName= xcSet.getProp('sectionName')
    rcSection= rcSectionDict[sectionName]
    baseSection= rcSection.getTemplateSection(posReb= None,negReb= None,YShReinf= None, ZShReinf= None)
    baseSection.name= setName+'Section'
    for e in xcSet.elements:
        e.setProp("baseSection", baseSection)
        e.setProp("reinforcementUpVector", geom.Vector3d(0,1,0)) # Y+
        e.setProp("reinforcementIVector", geom.Vector3d(1,0,0)) # X+
        # Longitudinal reinforcement.
        elementCenter= e.getPosCentroid(True)
        distLowerEdge= min(webLowerEdge1.dist(elementCenter), webLowerEdge2.dist(elementCenter), webLowerEdge3.dist(elementCenter), webLowerEdge4.dist(elementCenter))
        if(distLowerEdge<0.25):
            e.setProp("bottomReinforcementI", def_simple_RC_section.LongReinfLayers([webLowerEdgeReinf]))
            e.setProp("topReinforcementI", def_simple_RC_section.LongReinfLayers([webLowerEdgeReinf]))
            websLowerEdge.elements.append(e)
        else:
            e.setProp("bottomReinforcementI", def_simple_RC_section.LongReinfLayers([webLongitudinalInteriorReinf]))
            e.setProp("topReinforcementI", def_simple_RC_section.LongReinfLayers([webLongitudinalExteriorReinf]))
            
        # Transverse reinforcement.
        ePos2d= geom.Pos2d(elementCenter.x, elementCenter.y)
        elementZone= 'D'
        webTransverseExteriorReinf= webTransverseExteriorReinfD
        webTransverseInteriorReinf= webTransverseInteriorReinfD
        if(zoneA1.In(ePos2d,.05) or zoneA2.In(ePos2d,.05)):
            elementZone= 'A'
            webTransverseExteriorReinf= webTransverseExteriorReinfA
            webTransverseInteriorReinf= webTransverseInteriorReinfA
        elif(zoneB1.In(ePos2d,.05) or zoneB2.In(ePos2d,.05)):
            elementZone= 'B'
            webTransverseExteriorReinf= webTransverseExteriorReinfB
            webTransverseInteriorReinf= webTransverseInteriorReinfB
        elif(zoneC1.In(ePos2d,.05) or zoneC2.In(ePos2d,.05)):
            elementZone= 'C'
            webTransverseExteriorReinf= webTransverseExteriorReinfC
            webTransverseInteriorReinf= webTransverseInteriorReinfC
        e.setProp("bottomReinforcementII", def_simple_RC_section.LongReinfLayers([webTransverseInteriorReinf]))
        e.setProp("topReinforcementII", def_simple_RC_section.LongReinfLayers([webTransverseExteriorReinf]))
        
#### Bottom flange.
for setName in ['TapperedBottoms', 'BottomFlanges']:
    xcSet= modelSpace.getSet(setName)
    sectionName= xcSet.getProp('sectionName')
    rcSection= rcSectionDict[sectionName]
    baseSection= rcSection.getTemplateSection(posReb= None,negReb= None,YShReinf= None, ZShReinf= None)
    baseSection.name= setName+'Section'
    for e in xcSet.elements:
        e.setProp("baseSection", baseSection)
        e.setProp("reinforcementUpVector", geom.Vector3d(0,0,1)) # Z+
        e.setProp("reinforcementIVector", geom.Vector3d(1,0,0)) # X+
        e.setProp("bottomReinforcementI", def_simple_RC_section.LongReinfLayers([bottomFlangeLongitudinalBottomReinf]))
        e.setProp("topReinforcementI", def_simple_RC_section.LongReinfLayers([bottomFlangeLongitudinalTopReinf]))
        elementCenter= e.getPosCentroid(True)
        ePos2d= geom.Pos2d(elementCenter.x, elementCenter.y)
        elementZone= 'D'
        bottomFlangeTransverseBottomReinf= bottomFlangeTransverseBottomReinfD
        bottomFlangeTransverseTopReinf= bottomFlangeTransverseTopReinfD
        if(zoneA1.In(ePos2d,.05) or zoneA2.In(ePos2d,.05)):
            elementZone= 'A'
            bottomFlangeTransverseBottomReinf= bottomFlangeTransverseBottomReinfA
            bottomFlangeTransverseTopReinf= bottomFlangeTransverseTopReinfA
        elif(zoneB1.In(ePos2d,.05) or zoneB2.In(ePos2d,.05)):
            elementZone= 'B'
            bottomFlangeTransverseBottomReinf= bottomFlangeTransverseBottomReinfB
            bottomFlangeTransverseTopReinf= bottomFlangeTransverseTopReinfB
        elif(zoneC1.In(ePos2d,.05) or zoneC2.In(ePos2d,.05)):
            elementZone= 'C'
            bottomFlangeTransverseBottomReinf= bottomFlangeTransverseBottomReinfC
            bottomFlangeTransverseTopReinf= bottomFlangeTransverseTopReinfC        
        e.setProp("bottomReinforcementII", def_simple_RC_section.LongReinfLayers([bottomFlangeTransverseBottomReinf]))
        e.setProp("topReinforcementII", def_simple_RC_section.LongReinfLayers([bottomFlangeTransverseTopReinf]))

# Define sections.

## Define spatial distribution of reinforced concrete sections.
reinfConcreteSectionDistribution= RC_material_distribution.RCMaterialDistribution()
for xcSet in girderSets+bridgeDeckSets:
    reinfConcreteSectionDistribution.assignFromElementProperties(elemSet= xcSet.getElements)

#reinfConcreteSectionDistribution.report()

reinfConcreteSectionDistribution.dump()
