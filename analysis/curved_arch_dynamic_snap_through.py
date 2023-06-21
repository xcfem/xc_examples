# -*- coding: utf-8 -*-
''' Test based on the numerical examples in "A robust composite time integration scheme for snap-through problems by Yenny Chandra et. al"

The code is based in the OpenSeesPy version written by Amir Hossein Namadchi

https://github.com/AmirHosseinNamadchi/OpenSeesPy-Examples/blob/master/Curved%20arch.ipynb
'''
from __future__ import print_function
from __future__ import division

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2021, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"


import sys
import os
import json
import math
import numpy as np
import xc
from time import process_time
from model import predefined_spaces
from materials import typical_materials
from solution import predefined_solutions
import matplotlib.pyplot as plt

# Check if silent execution has been requested.
argv= sys.argv
silent= False
if(len(argv)>1):
    if 'silent' in argv[1:]:
        silent= True

# Units
mm = 1.0   # milimeters
N = 1.0    # Newtons
sec = 1.0  # Seconds

# Node Coordinates Matrix (size : nn x 3)
node_coords = np.array([[-152.4, 0], [-137.337, 2.91714],
                        [-122.218, 5.53039], [-107.049, 7.8387],
                        [-91.8371, 9.84114], [-76.5878, 11.5369],
                        [-61.3076, 12.9252], [-46.0024, 14.0057],
                        [-30.6787, 14.7777], [-15.3424, 15.2411],
                        [0, 15.3955], [15.3424, 15.2411], 
                        [30.6787, 14.7777], [46.0024, 14.0057],
                        [61.3076, 12.9252], [76.5878, 11.5369], 
                        [91.8371, 9.84114], [107.049, 7.8387], 
                        [122.218, 5.53039], [137.337, 2.91714],
                        [152.4, 0]], dtype = np.float64)*mm

# Modulus of Elasticity
E = 206843*(N/mm**2)
nu= 0.3 # Poisson's ratio.
G= E/(2.0*(1+nu))
# Mass Density
rho = (7.83e-9)*(N*(sec**2)/(mm**4))
# Cross-sectional area, 2nd Moment of Inertia
h= 0.6096
A, I_1 = (12.7*h*mm*mm,
          (1/12)*(12.7*(h**3))*mm**4)

# Problem type
feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor
nodes= preprocessor.getNodeHandler
modelSpace= predefined_spaces.StructuralMechanics2D(nodes)

# Adding nodes to the model object using list comprehensions
archNodes= list()
for nc in node_coords:
    archNodes.append(nodes.newNodeXY(float(nc[0]),float(nc[1])))

# Boundary conditions.
modelSpace.fixNode000(archNodes[0].tag) # first node.
modelSpace.fixNode000(archNodes[-1].tag) # last node.

# Materials definition
section= typical_materials.defElasticShearSection2d(preprocessor, "section",A,E,G,I_1, alpha= 2.42, linearRho= rho*A)

# Mesh generation

## Geometric transformations
trf= modelSpace.newCorotCrdTransf("trf")

## Seed element
elemHandler= preprocessor.getElementHandler
elemHandler.dimElem= 2 # Bars defined in a two-dimensional space.
elemHandler.defaultMaterial= section.name
elemHandler.defaultTransformation= trf.name

## Adding Elements
archElements= list() # Element container.
previousNode= archNodes[0]
for n in archNodes[1:]:
    beam2d= elemHandler.newElement("ElasticBeam2d",xc.ID([previousNode.tag,n.tag]))
    beam2d.h= h
    previousNode= n
    archElements.append(beam2d)

# Define loads
## load function (Applied @ top node)
F = lambda t: (t if t<=8 else 8)*N

## Dynamic Analysis Parameters
dt= 0.0001
time= 15
timeValues= list()
forceValues= list()
t= 0.0
while (t<time):
    timeValues.append(t)
    forceValues.append(F(t))
    t+= dt
loadHandler= preprocessor.getLoadHandler
lPatterns= loadHandler.getLoadPatterns
ts= lPatterns.newTimeSeries("path_time_ts","ts")
ts.path= xc.Vector(forceValues)
ts.time= xc.Vector(timeValues)
#### Create load pattern LP.
lp= lPatterns.newLoadPattern('default', 'lp')
lp.newNodalLoad(archNodes[10].tag, xc.Vector([0,-1,0]))
modelSpace.addLoadCaseToDomain(lp.name)

solProc= predefined_solutions.TransformationTRBDF2NewtonRaphson(feProblem, maxNumIter= 100, numSteps= 1, timeStep= dt)
solProc.setup()
analysis= solProc.analysis

# results container
timeLst= list() # time stations for plotting
dList= list() # vertical displacements of the top node


# start the timer
tic= process_time()

for i in range(len(timeValues)):
    analysis.analyze(1, dt)
    timeLst.append(preprocessor.getDomain.getTimeTracker.getCurrentTime)
    dList.append(archNodes[10].getDisp[1])
    

# stop the timer
toc = process_time()

# Read reference data from disk.
pth= os.path.dirname(__file__)
if(not pth):
  pth= "."
refDataFilePath= pth+'/curved_arch_dynamic_snap_through_ref_data.json'
refData= json.load( open(refDataFilePath, 'r'))
refTimeLst= refData['timeLst']
refDList= refData['dList']

# Compute error
timeRMSE = math.sqrt(np.square(np.subtract(timeLst,refTimeLst)).mean())
dispRMSE = math.sqrt(np.square(np.subtract(dList,refDList)).mean())


'''
'''
from misc_utils import log_messages as lmsg
fname= os.path.basename(__file__)
if (timeRMSE<1e-3) and (dispRMSE<1e-3):
   print('test '+fname+': ok.')
else:
    lmsg.error(fname+' ERROR.')

if not silent:
    print('timeRMSE= ', timeRMSE)
    print('dispRMSE= ', dispRMSE)
    print('Time elapsed:',toc-tic, 'sec')
    # print(timeValues)
    # print(forceValues)
    # Graphic stuff.
    ## Finite element mesh.
    from postprocess import output_handler
    oh= output_handler.OutputHandler(modelSpace)

    oh.displayFEMesh()
    # oh.displayDispRot(itemToDisp='uX',setToDisplay=pile)
    # oh.displayIntForcDiag(itemToDisp='Vy',setToDisplay=pile)
    # oh.displayIntForcDiag(itemToDisp='Mz',setToDisplay=pile)

    ## Results.
    plt.figure(figsize=(14,5))
    ax1 = plt.axes()  # standard axes
    plt.grid()
    plt.yticks(fontname = 'Liberation Sans', fontsize = 14)
    plt.xticks(fontname = 'Liberation Sans', fontsize = 14)
    plt.title('Time history of vertical displacement of the top node',
              {'fontname':'Liberation Sans',
               'fontstyle':'italic','size':18});

    ax2 = plt.axes([0.65, 0.60, 0.2, 0.25])


    ax1.plot(timeLst, dList,'k')
    ax2.plot(timeLst, dList,'k')
    rightLimit= time-1
    leftLimit= rightLimit-0.5
    ax2.set_xlim(left=leftLimit, right=rightLimit)
    ax2.set_ylim(bottom=-15, top=-30)

    ax1.set_xlabel('Time (sec)', {'fontname':'Liberation Sans',
                                'fontstyle':'italic','size':14})
    ax1.set_ylabel('Vertical Displacement (mm)', {'fontname':'Liberation Sans',
                                     'fontstyle':'italic','size':14});
    plt.show()
