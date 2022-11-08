# -*- coding: utf-8 -*-
import re
from actions import loads

# Loads cases.
loadCaseManager= lcm.LoadCaseManager(preprocessor)
loadCaseNames= list()

loadCaseNames.append('G1A') # Prefabricated beams self weight.
loadCaseNames.append('G1B') # Bridge deck self weight.
loadCaseNames.append('G2') # Dead load.
loadCaseNames.append('G3SHRA') # Girder initial shrinkage (before the deck slab is cast).
loadCaseNames.append('G3SHRB') # Girder and bridge deck concrete shrinkage (after the deck slab is cast).
loadCaseNames.append('G3CREEP') # Concrete creep.
loadCaseNames.append('Q1a1') # Tren de cargas 1 posición A1.
loadCaseNames.append('Q1a2') # Tren de cargas 1 posición A2.
loadCaseNames.append('Q1b1') # Trenes de cargas 1 y 2 posición B1.
loadCaseNames.append('Q1b2') # Trenes de cargas 1 y 2 posición B2.
loadCaseNames.append('Q1b1F') # Frenado trenes de cargas 1 y 2 posición B1.
loadCaseNames.append('Q1b2F') # Frenado trenes de cargas 1 y 2 posición B2.

loadCaseNames.append('Q21') # Left wind (Y-).
loadCaseNames.append('Q22') # Right wind (Y+).
# loadCaseNames.append('VLONG') # Viento longitudinal.
# loadCaseNames.append('S') # Snow.
loadCaseNames.append('Q31') # Thermal contraction.
loadCaseNames.append('Q31neopr') # Thermal contraction (bearings design).
loadCaseNames.append('Q32') # Thermal expansion.
loadCaseNames.append('Q32neopr') # Thermal expansion (bearings design).

loadCaseNames.append('LTPh1') # Load test phase 1.
loadCaseNames.append('LTPh2') # Load test phase 2.

loadCaseManager.defineSimpleLoadCases(loadCaseNames) 

# Load values.
gravityVector= xc.Vector([0.0,0.0,9.81])

## Self weight
cLC= loadCaseManager.setCurrentLoadCase('G1A')
cLC.description= 'Peso propio vigas prefabricadas.'
modelSpace.createSelfWeightLoad(girderSet,gravityVector)

cLC= loadCaseManager.setCurrentLoadCase('G1B')
cLC.description= 'Peso propio losa.'
modelSpace.createSelfWeightLoad(bridgeDeckSet,gravityVector)

## Shrinkage

def setStrainLoad(elementSet, strainValues):
    ''' Define a strain load.
    
    :param elementSet: set of elements to apply the load on.
    :param strainValue: value of the strain.
    '''
    eleLoad= cLC.newElementalLoad("shell_strain_load")
    eleLoad.elementTags= xc.ID(elementSet.getElementTags())
    sz= len(eleLoad.elementTags)
    if(sz==0):
        lmsg.warning('set: '+elementSet.name+' is empty\n')
    for gp in [0,1,2,3]: # for each Gauss point.
        for c in [0,1]: # for each component.
            eleLoad.setStrainComp(gp,c,strainValues[c]) #(id of Gauss point, id of component, value)
    

### Girder shrinkage
totalGirderShrinkage= 1.01e-4 # Shrinkage on girders.

#### Initial girder shrinkage (before the deck slab is cast).
initialGirderShrinkage= 2/3*totalGirderShrinkage
cLC= loadCaseManager.setCurrentLoadCase('G3SHRA')
cLC.description= 'Girder initial shrinkage.'
setStrainLoad(girderSet, [initialGirderShrinkage,initialGirderShrinkage])

#### Girder and deck shrinkage (after the deck slab is cast).
girderShrinkage= totalGirderShrinkage-initialGirderShrinkage
cLC= loadCaseManager.setCurrentLoadCase('G3SHRB')
cLC.description= 'Shrinkage.'
setStrainLoad(girderSet, [girderShrinkage,girderShrinkage])
deckShrinkage= 2.93e-4 # Shrinkage on girders.
setStrainLoad(bridgeDeckSet, [deckShrinkage,deckShrinkage])

