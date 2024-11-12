# -*- coding: utf-8 -*-
''' Nonlinear soil spring model inspired in the example 14.2 of the book "Principles of Foundation Engineering" of Braja M. Das. Eight Edition. CENGAGE Learning. 2016.'''

import math
import geom
import xc
from scipy.constants import g
from geotechnics import earth_pressure
from materials import typical_materials
from model import predefined_spaces
from solution import predefined_solutions
from materials.sections.fiber_section import def_column_RC_section
from materials.ehe import EHE_materials
from materials.ehe import EHE_limit_state_checking
import excavation_process as ep
from misc_utils import log_messages as lmsg
from tabulate import tabulate

lmsg.log('WARNING: work in progress. Use with caution.')

# Define finite element problem.
feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor   
nodes= preprocessor.getNodeHandler
## Problem type
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)

# Materials definition
## Soil material
soil= earth_pressure.RankineSoil(phi= math.radians(32), rho= 15.90e3/g, rhoSat= 19.33e3/g)
soil.Kh= 30e6
### Soil strata.
L1= 5.0 #5.0 # Excavation depth (m)
Dteory= 4.7
L= L1+1.3*Dteory # Total lenght (m)
soilLayersDepths= [0.0, L1, L]
soilLayers= [soil, soil, soil]
soilStrata= ep.SoilLayers(depths= soilLayersDepths, soils= soilLayers, waterTableDepth= None)

## Pile material.
concr= EHE_materials.HA30
steel= EHE_materials.B500S
diameter= 450e-3 # Cross-section diameter [m]
pileSection= def_column_RC_section.RCCircularSection(name='test',Rext= diameter/2.0, concrType=concr, reinfSteelType= steel)
xcPileSection= pileSection.defElasticShearSection2d(preprocessor)

# Problem geometry
pileSpacing= 1.0 # One pile every meter.
lines= list()
kPoints= list()
for depth in soilLayersDepths:
    kPoints.append(modelSpace.newKPoint(0,-depth,0))
kPt0= kPoints[0]
for kPt1 in kPoints[1:]:
    newLine= modelSpace.newLine(kPt0, kPt1)
    newLine.setElemSize(0.25)
    kPt0= kPt1
    lines.append(newLine)

# Mesh generation
## Geometric transformations
lin= modelSpace.newLinearCrdTransf("lin")
## Seed element
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.dimElem= 2 # Bars defined in a two-dimensional space.
seedElemHandler.defaultMaterial= xcPileSection.name
seedElemHandler.defaultTransformation= lin.name
beam2d= seedElemHandler.newElement("ElasticBeam2d")
beam2d.h= diameter
pileSet= preprocessor.getSets.defSet('pileSet')
for ln in lines:
    ln.genMesh(xc.meshDir.I)
    pileSet.lines.append(ln)
pileSet.fillDownwards()

## Constraints.
bottomNode= kPoints[-1].getNode()
modelSpace.fixNodeF0F(bottomNode.tag) # Fix vertical displacement.

## Define nonlinear springs.

### Define soil response diagrams.
soilResponseMaterials= dict()
tributaryAreas= dict()
nodesToExcavate= list() # Nodes in the excavation depth.
#### Compute tributary lengths.
pileSet.resetTributaries()
pileSet.computeTributaryLengths(False) # Compute tributary lenghts.
#### Define non-linear springs.
for n in pileSet.nodes:
    nodeDepth= -n.getInitialPos3d.y
    if(nodeDepth<L1):
        nodesToExcavate.append((nodeDepth, n))
    nonLinearSpringMaterial= None
    tributaryArea= 0.0
    if(nodeDepth>0.0): # Avoid zero soil response.
        tributaryLength= n.getTributaryLength()
        tributaryArea= tributaryLength*pileSpacing
        materialName= 'soilResponse_z_'+str(n.tag)
        nonLinearSpringMaterial= soilStrata.defHorizontalSubgradeReactionNlMaterialAtDepth(preprocessor, name= materialName, depth= nodeDepth, tributaryArea= tributaryArea)
        
    tributaryAreas[n.tag]= tributaryArea
    soilResponseMaterials[n.tag]= nonLinearSpringMaterial

