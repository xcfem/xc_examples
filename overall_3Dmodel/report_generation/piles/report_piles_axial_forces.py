import os
from solution import predefined_solutions
from postprocess.config import default_config

# import local modules
import sys
workingDirectory= default_config.setWorkingDirectory()+'/' #search env_config.py
import xc_model as xcM #FE model generation
import xc_combinations as xcC
import env_config as env

modelSpace=xcM.modelSpace
#Data combinaciones y nombre del fichero
reactNod={'pile1':{'node':xcM.nBottPile1,'description':'Pilote lado pérgola'},
          'pile2':{'node':xcM.nBottPile2,'description':'Pilote central'},
          'pile3':{'node':xcM.nBottPile3,'description':'Pilote lado viaducto'},
          }

# comentar para combinaciones quasipermanentes
combs=xcC.combContainer.SLS.rare
texFileName='pile_SLS_caract_Nmax.tex'
captionTable='Pilotes pila 1. Axil máximo en combinaciones de ELS caracterísitcas'
'''
# comentar para combinaciones ELS caracterísricas
combs=xcC.combContainer.SLS.qp
texFileName='pile_SLS_qperm_Nmax.tex'
captionTable='Pilotes pila 1. Axil máximo en combinaciones de ELS casipermanentes'
'''
# END data

# Calculation
for n in reactNod.keys():
    reactNod[n]['Nmax']=0
    reactNod[n]['combNmax']=' '
    reactNod[n]['combNmaxExpr']=' '
    
analysis= predefined_solutions.simple_static_linear(xcM.FEcase)
for cmb in combs.keys():
    cmbExpr=combs[cmb].expr
    modelSpace.addNewLoadCaseToDomain(cmb,cmbExpr)
    result= analysis.analyze(1)
    modelSpace.calculateNodalReactions()
    for n in reactNod.keys():
        N=reactNod[n]['node'].getReaction[2]
        if N > reactNod[n]['Nmax']:
            reactNod[n]['Nmax']=N
            reactNod[n]['combNmax']=cmb
            reactNod[n]['combNmaxExpr']=cmbExpr
    modelSpace.removeLoadCombination(cmb)

# Write table
import latex_functions as lf

texDir=env.cfg.projectDirTree.getFullReportPath()
texFileName=texDir+texFileName
texF=open(texFileName,'w') #
headLongtable=lf.gen_longtable_head(
    headTitles=['Posición','Axil máximo (kN)', 'Combinación'],
    justif='lrl',
    caption=captionTable,
    tit2ndLine=None
    )
texF.write(headLongtable)
for n in reactNod.keys():
    texF.write(reactNod[n]['description'] + ' & '+ str(round(reactNod[n]['Nmax']*1e-3,2)) + ' & '+ str(reactNod[n]['combNmax']) + '- '+str(reactNod[n]['combNmaxExpr'])+'\\\\ \n')
texF.write('\\end{longtable} \n')
texF.write('\\end{center}')
texF.close()
    
# Display maximum axial loads
out=xcM.out
for n in reactNod.keys():
    modelSpace.addNewLoadCaseToDomain(reactNod[n]['combNmax'],reactNod[n]['combNmaxExpr'])
    result= analysis.analyze(1)
    out.displayIntForcDiag('N',xcM.pileSet)
    modelSpace.removeLoadCombination(reactNod[n]['combNmax'])
                

    
    
