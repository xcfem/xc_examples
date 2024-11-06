from materials.ehe import EHE_materials
#from materials.sia262 import SIA262_materials
from materials.ec3 import EC3_materials

#Materials data
concrete=EHE_materials.HA30
reinfSteel=EHE_materials.B500S
S235JR= EC3_materials.S235JR
S235JR.gammaM= 1.00

# Soil
wModulus=20e7 # Winkler modulus of the foundation (springs in Z direction)
cRoz=0.2 #  fraction of the Winkler modulus to apply for friction in the contact plane (springs in X, Y directions)
