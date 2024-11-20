# -*- coding: utf-8 -*-
from materials.sections.fiber_section import section_report 
from postprocess.reports import graph_material 
import matplotlib.pyplot as plt
from postprocess.config import default_config
# import local modules
workingDirectory= default_config.setWorkingDirectory()
import env_config as env
import xc_init
#import xc_sets as xcS
from calculations import RC_sections_def as RCsect
# Common variables
out=xc_init.out ; modelSpace=xc_init.modelSpace ; prep=xc_init.prep
#

sect2Disp=RCsect.lstRCsects
sectGrWth='50mm' #width of the RC section graphic that we insert in the table of mechanical characteristics   
writeSection2=False # False if we don't want to write the text table for section 2 (in beam elements, usually section1=section2)

report_graphics_outDir= env.cfg.projectDirTree.getReportSectionsGrPath()
report_graphics_rltv_outDir=env.cfg.projectDirTree.getRltvReportSectionsGrPath()

reportFileName= env.cfg.projectDirTree.getReportSectionsFile()

report=open(reportFileName,'w')    #report latex file
#Functions to represent the interaction diagrams

def plotIntDiag(diag,title,xAxLab,yAxLab,grFileNm,reportFile,grRltvFileNm):
    diagGraphic=graph_material.InteractionDiagramGraphic(title)
    diagGraphic.decorations.xLabel= xAxLab
    diagGraphic.decorations.yLabel= yAxLab
    diagGraphic.setupGraphic(diag)
#    diagGraphic.savefig(grFileNm+'.eps')
    diagGraphic.savefig(grFileNm+'.jpeg')
    reportFile.write('\\begin{center}\n')
    reportFile.write('\includegraphics[width=80mm]{'+grRltvFileNm+'}\n')
    reportFile.write('\end{center}\n')

# #header

# report.write('# \documentclass{article}\n')
# report.write('# \usepackage{graphicx}\n')
# report.write('# \usepackage{multirow}\n')
# report.write('# \usepackage{wasysym}\n')
# report.write('# \usepackage{gensymb}\n\n')
# report.write('# \\begin{document}\n\n')


scSteel=None
scConcr=None
#for sect in sections.sections:
for sect in sect2Disp:
  sect.createSections()
  sect1=sect.lstRCSects[0]
  sect1.defRCSection(prep,'d')
  if writeSection2:
      sect2=sect.lstRCSects[1]
      sect2.defRCSection(prep,'d')
  #plotting of steel stress-strain diagram (only if not equal to precedent steel)
  if sect1.fiberSectionParameters.reinfSteelType!=scSteel or sect1.fiberSectionParameters.concrType!=scConcr:
     scSteel=sect1.fiberSectionParameters.reinfSteelType
     steelDiag=scSteel.plotDesignStressStrainDiagram(prep,path=report_graphics_outDir)
     steelGrphFile=scSteel.materialName+'_design_stress_strain_diagram'
     report.write('\\begin{center}\n')
     report.write('\includegraphics[width=120mm]{'+report_graphics_rltv_outDir+steelGrphFile+'}\n')
     report.write('\end{center}\n')
     scConcr=sect1.fiberSectionParameters.concrType
     concrDiag=scConcr.plotDesignStressStrainDiagram(prep,path=report_graphics_outDir)
     concrGrphFile=scConcr.materialName+'_design_stress_strain_diagram'
     report.write('\\begin{center}\n')
     report.write('\includegraphics[width=120mm]{'+report_graphics_rltv_outDir+concrGrphFile+'}\n')
     report.write('\end{center}\n')
     report.write('\\newpage\n\n')
  #Section 1
  # plotting of section geometric and mechanical properties
  sect1inf=section_report.SectionInfoHASimple(prep,sect1,sectGrWth=sectGrWth)
  texFileName=report_graphics_outDir+sect1.name+'.tex'
  textRltvFileName=report_graphics_rltv_outDir+sect1.name+'.tex'
  epsFileName=report_graphics_outDir+sect1.name+'.eps'
  epsRltvFileName=report_graphics_rltv_outDir+sect1.name+'.eps'
  sect1inf.writeReport(texFileName,epsFileName,epsRltvFileName)
  report.write('\input{'+textRltvFileName+'}\n')
  # plotting of interaction diagrams
  diagNMy= sect1.defInteractionDiagramNMy(prep)
  grFileName=report_graphics_outDir+sect1.name+'NMy'
  grRltvFileName=report_graphics_rltv_outDir+sect1.name+'NMy'
  plotIntDiag(diag=diagNMy,title=sect1.name+ ' N-My interaction diagram',xAxLab='My [kNm]',yAxLab='N [kN]',grFileNm=grFileName,reportFile=report,grRltvFileNm=grRltvFileName)
  diagNMz= sect1.defInteractionDiagramNMz(prep)
  grFileName=report_graphics_outDir+sect1.name+'NMz'
  grRltvFileName=report_graphics_rltv_outDir+sect1.name+'NMz'
  plotIntDiag(diag=diagNMz,title=sect1.name+ ' N-Mz interaction diagram',xAxLab='Mz [kNm]',yAxLab='N [kN]',grFileNm=grFileName,reportFile=report,grRltvFileNm=grRltvFileName)
  if writeSection2:
      #Section 2
      # plotting of section geometric and mechanical properties
      sect2inf=section_report.SectionInfoHASimple(prep,sect2,sectGrWth=sectGrWth)
      texFileName=report_graphics_outDir+sect2.name+'.tex'
      texRltvFileName=report_graphics_rltv_outDir+sect2.name+'.tex'
      epsFileName=report_graphics_outDir+sect2.name+'.eps'
      epsRltvFileName=report_graphics_rltv_outDir+sect2.name+'.eps'
      sect2inf.writeReport(texFileName,epsFileName,epsRltvFileName)
      report.write('\input{'+texRltvFileName+'}\n')
      # plotting of interaction diagrams
      diagNMy= sect2.defInteractionDiagramNMy(prep)
      grFileName=report_graphics_outDir+sect2.name+'NMy'
      grRltvFileName=report_graphics_rltv_outDir+sect2.name+'NMy'
      plotIntDiag(diag=diagNMy,title=sect2.name+ ' N-My interaction diagram',xAxLab='My [kNm]',yAxLab='N [kN]',grFileNm=grFileName,reportFile=report,grRltvFileNm=grRltvFileName)
      diagNMz= sect2.defInteractionDiagramNMz(prep)
      grFileName=report_graphics_outDir+sect2.name+'NMz'
      grRltvFileName=report_graphics_rltv_outDir+sect2.name+'NMz'
      plotIntDiag(diag=diagNMz,title=sect2.name+ ' N-Mz interaction diagram',xAxLab='Mz [kNm]',yAxLab='N [kN]',grFileNm=grFileName,reportFile=report,grRltvFileNm=grRltvFileName)
      
'''  
report.write('# \end{document}\n')
'''
report.close()
