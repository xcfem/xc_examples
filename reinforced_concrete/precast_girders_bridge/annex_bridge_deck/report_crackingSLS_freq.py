# -*- coding: utf-8 -*-
from postprocess.config import default_config
from postprocess.control_vars import *
from postprocess import limit_state_data as lsd
from postprocess.reports import report_generator as rprt

#FE model generation
exec(default_config.compileCode('../xc_model.py'))

#choose env_config:
#Load properties to display:
exec(default_config.compileCode(cfg.projectDirTree.getVerifCrackFreqFile()))


#  Config
# Ordered list of sets (defined in model_data.py as instances of
# utils_display.setToDisplay) to be included in the report
setsShEl=[setArmMurEstr]
# Ordered list of arguments to be included in the report
# Possible arguments: 'getMaxSteelStress', 'getCF'
argsShEl= ['getCF','getMaxSteelStress']
# Ordered list of lists [set of beam elements, view to represent this set] to
# be included in the report. 
# The sets are defined in model_data.py as instances of
# utils_display.setToDisplay and the possible views are: 'XYZPos','XNeg','XPos',
# 'YNeg','YPos','ZNeg','ZPos'  (defaults to 'XYZPos')

setsBmEl=[]

# Ordered list of lists [arguments, scale to represent the argument] to be
# included in the report for beam elements
# Possible arguments: 'getMaxSteelStress', 'getCF'

argsBmEl=[]
                     
#  End config 
limitStateLabel=lsd.freqLoadsCrackControl.label
report.checksReport(limitStateLabel, setsShEl, argsShEl, setsBmEl, argsBmEl)





