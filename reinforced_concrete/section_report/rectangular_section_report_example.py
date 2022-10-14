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

width= 1.0 # Cross-section width.
depth= 0.4 # Cross-section depth.
nCover= 0.025+12e-3 # Nominal cover.


# Longitudinal reinforcement
mainBars= EHE_materials.rebarsEHE['fi20']
rebarDiam= mainBars['d'] # Bar diameter.
rebarArea= mainBars['area']
numOfRebars= 6
lowerRow= def_simple_RC_section.ReinfRow(areaRebar= rebarArea, width= width, nRebars= numOfRebars, nominalCover= nCover-rebarDiam/2.0, nominalLatCover= nCover-rebarDiam/2.0)
upperRow= def_simple_RC_section.ReinfRow(areaRebar= rebarArea, width= width, nRebars= numOfRebars, nominalCover= nCover-rebarDiam/2.0, nominalLatCover= nCover-rebarDiam/2.0)

# Shear reinforcement
stirrups= EHE_materials.rebarsEHE['fi12']
shearReinfArea= stirrups['area']
nBranches= 4
shearReinf= def_simple_RC_section.ShearReinforcement(familyName= "sh",nShReinfBranches= nBranches, areaShReinfBranch= shearReinfArea, shReinfSpacing= 0.25, angAlphaShReinf= math.pi/2.0,angThetaConcrStruts= math.pi/4.0)

# Section 1
section1= def_simple_RC_section.RCRectangularSection(name='RectgSection 1',width= width, depth= depth, concrType=concr, reinfSteelType= steel)
section1.positvRebarRows= def_simple_RC_section.LongReinfLayers([lowerRow])
section1.negatvRebarRows= def_simple_RC_section.LongReinfLayers([upperRow])
section1.shReinfY= shearReinf

feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor

# Define fiber section.
section1.defRCSection(preprocessor,matDiagType= 'd')
# Compute interaction diagram.
diagIntsecHA= section1.defInteractionDiagram(preprocessor)

# Internal forces.
Nd= -10e3
Md= 280e3
Vd= 109.24e3

# Bending. Compute capacity factor.
fc= diagIntsecHA.getCapacityFactor(geom.Pos3d(Nd, Md,0))
ratio1= abs(fc-0.992996105120297)/0.992996105120297

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
    print('  total reinforcement area As= ', section1.getMainReinforcementArea()*1e4, 'mm2')
    print("  bending capacity factor: fc= ",fc)
    
from misc_utils import log_messages as lmsg
fname= os.path.basename(__file__)
if comparisonOK and (ratio1<1e-6):
   print('test '+fname+': ok.')
else:
    lmsg.error(fname+' ERROR.')
