# -*- coding: utf-8 -*-

import math
import geom
import xc
from materials import typical_materials
from model import predefined_spaces
from solution import predefined_solutions

# Created by Amin Rahmani, Ph.D., P.E. - July 14, 2019
# Copyright © 2019 Amin Rahmani. All rights reserved.

#========================================================================================
#                               ****   Notes  ****
# This code performs STATIC lateral soil-beam interaction analysis using p-y springs. The code can be used for both soil-pile and soil-wall interaction evaluations. 
# The "uniaxialMaterial ENT" was used in this model to enable the end-user to define different backnone curves on left and right sides of a retaining wall.
# You need to makes changes on the lines that the comment "User-Defined" appears. Please go through all the command lines before running it.
# Units are Imperial (lbf, ft, sec).  
# Outputs will be saved in a folder titled "Outputs".
# p-y springs below the ground level will be generated at every #zSize (typically 2 ft) depth of the proposed pile.
#========================================================================================
#http://geotechsimulation.com/2019/07/21/beam-on-nonlinear-winkler-foundation-bnwf-model-for-soil-pile-and-soil-wall-interaction-analyses/

#### Definition of Global Directions
####################################
### Dir Z: Starts at ground surface and extends downward below ground
### Dir X: To the left side
### Dir Y: Perpendicular to the plane of the paper

#######################################################################
#### Input parameters used for creating the geometry of soil-pile model 
#######################################################################
gravX= 0.0000
gravY= 0.0000
gravZ=  32.2 # gravity in direction Z. The value would be +9.81 if metric units are used.

#### Pile length                                  
LP= 60.0 # User-defined --- Total pile length (from top to tip of the pile)
LP_emb= 50.0 # User-defined --- embedded pile length below the ground surface.\
	     # \in soil-wall analysis this length would be the embedded depth of pile below the excavation bottom
             # \in front face of the wall.

#### Pile element size
elemSize= 2.0 # User-Defined 

numZele_emb= math.ceil(LP_emb/elemSize)

if(LP_emb == LP):
    numZele_above_grade= 0 # number of elements in z  direction    direction
else:
    numZele_above_grade= math.ceil((LP-LP_emb)/elemSize)

# Define finite element problem.
feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor   
nodes= preprocessor.getNodeHandler
## Problem type
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)

# Materials definition
### Pile section dimensions
D= 3.0 # User-Defined --- Pile Cross section diameter
t= 0.042 # User-Defined --- Pile Cross section wall thickness
A= 0.25*math.pi*pow(D,2)-0.25*math.pi*pow(D-2.0*t,2) 	      # User-Defined
sry= 2.42 # Shear coefficient.
Ay= A/sry
I= 0.25*math.pi*pow(D/2.0,4)-0.25*math.pi*pow(D/2.0-t,4) # User-Defined 
E= 4176.0e+6 # User-Defined --- Pile material elastic modulus
G= E/2.0/(1+0.20)
h= 2.0*math.sqrt(A/math.pi) # Beam cross-section depth.
scc= typical_materials.defElasticShearSection2d(preprocessor, "scc",A,E,G,I,alpha= Ay/A)

# Problem geometry
points= preprocessor.getMultiBlockTopology.getPoints
if(LP>LP_emb):
    pt0= points.newPoint(geom.Pos3d(0,LP-LP_emb,0))
pt1= points.newPoint(geom.Pos3d(0,0,0))
pt2= points.newPoint(geom.Pos3d(0,-LP_emb,0))

### Define line below ground level
linesToMesh= list()
lines= preprocessor.getMultiBlockTopology.getLines
lBelow= lines.newLine(pt1.tag,pt2.tag)
lBelow.setElemSize(elemSize)
linesToMesh.append(lBelow)

### Define line above ground level
if(LP>LP_emb):
    lAbove= lines.newLine(pt0.tag,pt1.tag)
    linesToMesh.append(lAbove)

# Mesh generation

## Geometric transformations
lin= modelSpace.newLinearCrdTransf("lin")

## Seed element
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.dimElem= 2 # Bars defined in a two-dimensional space.
seedElemHandler.defaultMaterial= scc.name
seedElemHandler.defaultTransformation= lin.name
beam2d= seedElemHandler.newElement("ElasticBeam2d",xc.ID([0,0]))
beam2d.h= h

for l in linesToMesh:
    l.genMesh(xc.meshDir.I)

# Define Spring Nodes Below Ground Level
springPairs= list()
for n in lBelow.nodes:
    newNode= nodes.duplicateNode(n.tag)
    modelSpace.fixNode000(newNode.tag)
    springPairs.append((n, newNode))


