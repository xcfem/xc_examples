# -*- coding: utf-8 -*-
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
from postprocess.reports import report_generator as rprt
from postprocess.config import default_config
import json

# import local modules
import sys
workingDirectory= default_config.findWorkingDirectory()+'/' #search env_config.py
sys.path.append(workingDirectory)
import env_config as env
import xc_model as model #FE model generation

# Load properties to display:
model.modelSpace.readControlVars(inputFileName= env.cfg.projectDirTree.getVerifNormStrFile())

limitStateLabel= lsd.normalStressesResistance.label

# Ordered list of sets (defined in model_data.py as instances of
# utils_display.setToDisplay) to be included in the report
setsShEl=[]
# Ordered list of arguments to be included in the report
# Possible arguments: 'CF', 'N', 'My', 'Mz'
argsShEl= ['CF','N', 'My'] 

# Ordered list of lists [set of beam elements, view to represent this set] to
# be included in the report. 
# The sets are defined in model_data.py as instances of
# utils_display.setToDisplay and the possible views are: 'XYZPos','XNeg','XPos',
# 'YNeg','YPos','ZNeg','ZPos'  (defaults to 'XYZPos')
setsBmEl=[model.pilotesT1A,model.pilotesT1B,model.pilotesT2,model.pilotesT3,model.pilotesT4]+[model.fbeamZA1,model.fbeamZA4a,model.fbeamZA4b,model.fbeamZA2,model.fbeamZA3,model.fbeamZA6,model.fbeamZA5]
# Ordered list of lists [arguments, scale to represent the argument] to be
# included in the report for beam elements
# Possible arguments: 'CF', 'N', 'My', 'Mz'
argsBmEl=['CF','N','My','Mz']

report=rprt.ReportGenerator(model.modelSpace,env.cfg)

report.checksReport(limitStateLabel,setsShEl,argsShEl,setsBmEl,argsBmEl)

