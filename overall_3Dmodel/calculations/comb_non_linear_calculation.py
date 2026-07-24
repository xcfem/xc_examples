# -*- coding: utf-8 -*-
from postprocess.config import default_config
from solution import predefined_solutions
# local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import env_config as env
#import steel_beams_def as sMemb # steel members
import xc_init
import xc_geom as xcG # Geometry and sets
import xc_materials as xcM # Materials
import xc_fem as xcF # FE model
import xc_boundc as xcB # Boundary conditions
import xc_loads as xcL # loads (typical)
import xc_roadway_loads as xcLr # roadway loads
import xc_lcases as xcLC # load cases
import xc_combinations as xcC # SLS and ULS combinations

class CustomSolver(predefined_solutions.PlainNewtonRaphsonMUMPS):
    def __init__(self, prb):
        super(CustomSolver,self).__init__(prb= prb, name= 'test', maxNumIter= 30, printFlag= 1, convergenceTestTol= 1e-1)

cmb=xcC.combContainer.SLS.rare['ELSR1']
modelSpace.addNewLoadCaseToDomain(cmb.name,cmb.expr)
modelSpace.setSolutionProcedureType(CustomSolver)
modelSpace.analyze(calculateNodalReactions=True)
