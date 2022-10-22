# -*- coding: utf-8 -*-
from postprocess.config import default_config
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd

#FE model generation
exec(default_config.compileCode('../xc_model.py'))

#choose env_config:
#Load properties to display:
exec(default_config.compileCode(cfg.projectDirTree.getVerifCrackFreqFile()))


#  Config
argument= 'getCF' # Possible arguments: 'getCF', 'getMaxN', 'getMaxSteelStress'
#argument='getMaxN'
argument='getMaxSteelStress'

#setDisp= bridgeDeckSet
#setDisp= girderSet
#setDisp= girderWebs
#setDisp= girderBottomFlanges
#setDisp= girderTapperedBottoms
setDisp= girderWebs

#rgMinMax=[0,1]     #truncate values to be included in the range
rgMinMax=None                     #(if None -> don't truncate)
                     
#  End config 


oh.displayFieldDirs1and2(limitStateLabel=lsd.freqLoadsCrackControl.label, argument=argument, setToDisplay=setDisp, component=None, fileName=None, defFScale=0.0, rgMinMax=rgMinMax)




