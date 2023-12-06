# -*- coding: utf-8 -*-
'''Displacement control integrator trivial test.'''

from __future__ import print_function
from __future__ import division

import xc
from solution import predefined_solutions
from model import predefined_spaces
from materials import typical_materials

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2022, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"


# Problem type
feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor
nodes= preprocessor.getNodeHandler
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)

# Define materials
k= typical_materials.defElasticMaterial(preprocessor, "k",E= 1)

# Define mesh.
n1= nodes.newNodeXY(0,0)
n2= nodes.newNodeXY(0,0)

# Define element.
elements= preprocessor.getElementHandler
elements.defaultMaterial= k.name
elements.dimElem= 2 # Dimension of element space
spring= elements.newElement("ZeroLength",xc.ID([n1.tag,n2.tag]))

# Constraints
modelSpace.fixNode000(n1.tag)
modelSpace.fixNodeF00(n2.tag)

# Create recorders
reacN1= list()
recReacN1= preprocessor.getDomain.newRecorder("node_prop_recorder",None)
recReacN1.setNodes(xc.ID([n1.tag]))
recReacN1.callbackRecord= "reacN1.append([self.getDomain.getTimeTracker.getCurrentTime, self.getReaction[0]])"
recReacN1.callbackSetup= "self.getDomain.calculateNodalReactions(True,1e-4)"

# Define load.
## Constant load definition.
P= -1
constantTS= modelSpace.newTimeSeries(name= "constantTS", tsType= "constant_ts")
constantLP= modelSpace.newLoadPattern(name= 'constantLP')
constantLP.timeSeries= constantTS
modelSpace.setCurrentLoadPattern(constantLP.name)
constantLP.newNodalLoad(n2.tag, xc.Vector([P,0,0]))
modelSpace.addLoadCaseToDomain(constantLP.name)

## Solve for constant load.
solProc= predefined_solutions.PlainNewtonRaphson(prb= feProblem, numSteps= 1, printFlag= 1)
solProc.setup()
result= solProc.solve(calculateNodalReactions= True)
disp0= n2.getDisp[0]
refDisp0= P/k.E
ratio0= abs(disp0-refDisp0)/refDisp0
R0= n1.getReaction[0]


# Displacement control.
## Linear load definition.
linearTS= modelSpace.newTimeSeries(name= "linearTS", tsType= "linear_ts")
linearLP= modelSpace.newLoadPattern(name= '0')
linearLP.timeSeries= linearTS
linearLP.newNodalLoad(n2.tag,xc.Vector([1,0,0]))
## We add the load case to domain.
modelSpace.addLoadCaseToDomain(linearLP.name)

# Solution
dispIncrement= 0.5
maxU= 10
numSteps= int((maxU-disp0)/dispIncrement)
solProc= predefined_solutions.SimpleNewtonRaphsonDisplacementControl(prb= feProblem, node= n2, dof= 0, increment= dispIncrement, numSteps= numSteps, convTestType= 'norm_unbalance_conv_test', convergenceTestTol= 1e-9, maxNumIter= 40, printFlag= 1)
#solProc= predefined_solutions.SimpleNewtonRaphsonDisplacementControl(prb= feProblem, node= n2, dof= 0, increment= dispIncrement, numSteps= numSteps, convergenceTestTol= 1e-9, maxNumIter= 40, printFlag= 1)

solProc.solve(calculateNodalReactions= True)

deltax= n2.getDisp[0]
ratio1= abs(deltax-maxU)/maxU
R= n1.getReaction[0]
F= k.E*deltax
ratio2= abs(F+R)/F

print('numSteps= ', numSteps)
# print('reactions: ', reacN1)
print('disp0= ', disp0)
print('ratio0= ', ratio0)
print('R0= ', R0)
print("dx= ",deltax)
print("ratio1= ",ratio1)
print("R= ",R)
print("F= ",F)
print("ratio2= ",ratio2)
'''
'''

import os
from misc_utils import log_messages as lmsg
fname= os.path.basename(__file__)
if (abs(ratio0)<1e-12) & (abs(ratio1)<1e-12) & (abs(ratio2)<1e-12):
    print('test '+fname+': ok.')
else:
    lmsg.error(fname+' ERROR.')
    
# # Display results
# ## Extract results.
# ti= list()
# Rzi= list()
# for r in reacN1:
#     ti.append(r[0])
#     Rzi.append(r[1])
# ## Show diagram
# import matplotlib.pyplot as plt
# plt.plot(ti, Rzi)
# plt.title("Nodal reaction.")
# plt.xlabel('T')
# plt.ylabel('Reaction')
# plt.show()