# Define Spring Materials

##### Dummy Rigid Spring With Zero Tension
##########################################

E_Spring= 1.0e+22  # Rigid Dummy Spring

# uniaxialMaterial ENT 1000 E_Spring
rigidDummySpring= typical_materials.defElastNoTensMaterial(preprocessor, "rigidDummySpring",E_Spring)

# P-Y Springs Left Side of Beam

#### User-Defined --- Imported from LPile Program --- Must start from 2001 (ground surface) ---- Number of elements should be the same as "Num_Springs"
#### At the ground surface, do not use 0.0 force values. Use very small number such as 0.0001 lbf instead. For example "uniaxialMaterial MultiLinear	1001	0.02	0.0001	0.04	0.0001	0.08	0.0001	0.25	0.0001"
leftSpringsMaterials= dict()
leftSpringsMaterials[1001]= typical_materials.defMultiLinearMaterial(preprocessor, name="1001",points= [(0.02, 0.0001), (0.05, 0.0001), (0.1, 0.0001), (0.270833333, 0.0001)	])
leftSpringsMaterials[1002]= typical_materials.defMultiLinearMaterial(preprocessor, name="1002",points= [(0.02, 3923), (0.05, 5377), (0.1, 5598), (0.270833333, 5597.920139)])
leftSpringsMaterials[1003]= typical_materials.defMultiLinearMaterial(preprocessor, name="1003",points= [(0.02, 7977), (0.05, 11064), (0.1, 11612), (0.270833333, 11611.62039)])
leftSpringsMaterials[1004]= typical_materials.defMultiLinearMaterial(preprocessor, name="1004",points= [(0.02, 11426), (0.05, 15200), (0.1, 15698), (0.270833333, 15698.39805)])
leftSpringsMaterials[1005]= typical_materials.defMultiLinearMaterial(preprocessor, name="1005",points= [(0.02, 13527), (0.05, 15957), (0.1, 16100), (0.270833333, 16100.41376)])
leftSpringsMaterials[1006]= typical_materials.defMultiLinearMaterial(preprocessor, name="1006",points= [(0.02, 29728), (0.05, 31899), (0.1, 42994), (0.270833333, 42993.79511)])
leftSpringsMaterials[1007]= typical_materials.defMultiLinearMaterial(preprocessor, name="1007",points= [(0.02, 58011), (0.05, 62499), (0.1, 82527), (0.270833333, 82526.86196)])
leftSpringsMaterials[1008]= typical_materials.defMultiLinearMaterial(preprocessor, name="1008",points= [(0.02, 74906), (0.05, 84375), (0.1, 96281), (0.270833333, 96281.33744)])
leftSpringsMaterials[1009]= typical_materials.defMultiLinearMaterial(preprocessor, name="1009",points= [(0.02, 92965), (0.05, 109128), (0.1, 110025), (0.270833333, 110025.0984)])
leftSpringsMaterials[1010]= typical_materials.defMultiLinearMaterial(preprocessor, name="1010",points= [(0.02, 111235), (0.05, 136510), (0.1, 138589), (0.270833333, 138589.1717)])
leftSpringsMaterials[1011]= typical_materials.defMultiLinearMaterial(preprocessor, name="1011",points= [(0.02, 128739), (0.05, 166233), (0.1, 170379), (0.270833333, 170379.0124)])
leftSpringsMaterials[1012]= typical_materials.defMultiLinearMaterial(preprocessor, name="1012",points= [(0.02, 147257), (0.05, 198279), (0.1, 205383), (0.270833333, 205383.3682)])
leftSpringsMaterials[1013]= typical_materials.defMultiLinearMaterial(preprocessor, name="1013",points= [(0.02, 166789), (0.05, 231777), (0.1, 243587), (0.270833333, 243586.7862)])
leftSpringsMaterials[1014]= typical_materials.defMultiLinearMaterial(preprocessor, name="1014",points= [(0.02, 187024), (0.05, 266779), (0.1, 284966), (0.270833333, 284965.704)])
leftSpringsMaterials[1015]= typical_materials.defMultiLinearMaterial(preprocessor, name="1015",points= [(0.02, 204049), (0.05, 304175), (0.1, 329459), (0.270833333, 329458.9062)])
leftSpringsMaterials[1016]= typical_materials.defMultiLinearMaterial(preprocessor, name="1016",points= [(0.02, 220859), (0.05, 341242), (0.1, 377034), (0.270833333, 377033.8792)])
leftSpringsMaterials[1017]= typical_materials.defMultiLinearMaterial(preprocessor, name="1017",points= [(0.02, 237964), (0.05, 378447), (0.1, 427654), (0.270833333, 427653.8222)])
leftSpringsMaterials[1018]= typical_materials.defMultiLinearMaterial(preprocessor, name="1018",points= [(0.02, 255365), (0.05, 417450), (0.1, 481137), (0.270833333, 481137.0883)])
leftSpringsMaterials[1019]= typical_materials.defMultiLinearMaterial(preprocessor, name="1019",points= [(0.02, 273062), (0.05, 458250), (0.1, 537513), (0.270833333, 537513.3165)])
leftSpringsMaterials[1020]= typical_materials.defMultiLinearMaterial(preprocessor, name="1020",points= [(0.02, 291055), (0.05, 500847), (0.1, 596823), (0.270833333, 596823.3453)])
leftSpringsMaterials[1021]= typical_materials.defMultiLinearMaterial(preprocessor, name="1021",points= [(0.02, 309344), (0.05, 540243), (0.1, 658217), (0.270833333, 658217.4493)])
leftSpringsMaterials[1022]= typical_materials.defMultiLinearMaterial(preprocessor, name="1022",points= [(0.02, 327930), (0.05, 577936), (0.1, 722599), (0.270833333, 722599.3883)])
leftSpringsMaterials[1023]= typical_materials.defMultiLinearMaterial(preprocessor, name="1023",points= [(0.02, 346810.77), (0.05, 616642.04), (0.1, 789806.5), (0.27, 789806.5)])
leftSpringsMaterials[1024]= typical_materials.defMultiLinearMaterial(preprocessor, name="1024",points= [(0.02, 365988.01), (0.05, 656362.49), (0.1, 858021.68), (0.27, 858021.68)])
leftSpringsMaterials[1025]= typical_materials.defMultiLinearMaterial(preprocessor, name="1025",points= [(0.02, 385461.29), (0.05, 697096.92), (0.1, 928656.37), (0.27, 928656.37)])
leftSpringsMaterials[1026]= typical_materials.defMultiLinearMaterial(preprocessor, name="1026",points= [(0.02, 202615.29), (0.05, 369422.67), (0.1, 501030.94), (0.27, 501030.94)])

