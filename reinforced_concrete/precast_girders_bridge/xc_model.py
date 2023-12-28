# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

import os
import math
import re
import geom
import xc

from misc_utils import log_messages as lmsg
from model import predefined_spaces
# Materials
from materials.ehe import EHE_materials
from materials.prestressing import pre_tensioned_tendons
from materials import bridge_bearings as bb
from postprocess import element_section_map
from materials.sections.fiber_section import def_simple_RC_section
from postprocess import RC_material_distribution
# Loads
from actions import load_cases as lcm
from actions import combinations as combs
from actions.load_combination_utils import utils
# Solution
from solution import predefined_solutions
# Postprocess
from postprocess import output_handler
from postprocess.config import default_config

deckWidth= 11.2 # Deck width.
girdersDepth= 1.4 # Girders depth.

def connectNodesToConcrete(nodes, elementSet, connectorSet):
    ''' Connect the nodes on the prestressing strands to the
        reinforced concrete elements.

    :param nodes: prestressing strand nodes to connect.
    :param elementSet: concrete elements to connect to.
    :param connectorSet: container for the new elements that
                         connect the nodes to the existing 
                         elements.
    '''
    gluedDOFs= xc.ID([0,1,2,3,4,5])
    for n in nodes:
        elementToGlue= elementSet.getNearestElement(n.getInitialPos3d)
        nPos= n.getInitialPos3d
        newNodePos= elementToGlue.getProjection(nPos,True)
        newNode= modelSpace.newNode(newNodePos.x, newNodePos.y, newNodePos.z)
        # Fix the new node to the element.
        glue= modelSpace.constraints.newGlueNodeToElement(newNode,elementToGlue,gluedDOFs)
        # Create a new element connecting the nodes.
        connectorXZVector= modelSpace.getSuitableXZVector(n,newNode)
        connectorTrfName= "lin_"+str(n.tag)+'_'+str(newNode.tag)
        d= nPos.dist(newNodePos)
        if(d<0.005): # Too short element
            lmsg.error('Element too short',l.tag, n.tag, elementToGlue.tag, d)
        connectorTransf= modelSpace.newLinearCrdTransf(connectorTrfName,connectorXZVector)
        elements.defaultTransformation= connectorTransf.name
        connectorElement= elements.newElement("ElasticBeam3d",xc.ID([n.tag,newNode.tag]))
        connectorSet.elements.append(connectorElement)

workingDirectory= default_config.setWorkingDirectory()

import env_config
FEcase= xc.FEProblem()
fname= os.path.abspath(__file__).strip('.py')
FEcase.title= 'Test'
exec(cfg.compileCode('tablero_rev04_blocks.py'))
# Problem type
preprocessor=FEcase.getPreprocessor
nodes= preprocessor.getNodeHandler
modelSpace= predefined_spaces.StructuralMechanics3D(nodes) 

xcTotalSet= modelSpace.getTotalSet()

# Group bridge parts.

## Create sets
setKeys= [('IFCDiaphragm.*', 'Diaphragms'), ('IFCGirder[12]Webs','GirderWebs'), ('IFCGirder[12]Tops','GirderTops'), ('IFCGirder[12]TaperedBottomFlange','TapperedBottoms'), ('IFCGirder[12]BottomFlange', 'BottomFlanges'), ('IFCGirder[12]Link', 'GirderLink'), ('IFCBridgeDeckExt.*', 'BridgeDeckExt'), ('IFCBridgeDeckGirder.*', 'BridgeDeckGirder'), ('IFCBridgeDeckInt.*', 'BridgeDeckInt'), ('IFCTendon.*','LowerTendons'), ('IFCUpperTendon.*','UpperTendons')]
xcSets= list()

for key in setKeys:
    setName= key[1]
    xcSets.append(modelSpace.defSet(setName))

