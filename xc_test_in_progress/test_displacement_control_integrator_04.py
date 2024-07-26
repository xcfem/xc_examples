# -*- coding: utf-8 -*-
''' Trivial text to check the change of the integrator from load control to displacement control.
'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2023, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

import xc
from model import predefined_spaces
from materials import typical_materials
from solution import predefined_solutions

def moment_curvature(modelSpace, uniMat, axialLoad, maxD, numIncr):
    ''' Compute the axial force - displacement diagram.

    :param modelSpace: finite element model wrapper.
    :param uniMat: uniaxial material.
    :param axialLoad: axial load.
    :param maxD: maximum value of the displacement to reach.
    :param numIncr: number of increments for the analysis.
    '''
    # Define two nodes at (0,0)
    nod1= modelSpace.newNodeXY(0.0, 0.0)
    nod2= modelSpace.newNodeXY(1.0, 0.0)

    # Fix all degrees of freedom except axial.
    modelSpace.fixNode000(nod1.tag)
    modelSpace.fixNodeF00(nod2.tag)

    # Define element
    #                         tag ndI ndJ  secTag
    elements= preprocessor.getElementHandler
    elements.defaultMaterial= uniMat.name
    elements.dimElem= 2 # Dimension of element space
    truss= elements.newElement("Truss",xc.ID([nod1.tag,nod2.tag]))
    truss.sectionArea= .01
    

    # Create recorders
    recDFree= modelSpace.newRecorder("node_prop_recorder",None)
    recDFree.setNodes(xc.ID([nod2.tag]))
    recDFree.callbackRecord= "modelSpace.ti.append(self.getDomain.getTimeTracker.getCurrentTime); modelSpace.dx.append(self.getDisp[0])"
    myRecorder= feProblem.getDomain.newRecorder("element_prop_recorder",None)
    myRecorder.setElements(xc.ID([truss.tag]))
    myRecorder.callbackRecord= "modelSpace.ni.append(self.getN())"
    myRecorder.callbackSetup= "self.getDomain.calculateNodalReactions(True,1e-4)"

    # Define constant axial load
    loadHandler= modelSpace.getLoadHandler()
    lPatterns= loadHandler.getLoadPatterns
    constantTS= lPatterns.newTimeSeries("constant_ts","constantTS")
    constantLP= modelSpace.newLoadPattern(name= 'constantLP')
    constantLP.timeSeries= constantTS
    modelSpace.setCurrentLoadPattern(constantLP.name)
    nod2.newLoad(xc.Vector([P,0,0]))
    modelSpace.addLoadCaseToDomain(constantLP.name)

    # Define analysis parameters
    solProc= predefined_solutions.PlainNewtonRaphson(prb= feProblem, printFlag= 0, maxNumIter= 100)
    solProc.setup()
    analysis= solProc.analysis
    
    # Do one analysis for constant axial load
    result= analysis.analyze(1)
    print('DISP0= ', nod2.getDisp[0],'\n')

    # Define reference force
    linearTS= lPatterns.newTimeSeries("linear_ts","LinearTS")
    linearLP= modelSpace.newLoadPattern(name= 'linearLP')
    linearLP.timeSeries= linearTS
    modelSpace.setCurrentLoadPattern(linearLP.name)
    nod2.newLoad(xc.Vector([1,0,0]))
    modelSpace.addLoadCaseToDomain(linearLP.name)

    # Compute displacement increment
    dD= maxD/numIncr

    # Use displacement control at node 2 for section analysis
    solProc.integrator= solProc.solutionStrategy.newIntegrator('displacement_control_integrator', solProc.integratorParameters)
    solProc.integrator.nodeTag= nod2.tag
    solProc.integrator.dof= 0
    solProc.integrator.increment= dD
    solProc.integrator.minIncrement= dD
    solProc.integrator.maxIncrement= dD
    solProc.integrator.numIncr= 100

    print('before: ', solProc.integrator.increment)
    # Do the section analysis
    analysis.analyze(numIncr)
    print('after: ', solProc.integrator.increment)
    
    return uniMat.E*truss.sectionArea

def plot_diagram(plt, di, ni):
    ''' Plot the section moment-curvature diagram.

    :plt: matplotlib module.
    :di: displacement values.
    :ni: axiald load values.
    '''
    plt.plot(di, ni, "-b")

    # Add title and axis names
    plt.title('N-Ux diagram')
    plt.xlabel('displacement')
    plt.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
    plt.xticks(rotation = 90)
    plt.ylabel('axial load')
    plt.show()

# Define problem
feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor
nodes= preprocessor.getNodeHandler
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)

# Define uniaxial materials
## Reinforcing steel
reinforcingSteel= typical_materials.defSteel01(preprocessor, 'reinforcingSteel', E= 2e9, fy= 500e6, b= .01)
#reinforcingSteel= typical_materials.defElasticMaterial(preprocessor, name= 'reinforcingSteel', E= 2e9)

# Estimate yield displacement
epsy= 500e6/reinforcingSteel.E # steel yield strain
Dy= epsy*1.0

print("Estimated yield displacement: ", Dy)

# Set axial load 
P= -18e5

mu= 2 # Target ductility for analysis
numIncr= 100 # Number of analysis increments

modelSpace.ti= list()
modelSpace.dx= list()
modelSpace.ni= list()
EA= moment_curvature(modelSpace, uniMat= reinforcingSteel, axialLoad= P, maxD= Dy*mu, numIncr= numIncr)

print('max. displacement: ', Dy*mu)
print('max. axial force: ', Dy*mu*EA)
'''
print(modelSpace.ti)
print(modelSpace.dx)
print(modelSpace.ni)
'''

# Display Matplotlib graphics.
import matplotlib.pyplot as plt
plot_diagram(plt, modelSpace.dx, modelSpace.ni)

