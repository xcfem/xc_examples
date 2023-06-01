# -*- coding: utf-8 -*-
''' Display normal stresses checking results.'''
import sys
from postprocess.config import default_config
from postprocess import limit_state_data as lsd
from postprocess.control_vars import *

import xc_model # Import finite element model.

#Load properties to display:
preprocessor= xc_model.modelSpace.preprocessor
exec(open(xc_model.cfg.projectDirTree.getVerifNormStrFile()).read())


#  Config
argument= 'CF' #Possible arguments: 'CF', 'N', 'My','Mz'

#setDisp= xc_model.model_geometry.deckSlabSet
setDisp= xc_model.concreteSet

rgMinMax= None
#rgMinMax=[0, 1.01]     #truncate values to be included in the range
                       #(if None -> don't truncate)
                     
#  End config 

# if(argument=='My'):
#     rgMinMax= [-140e3,140e3]

#xc_model.oh.displayLocalAxes(setToDisplay=setDisp)
xc_model.oh.displayBeamResult(attributeName=lsd.normalStressesResistance.label, itemToDisp= argument, beamSetDispRes= setDisp,setToDisplay=setDisp, fileName=None, defFScale=0.0)
