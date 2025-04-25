from materials.ec2 import EC2_materials
from materials.ec3 import EC3_materials

#Materials data
concrete=EC2_materials.C30
strSeel= EC3_materials.S235JR
strSeel.gammaM= 1.00
#S335JR= EC3_materials.S335JR
#S335JR.gammaM= 1.00
# Shear connections (SC) properties
fu_SC=450e6 #[N/m2]
fi_SC=19e-3 #[m] diameter
h_SC=125e-3 # [m] height

