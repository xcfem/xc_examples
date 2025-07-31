# -*- coding: utf-8 -*-
import math
from postprocess.config import default_config
from materials.sections.fiber_section import def_simple_RC_section as rcs
from postprocess import element_section_map
from postprocess.config import default_config
from postprocess import RC_material_distribution
from misc_utils import log_messages as lmsg

# import local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import data_geom as datG
import data_materials as datM
import xc_init
import xc_geom as xcG #FE model generation
import xc_materials as xcM # Materials
import xc_fem as xcF # FE model

# NOTE: be carefull with the shell sets so that they do not contain the embebbed beams.

# Common variables
prep=xc_init.prep
out=xc_init.out
#

plotSection=False # True if sections are depicted (in that case comment the dump line at the
                 # end of the script)
                 # False if sections are not depicted (in that case uncomment the dump line at the
                 # end of the script)
reinfConcreteSectionDistribution= RC_material_distribution.RCMaterialDistribution()
sectContainer= reinfConcreteSectionDistribution.sectionDefinition #sectContainer container


cover=35 # nominal cover [mm]

# **Concrete sections
#instances of element_section_map.LegacyRCSlabBeamSection that define the
#variables that make up THE TWO reinforced concrete sections in the two
#reinforcement directions of a slab or the front and back ending sections
#of a beam element

def append2container(RCsects,sets2apply,plot=False):
    sectContainer.append(RCsects)
    for s in sets2apply:
        reinfConcreteSectionDistribution.assign(elemSet=s.getElements,setRCSects=RCsects)
    if plot:
        RCsects.plot(prep,matDiagType='k')

## Deck
cover=datM.deckCover
fiLong=16e-3
sLong=0.10
fiTransv=12e-3
sTransv=0.15
sets2apply=[xcG.decklv1,xcG.decklv2]
fiStirr=10e-3
sStirr1=0.1
nStirr1=4
sStirr2=0.5
nStirr2=10
coverStirrTop=cover
coverLongTop=coverStirrTop+fiStirr
coverTransvTop=coverLongTop+fiLong
coverStirrBot=0.01
coverLongBot=coverStirrBot+fiStirr
coverTransvBot=coverLongBot+fiLong
deckRCsects= element_section_map.RCSlabBeamSection(name='deckRCsects',sectionDescr='slab of shell elements',concrType=datM.concrete, reinfSteelType=datM.reinfSteel,depth=datG.deckTh)
deckRCsects.dir1PositvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_m(fiTransv,sTransv,coverTransvTop),rcs.rebLayer_m(fiStirr,sStirr1,coverStirrTop)])
deckRCsects.dir1NegatvRebarRows=rcs.LongReinfLayers([rcs.rebLayer_m(fiTransv,sTransv,coverTransvBot),rcs.rebLayer_m(fiStirr,sStirr1,coverStirrBot)])
deckRCsects.dir2PositvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_m(fiLong,sLong,coverLongTop)])
deckRCsects.dir2NegatvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_m(fiLong,sLong,coverLongBot)])
deckRCsects.dir1ShReinfY=rcs.ShearReinforcement(familyName= "sh1Y",nShReinfBranches= nStirr1, areaShReinfBranch= math.pi*(fiStirr)**2/4., shReinfSpacing= sStirr1, angAlphaShReinf= math.pi/2.0,angThetaConcrStruts= math.pi/4.0)
deckRCsects.dir2ShReinfY=rcs.ShearReinforcement(familyName= "sh2Y",nShReinfBranches= nStirr2, areaShReinfBranch= math.pi*(fiStirr)**2/4., shReinfSpacing= sStirr2, angAlphaShReinf= math.pi/2.0,angThetaConcrStruts= math.pi/4.0)
append2container(deckRCsects,sets2apply,plot=plotSection)

## Footing
sets2apply=[xcG.foot]
footRCsects= element_section_map.RCSlabBeamSection(name='footRCsects',sectionDescr='footing',concrType=datM.concrete, reinfSteelType=datM.reinfSteel,depth=datG.footTh)
#D1: transversal rebars
#D2: longitudinal rebars
footRCsects.dir1PositvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_m(12e-3,0.150,35e-3)])
footRCsects.dir1NegatvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_m(12e-3,0.150,35e-3)])
footRCsects.dir2PositvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_m(16e-3,0.150,35e-3)])
footRCsects.dir2NegatvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_m(16e-3,0.150,35e-3)])
append2container(footRCsects,sets2apply,plot=plotSection)
    
## Wall
sets2apply=[xcG.wall]
wallRCsects= element_section_map.RCSlabBeamSection(name='wallRCsects',sectionDescr='wall of shell elements',concrType=datM.concrete, reinfSteelType=datM.reinfSteel,depth=datG.wallTh)
wallRCsects.dir1PositvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(20,200,cover)])
wallRCsects.dir1NegatvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(25,150,cover)])
wallRCsects.dir2PositvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(16,150,cover)])
wallRCsects.dir2NegatvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(12,150,cover)])
append2container(wallRCsects,sets2apply,plot=plotSection)

