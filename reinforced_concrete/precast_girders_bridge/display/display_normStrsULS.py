# -*- coding: utf-8 -*-
from postprocess.config import default_config
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
# from postprocess.xcVtk import vtk_graphic_base
# from postprocess import output_handler

#FE model generation
exec(default_config.compileCode('../xc_model.py'))

#choose env_config:
#Load properties to display:
exec(open(cfg.projectDirTree.getVerifNormStrFile()).read())


#  Config
argument= 'My' #Possible arguments: 'CF', 'N', 'My','Mz'

#setDisp= bridgeDeckSet
#setDisp= girderSet
#setDisp= girderWebs
#setDisp= websLowerEdge
setDisp= diaphragmSet
#setDisp= girderBottomFlanges
#setDisp= girderTapperedBottoms

rgMinMax= None
#rgMinMax=[0, 1.01]     #truncate values to be included in the range
                       #(if None -> don't truncate)
                     
#  End config 

# if(argument=='My'):
#     rgMinMax= [-140e3,140e3]

#oh.displayLocalAxes(setToDisplay=setDisp)
oh.displayFieldDirs1and2(limitStateLabel=lsd.normalStressesResistance.label,argument=argument,setToDisplay=setDisp,component=None,fileName=None,defFScale=0.0,rgMinMax=rgMinMax)




