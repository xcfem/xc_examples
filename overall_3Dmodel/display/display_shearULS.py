# -*- coding: utf-8 -*-
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
from postprocess.xcVtk import vtk_graphic_base
from postprocess import output_handler

# local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import env_config as env
import model_gen as model #FE model generation

#Load properties to display:
model.modelSpace.readControlVars(inputFileName= env.cfg.projectDirTree.getVerifShearFile())

#  Config
arguments= ['CF']       #Possible arguments: 'CF', 'N', 'My', 'Mz', 'Mu', 'Vy',
                     #'Vz', 'theta', 'Vcu', 'Vsu', 'Vu'
sets2Disp=[model.wall,model.foot,model.decklv1,model.decklv2]  #Sets of shell elements to be displayed

rgMinMax=(0,1.0)     #truncate values to be included in the range
                     #(if None -> don't truncate)
cameraParameters= vtk_graphic_base.CameraParameters('XYZPos')
rgMinMax=(0,1.0)     #truncate values to be included in the range
                     #(if None -> don't truncate)
#  End config
                                 
oh.outputStyle.cameraParameters= cameraParameters
for st in sets2Disp:
    for arg in arguments:
        model.out.displayFieldDirs1and2(limitStateLabel=lsd.shearResistance.label,argument=arg,setToDisplay= st,component=None,fileName=None, defFScale=0.0,rgMinMax=rgMinMax)





