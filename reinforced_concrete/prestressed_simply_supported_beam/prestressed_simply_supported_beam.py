# -*- coding: utf-8 -*-
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AO_O)"
__copyright__= "Copyright 2022, LCPT and AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es ana.ortega@ciccp.es"

import math
import geom
from geom_utils import parabola as pb
from materials.ec2 import EC2_materials
from materials.ehe import EHE_materials
from materials.ec2 import EC2_limit_state_checking
from materials.sections import section_properties
from rough_calculations import ng_simple_beam as sb
import numpy as np

# Section geometry.
webWidth= 0.31
chamferSide= 0.05
webHeight= 0.65
flangeWidth= 1.0
flangeThickness= 0.15
crossSectionGeometry= section_properties.TSection(name= '', webWidth= webWidth, webHeight= webHeight, flangeWidth= flangeWidth, flangeThickness= flangeThickness, chamferSide= chamferSide)
crossSectionPlg= crossSectionGeometry.plg
centroidPos= crossSectionPlg.getCenterOfMass()
crossSectionHeight= webHeight+chamferSide+flangeThickness
crossSectionArea= crossSectionPlg.getArea()
crossSectionInertia= crossSectionPlg.getIx()

# Materials.
concrete= EC2_materials.C40
# Strands for prestressed concrete.
strand= EHE_materials.Y1860S7Strand_15_7
## Main reinforcement.
reinfSteel= EHE_materials.B500S
mainReinfDiameter= 25e-3
mainReinfRebarArea= EHE_materials.Fi25
## Shear reinforcement.
webStirrupsSteel= EHE_materials.B400S
webStirrupsSpacing= 0.15
webStirrupsAngle= math.pi/2.0 # Vertical web stirrups.
webStirrups= EC2_materials.rebarsEC2['fi12'] # rebar diameter
webStirrupsArea= webStirrups['area'] # rebar area
webStirrupsNumberOfLegs= 2
Asw= webStirrupsNumberOfLegs*webStirrupsArea # cross-sectional area of the shear reinforcement

## Flange transverse reinforcement.
flangeStirrupsSpacing= webStirrupsSpacing
flangeStirrupsSteel= webStirrupsSteel
flangeStirrups= EC2_materials.rebarsEC2['fi10'] # rebar diameter
flangeStirrupsArea= flangeStirrups['area'] # rebar area
flangeStirrupsNumberOfLegs= 2
Asf= flangeStirrupsNumberOfLegs*flangeStirrupsArea # cross-sectional area of the shear reinforcement

# Beam.
beam= sb.SimpleBeam(E= concrete.Ecm(), I= crossSectionInertia, l= 20)
abutmentWidth= 0.75
beamSupportedLength= 0.6
beamOffset= beamSupportedLength-abutmentWidth/2.0
## Effective width of flanges (clause 5.3.2.1 of EC2:2004).
flangeEffectiveWidth= min(webWidth+0.2*(flangeWidth-webWidth)+0.1*beam.l, flangeWidth)

# Cable geometry
prestressingCover= 0.1
#eccentricity= centroidPos.y-prestressingCover
eccentricity= -crossSectionGeometry.yMin()-prestressingCover
p0= geom.Pos2d(0.0, centroidPos.y)
p1= geom.Pos2d(beam.l/2.0, -eccentricity)
p2= geom.Pos2d(beam.l, centroidPos.y)
cableAxis= pb.Parabola(p0, p1, p2)

               
# Actions
## Permanent actions.
concreteDensity= 2500.0
gravity= 9.81 # m/s2
crossSectionSelfWeigth= crossSectionArea*gravity*concreteDensity
selfWeight= crossSectionSelfWeigth
pavementWeight= 1.5e3*flangeWidth # N/m
plainConcreteWeight= 2400*gravity*.08*flangeWidth # N/m (slope molding).
deckWaterproofingWeight= 1e3*flangeWidth # N/m (deck waterproofing).
antiVandalismProtectionWeight= 1e3*flangeWidth # N/m (anti-vandalism protection on edge beam).
deadLoad= pavementWeight+plainConcreteWeight+deckWaterproofingWeight+antiVandalismProtectionWeight
permanentLoad= selfWeight+deadLoad