### Duplicate nodes below ground level.
springPairs= list()
for n in pileSet.nodes:
    nodeTag= n.tag
    if(nodeTag in soilResponseMaterials):
        newNode= nodes.duplicateNode(nodeTag)
        modelSpace.fixNode000(newNode.tag)
        springPairs.append((n, newNode))

### Define Spring Elements
elements= preprocessor.getElementHandler
elements.dimElem= 2 #Element dimension.
leftZLElements= dict()
rightZLElements= dict()
for i, pair in enumerate(springPairs):
    nodeTag= pair[0].tag
    soilResponseMaterial= soilResponseMaterials[nodeTag]
    if(soilResponseMaterial): # Spring defined for this node.
        # Material for the left spring
        elements.defaultMaterial= soilResponseMaterial.name
        # Springs on the left side of the beam
        zlLeft= elements.newElement("ZeroLength",xc.ID([pair[1].tag, pair[0].tag]))
        zlLeft.setupVectors(xc.Vector([-1,0,0]),xc.Vector([0,-1,0]))
        leftZLElements[nodeTag]= zlLeft
        
        # Springs on the right side of the beam
        zlRight= elements.newElement("ZeroLength",xc.ID([pair[0].tag, pair[1].tag]))
        zlRight.setupVectors(xc.Vector([1,0,0]),xc.Vector([0,1,0]))
        rightZLElements[nodeTag]= zlRight


# Solve 
numSteps= 10
#solProc= predefined_solutions.PenaltyKrylovNewton(prb= feProblem, numSteps= numSteps, maxNumIter= 300, convergenceTestTol= 1e-6, printFlag= 0)
solProc= predefined_solutions.PenaltyNewtonRaphson(prb= feProblem, numSteps= numSteps, maxNumIter= 300, convergenceTestTol= 1e-5, printFlag= 0)
ok= solProc.solve()
if(ok!=0):
    lmsg.error('Can\'t solve')
    exit(1)

reactionCheckTolerance= 1e-6
updatedElements= ep.excavation_process(preprocessor= preprocessor, solProc= solProc, nodesToExcavate= nodesToExcavate, elementsOnExcavationSide= leftZLElements, maxDepth= 5.0, tributaryAreas= tributaryAreas, soil= soil)
modelSpace.calculateNodalReactions(reactionCheckTolerance= reactionCheckTolerance)

finalResults= ep.get_results_dict(soil= soil, tributaryAreas= tributaryAreas, springPairs= springPairs, pileWallElements= pileSet.lines)
outputTable= ep.get_results_table(resultsDict= finalResults)

# Compute maximum bending moment.
MMin= 6.023e23
MMax= -MMin
for nodeTag in finalResults:
    nodeResults= finalResults[nodeTag]
    depth= nodeResults['depth']
    M= nodeResults['M']
    MMin= min(MMin, M)
    MMax= max(MMax, M)
    
refValue= -212.0886594633984e3
err= abs(max(abs(MMax), abs(MMin))+refValue)/refValue

import os
fname= os.path.basename(__file__)
content= tabulate(outputTable, headers= 'firstrow', tablefmt="tsv")
print('\nASCII output:')
print(content)
csvFileName= fname.replace(".py", ".csv")
with open(csvFileName, "w") as csvFile:
    csvFile.write(content)
print('MMax= ', MMax/1e3, 'kN.m')
print('MMin= ', MMin/1e3, 'kN.m')
print('err= ', err)
'''
'''

from misc_utils import log_messages as lmsg
if abs(err)<.05:
    print('test: '+fname+': ok.')
else:
    lmsg.error('test: '+fname+' ERROR.')

# Matplotlib output.
# ep.plot_results(resultsDict= finalResults, title= 'Based on the example 14.2 of the book "Principles of Foundation Engineering" of Braja M. Das.')

# # VTK Graphic output.
# from postprocess import output_handler
# oh= output_handler.OutputHandler(modelSpace)
# # oh.displayFEMesh(setsToDisplay= [pileSet])
# #oh.displayLocalAxes()
# #oh.displayLoads()
# oh.displayReactions(reactionCheckTolerance= reactionCheckTolerance)
# oh.displayDispRot('uX', defFScale= 10.0)
# oh.displayIntForcDiag('M')
# oh.displayIntForcDiag('V')
