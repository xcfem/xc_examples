# -*- coding: utf-8 -*-

exec(open("./xc_model.py").read()) #FE model generation

# Graphic stuff.
from postprocess import output_handler
oh= output_handler.OutputHandler(modelSpace)

oh.displayBlocks()#setToDisplay= beamSet)
oh.displayFEMesh()
#oh.displayLocalAxes(setToDisplay= beamSet)
# oh.displayStrongWeakAxis(setToDisplay= beamSet)
# oh.displayLoads()#setToDisplay= lvlBlindFasciaSet)
# oh.displayReactions(reactionCheckTolerance= 1e-4)
# oh.displayDispRot(itemToDisp='uZ', defFScale= 10.0)
#oh.displayIntForcDiag(itemToDisp= 'Mz', setToDisplay= beamSet)
#oh.displayIntForcDiag(itemToDisp= 'Qy', setToDisplay= xcTotalSet)
#oh.displayIntForcDiag(itemToDisp= 'Mz', setToDisplay= xcTotalSet)
#oh.displayIntForcDiag(itemToDisp= 'T', setToDisplay= beamSet)