##### P-Y Springs Right Side of Beam
###########################################

#### User-Defined --- Imported from LPile Program --- Must start from 2001 (ground surface)  ---- Number of elements should be the same as "Num_Springs"
#### At the ground surface, do not use 0.0 force values. Use very small number such as 0.0001 lbf instead. For example "uniaxialMaterial MultiLinear	1001	0.02	0.0001	0.04	0.0001	0.08	0.0001	0.25	0.0001"
rightSpringsMaterials= dict()
rightSpringsMaterials[2001]= typical_materials.defMultiLinearMaterial(preprocessor, name="2001",points= [(0.02, 0.0001), (0.05, 0.0001), (0.1, 0.0001), (0.27, 0.0001)])
rightSpringsMaterials[2002]= typical_materials.defMultiLinearMaterial(preprocessor, name="2002",points= [(0.02, 3923.32), (0.05, 5377.45), (0.1, 5597.92), (0.27, 5597.92)])
rightSpringsMaterials[2003]= typical_materials.defMultiLinearMaterial(preprocessor, name="2003",points= [(0.02, 7977.46), (0.05, 11063.67), (0.1, 11611.62), (0.27, 11611.62)])
rightSpringsMaterials[2004]= typical_materials.defMultiLinearMaterial(preprocessor, name="2004",points= [(0.02, 11425.57), (0.05, 15200.34), (0.1, 15698.4), (0.27, 15698.4)])
rightSpringsMaterials[2005]= typical_materials.defMultiLinearMaterial(preprocessor, name="2005",points= [(0.02, 13526.59), (0.05, 15957.33), (0.1, 16100.41), (0.27, 16100.41)])
rightSpringsMaterials[2006]= typical_materials.defMultiLinearMaterial(preprocessor, name="2006",points= [(0.02, 29727.57), (0.05, 31899.2), (0.1, 42993.8), (0.27, 42993.8)])
rightSpringsMaterials[2007]= typical_materials.defMultiLinearMaterial(preprocessor, name="2007",points= [(0.02, 58010.6), (0.05, 62498.84), (0.1, 82526.86), (0.27, 82526.86)])
rightSpringsMaterials[2008]= typical_materials.defMultiLinearMaterial(preprocessor, name="2008",points= [(0.02, 74905.84), (0.05, 84375.43), (0.1, 96281.34), (0.27, 96281.34)])
rightSpringsMaterials[2009]= typical_materials.defMultiLinearMaterial(preprocessor, name="2009",points= [(0.02, 92965.16), (0.05, 109128.25), (0.1, 110025.1), (0.27, 110025.1)])
rightSpringsMaterials[2010]= typical_materials.defMultiLinearMaterial(preprocessor, name="2010",points= [(0.02, 111234.95), (0.05, 136510.48), (0.1, 138589.17), (0.27, 138589.17)])
rightSpringsMaterials[2011]= typical_materials.defMultiLinearMaterial(preprocessor, name="2011",points= [(0.02, 128738.91), (0.05, 166232.73), (0.1, 170379.01), (0.27, 170379.01)])
rightSpringsMaterials[2012]= typical_materials.defMultiLinearMaterial(preprocessor, name="2012",points= [(0.02, 147256.85), (0.05, 198278.97), (0.1, 205383.37), (0.27, 205383.37)])
rightSpringsMaterials[2013]= typical_materials.defMultiLinearMaterial(preprocessor, name="2013",points= [(0.02, 166788.78), (0.05, 231776.72), (0.1, 243586.79), (0.27, 243586.79)])
rightSpringsMaterials[2014]= typical_materials.defMultiLinearMaterial(preprocessor, name="2014",points= [(0.02, 187024.01), (0.05, 266779.07), (0.1, 284965.7), (0.27, 284965.7)])
rightSpringsMaterials[2015]= typical_materials.defMultiLinearMaterial(preprocessor, name="2015",points= [(0.02, 204049.44), (0.05, 304174.57), (0.1, 329458.91), (0.27, 329458.91)])
rightSpringsMaterials[2016]= typical_materials.defMultiLinearMaterial(preprocessor, name="2016",points= [(0.02, 220858.56), (0.05, 341241.87), (0.1, 377033.88), (0.27, 377033.88)])
rightSpringsMaterials[2017]= typical_materials.defMultiLinearMaterial(preprocessor, name="2017",points= [(0.02, 237963.67), (0.05, 378447.5), (0.1, 427653.82), (0.27, 427653.82)])
rightSpringsMaterials[2018]= typical_materials.defMultiLinearMaterial(preprocessor, name="2018",points= [(0.02, 255364.8), (0.05, 417450.22), (0.1, 481137.09), (0.27, 481137.09)])
rightSpringsMaterials[2019]= typical_materials.defMultiLinearMaterial(preprocessor, name="2019",points= [(0.02, 273061.96), (0.05, 458250.05), (0.1, 537513.32), (0.27, 537513.32)])
rightSpringsMaterials[2020]= typical_materials.defMultiLinearMaterial(preprocessor, name="2020",points= [(0.02, 291055.14), (0.05, 500846.96), (0.1, 596823.35), (0.27, 596823.35)])
rightSpringsMaterials[2021]= typical_materials.defMultiLinearMaterial(preprocessor, name="2021",points= [(0.02, 309344.32), (0.05, 540243.05), (0.1, 658217.45), (0.27, 658217.45)])
rightSpringsMaterials[2022]= typical_materials.defMultiLinearMaterial(preprocessor, name="2022",points= [(0.02, 327929.54), (0.05, 577935.56), (0.1, 722599.39), (0.27, 722599.39)])
rightSpringsMaterials[2023]= typical_materials.defMultiLinearMaterial(preprocessor, name="2023",points= [(0.02, 346810.77), (0.05, 616642.04), (0.1, 789806.5), (0.27, 789806.5)])
rightSpringsMaterials[2024]= typical_materials.defMultiLinearMaterial(preprocessor, name="2024",points= [(0.02, 365988.01), (0.05, 656362.49), (0.1, 858021.68), (0.27, 858021.68)])
rightSpringsMaterials[2025]= typical_materials.defMultiLinearMaterial(preprocessor, name="2025",points= [(0.02, 385461.29), (0.05, 697096.92), (0.1, 928656.37), (0.27, 928656.37)])
rightSpringsMaterials[2026]= typical_materials.defMultiLinearMaterial(preprocessor, name="2026",points= [(0.02, 202615.29), (0.05, 369422.67), (0.1, 501030.94), (0.27, 501030.94)])