## Surfaces: put each part on its set and create the corresponding section.
reinfSteel= EHE_materials.B500S
rcSectionDict= dict()
for s in xcTotalSet.surfaces:
    s.setElemSizeIJ(0.5,0.5) # Set element size
    label= s.getProp('labels')[0]
    attributes= s.getProp('attributes')
    for sk in setKeys: # set keys defined at the top of this file
        regExp= sk[0]
        if(re.match(regExp, label)):
            setName= sk[1]
            xcSet= modelSpace.getSet(setName)
            xcSet.surfaces.append(s)
            concrete= EHE_materials.concrOfName[attributes['matId'].replace('-','')]
            thickness= attributes['Thickness']
            sectionName= setName+'_section'
            if(sectionName not in rcSectionDict):
                sectionDescr= setName+' section, thickness '+str(thickness)+' m.'
                rcSection= element_section_map.LegacyRCSlabBeamSection(name= sectionName,sectionDescr= sectionDescr, concrType= concrete, reinfSteelType= reinfSteel, depth= thickness)
                rcSectionDict[sectionName]= rcSection
            xcSet.setProp('sectionName', sectionName)
            
preprocessor.getMultiBlockTopology.getSurfaces.conciliaNDivs()

## Tendons.
strand= EHE_materials.Y1860S7Strand_15_3
strandInitialStress= 1395e6
### Stress losses due to shrinkage and creep are computed automatically
### when those strains are introduced into the model.
strandWedgePenetrationLosses= 41.4e6
prestressingSteel= strand.defDiagK(preprocessor,strandInitialStress-strandWedgePenetrationLosses)
lowerTendonSet= modelSpace.getSet('LowerTendons')
upperTendonSet= modelSpace.getSet('UpperTendons')
for l in xcTotalSet.lines:
    if(l.hasProp('labels')):
        label= l.getProp('labels')[0]
        if(label.startswith('IFCTendon')):
            l.setElemSize(0.25) # Set element size
            IfcProperties= l.getProp('attributes')['IfcProperties']
            bondedLength= float(IfcProperties['Bonded length'].split(';')[4])
            tang= l.getTang(0.0)
            vDir= geom.Vector3d(tang[0], tang[1], tang[2])
            p1= l.getP1(); p2= l.getP2()
            p1.pos= p1.pos+bondedLength*vDir
            p2.pos= p2.pos-bondedLength*vDir
            lowerTendonSet.lines.append(l)
        elif(label.startswith('IFCUpperTendon')):
            l.setElemSize(0.25) # Set element size
            upperTendonSet.lines.append(l)

## Define material for shell elements.
stiffnessReductionFactor= 1.0 # Stiffness reduction due to concrete cracking.
#stiffnessReductionFactor= 6.0
shellMaterialDict= dict()
for key in rcSectionDict:
    rcSection= rcSectionDict[key]
    shellMaterial= rcSection.getElasticMembranePlateSection(preprocessor, stiffnessReductionFactor)
    shellMaterialDict[key]= shellMaterial

# Create mesh
seedElemHandler= preprocessor.getElementHandler.seedElemHandler

for key in setKeys:
    setName= key[1]
    xcSet= modelSpace.getSet(setName)
    if((setName=='LowerTendons') or (setName=='UpperTendons')):
        seedElemHandler.defaultMaterial= prestressingSteel.name
        seedElemHandler.dimElem= 3
        elem= seedElemHandler.newElement("Truss",xc.ID([0,0])) 
        elem.sectionArea= strand.area
    else:
        sectionName= xcSet.getProp('sectionName')
        shellMaterial= shellMaterialDict[sectionName]
        seedElemHandler.defaultMaterial= shellMaterial.name
        elem= seedElemHandler.newElement("ShellMITC4",xc.ID([0,0,0,0]))
    xcSet.genMesh(xc.meshDir.I)

    
## Girders set.
girderSetsNames= ['Diaphragms', 'GirderWebs', 'GirderTops', 'TapperedBottoms', 'BottomFlanges']
girderSets= list()
girderSet= modelSpace.defSet('girderSet')
for setName in girderSetsNames:
    xcSet= modelSpace.getSet(setName)
    girderSet+=(xcSet)
    girderSets.append(xcSet)
girderSet.fillDownwards()
### Some convenience sets.
girderWebs= modelSpace.getSet('GirderWebs')
girderBottomFlanges= modelSpace.getSet('BottomFlanges')
girderTapperedBottoms= modelSpace.getSet('TapperedBottoms')


## Bridge deck.
bridgeDeckSetsNames= ['BridgeDeckExt', 'BridgeDeckGirder', 'BridgeDeckInt']
bridgeDeckSets= list()
bridgeDeckSet= modelSpace.defSet('bridgeDeckSet')
for setName in bridgeDeckSetsNames:
    xcSet= modelSpace.getSet(setName)
    bridgeDeckSet+=(xcSet)
    bridgeDeckSets.append(xcSet)