## Live loads.
uniformLiveLoad= 4.31e3*flangeWidth # N/m (uniform live load).

# Prestressing
loadToCompensate= 0.80*permanentLoad
midSpanPrestressingForce= loadToCompensate*beam.l**2/8.0/eccentricity
losses= .2
initialPrestressingForce= midSpanPrestressingForce/(1-losses)
prestressingStress= 0.75*strand.fmax
reqActiveReinforcementArea= initialPrestressingForce/prestressingStress
reqActiveReinforcementCapacity= reqActiveReinforcementArea*strand.fmax
## Active reinforcement.
numberOfStrands= math.ceil(reqActiveReinforcementArea/strand.area)
ductDiameter= 81e-3 # duct diameter.
ductArea= math.pi*(ductDiameter/2.0)**2

spiralReinforcementExtDiameter= 220e-3
spiralReinforcementCover= (webWidth-spiralReinforcementExtDiameter)/2.0 # Catálogo VSL
prestressingCompression= -midSpanPrestressingForce/crossSectionPlg.getArea()

# Design for initial condition
prestressingMidSpanBendingMoment= midSpanPrestressingForce*eccentricity
initialCondBendingMoment= prestressingMidSpanBendingMoment-selfWeight*beam.l**2/8.0
initialCondMaxStress= prestressingCompression+initialCondBendingMoment/crossSectionPlg.getIx()*(crossSectionHeight-centroidPos.y)
initialCondMinStress= prestressingCompression-initialCondBendingMoment/crossSectionPlg.getIx()*centroidPos.y
allowableCompression= 0.45*concrete.fck

# Design under frequent load
## Stresses
frequentLoad= permanentLoad+0.4*uniformLiveLoad
frequentLoadBendingMoment= prestressingMidSpanBendingMoment-(frequentLoad)*beam.l**2/8.0
frequentLoadMinStress= prestressingCompression+frequentLoadBendingMoment/crossSectionPlg.getIx()*(crossSectionHeight-centroidPos.y)
frequentLoadMaxStress= prestressingCompression-frequentLoadBendingMoment/crossSectionPlg.getIx()*centroidPos.y

## Deflection
### Bending moment.
def MfrequentLoad(x):
    '''Bending moment law.'''
    eccentricity= centroidPos.y-cableAxis.y(x)
    retval= -midSpanPrestressingForce*eccentricity
    retval+= beam.getBendingMomentUnderUniformLoad(q= -frequentLoad, x= x)
    return retval

deflectionUnderFrequentLoad= beam.computeDeflection(x= beam.l/2.0, M= MfrequentLoad)

# Passive reinforcement design (ULS)
## Main reinforcement.
passiveReinfCover= 0.045+mainReinfDiameter/2.0
effectiveDepth= crossSectionHeight-passiveReinfCover
innerLeverArm= 0.9*effectiveDepth
ulsLoad= 1.5*(permanentLoad+uniformLiveLoad)
ulsBendingMoment= ulsLoad*beam.l**2/8.0
Fp= numberOfStrands*strand.Fp()
prestressingBendingMoment= Fp*0.9*(crossSectionHeight-prestressingCover)
reqAs= (ulsBendingMoment-prestressingBendingMoment)/(0.9*reinfSteel.fyd()*(crossSectionHeight-passiveReinfCover))
numberOfMainRebars= math.ceil(reqAs/mainReinfRebarArea)
passiveReinfArea= numberOfMainRebars*mainReinfRebarArea
def Muls(x):
    '''Bending moment law.'''
    eccentricity= centroidPos.y-cableAxis.y(x)
    retval= -midSpanPrestressingForce*eccentricity
    retval+= beam.getBendingMomentUnderUniformLoad(q= -ulsLoad, x= x)
    return retval

