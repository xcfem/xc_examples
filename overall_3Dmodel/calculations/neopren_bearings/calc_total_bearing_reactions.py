# -*- coding: utf-8 -*-
import math
from solution import predefined_solutions
from postprocess.config import default_config
import yaml
from pathlib import Path

# import local modules
import sys
workingDirectory= default_config.findWorkingDirectory()+'/' #search env_config.py
sys.path.append(workingDirectory)
import data_slab as datS
import xc_model as model #FE model generation
import load_case_definition as LCdef

dictLCG=yaml.safe_load(Path(workingDirectory+'LC_graph.yaml').read_text())
f = open('result_total_bearing_reactions_1.tex','w')
analysis= predefined_solutions.simple_static_linear(model.FEcase)
for ky in LCdef.listLCs_1:
    lcg=dictLCG[ky]
    model.modelSpace.removeAllLoadPatternsFromDomain()
    model.modelSpace.addLoadCaseToDomain(lcg['LCname'])
#    model.out.displayLoads()
    model.modelSpace.revertToStart()
    result= analysis.analyze(1)
    model.modelSpace.calculateNodalReactions()
    totalRx=0; totalRy=0; totalRz=0
    # pots
    for e in [model.potPUpier1,model.potPLpier1]:
        ang=datS.skewPier1Rad
        Flong=e.getFXlocal()
        Ftransv=e.getFYlocal()
        totalRx-=-Flong*math.sin(ang)-Ftransv*math.cos(ang)
        totalRy-=Flong*math.cos(ang)-Ftransv*math.sin(ang)
        totalRz-=e.getFZlocal()
    for e in [model.potPUpier2,model.potPLpier2]:
        ang=datS.skewPier2Rad
        Flong=e.getFXlocal()
        Ftransv=e.getFYlocal()
        totalRx-=-Flong*math.sin(ang)-Ftransv*math.cos(ang)
        totalRy-=Flong*math.cos(ang)-Ftransv*math.sin(ang)
        totalRz-=e.getFZlocal()
    # elastomeric bearings
    for e in model.elastomericBearings.elements:
        mx=e.getMaterials()[0]
        my=e.getMaterials()[1]
        mz=e.getMaterials()[2]
        totalRx-=mx.getStress()
        totalRy-=my.getStress()
        totalRz-=mz.getStress()
    # for pnt in model.WslabPileBasePoints+model.EslabPileBasePoints:
    #     n=pnt.getNode()
    #     Rn=n.getReaction
    #     print('Rz=', Rn[2])
    #     totalRx+=Rn[0]
    #     totalRy+=Rn[1]
    #     totalRz+=Rn[2]
    f.write('\n')
    f.write('        *** ACCIÓN '+lcg['description']+ ' *** \n')
    f.write('total Fx='+str(round(totalRx*1e-3,2))+' kN \n' )
    f.write('total Fy='+str(round(totalRy*1e-3,2)) +' kN \n' )
    f.write('total Fz='+str(round(totalRz*1e-3,2)) +' kN \n' )
    f.write('\n')
    # print('        *** ACCIÓN '+lcg['description']+ ' *** \n')
    # print('total Fx='+str(round(totalRx*1e-3,2))+' kN \n' )
    # print('total Fy='+str(round(totalRy*1e-3,2)) +' kN \n' )
    # print('total Fz='+str(round(totalRz*1e-3,2)) +' kN \n' )
    # Reactions at slab piles
    
f.close()

         
    

       

    
