import os
from solution import predefined_solutions
from postprocess.config import default_config

# import local modules
import sys
workingDirectory= default_config.setWorkingDirectory()+'/' #search env_config.py
import xc_model as xcM #FE model generation
import xc_combinations as xcC
import env_config as env

out=xcM.out

modelSpace=xcM.modelSpace
#Data combinaciones y nombre del fichero
tieElem={'tie12':{'elem':xcM.tieSet.elements[0],'description':'Tirante P1-P2 (lado pérg-central)'},
          'tie23':{'elem':xcM.tieSet.elements[1],'description':'Tirante P3-P2 (lado viad-central)'},
          'tie13':{'elem':xcM.tieSet.elements[2],'description':'Tirante P1-P3 (lado perg- lado viad)'},
          }
combs=xcC.combContainer.ULS.perm
texFileName='tie_ULS_perm_Nmax.tex'
captionTable='Tirantes encepado pila 1. Axil máximo en combinaciones de ELU'

# END data

# Calculation
for e in tieElem.keys():
    tieElem[e]['Nmax']=0
    tieElem[e]['combNmax']=' '
    tieElem[e]['combNmaxExpr']=' '
    
analysis= predefined_solutions.simple_static_linear(xcM.FEcase)
for cmb in combs.keys():
    cmbExpr=combs[cmb].expr
    modelSpace.addNewLoadCaseToDomain(cmb,cmbExpr)
    result= analysis.analyze(1)
    modelSpace.calculateNodalReactions()
    for e in tieElem.keys():
        N=tieElem[e]['elem'].getN()
        print
        if N > tieElem[e]['Nmax']:
            tieElem[e]['Nmax']=N
            tieElem[e]['combNmax']=cmb
            tieElem[e]['combNmaxExpr']=cmbExpr
    modelSpace.removeLoadCombination(cmb)

# Write table
import latex_functions as lf

texDir=env.cfg.projectDirTree.getFullReportPath()
texFileName=texDir+texFileName
texF=open(texFileName,'w') #
headLongtable=lf.gen_longtable_head(
    headTitles=['Elemento','Axil máximo (kN)', 'Combinación'],
    justif='lrl',
    caption=captionTable,
    tit2ndLine=None
    )
texF.write(headLongtable)
for e in tieElem.keys():
    texF.write(tieElem[e]['description'] + ' & '+ str(round(tieElem[e]['Nmax']*1e-3,2)) + ' & '+ str(tieElem[e]['combNmax']) + '- '+str(tieElem[e]['combNmaxExpr'])+'\\\\ \n')
texF.write('\\end{longtable} \n')
texF.write('\\end{center}')
texF.close()

# Display maximum axial loads
for e in tieElem.keys():
    modelSpace.addNewLoadCaseToDomain(tieElem[e]['combNmax'],tieElem[e]['combNmaxExpr'])
    result= analysis.analyze(1)
    out.displayIntForcDiag('N',xcM.tieSet)
    modelSpace.removeLoadCombination(tieElem[e]['combNmax'])
    

    

    
    
