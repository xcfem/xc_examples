# -*- coding: utf-8 -*-

from postprocess.config import default_config
from materials.sections.fiber_section import def_simple_RC_section as rcs
from postprocess import element_section_map

# import local modules
import sys
workingDirectory= default_config.findWorkingDirectory()+'/' #search env_config.py
sys.path.append(workingDirectory)
import data as dat
import model_gen as model #FE model generation

# **Concrete sections
#instances of element_section_map.LegacyRCSlabBeamSection that define the
#variables that make up THE TWO reinforced concrete sections in the two
#reinforcement directions of a slab or the front and back ending sections
#of a beam element

deckRCSects= element_section_map.LegacyRCSlabBeamSection(name='deckRCSects',sectionDescr='slab of shell elements',concrType=dat.concrete, reinfSteelType=dat.reinfSteel,depth=dat.deckTh,elemSet=model.decks)  
deckRCSects.dir1PositvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(12,150,35)])
deckRCSects.dir1NegatvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(12,200,35)])
deckRCSects.dir2PositvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(16,250,35)])
deckRCSects.dir2NegatvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(16,100,35)])
import math
areaFi8=math.pi*0.008**2/4.
shear1=rcs.ShearReinforcement(familyName= "shear1",nShReinfBranches= 1.0,areaShReinfBranch= areaFi8,shReinfSpacing= 0.20,angAlphaShReinf= math.pi/2.0,angThetaConcrStruts= math.radians(30))
shear2=rcs.ShearReinforcement(familyName= "shear2",nShReinfBranches= 1.0,areaShReinfBranch= areaFi8,shReinfSpacing= 0.15,angAlphaShReinf= math.pi/2.0,angThetaConcrStruts= math.radians(30))
deckRCSects.dir1ShReinfY=shear1
deckRCSects.dir2ShReinfY=shear2


footRCSects= element_section_map.LegacyRCSlabBeamSection(name='footRCSects',sectionDescr='footation',concrType=dat.concrete, reinfSteelType=dat.reinfSteel,depth=dat.footTh,elemSet=model.foot)
#D1: transversal rebars
#D2: longitudinal rebars
footRCSects.dir1PositvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(12,150,35)])
footRCSects.dir1NegatvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(12,150,35)])
footRCSects.dir2PositvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(16,150,35)])
footRCSects.dir2NegatvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(16,150,35)])

wallRCSects= element_section_map.LegacyRCSlabBeamSection(name='wallRCSects',sectionDescr='wall of shell elements',concrType=dat.concrete, reinfSteelType=dat.reinfSteel,depth=dat.wallTh,elemSet=model.wall)  
wallRCSects.dir1PositvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(20,200,35)])
wallRCSects.dir1NegatvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(25,150,35)])
wallRCSects.dir2PositvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(16,150,35)])
wallRCSects.dir2NegatvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(12,150,35)])


beamXRCsect=element_section_map.LegacyRCSlabBeamSection(name='beamXRCsect',sectionDescr='beam elements in X direction',concrType=dat.concrete, reinfSteelType=dat.reinfSteel,width=dat.wbeamX,depth=dat.hbeamX,elemSet=model.beamX)
beamXRCsect.dir1PositvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(20,50,35)])
beamXRCsect.dir1NegatvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(22,50,35)])
beamXRCsect.dir2PositvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(20,50,35)])
beamXRCsect.dir2NegatvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(22,50,35)])


beamYRCsect=element_section_map.LegacyRCSlabBeamSection(name='beamYRCsect',sectionDescr='beam elements in Y direction',concrType=dat.concrete, reinfSteelType=dat.reinfSteel,width=dat.wbeamY,depth=dat.hbeamY,elemSet=model.beamY)
beamYRCsect.dir1PositvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(20,150,35)])
beamYRCsect.dir1NegatvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(22,150,35)])
beamYRCsect.dir2PositvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(20,150,35)])
beamYRCsect.dir2NegatvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(22,150,35)])


columnZRCsect=element_section_map.LegacyRCSlabBeamSection(name='columnZRCsect',sectionDescr='columnZ',concrType=dat.concrete, reinfSteelType=dat.reinfSteel,width=dat.wcolumnZ,depth=dat.hcolumnZ,elemSet=model.columnZ)
columnZRCsect.dir1PositvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(20,150,35)])
columnZRCsect.dir1NegatvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(22,150,35)])
columnZRCsect.dir2PositvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(20,150,35)])
columnZRCsect.dir2NegatvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(22,150,35)])


