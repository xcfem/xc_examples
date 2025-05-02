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
strSteelProp=tm.MaterialData(name='strSteelProp',E=datM.strSteel.E,nu=datM.strSteel.nu,rho=datM.strSteel.rho)
SCsteelProp=tm.MaterialData(name='SCsteelProp',E=datM.SCsteel.E,nu=datM.SCsteel.nu,rho=datM.SCsteel.rho)
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
# Transverse stiffeners
Tstiff_mat=tm.DeckMaterialData(name='Tstiff_mat',thickness=datG.TSth,material=strSteelProp)
#slab
slab_mat=tm.DeckMaterialData(name='slab_mat',thickness= datG.slabTh,material=concrProp)
# shear connections
from materials.sections import section_properties as sectpr
shearC_gsect=sectpr.CircularSection(name='shearC_gsect',Rext=datM.fi_SC/2.)
shearC_mat=tm.BeamMaterialData(name='shearC_mat',section=shearC_gsect,material=SCsteelProp)

for mat in [bfST1_mat,tfST1_mat,wST1_mat,
            bfST2_mat,tfST2_mat,wST2_mat,
            bfST3_mat,tfST3_mat,wST3_mat,
            Tstiff_mat,
            slab_mat,
            ]:
    mat.setupElasticSection(preprocessor=prep)
for mat in [shearC_mat]:
    mat.defElasticShearSection3d(preprocessor=prep)
# Stiffness diaphragms materials
BF_ID_mat=tm.defElasticMaterial(prep, "BF_ID_mat",datM.K_BF_ID) # bottom flange
TF_ID_mat=tm.defElasticMaterial(prep, "TF_ID_mat",datM.K_TF_ID) # diaphragm top flange

