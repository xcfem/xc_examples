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
for rcs in sect2Disp:
    rcs.pdfReport(graphicWidth=sectGrWth,showPDF= True, keepPDF= False, preprocessor= prep, matDiagType= 'k')
