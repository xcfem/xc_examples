'''
This scipt calculates the maximum acceleration for a single-degree-of-freedom 
model with varying natural periods, forced into motion by the same dinamic 
event, that is given as parameter as an earthquake's time-history recording.

The file used in this example as time-history input is organized in the 
following columns:
   Time[s] Acceleration comp. N30W [g]  Acc. comp. E30W [g]  Acc. comp. V [g]

The sprectrum calculated in this script corresponds to component N30W [g]
Usually, the input consists in a succession of accelerations values for which time-step is known. 

# As a result, the response spectrum period-acceleration is plotted
'''
import numpy as np
import matplotlib.pyplot as plt
# from scipy.constants import g
import xc
from model import predefined_spaces
from materials import typical_materials
from solution import predefined_solutions
from misc_utils import log_messages as lmsg

solve= True
# Data
goundAccSeriesFile= './LOR_20110511_164726.acc' # file containinig the ground acceleration values. 

periodRange=[0.01,5] # minimum and max. period in seconds
nPeriods=250 # number of periods to be processed
damping_ratio= .05 # Damping ratio. 

## Read de time-history file
lorca_t= list()
lorca_a_norte= list()
lorca_a_este= list()
lorca_a_vert= list()
def is_number(s):
    try:
        float(s)
    except ValueError:  # Failed
        return False
    else:  # Succeeded
        return True
with open(goundAccSeriesFile, 'r') as f:
    for line in f:
        fields= line.split(' ')
        if(is_number(fields[0])):
            lorca_t.append(float(fields[0]))
            lorca_a_norte.append(float(fields[1]))#*g)
            lorca_a_este.append(float(fields[2]))#*g)
            lorca_a_vert.append(float(fields[3]))#*g)
##   
timeVals=[t for t in lorca_t]
grAccelVals=[a for a in lorca_a_norte]
# End data.
timeStep= timeVals[1]-timeVals[0]

# Compute the periods to consider in the spectrum.
periods=np.linspace(periodRange[0],periodRange[1],num=nPeriods)
periods=[round(T,3) for T in periods]
caseDct=dict() # dictionary that stores for each period the element created and the maximum acceleration calculated

feProblem= xc.FEProblem()
prep=  feProblem.getPreprocessor
nodeHandler= prep.getNodeHandler
modelSpace= predefined_spaces.SolidMechanics1D(nodeHandler)

elements=prep.getElementHandler
elements.dimElem= 1
loadHandler= prep.getLoadHandler
# Create zero-length elements for all the periods and append to dictionary
for T in periods:
    n1= modelSpace.newNodeX(0)
    n2= modelSpace.newNodeX(0)
    mass= 1 # mass
    n2.mass= xc.Matrix([[mass]])  # node mass matrix.
    
    modelSpace.fixNode0(n1.tag)
    omega=2*np.pi/T # angular frequency
    c = 2*damping_ratio*omega # Damping
    # Rayleigh damping factors.
    n2.setRayleighDampingFactor(c)


    K= (omega**2)*mass # stiffness
    matElast= typical_materials.defElasticMaterial(preprocessor= prep, name= "matElast"+str(T), E= K)
    elements.defaultMaterial= matElast.name
    el=elements.newElement("ZeroLength",xc.ID([n1.tag,n2.tag]))
    caseDct[T]={'elem':el,'n2Tag':n2.tag}

# loads definition
lPatterns= loadHandler.getLoadPatterns
ts= lPatterns.newTimeSeries("constant_ts","ts")
gm= lPatterns.newLoadPattern("uniform_excitation","gm")
mr= gm.motionRecord
hist= mr.history
accel= lPatterns.newTimeSeries("path_ts","accel")
accel.path= xc.Vector(grAccelVals)
# IMPORTANT: set the time step of the accelerogram (defaults to 1)
accel.timeIncr= timeVals[1]-timeVals[0] 
print(accel.timeIncr)
hist.accel= accel
hist.delta= timeStep # Time integration step.
#We add the load case to domain.
lPatterns.addToDomain(gm.name)

## Dynamic analysis.
# Define RECORDERS

nodeTags= list()
cAccel= dict()

for T in periods:
    nTag= caseDct[T]['n2Tag']
    nodeTags.append(nTag)
    cAccel[nTag]= list()
    
recAccel= prep.getDomain.newRecorder("node_prop_recorder",None)
recAccel.setNodes(xc.ID(nodeTags))
recAccel.callbackRecord= "cAccel[self.tag].append((self.getDomain.getTimeTracker.getCurrentTime,self.getAccel[0]))"


prep.getDomain.setTime(timeVals[0])
solProc= predefined_solutions.PlainNewmarkNewtonRaphson(feProblem, numSteps= len(timeVals), timeStep= timeStep, convergenceTestTol= 1e-6, maxNumIter= 10, printFlag= 0)
if(solve):
    result= solProc.solve()
    if(result!=0):
        lmsg.error('Dynamic analysis failed.')
        quit()

    for T in periods:
        max_acc=0
        nTag=caseDct[T]['n2Tag']
        resAcc=cAccel[nTag]
        nodeAbsAcc=[abs(res[1]) for res in  resAcc]
        maxAccel= max(nodeAbsAcc)
        caseDct[T]['maxAccel']= maxAccel

    maxAccelPeriods=[caseDct[T]['maxAccel'] for T in periods]

# 5. Visualización
# Plot accelerogram
plt.figure(figsize=(100, 5))
plt.plot(timeVals, hist.accel.getPathList())
plt.title('Accelerogram.')
plt.xlabel('t(s)')
plt.ylabel('Acceleration $(m/s^2)$')
plt.xlim(10, 17)  # Zoom en el rango de tiempos de interés
plt.grid(True)
plt.show()

if(solve):
    # Plot period spectogram
    plt.figure(figsize=(10, 5))
    plt.plot(periods, maxAccelPeriods)
    plt.title('Period spectrum of the accelerogram.')
    plt.xlabel('Period (s)')
    plt.ylabel('Acceleration (g)')#$(m/s^2)$')
    plt.xlim(0,5) # Zoom en el rango de periodos de interés
    plt.fill_between(periods,maxAccelPeriods,alpha=0.1)
    plt.grid(True)
    plt.show()