bridgeDeckSet.fillDownwards()

## Define reinforcement
exec(cfg.compileCode('reinfDef.py'))

# Concrete set
concreteSet= modelSpace.defSet('concreteSet')
concreteSet+= girderSet
concreteSet+= bridgeDeckSet
concreteSet.fillDownwards()

# Tendon set
tendonSet= modelSpace.defSet('tendonSet')
tendonSet+= lowerTendonSet
tendonSet+= upperTendonSet
tendonSet.fillDownwards()

## Prestressed bottom flanges
prestressedBottomFlanges= modelSpace.defSet('prestressedBottomFlanges')
prestressedBottomFlanges+= modelSpace.getSet('TapperedBottoms')
prestressedBottomFlanges+= modelSpace.getSet('BottomFlanges')
prestressedBottomFlanges.fillDownwards()
girderTopSet= modelSpace.getSet('GirderTops')
girderTopSet.fillDownwards()

logFileName= workingDirectory+fname+'.log'
FEcase.logFileName= logFileName # Don't show warning messages during this process.
## Glue tendons to concrete
glueRCSection= def_simple_RC_section.RCRectangularSection(concrType= concrete, width= 0.15, depth= 0.15)
glueXCSection= glueRCSection.defElasticShearSection3d(modelSpace.preprocessor)
elements= modelSpace.getElementHandler()
elements.defaultMaterial= glueXCSection.name
connectorSet= modelSpace.defSet('connectorSet')
xcSets.append(connectorSet)
for l in lowerTendonSet.lines: # Tendons in girder bottom flange.
    connectNodesToConcrete(l.nodes, prestressedBottomFlanges, connectorSet)
for l in upperTendonSet.lines: # Tendons in girder top.
    connectNodesToConcrete(l.nodes, girderTopSet, connectorSet)
FEcase.logFileName= 'clog' # Show them again.

## Fix initial stresses inside transference lenghts.
for l in lowerTendonSet.lines: # Tendons in girder bottom flange.
    org= l.getP1().getPos
    attributes= l.getProp('attributes')
    ifcProperties= attributes['IfcProperties']
    transfLength= float(IfcProperties['Transference length'].split(';')[4])
    tendon= pre_tensioned_tendons.StraightStrand(strand, transfLength= transfLength, xInit= 0.0, xEnd= l.getLength())
    for e in l.elements:
        eCenterPos= e.getPosCentroid(True)
        x= eCenterPos.dist(org)
        stressFactor= tendon.getStressFactor(x)
        mat= e.getMaterial()
        mat.initialStress*= stressFactor
for l in lowerTendonSet.lines: # Upper tendons in girder.
    org= l.getP1().getPos
    attributes= l.getProp('attributes')
    transfLength= 0.0
    tendon= pre_tensioned_tendons.StraightStrand(strand, transfLength= transfLength, xInit= 0.0, xEnd= l.getLength())
    for e in l.elements:
        eCenterPos= e.getPosCentroid(True)
        x= eCenterPos.dist(org)
        stressFactor= tendon.getStressFactor(x)
        mat= e.getMaterial()
        mat.initialStress*= stressFactor

# Constraints
supportSet= modelSpace.defSet('supportSet')
for p in xcTotalSet.points:
    if(p.hasProp('attributes')):
        attributes= p.getProp('attributes')
        ifc_type= attributes['IfcType']
        if(ifc_type=='Structural Point Connection'):
            pos= p.getPos
            n= xcTotalSet.getNearestNode(pos)
            nPos= n.getInitialPos3d
            if(pos.dist(nPos)>0.01):
                lmsg.error('No nodes at support position: ', pos)
            supportSet.nodes.append(n)

