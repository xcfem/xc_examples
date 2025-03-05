# -*- coding: utf-8 -*-
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
from postprocess.xcVtk import vtk_graphic_base
from postprocess.config import default_config
# import local modules
workingDirectory= default_config.setWorkingDirectory() 
import env_config as env
import xc_init
import xc_sets as xcS
# Common variables
out=xc_init.out ; modelSpace=xc_init.modelSpace ; prep=xc_init.prep
#
sets2Disp=[xcS.wallSet]
arguments=[ 'CF']     #Possible arguments: 'CF', 'N', 'My', 'Mz', 's_rmax', 'sigma_s', 'sigma_c', 'wk'
rgMinMax=(0,1.0)#None
cameraParameters= vtk_graphic_base.CameraParameters('XYZPos')
out.outputStyle.cameraParameters= cameraParameters
modelSpace.readControlVars(inputFileName=env.cfg.projectDirTree.getVerifCrackFreqFile())
for st in sets2Disp:
    for arg in arguments:
        out.displayFieldDirs1and2(limitStateLabel=lsd.freqLoadsCrackControl.label,argument=arg,setToDisplay=st,component=None,fileName=None,defFScale=0.0,rgMinMax=rgMinMax) 