##### Springs in Series on the Left and Right Sides of Pile/Wall
################################################################
sz= len(leftSpringsMaterials)
leftSeriesMaterials= dict()
rightSeriesMaterials= dict()

for k in range(1,sz+1):
    leftSeriesIndex= 3000+k
    leftSpringIndex= 1000+k
    leftSeriesMaterials[leftSeriesIndex]= typical_materials.defSeriesMaterial(preprocessor, name= str(leftSeriesIndex), materialsToConnect= [rigidDummySpring.name, leftSpringsMaterials[leftSpringIndex].name])
    rightSeriesIndex= 4000+k
    rightSpringIndex= 2000+k
    rightSeriesMaterials[rightSeriesIndex]= typical_materials.defSeriesMaterial(preprocessor, name= str(rightSeriesIndex), materialsToConnect= [rigidDummySpring.name, rightSpringsMaterials[rightSpringIndex].name])


# Define Spring Elements
elements= preprocessor.getElementHandler
elements.dimElem= 2 #Element dimension.
leftZLElements= dict()
rightZLElements= dict()
for i, pair in enumerate(springPairs):
    k= i+1
    leftSeriesIndex= 3000+k
    elements.defaultMaterial=  leftSeriesMaterials[leftSeriesIndex].name
    # Springs on the leftside of the beam
    zlLeft= elements.newElement("ZeroLength",xc.ID([pair[0].tag, pair[1].tag]))
    zlLeft.setupVectors(xc.Vector([1,0,0]),xc.Vector([0,1,0]))
    leftZLElements[leftSeriesIndex]= zlLeft
    rightSeriesIndex= 4000+k
    elements.defaultMaterial= rightSeriesMaterials[rightSeriesIndex].name
    # Springs on the rightside of the beam
    zlRight= elements.newElement("ZeroLength",xc.ID([pair[1].tag, pair[0].tag]))
    zlRight.setupVectors(xc.Vector([-1,0,0]),xc.Vector([0,-1,0]))
    rightZLElements[rightSeriesIndex]= zlRight