## Shear reinforcement.
ulsShear= ulsLoad*beam.l/2.0
prestressingAngle= cableAxis.alpha(0.0)
Nc= -midSpanPrestressingForce*math.cos(prestressingAngle)
concreteArea= crossSectionArea-ductArea-passiveReinfArea
crackedVRdc= EC2_limit_state_checking.getShearResistanceCrackedNoShearReinf(concrete= concrete, NEd= Nc, Ac= concreteArea, Asl= passiveReinfArea, bw= webWidth-1.2*ductDiameter, d= effectiveDepth, nationalAnnex= 'Spain')
minShearReinfArea= EC2_limit_state_checking.getMinShearReinforcementArea(concrete, webStirrupsSteel, s= webStirrupsSpacing, bw= webWidth, nationalAnnex= 'Spain')
maxShearReinfArea= EC2_limit_state_checking.getMaximumEffectiveShearReinforcement(concrete, NEd= Nc, Ac= concreteArea, bw= webWidth, s= webStirrupsSpacing, shearReinfSteel= webStirrupsSteel, shearReinfAngle= webStirrupsAngle, nationalAnnex= 'Spain')
#optimumStrutAngle= EC2_limit_state_checking.getStrutAngleForSimultaneousCollapse(concrete, bw= webWidth-1.2*ductDiameter, s= webStirrupsSpacing, Asw= Asw, shearReinfSteel= webStirrupsSteel, shearReinfAngle= webStirrupsAngle)
strutAngle= math.radians(26.57)
VRdMax= EC2_limit_state_checking.getMaximumShearWebStrutCrushing(concrete= concrete, NEd= Nc, Ac= concreteArea, bw= webWidth-1.2*ductDiameter, z= innerLeverArm, shearReinfAngle= webStirrupsAngle, webStrutAngle= strutAngle, nationalAnnex= 'Spain')
VRds= EC2_limit_state_checking.getShearResistanceShearReinf(concrete= concrete, NEd= Nc, Ac= concreteArea, bw= webWidth-1.2*ductDiameter, Asw= Asw, s= webStirrupsSpacing, z= innerLeverArm, shearReinfSteel= webStirrupsSteel, shearReinfAngle= webStirrupsAngle, webStrutAngle= strutAngle, nationalAnnex= 'Spain')

# Reinforcement for shear between the flange and the web.

## Bending moment.
x0= 0.0
x1= 1.0
DeltaX= x1-x0 # length under consideration (see figure 6.7 on EC2:2004).
MEdx0= Muls(x= x0)
MEdx1= Muls(x= x1)

## Shear between the flange and the web.
flangeArea= flangeThickness*flangeWidth
flangeOverhangArea= flangeThickness*(flangeWidth-webWidth)/2.0
areaRatio= flangeOverhangArea/flangeArea
### Compression increment.
flangeCompIncr= (MEdx1-MEdx0)/innerLeverArm
flangeOverhangCompIncr= flangeCompIncr*areaRatio
### Longitudinal shear stress.
longitudinalShearStress= flangeOverhangCompIncr/flangeThickness/DeltaX
## Flange struts crushing
flangeStrutAngle= math.radians(45)
flange_vRdMax= EC2_limit_state_checking.getMaximumShearFlangeStrutCrushingStress(concrete, flangeStrutAngle, nationalAnnex= 'Spain')
flange_VRdMax= flange_vRdMax*DeltaX*flangeThickness
flange_VRdc= EC2_limit_state_checking.getConcreteFlangeShearStrength(concrete, hf= flangeThickness, DeltaX= DeltaX, nationalAnnex= 'Spain')
flange_vRds= EC2_limit_state_checking.getFlangeShearResistanceShearReinfStress(concrete, hf= flangeThickness, Asf= Asf, sf= flangeStirrupsSpacing, shearReinfSteel= flangeStirrupsSteel, flangeStrutAngle= flangeStrutAngle, compressionFlange= True, nationalAnnex= 'Spain')
flange_VRds= flange_vRds*DeltaX*flangeThickness