## Elastomeric bearings
hNetoNeopr= 44e-3 # rubber thickness (total).
aNeopr= 0.400 # bearing length
bNeopr= 0.500 # bearing widht
Gneopr= 800e3 # shear modulus of the elastomeric material.
Eneopr= 600e6 # elastic modulus of the elastomeric material.
cThickness= 0.25 # Thickness of the beam lower flange
sThickness= 0.03 # Thicknes of top and bottom steel plates.
fixedNodeSet= modelSpace.defSet('fixedNodeSet')
## Bearing connectors
bearingConnectorRCSection= def_simple_RC_section.RCRectangularSection(concrType= concrete, width= aNeopr+0.1, depth= bNeopr+0.1)
bearingConnectorXCSection= bearingConnectorRCSection.defElasticShearSection3d(modelSpace.preprocessor)
### Elastomeric bearings materials
neopr= bb.ElastomericBearing(G=Gneopr,a=aNeopr,b=bNeopr,e=hNetoNeopr)
neopr.defineMaterials(modelSpace.preprocessor)
bearingSet= modelSpace.defSet('bearingSet')
for n in supportSet.nodes:
    # Create the node at the top of the elastomeric beam
    nPos= n.getInitialPos3d
    n1= modelSpace.newNode(nPos.x, nPos.y, nPos.z-cThickness/2.0-sThickness)
    n1Pos= n1.getInitialPos3d
    # Create bar between the two nodes.
    d= nPos.dist(n1Pos)
    if(d<0.005): # Too short element
        lmsg.error('Element too short',l.tag, n.tag, elementToGlue.tag, d)
    bearingConnectorXZVector= modelSpace.getSuitableXZVector(n,n1)
    bearingConnectorTrfName= "lin_"+str(n.tag)+'_'+str(n1.tag)
    bearingConnectorTransf= modelSpace.newLinearCrdTransf(bearingConnectorTrfName,bearingConnectorXZVector)
    elements.defaultTransformation= bearingConnectorTransf.name
    elements.defaultMaterial= bearingConnectorXCSection.name
    bearingConnectorElement= elements.newElement("ElasticBeam3d",xc.ID([n.tag,n1.tag]))
    # Create a fixed node on the bearing bottom
    n0= modelSpace.newNode(nPos.x, nPos.y, nPos.z-cThickness/2.0-sThickness)
    modelSpace.fixNode('000_000',n0.tag)
    fixedNodeSet.nodes.append(n0)
    # Create the element representing the 
    bearing= neopr.putBetweenNodes(modelSpace,n0.tag,n1.tag)
    bearingSet.elements.append(bearing)

# Deck borders
deckRightBorderSet= modelSpace.defSet('deckRightBorderSet')
deckLeftBorderSet= modelSpace.defSet('deckLeftBorderSet')
for n in modelSpace.getSet('BridgeDeckExt').nodes:
    pos= n.getInitialPos3d
    if(abs(pos.y)<0.01): # Y- border
        deckRightBorderSet.nodes.append(n)
    if(abs(pos.y-11.2)<0.01): # Y+ border
        deckLeftBorderSet.nodes.append(n)

# Roadway borders
roadwayRightBorderSet= modelSpace.defSet('roadwayRightBorderSet')
roadwayLeftBorderSet= modelSpace.defSet('roadwayLeftBorderSet')
for n in bridgeDeckSet.nodes:
    pos= n.getInitialPos3d
    if(abs(pos.y-1.260)<0.1): # Y- border
        roadwayRightBorderSet.nodes.append(n)
    if(abs(pos.y-9.938)<0.1): # Y+ border
        roadwayLeftBorderSet.nodes.append(n)


# Girder web faces
rightWindGirderWebFaceSet= modelSpace.defSet('rightWindGirderWebFaceSet')
leftWindGirderWebFaceSet= modelSpace.defSet('leftWindGirderWebFaceSet')
windDirection= geom.Vector3d(0.0,1.0,0.0)
for e in modelSpace.getSet('GirderWebs').elements:
    kVector= e.getKVector3d(True)
    dot= windDirection.dot(kVector)
    if(dot<0): # Y+ face
        rightWindGirderWebFaceSet.elements.append(e)
    else:
        leftWindGirderWebFaceSet.elements.append(e)
leftWindGirderWebFaceSet.fillDownwards()
rightWindGirderWebFaceSet.fillDownwards()

# Solution

