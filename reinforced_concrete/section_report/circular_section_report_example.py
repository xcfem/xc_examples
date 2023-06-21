# -*- coding: utf-8 -*-
''' Example showing how to obtain a LaTeX report and a DXF drawing
    from an RCthe section.
   Home made test.'''
from __future__ import division
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2015, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"


import sys
import os
import filecmp
import geom
import xc
import math
import ezdxf
from materials.ehe import EHE_materials
from materials.sections.fiber_section import def_simple_RC_section
from materials.sections.fiber_section import def_column_RC_section

# Check if silent execution has been requested.
argv= sys.argv
silent= False
if(len(argv)>1):
    if 'silent' in argv[1:]:
        silent= True

# Materials definition
concr= EHE_materials.HA30
concr.alfacc=1.0
steel= EHE_materials.B500S

radius= 0.5 # Cross-section radius expressed in meters.
nCover= 0.025+12e-3

# Section 1
rebarDiam= 32e-3 # Bar diameter expressed in meters.
cover= nCover+rebarDiam/2.0 # Concrete cover expressed in meters.
rebarArea= math.pi*(rebarDiam/2.0)**2 # Rebar area expressed in square meters.
section1= def_column_RC_section.RCCircularSection(name='CircSection 1',Rext= radius, concrType=concr, reinfSteelType= steel)

# Longitudinal reinforcement
section1.mainReinf= def_simple_RC_section.LongReinfLayers([def_simple_RC_section.ReinfRow(rebarsDiam= rebarDiam, nRebars=24, width= 2*math.pi*(radius-cover), nominalCover= nCover)])

# Shear reinforcement
stirrups= EHE_materials.rebarsEHE['fi12']
shearReinfArea= stirrups['area']
nBranches= 4
section1.shReinf= def_simple_RC_section.ShearReinforcement(familyName= "sh",nShReinfBranches= nBranches, areaShReinfBranch= shearReinfArea, shReinfSpacing= 0.25, angAlphaShReinf= math.pi/2.0,angThetaConcrStruts= math.pi/4.0)

feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor

# Define fiber section.
section1.defRCSection(preprocessor,matDiagType= 'd')
# Compute interaction diagram.
diagIntsecHA= section1.defInteractionDiagram(preprocessor)

# Internal forces.
Nd= -10e3
Md= 2800e3
Vd= 1090.24e3

# Bending. Compute capacity factor.
fc= diagIntsecHA.getCapacityFactor(geom.Pos3d(Nd, Md,0))
ratio1= abs(fc-0.9556451619964796)/0.9556451619964796

# Report
## Get current path.
pth= os.path.dirname(__file__)
if(not pth):
    pth= '.'
## Get valid filename from section name.
baseOutputFileName= ''.join(x for x in section1.name if x.isalnum())
latexOutputFileName= baseOutputFileName+'.tex'
latexOutputPath= pth+'/'+latexOutputFileName
latexOutputFile= open(latexOutputPath, 'w')
## Write report.
section1.latexReport(latexOutputFile)
latexOutputFile.close()

# Compare with reference file.
refFile= pth+'/../../reference_files/ref_'+latexOutputFileName
comparisonOK= filecmp.cmp(refFile, latexOutputPath, shallow=False)



# DXF output
doc = ezdxf.new("R2000")
msp = doc.modelspace()
section1.writeDXF(msp)
dxfOutputFileName= './'+baseOutputFileName+'.dxf'
doc.saveas(dxfOutputFileName)

if not silent:
    print('Comparison OK: ', comparisonOK)
    # print(thisFile)
    print('Bending.')
    print('  reinf. layers As= ', section1.mainReinf.getAs())
    print("  bending capacity factor: fc= ",fc)
else: # your garbage you clean it.
    os.remove(dxfOutputFileName)
    os.remove(latexOutputPath)
    os.remove(dxfOutputFileName.replace(".dxf",".png"))
    os.remove(dxfOutputFileName.replace(".dxf",".eps"))
   
from misc_utils import log_messages as lmsg
fname= os.path.basename(__file__)
if comparisonOK and (ratio1<1e-6):
   print('test '+fname+': ok.')
else:
    lmsg.error(fname+' ERROR.')
