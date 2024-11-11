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
## Pile material.
concr= EHE_materials.HA30
steel= EHE_materials.B500S
diameter= 450e-3 # Cross-section diameter [m]
cover= 0.07 # Cover [m]
pileSection= def_column_RC_section.RCCircularSection(name='test',Rext= diameter/2.0, concrType=concr, reinfSteelType= steel)
xcPileSection= pileSection.defElasticShearSection2d(preprocessor)

# Problem geometry
pileSpacing= 1.0 # One pile every meter.
L1= 5.0 #5.0 # Excavation depth (m)
Dteory= 4.7
L= L1+1.3*Dteory # Total lenght (m)
points= preprocessor.getMultiBlockTopology.getPoints
pt1= points.newPoint(geom.Pos3d(0,0,0))
pt2= points.newPoint(geom.Pos3d(0,-L,0))
lines= preprocessor.getMultiBlockTopology.getLines
ln= lines.newLine(pt1.tag, pt2.tag)
ln.setElemSize(0.25)

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
ln.genMesh(xc.meshDir.I)

## Constraints.
modelSpace.fixNodeF0F(pt2.getNode().tag) # Fix vertical displacement.

## Define nonlinear springs.
Kh= 30e6

### Define soil response diagrams.
soilResponseMaterials= dict()
tributaryAreas= dict()
nodesToExcavate= list() # Nodes in the excavation depth.
ln.resetTributaries()
ln.computeTributaryLengths(False) # Compute tributary lenghts.
for n in ln.nodes:
    nodeDepth= -n.getInitialPos3d.y
    if(nodeDepth<L1):
        nodesToExcavate.append((nodeDepth, n))
    nonLinearSpringMaterial= None
    tributaryArea= 0.0
    if(nodeDepth>0.0): # Avoid zero soil response.
        tributaryLength= n.getTributaryLength()
        tributaryArea= tributaryLength*pileSpacing
        materialName= 'soilResponse_z_'+str(n.tag)
        nonLinearSpringMaterial= soil.defHorizontalSubgradeReactionNlMaterial(preprocessor, name= materialName, depth= nodeDepth, tributaryArea= tributaryArea, Kh= Kh)
        
        #print('node: ', n.tag, ' node depth: ', '{:.2f}'.format(nodeDepth), ' tributary area: ',  '{:.2f}'.format(tributaryArea), 'init strain: ', initStrain)
    tributaryAreas[n.tag]= tributaryArea
    soilResponseMaterials[n.tag]= nonLinearSpringMaterial

pileSet= preprocessor.getSets.defSet('pileSet')
for e in ln.elements:
    pileSet.getElements.append(e)

# Sort nodes to excavate on depth.

### Duplicate nodes below ground level.
springPairs= list()
for n in ln.nodes:
    newNode= nodes.duplicateNode(n.tag)
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

numSteps= 10

# Solve 
#solProc= predefined_solutions.PenaltyKrylovNewton(prb= feProblem, numSteps= numSteps, maxNumIter= 300, convergenceTestTol= 1e-6, printFlag= 0)
solProc= predefined_solutions.PenaltyNewtonRaphson(prb= feProblem, numSteps= numSteps, maxNumIter= 300, convergenceTestTol= 1e-5, printFlag= 0)
ok= solProc.solve()
if(ok!=0):
    lmsg.error('Can\'t solve')
    exit(1)

reactionCheckTolerance= 1e-6
updatedElements= ep.excavation_process(preprocessor= preprocessor, solProc= solProc, nodesToExcavate= nodesToExcavate, elementsOnExcavationSide= leftZLElements, maxDepth= 5.0, tributaryAreas= tributaryAreas, soil= soil, Kh= Kh)
modelSpace.calculateNodalReactions(reactionCheckTolerance= reactionCheckTolerance)

finalResults= ep.get_results_dict(soil= soil, tributaryAreas= tributaryAreas, springPairs= springPairs, pileWallElements= [ln])
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

'''
print('\nASCII output:')
print(tabulate(outputTable, headers= 'firstrow'))
print('MMax= ', MMax/1e3, 'kN.m')
print('MMin= ', MMin/1e3, 'kN.m')
print('err= ', err)
'''

import os
from misc_utils import log_messages as lmsg
fname= os.path.basename(__file__)
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