#solProc= predefined_solutions.PenaltyModifiedNewtonUMF(FEcase, convergenceTestTol= .01, printFlag= 2, convTestType= 'norm_unbalance_conv_test', numberingMethod= 'rcm')
solProc= predefined_solutions.PenaltyModifiedNewtonMUMPS(FEcase, convergenceTestTol= .005, printFlag= 0, convTestType= 'norm_disp_incr_conv_test', numberingMethod= 'rcm')
#solProc= predefined_solutions.PenaltyModifiedNewtonUMF(FEcase, convergenceTestTol= .005, printFlag= 2, convTestType= 'norm_disp_incr_conv_test', numberingMethod= 'rcm')

reactionCheckTol= 5.0

def solve_for_initial_state(loadCombExpr:str):
    ''' Compute solution for the initial state.

    loadCombExpr: string containing the expression of the load combination
    to analyze.
    '''
    modelSpace.removeAllLoadPatternsFromDomain()
    modelSpace.revertToStart()
    modelSpace.deactivateElements(bridgeDeckSet) # Deactivate bridge deck.

    combDict= utils.getCombinationDict(loadCombExpr)
    g1factor= float(combDict['G1']) # Self weight factor.
    g2factor= float(combDict['G2']) # Dead load factor.
    g3factor= float(combDict['G3']) # Creep and shrinkage effects factor.
    pFactor= float(combDict['P1']) # Prestressing factor.

    if(pFactor!=1.0):
        lmsg.warning('Factor for presstressing action different from 1.0 ('+str(pFactor)+') not implemented (it will be ignored).\n')
    analOk= solProc.solve()
    if(analOk!=0):
        lmsg.error('Can\'t solve for prestressing.')
        quit()
    else:
        print('prestressing.')

    lc0= modelSpace.addLoadCaseToDomain('G1A')
    lc0.gammaF= g1factor
    analOk= solProc.solve()
    if(analOk!=0):
        lmsg.error('Can\'t solve for: '+lc0.name)
        quit()
    else:
        print('girders in place')

    # Girders initial shrinkage
    lcG3SHRA= modelSpace.addLoadCaseToDomain('G3SHRA')
    lcG3SHRA.gammaF= g3factor
    analOk= solProc.solve()
    if(analOk!=0):
        lmsg.error('Can\'t solve for: '+lcG3SHRA.name)
        quit()
    else:
        print('girders initial shrinkage')
    
    # Remove stresses on bridge bearings.
    for e in bearingSet.elements:
        e.revertToStart()
    analOk= solProc.solve()
    if(analOk!=0):
        lmsg.error('Can\'t solve for bearings reset.')
        quit()
    else:
        print('removed stresses on bridge bearings')

    # Activate bridge deck.
    modelSpace.activateElements(bridgeDeckSet) 
    lc0B= modelSpace.addLoadCaseToDomain('G1B')
    lc0B.gammaF= g1factor
    analOk= solProc.solve()
    if(analOk!=0):
        lmsg.error('Can\'t solve for: '+lc0B.name)
        quit()
    else:
        print('activate bridge deck')

    # Shrinkage
    lcG3SHRB= modelSpace.addLoadCaseToDomain('G3SHRB')
    lcG3SHRB.gammaF= g3factor
    analOk= solProc.solve()
    if(analOk!=0):
        lmsg.error('Can\'t solve for: '+lcG3SHRB.name)
        quit()
    else:
        print('shrinkage')
    
    # Creep.
    lcG3CREEP= modelSpace.getLoadPattern('G3CREEP')
    lcG3CREEP.gammaF= g3factor
    # If not already defined, define creep
    if(lcG3CREEP.getNumLoads==0):
        setCreepLoad(girderSets, concreteAge, girdersConcreteAgeAtLoading)
        setCreepLoad(bridgeDeckSets, concreteAge, deckConcreteAgeAtLoading)
    lcG3CREEP= modelSpace.addLoadCaseToDomain('G3CREEP')
    analOk= solProc.solve(calculateNodalReactions= True, reactionCheckTolerance= reactionCheckTol)
    if(analOk!=0):
        lmsg.error('Can\'t solve for: '+lcG3CREEP.name)
        quit()
    else:
        print('creep')
    return analOk

