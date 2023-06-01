# -*- coding: utf-8 -*-
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
from postprocess.xcVtk import vtk_graphic_base
from postprocess.xcVtk.FE_model import quick_graphics as qg
from postprocess.config import default_config

# local modules
import sys
workingDirectory= default_config.findWorkingDirectory()+'/' #search env_config.py
sys.path.append(workingDirectory)
import env_config as env
import model_gen as model #FE model generation

#Load properties to display:
model.modelSpace.readControlVars(inputFileName= env.cfg.projectDirTree.getVerifShearFile())

#  Config
arguments= ['CF']      #Available arguments:
                    # RC elements:'CF', 'N', 'My', 'Mz', 'Mu',
                    #             'Vy', 'Vz', 'theta', 'Vcu', 'Vsu', 'CF'
                    # steel elements: 'CF', 'Vy'
sets2DispRes= [model.beamXconcr,model.beamY,model.columnZconcr]   #sets of linear elements to display results
setDisp=model.overallSet   #set of elements (any type) to be displayed
cameraParameters= vtk_graphic_base.CameraParameters('XYZPos')
model.out.outputStyle.cameraParameters= cameraParameters

#  End config 

for st in sets2DispRes:
    for arg in arguments:
        model.out.displayBeamResult(attributeName=lsd.shearResistance.label,itemToDisp=arg,beamSetDispRes=st,setToDisplay=setDisp,caption=None,fileName=None,defFScale=0.0,defaultDirection='J')
