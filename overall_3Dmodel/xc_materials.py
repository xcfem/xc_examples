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
# structural steel for shell elements (von mises linear analysis)
strSteelPlate=tm.defElasticIsotropic3d(preprocessor=prep,name='strSteelPlate',E=datM.strSteel.E,nu=datM.strSteel.nu,rho=datM.strSteel.rho)
# for Von mises Structural steel Non-linear analysis. Steel must be previously set J2PlateFibre and
# shell elements as MembranePlateFiberSection.
AISI304L= tm.defJ2PlateFibre(preprocessor=preprocessor, name='AISI304L', E=AISI_E, nu=0.3, fy=AISI_fy,alpha=AISI_alpha,rho=7850) 

# Isotropic elastic section-material appropiate for plate and shell analysis
deck_mat=tm.DeckMaterialData(name='deck_mat',thickness= datG.deckTh,material=concrProp)
deck_mat.setupElasticSection(preprocessor=prep)   #creates the section-material
wall_mat=tm.DeckMaterialData(name='wall_mat',thickness= datG.wallTh,material=concrProp)
wall_mat.setupElasticSection(preprocessor=prep)   #creates the section-material
foot_mat=tm.DeckMaterialData(name='foot_mat',thickness= datG.footTh,material=concrProp)
foot_mat.setupElasticSection(preprocessor=prep)   #creates the section-material

# Materials for analysis vonmises verification
steelPlate_mat=tm.defMembranePlateFiberSection(prep,name='steelPlate_mat',h= datG.steelPlateThck,nDMaterial=strSteelPlate)
'''for non-linear analysis. Steel must be previously set J2PlateFibre and
shell elements as MembranePlateFiberSection.
Ensure that in model_gen.py materials for non-linear analysis are 
uncommented
'''
steelPlate_mat=tm.defMembranePlateFiberSection(prep,name='steelPlate_mat',h= datG.steelPlateThck,nDMaterial=datM.AISI304L)

#Geometric sections
#rectangular sections
from materials.sections import section_properties as sectpr
geomSectBeamX=sectpr.RectangularSection(name='geomSectBeamX',b=datG.wbeamX,h=datG.hbeamX)
geomSectBeamY=sectpr.RectangularSection(name='geomSectBeamY',b=datG.wbeamY,h=datG.hbeamY)

# Elastic material-section appropiate for 3D beam analysis, including shear
  # deformations.
  # Attributes:
  #   name:         name identifying the section
  #   section:      instance of a class that defines the geometric and
  #                 mechanical characteristiscs
  #                 of a section (e.g: RectangularSection, CircularSection,
  #                 ISection, ...)
  #   material:     instance of a class that defines the elastic modulus,
  #                 shear modulus and mass density of the material

beamXconcr_mat= tm.BeamMaterialData(name= 'beamXconcr_mat', section=geomSectBeamX, material=concrProp)
beamXconcr_mat.defElasticShearSection3d(preprocessor=prep)
beamY_mat= tm.BeamMaterialData(name= 'beamY_mat', section=geomSectBeamY, material=concrProp)
beamY_mat.defElasticShearSection3d(preprocessor=prep)
# cylindrical column
columnZconcr_gsect=sectpr.CircularSection(name='columnZconcr_gsect',Rext=datG.fiColumnZ/2.)
columnZconcr_mat=tm.BeamMaterialData(name='columnZconcr_mat', section=columnZconcr_gsect, material=concrProp)
columnZconcr_mat.defElasticShearSection3d(preprocessor=prep)

# Steel material-section appropiate for 3D beam analysis, including shear
  # deformations.
  # Attributes:
  #   steel:         steel material (
  #   name: name of the standard steel profile. Types: IPEShape, HEShape,
  #         UPNShape, AUShape, CHSShape
  #      (defined in materials.sections.structural_shapes.arcelor_metric_shapes)
columnZsteel_mat= EC3_materials.HEShape(steel=datM.strSteel,name='HE_200_A')
columnZsteel_mat.defElasticShearSection3d(prep)
columnZsteel_mat.sectionClass=1
beamXsteel_mat= EC3_materials.IPEShape(steel=datM.strSteel,name='IPE_A_300')
beamXsteel_mat.defElasticShearSection3d(prep)
beamXsteel_mat.sectionClass=1

# X spring material
Xspring_mat= tm.defElasticMaterial(prep, "kx",datM.KXspring)
