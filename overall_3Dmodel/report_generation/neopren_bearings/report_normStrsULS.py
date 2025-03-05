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
#setsShEl=[model.platform030]
#setsShEl=[model.slab065Pier1,model.slab065Pier2]
#setsShEl=[model.strips030]
setsShEl=[model.portSlabStripsZA1,model.portSlabStripsZA2]
# Ordered list of arguments to be included in the report
# Possible arguments: 'CF', 'N', 'My', 'Mz'
argsShEl= ['CF','N', 'My'] ; rgMinMax=None
argsShEl= ['CF']; rgMinMax=[0,1]

# Ordered list of lists [set of beam elements, view to represent this set] to
# be included in the report. 
# The sets are defined in model_data.py as instances of
# utils_display.setToDisplay and the possible views are: 'XYZPos','XNeg','XPos',
# 'YNeg','YPos','ZNeg','ZPos'  (defaults to 'XYZPos')
#setsBmEl=[model.columnsT1,model.columnsT2,model.columnsT3,model.columnsT4]
#setsBmEl=[model.lintelZA1,model.lintelZA3,model.lintelZA2,model.lintelZA4,model.lintelZA5]
setsBmEl=[]
# Ordered list of lists [arguments, scale to represent the argument] to be
# included in the report for beam elements
# Possible arguments: 'CF', 'N', 'My', 'Mz'
argsBmEl=['CF','N','My','Mz']

report=rprt.ReportGenerator(model.modelSpace,env.cfg)

report.checksReport(limitStateLabel,setsShEl,argsShEl,setsBmEl,argsBmEl,rgMinMax=rgMinMax)

