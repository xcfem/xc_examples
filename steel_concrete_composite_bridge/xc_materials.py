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
#strSteelProp=tm.MaterialData(name='strSteelProp',E=datM.strSteel.E,nu=datM.strSteel.nu,rho=datM.strSteel.rho)
#SCsteelProp=tm.MaterialData(name='SCsteelProp',E=datM.SCsteel.E,nu=datM.SCsteel.nu,rho=datM.SCsteel.rho)
# Materials for linear analysis vonmises verification
strSteel=tm.defElasticIsotropic3d(preprocessor=prep,name='strSteel',E=datM.strSteel.E,nu=datM.strSteel.nu,rho=datM.strSteel.rho)
#SCsteel=tm.defElasticIsotropic3d(preprocessor=prep,name='SCsteel',E=datM.SCsteel.E,nu=datM.SCsteel.nu,rho=datM.SCsteel.rho)
SCsteelProp=tm.MaterialData(name='SCsteelProp',E=datM.SCsteel.E,nu=datM.SCsteel.nu,rho=datM.SCsteel.rho)
## Section type 1
dat=datG.sbeam_st1
bfST1_mat=tm.defMembranePlateFiberSection(prep,name='bfST1_mat',h= dat['bf_t'],nDMaterial=strSteel)
tfST1_mat=tm.defMembranePlateFiberSection(prep,name='tfST1_mat',h= dat['tf_t'],nDMaterial=strSteel)
wST1_mat=tm.defMembranePlateFiberSection(prep,name='wST1_mat',h= dat['w_t'],nDMaterial=strSteel)
## Section type 2
dat=datG.sbeam_st2
bfST2_mat=tm.defMembranePlateFiberSection(prep,name='bfST2_mat',h= dat['bf_t'],nDMaterial=strSteel)
tfST2_mat=tm.defMembranePlateFiberSection(prep,name='tfST2_mat',h= dat['tf_t'],nDMaterial=strSteel)
wST2_mat=tm.defMembranePlateFiberSection(prep,name='wST2_mat',h= dat['w_t'],nDMaterial=strSteel)
## Section type 3
dat=datG.sbeam_st3
bfST3_mat=tm.defMembranePlateFiberSection(prep,name='bfST3_mat',h= dat['bf_t'],nDMaterial=strSteel)
tfST3_mat=tm.defMembranePlateFiberSection(prep,name='tfST3_mat',h= dat['tf_t'],nDMaterial=strSteel)
wST3_mat=tm.defMembranePlateFiberSection(prep,name='wST3_mat',h= dat['w_t'],nDMaterial=strSteel)
# Transverse stiffeners
Tstiff_mat=tm.defMembranePlateFiberSection(prep,name='Tstiff_mat',h=datG.TSth,nDMaterial=strSteel)
#slab
slab_mat=tm.DeckMaterialData(name='slab_mat',thickness= datG.slabTh,material=concrProp)
# shear connections
from materials.sections import section_properties as sectpr
shearC_gsect=sectpr.CircularSection(name='shearC_gsect',Rext=datM.fi_SC/2.)
shearC_mat=tm.BeamMaterialData(name='shearC_mat',section=shearC_gsect,material=SCsteelProp)

for mat in [slab_mat,
            ]:
    mat.setupElasticSection(preprocessor=prep)
for mat in [shearC_mat]:
    mat.defElasticShearSection3d(preprocessor=prep)
# Stiffness diaphragms materials
BF_ID_mat=tm.defElasticMaterial(prep, "BF_ID_mat",datM.K_BF_ID) # bottom flange
TF_ID_mat=tm.defElasticMaterial(prep, "TF_ID_mat",datM.K_TF_ID) # diaphragm top flange

