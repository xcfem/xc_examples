# -*- coding: utf-8 -*-
''' Inertia load on MITC4 shell elements. 
    Equilibrium based home made test.'''

from __future__ import division
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2020, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

import math
import xc_base
import geom
import xc
from model import predefined_spaces
from solution import predefined_solutions
from materials import typical_materials
from postprocess import output_handler

feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor
nodes= preprocessor.getNodeHandler

# Problem type
modelSpace= predefined_spaces.StructuralMechanics3D(nodes)
n1= nodes.newNodeXYZ(0.,1.0,0.)
n2= nodes.newNodeXYZ(0., 0.5, 0.)
n3= nodes.newNodeXYZ(0., 0., 0.)
n4= nodes.newNodeXYZ(1.0, 1., 0.)
n5= nodes.newNodeXYZ(1.0, 0.5, 0.)
n6= nodes.newNodeXYZ(1.0, 0., 0.)
n7= nodes.newNodeXYZ(2.0, 1., 0.)
n8= nodes.newNodeXYZ(2.0, 0.5, 0.)
n9= nodes.newNodeXYZ(2.0, 0., 0.)
n10= nodes.newNodeXYZ(3.0, 1., 0.)
n11= nodes.newNodeXYZ(3.0, 0.5, 0.)
n12= nodes.newNodeXYZ(3.0, 0., 0.)
n13= nodes.newNodeXYZ(4.0, 1., 0.)
n14= nodes.newNodeXYZ(4.0, 0.5, 0.)
n15= nodes.newNodeXYZ(4.0, 0., 0.)
n16= nodes.newNodeXYZ(5., 1., 0.)
n17= nodes.newNodeXYZ(5., 0.5, 0.)
n18= nodes.newNodeXYZ(5., 0., 0.)
n19= nodes.newNodeXYZ(6.0, 1., 0.)
n20= nodes.newNodeXYZ(6.0, 0.5, 0.)
n21= nodes.newNodeXYZ(6.0, 0., 0.)
n22= nodes.newNodeXYZ(7.0, 1., 0.)
n23= nodes.newNodeXYZ(7.0, 0.5, 0.)
n24= nodes.newNodeXYZ(7.0, 0., 0.)
n25= nodes.newNodeXYZ(8.0, 1., 0.)
n26= nodes.newNodeXYZ(8.0, 0.5, 0.)
n27= nodes.newNodeXYZ(8.0, 0., 0.)
n28= nodes.newNodeXYZ(9.0, 1., 0.)
n29= nodes.newNodeXYZ(9.0, 0.5, 0.)
n30= nodes.newNodeXYZ(9.0, 0., 0.)
n31= nodes.newNodeXYZ(10., 1., 0.)
n32= nodes.newNodeXYZ(10., 0.5, 0.)
n33= nodes.newNodeXYZ(10., 0., 0.)

# Constraints.
constrainedNodes= [n1, n2, n3]
for n in constrainedNodes:
    modelSpace.fixNode000_000(n.tag)

# Materials
E= 1.2e6
nu= 0.3
elast3d= typical_materials.defElasticIsotropic3d(preprocessor, "elast3d",E,nu,rho= 0.0)
thickness= 0.1
plateFiber= typical_materials.defMembranePlateFiberSection(preprocessor, name= "plateFiber", h= thickness, nDMaterial= elast3d)
## Full circle moment
I= 1/12.0*1.0*thickness**3
L= 10.0 # lenght of the beam
Mcircle= 2.0*math.pi*E*I/L

