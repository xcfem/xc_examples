from postprocess.config import default_config

# import local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import xc_model as xcM

# Common variables
out=xcM.out

out.displayNodeValueDiagram(itemToDisp= 'k_x', setToDisplay=None,fileName=None,caption= 'Spring stiffness X direction', defaultDirection= 'X', defaultValue= 0.0,rgMinMax=None)
out.displayNodeValueDiagram(itemToDisp= 'k_y', setToDisplay=None,fileName=None,caption= 'Spring stiffness Y direction', defaultDirection= 'Y', defaultValue= 0.0,rgMinMax=None)
out.displayNodeValueDiagram(itemToDisp= 'k_z', setToDisplay=None,fileName=None,caption= 'Spring stiffness Z direction', defaultDirection= 'X', defaultValue= 0.0,rgMinMax=None)