## Creep
def setCreepLoad(setList, concreteAge, concreteAgeAtLoading):
    ''' Define the creep load for the elements of the set.

    :param setList: list of sets containing the elements that creep.
    :param concreteAge: concrete age in days at the moment considered.
    :param concreteAgeAtLoading: age of concrete in days at loading.
    '''
    cLC= loadCaseManager.setCurrentLoadCase('G3CREEP')
    for gSet in setList:
        sectionName= gSet.getProp('sectionName')
        rcSection= rcSectionDict[sectionName]
        concrType= rcSection.concrType
        for e in gSet.getElements:
            avgStress1= e.getMeanInternalForce("n1")/rcSection.depth
            avgStress2= e.getMeanInternalForce("n2")/rcSection.depth
            if((avgStress1**2+avgStress2**2)<0.1):
                lmsg.warning('Concrete stresses are very small. No creep expected.') 
            eps1= concrType.getCreepDeformation(concreteAgeAtLoading,concreteAge,HR*100,rcSection.depth,avgStress1)
            eps2= concrType.getCreepDeformation(concreteAgeAtLoading,concreteAge,HR*100,rcSection.depth,avgStress2)
            strainValues= [eps1,eps2]
            eleLoad= cLC.newElementalLoad("shell_strain_load")
            eleLoad.elementTags= xc.ID([e.tag])
            for gp in [0,1,2,3]: # for each Gauss point.
                for c in [0,1]: # for each component.
                    eleLoad.setStrainComp(gp,c,strainValues[c]) #(id of Gauss point, id of component, value)

deckLength= 24.76 # Length of the deck edge.

# Loaded zones.

## Walkways
walkway1Set= modelSpace.defSet('walkway1Set')
walkway2Set= modelSpace.defSet('walkway2Set')
notionalLane1Set= modelSpace.defSet('notionalLane1Set')
notionalLane2Set= modelSpace.defSet('notionalLane2Set')
notionalLaneRSet= modelSpace.defSet('notionalLaneRSet')
for s in xcTotalSet.surfaces:
    if 'IFCWalkway1' in s.getProp('labels'):
        modelSpace.pickElementsInZone(zone= s.getPolygon(), resultSet= walkway1Set, originSet= bridgeDeckSet)
    if 'IFCWalkway2' in s.getProp('labels'):
        modelSpace.pickElementsInZone(zone= s.getPolygon(), resultSet= walkway2Set, originSet= bridgeDeckSet)
    if 'IFCNotionalLane1' in s.getProp('labels'):
        modelSpace.pickElementsInZone(zone= s.getPolygon(), resultSet= notionalLane1Set, originSet= bridgeDeckSet)
    if 'IFCNotionalLane2a' in s.getProp('labels'):
        modelSpace.pickElementsInZone(zone= s.getPolygon(), resultSet= notionalLane2Set, originSet= bridgeDeckSet)
    if 'IFCNotionalLane2b' in s.getProp('labels'):
        modelSpace.pickElementsInZone(zone= s.getPolygon(), resultSet= notionalLane2Set, originSet= bridgeDeckSet)
    if 'IFCNotionalLaneR' in s.getProp('labels'):
        modelSpace.pickElementsInZone(zone= s.getPolygon(), resultSet= notionalLaneRSet, originSet= bridgeDeckSet)

notionalLanes= [notionalLane1Set, notionalLane2Set, notionalLaneRSet]

# Dead load.
cLC= loadCaseManager.setCurrentLoadCase('G2')
cLC.description= 'Dead load.'

## Rigid barrier
numNodesRigidBarrier= len(roadwayRightBorderSet.nodes)+len(roadwayLeftBorderSet.nodes)
rigidBarrierLoad= 2.0*8e3*deckLength/numNodesRigidBarrier # load/node
for n in roadwayRightBorderSet.nodes:
    cLC.newNodalLoad(n.tag, xc.Vector([0.0,0.0,-rigidBarrierLoad,0.0,0.0,0.0]))
for n in roadwayLeftBorderSet.nodes:
    cLC.newNodalLoad(n.tag, xc.Vector([0.0,0.0,-rigidBarrierLoad,0.0,0.0,0.0]))
## Walkways
for e in walkway1Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-8.0e3]))
for e in walkway2Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-8.0e3]))
## Vandal protection
numNodesVandalProtection= len(deckRightBorderSet.nodes)+len(deckLeftBorderSet.nodes)
vandalProtectionLoad= 2.0*1e3*deckLength/numNodesVandalProtection # load/node
for n in deckRightBorderSet.nodes:
    cLC.newNodalLoad(n.tag, xc.Vector([0.0,0.0,-vandalProtectionLoad,0.0,0.0,0.0]))
for n in deckLeftBorderSet.nodes:
    cLC.newNodalLoad(n.tag, xc.Vector([0.0,0.0,-vandalProtectionLoad,0.0,0.0,0.0]))

