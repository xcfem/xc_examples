# -*- coding: utf-8 -*-
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
from postprocess import output_handler
from postprocess.config import default_config

# local modules
import sys
workingDirectory= default_config.findWorkingDirectory()+'/' #search env_config.py
sys.path.append(workingDirectory)
import env_config as env

#FE model generation
import model_gen.py as model #FE model generation

#Load properties to display:
import env.cfg.projectDirTree.getVerifFatigueFile()

limitStateLabel= lsd.fatigueResistance.label

#Possible arguments: 'getAbsSteelStressIncrement',  'concreteBendingCF',  'concreteLimitStress',  'shearLimit' , 'concreteShearCF', 'Mu',  'Vu'

argument='getAbsSteelStressIncrement'

setDisp= allShells
oh= output_handler.OutputHandler(modelSpace)
oh.outputStyle.cameraParameters= cameraParameters
oh.displayFieldDirs1and2(limitStateLabel,argument,setToDisplay=setDisp,component=None, fileName= None,defFScale=0.0)