class InitialStateStorage(object):

    def __init__(self):
        ''' Constructor.'''
        self.storedStates= dict()
        self.initialStateLoads= ['G1', 'G2', 'G3', 'P1']
        self.db= modelSpace.getNewDatabase('../aux1/initial_state.db')

    def solveForInitialState(self, initialState):
        ''' Compute and store the solution for the initial state argument.

        :param initialState: load combination corresponding to an initial state.
        '''
        initStateKey= utils.getFileNameFromCombinationExpresion(initialState)
        if initStateKey in self.storedStates:
            pseudoTime= self.storedStates[initStateKey]
            modelSpace.restore(pseudoTime)
        else:
            result= solve_for_initial_state(initialState)
            if(result!= 0):
                lmsg.error('Error when solving for: '+initialState+'(analOk='+str(result)+')')
                quit()
            pseudoTime= 100+len(self.storedStates)
            modelSpace.save(pseudoTime)
            self.storedStates[initStateKey]= pseudoTime

    def solve(self, combName, combExpr):
        ''' Solve for the comb expression argument.

        :param combName: load combination name.
        :param combExpr: load combination expression.
        '''
        initialState, loadState= utils.splitCombination(combExpr, self.initialStateLoads)
        print(combName, 'initial state: ', initialState, ' load state:', loadState)
        self.solveForInitialState(initialState) # initial state.

        loadPatternDict= utils.getCombinationDict(loadState)
        for key in loadPatternDict: # rest of the loads.
            lp= modelSpace.addLoadCaseToDomain(key)
            lp.gammaF= loadPatternDict[key]
        #print(modelSpace.getActiveLoadPatternNames())
        analOk= solProc.solve(calculateNodalReactions= True, reactionCheckTolerance= reactionCheckTol)
        if(analOk!=0):
            lmsg.error('Can\'t solve for: '+lc.name)
            quit()
        else:
            print(combName)
        return analOk
        
    def computeResponses(self, combContainer, limitState, displayFunction= None, setCalc= None):
        ''' Compute response for the serviciability limit states in the 
            container.

        :param combContainer: object containing the load combinations to 
                              solve for.
        '''
        if(limitState):
            limitState.createOutputFiles()
            internalForcesDict= dict()
            reactionsDict= dict()
            combinations= limitState.getCorrespondingLoadCombinations(combContainer)
        else:
            lmsg.error('Limit state not defined.')
        for key in combinations:
            comb= combinations[key]
            result= self.solve(comb.name, comb.expr)
            if(result!= 0):
                lmsg.error('Error when solving for: '+lcName+'(analOk='+str(result)+')')
                quit()
            # Write/display results.
            if(displayFunction):
                displayFunction()
            if(limitState):
                internalForcesDict.update(limitState.getInternalForcesDict(comb.name, setCalc.elements))
                reactionsDict.update(limitState.getReactionsDict(comb.name, fixedNodeSet.nodes))
                limitState.writeDisplacements(comb.name, setCalc.nodes)
                
            modelSpace.removeAllLoadPatternsFromDomain()
        if(limitState):
            limitState.writeInternalForces(internalForcesDict)
            limitState.writeReactions(reactionsDict)
        return result

def solve(loadCaseName, computeInitialState= False):
    ''' Compute solution for the load case argument.

    loadCaseName: name of the load case to analyze.
    '''
    # Initial state.
    analOk= 0
    if(computeInitialState):
        analOk= initial_state()
    # Load pattern.
    if(loadCaseName!=''):
        lc= modelSpace.addLoadCaseToDomain(loadCaseName)
        analOk= solProc.solve(calculateNodalReactions= True, reactionCheckTolerance= reactionCheckTol)
        if(analOk!=0):
            lmsg.error('Can\'t solve for: '+lc.name)
            quit()
        else:
            print(loadCaseName)

    return analOk

# Graphic stuff.
oh= output_handler.OutputHandler(modelSpace)
# oh.displayBlocks()
# oh.displayFEMesh(setsToDisplay= girderSet)
#oh.displayFEMesh(setsToDisplay= [leftWindGirderWebFaceSet]) #xcSets)leftWindWindwardPanel= loads.SlidingVectorLoad((name='leftWindWindwardPanel', nodes= deckLeftBorderSet.nodes, pntCoord= leftSidePanelCenter, loadVector= xc.Vector([0.0,winwardPanelForce,0.0,0.0,0.0,0.0])

#oh.displayLocalAxes(setToDisplay= girderSet)
# oh.displayLocalAxes(setToDisplay= bridgeDeckSet)
# oh.displayStrongWeakAxis(setToDisplay= bracingYShapeSet)
