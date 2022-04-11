# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AO_O)"
__copyright__= "Copyright 2022, LCPT and AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es ana.ortega@ciccp.es"

import geom
import xc

from misc_utils import log_messages as lmsg
from import_export import reader_base
from import_export import freecad_reader
from import_export import neutral_mesh_description as nmd
from model import predefined_spaces
from materials import typical_materials
from materials.awc_nds import structural_panels
from materials.awc_nds import dimensional_lumber as dl
from materials.awc_nds import pr_400_i_joists
from materials.awc_nds import AWCNDS_materials
from materials.awc_nds import AWCNDS_limit_state_checking as nds
import os
from actions import load_cases as lcm
from actions import combinations as combs
from solution import predefined_solutions
from postprocess.config import default_config
from postprocess import limit_state_data as lsd

# Unit conversion.
gravity= 9.81 # m/s2
inchToMeter= 0.0254
psf2N_m2= 0.047880258888889e3

# Input data
def getRelativeCoo(pt):
    return [pt[0]/1000.0,pt[1]/1000.0,pt[2]/1000.0]

groupsToImport= ['LongLVLBeam.*', 'LVLBeam.*', 'ShortLVLBeam.*', 'LongJoist[0-9]*', 'Joist[0-9]*', 'Support.*', 'momentRelease.*']

freeCADFileName= 'roof_floor_joists_and_lvl_beams.FCStd'

# Finite element problem.
FEcase= xc.FEProblem()
FEcase.title= 'Second floor joists and LVL beams.'
preprocessor= FEcase.getPreprocessor
nodes= preprocessor.getNodeHandler
modelSpace= predefined_spaces.StructuralMechanics3D(nodes)

## Problem geometry
## Import geometry from FreeCAD.
modelSpace.importFromFreeCAD(fileName= freeCADFileName, groupsToImport= groupsToImport, getRelativeCoo= getRelativeCoo, threshold= 0.001)

## *********** SPLIT IMPORTED LINES. ***************
xcTotalSet= modelSpace.getTotalSet()
xcTotalSet.getEntities.splitLinesAtIntersections(1e-3)
## *********** SPLITTED! ***************

## Define sets
joistSet= preprocessor.getSets.defSet('joistSet')
longJoistSet= preprocessor.getSets.defSet('longJoistSet')
shortBeamSet= preprocessor.getSets.defSet('shortBeamSet')
beamSet= preprocessor.getSets.defSet('beamSet')
longBeamSet= preprocessor.getSets.defSet('longBeamSet')
skyLightLoadedSet= preprocessor.getSets.defSet('skyLightLoadedSet')
anchorSet= preprocessor.getSets.defSet('anchorSet')


meshSets= [joistSet, longJoistSet, shortBeamSet, beamSet, longBeamSet]

### Classify the block topology objects (points, lines, surfaces, volumes).
setsFromLabels= [('Joist.*', joistSet),('LongJoist.*', longJoistSet), ('LongLVLBeam.*', longBeamSet), ('LVLBeam.*', beamSet), ('ShortLVLBeam.*', shortBeamSet), ('Support.*', anchorSet)]
modelSpace.classifyBlockTopologyObjects(setsFromLabels)

## Define element orientation (normally this must be read from the IFC file),
## and element size.
globalZVector= geom.Vector3d(0,0,1)
elementLength= 0.5
for l in xcTotalSet.lines:
    iVector= l.getIVector
    kVector= globalZVector.cross(iVector)
    l.setProp('webOrientation', -kVector)
    l.setElemSize(elementLength)

## Template coordinate transformation.
linCT= preprocessor.getTransfCooHandler.newLinearCrdTransf3d('linCT')
linCT.xzVector= xc.Vector([1.0,0,0])

# Materials
shortBeamsSection= structural_panels.LVLHeaderSections['1.75x11-7/8']
beamsSection= structural_panels.LVLHeaderSections['5.25x11-7/8']
longBeamsSection= structural_panels.LVLHeaderSections['7x11-7/8']#'3.5x18']
longJoistsSection= pr_400_i_joists.pr400_i_joists['PRI-20_241']
joistsWood=  dl.SouthernPineWood(name='SouthernPine', grade= 'no_2', sub_grade= '')
joistsSection= AWCNDS_materials.DimensionLumberSection(name= '2x8', woodMaterial= joistsWood)

# Mesh generation.
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultTransformation= "linCT"

