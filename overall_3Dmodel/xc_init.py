
import sys
import xc
from model import predefined_spaces
# Default configuration of environment variables.
from postprocess.config import default_config
from postprocess import output_styles as outSty
from postprocess import output_handler as outHndl
# import local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
sys.path.append(workingDirectory)
import env_config as env
sty=outSty.OutputStyle() 
FEcase= xc.FEProblem()
prep=FEcase.getPreprocessor
nodes= prep.getNodeHandler
elements= prep.getElementHandler
elements.dimElem= 3
# Problem type
modelSpace= predefined_spaces.StructuralMechanics3D(nodes) #Defines the
# dimension of the space: nodes by three coordinates (x,y,z) and 
# six DOF for each node (Ux,Uy,Uz,thetaX,thetaY,thetaZ)
out=outHndl.OutputHandler(modelSpace,sty)
