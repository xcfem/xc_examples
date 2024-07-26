# -*- coding: utf-8 -*-
from solution import predefined_solutions
from postprocess.config import default_config

# import local modules
workingDirectory= default_config.setWorkingDirectory() # search env_config.py
import model_gen as model #FE model generation

for ls in [model.QearthPressWall,model.QearthPWallStrL]:
    model.modelSpace.removeAllLoadPatternsFromDomain()
    model.modelSpace.addLoadCaseToDomain(ls.name)
    analysis= predefined_solutions.simple_static_linear(model.FEcase)
    result= analysis.analyze(1)
    model.out.displayDispRot('uX')
    model.out.displayDispRot('uY')
    model.out.displayDispRot('uZ')
    model.out.displayIntForc('N1',model.wall)
    model.out.displayIntForc('N2',model.wall)
    model.out.displayIntForc('N12',model.wall)
    model.out.displayIntForc('Q1',model.wall)
    model.out.displayIntForc('Q2',model.wall)
    model.out.displayIntForc('M1',model.wall)
    model.out.displayIntForc('M2',model.wall)
    model.out.displayIntForc('M12',model.wall)
    