def createMesh(xcSet, section):
    xcSection= section.defElasticShearSection3d(preprocessor)
    seedElemHandler.defaultMaterial= section.name

    for l in xcSet.getLines:
        vDir= l.getProp('webOrientation')
        l.setProp('crossSection', section)
        linCT.xzVector= xc.Vector([vDir.x, vDir.y, vDir.z])
        elem= seedElemHandler.newElement("ElasticBeam3d",xc.ID([0,0]))
        l.genMesh(xc.meshDir.I)
    xcSet.fillDownwards()
    
## Beams.
createMesh(shortBeamSet, shortBeamsSection)
createMesh(beamSet, beamsSection)
createMesh(longBeamSet, longBeamsSection)
## Joists.
createMesh(joistSet, joistsSection)
createMesh(longJoistSet, longJoistsSection)

## Constraints
### Supports.
for p in anchorSet.getPoints:
    if(not p.hasNode):
        lmsg.warning('point: '+str(p.name)+' not meshed.')
    else:
        n= p.getNode()
        modelSpace.fixNode('000_FFF',n.tag)
        
# ## "Remove" torsional stiffness
# for e in beamSet.elements:
#     sp= e.sectionProperties
#     sp.J/=10000.0
#     e.setSectionProperties(sp)

### Pinned joints.
stiffnessFactors= [1.0e7,1.0e7,1.0e7,1e-5,1e-5,1e-5]
for l in xcTotalSet.lines:
    attributes= l.getProp('attributes')
    predefinedType=''
    if 'PredefinedType' in attributes:
        predefinedType= attributes['PredefinedType']
    else:
        print(l.getProp('labels'))
        print(attributes)
        print('Error')
    if(predefinedType=='PIN_JOINED_MEMBER'):
        modelSpace.releaseLineExtremities(l, stiffnessFactors= stiffnessFactors)

for p in xcTotalSet.points:
    attributes= p.getProp('attributes')
    if 'IfcType' in attributes:
        ifcType= attributes['IfcType']
        if(ifcType=='Structural Point Connection'):
            connectedMemberLabel= attributes['IfcDescription'] # Dirty solution indeed :(
            nearestMember, vertexIndex, minDist= reader_base.findConnectedMember(xcTotalSet.lines, connectedMemberLabel, p.getPos)
            modelSpace.releaseLineExtremities(nearestMember, stiffnessFactors= stiffnessFactors, extremitiesToRelease= [vertexIndex])

# Check for floating nodes.
floatingNodes= modelSpace.getFloatingNodes()
if(len(floatingNodes)>0):
    lmsg.error('There are '+str(len(floatingNodes))+' floating nodes. Can\'t compute solution.')
    quit()
    
# Skylight loaded set.
skyLightWidth= 1.022
skyLightLoadedLines= ['LongLVLBeam010', 'LongLVLBeam003', 'ShortLVLBeam007']


for l in xcTotalSet.lines:
    #print(l.getPropNames())
    labels= l.getProp('labels')
    for skyLL in skyLightLoadedLines:
        if skyLL in labels:
            skyLightLoadedSet.lines.append(l)

# Loads

## Define "spacing" property
spacing= 24*inchToMeter
for l in joistSet.lines:
    l.setProp('spacing', spacing)
for l in longJoistSet.lines:
    l.setProp('spacing', spacing)
for l in shortBeamSet.lines:
    l.setProp('spacing', spacing)
for l in beamSet.lines:
    l.setProp('spacing', spacing)
for l in longBeamSet.lines:
    l.setProp('spacing', spacing)

loadCaseManager= lcm.LoadCaseManager(preprocessor)
loadCaseNames= ['deadLoad', 'liveLoad', 'windLoad', 'snowLoad']
loadCaseManager.defineSimpleLoadCases(loadCaseNames)

def loadOnLines(xcSet, loadVector):
    for l in xcSet.getLines:
        spacing= l.getProp('spacing')
        for e in l.getElements:
            e.vector3dUniformLoadGlobal(spacing*loadVector)
            
def loadOnLineSets(setList, loadVector):
    for s in setList:
        loadOnLines(s, loadVector)

## Dead load.
cLC= loadCaseManager.setCurrentLoadCase('deadLoad')

# ### Self weight on elements.
gravityVector= xc.Vector([0,0,gravity])
for e in xcTotalSet.elements:
    dim= e.getDimension
    if(dim==1):
        e.createInertiaLoad(gravityVector)

### Dead load on elements.
deadL= (9.4+2.75+30)*psf2N_m2
uniformLoad= xc.Vector([0.0,0.0,-deadL])
loadedSets= [joistSet, longJoistSet, shortBeamSet, beamSet, longBeamSet]
loadOnLineSets(loadedSets,uniformLoad)
#### Skylight load.
skyLightDeadLoad= (8+30)*psf2N_m2/spacing*(skyLightWidth/2.0)
uniformLoad= xc.Vector([0.0,0.0,-skyLightDeadLoad])
loadedSets= [skyLightLoadedSet]
loadOnLineSets(loadedSets,uniformLoad)