# Elements
elements= preprocessor.getElementHandler
elements.defaultMaterial= plateFiber.name
e1= elements.newElement("ShellNLDKGQ",xc.ID([n1.tag,n2.tag,n5.tag,n4.tag]))
e2= elements.newElement("ShellNLDKGQ",xc.ID([n3.tag, n6.tag, n5.tag, n2.tag]))
e3= elements.newElement("ShellNLDKGQ",xc.ID([n5.tag, n8.tag, n7.tag, n4.tag]))
e4= elements.newElement("ShellNLDKGQ",xc.ID([n6.tag, n9.tag, n8.tag, n5.tag]))
e5= elements.newElement("ShellNLDKGQ",xc.ID([n8.tag, n11.tag, n10.tag, n7.tag]))
e6= elements.newElement("ShellNLDKGQ",xc.ID([n9.tag, n12.tag, n11.tag, n8.tag]))
e7= elements.newElement("ShellNLDKGQ",xc.ID([n11.tag, n14.tag, n13.tag, n10.tag]))
e8= elements.newElement("ShellNLDKGQ",xc.ID([n12.tag, n15.tag, n14.tag, n11.tag]))
e9= elements.newElement("ShellNLDKGQ",xc.ID([n14.tag, n17.tag, n16.tag, n13.tag]))
e10= elements.newElement("ShellNLDKGQ",xc.ID([n15.tag, n18.tag, n17.tag, n14.tag]))
e11= elements.newElement("ShellNLDKGQ",xc.ID([n17.tag, n20.tag, n19.tag, n16.tag]))
e12= elements.newElement("ShellNLDKGQ",xc.ID([n18.tag, n21.tag, n20.tag, n17.tag]))
e13= elements.newElement("ShellNLDKGQ",xc.ID([n20.tag, n23.tag, n22.tag, n19.tag]))
e14= elements.newElement("ShellNLDKGQ",xc.ID([n21.tag, n24.tag, n23.tag, n20.tag]))
e15= elements.newElement("ShellNLDKGQ",xc.ID([n23.tag, n26.tag, n25.tag, n22.tag]))
e16= elements.newElement("ShellNLDKGQ",xc.ID([n24.tag, n27.tag, n26.tag, n23.tag]))
e17= elements.newElement("ShellNLDKGQ",xc.ID([n26.tag, n29.tag, n28.tag, n25.tag]))
e18= elements.newElement("ShellNLDKGQ",xc.ID([n27.tag, n30.tag, n29.tag, n26.tag]))
e19= elements.newElement("ShellNLDKGQ",xc.ID([n29.tag, n32.tag, n31.tag, n28.tag]))
e20= elements.newElement("ShellNLDKGQ",xc.ID([n30.tag, n33.tag, n32.tag, n29.tag]))


# Recorders
nTags= list()
xcTotalSet= modelSpace.getTotalSet()
for n in xcTotalSet.nodes:
    nTags.append(n.tag)
dof1Disp= list()
recD= preprocessor.getDomain.newRecorder("node_prop_recorder",None)
recD.setNodes(xc.ID(nTags))
recD.callbackRecord= "dof1Disp.append([self.tag, self.getDomain.getTimeTracker.getCurrentTime, self.getDisp])"
reactions= list()
recR= preprocessor.getDomain.newRecorder("node_prop_recorder",None)
recR.setNodes(xc.ID(nTags))
recR.callbackRecord= "reactions.append([self.tag, self.getDomain.getTimeTracker.getCurrentTime, self.getReaction])"

# Loading
loadPatterns= preprocessor.getLoadHandler.getLoadPatterns
linearTS= loadPatterns.newTimeSeries("linear_ts","ts")
loadPatterns.currentTimeSeries= "ts"
lp0= loadPatterns.newLoadPattern("default","0")
M= 0.25*Mcircle
lp0.newNodalLoad(n31.tag,xc.Vector([0,0,0,0,0.25*M,0]))
lp0.newNodalLoad(n32.tag,xc.Vector([0,0,0,0,0.5*M,0]))
lp0.newNodalLoad(n33.tag,xc.Vector([0,0,0,0,0.25*M,0]))
modelSpace.setCurrentLoadPattern(lp0.name)

# We add the load case to domain.
modelSpace.addLoadCaseToDomain(lp0.name)

# Solution
solu= feProblem.getSoluProc
solCtrl= solu.getSoluControl
solModels= solCtrl.getModelWrapperContainer
sm= solModels.newModelWrapper("sm")
cHandler= sm.newConstraintHandler("plain_handler")
numberer= sm.newNumberer("default_numberer")
numberer.useAlgorithm("simple")
solutionStrategies= solCtrl.getSolutionStrategyContainer
solutionStrategy= solutionStrategies.newSolutionStrategy("solutionStrategy","sm")
solAlgo= solutionStrategy.newSolutionAlgorithm('krylov_newton_soln_algo')
ctest= solutionStrategy.newConvergenceTest('norm_disp_incr_conv_test')
ctest.tol= 1e-3
ctest.maxNumIter= 1000
ctest.printFlag= 0
integ= solutionStrategy.newIntegrator("load_control_integrator",xc.Vector([]))
integ.dLambda1= 0.001
soe= solutionStrategy.newSystemOfEqn("band_gen_lin_soe")
solver= soe.newSolver("band_gen_lin_lapack_solver")
analysis= solu.newAnalysis("static_analysis","solutionStrategy","")
result= analysis.analyze(4000)

disp= n32.getDisp
u= disp[0]
v= disp[2]
normU= abs(u)/L
normV= abs(v)/L
theta1= disp[4]
theta1Theor= M*L/(E*I)

print('Mcircle= ', Mcircle)
print(disp)
print('normU= ', normU)
print('normV= ', normV)
print('theta1= ', theta1)
print('theta1Theor= ', theta1Theor)

#########################################################
# Graphic stuff.
oh= output_handler.OutputHandler(modelSpace)
oh.displayFEMesh(defFScale= 1.0)
