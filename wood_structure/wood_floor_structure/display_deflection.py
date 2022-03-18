# -*- coding: utf-8 -*-

exec(open("./xc_model.py").read()) #FE model generation
from serviceability_limit_states import ibc_2018_sls
from colorama import Fore
from colorama import Style

# Solution
# Linear static analysis.
analysis= predefined_solutions.simple_static_linear(FEcase)
#analysis= predefined_solutions.penalty_modified_newton(FEcase)

def getDeflectionLimit(span, ibcLoadCase):
    loadComb= deflectionLoadCombinations[ibcLoadCase]
    dl= ('deadLoad' in loadComb)
    ll= ('liveLoad' in loadComb)
    sl= ('snowLoad' in loadComb)
    wl= ('windLoad' in loadComb)
    return ibc_2018_sls.getDeflectionLimit(span= span, memberType= 'Roof', memberSubType= 'NonPlasterCeiling', deadLoad= dl, liveLoad= ll, snowLoad= sl, windLoad= wl)

#span= 5.476
span= 6.906
worstCase= None
worstDeflection= 0.0
for key in deflectionLoadCombinations:
    loadCaseName= 'SLS'+key
    modelSpace.addLoadCaseToDomain(loadCaseName)
    deflectionLimit= getDeflectionLimit(span, key)
    result= analysis.analyze(1)
    maxDeflection= 0.0
    for l in xcTotalSet.lines:
        for n in l.nodes:
            currentPos= n.getCurrentPos3d(1.0)
            deflection= l.dist(currentPos)
            maxDeflection= max(maxDeflection, deflection)
    maxDeflection*= 1.2
    if(abs(maxDeflection)>worstDeflection):
        worstDeflection= abs(maxDeflection)
        worstCase= loadCaseName
    deflectionOk= (maxDeflection<=deflectionLimit)
    outputStr= 'max. deflection ('+loadCaseName+'): '+str(maxDeflection*1e3)+ ' mm (L/'+str(span/maxDeflection)+') deflection limit: '+ str(deflectionLimit*1e3)+ 'mm (L/'+str(span/deflectionLimit)+') => '
    if(deflectionOk):
        print(Fore.GREEN+outputStr+'OK'+Style.RESET_ALL)
    else:
        print(Fore.RED+outputStr+'KO'+Style.RESET_ALL)
    modelSpace.removeLoadCaseFromDomain(loadCaseName)
    modelSpace.revertToStart()

# Display worst case.
## Solve (again).
modelSpace.addLoadCaseToDomain(worstCase)
# Solution
# Linear static analysis.
analysis= predefined_solutions.simple_static_linear(FEcase)
#analysis= predefined_solutions.penalty_modified_newton(FEcase)
result= analysis.analyze(1)
# failedNode= modelSpace.locateEquationNumber(269)
# failedPos= failedNode.getInitialPos3d
# print(failedNode.tag, failedPos)
# quit()

# Graphic stuff.
from postprocess import output_handler
oh= output_handler.OutputHandler(modelSpace)

# oh.displayBlocks()#setToDisplay= beamSet)
# oh.displayFEMesh()
#oh.displayLocalAxes(setToDisplay= beamSet)
# oh.displayStrongWeakAxis(setToDisplay= beamSet)
# oh.displayLoads()#setToDisplay= lvlBlindFasciaSet)
# oh.displayReactions(reactionCheckTolerance= 1e-4)
oh.displayDispRot(itemToDisp='uZ', defFScale= 10.0)#, setToDisplay= longBeamSet)
# oh.displayIntForcDiag(itemToDisp= 'Mz')#, setToDisplay= beamSet)
#oh.displayIntForcDiag(itemToDisp= 'Qy', setToDisplay= xcTotalSet)
#oh.displayIntForcDiag(itemToDisp= 'Mz', setToDisplay= xcTotalSet)
#oh.displayIntForcDiag(itemToDisp= 'T', setToDisplay= beamSet)
