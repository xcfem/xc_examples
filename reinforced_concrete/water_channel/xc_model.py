# -*- coding: utf-8 -*-
''' Design of the channel section.'''

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2022, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

# Problem geometry.
wallThickness= 0.3
channelWidth= 3-wallThickness
channelHeight= 2.3-wallThickness/2.0

import math
import geom
import xc
from model import predefined_spaces
from materials.ec2 import EC2_materials
from materials.sections.fiber_section import def_simple_RC_section
from postprocess import RC_material_distribution
from model.boundary_cond import spring_bound_cond as springs
from actions import load_cases as lcm
from scipy.constants import g
from geotechnics import earth_pressure as ep
from actions.earth_pressure import earth_pressure
from postprocess.config import default_config
from solution import predefined_solutions


# Working directory setup
cfg= default_config.EnvConfig(fNameMark= 'xc_model.py')

# Problem type.
feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor
nodes= preprocessor.getNodeHandler
solProc= predefined_solutions.PlainNewtonRaphsonBandGen(feProblem, maxNumIter= 100, convergenceTestTol= 1e-2, printFlag= 0)
solProc.setup()
modelSpace= predefined_spaces.StructuralMechanics2D(nodes, solProcType= None)
modelSpace.analysis= solProc.analysis

# Problem geometry.
# 
# p0          p3
#   +        + 
#   |        |
#   |        |
#   |        |
#   +--------+
# p1         p2
#

p0= modelSpace.newKPoint(-channelWidth/2.0, 2.3, 0.0)
p1= modelSpace.newKPoint(-channelWidth/2.0, 0.0, 0.0)
p2= modelSpace.newKPoint(channelWidth/2.0, 0.0, 0.0)
p3= modelSpace.newKPoint(channelWidth/2.0, 2.3, 0.0)

l1= modelSpace.newLine(p1,p0)
l2= modelSpace.newLine(p1,p2)
l3= modelSpace.newLine(p2,p3)

# Materials.
## Materials.
concrete= EC2_materials.C30
steel= EC2_materials.S500B

## Reinforcement row scheme:
#
#    |  o    o    o    o    o    o    o    o    o    o  |
#    <->           <-->                               <-> 
#    lateral      spacing                           lateral
#     cover                                          cover
#

## Geometry of the reinforcement.
rebarSpacing= 0.15 # spacing of reinforcement.
concreteCover= 0.040 # concrete cover.
lateralCover= 0.0 # concrete cover for the bars at the extremities of the row.
rcSectionWidth= 1.0
### Reinforcement row.
barDiameter= 8e-3 # Diameter of the reinforcement bar.
rowA= def_simple_RC_section.ReinfRow(rebarsDiam= barDiameter, rebarsSpacing= rebarSpacing, width= rcSectionWidth, nominalCover= concreteCover, nominalLatCover= lateralCover)

## RC section.
rcSection= def_simple_RC_section.RCRectangularSection(name='ChannelRCSection', width= 1.0, depth= wallThickness, concrType= concrete, reinfSteelType= steel)
xcSection= rcSection.defElasticShearSection2d(preprocessor)
## Backfill soil.
backfillSoilModel= ep.RankineSoil(phi= math.radians(30),rho= 2e3) #Characteristic values.

# Generate mesh.
## Geometric transformations
lin= modelSpace.newLinearCrdTransf("lin")
## Seed element.
seedElemHandler= modelSpace.getElementHandler().seedElemHandler
seedElemHandler.defaultTransformation= lin.name
seedElemHandler.defaultMaterial= xcSection.name
beam2d= seedElemHandler.newElement("ElasticBeam2d",xc.ID([0,0]))
beam2d.h= wallThickness
## Generate mesh.
for l in [l1, l2, l3]:
    l.nDiv= 10
    l.genMesh(xc.meshDir.I)

# Elastic foundation.
## Set the soil parameters.
wModulus= 10e6 # N/m3 Winkler modulus.
cRoz= 2/3.0*math.tan(math.radians(25)) # Foundation base-soil friction coefficient
elasticFoundation= springs.ElasticFoundation(wModulus= 10e6, cRoz= cRoz,noTensionZ=True)
## Generate springs.
elasticFoundation.generateSprings(l2)


# Define reinforcement
## Store element reinforcement properties. Assign to each element the properties
# that will be used to define its reinforcement on each direction:
#
# - baseSection: RCSectionBase derived object containing the geometry
#                and the material properties of the reinforcec concrete
#                section.
# - reinforcementUpVector: reinforcement "up" direction which defines
#                          the position of the positive reinforcement
#                          (bottom) and the negative reinforcement
#                          (up).
# - bottomReinforcement: LongReinfLayers objects defining the 
#                        reinforcement at the bottom of the section.
# - topReinforcement: LongReinfLayers objects defining the 
#                     reinforcement at the top of the section.
# - shearReinforcement: ShearReinforcement objects defining the 
#                       reinforcement at the bottom of the section.
reinforcementUpVector= geom.Vector3d(-1,0,0) # X-. This vector defines the
                                             # meaning of "top reinforcement"
                                             # or "bottom reinforcement".
