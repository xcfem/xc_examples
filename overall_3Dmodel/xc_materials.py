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

# Isotropic elastic section-material appropiate for plate and shell analysis
deck_mat=tm.DeckMaterialData(name='deck_mat',thickness= datG.deckTh,material=concrProp)
deck_mat.setupElasticSection(preprocessor=prep)   #creates the section-material
wall_mat=tm.DeckMaterialData(name='wall_mat',thickness= datG.wallTh,material=concrProp)
wall_mat.setupElasticSection(preprocessor=prep)   #creates the section-material
foot_mat=tm.DeckMaterialData(name='foot_mat',thickness= datG.footTh,material=concrProp)
foot_mat.setupElasticSection(preprocessor=prep)   #creates the section-material

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
columnZsteel_mat= EC3_materials.HEShape(steel=datM.S235JR,name='HE_200_A')
columnZsteel_mat.defElasticShearSection3d(prep)
columnZsteel_mat.sectionClass=1
beamXsteel_mat= EC3_materials.IPEShape(steel=datM.S235JR,name='IPE_A_300')
beamXsteel_mat.defElasticShearSection3d(prep)
beamXsteel_mat.sectionClass=1

# X spring material
Xspring_mat= typical_materials.defElasticMaterial(preprocessor, "kx",datM.KSpring)