# beam X
sets2apply=[xcG.beamXconcr]
cover=40e-3
fiTop=25e-3
nTop=13
fiBot=25e-3
nBot=13
fiLat=20e-3
nLat=8
latTopCover=cover+fiTop
sLat=0.05
fiStirr=16e-3
sStirr=0.15
beamXRCsect=element_section_map.RCSlabBeamSection(name='beamXRCsect',sectionDescr='beam elements in X direction',concrType=datM.concrete, reinfSteelType=datM.reinfSteel,width=datG.wbeamX,depth=datG.hbeamX)
topBotRebLy=[rcs.rebLayerByNumFi_m(nTop, fiTop, cover+fiStirr, latC=cover, L=datG.wbeamX)]
#             rcs.rebLayerByNumFi_m(nTop, fiTop, cover+2*fiTop, latC=cover, L=datP.wLT)]
latRebLy=list()
for i in range(nLat):
    latRebLy.append(rcs.rebLayerByNumFi_m(2, fiLat, latTopCover+i*sLat, latC=cover, L=datG.hbeamX))

beamXRCsect.dir1PositvRebarRows=rcs.LongReinfLayers(topBotRebLy+latRebLy)
beamXRCsect.dir1NegatvRebarRows=rcs.LongReinfLayers(topBotRebLy)
beamXRCsect.dir2PositvRebarRows=rcs.LongReinfLayers(topBotRebLy+latRebLy)
beamXRCsect.dir2NegatvRebarRows=rcs.LongReinfLayers(topBotRebLy)
beamXRCsect.dir1ShReinfY=rcs.ShearReinforcement(familyName= "sh1",nShReinfBranches= 2, areaShReinfBranch= math.pi*(fiStirr)**2/4., shReinfSpacing= sStirr, angAlphaShReinf= math.pi/2.0,angThetaConcrStruts= math.pi/4.0)
beamXRCsect.dir2ShReinfY=rcs.ShearReinforcement(familyName= "sh2",nShReinfBranches= 2, areaShReinfBranch= math.pi*(fiStirr)**2/4., shReinfSpacing= sStirr, angAlphaShReinf= math.pi/2.0,angThetaConcrStruts= math.pi/4.0)
append2container(beamXRCsect,sets2apply,plot=plotSection)

# beam Y
sets2apply=[xcG.beamY]
beamYRCsect=element_section_map.RCSlabBeamSection(name='beamYRCsect',sectionDescr='beam elements in Y direction',concrType=datM.concrete, reinfSteelType=datM.reinfSteel,width=datG.wbeamY,depth=datG.hbeamY)
beamYRCsect.dir1PositvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(20,150,cover)])
beamYRCsect.dir1NegatvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(22,150,cover)])
beamYRCsect.dir2PositvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(20,150,cover)])
beamYRCsect.dir2NegatvRebarRows= rcs.LongReinfLayers([rcs.rebLayer_mm(22,150,cover)])
append2container(beamYRCsect,sets2apply,plot=plotSection)

# columns Z. Circular sections
sets2apply=[xcG.columnZconcr]
from materials.sections.fiber_section import def_column_RC_section as rccs
columnZconcrSect=rccs.RCCircularSection(name='columnZconcrSect',sectionDescr='cylindric columns Z',Rext= datG.fiColumnZ/2.0, concrType=datM.concrete, reinfSteelType= datM.reinfSteel)
fiStirr=10
columnZconcrSect.mainReinf=rcs.LongReinfLayers([rcs.ReinfRow(rebarsDiam= 20*1e-3, nRebars= 14, width= math.pi*(datG.fiColumnZ-2*(cover-3+fiStirr*1e-3)), nominalCover= cover)]) # in circular sections 'width' is the perimeter of the circumference that surrounds reinforcing bars
columnZconcrSect.shReinf=rcs.ShearReinforcement(familyName= "sh",nShReinfBranches= 2, areaShReinfBranch= math.pi*(fiStirr*1e-3)**2/4., shReinfSpacing= 0.15, angAlphaShReinf= math.pi/2.0,angThetaConcrStruts= math.pi/4.0)
columnZconcrRCsects= element_section_map.RCMemberSection(name='columnZconcrRCsects',templateSections=[columnZconcrSect,columnZconcrSect])
append2container(columnZconcrRCsects,sets2apply,plotSection)

#
if plotSection:
    lmsg.warning('The RC sections have not been dumped. If you want to dump them, set plotSection=False and run the script again')
else:
    reinfConcreteSectionDistribution.dump()

lstRCsects=[deckRCsects,footRCsects,wallRCsects,beamXRCsect,beamYRCsect,columnZconcrRCsects]
