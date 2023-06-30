# -*- coding: utf-8 -*-
''' Slope stability analysis from Griffiths and Lane (1999) paper.

Example 1: Homogeneous slope with no foundation layer (D=1) # ref: Griffiths, D. V. and Lane P. A. (1999). Slope stability analysis by Finite elements Geotechnique 49, No. 3, 387-403.

Somewhat inspired on the code from: https://gitlab.com/geosharma/opensees-examples/-/blob/master/geotech/2d_slope_stability_griffiths/ex1/src/2d_slopestability_griffiths_lane_1999_ex1.py
'''

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AO_O)"
__copyright__= "Copyright 2023, LCPT and AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es ana.ortega@ciccp.es"

from scipy.constants import g
import math
import xc
import geom
from model import predefined_spaces
from geotechnics import frictional_cohesive_soil as fcs
from actions import loads
from solution import predefined_solutions

# Geometry of the slope.
H= 10 # Height of the slope.
b= 1.2*H # Width of the top surface.
B= b+2*H # Width of the bottom surface.
slope= math.pi/2.0-math.atan2(B-b,H)

# Safety factor
safetyFactor= 1.432
elasticMaterial= False
# Soil properties.
E= 1e8 # Pa
nu= 0.30
phi= math.atan(math.tan(math.radians(20))/safetyFactor) # Effective internal friction angle of the soil.
gamma= 20e3 # N/m3 soil unit weight.
rho= gamma/g # kg/m3 soil density.
c= 0.05*gamma*H/safetyFactor # Effective cohesion N/m2
soil= fcs.FrictionalCohesiveSoil(phi= phi, c= c, rho= rho, E= E, nu= nu) 

# Finite element problem.
## Problem type
feProblem= xc.FEProblem()
preprocessor= feProblem.getPreprocessor
nodes= preprocessor.getNodeHandler
modelSpace= predefined_spaces.SolidMechanics2D(nodes)

## Problem geometry.
### K-points.
points= preprocessor.getMultiBlockTopology.getPoints
pt1= points.newPoint(geom.Pos3d(0,0,0))
pt2= points.newPoint(geom.Pos3d(B,0,0))
pt3= points.newPoint(geom.Pos3d(b,H,0))
pt4= points.newPoint(geom.Pos3d(0,H,0))
### Surface.
surfaces= preprocessor.getMultiBlockTopology.getSurfaces
s1= surfaces.newQuadSurfacePts(pt1.tag,pt2.tag,pt3.tag,pt4.tag)
s1.setElemSizeIJ(0.5,0.5) # Element size in (pt1->pt2,pt2->pt3) directions

## Define material.
#---failure surface and associativity
rhoBar= 0.0 # related to dilation? controls evolution of plastic volume change, 0 ≤ rhoBar ≤ rho
#---isotropic hardening
Kinf= 0.0 # isotropic hardening Kinf ≥ 0.
Ko= 0.0 # nonlinear isotropic strain hardening parameter, Ko ≥ 0.
delta1= 0.0 #
#---kinematic hardening
hard= 0.0 # linear strain hardening parameter, hard ≥ 0
theta= 0.0 # controls relative proportions of isotropic and kinematic hardening, 0 ≤ theta ≤ 1 
#---tension softening
delta2= 0.0
referencePressure= 101.325e3 # reference pressure (1 atm).
if(elasticMaterial):
    material= soil.getElasticIsotropicMaterialPlaneStrain(preprocessor, name= 'ElasticTest')
else:
    material= druckerPragerMaterial= soil.getDruckerPragerMaterialPlaneStrain(preprocessor, name= 'Drucker-PragerTest', rhoBar= rhoBar, Kinf= Kinf, Ko= Ko, delta1= delta1, H= hard, theta= theta, delta2= delta2, elastFlag= 2, pAtm= referencePressure)
    
## Mesh generation.
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial= material.name
elem= seedElemHandler.newElement("FourNodeQuad",xc.ID([0,0,0,0]))
s1.genMesh(xc.meshDir.I)