## Pavement
pavementWeight= 1.725e3
for s in notionalLanes:
    for e in s.elements:
        e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-pavementWeight]))

# Traffic loads.

## Loaded points.
TS1Pos1Set= modelSpace.defSet('TS1Pos1Set')
TS1Pos2Set= modelSpace.defSet('TS1Pos2Set')
TS2Pos1Set= modelSpace.defSet('TS2Pos1Set')
TS2Pos2Set= modelSpace.defSet('TS2Pos2Set')
for p in xcTotalSet.points:
    if 'IFCTS1Pos1a' in p.getProp('labels'):
        modelSpace.pickNodeOnPoint(pt= p.getPos, resultSet= TS1Pos1Set, originSet= bridgeDeckSet)
    if 'IFCTS1Pos1b' in p.getProp('labels'):
        modelSpace.pickNodeOnPoint(pt= p.getPos, resultSet= TS1Pos1Set, originSet= bridgeDeckSet)
    if 'IFCTS1Pos1c' in p.getProp('labels'):
        modelSpace.pickNodeOnPoint(pt= p.getPos, resultSet= TS1Pos1Set, originSet= bridgeDeckSet)
    if 'IFCTS1Pos1d' in p.getProp('labels'):
        modelSpace.pickNodeOnPoint(pt= p.getPos, resultSet= TS1Pos1Set, originSet= bridgeDeckSet)
    if 'IFCTS1Pos2a' in p.getProp('labels'):
        modelSpace.pickNodeOnPoint(pt= p.getPos, resultSet= TS1Pos2Set, originSet= bridgeDeckSet)
    if 'IFCTS1Pos2b' in p.getProp('labels'):
        modelSpace.pickNodeOnPoint(pt= p.getPos, resultSet= TS1Pos2Set, originSet= bridgeDeckSet)
    if 'IFCTS1Pos2c' in p.getProp('labels'):
        modelSpace.pickNodeOnPoint(pt= p.getPos, resultSet= TS1Pos2Set, originSet= bridgeDeckSet)
    if 'IFCTS1Pos2d' in p.getProp('labels'):
        modelSpace.pickNodeOnPoint(pt= p.getPos, resultSet= TS1Pos2Set, originSet= bridgeDeckSet)
    if 'IFCTS2Pos1a' in p.getProp('labels'):
        modelSpace.pickNodeOnPoint(pt= p.getPos, resultSet= TS2Pos1Set, originSet= bridgeDeckSet)
    if 'IFCTS2Pos1b' in p.getProp('labels'):
        modelSpace.pickNodeOnPoint(pt= p.getPos, resultSet= TS2Pos1Set, originSet= bridgeDeckSet)
    if 'IFCTS2Pos1c' in p.getProp('labels'):
        modelSpace.pickNodeOnPoint(pt= p.getPos, resultSet= TS2Pos1Set, originSet= bridgeDeckSet)
    if 'IFCTS2Pos1d' in p.getProp('labels'):
        modelSpace.pickNodeOnPoint(pt= p.getPos, resultSet= TS2Pos1Set, originSet= bridgeDeckSet)
    if 'IFCTS2Pos2a' in p.getProp('labels'):
        modelSpace.pickNodeOnPoint(pt= p.getPos, resultSet= TS2Pos2Set, originSet= bridgeDeckSet)
    if 'IFCTS2Pos2b' in p.getProp('labels'):
        modelSpace.pickNodeOnPoint(pt= p.getPos, resultSet= TS2Pos2Set, originSet= bridgeDeckSet)
    if 'IFCTS2Pos2c' in p.getProp('labels'):
        modelSpace.pickNodeOnPoint(pt= p.getPos, resultSet= TS2Pos2Set, originSet= bridgeDeckSet)
    if 'IFCTS2Pos2d' in p.getProp('labels'):
        modelSpace.pickNodeOnPoint(pt= p.getPos, resultSet= TS2Pos2Set, originSet= bridgeDeckSet)

### Q1a1
cLC= loadCaseManager.setCurrentLoadCase('Q1a1')
cLC.description= 'Vehículo pesado 600 kN en posición A1.'
#### Tandem set 1 position A1.
for n in TS1Pos1Set.nodes:
    cLC.newNodalLoad(n.tag, xc.Vector([0.0,0.0,-150e3,0.0,0.0,0.0]))
