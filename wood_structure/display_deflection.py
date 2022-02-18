# -*- coding: utf-8 -*-

exec(open("./xc_model.py").read()) #FE model generation

loadCaseName= 'SLSEQ1609'
#loadCaseName= 'SLSLIVE'
modelSpace.addLoadCaseToDomain(loadCaseName)

# Solution
# Linear static analysis.
analysis= predefined_solutions.simple_static_linear(FEcase)
#analysis= predefined_solutions.penalty_modified_newton(FEcase)
result= analysis.analyze(1)

maxDeflection= 0.0
for n in beamSet.nodes:
    uZ= abs(n.getDisp[2])
    maxDeflection= max(maxDeflection, uZ)
maxDeflection*= 1.2
span= 6.667
liveLoadReferenceDeflection= span/540
totalLoadReferenceDeflection= span/360
deflectionOk= 'KO'
if(loadCaseName=='SLSLIVE'):
    if(maxDeflection<=liveLoadReferenceDeflection):
        deflectionOk= 'OK'
elif(loadCaseName=='SLSEQ1609'):
    if(maxDeflection<=totalLoadReferenceDeflection):
        deflectionOk= 'OK'
    
print('max. deflection (', loadCaseName,'): ',maxDeflection*1e3, 'mm (L/',span/maxDeflection,') =>', deflectionOk)

# Graphic stuff.
from postprocess import output_handler
oh= output_handler.OutputHandler(modelSpace)

# oh.displayBlocks(setToDisplay= beamSet)
# oh.displayFEMesh()
#oh.displayLocalAxes(setToDisplay= beamSet)
# oh.displayStrongWeakAxis(setToDisplay= beamSet)
#oh.displayLoads()#setToDisplay= lvlBlindFasciaSet)
oh.displayReactions(reactionCheckTolerance= 1e-4)
oh.displayDispRot(itemToDisp='uZ', defFScale= 10.0)
#oh.displayIntForcDiag(itemToDisp= 'Mz', setToDisplay= beamSet)
#oh.displayIntForcDiag(itemToDisp= 'Qy', setToDisplay= xcTotalSet)
#oh.displayIntForcDiag(itemToDisp= 'Mz', setToDisplay= xcTotalSet)
#oh.displayIntForcDiag(itemToDisp= 'T', setToDisplay= beamSet)
