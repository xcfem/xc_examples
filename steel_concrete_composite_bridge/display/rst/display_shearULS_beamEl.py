# -*- coding: utf-8 -*-
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
from postprocess.xcVtk import vtk_graphic_base
from postprocess.config import default_config
# local modules
workingDirectory= default_config.setWorkingDirectory() 
import env_config as env
import xc_init
import xc_sets as xcS
# Common variables
out=xc_init.out ; modelSpace=xc_init.modelSpace ; prep=xc_init.prep
#
sets2DispRes=[xcS.columnZconcrSet]
setDisp=xcS.overallSet
arguments= ['Vy']   #Available arguments:
                    # RC:    'CF', 'N', 'My', 'Mz', 'Mu',
                    #        'Vy', 'Vz', 'theta', 'Vcu', 'Vsu', 'CF'
                    # steel: 'CF', 'Vy'
cameraParameters= vtk_graphic_base.CameraParameters('XYZPos')
out.outputStyle.cameraParameters= cameraParameters
modelSpace.readControlVars(inputFileName= env.cfg.projectDirTree.getVerifShearFile())
rgMinMax=None
for st in sets2DispRes:
    for arg in arguments:
        out.displayBeamResult(attributeName=lsd.shearResistance.label,itemToDisp=arg,beamSetDispRes=st,setToDisplay=setDisp,caption=None,fileName=None,defFScale=0.0,defaultDirection='J',rgMinMax=rgMinMax)