#### Surface loads.
for e in notionalLane1Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-9.0e3]))
for e in walkway1Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-5.0e3]))
### Q1a2
cLC= loadCaseManager.setCurrentLoadCase('Q1a2')
cLC.description= 'Vehículo pesado 600 kN en posición A2.'
#### Tandem set 1 position A2.
for n in TS1Pos2Set.nodes:
    cLC.newNodalLoad(n.tag, xc.Vector([0.0,0.0,-150e3,0.0,0.0,0.0]))
#### Surface loads.
for e in notionalLane1Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-9.0e3]))
for e in walkway1Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-5.0e3]))
### Q1b1
cLC= loadCaseManager.setCurrentLoadCase('Q1b1')
cLC.description= 'Vehículo pesados 600 kN y 400 kN en posición B1.'
#### Tandem set 1 position B1.
for n in TS1Pos1Set.nodes:
    cLC.newNodalLoad(n.tag, xc.Vector([0.0,0.0,-150e3,0.0,0.0,0.0]))
#### Tandem set 2 position B1.
for n in TS2Pos1Set.nodes:
    cLC.newNodalLoad(n.tag, xc.Vector([0.0,0.0,-100e3,0.0,0.0,0.0]))
#### Surface loads.
for e in notionalLane1Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-9.0e3]))
for e in notionalLane2Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-2.5e3]))
for e in notionalLaneRSet.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-2.5e3]))
for e in walkway1Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-5.0e3]))
for e in walkway2Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-5.0e3]))
### Q1b2
cLC= loadCaseManager.setCurrentLoadCase('Q1b2')
cLC.description= 'Vehículo pesados 600 kN y 400 kN en posición B2.'
#### Tandem set 1 position B2.
for n in TS1Pos2Set.nodes:
    cLC.newNodalLoad(n.tag, xc.Vector([0.0,0.0,-150e3,0.0,0.0,0.0]))
#### Tandem set 2 position B2.
for n in TS2Pos2Set.nodes:
    cLC.newNodalLoad(n.tag, xc.Vector([0.0,0.0,-100e3,0.0,0.0,0.0]))
#### Surface loads.
for e in notionalLane1Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-9.0e3]))
for e in notionalLane2Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-2.5e3]))
for e in notionalLaneRSet.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-2.5e3]))
for e in walkway1Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-5.0e3]))
for e in walkway2Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-5.0e3]))
### Q1b1F
cLC= loadCaseManager.setCurrentLoadCase('Q1b1F')
cLC.description= 'Frenado. Vehículos pesados 600 kN y 400 kN en posición B1.'
#### Tandem set 1 position B1.
for n in TS1Pos1Set.nodes:
    cLC.newNodalLoad(n.tag, xc.Vector([-150e3*0.6,0.0,-150e3*0.75,0.0,0.0,0.0]))
#### Tandem set 2 position B1.
for n in TS2Pos1Set.nodes:
    cLC.newNodalLoad(n.tag, xc.Vector([0.0,0.0,-100e3,0.0,0.0,0.0]))
#### Surface loads.
for e in notionalLane1Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([-9.0e3*0.1,0.0,-9.0e3*0.4]))
for e in notionalLane2Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-2.5e3]))
for e in notionalLaneRSet.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-2.5e3]))
for e in walkway1Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-5.0e3]))
for e in walkway2Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-5.0e3]))
### Q1b2F
cLC= loadCaseManager.setCurrentLoadCase('Q1b2F')
cLC.description= 'Frenado. Vehículos pesados 600 kN y 400 kN en posición B2.'
#### Tandem set 1 position B2.
for n in TS1Pos2Set.nodes:
    cLC.newNodalLoad(n.tag, xc.Vector([-150e3*0.6,0.0,-150e3*0.75,0.0,0.0,0.0]))
#### Tandem set 2 position B2.
for n in TS2Pos2Set.nodes:
    cLC.newNodalLoad(n.tag, xc.Vector([0.0,0.0,-100e3,0.0,0.0,0.0]))
#### Surface loads.
for e in notionalLane1Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([-9.0e3*0.1,0.0,-9.0e3*0.4]))
for e in notionalLane2Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-2.5e3]))
for e in notionalLaneRSet.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-2.5e3]))
for e in walkway1Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-5.0e3]))
for e in walkway2Set.elements:
    e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-5.0e3]))

# Load test loads.