### Live load.
cLC= loadCaseManager.setCurrentLoadCase('liveLoad')

#### Live load on elements.
liveL= (40.0+5.0)*psf2N_m2
uniformLoad= xc.Vector([0.0,0.0,-liveL])
loadedSets= [joistSet, longJoistSet, shortBeamSet, beamSet, longBeamSet]
loadOnLineSets(loadedSets,uniformLoad)
#### Skylight load.
skyLightLiveLoad= 40*psf2N_m2/spacing*(skyLightWidth/2.0)
uniformLoad= xc.Vector([0.0,0.0,-skyLightLiveLoad])
loadedSets= [skyLightLoadedSet]
loadOnLineSets(loadedSets,uniformLoad)

### Snow load.
cLC= loadCaseManager.setCurrentLoadCase('snowLoad')

#### Snow load on elements.
regularSnowLoad= 0.7*1.1*1*1*40.0*psf2N_m2
##### Sliding snow.
slidingSnowLoad= 2*2.5*0.4*regularSnowLoad/3.788
snowL= regularSnowLoad+slidingSnowLoad
uniformLoad= xc.Vector([0.0,0.0,-snowL])
loadedSets= [joistSet, longJoistSet, shortBeamSet, beamSet, longBeamSet]
loadOnLineSets(loadedSets,uniformLoad)
#### Skylight load.
skyLightSnowLoad= 40*psf2N_m2/spacing*(skyLightWidth/2.0)
uniformLoad= xc.Vector([0.0,0.0,-skyLightSnowLoad])
loadedSets= [skyLightLoadedSet]
loadOnLineSets(loadedSets,uniformLoad)

# Load combination definition
combContainer= combs.CombContainer()

## Basic load combinations according to Section 1605.3.1 of IBC.

ibcLoadCombinations= dict()
ibcLoadCombinations['EQ1608']= '1.0*deadLoad' # Equation 16-8
ibcLoadCombinations['EQ1609']= '1.0*deadLoad+1.0*liveLoad' # Equation 16-9
ibcLoadCombinations['EQ1610']= '1.0*deadLoad+1.0*snowLoad' # Equation 16-10
ibcLoadCombinations['EQ1611']= '1.0*deadLoad+0.75*liveLoad+0.75*snowLoad' # Equation 16-11
ibcLoadCombinations['EQ1612']= '1.0*deadLoad+0.6*windLoad' # Equation 16-12
ibcLoadCombinations['EQ1613']= '1.0*deadLoad+0.45*windLoad+0.75*liveLoad+0.75*snowLoad' # Equation 16-13
### Equation 16-14-> doesn't apply
ibcLoadCombinations['EQ1615']= '0.6*deadLoad+0.6*windLoad' # Equation 16-15
### Equation 16-16 -> doesn't apply

### load combinations for deflection.
deflectionLoadCombinations= dict()
deflectionLoadCombinations['dflEQ1609']= '1.0*deadLoad+1.0*liveLoad'
deflectionLoadCombinations['dflEQ1610']= '1.0*snowLoad'
deflectionLoadCombinations['dflEQ1611']= '0.75*liveLoad+0.75*snowLoad'
deflectionLoadCombinations['dflEQ1612']= '0.6*windLoad'
deflectionLoadCombinations['dflEQ1613']= '0.45*windLoad+0.75*liveLoad+0.75*snowLoad'

## Serviceability limit states.
for lcKey in deflectionLoadCombinations:
    lc= deflectionLoadCombinations[lcKey]
    combContainer.SLS.qp.add('SLS'+lcKey, lc)
    
## Ultimate limit states.
for lcKey in ibcLoadCombinations:
    lc= ibcLoadCombinations[lcKey]
    combContainer.ULS.perm.add('ULS'+lcKey, lc)

combContainer.dumpCombinations(preprocessor)

# Limit state checking.

ndsCalcSet= modelSpace.defSet('ndsCalcSet')# Elements to be checked as NDS members.
ndsMembers= list() # NDS members list.
for l in xcTotalSet.getLines:
    Lx= 0.5 # continuously braced.
    memberSection= l.getProp('crossSection')
    member= nds.Member(name= l.name, section= memberSection, unbracedLengthX= Lx, lstLines= [l])
    #member.setControlPoints()
    ndsMembers.append(member)
    
# Setup working directory.
lsd.LimitStateData.envConfig= default_config.get_temporary_env_config()