for e in l1.elements:
    e.setProp("baseSection", rcSection)
    e.setProp("reinforcementUpVector", reinforcementUpVector) # Y+
    e.setProp("bottomReinforcement", def_simple_RC_section.LongReinfLayers([rowA]))
    e.setProp("topReinforcement", def_simple_RC_section.LongReinfLayers([rowA]))
    
reinforcementUpVector= geom.Vector3d(1,0,0) # X+. This vector defines the
                                            # meaning of "top reinforcement"
                                            # or "bottom reinforcement".
for e in l3.elements:
    e.setProp("baseSection", rcSection)
    e.setProp("reinforcementUpVector", reinforcementUpVector) # Y+
    e.setProp("bottomReinforcement", def_simple_RC_section.LongReinfLayers([rowA]))
    e.setProp("topReinforcement", def_simple_RC_section.LongReinfLayers([rowA]))
    
reinforcementUpVector= geom.Vector3d(0,1,0) # Y+. This vector defines the
                                            # meaning of "top reinforcement"
                                            # or "bottom reinforcement".
for e in l2.elements:
    e.setProp("baseSection", rcSection)
    e.setProp("reinforcementUpVector", reinforcementUpVector) # Y+
    e.setProp("bottomReinforcement", def_simple_RC_section.LongReinfLayers([rowA]))
    e.setProp("topReinforcement", def_simple_RC_section.LongReinfLayers([rowA]))


# Define sets.
xcTotalSet= modelSpace.getTotalSet()
concreteSet= modelSpace.defSet('concreteSet')
for l in xcTotalSet.lines:
    concreteSet.lines.append(l)
concreteSet.fillDownwards()

# Define sections.
## Define spatial distribution of reinforced concrete sections.
reinfConcreteSectionDistribution= RC_material_distribution.RCMaterialDistribution()
reinfConcreteSectionDistribution.assignFromElementProperties(elemSet= concreteSet.getElements)
reinfConcreteSectionDistribution.dump()
# Ends model reinforcement

## Define loads.
### Loads cases.
loadCaseManager= lcm.LoadCaseManager(modelSpace.preprocessor)
loadCaseNames= list()
loadCaseNames.append('G') # Self weight.
loadCaseNames.append('W') # Water pressure.
loadCaseNames.append('E') # Earth pressure.
loadCaseNames.append('T') # Traffic load.

loadCaseManager.defineSimpleLoadCases(loadCaseNames) 
### Load values.
gravityVector= xc.Vector([0.0,g])

#### Self weight.
cLC= loadCaseManager.setCurrentLoadCase('G')
cLC.description= 'Peso propio.'
modelSpace.createSelfWeightLoad(concreteSet,gravityVector)

#### Water pressure.
cLC= loadCaseManager.setCurrentLoadCase('W')
cLC.description= 'Presión hidrostática.'
for e in l1.elements:
    centroid= e.getPosCentroid(True)
    y= centroid.y
    depth= channelHeight-y
    pressure= 1e3*g*depth
    e.vector2dUniformLoadGlobal(xc.Vector([pressure,0]))
for e in l2.elements:
    centroid= e.getPosCentroid(True)
    y= centroid.y
    depth= channelHeight-y
    weight= 1e3*g*depth
    e.vector2dUniformLoadGlobal(xc.Vector([0,-weight]))
for e in l3.elements:
    centroid= e.getPosCentroid(True)
    y= centroid.y
    depth= channelHeight-y
    pressure= 1e3*g*depth
    e.vector2dUniformLoadGlobal(xc.Vector([-pressure,0]))

#### Earth pressure.
cLC= loadCaseManager.setCurrentLoadCase('E')
cLC.description= 'Empuje de tierras.'
gSoil= backfillSoilModel.rho*g
K0= backfillSoilModel.K0Jaky() # pressure at rest.
backfillPressureModel= earth_pressure.EarthPressureModel(zGround= channelHeight, zBottomSoils=[-1e3], KSoils= [K0], gammaSoils= [gSoil], zWater= -1e3, gammaWater= 1000*g, qUnif=0)
##### On left wall.
backfillPressureModel.vDir= xc.Vector([-1,0])
backfillPressureModel.xcSet= l1
backfillPressureModel.appendLoadToCurrentLoadPattern(iCoo= 1, delta= 0)
##### On right wall.
backfillPressureModel.vDir= xc.Vector([1,0])
backfillPressureModel.xcSet= l3
backfillPressureModel.appendLoadToCurrentLoadPattern(iCoo= 1, delta= 0)

#### Traffic load.
cLC= loadCaseManager.setCurrentLoadCase('T')
cLC.description= 'Sobrecarga de tráfico.'
q= 10e3 # 10 kN/m2
for e in l3.elements:
    e.vector2dUniformLoadGlobal(xc.Vector([-q,0]))

# Load combinations
import load_combinations.channel_load_combinations
combContainer= load_combinations.channel_load_combinations.combContainer


# Graphic stuff.
from postprocess import output_handler
oh= output_handler.OutputHandler(modelSpace)

#oh.displayBlocks()#setToDisplay= deckSlabSet)
#oh.displayFEMesh()#setsToDisplay= [southSideWallSet])
#oh.displayDispRot(itemToDisp='uX',defFScale= 10.0,setToDisplay=dispSet)
#oh.displayLoads(setToDisplay= structureSet)
#oh.displayDispRot(itemToDisp='uZ',defFScale= 1000.0, setToDisplay= structureSet)