## Loaded points.
LTPh1Set= modelSpace.defSet('LTPh1Set')
LTPh2Set= modelSpace.defSet('LTPh2Set')
for p in xcTotalSet.points:
    labels= p.getProp('labels')
    ltphRegex= re.compile('IFCLTPh.*')
    if any((match:= ltphRegex.match(lbl)) for lbl in labels):
        tokens= match.group(0).split('_')
        phase= tokens[0][-1]
        cLC= loadCaseManager.setCurrentLoadCase('LTPh'+phase)
        loadValue= -float(tokens[2])*1e3
        pos= p.getPos
        n= bridgeDeckSet.getNearestNode(pos)
        cLC.newNodalLoad(n.tag, xc.Vector([0.0,0.0,loadValue,0.0,0.0,0.0]))

    
# Wind loads.

## Force on the protection panels.
panelHeight= 2.5
winwardPanelForce= 4.23e3*deckLength # Wind force on winward panel
leewardPanelForce= 2.41e3*deckLength # Wind force on leeward panel
leftSidePanelCenter= geom.Pos3d(8.81218,11.20,.4+panelHeight/2.0)
rightSidePanelCenter= geom.Pos3d(12.38,0.0,.4+panelHeight/2.0)
## Force on girder webs.
winwardGirderPressure= 1.45e3/girdersDepth # Wind pressure on winward girder web
leewardGirderPressure= 0.48e3/girdersDepth # Wind pressure on winward girder web

## Left wind (Y-)
cLC= loadCaseManager.setCurrentLoadCase('Q21')
cLC.description= 'Left wind (Y-).'

### Left wind on protection panels.
#### Windward panel (left panel)
leftWindWindwardPanel= loads.SlidingVectorLoad(name='leftWindWindwardPanel', nodes= deckLeftBorderSet.nodes, pntCoord= leftSidePanelCenter, loadVector= xc.Vector([0.0,-winwardPanelForce,0.0,0.0,0.0,0.0]))
leftWindWindwardPanel.appendLoadToCurrentLoadPattern()
#### Leeward panel (right panel).
leftWindLeewardPanel= loads.SlidingVectorLoad(name='leftWindLeewardPanel', nodes= deckRightBorderSet.nodes, pntCoord= rightSidePanelCenter, loadVector= xc.Vector([0.0,-leewardPanelForce,0.0,0.0,0.0,0.0]))
leftWindLeewardPanel.appendLoadToCurrentLoadPattern()

### Left wind on girders.
leftWindwardGirderWeb= list() # Winward girder web for left wind.
leftLeewardGirderWeb= list() # Leeward girder web for left wind.

for e in leftWindGirderWebFaceSet.elements:
    pos= e.getPosCentroid(True)
    if(pos.y<deckWidth/2.0):
        leftLeewardGirderWeb.append(e.tag)
    else:
        leftWindwardGirderWeb.append(e.tag)

leftWindLeewardGirderPressure= cLC.newElementalLoad("shell_uniform_load")
leftWindLeewardGirderPressure.elementTags= xc.ID(leftLeewardGirderWeb)
leftWindLeewardGirderPressure.transComponent= -leewardGirderPressure

leftWindWindwardGirderPressure= cLC.newElementalLoad("shell_uniform_load")
leftWindWindwardGirderPressure.elementTags= xc.ID(leftWindwardGirderWeb)
leftWindWindwardGirderPressure.transComponent= -winwardGirderPressure

## Right wind (Y+)
cLC= loadCaseManager.setCurrentLoadCase('Q22')
cLC.description= 'Right wind (Y+).'

### Right wind on protection panels.
#### Windward panel (right panel)
rightWindWindwardPanel= loads.SlidingVectorLoad(name='rightWindWindwardPanel', nodes= deckRightBorderSet.nodes, pntCoord= rightSidePanelCenter, loadVector= xc.Vector([0.0,winwardPanelForce,0.0,0.0,0.0,0.0]))
rightWindWindwardPanel.appendLoadToCurrentLoadPattern()
#### Leeward panel (left panel).
rightWindLeewardPanel= loads.SlidingVectorLoad(name='rightWindLeewardPanel', nodes= deckLeftBorderSet.nodes, pntCoord= leftSidePanelCenter, loadVector= xc.Vector([0.0,leewardPanelForce,0.0,0.0,0.0,0.0]))
rightWindLeewardPanel.appendLoadToCurrentLoadPattern()

### Right wind on girders.
rightWindwardGirderWeb= list() # Winward girder web for right wind.
rightLeewardGirderWeb= list() # Leeward girder web for right wind.

for e in rightWindGirderWebFaceSet.elements:
    pos= e.getPosCentroid(True)
    if(pos.y>deckWidth/2):
        rightLeewardGirderWeb.append(e.tag)
    else:
        rightWindwardGirderWeb.append(e.tag)

