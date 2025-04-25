# Definition of materials for each set of elements
from materials import typical_materials as tm
from materials.ec3 import EC3_materials

# import local modules
from postprocess.config import default_config
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import xc_init
import data_geom as datG
import data_materials as datM 
# Common variables
prep=xc_init.prep

#                         *** MATERIALS *** 
concrProp=tm.MaterialData(name='concrProp',E=datM.concrete.Ecm(),nu=datM.concrete.nuc,rho=datM.concrete.density())
strSteelProp=tm.MaterialData(name='strSteelProp',E=datM.strSeel.E,nu=datM.strSeel.nu,rho=datM.strSeel.rho)
# Isotropic elastic section-material appropiate for plate and shell analysis
## Section type 1
dat=datG.sbeam_st1
bfST1_mat=tm.DeckMaterialData(name='bfST1_mat',thickness= dat['bf_t'],material=strSteelProp)
tfST1_mat=tm.DeckMaterialData(name='tfST1_mat',thickness= dat['tf_t'],material=strSteelProp)
wST1_mat=tm.DeckMaterialData(name='wST1_mat',thickness= dat['w_t'],material=strSteelProp)
## Section type 2
dat=datG.sbeam_st2
bfST2_mat=tm.DeckMaterialData(name='bfST2_mat',thickness= dat['bf_t'],material=strSteelProp)
tfST2_mat=tm.DeckMaterialData(name='tfST2_mat',thickness= dat['tf_t'],material=strSteelProp)
wST2_mat=tm.DeckMaterialData(name='wST2_mat',thickness= dat['w_t'],material=strSteelProp)
## Section type 3
dat=datG.sbeam_st3
bfST3_mat=tm.DeckMaterialData(name='bfST3_mat',thickness= dat['bf_t'],material=strSteelProp)
tfST3_mat=tm.DeckMaterialData(name='tfST3_mat',thickness= dat['tf_t'],material=strSteelProp)
wST3_mat=tm.DeckMaterialData(name='wST3_mat',thickness= dat['w_t'],material=strSteelProp)
#slab
slab_mat=tm.DeckMaterialData(name='slab_mat',thickness= datG.slabTh,material=concrProp)

for mat in [bfST1_mat,tfST1_mat,wST1_mat,
            bfST2_mat,tfST2_mat,wST2_mat,
            bfST3_mat,tfST3_mat,wST3_mat,
            slab_mat
            ]:
    mat.setupElasticSection(preprocessor=prep)