## Constraints.
### Populate nodes to constraint.
leftSideNodes= list()
bottomSideNodes= list()
for side in s1.getSides: # iterate through surface sides.
    p= side.getEdge.getCentroid()
    if(abs(p.y)<1e-3):
        for n in side.getEdge.nodes:
            bottomSideNodes.append(n)
    if(abs(p.x)<1e-3):
        for n in side.getEdge.nodes:
            leftSideNodes.append(n)
### Remove corner node from leftSideNodes.
cornerNode= pt1.getNode()
nodeToRemove= None
for n in leftSideNodes:
    if(n.tag==cornerNode.tag):
        nodeToRemove= n
leftSideNodes.remove(nodeToRemove)
### Fix nodes on bottom side.
for n in bottomSideNodes:
    modelSpace.fixNode('00', n.tag)
### Roller for nodes on left side.
for n in leftSideNodes:
    modelSpace.fixNode('0F', n.tag)

## Define loads.
#### Create path time series TS1.
ts= modelSpace.newTimeSeries(name= 'ts', tsType= "path_time_ts")
ts.path= xc.Vector([0, 1])
ts.time= xc.Vector([0, 100])

lp0= modelSpace.newLoadPattern(name= '0')
modelSpace.setCurrentLoadPattern(lp0.name)
accel= xc.Vector([0,g])
for e in s1.elements:
    e.createInertiaLoad(accel)
modelSpace.addLoadCaseToDomain(lp0.name)

## Solution.
# Static analysis.
#solProc= predefined_solutions.PlainKrylovNewton(feProblem, convergenceTestTol= 1e-3, convTestType= 'norm_disp_incr_conv_test', maxNumIter= 50, printFlag= 1)
solProc= predefined_solutions.PlainKrylovNewton(feProblem, convergenceTestTol= 1e-3, convTestType= 'norm_unbalance_conv_test', maxNumIter= 50, printFlag= 1)
solProc.setup()
solProc.integrator.dLambda1= 1
result= solProc.analysis.analyze(100)

# Compute maximum nodal displacement.
deltaMax= 0.0
for n in s1.nodes:
    deltaMax= max(deltaMax, n.getDisp.Norm2())
deltaMax= math.sqrt(deltaMax)
# Compute dimensionless displacement.
dimensionlessDisplacement= E/gamma/H**2*deltaMax

# Compute reactions.
modelSpace.calculateNodalReactions(True, 1e-4)
Ry= 0.0
## Fix nodes on bottom side.
for n in bottomSideNodes:
    Ry+= n.getReaction[1]
## Roller for nodes on left side.
for n in leftSideNodes:
    Ry+= n.getReaction[1]
totalWeight= gamma*s1.getArea()
errorInReaction= abs(Ry-totalWeight)/totalWeight


print('Problem geometry: ')
print('  Height of the slope: ', str(H)+' m')
print('  Angle of the slope: ', str(math.degrees(slope))+'º')
print('\nSoil parameters: ')
print('  Soil unit weight: ', str(gamma/1e3)+' kN/m3')
print('  Effective internal friction angle: ', str(math.degrees(phi))+'º')
print('  Effective cohesion: ', str(c/1e3)+' kN')
print('\nResults: ')
print('  Safety factor: ', str(safetyFactor))
print('  Maximum displacement: ', str(deltaMax*1e3)+' mm')
print('  Dimensionless displacement: ', str(dimensionlessDisplacement))
print('  Vertical reaction: ', str(Ry/1e3)+' kN')
print('  Error in reaction: ', errorInReaction)

#Graphic stuff.
from postprocess import output_handler
oh= output_handler.OutputHandler(modelSpace)

#oh.displayBlocks()#setToDisplay= )
# oh.displayFEMesh()#setsToDisplay=[])
# oh.displayLocalAxes()
# oh.displayLoads()
# oh.displayReactions()
oh.displayDispRot(itemToDisp='uX', defFScale= 150.0)
oh.displayDispRot(itemToDisp='uY', defFScale= 150.0)
# oh.displayStresses('sigma_yy')
# oh.displayVonMisesStresses()
if(not elasticMaterial):
    #oh.displayState(itemToDisp= 'invariant_ep') # itemToDisp: invariant_1, norm_eta, invariant_ep, norm_dev_ep, norm_ep
    #oh.displayState(itemToDisp= 'norm_ep')
    oh.displayState(itemToDisp= 'norm_dev_ep')
