# -*- coding: utf-8 -*-
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
from postprocess.xcVtk import vtk_graphic_base
from postprocess.config import default_config

# local modules
import sys
workingDirectory= default_config.findWorkingDirectory()+'/' #search env_config.py
sys.path.append(workingDirectory)
import env_config as env
import model_gen as model #FE model generation

#Load properties to display:
model.modelSpace.readControlVars(inputFileName= env.cfg.projectDirTree.getVerifNormStrFile())

#  Config
arguments=[ 'CF' ]      #Possible arguments:
                     #RC elem: 'CF', 'N', 'My', 'Mz'
                     #steel elem: 'CF', 'N', 'My', 'Mz','Ncrd','McRdy','McRdz',
                     #            'MvRdz','MbRdz','chiLT'
sets2DispRes= [model.beamXconcr,model.beamY,model.columnZconcr]   #sets of linear elements to display results
setDisp=model.overallSet   #set of elements (any type) to be displayed

cameraParameters= vtk_graphic_base.CameraParameters('XYZPos')
model.out.outputStyle.cameraParameters= cameraParameters
#  End config 

for st in sets2DispRes:
    for arg in arguments:
        model.out.displayBeamResult(attributeName=lsd.normalStressesResistance.label, itemToDisp=arg, beamSetDispRes=st, setToDisplay=setDisp, caption=None, fileName=None, defFScale=0.0,defaultDirection='J')



