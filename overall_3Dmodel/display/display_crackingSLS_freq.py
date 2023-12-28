# -*- coding: utf-8 -*-
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
from postprocess.xcVtk import vtk_graphic_base
from postprocess.config import default_config

# local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import env_config as env
import model_gen as model #FE model generation

#Load properties to display:
model.modelSpace.readControlVars(inputFileName= env.cfg.projectDirTree.getVerifCrackFreqFile())

#  Config
arguments=[ 'getCF']     #Possible arguments: 'getCF', 'getMaxN', 'getMaxSteelStress'
sets2Disp=[model.wall,model.foot,model.decklv1,model.decklv2]  #Sets of shell elements to be displayed
rgMinMax=(0,1.0)     #truncate values to be included in the range
                     #(if None -> don't truncate)
cameraParameters= vtk_graphic_base.CameraParameters('XYZPos')
model.out.outputStyle.cameraParameters= cameraParameters
#  End config 

for st in sets2Disp:
    for arg in arguments:
        model.out.displayFieldDirs1and2(limitStateLabel=lsd.freqLoadsCrackControl.label,argument=arg,setToDisplay=st,component=None,fileName=None,defFScale=0.0,rgMinMax=rgMinMax) 




