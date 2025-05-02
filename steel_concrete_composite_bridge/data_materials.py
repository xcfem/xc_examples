from materials.ec2 import EC2_materials
from materials.ec3 import EC3_materials
# import local modules
from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import data_geom as datG

#Materials data
concrete=EC2_materials.C30
strSteel= EC3_materials.S235JR
strSteel.gammaM= 1.00
SCsteel=EC3_materials.bolt4dot8Steel
SCsteel.gammaM= 1.00
#S335JR= EC3_materials.S335JR
#S335JR.gammaM= 1.00
# Shear connections (SC) properties
#fu_SC=450e6 #[N/m2]
fi_SC=19e-3 #[m] diameter
#h_SC=125e-3 # [m] height

# Stiffness diaphragms
K_BF_ID=11776e3 # [N/m] siffness diaphragm bottom flange
K_TF_ID=650656e3 # [N/m] siffness diaphragm top flange
