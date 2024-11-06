# -*- coding: utf-8 -*-
import os
from postprocess.config import default_config
from postprocess import RC_material_distribution
from postprocess import element_section_map

# Reinforced concrete material distribution over the elements of the FE model.
# Concrete of type concrete01 with no tension branch

# import local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import data as dat
import xc_model as model #FE model generation

#RC-sections definition file.
import RC_sections_def as RCsect

#list of RC sections (from those whose attributes (materials, geometry, refinforcement, set of elements to which apply, ... are defined in the file 'RC_sections_def.py') that we want to process in order to run different limit-state checkings.
lstOfSectRecords=[RCsect.deckRCSects,RCsect.footRCSects,RCsect.wallRCSects,RCsect.beamXRCsect,RCsect.beamYRCsect,RCsect.columnZRCsect]

reinfConcreteSectionDistribution= RC_material_distribution.RCMaterialDistribution()
sections= reinfConcreteSectionDistribution.sectionDefinition #sections container


#Generation of 2 fiber sections (1 and 2 direction) for each record in list
#lstOfSectRecords. Inclusion of these section-groups in the sections container
for secRec in lstOfSectRecords:
    sections.append(secRec)

#Generation of the distribution of material extended to the elements of the
#FE model, assigning to each element the section-group that corresponds to it
for secRec in lstOfSectRecords:
    secRec.elemSetName= secRec.elemSet.name
    reinfConcreteSectionDistribution.assign(elemSet= secRec.elemSet.getElements,setRCSects= secRec)
    secRec.elemSet= None # Pickle can't write sets yet.
reinfConcreteSectionDistribution.dump()