print('Geometry.')
print('  Section geometry.')
print('    centroid: ', centroidPos)
print('    depth: ', crossSectionHeight, 'm')
print('    area: ', crossSectionArea, ' m2')
print('    inertia: ', crossSectionInertia, ' m4')
print('    effective width of flange: ', flangeEffectiveWidth, ' m')
print('  Section geometry.')
print('    span: ', beam.l, ' m')
print('    slenderness: 1/', beam.l/crossSectionHeight)

print('Loads.')
print('  self weight: ',  selfWeight/1e3, 'kN/m')
print('  dead load: ',  deadLoad/1e3, 'kN/m')
print('  initial prestressing force P0= ',  initialPrestressingForce/1e3, 'kN')

print('Presstressing.')
print('  Design for initial condition:')
print('    initial condition bending moment: ', initialCondBendingMoment/1e3, 'kN.m')
print('    initial condition maximum stress: ', initialCondMaxStress/1e6, 'MPa')
print('    concrete tension strength: ', concrete.getFctm()/1e6, 'MPa')
print('    initial condition minimum stress: ', initialCondMinStress/1e6, 'MPa')
print('    allowable compression: ', allowableCompression/1e6, 'MPa')

print('  Design under frequent load.')
print('    frequent load bending moment: ', frequentLoadBendingMoment/1e3, 'kN.m')
print('    maximum stress under frequent load: ', frequentLoadMaxStress/1e6, 'MPa')
print('    concrete tension strength: ', concrete.getFctm()/1e6, 'MPa')
print('    frequent load minimum stress: ', frequentLoadMinStress/1e6, 'MPa')
print('    allowable compression: ', allowableCompression/1e6, 'MPa')
print('    deflection under frequent load: ', deflectionUnderFrequentLoad*1e3, ' mm')

print('Active reinforcement.')
print('  required active reinforcement area Ap= ',  reqActiveReinforcementArea*1e6, 'mm2')
print('  required active reinforcement capacity Pmax= ',  reqActiveReinforcementCapacity/1e3, 'kN')
print('  number of strands: ', numberOfStrands)
print('  strand diameter: ', strand.diameter*1e3, 'mm')
print('  strand area: ', strand.area*1e6, 'mm2')
print('  tendon area: ', numberOfStrands*strand.area*1e6, 'mm2')
print('  duct area: ', ductArea*1e4, 'cm2')
print('  spiral reinforcement cover: ',  spiralReinforcementCover*1e3, 'mm')

print('Passive reinforcement.')
print('  Main reinforcement (bending).')
print('    mid-span bending moment (ELU): ', ulsBendingMoment/1e3, 'kN.m')
print('    active reinforcement stress Fp= ', Fp/1e3, ' kN')
print('    active reinforcement bending moment Mp= ', prestressingBendingMoment/1e3, ' kN.m')
print('    passive reinforcement bending moment Mdd= ', (ulsBendingMoment-prestressingBendingMoment)/1e3, ' kN.m')
print('    passive reinforcement required area= ', reqAs*1e4, 'cm2')
print('    number of rebars: ', numberOfMainRebars, '25 mm rebars.')
print('  Web shear reinforcement.')
print('    maximum shear force (ELU): VEd= ', ulsShear/1e3, 'kN')
print('    angle of prestressing cable: ', math.degrees(prestressingAngle), 'º')
print('    axial load: ', Nc/1e3, 'kN')
print('    strut angle: theta= ', math.degrees(strutAngle), 'º')
print('    ultimate shear force due to diagonal compression in the web: VRdMax=', VRdMax/1e3, 'kN')
print('    shear strength for cracked sections subjected to bending moment. VRdc= ', crackedVRdc/1e3, 'kN')
print('    minimum shear reinforcement required area= ', minShearReinfArea*1e4, 'cm2')
print('    maximum shear reinforcement allowable area= ', maxShearReinfArea*1e4, 'cm2')
print('    stirrups steel: ', webStirrupsSteel.materialName)
print('    number of legs: ', webStirrupsNumberOfLegs)
print('    diameter of stirrups: ', int(webStirrups['d']*1e3),'mm')
print('    stirrups spacing: ', webStirrupsSpacing*1e3,'mm')
print('    shear reinforcement area: Asw= ', Asw*1e4, 'cm2')
print('    shear strength VRds= ', VRds/1e3, 'kN')
print('  Shear reinforcement between the flange and the web.')
print('    flange overhang compression increment: VEd= ', flangeOverhangCompIncr/1e3, 'kN')
print('    longitudinal shear stress: vEd= ', longitudinalShearStress/1e6, 'MPa')
print('    maximum shear stress due to diagonal compression in the flange: vRdMax=', flange_vRdMax/1e6, 'MPa')
print('    maximum shear due to diagonal compression in the flange: VRdMax=', flange_VRdMax/1e3, 'kN')
print('    maximum shear resisted by the concrete: VRdc=', flange_VRdc/1e3, 'kN')
print('    stirrups steel: ', flangeStirrupsSteel.materialName)
print('    number of legs: ', flangeStirrupsNumberOfLegs)
print('    diameter of stirrups: ', int(flangeStirrups['d']*1e3),'mm')
print('    stirrups spacing: ', flangeStirrupsSpacing*1e3,'mm')
print('    shear reinforcement area: Asw= ', Asw*1e4, 'cm2')
print('    maximum shear stress due to the strength of the transverse reinforcement: vRds=', flange_vRds/1e6, 'MPa')
print('    maximum shear due to the strength of the transverse reinforcement: VRds=', flange_VRds/1e3, 'kN')

      
import matplotlib.pyplot as plt