# # Record Data

# dataDir= Outputs
# file mkdir dataDir

# ### Pile Recorders
# eval "recorder Node -file dataDir/disppile_below_ground.out           -time -nodeRange 1 [expr numZele_emb+1] -dof 1 2 3 4 5 6 disp"
# eval "recorder Element -file dataDir/pileforcesGlob_below_ground.out  -time -eleRange  1 numZele_emb  globalForce"

# eval "recorder Node -file dataDir/disppile_above_ground.out           -time -nodeRange [expr numZele_emb+2] [expr numZele_emb+1+numZele_above_grade] -dof 1 2 3 4 5 6 disp"
# eval "recorder Element -file dataDir/pileforcesGlob_above_ground.out  -time -eleRange  [expr numZele_emb+1] [expr numZele_emb+numZele_above_grade]  globalForce"

# eval "recorder Element -file dataDir/Soilreaction_left.out  -time -eleRange  5001 [expr 5000+Num_Springs]  force"
# eval "recorder Element -file dataDir/Soilreaction_right.out  -time -eleRange  4001 [expr 4000+Num_Springs]  force"

# Apply Load on Pile Head or Uniform Load
## Node top element.
nTop= linesToMesh[-1].getP1().getNode()
print('Y top node: ', nTop.getInitialPos3d.y)

lp0= modelSpace.newLoadPattern(name= '0')
lp0.newNodalLoad(nTop.tag,xc.Vector([12360,0.0,0.0]))
# We add the load case to domain.
modelSpace.addLoadCaseToDomain(lp0.name)


# pattern Plain 2000 "Linear" {
	
# 	######## Pile Head Displacement and Rotation
#     #sp [expr numZele_emb+numZele_above_grade+1] 1 0.25 # User-Defined
    
# 	######## Pile Head Load	
# 	#load [expr numZele_emb+numZele_above_grade+1] 200000.0 0.0 0.0 0.0 0.0 0.0 # User-Defined
	
# 	######## Distributed Pressure	
# 	for { k= 1 } { k <= [expr numZele_emb-1] } { incr k 1 } {
#     		load [expr k+1] [expr 26880.0+(k-1)*2880.0] 0.0 0.0 0.0 0.0 0.0 # User-Defined
#      }
# 	#### load at pile tip 
# 	load [expr numZele_emb+1] 47640.0 0.0 0.0 0.0 0.0 0.0 # User-Defined
# 	#### Load at pile top element			
# 	eleLoad -ele 1  -type -beamPoint 12360 0.0 0.16 # User-Defined
# }


# Pile Static Analysis 

solProc= predefined_solutions.PenaltyKrylovNewton(prb= feProblem, numSteps= 500)

solProc.solve()

# test NormDispIncr 1.0e-4 100 1



print(" ## End of Analysis!! ## ")


from postprocess import output_handler
# Graphic stuff.
oh= output_handler.OutputHandler(modelSpace)
oh.displayFEMesh()
#oh.displayLocalAxes()
oh.displayLoads()
oh.displayDispRot('uX')
oh.displayIntForcDiag('M')
oh.displayIntForcDiag('V')

