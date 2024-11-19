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

#Load properties to display:
model.modelSpace.readControlVars(inputFileName= env.cfg.projectDirTree.getVerifCrackQpermFile())

limitStateLabel= lsd.quasiPermanentLoadsCrackControl.label

# Ordered list of sets (defined in model_data.py as instances of
# utils_display.setToDisplay) to be included in the report
setsShEl=[]
# Ordered list of arguments to be included in the report
# Possible arguments SIA: 'getMaxSteelStress', 'getCF'
# Possible arguments EHE: 'CF','wk','s_rmax','sigma_s','sigma_c','N','My','Mz'
argsShEl=['CF','wk','sigma_s','sigma_c','N','My','Mz'] 

# Ordered list of lists [set of beam elements, view to represent this set] to
# be included in the report. 
# The sets are defined in model_data.py as instances of
# utils_display.setToDisplay and the possible views are: 'XYZPos','XNeg','XPos',
# 'YNeg','YPos','ZNeg','ZPos'  (defaults to 'XYZPos')
setsBmEl=[model.pilotesT1A,model.pilotesT1B,model.pilotesT2,model.pilotesT3,model.pilotesT4]
#setsBmEl=[model.fbeamZA1,model.fbeamZA4a,model.fbeamZA4b,model.fbeamZA2,model.fbeamZA3,model.fbeamZA6,model.fbeamZA5]


# Ordered list of lists [arguments, scale to represent the argument] to be
# included in the report for beam elements
# Possible arguments SIA: 'getMaxSteelStress', 'getCF'
# Possible arguments EHE: 'CF','wk','s_rmax','sigma_s','sigma_c','N','My','Mz'
# argsBmEl=['getCF','getMaxSteelStress']
argsBmEl=['CF','wk','sigma_s','sigma_c','N','My','Mz'] 
report=rprt.ReportGenerator(model.modelSpace,env.cfg)
report.checksReport(limitStateLabel,setsShEl,argsShEl,setsBmEl,argsBmEl)