def plotCableAxis(h, span, beamOffset, cableAxis, step):
    ''' Draw the axis of the cable.

    :param h: cross-section depth.
    :param span: beam span.
    :param beamOffset: lenght of the beam outside its span.
    :param cableAxis: function that represent the geometry of the cable.
    :param step: distance between axis points.
    '''
    xi= list()
    yi= list()
    retval= list()
    length= span+beamOffset
    n= int(length//step)-2 # floor division
    remainder= (length-step*n)/2.0
    xi= [-beamOffset/2.0, remainder]
    xi.extend([step]*n)
    xi.append(remainder)
    xi= np.add.accumulate(xi)
    yi= list()
    for x in xi:
        y= cableAxis.y(x)
        yi.append(y)
        retval.append((x,y))
    plt.plot(xi, yi, '-')
    plt.grid()
    plt.show()
    return retval
    

# Draw cross section.
crossSectionGeometry.draw()

# Draw cable axis.
cablePoints= plotCableAxis(h= crossSectionHeight, span= beam.l, beamOffset= beamOffset, cableAxis= cableAxis, step= 1.0)
beamContourPoints= [(-beamOffset/2.0, 0.0), (beam.l+beamOffset/2.0, 0.0), (beam.l+beamOffset/2.0, crossSectionHeight), (-beamOffset/2.0, crossSectionHeight), (-beamOffset/2.0, 0.0)]

import ezdxf
import logging

# Avoid info messages
logging.getLogger(ezdxf.__name__).setLevel(logging.ERROR)
doc = ezdxf.new("R2000")
msp = doc.modelspace()

msp.add_lwpolyline(cablePoints, dxfattribs={"layer": 'cable_axis'})
msp.add_lwpolyline(beamContourPoints, dxfattribs={"layer": 'beam'})
textOffset= .05
for iD, p in enumerate(cablePoints):
    (x,y)= p
    xText= '{:+.3f}'.format(x)
    yText= '{:+.3f}'.format(y)
    idText= str(iD)
    attribs= dxfattribs={"layer": "TEXTLAYER", 'height': 0.1, 'rotation': 90}
    msp.add_text(
        xText, 
        dxfattribs= attribs).set_pos((x-textOffset, -2.0), align="CENTER")
    msp.add_text(
        yText, 
        dxfattribs= attribs).set_pos((x-textOffset, -1.0), align="CENTER")
    msp.add_text(
        idText, 
        dxfattribs= attribs).set_pos((x-textOffset, -3.0), align="CENTER")
    msp.add_line((x, -3), (x, -.1), dxfattribs={"color": 1})

doc.saveas("prestressed_beam.dxf")
