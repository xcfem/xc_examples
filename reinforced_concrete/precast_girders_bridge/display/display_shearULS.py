# -*- coding: utf-8 -*-
from postprocess.config import default_config
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd

#FE model generation
exec(default_config.compileCode('../xc_model.py'))

#choose env_config:
#Load properties to display:
exec(open(cfg.projectDirTree.getVerifShearFile()).read())


#  Config
argument= 'CF' #Possible arguments: 'CF', 'N', 'My', 'Mz', 'Mu', 'Vy',
               # 'Vz', 'theta', 'Vcu', 'Vsu', 'Vu'

setDisp= bridgeDeckSet
#setDisp= girderSet
#setDisp= girderWebs
#setDisp= girderBottomFlanges
#setDisp= girderTapperedBottoms

#rgMinMax=[0,0.97]     #truncate values to be included in the range
rgMinMax=None                     #(if None -> don't truncate)
                     
#  End config 


oh.displayFieldDirs1and2(limitStateLabel=lsd.shearResistance.label,argument=argument,setToDisplay=setDisp,component=None,fileName=None,defFScale=0.0,rgMinMax=rgMinMax)




