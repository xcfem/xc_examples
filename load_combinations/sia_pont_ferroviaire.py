# -*- coding: utf-8 -*-

import loadCombinations
from actions.load_combination_utils import sia260
from actions.load_combination_utils import utils as ec


lcg= sia260.controlCombGenerator
PP1= lcg.insert("SIA260","permanentes",loadCombinations.Action("G","Poids propre"),"permanent","permanentes")

LM6= lcg.insert("SIA260","variables",loadCombinations.Action("LM6","Modèle de charge 6"),"voie_etroite_load_model_6","trafic_ferroviaire")
LM6.relationships.appendIncompatible("LM7")

LM7= lcg.insert("SIA260","variables",loadCombinations.Action("LM7","Modèle de charge 7"),"voie_etroite_load_model_7","trafic_ferroviaire")
LM7.relationships.appendIncompatible("LM6")

LM8= lcg.insert("SIA260","variables",loadCombinations.Action("LM8","Modèle de charge 8"),"voie_etroite_load_model_8","trafic_ferroviaire")
LM8.relationships.appendIncompatible("LM6")
LM8.relationships.appendIncompatible("LM7")

LM7DF= lcg.insert("SIA260","variables",loadCombinations.Action("LM7DF","Démarrage"),"voie_etroite_load_model_7","trafic_ferroviaire")
LM7DF.relationships.appendMain("LM7")
LM7DF.relationships.appendIncompatible("LM7FC")

LM7FC= lcg.insert("SIA260","variables",loadCombinations.Action("LM7FC","Force centrifugue"),"voie_etroite_load_model_7","trafic_ferroviaire")
LM7FC.relationships.appendMain("LM7")

Vent= lcg.insert("SIA260","variables",loadCombinations.Action("V","Vent"),"vent","variables")
Vent.relationships.appendMain("LM8")

TPos= lcg.insert("SIA260","variables",loadCombinations.Action("TPos","Température +"),"temperature","variables")
TPos.relationships.appendIncompatible("TNeg")
TPos.relationships.appendIncompatible("LM8")
TNeg= lcg.insert("SIA260","variables",loadCombinations.Action("TNeg","Température -"),"temperature","variables")
TNeg.relationships.appendIncompatible("TPos")
TNeg.relationships.appendIncompatible("LM8")

LM6DR1= lcg.insert("SIA260","accidentales",loadCombinations.Action("LM6DR1","Dérraillement type 1 (LM6)."),"voie_etroite_choc","accidentales")
LM6DR1.relationships.appendIncompatible("TPos")
LM6DR1.relationships.appendIncompatible("TNeg")
LM6DR1.relationships.appendIncompatible("LM.*")

LM7DR1= lcg.insert("SIA260","accidentales",loadCombinations.Action("LM7DR1","Dérraillement type 1 (LM7)."),"voie_etroite_choc","accidentales")
LM7DR1.relationships.appendIncompatible("TPos")
LM7DR1.relationships.appendIncompatible("TNeg")
LM7DR1.relationships.appendIncompatible("LM.*")

LMDR2= lcg.insert("SIA260","accidentales",loadCombinations.Action("LMDR2","Dérraillement type 2."),"voie_etroite_choc","accidentales")
LMDR2.relationships.appendIncompatible("TPos")
LMDR2.relationships.appendIncompatible("TNeg")
LMDR2.relationships.appendIncompatible("LM.*")

Choc= lcg.insert("SIA260","accidentales",loadCombinations.Action("Choc","Choc."),"voie_etroite_choc","accidentales")
Choc.relationships.appendMain("LM7")
Choc.relationships.appendIncompatible("TPos")
Choc.relationships.appendIncompatible("TNeg")

lcg.genera()



print("ELS fréq.")
ec.writeXCLoadCombinations(prefix= "ELSF", loadCombinations= lcg.getLoadCombinations.getSLSFrequentCombinations, outputFileName= "load_combs_els_freq.py")


print("ELS quasi perm.")
ec.writeXCLoadCombinations(prefix= "ELSQP", loadCombinations= lcg.getLoadCombinations.getSLSQuasiPermanentCombinations, outputFileName= "load_combs_els_qp.py")


print("ELU")
ec.writeXCLoadCombinations(prefix= "ELU", loadCombinations= lcg.getLoadCombinations.getULSTransientCombinations, outputFileName= "load_combs_elu.py")

print("ACCID")
ec.writeXCLoadCombinations(prefix= "ELUA", loadCombinations= lcg.getLoadCombinations.getULSAccidentalCombinations, outputFileName= "load_combs_acc.py")

