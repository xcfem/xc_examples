# -*- coding: utf-8 -*-
''' Test based on the example «Elastic Response Spectra» by Amir Hossein 
Namadchi.

See https://github.com/AmirHosseinNamadchi/OpenSeesPy-Examples/blob/master/Elastic%20Response%20Spectra.ipynb
'''
import os
import json
import numpy as np
import xc
from model import predefined_spaces
from materials import typical_materials
from solution import predefined_solutions
import matplotlib.pyplot as plt

def analyze_SDOF(period, damping_ratio):
    
    # natural frequency
    omega = (2*np.pi)/period
    # stiffness
    k = omega**2
    # Damping
    c = 2*damping_ratio*omega
    
    # Model Definition
    feProblem= xc.FEProblem()
    preprocessor=  feProblem.getPreprocessor
    nodeHandler= preprocessor.getNodeHandler
    modelSpace= predefined_spaces.SolidMechanics1D(nodeHandler)

    n1= modelSpace.newNode(0.0)
    n2= modelSpace.newNode(0.0)
    matElast= typical_materials.defElasticMaterial(preprocessor, name= "matElast", E= k)
    modelSpace.setDefaultMaterial(matElast)
    modelSpace.setElementDimension(1)
    zl= modelSpace.newElement('ZeroLength', [n1.tag, n2.tag])

    # unit mass is assumed
    n2.mass= xc.Matrix([[1.0]])  # node mass matrix.

    # Rayleigh damping factors.
    alphaM= c # factor applied to elements or nodes mass matrix
    betaK= 0.0 # factor applied to elements current stiffness matrix.
    betaKinit= 0.0 # factor applied to elements initial stiffness matrix.
    betaKcomm= 0.0 # factor applied to elements committed stiffness matrix.
    rayleigh= xc.RayleighDampingFactors(alphaM, betaK, betaKinit, betaKcomm)
    # print('damping factors: ', rayleigh)
    # preprocessor.getDomain.setRayleighDampingFactors(rayleigh)
    #zl.setRayleighDampingFactors(rayleigh)
    #zl.setUseRayleighDampingFlag(1) # Compute the element damping matrix
                                    # from its damping coefficients.
    n2.setRayleighDampingFactor(alphaM)

    modelSpace.fixNode0(n1.tag)

    ## Loading
    dt= 0.02
    # loads definition
    loadHandler= preprocessor.getLoadHandler
    lPatterns= loadHandler.getLoadPatterns
    ts= lPatterns.newTimeSeries("constant_ts","ts")
    gm= lPatterns.newLoadPattern("uniform_excitation","gm")
    mr= gm.motionRecord
    hist= mr.history
    timeValues= el_centro_raw[:,0]
    accelerationValues= list(el_centro_raw[:,1]*g)
    accel= lPatterns.newTimeSeries("path_ts","accel")
    accel.path= xc.Vector(accelerationValues)
    accel.timeIncr= timeValues[1]-timeValues[0] 
    hist.accel= accel
    hist.delta= dt # Time integration step.
    #We add the load case to domain.
    lPatterns.addToDomain(gm.name)

    preprocessor.getDomain.setTime(timeValues[0])
    solProc= predefined_solutions.PlainLinearNewmark(feProblem, numSteps= 1, timeStep= dt, constraintHandlerType= 'transformation', maxNumIter= 10, printFlag= 0)
    solProc.setup()
    analysis= solProc.getAnalysis()
    
    results= {'D':[],'V':[], 'A':[]}
    for i in range(len(timeValues)):
        analysis.analyze(1, dt)
        results['D'].append(n2.getDisp[0])
        results['V'].append(n2.getVel[0])
        results['A'].append(n2.getAccel[0])    
        
    return {'SD': np.max(np.abs(results['D'])),
            'SV': np.max(np.abs(results['V'])),
            'SA': np.max(np.abs(results['A']))}

# Loading El Centro EQ data (North-south component)
el_centro_raw= np.loadtxt('elCentro.txt')

# Plot accelerogram.
plt.figure(figsize=(15,3))
plt.plot(el_centro_raw[:,0], el_centro_raw[:,1], color='k')

plt.ylabel('$\ddot{d_g} (g)$', {'size':14})
plt.xlabel('Time (sec)', {'fontstyle':'italic','size':13})

plt.grid()
plt.yticks(fontsize= 14)
plt.xticks(fontsize= 14)
plt.xlim([0.0, el_centro_raw[-1,0]]);
plt.show()

# Define a period range below
T_min= 0.00001
T_max= 5
dT= 0.05
# a list of damping ratios to be included
zeta_list= np.array([0.02, 0.03, 0.05])


# Base units
cm= 1.0
sec= 1.0
# Gravitational constant
g= 981*cm/sec**2

# Use nested loops to analyse the system for various damping ratios and periods.
data_frame = dict()

for z in zeta_list:    
    # re-initialization
    resp = {'T':[0],'SD':[0], 'SV':[0], 'SA':[0]}
    
    for T in np.arange(T_min, T_max, dT):
        SR = analyze_SDOF(T, z)
        resp['SD'].append(SR['SD'])
        resp['SV'].append(SR['SV'])
        resp['SA'].append(SR['SA'])
        resp['T'].append(T)
    
    # Appending keys and values dynamically
    data_frame[z] = resp
    print('Done with zeta= '+str(z)+'!')

# Save ouput as reference.
outputPath= './'#'/tmp'
fname= os.path.basename(__file__)
jsonFileName= outputPath+'/'+fname.replace('.py', '.json')
with open(jsonFileName, 'w') as f:
    json.dump(data_frame, f)
print('XXX continue here.')
    
# Graphic output.
## Displacment -----------
plt.figure(figsize=(14,5))

[plt.plot(data_frame[z]['T'], data_frame[z]['SD'],
          label=('$\zeta$ = '+str(z))) for z in zeta_list]

plt.ylabel('Displacement (cm)', {'fontstyle':'italic','size':14})
plt.xlabel('Period (sec)', {'fontstyle':'italic','size':14})
plt.legend()
plt.grid()
plt.yticks(fontsize = 14)
plt.xticks(fontsize = 14)
plt.title('Displacement Response Spectrum',
          {'fontstyle':'italic','size':18});
plt.show()

# Velocity ------------
plt.figure(figsize=(14,5))

[plt.plot(data_frame[z]['T'], data_frame[z]['SV'],
          label=('$\zeta$ = '+str(z))) for z in zeta_list]

plt.ylabel('Velocity (cm/sec)', {'fontstyle':'italic','size':14})
plt.xlabel('Period (sec)', {'fontstyle':'italic','size':14})
plt.legend()
plt.grid()
plt.yticks(fontsize = 14)
plt.xticks(fontsize = 14)
plt.title('Veloctiy Response Spectrum', 
          {'fontstyle':'italic','size':18});
plt.show()

# Acceleration ------------
plt.figure(figsize=(14,5))

[plt.plot(data_frame[z]['T'], np.array(data_frame[z]['SA'])/g,
          label=('$\zeta$ = '+str(z))) for z in zeta_list]

plt.ylabel('Acceleration (g)', {'fontstyle':'italic','size':14})
plt.xlabel('Period (sec)', {'fontstyle':'italic','size':14})
plt.legend()
plt.grid()
plt.yticks(fontsize = 14)
plt.xticks(fontsize = 14)
plt.title('Acceleration Response Spectrum',
          {'fontstyle':'italic','size':18});
plt.show()
