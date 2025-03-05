# -*- coding: utf-8 -*-
from materials.sections.fiber_section import section_report 
from postprocess.reports import graph_material 
import matplotlib.pyplot as plt
from postprocess.config import default_config
from postprocess.reports import rc_section_reports as rcsr
# import local modules
workingDirectory= default_config.setWorkingDirectory()
import env_config as env
import xc_init
#import xc_sets as xcS
from calculations import RC_sections_def as RCsect
# Common variables
out=xc_init.out ; modelSpace=xc_init.modelSpace ; prep=xc_init.prep
#
rcSects2Report=[RCsect.lstRCsects[-1]]

RCreport=rcsr.RCSectionReportGenerator(env.cfg)
RCreport.rcSectionsReport(prep,rcSects2Report,writeSection2= True)

