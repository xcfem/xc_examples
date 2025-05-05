# -*- coding: utf-8 -*-
''' Report shrinkage calculation example.'''

from __future__ import division
from __future__ import print_function

from materials.ec2 import EC2_materials
from postprocess.reports import report_shrinkage

import latex_functions as lf
B= 10
H= 0.25
area_deck=B*H
perim_deck=2*(B+H)
#       Data
outputFileNm='./shrinkage_report.tex'
#Type of concrete used in the deck slab
concrDeck=EC2_materials.C30
concrDeck.cemType='N'   #class N cement
RH=70                   #ambient relative humidity(%)

#Shrinkage deformation at traffic openning
t=10000     #age of the concrete t infinito
ts=1     #drying shrinkage begins at the age 1 day
Ac=area_deck     #area of the concrete slab (m2)
#print ('Ac=',Ac)
u=perim_deck     #perimeter exposed to drying (m)
#         end data


#print ('u=',u)
h0=2*Ac/u    #notional size of the member h0 (m)
#print ('h0=',h0)
#   autogenous shrinkage
Epscainf=concrDeck.getShrEpscainf(t)  #coefficient for calculating the autogenous shrinkage strain
#print( 'Epscainf=',Epscainf)
Betaast=concrDeck.getShrBetaast(t)    #coefficient for calculating the autogenous shrinkage strain
#print( 'Betaast=',Betaast)
Epsca=concrDeck.getShrEpsca(t)        #Autogenous shrinkage strain
#print( 'Epsca=',Epsca)

#   drying shrinkage
BetaRH=concrDeck.getShrBetaRH(RH)   #Coefficient for the calculation of the basic drying shrinkage strain
#print( 'BetaRH=',BetaRH)
Alfads1=concrDeck.getShrAlfads1()   #Coefficient for the calculation of the basic drying shrinkage strain
#print( 'Alfads1=',Alfads1)
Alfads2=concrDeck.getShrAlfads2()   #Coefficient for the calculation of the
                                    #basic drying shrinkage strain
#print( 'Alfads2=',Alfads2)
Epscd0=concrDeck.getShrEpscd0(RH)   #Basic drying shrinkage strain
#print( 'Epscd0=',Epscd0)
Kh=concrDeck.getShrKh(h0)         #coefficient  for the calculation of the
                                    #drying shrinkage strain
#print( 'Kh=',Kh)
Betadstts=concrDeck.getShrBetadstts(t,ts,h0)   #coefficient  for the
                                    #calculation of the drying shrinkage strain
#print( 'Betadstts=',Betadstts)
Epscd=concrDeck.getShrEpscd(t,ts,RH,h0)   #Drying shrinkage strain
#print( 'Epscd=',Epscd)
Epscs=concrDeck.getShrEpscs(t,ts,RH,h0)   #Total shrinkage 
#print( 'Epscs=',Epscs)

outputF= open(outputFileNm, 'w')
outputF.write(lf.gen_latex_simple_document_head())
outputF.write(report_shrinkage.latex_spanish(concrDeck.fck, RH, Ac, u, h0, Epscainf, Betaast, t, Epsca, BetaRH, Alfads1, Alfads2, Epscd0, Kh, Betadstts, Epscd, Epscs))
outputF.write('\\end{document} \n')
outputF.close()