rightWindLeewardGirderPressure= cLC.newElementalLoad("shell_uniform_load")
rightWindLeewardGirderPressure.elementTags= xc.ID(rightLeewardGirderWeb)
rightWindLeewardGirderPressure.transComponent= -leewardGirderPressure

rightWindWindwardGirderPressure= cLC.newElementalLoad("shell_uniform_load")
rightWindWindwardGirderPressure.elementTags= xc.ID(rightWindwardGirderWeb)
rightWindWindwardGirderPressure.transComponent= -winwardGirderPressure
                                               
# Thermal loads.
alpha= 1.0e-5 # Thermal expansion coefficient of concrete and steel 1/ºC
zTop= 0.1550904914692656
zBottom= -1.35

def tempGradient(z, Ttop, Tbottom, zTop, zBottom):
    ''' Return the temperature corresponding to "z" coordinate

    :param z: z coordinate.
    :param Ttop: temperature at the top of the deck.
    :param Tbottom: temperature at the bottom of the deck.
    :param zTop: z coordinate of the top of the deck.
    :param zBottom: z coordinate of the bottom of the deck.
    '''
    return (Ttop-Tbottom)/(zTop-zBottom)*(z-zBottom)+Tbottom

def applyThermalLoad(Ttop, Tbottom, zTop, zBottom):
    ''' Apply to the model the thermal load defined by the arguments.

    :param Ttop: temperature at the top of the deck.
    :param Tbottom: temperature at the bottom of the deck.
    :param zTop: z coordinate of the top of the deck.
    :param zBottom: z coordinate of the bottom of the deck.
    '''
    # Shell elements.
    for e in concreteSet.elements:
        eleLoad= cLC.newElementalLoad("shell_strain_load")
        eleLoad.elementTags= xc.ID([e.tag])
        # Gauss points positions
        gaussPoints= e.getGaussModel().getGaussPoints()
        for i, p in enumerate(gaussPoints):
            gpPos= e.getCartesianCoordinates(p, True)
            AT= tempGradient(gpPos.z, Ttop, Tbottom, zTop, zBottom)
            eleLoad.setStrainComp(i,0,alpha*AT)
            eleLoad.setStrainComp(i,1,alpha*AT)

    # Truss elements (prestressing chords)
    for e in tendonSet.elements:
        eleLoad= cLC.newElementalLoad("truss_strain_load")
        eleLoad.elementTags= xc.ID([e.tag])
        nodes= e.getNodes
        pos1= nodes[0].getInitialPos3d
        AT1= tempGradient(pos1.z, Ttop, Tbottom, zTop, zBottom)
        pos2= nodes[1].getInitialPos3d
        AT2= tempGradient(pos2.z, Ttop, Tbottom, zTop, zBottom)
        eleLoad.eps1= alpha*AT1
        eleLoad.eps2= alpha*AT2

## Thermal contraction.
cLC= loadCaseManager.setCurrentLoadCase('Q31')
cLC.description= 'Thermal contraction.'
Ttop= -10.33 # Temperature at top side (Celsius degrees)
Tbottom= Ttop-5.0 # Temperature at bottom side (Celsius degrees)
applyThermalLoad(Ttop, Tbottom, zTop, zBottom)

cLC= loadCaseManager.setCurrentLoadCase('Q31neopr')
cLC.description= 'Thermal contraction (bearings design).'
Ttop= -10.33+15.0 # Temperature at top side (Celsius degrees)
Tbottom= Ttop-5.0+15.0 # Temperature at bottom side (Celsius degrees)
applyThermalLoad(Ttop, Tbottom, zTop, zBottom)

## Thermal expansion.
cLC= loadCaseManager.setCurrentLoadCase('Q32')
cLC.description= 'Thermal expansion.'
Ttop= 47.7 # Temperature at top side (Celsius degrees)
Tbottom= Ttop-10.0 # Temperature at bottom side (Celsius degrees)

applyThermalLoad(Ttop, Tbottom, zTop, zBottom)

cLC= loadCaseManager.setCurrentLoadCase('Q32neopr')
cLC.description= 'Thermal expansion (bearings design).'
Ttop= 47.7+15.0 # Temperature at top side (Celsius degrees)
Tbottom= Ttop-10.0+15.0 # Temperature at bottom side (Celsius degrees)

applyThermalLoad(Ttop, Tbottom, zTop, zBottom)


