# -*- coding: utf-8 -*-
''' Reference: Thomson, Ref 9: Vibration Theory and Applications, pg. 264, clause 8.2.
   '''
from __future__ import division
from __future__ import print_function

import math
import geom
import xc
from model import predefined_spaces
from materials import typical_materials

__author__= "Luis C. Pérez Tato (LCPT), Ana Ortega (AO_O)"
__copyright__= "Copyright 2014, LCPT, AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com ana.ortega.ort@gmail.com"

E= 2.1e11 # steel Young modulus [Pa]
ro=7850   #steel specific mass [kg/m3]
l= 2.0 # String length [m]
sigmaPret= E*0.005 # Prestressing force [N]
area= 2.0e-6     # Cross-sectional area [m2]
Mass= ro*area # Mass per unit length.
NumDiv= 13
fPret= sigmaPret*area # Prestressing force (pounds)


# Model definition
feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor
nodes= preprocessor.getNodeHandler
# Problem type
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)

# Materials definition
typical_materials.defCableMaterial(preprocessor, "cable",E,sigmaPret,ro)

# Seed element definition
seedElemHandler= preprocessor.getElementHandler.seedElemHandler
seedElemHandler.defaultMaterial= "cable"
seedElemHandler.dimElem= 2 # Dimension of element space
seedElemHandler.defaultTag= 1 #Tag for the next element.
truss= seedElemHandler.newElement("CorotTruss",xc.ID([0,0]))
truss.sectionArea= area
# seed element definition ends

points= preprocessor.getMultiBlockTopology.getPoints
pt1= points.newPoint(1,geom.Pos3d(0.0,0.0,0.0))
pt2= points.newPoint(2,geom.Pos3d(l,0.0,0.0))
lines= preprocessor.getMultiBlockTopology.getLines
l= lines.newLine(pt1.tag,pt2.tag)

l.nDiv= NumDiv
l.genMesh(xc.meshDir.I)
    
# Constraints
predefined_spaces.ConstraintsForLineExtremeNodes(l,modelSpace.fixNode000)
predefined_spaces.ConstraintsForLineInteriorNodes(l,modelSpace.fixNodeFF0)

#Analysis
solProc=feProblem.getSoluProc
solCtrl= solProc.getSoluControl
solModels= solCtrl.getModelWrapperContainer
analAggrContainer= solCtrl.getSolutionStrategyContainer
#static analysis
sm= solModels.newModelWrapper("sm")
cHandler= sm.newConstraintHandler("plain_handler")
numberer= sm.newNumberer("default_numberer")
numberer.useAlgorithm("simple")
solutionStrategy= analAggrContainer.newSolutionStrategy("solutionStrategy","sm")
solAlgo= solutionStrategy.newSolutionAlgorithm("newton_raphson_soln_algo")
ctest= solutionStrategy.newConvergenceTest("norm_unbalance_conv_test")
ctest.tol= 1e-8
ctest.maxNumIter= 100
integ= solutionStrategy.newIntegrator("load_control_integrator",xc.Vector([]))
Nstep= 10  #  apply load in 10 steps
DInc= 1./Nstep 	#  first load increment
integ.dLambda1= DInc
soe= solutionStrategy.newSystemOfEqn("band_gen_lin_soe")
solver= soe.newSolver("band_gen_lin_lapack_solver")
analysis= solProc.newAnalysis("static_analysis","solutionStrategy","")
result= analysis.analyze(Nstep)

elements= preprocessor.getElementHandler
ele1= elements.getElement(1)
tension= ele1.getN()
sigma= ele1.getMaterial().getStress()
print("stress= ",sigma)
print("tension= ",tension)


# Eigen solution procedure
sm= solModels.newModelWrapper("sm")
cHandler= sm.newConstraintHandler("transformation_constraint_handler")
numberer= sm.newNumberer("default_numberer")
numberer.useAlgorithm("rcm")
solutionStrategy= analAggrContainer.newSolutionStrategy("solutionStrategy","sm")
solAlgo= solutionStrategy.newSolutionAlgorithm("frequency_soln_algo")
soe= solutionStrategy.newSystemOfEqn("sym_band_eigen_soe")
solver= soe.newSolver("sym_band_eigen_solver")
analysis= solProc.newAnalysis("eigen_analysis","solutionStrategy","")
integ= solutionStrategy.newIntegrator("eigen_integrator",xc.Vector([]))
Neigen=3
analOk= analysis.analyze(Neigen)

eig1= analysis.getEigenvalue(1)
eig2= analysis.getEigenvalue(2)
eig3= analysis.getEigenvalue(3)
f1= math.sqrt(eig1)/(2*math.pi)
f2= math.sqrt(eig2)/(2*math.pi)
f3= math.sqrt(eig3)/(2*math.pi)

print("eig1= ",eig1)
print("eig2= ",eig2)
print("eig3= ",eig3)
print("f1= ",math.sqrt(eig1)/(2*math.pi))
print("f2= ",math.sqrt(eig2)/(2*math.pi))
print("f3= ",math.sqrt(eig3)/(2*math.pi))

  
