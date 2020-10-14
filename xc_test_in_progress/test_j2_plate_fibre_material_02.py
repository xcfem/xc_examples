# -*- coding: utf-8 -*-
'''Verification test based on the paper: "Finite Element Modeling of Gusset Plate Failure 
   Using Opensees" by Andrew J. Walker
   section 3.7 "Simple Tension Verification", page 54 and following.
'''

from __future__ import division
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AO_O)"
__copyright__= "Copyright 2020, LCPT and AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com ana.ortega.ort@gmail.com"

import math
import xc_base
import geom
import xc
from solution import predefined_solutions
from model import predefined_spaces
from materials import typical_materials

# Data
# Units
in2m=0.0254       # inches to m
ksi2Pa=6.89476e6  # ksi to Pa
kip2N=4448.2216   # kips to N

width=1*in2m   # Rod width (m)
thickness=1*in2m   # Rod thickness (m)
L= 50*in2m # Length of the rod (m)

E= 29000*ksi2Pa # Young’s modulus (Pa)
nu= 0.3 # Poisson’s ratio
sg_yield= 60*ksi2Pa # Allowable stress: yield stress of steel (Pa)
alpha=0.05  # strain hardening ratio

# Problem type
feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor
nodes= preprocessor.getNodeHandler 
modelSpace= predefined_spaces.StructuralMechanics3D(nodes)


# Material definition
j2plate= typical_materials.defJ2PlateFibre(preprocessor, "j2plate",E,nu,fy= sg_yield, alpha=alpha,rho= 7850.0)

plateFiber= typical_materials.defMembranePlateFiberSection(preprocessor, name= "plateFiber", h= thickness, nDMaterial= j2plate);

# Problem geometry
# The “bottom-up method” generates the geometry of the system
# going  from  key  points (0D) to lines (1D) and areas (2D)
# up to volumes (3D).

p1= modelSpace.newKPoint(0.0,width/2)
p2= modelSpace.newKPoint(L,width/2)
p3= modelSpace.newKPoint(L,-width/2)
p4= modelSpace.newKPoint(0.0,-width/2.0)

s= modelSpace.newSurface([p1,p2,p3,p4])
s.setElemSizeIJ(L/70,width/10)
#s.nDivI= 50 # Number of divisions on p1->p2 and p3->p4
#s.nDivJ= 10 # Number of divisions on p2->p3 and p4->p1

# Meshing

## Define template element
## Before we can create a mesh for our model, we need to choose which
## type of finite element we will want to use for our mesh.
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial= plateFiber.name
quad= seedElemHandler.newElement("ShellMITC4",xc.ID([0,0,0,0]))

## Generate mesh
s.genMesh(xc.meshDir.I)

xcTotalSet= modelSpace.getTotalSet()
numElementsTeor= s.nDivI*s.nDivJ
numElements= xcTotalSet.getNumElements
numNodesTeor= (s.nDivI+1)*(s.nDivJ+1)
numNodes= xcTotalSet.getNumNodes

## Boundary conditions

### Get the line between p4 and p1
l14= modelSpace.getLineWithEndPoints(p1,p4)
### Fix nodes in 1->4 line.
for n in l14.nodes:
    modelSpace.fixNode000_FFF(n.tag)

## Loads
l23= modelSpace.getLineWithEndPoints(p2,p3)
nnod=len(l23.nodes)
maxLoad=100*kip2N
### Create load pattern.
lp0= modelSpace.newLoadPattern('0')
### Distribute the load over nodes in line 2-3
for n in l23.nodes:
    lp0.newNodalLoad(n.tag,xc.Vector([maxLoad/nnod,0,0,0,0,0]))
modelSpace.addLoadCaseToDomain(lp0.name)


# Solution
result=list()
for i in range(7):
    lp0.gammaF= 0.1*(i+1)
    ## Solve
    modelSpace.analysis= predefined_solutions.plain_krylov_newton(modelSpace.preprocessor.getProblem,mxNumIter=300, convergenceTestTol=1e-12,printFlag=0)
    analOK= modelSpace.analyze(calculateNodalReactions= True)
    dispX=0
    for n in l23.nodes:
        dispX+=n.getDisp[0]
    F=round(maxLoad*lp0.gammaF/kip2N,1)
    uX=round(dispX/nnod/in2m,4)
    print('F=',F, ' kips , uX=',uX , ' in')
    result.append((F,uX))
for i in range(5):
    lp0.gammaF= 0.6+(i*0.025)
    ## Solve
    modelSpace.analysis= predefined_solutions.plain_krylov_newton(modelSpace.preprocessor.getProblem,mxNumIter=300, convergenceTestTol=1e-12,printFlag=0)
    analOK= modelSpace.analyze(calculateNodalReactions= True)
    dispX=0
    for n in l23.nodes:
        dispX+=n.getDisp[0]
    F=round(maxLoad*lp0.gammaF/kip2N,1)
    uX=round(dispX/nnod/in2m,4)
    print('F=',F, ' kips , uX=',uX , ' in')
    result.append((F,uX))
    

quit()
# from postprocess import output_handler
# oh= output_handler.OutputHandler(modelSpace)
# oh.displayLoads()



import os
from misc_utils import log_messages as lmsg
fname= os.path.basename(__file__)
if(ratio1<0.05 and ratio2<0.06 and ratio3<0.05): # Good results :)
  print("test ",fname,": ok.")
else:
  lmsg.error(fname+' ERROR.')
  
# Graphic stuff.
from postprocess import output_handler
oh= output_handler.OutputHandler(modelSpace)
oh.displayFEMesh()
oh.displayLocalAxes()
oh.displayLoads()
oh.displayDispRot('uY')
oh.displayStrains('epsilon_xx')
oh.displayStresses('sigma_11')
oh.displayVonMisesStresses(vMisesCode= 'max_von_mises_stress')
