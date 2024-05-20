# -*- coding: utf-8 -*-
#!/usr/bin/env python
''' XC Python version of the script described here:

https://opensees.berkeley.edu/wiki/index.php/Excavation_Supported_by_Cantilevered_Sheet_Pile_Wall

#######################################################################
#                                                                     #
#  Excavation of cohesionless soil supported by a cantilevered sheet  #
#  pile wall.  2D Plane Strain analysis.  Beam elements define the    #
#  wall, and beam-contact elements are used to create a frictional    #
#  soil-pile interface. Initial state analysis is used to create      #
#  an initial state of stress and strain due to gravity without the   #
#  corresponding displacements.                                       #
#                                                                     #
#   Created by:  Chris McGann                                         #
#                Pedro Arduino                                        #
#              --University of Washington--                           #
#                                                                     #
# ---> Basic units are kN and m                                       #
#                                                                     #
#######################################################################
#
'''

__author__= "Luis C. Pérez Tato"
__copyright__= "Copyright 2021, LCPT AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es ana.ortega@ciccp.es"

import math
import xc
import geom
from model import predefined_spaces
from model.boundary_cond import opensees_style
from materials import typical_materials
from misc_utils import log_messages as lmsg

#-----------------------------------------------------------------------------
#  0. DEFINE FE PROBLEM
#-----------------------------------------------------------------------------
feProblem= xc.FEProblem()
preprocessor=  feProblem.getPreprocessor
nodes= preprocessor.getNodeHandler 
modelSpace= predefined_spaces.SolidMechanics2D(nodes)

#-----------------------------------------------------------------------------
#  1. CREATE SOIL NODES AND FIXITIES
#-----------------------------------------------------------------------------
# define soil nodes
n1= modelSpace.newNodeXY( -5.250, 0.000)
n2= modelSpace.newNodeXY( -5.250, 0.500)
n3= modelSpace.newNodeXY( -4.750, 0.000)
n4= modelSpace.newNodeXY( -4.750, 0.500)
n5= modelSpace.newNodeXY( -4.250, 0.000)
n6= modelSpace.newNodeXY( -5.250, 1.000)
n7= modelSpace.newNodeXY( -4.750, 1.000)
n8= modelSpace.newNodeXY( -4.250, 0.500)
n9= modelSpace.newNodeXY( -4.250, 1.000)
n10= modelSpace.newNodeXY( -5.250, 1.500)
n11= modelSpace.newNodeXY( -3.750, 0.000)
n12= modelSpace.newNodeXY( -4.750, 1.500)
n13= modelSpace.newNodeXY( -3.750, 0.500)
n14= modelSpace.newNodeXY( -3.750, 1.000)
n15= modelSpace.newNodeXY( -4.250, 1.500)
n16= modelSpace.newNodeXY( -3.250, 0.000)
n17= modelSpace.newNodeXY( -5.250, 2.000)
n18= modelSpace.newNodeXY( -4.750, 2.000)
n19= modelSpace.newNodeXY( -3.250, 0.500)
n20= modelSpace.newNodeXY( -3.750, 1.500)
n21= modelSpace.newNodeXY( -3.250, 1.000)
n22= modelSpace.newNodeXY( -4.250, 2.000)
n23= modelSpace.newNodeXY( -5.250, 2.500)
n24= modelSpace.newNodeXY( -2.750, 0.000)
n25= modelSpace.newNodeXY( -3.250, 1.500)
n26= modelSpace.newNodeXY( -3.750, 2.000)
n27= modelSpace.newNodeXY( -4.750, 2.500)
n28= modelSpace.newNodeXY( -2.750, 0.500)
n29= modelSpace.newNodeXY( -4.250, 2.500)
n30= modelSpace.newNodeXY( -2.750, 1.000)
n31= modelSpace.newNodeXY( -3.250, 2.000)
n32= modelSpace.newNodeXY( -3.750, 2.500)
n33= modelSpace.newNodeXY( -2.750, 1.500)
n34= modelSpace.newNodeXY( -5.250, 3.000)
n35= modelSpace.newNodeXY( -2.250, 0.000)
n36= modelSpace.newNodeXY( -4.750, 3.000)
n37= modelSpace.newNodeXY( -2.250, 0.500)
n38= modelSpace.newNodeXY( -4.250, 3.000)
n39= modelSpace.newNodeXY( -2.250, 1.000)
n40= modelSpace.newNodeXY( -3.250, 2.500)
n41= modelSpace.newNodeXY( -2.750, 2.000)
n42= modelSpace.newNodeXY( -3.750, 3.000)
n43= modelSpace.newNodeXY( -2.250, 1.500)
n44= modelSpace.newNodeXY( -5.250, 3.500)
n45= modelSpace.newNodeXY( -1.750, 0.000)
n46= modelSpace.newNodeXY( -2.750, 2.500)
n47= modelSpace.newNodeXY( -4.750, 3.500)
n48= modelSpace.newNodeXY( -1.750, 0.500)
n49= modelSpace.newNodeXY( -2.250, 2.000)
n50= modelSpace.newNodeXY( -3.250, 3.000)
n51= modelSpace.newNodeXY( -1.750, 1.000)
n52= modelSpace.newNodeXY( -4.250, 3.500)
n53= modelSpace.newNodeXY( -3.750, 3.500)
n54= modelSpace.newNodeXY( -1.750, 1.500)
n55= modelSpace.newNodeXY( -2.250, 2.500)
n56= modelSpace.newNodeXY( -2.750, 3.000)
n57= modelSpace.newNodeXY( -5.250, 4.000)
n58= modelSpace.newNodeXY( -1.250, 0.000)
n59= modelSpace.newNodeXY( -1.250, 0.500)
n60= modelSpace.newNodeXY( -4.750, 4.000)
n61= modelSpace.newNodeXY( -1.750, 2.000)
n62= modelSpace.newNodeXY( -3.250, 3.500)
n63= modelSpace.newNodeXY( -4.250, 4.000)
n64= modelSpace.newNodeXY( -1.250, 1.000)
n65= modelSpace.newNodeXY( -2.250, 3.000)
n66= modelSpace.newNodeXY( -3.750, 4.000)
n67= modelSpace.newNodeXY( -1.250, 1.500)
n68= modelSpace.newNodeXY( -1.750, 2.500)
n69= modelSpace.newNodeXY( -2.750, 3.500)
n70= modelSpace.newNodeXY( -1.250, 2.000)
n71= modelSpace.newNodeXY( -3.250, 4.000)
n72= modelSpace.newNodeXY( -0.750, 0.000)
n73= modelSpace.newNodeXY( -5.250, 4.500)
n74= modelSpace.newNodeXY( -4.750, 4.500)
n75= modelSpace.newNodeXY( -0.750, 0.500)
n76= modelSpace.newNodeXY( -4.250, 4.500)
n77= modelSpace.newNodeXY( -1.750, 3.000)
n78= modelSpace.newNodeXY( -2.250, 3.500)
n79= modelSpace.newNodeXY( -0.750, 1.000)
n80= modelSpace.newNodeXY( -1.250, 2.500)
n81= modelSpace.newNodeXY( -2.750, 4.000)
n82= modelSpace.newNodeXY( -3.750, 4.500)
n83= modelSpace.newNodeXY( -0.750, 1.500)
n84= modelSpace.newNodeXY( -0.750, 2.000)
n85= modelSpace.newNodeXY( -3.250, 4.500)
n86= modelSpace.newNodeXY( -1.750, 3.500)
n87= modelSpace.newNodeXY( -5.250, 5.000)
n88= modelSpace.newNodeXY( -0.250, 0.000)
n89= modelSpace.newNodeXY( -1.250, 3.000)
n90= modelSpace.newNodeXY( -2.250, 4.000)
n91= modelSpace.newNodeXY( -4.750, 5.000)
n92= modelSpace.newNodeXY( -0.250, 0.500)
n93= modelSpace.newNodeXY( -0.250, 1.000)
n94= modelSpace.newNodeXY( -4.250, 5.000)
n95= modelSpace.newNodeXY( -0.750, 2.500)
n96= modelSpace.newNodeXY( -2.750, 4.500)
n97= modelSpace.newNodeXY( -3.750, 5.000)
n98= modelSpace.newNodeXY( -0.250, 1.500)
n102= modelSpace.newNodeXY( -1.750, 4.000)
n103= modelSpace.newNodeXY( -1.250, 3.500)
n104= modelSpace.newNodeXY( -3.250, 5.000)
n105= modelSpace.newNodeXY( -0.250, 2.000)
n107= modelSpace.newNodeXY( -0.750, 3.000)
n108= modelSpace.newNodeXY( -2.250, 4.500)
n109= modelSpace.newNodeXY( 0.250, 0.000)
n110= modelSpace.newNodeXY( -5.250, 5.500)
n111= modelSpace.newNodeXY( -4.750, 5.500)
n112= modelSpace.newNodeXY( 0.250, 0.500)
n114= modelSpace.newNodeXY( -2.750, 5.000)
n115= modelSpace.newNodeXY( -0.250, 2.500)
n116= modelSpace.newNodeXY( 0.250, 1.000)
n117= modelSpace.newNodeXY( -4.250, 5.500)
n118= modelSpace.newNodeXY( -1.250, 4.000)
n119= modelSpace.newNodeXY( 0.250, 1.500)
n120= modelSpace.newNodeXY( -3.750, 5.500)
n121= modelSpace.newNodeXY( -1.750, 4.500)
n122= modelSpace.newNodeXY( -0.750, 3.500)
n124= modelSpace.newNodeXY( -2.250, 5.000)
n125= modelSpace.newNodeXY( -0.250, 3.000)
n126= modelSpace.newNodeXY( 0.250, 2.000)
n127= modelSpace.newNodeXY( -3.250, 5.500)
n129= modelSpace.newNodeXY( -5.250, 6.000)
n130= modelSpace.newNodeXY( 0.750, 0.000)
n131= modelSpace.newNodeXY( 0.750, 0.500)
n132= modelSpace.newNodeXY( -1.250, 4.500)
n133= modelSpace.newNodeXY( -4.750, 6.000)
n134= modelSpace.newNodeXY( -0.750, 4.000)
n135= modelSpace.newNodeXY( 0.250, 2.500)
n136= modelSpace.newNodeXY( -2.750, 5.500)
n137= modelSpace.newNodeXY( -4.250, 6.000)
n138= modelSpace.newNodeXY( 0.750, 1.000)
n139= modelSpace.newNodeXY( -0.250, 3.500)
n140= modelSpace.newNodeXY( -1.750, 5.000)
n142= modelSpace.newNodeXY( -3.750, 6.000)
n143= modelSpace.newNodeXY( 0.750, 1.500)
n144= modelSpace.newNodeXY( 0.250, 3.000)
n145= modelSpace.newNodeXY( -2.250, 5.500)
n146= modelSpace.newNodeXY( 0.750, 2.000)
n147= modelSpace.newNodeXY( -3.250, 6.000)
n148= modelSpace.newNodeXY( -0.750, 4.500)
n149= modelSpace.newNodeXY( -1.250, 5.000)
n150= modelSpace.newNodeXY( -0.250, 4.000)
n152= modelSpace.newNodeXY( 1.250, 0.000)
n153= modelSpace.newNodeXY( 0.750, 2.500)
n154= modelSpace.newNodeXY( -5.250, 6.500)
n155= modelSpace.newNodeXY( -2.750, 6.000)
n156= modelSpace.newNodeXY( -4.750, 6.500)
n157= modelSpace.newNodeXY( 1.250, 0.500)
n158= modelSpace.newNodeXY( 0.250, 3.500)
n159= modelSpace.newNodeXY( -1.750, 5.500)
n160= modelSpace.newNodeXY( -4.250, 6.500)
n161= modelSpace.newNodeXY( 1.250, 1.000)
n162= modelSpace.newNodeXY( 1.250, 1.500)
n163= modelSpace.newNodeXY( -3.750, 6.500)
n164= modelSpace.newNodeXY( 0.750, 3.000)
n165= modelSpace.newNodeXY( -2.250, 6.000)
n166= modelSpace.newNodeXY( -0.250, 4.500)
n167= modelSpace.newNodeXY( -0.750, 5.000)
n169= modelSpace.newNodeXY( -3.250, 6.500)
n170= modelSpace.newNodeXY( 1.250, 2.000)
n171= modelSpace.newNodeXY( 0.250, 4.000)
n172= modelSpace.newNodeXY( -1.250, 5.500)
n173= modelSpace.newNodeXY( 0.750, 3.500)
n174= modelSpace.newNodeXY( -1.750, 6.000)
n175= modelSpace.newNodeXY( -2.750, 6.500)
n176= modelSpace.newNodeXY( 1.250, 2.500)
n177= modelSpace.newNodeXY( -5.250, 7.000)
n178= modelSpace.newNodeXY( 1.750, 0.000)
n179= modelSpace.newNodeXY( -4.750, 7.000)
n180= modelSpace.newNodeXY( 1.750, 0.500)
n181= modelSpace.newNodeXY( 1.750, 1.000)
n182= modelSpace.newNodeXY( -0.250, 5.000)
n183= modelSpace.newNodeXY( -4.250, 7.000)
n185= modelSpace.newNodeXY( 0.250, 4.500)
n186= modelSpace.newNodeXY( -0.750, 5.500)
n187= modelSpace.newNodeXY( 1.750, 1.500)
n188= modelSpace.newNodeXY( -2.250, 6.500)
n189= modelSpace.newNodeXY( 1.250, 3.000)
n190= modelSpace.newNodeXY( -3.750, 7.000)
n191= modelSpace.newNodeXY( 0.750, 4.000)
n192= modelSpace.newNodeXY( -1.250, 6.000)
n193= modelSpace.newNodeXY( 1.750, 2.000)
n194= modelSpace.newNodeXY( -3.250, 7.000)
n195= modelSpace.newNodeXY( -1.750, 6.500)
n196= modelSpace.newNodeXY( 1.250, 3.500)
n198= modelSpace.newNodeXY( 1.750, 2.500)
n199= modelSpace.newNodeXY( -0.250, 5.500)
n200= modelSpace.newNodeXY( 0.250, 5.000)
n201= modelSpace.newNodeXY( -2.750, 7.000)
n202= modelSpace.newNodeXY( -0.750, 6.000)
n203= modelSpace.newNodeXY( 0.750, 4.500)
n204= modelSpace.newNodeXY( -5.250, 7.500)
n205= modelSpace.newNodeXY( 2.250, 0.000)
n206= modelSpace.newNodeXY( -4.750, 7.500)
n207= modelSpace.newNodeXY( 2.250, 0.500)
n208= modelSpace.newNodeXY( -4.250, 7.500)
n209= modelSpace.newNodeXY( 2.250, 1.000)
n210= modelSpace.newNodeXY( 1.750, 3.000)
n211= modelSpace.newNodeXY( -2.250, 7.000)
n212= modelSpace.newNodeXY( 1.250, 4.000)
n213= modelSpace.newNodeXY( -1.250, 6.500)
n214= modelSpace.newNodeXY( 2.250, 1.500)
n215= modelSpace.newNodeXY( -3.750, 7.500)
n216= modelSpace.newNodeXY( -3.250, 7.500)
n217= modelSpace.newNodeXY( 2.250, 2.000)
n218= modelSpace.newNodeXY( 0.250, 5.500)
n220= modelSpace.newNodeXY( 0.750, 5.000)
n221= modelSpace.newNodeXY( -0.250, 6.000)
n222= modelSpace.newNodeXY( -1.750, 7.000)
n223= modelSpace.newNodeXY( 1.750, 3.500)
n224= modelSpace.newNodeXY( -0.750, 6.500)
n225= modelSpace.newNodeXY( 1.250, 4.500)
n226= modelSpace.newNodeXY( -2.750, 7.500)
n227= modelSpace.newNodeXY( 2.250, 2.500)
n228= modelSpace.newNodeXY( -5.250, 8.000)
n229= modelSpace.newNodeXY( 2.750, 0.000)
n230= modelSpace.newNodeXY( -4.750, 8.000)
n231= modelSpace.newNodeXY( 2.750, 0.500)
n232= modelSpace.newNodeXY( -4.250, 8.000)
n233= modelSpace.newNodeXY( 2.750, 1.000)
n234= modelSpace.newNodeXY( 1.750, 4.000)
n235= modelSpace.newNodeXY( -1.250, 7.000)
n236= modelSpace.newNodeXY( -2.250, 7.500)
n237= modelSpace.newNodeXY( 2.250, 3.000)
n238= modelSpace.newNodeXY( -3.750, 8.000)
n239= modelSpace.newNodeXY( 0.750, 5.500)
n240= modelSpace.newNodeXY( 2.750, 1.500)
n241= modelSpace.newNodeXY( 0.250, 6.000)
n243= modelSpace.newNodeXY( 1.250, 5.000)
n244= modelSpace.newNodeXY( -0.250, 6.500)
n245= modelSpace.newNodeXY( 2.750, 2.000)
n246= modelSpace.newNodeXY( -3.250, 8.000)
n247= modelSpace.newNodeXY( -1.750, 7.500)
n248= modelSpace.newNodeXY( 2.250, 3.500)
n249= modelSpace.newNodeXY( -0.750, 7.000)
n250= modelSpace.newNodeXY( 1.750, 4.500)
n251= modelSpace.newNodeXY( -2.750, 8.000)
n252= modelSpace.newNodeXY( 2.750, 2.500)
n253= modelSpace.newNodeXY( 0.750, 6.000)
n254= modelSpace.newNodeXY( 2.250, 4.000)
n255= modelSpace.newNodeXY( -5.250, 8.500)
n256= modelSpace.newNodeXY( 3.250, 0.000)
n257= modelSpace.newNodeXY( -1.250, 7.500)
n258= modelSpace.newNodeXY( -4.750, 8.500)
n259= modelSpace.newNodeXY( 1.250, 5.500)
n260= modelSpace.newNodeXY( 0.250, 6.500)
n261= modelSpace.newNodeXY( 3.250, 0.500)
n262= modelSpace.newNodeXY( -2.250, 8.000)
n263= modelSpace.newNodeXY( 2.750, 3.000)
n265= modelSpace.newNodeXY( -4.250, 8.500)
n266= modelSpace.newNodeXY( 3.250, 1.000)
n267= modelSpace.newNodeXY( -0.250, 7.000)
n268= modelSpace.newNodeXY( 1.750, 5.000)
n269= modelSpace.newNodeXY( -3.750, 8.500)
n270= modelSpace.newNodeXY( 3.250, 1.500)
n271= modelSpace.newNodeXY( -3.250, 8.500)
n272= modelSpace.newNodeXY( -1.750, 8.000)
n273= modelSpace.newNodeXY( 3.250, 2.000)
n274= modelSpace.newNodeXY( 2.750, 3.500)
n275= modelSpace.newNodeXY( 2.250, 4.500)
n276= modelSpace.newNodeXY( -0.750, 7.500)
n277= modelSpace.newNodeXY( 1.250, 6.000)
n278= modelSpace.newNodeXY( 0.750, 6.500)
n279= modelSpace.newNodeXY( -2.750, 8.500)
n280= modelSpace.newNodeXY( 3.250, 2.500)
n281= modelSpace.newNodeXY( 0.250, 7.000)
n282= modelSpace.newNodeXY( 1.750, 5.500)
n283= modelSpace.newNodeXY( -1.250, 8.000)
n284= modelSpace.newNodeXY( 2.750, 4.000)
n286= modelSpace.newNodeXY( 3.750, 0.000)
n287= modelSpace.newNodeXY( -5.250, 9.000)
n288= modelSpace.newNodeXY( -4.750, 9.000)
n289= modelSpace.newNodeXY( -2.250, 8.500)
n290= modelSpace.newNodeXY( 2.250, 5.000)
n291= modelSpace.newNodeXY( -0.250, 7.500)
n292= modelSpace.newNodeXY( 3.250, 3.000)
n293= modelSpace.newNodeXY( 3.750, 0.500)
n294= modelSpace.newNodeXY( -4.250, 9.000)
n295= modelSpace.newNodeXY( 3.750, 1.000)
n296= modelSpace.newNodeXY( -3.750, 9.000)
n297= modelSpace.newNodeXY( 3.750, 1.500)
n298= modelSpace.newNodeXY( -0.750, 8.000)
n299= modelSpace.newNodeXY( 2.750, 4.500)
n300= modelSpace.newNodeXY( -1.750, 8.500)
n301= modelSpace.newNodeXY( 3.250, 3.500)
n302= modelSpace.newNodeXY( 1.250, 6.500)
n303= modelSpace.newNodeXY( 3.750, 2.000)
n304= modelSpace.newNodeXY( 0.750, 7.000)
n305= modelSpace.newNodeXY( -3.250, 9.000)
n306= modelSpace.newNodeXY( 1.750, 6.000)
n307= modelSpace.newNodeXY( 2.250, 5.500)
n308= modelSpace.newNodeXY( 0.250, 7.500)
n309= modelSpace.newNodeXY( 3.750, 2.500)
n310= modelSpace.newNodeXY( -2.750, 9.000)
n312= modelSpace.newNodeXY( 3.250, 4.000)
n313= modelSpace.newNodeXY( -1.250, 8.500)
n314= modelSpace.newNodeXY( 2.750, 5.000)
n315= modelSpace.newNodeXY( -0.250, 8.000)
n316= modelSpace.newNodeXY( 3.750, 3.000)
n317= modelSpace.newNodeXY( -2.250, 9.000)
n318= modelSpace.newNodeXY( -5.250, 9.500)
n319= modelSpace.newNodeXY( 4.250, 0.000)
n320= modelSpace.newNodeXY( -4.750, 9.500)
n321= modelSpace.newNodeXY( 4.250, 0.500)
n322= modelSpace.newNodeXY( 1.250, 7.000)
n323= modelSpace.newNodeXY( -4.250, 9.500)
n324= modelSpace.newNodeXY( 4.250, 1.000)
n325= modelSpace.newNodeXY( 1.750, 6.500)
n326= modelSpace.newNodeXY( 0.750, 7.500)
n327= modelSpace.newNodeXY( 2.250, 6.000)
n328= modelSpace.newNodeXY( -0.750, 8.500)
n329= modelSpace.newNodeXY( 3.250, 4.500)
n330= modelSpace.newNodeXY( 4.250, 1.500)
n331= modelSpace.newNodeXY( -3.750, 9.500)
n332= modelSpace.newNodeXY( -1.750, 9.000)
n333= modelSpace.newNodeXY( 3.750, 3.500)
n334= modelSpace.newNodeXY( 4.250, 2.000)
n335= modelSpace.newNodeXY( 2.750, 5.500)
n336= modelSpace.newNodeXY( 0.250, 8.000)
n337= modelSpace.newNodeXY( -3.250, 9.500)
n339= modelSpace.newNodeXY( 4.250, 2.500)
n340= modelSpace.newNodeXY( -2.750, 9.500)
n341= modelSpace.newNodeXY( 3.750, 4.000)
n342= modelSpace.newNodeXY( -1.250, 9.000)
n343= modelSpace.newNodeXY( 3.250, 5.000)
n344= modelSpace.newNodeXY( -0.250, 8.500)
n345= modelSpace.newNodeXY( 1.750, 7.000)
n346= modelSpace.newNodeXY( 2.250, 6.500)
n347= modelSpace.newNodeXY( 1.250, 7.500)
n348= modelSpace.newNodeXY( 4.250, 3.000)
n349= modelSpace.newNodeXY( -2.250, 9.500)
n350= modelSpace.newNodeXY( 2.750, 6.000)
n351= modelSpace.newNodeXY( -5.250, 10.000)
n352= modelSpace.newNodeXY( 4.750, 0.000)
n353= modelSpace.newNodeXY( 0.750, 8.000)
n354= modelSpace.newNodeXY( -4.750, 10.000)
n355= modelSpace.newNodeXY( 4.750, 0.500)
n356= modelSpace.newNodeXY( 4.750, 1.000)
n357= modelSpace.newNodeXY( -4.250, 10.000)
n358= modelSpace.newNodeXY( 3.750, 4.500)
n359= modelSpace.newNodeXY( -0.750, 9.000)
n360= modelSpace.newNodeXY( -3.750, 10.000)
n361= modelSpace.newNodeXY( 4.750, 1.500)
n362= modelSpace.newNodeXY( 4.250, 3.500)
n363= modelSpace.newNodeXY( 0.250, 8.500)
n364= modelSpace.newNodeXY( 3.250, 5.500)
n365= modelSpace.newNodeXY( -1.750, 9.500)
n366= modelSpace.newNodeXY( -3.250, 10.000)
n367= modelSpace.newNodeXY( 4.750, 2.000)
n369= modelSpace.newNodeXY( 1.750, 7.500)
n370= modelSpace.newNodeXY( 2.250, 7.000)
n371= modelSpace.newNodeXY( 3.750, 5.000)
n372= modelSpace.newNodeXY( -0.250, 9.000)
n373= modelSpace.newNodeXY( 4.750, 2.500)
n374= modelSpace.newNodeXY( 2.750, 6.500)
n375= modelSpace.newNodeXY( -1.250, 9.500)
n376= modelSpace.newNodeXY( -2.750, 10.000)
n377= modelSpace.newNodeXY( 4.250, 4.000)
n378= modelSpace.newNodeXY( 1.250, 8.000)
n379= modelSpace.newNodeXY( 3.250, 6.000)
n380= modelSpace.newNodeXY( 0.750, 8.500)
n381= modelSpace.newNodeXY( 4.750, 3.000)
n382= modelSpace.newNodeXY( -2.250, 10.000)
n383= modelSpace.newNodeXY( 5.250, 0.000)
n384= modelSpace.newNodeXY( 4.250, 4.500)
n385= modelSpace.newNodeXY( 5.250, 0.500)
n386= modelSpace.newNodeXY( -0.750, 9.500)
n387= modelSpace.newNodeXY( 0.250, 9.000)
n388= modelSpace.newNodeXY( 5.250, 1.000)
n389= modelSpace.newNodeXY( 3.750, 5.500)
n390= modelSpace.newNodeXY( 4.750, 3.500)
n391= modelSpace.newNodeXY( -1.750, 10.000)
n392= modelSpace.newNodeXY( 2.250, 7.500)
n393= modelSpace.newNodeXY( 5.250, 1.500)
n394= modelSpace.newNodeXY( 2.750, 7.000)
n395= modelSpace.newNodeXY( 1.750, 8.000)
n397= modelSpace.newNodeXY( 5.250, 2.000)
n398= modelSpace.newNodeXY( 1.250, 8.500)
n399= modelSpace.newNodeXY( 3.250, 6.500)
n400= modelSpace.newNodeXY( -0.250, 9.500)
n401= modelSpace.newNodeXY( 4.250, 5.000)
n402= modelSpace.newNodeXY( -1.250, 10.000)
n403= modelSpace.newNodeXY( 4.750, 4.000)
n404= modelSpace.newNodeXY( 5.250, 2.500)
n405= modelSpace.newNodeXY( 0.750, 9.000)
n406= modelSpace.newNodeXY( 3.750, 6.000)
n407= modelSpace.newNodeXY( 5.250, 3.000)
n408= modelSpace.newNodeXY( 2.750, 7.500)
n409= modelSpace.newNodeXY( 4.750, 4.500)
n410= modelSpace.newNodeXY( -0.750, 10.000)
n411= modelSpace.newNodeXY( 2.250, 8.000)
n412= modelSpace.newNodeXY( 0.250, 9.500)
n413= modelSpace.newNodeXY( 4.250, 5.500)
n414= modelSpace.newNodeXY( 1.750, 8.500)
n415= modelSpace.newNodeXY( 3.250, 7.000)
n416= modelSpace.newNodeXY( 5.250, 3.500)
n418= modelSpace.newNodeXY( 1.250, 9.000)
n419= modelSpace.newNodeXY( 3.750, 6.500)
n420= modelSpace.newNodeXY( 4.750, 5.000)
n421= modelSpace.newNodeXY( -0.250, 10.000)
n422= modelSpace.newNodeXY( 4.250, 6.000)
n423= modelSpace.newNodeXY( 5.250, 4.000)
n424= modelSpace.newNodeXY( 0.750, 9.500)
n425= modelSpace.newNodeXY( 2.750, 8.000)
n426= modelSpace.newNodeXY( 3.250, 7.500)
n427= modelSpace.newNodeXY( 2.250, 8.500)
n428= modelSpace.newNodeXY( 3.750, 7.000)
n429= modelSpace.newNodeXY( 1.750, 9.000)
n430= modelSpace.newNodeXY( 0.250, 10.000)
n431= modelSpace.newNodeXY( 4.750, 5.500)
n432= modelSpace.newNodeXY( 5.250, 4.500)
n433= modelSpace.newNodeXY( 1.250, 9.500)
n434= modelSpace.newNodeXY( 4.250, 6.500)
n436= modelSpace.newNodeXY( 5.250, 5.000)
n437= modelSpace.newNodeXY( 0.750, 10.000)
n438= modelSpace.newNodeXY( 4.750, 6.000)
n439= modelSpace.newNodeXY( 2.750, 8.500)
n440= modelSpace.newNodeXY( 3.250, 8.000)
n441= modelSpace.newNodeXY( 3.750, 7.500)
n442= modelSpace.newNodeXY( 2.250, 9.000)
n443= modelSpace.newNodeXY( 4.250, 7.000)
n444= modelSpace.newNodeXY( 1.750, 9.500)
n445= modelSpace.newNodeXY( 5.250, 5.500)
n446= modelSpace.newNodeXY( 1.250, 10.000)
n447= modelSpace.newNodeXY( 4.750, 6.500)
n448= modelSpace.newNodeXY( 3.250, 8.500)
n449= modelSpace.newNodeXY( 3.750, 8.000)
n450= modelSpace.newNodeXY( 2.750, 9.000)
n451= modelSpace.newNodeXY( 5.250, 6.000)
n452= modelSpace.newNodeXY( 4.250, 7.500)
n453= modelSpace.newNodeXY( 2.250, 9.500)
n454= modelSpace.newNodeXY( 4.750, 7.000)
n455= modelSpace.newNodeXY( 1.750, 10.000)
n456= modelSpace.newNodeXY( 5.250, 6.500)
n457= modelSpace.newNodeXY( 3.750, 8.500)
n458= modelSpace.newNodeXY( 3.250, 9.000)
n459= modelSpace.newNodeXY( 4.250, 8.000)
n460= modelSpace.newNodeXY( 2.750, 9.500)
n461= modelSpace.newNodeXY( 2.250, 10.000)
n462= modelSpace.newNodeXY( 4.750, 7.500)
n463= modelSpace.newNodeXY( 5.250, 7.000)
n464= modelSpace.newNodeXY( 3.750, 9.000)
n465= modelSpace.newNodeXY( 4.250, 8.500)
n466= modelSpace.newNodeXY( 3.250, 9.500)
n467= modelSpace.newNodeXY( 4.750, 8.000)
n468= modelSpace.newNodeXY( 2.750, 10.000)
n469= modelSpace.newNodeXY( 5.250, 7.500)
n470= modelSpace.newNodeXY( 4.250, 9.000)
n471= modelSpace.newNodeXY( 3.750, 9.500)
n472= modelSpace.newNodeXY( 4.750, 8.500)
n473= modelSpace.newNodeXY( 3.250, 10.000)
n474= modelSpace.newNodeXY( 5.250, 8.000)
n475= modelSpace.newNodeXY( 4.250, 9.500)
n476= modelSpace.newNodeXY( 3.750, 10.000)
n477= modelSpace.newNodeXY( 4.750, 9.000)
n478= modelSpace.newNodeXY( 5.250, 8.500)
n479= modelSpace.newNodeXY( 4.750, 9.500)
n480= modelSpace.newNodeXY( 4.250, 10.000)
n481= modelSpace.newNodeXY( 5.250, 9.000)
n482= modelSpace.newNodeXY( 4.750, 10.000)
n483= modelSpace.newNodeXY( 5.250, 9.500)
n484= modelSpace.newNodeXY( 5.250, 10.000)

lmsg.setLevel(lmsg.INFO)
lmsg.log("Finished creating all soil nodes...")

# define fixities for soil nodes
constraintHandler= modelSpace.constraints
opensees_style.fix(constraintHandler= constraintHandler, idNode= n1.tag, dofs=[1, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n2.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n3.tag, dofs=[0, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n5.tag, dofs=[0, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n6.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n10.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n11.tag, dofs=[0, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n16.tag, dofs=[0, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n17.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n23.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n24.tag, dofs=[0, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n34.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n35.tag, dofs=[0, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n44.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n45.tag, dofs=[0, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n57.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n58.tag, dofs=[0, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n72.tag, dofs=[0, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n73.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n87.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n88.tag, dofs=[0, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n109.tag, dofs=[0, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n110.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n129.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n130.tag, dofs=[0, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n152.tag, dofs=[0, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n154.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n177.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n178.tag, dofs=[0, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n204.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n205.tag, dofs=[0, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n228.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n229.tag, dofs=[0, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n255.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n256.tag, dofs=[0, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n286.tag, dofs=[0, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n287.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n318.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n319.tag, dofs=[0, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n351.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n352.tag, dofs=[0, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n383.tag, dofs=[1, 1])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n385.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n388.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n393.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n397.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n404.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n407.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n416.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n423.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n432.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n436.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n445.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n451.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n456.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n463.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n469.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n474.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n478.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n481.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n483.tag, dofs=[1, 0])
opensees_style.fix(constraintHandler= constraintHandler, idNode= n484.tag, dofs=[1, 0])

lmsg.log("Finished creating all boundary conditions...")

#-----------------------------------------------------------------------------
#  2. DESIGNATE LIST OF PERMANENT NODES (NEVER REMOVED) FOR RECORDERS
#-----------------------------------------------------------------------------
mNodeInfo= list()
mNodeInfo.append(n1)
mNodeInfo.append(n2)
mNodeInfo.append(n3)
mNodeInfo.append(n4)
mNodeInfo.append(n5)
mNodeInfo.append(n6)
mNodeInfo.append(n7)
mNodeInfo.append(n8)
mNodeInfo.append(n9)
mNodeInfo.append(n10)
mNodeInfo.append(n11)
mNodeInfo.append(n12)
mNodeInfo.append(n13)
mNodeInfo.append(n14)
mNodeInfo.append(n15)
mNodeInfo.append(n16)
mNodeInfo.append(n17)
mNodeInfo.append(n18)
mNodeInfo.append(n19)
mNodeInfo.append(n20)
mNodeInfo.append(n21)
mNodeInfo.append(n22)
mNodeInfo.append(n23)
mNodeInfo.append(n24)
mNodeInfo.append(n25)
mNodeInfo.append(n26)
mNodeInfo.append(n27)
mNodeInfo.append(n28)
mNodeInfo.append(n29)
mNodeInfo.append(n30)
mNodeInfo.append(n31)
mNodeInfo.append(n32)
mNodeInfo.append(n33)
mNodeInfo.append(n34)
mNodeInfo.append(n35)
mNodeInfo.append(n36)
mNodeInfo.append(n37)
mNodeInfo.append(n38)
mNodeInfo.append(n39)
mNodeInfo.append(n40)
mNodeInfo.append(n41)
mNodeInfo.append(n42)
mNodeInfo.append(n43)
mNodeInfo.append(n44)
mNodeInfo.append(n45)
mNodeInfo.append(n46)
mNodeInfo.append(n47)
mNodeInfo.append(n48)
mNodeInfo.append(n49)
mNodeInfo.append(n50)
mNodeInfo.append(n51)
mNodeInfo.append(n52)
mNodeInfo.append(n53)
mNodeInfo.append(n54)
mNodeInfo.append(n55)
mNodeInfo.append(n56)
mNodeInfo.append(n57)
mNodeInfo.append(n58)
mNodeInfo.append(n59)
mNodeInfo.append(n60)
mNodeInfo.append(n61)
mNodeInfo.append(n62)
mNodeInfo.append(n63)
mNodeInfo.append(n64)
mNodeInfo.append(n65)
mNodeInfo.append(n66)
mNodeInfo.append(n67)
mNodeInfo.append(n68)
mNodeInfo.append(n69)
mNodeInfo.append(n70)
mNodeInfo.append(n71)
mNodeInfo.append(n72)
mNodeInfo.append(n73)
mNodeInfo.append(n74)
mNodeInfo.append(n75)
mNodeInfo.append(n76)
mNodeInfo.append(n77)
mNodeInfo.append(n78)
mNodeInfo.append(n79)
mNodeInfo.append(n80)
mNodeInfo.append(n81)
mNodeInfo.append(n82)
mNodeInfo.append(n83)
mNodeInfo.append(n84)
mNodeInfo.append(n85)
mNodeInfo.append(n86)
mNodeInfo.append(n87)
mNodeInfo.append(n88)
mNodeInfo.append(n89)
mNodeInfo.append(n90)
mNodeInfo.append(n91)
mNodeInfo.append(n92)
mNodeInfo.append(n93)
mNodeInfo.append(n94)
mNodeInfo.append(n95)
mNodeInfo.append(n96)
mNodeInfo.append(n97)
mNodeInfo.append(n98)

# mNodeInfo.append(n99)
# mNodeInfo.append(n100)
# mNodeInfo.append(n101)
mNodeInfo.append(n102)
mNodeInfo.append(n103)
mNodeInfo.append(n104)
mNodeInfo.append(n105)

# mNodeInfo.append(n106)
mNodeInfo.append(n107)
mNodeInfo.append(n108)
mNodeInfo.append(n109)
mNodeInfo.append(n110)
mNodeInfo.append(n111)
mNodeInfo.append(n112)
# mNodeInfo.append(n113)
mNodeInfo.append(n114)
mNodeInfo.append(n115)
mNodeInfo.append(n116)
mNodeInfo.append(n117)
mNodeInfo.append(n118)
mNodeInfo.append(n119)
mNodeInfo.append(n120)
mNodeInfo.append(n121)
mNodeInfo.append(n122)
# mNodeInfo.append(n123)
mNodeInfo.append(n124)
mNodeInfo.append(n125)
mNodeInfo.append(n126)
mNodeInfo.append(n127)
# mNodeInfo.append(n128)
mNodeInfo.append(n129)
mNodeInfo.append(n130)
mNodeInfo.append(n131)
mNodeInfo.append(n132)
mNodeInfo.append(n133)
mNodeInfo.append(n134)
mNodeInfo.append(n135)
mNodeInfo.append(n136)
mNodeInfo.append(n137)
mNodeInfo.append(n138)
mNodeInfo.append(n139)
mNodeInfo.append(n140)

# mNodeInfo.append(n141)
mNodeInfo.append(n142)
mNodeInfo.append(n143)
mNodeInfo.append(n144)
mNodeInfo.append(n145)
mNodeInfo.append(n146)
mNodeInfo.append(n147)
mNodeInfo.append(n148)
mNodeInfo.append(n149)
mNodeInfo.append(n150)

# mNodeInfo.append(n151)
mNodeInfo.append(n152)
mNodeInfo.append(n153)
mNodeInfo.append(n154)
mNodeInfo.append(n155)
mNodeInfo.append(n156)
mNodeInfo.append(n157)
mNodeInfo.append(n158)
mNodeInfo.append(n159)
mNodeInfo.append(n160)
mNodeInfo.append(n161)
mNodeInfo.append(n162)
mNodeInfo.append(n163)
mNodeInfo.append(n164)
mNodeInfo.append(n165)
mNodeInfo.append(n166)
mNodeInfo.append(n167)

# mNodeInfo.append(n168)
mNodeInfo.append(n169)
mNodeInfo.append(n170)
mNodeInfo.append(n171)
mNodeInfo.append(n172)
mNodeInfo.append(n173)
mNodeInfo.append(n174)
mNodeInfo.append(n175)
mNodeInfo.append(n176)
mNodeInfo.append(n177)
mNodeInfo.append(n178)
mNodeInfo.append(n179)
mNodeInfo.append(n180)
mNodeInfo.append(n181)
mNodeInfo.append(n182)
mNodeInfo.append(n183)

# mNodeInfo.append(n184)
mNodeInfo.append(n185)
mNodeInfo.append(n186)
mNodeInfo.append(n187)
mNodeInfo.append(n188)
mNodeInfo.append(n189)
mNodeInfo.append(n190)
mNodeInfo.append(n191)
mNodeInfo.append(n192)
mNodeInfo.append(n193)
mNodeInfo.append(n194)
mNodeInfo.append(n195)
mNodeInfo.append(n196)

# mNodeInfo.append(n197)
mNodeInfo.append(n198)
mNodeInfo.append(n199)
mNodeInfo.append(n200)
mNodeInfo.append(n201)
mNodeInfo.append(n202)
mNodeInfo.append(n203)
mNodeInfo.append(n204)
mNodeInfo.append(n205)
mNodeInfo.append(n206)
mNodeInfo.append(n207)
mNodeInfo.append(n208)
mNodeInfo.append(n209)
mNodeInfo.append(n210)
mNodeInfo.append(n211)
mNodeInfo.append(n212)
mNodeInfo.append(n213)
mNodeInfo.append(n214)
mNodeInfo.append(n215)
mNodeInfo.append(n216)
mNodeInfo.append(n217)

# mNodeInfo.append(n219)
mNodeInfo.append(n220)
mNodeInfo.append(n221)
mNodeInfo.append(n222)
mNodeInfo.append(n223)
mNodeInfo.append(n224)
mNodeInfo.append(n225)
mNodeInfo.append(n226)
mNodeInfo.append(n227)
mNodeInfo.append(n228)
mNodeInfo.append(n229)
mNodeInfo.append(n230)
mNodeInfo.append(n231)
mNodeInfo.append(n232)
mNodeInfo.append(n233)
mNodeInfo.append(n234)
mNodeInfo.append(n235)
mNodeInfo.append(n236)
mNodeInfo.append(n237)
mNodeInfo.append(n238)
mNodeInfo.append(n240)

# mNodeInfo.append(n242)
mNodeInfo.append(n243)
mNodeInfo.append(n244)
mNodeInfo.append(n245)
mNodeInfo.append(n246)
mNodeInfo.append(n247)
mNodeInfo.append(n248)
mNodeInfo.append(n249)
mNodeInfo.append(n250)
mNodeInfo.append(n251)
mNodeInfo.append(n252)
mNodeInfo.append(n254)
mNodeInfo.append(n255)
mNodeInfo.append(n256)
mNodeInfo.append(n257)
mNodeInfo.append(n258)
mNodeInfo.append(n261)
mNodeInfo.append(n262)
mNodeInfo.append(n263)
mNodeInfo.append(n265)

# mNodeInfo.append(n264)
mNodeInfo.append(n266)
mNodeInfo.append(n267)
mNodeInfo.append(n268)
mNodeInfo.append(n269)
mNodeInfo.append(n270)
mNodeInfo.append(n271)
mNodeInfo.append(n272)
mNodeInfo.append(n273)
mNodeInfo.append(n274)
mNodeInfo.append(n275)
mNodeInfo.append(n276)
mNodeInfo.append(n279)
mNodeInfo.append(n280)
mNodeInfo.append(n283)
mNodeInfo.append(n284)

# mNodeInfo.append(n285)
mNodeInfo.append(n286)
mNodeInfo.append(n287)
mNodeInfo.append(n288)
mNodeInfo.append(n289)
mNodeInfo.append(n290)
mNodeInfo.append(n291)
mNodeInfo.append(n292)
mNodeInfo.append(n293)
mNodeInfo.append(n294)
mNodeInfo.append(n295)
mNodeInfo.append(n296)
mNodeInfo.append(n297)
mNodeInfo.append(n298)
mNodeInfo.append(n299)
mNodeInfo.append(n300)
mNodeInfo.append(n301)
mNodeInfo.append(n303)
mNodeInfo.append(n305)
mNodeInfo.append(n309)
mNodeInfo.append(n310)

# mNodeInfo.append(n311)
mNodeInfo.append(n312)
mNodeInfo.append(n313)
mNodeInfo.append(n314)
mNodeInfo.append(n315)
mNodeInfo.append(n316)
mNodeInfo.append(n317)
mNodeInfo.append(n318)
mNodeInfo.append(n319)
mNodeInfo.append(n320)
mNodeInfo.append(n321)
mNodeInfo.append(n323)
mNodeInfo.append(n324)
mNodeInfo.append(n328)
mNodeInfo.append(n329)
mNodeInfo.append(n330)
mNodeInfo.append(n331)
mNodeInfo.append(n332)
mNodeInfo.append(n333)
mNodeInfo.append(n334)
mNodeInfo.append(n337)

# mNodeInfo.append(n338)
mNodeInfo.append(n339)
mNodeInfo.append(n340)
mNodeInfo.append(n341)
mNodeInfo.append(n342)
mNodeInfo.append(n343)
mNodeInfo.append(n344)
mNodeInfo.append(n348)
mNodeInfo.append(n349)
mNodeInfo.append(n351)
mNodeInfo.append(n352)
mNodeInfo.append(n354)
mNodeInfo.append(n355)
mNodeInfo.append(n356)
mNodeInfo.append(n357)
mNodeInfo.append(n358)
mNodeInfo.append(n359)
mNodeInfo.append(n360)
mNodeInfo.append(n361)
mNodeInfo.append(n362)
mNodeInfo.append(n365)
mNodeInfo.append(n366)
mNodeInfo.append(n367)

# mNodeInfo.append(n368)
mNodeInfo.append(n371)
mNodeInfo.append(n372)
mNodeInfo.append(n373)
mNodeInfo.append(n375)
mNodeInfo.append(n376)
mNodeInfo.append(n377)
mNodeInfo.append(n381)
mNodeInfo.append(n382)
mNodeInfo.append(n383)
mNodeInfo.append(n384)
mNodeInfo.append(n385)
mNodeInfo.append(n386)
mNodeInfo.append(n388)
mNodeInfo.append(n390)
mNodeInfo.append(n391)
mNodeInfo.append(n393)

# mNodeInfo.append(n396)
mNodeInfo.append(n397)
mNodeInfo.append(n400)
mNodeInfo.append(n401)
mNodeInfo.append(n402)
mNodeInfo.append(n403)
mNodeInfo.append(n404)
mNodeInfo.append(n407)
mNodeInfo.append(n409)
mNodeInfo.append(n410)
mNodeInfo.append(n416)

# mNodeInfo.append(n417)
mNodeInfo.append(n420)
mNodeInfo.append(n421)
mNodeInfo.append(n423)
mNodeInfo.append(n432)

#mNodeInfo.append(n435)
mNodeInfo.append(n436)

#-----------------------------------------------------------------------------
#  3. CREATE LAGRANGE MULTIPLIER NODES FOR BEAM CONTACT ELEMENTS
#-----------------------------------------------------------------------------
lagrangeNodes= dict()
for k in range(1, 42+1):
    lagrangeNodes[1000+k]= modelSpace.newNodeXY(0.00, 0.00)
 
lmsg.log("Finished creating all nodes...")

#-----------------------------------------------------------------------------
#  4. CREATE SOIL MATERIALS
#-----------------------------------------------------------------------------
#

# define pressure depended material for soil
#nDMaterial PressureDependMultiYield02 5 2 1.8 9.6e3 2.7e4 36 0.1 \
#101.0 0.0 26 0.067 0.23 0.06 \
#0.27 20 5.0 3.0 1.0 \
#0.0 0.77 0.9 0.02 0.7 101.0
#set thick1 1.0
soilMat= typical_materials.defPressureDependentMultiYield02Material(preprocessor= preprocessor, name= 'soilMat', nd= 2, rho= 1.8,  refShearModul= 9.6e3, refBulkModul= 2.7e4, frictionAng= math.radians(36),  peakShearStra= 0.1, refPress= -101.0, pressDependCoe= 0.0, phaseTransformAngle= math.radians(26), contractionParam1= 0.067, contractionParam3= 0.23, dilationParam1= 0.06, dilationParam3= 0.27, numberOfYieldSurf= 20, contractionParam2= 5.0, dilationParam2= 3.0, liquefactionParam1= 1.0, liquefactionParam2= 0.0, e= 0.77, volLimit1= 0.9, volLimit2= 0.02, volLimit3= 0.7, atm= 101.0)
# element thickness
thick1= 1.0
# body force in x-direction
#set xWgt1  0.00
xWgt1 = 0.00
# body force in y-direction
#set yWgt1  [expr -9.81*1.8]
yWgt1 = -9.81*1.8

# create wrapper material for initial state analysis
matWrapper= typical_materials.defInitialStateAnalysisWrapper(preprocessor= preprocessor, name= 'matWrapper', ndim= 2, encapsulatedMaterial= soilMat)

lmsg.log("Finished creating all soil materials...")
#-----------------------------------------------------------------------------
#  5. CREATE SOIL ELEMENTS
#-----------------------------------------------------------------------------
#

modelSpace.setDefaultMaterial(matWrapper)
#element quad 1 109 130 131 112  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad1= modelSpace.newElement('FourNodeQuad', [n109.tag, n130.tag, n131.tag, n112.tag])
quad1.thickness= thick1
#element quad 2 130 152 157 131  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad2= modelSpace.newElement('FourNodeQuad', [n130.tag, n152.tag, n157.tag, n131.tag])
quad2.thickness= thick1
#element quad 3 152 178 180 157  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad3= modelSpace.newElement('FourNodeQuad', [n152.tag, n178.tag, n180.tag, n157.tag])
quad3.thickness= thick1
#element quad 4 178 205 207 180  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad4= modelSpace.newElement('FourNodeQuad', [n178.tag, n205.tag, n207.tag, n180.tag])
quad4.thickness= thick1
#element quad 5 205 229 231 207  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad5= modelSpace.newElement('FourNodeQuad', [n205.tag, n229.tag, n231.tag, n207.tag])
quad5.thickness= thick1
#element quad 6 229 256 261 231  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad6= modelSpace.newElement('FourNodeQuad', [n229.tag, n256.tag, n261.tag, n231.tag])
quad6.thickness= thick1
#element quad 7 256 286 293 261  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad7= modelSpace.newElement('FourNodeQuad', [n256.tag, n286.tag, n293.tag, n261.tag])
quad7.thickness= thick1
#element quad 8 286 319 321 293  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad8= modelSpace.newElement('FourNodeQuad', [n286.tag, n319.tag, n321.tag, n293.tag])
quad8.thickness= thick1
#element quad 9 319 352 355 321  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad9= modelSpace.newElement('FourNodeQuad', [n319.tag, n352.tag, n355.tag, n321.tag])
quad9.thickness= thick1
#element quad 10 352 383 385 355  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad10= modelSpace.newElement('FourNodeQuad', [n352.tag, n383.tag, n385.tag, n355.tag])
quad10.thickness= thick1
#element quad 11 112 131 138 116  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad11= modelSpace.newElement('FourNodeQuad', [n112.tag, n131.tag, n138.tag, n116.tag])
quad11.thickness= thick1
#element quad 12 131 157 161 138  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad12= modelSpace.newElement('FourNodeQuad', [n131.tag, n157.tag, n161.tag, n138.tag])
quad12.thickness= thick1
#element quad 13 157 180 181 161  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad13= modelSpace.newElement('FourNodeQuad', [n157.tag, n180.tag, n181.tag, n161.tag])
quad13.thickness= thick1
#element quad 14 180 207 209 181  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad14= modelSpace.newElement('FourNodeQuad', [n180.tag, n207.tag, n209.tag, n181.tag])
quad14.thickness= thick1
#element quad 15 207 231 233 209  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad15= modelSpace.newElement('FourNodeQuad', [n207.tag, n231.tag, n233.tag, n209.tag])
quad15.thickness= thick1
#element quad 16 231 261 266 233  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad16= modelSpace.newElement('FourNodeQuad', [n231.tag, n261.tag, n266.tag, n233.tag])
quad16.thickness= thick1
#element quad 17 261 293 295 266  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad17= modelSpace.newElement('FourNodeQuad', [n261.tag, n293.tag, n295.tag, n266.tag])
quad17.thickness= thick1
#element quad 18 293 321 324 295  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad18= modelSpace.newElement('FourNodeQuad', [n293.tag, n321.tag, n324.tag, n295.tag])
quad18.thickness= thick1
#element quad 19 321 355 356 324  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad19= modelSpace.newElement('FourNodeQuad', [n321.tag, n355.tag, n356.tag, n324.tag])
quad19.thickness= thick1
#element quad 20 355 385 388 356  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad20= modelSpace.newElement('FourNodeQuad', [n355.tag, n385.tag, n388.tag, n356.tag])
quad20.thickness= thick1
#element quad 21 116 138 143 119  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad21= modelSpace.newElement('FourNodeQuad', [n116.tag, n138.tag, n143.tag, n119.tag])
quad21.thickness= thick1
#element quad 22 138 161 162 143  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad22= modelSpace.newElement('FourNodeQuad', [n138.tag, n161.tag, n162.tag, n143.tag])
quad22.thickness= thick1
#element quad 23 161 181 187 162  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad23= modelSpace.newElement('FourNodeQuad', [n161.tag, n181.tag, n187.tag, n162.tag])
quad23.thickness= thick1
#element quad 24 181 209 214 187  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad24= modelSpace.newElement('FourNodeQuad', [n181.tag, n209.tag, n214.tag, n187.tag])
quad24.thickness= thick1
#element quad 25 209 233 240 214  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad25= modelSpace.newElement('FourNodeQuad', [n209.tag, n233.tag, n240.tag, n214.tag])
quad25.thickness= thick1
#element quad 26 233 266 270 240  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad26= modelSpace.newElement('FourNodeQuad', [n233.tag, n266.tag, n270.tag, n240.tag])
quad26.thickness= thick1
#element quad 27 266 295 297 270  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad27= modelSpace.newElement('FourNodeQuad', [n266.tag, n295.tag, n297.tag, n270.tag])
quad27.thickness= thick1
#element quad 28 295 324 330 297  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad28= modelSpace.newElement('FourNodeQuad', [n295.tag, n324.tag, n330.tag, n297.tag])
quad28.thickness= thick1
#element quad 29 324 356 361 330  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad29= modelSpace.newElement('FourNodeQuad', [n324.tag, n356.tag, n361.tag, n330.tag])
quad29.thickness= thick1
#element quad 30 356 388 393 361  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad30= modelSpace.newElement('FourNodeQuad', [n356.tag, n388.tag, n393.tag, n361.tag])
quad30.thickness= thick1
#element quad 31 119 143 146 126  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad31= modelSpace.newElement('FourNodeQuad', [n119.tag, n143.tag, n146.tag, n126.tag])
quad31.thickness= thick1
#element quad 32 143 162 170 146  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad32= modelSpace.newElement('FourNodeQuad', [n143.tag, n162.tag, n170.tag, n146.tag])
quad32.thickness= thick1
#element quad 33 162 187 193 170  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad33= modelSpace.newElement('FourNodeQuad', [n162.tag, n187.tag, n193.tag, n170.tag])
quad33.thickness= thick1
#element quad 34 187 214 217 193  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad34= modelSpace.newElement('FourNodeQuad', [n187.tag, n214.tag, n217.tag, n193.tag])
quad34.thickness= thick1
#element quad 35 214 240 245 217  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad35= modelSpace.newElement('FourNodeQuad', [n214.tag, n240.tag, n245.tag, n217.tag])
quad35.thickness= thick1
#element quad 36 240 270 273 245  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad36= modelSpace.newElement('FourNodeQuad', [n240.tag, n270.tag, n273.tag, n245.tag])
quad36.thickness= thick1
#element quad 37 270 297 303 273  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad37= modelSpace.newElement('FourNodeQuad', [n270.tag, n297.tag, n303.tag, n273.tag])
quad37.thickness= thick1
#element quad 38 297 330 334 303  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad38= modelSpace.newElement('FourNodeQuad', [n297.tag, n330.tag, n334.tag, n303.tag])
quad38.thickness= thick1
#element quad 39 330 361 367 334  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad39= modelSpace.newElement('FourNodeQuad', [n330.tag, n361.tag, n367.tag, n334.tag])
quad39.thickness= thick1
#element quad 40 361 393 397 367  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad40= modelSpace.newElement('FourNodeQuad', [n361.tag, n393.tag, n397.tag, n367.tag])
quad40.thickness= thick1
#element quad 41 126 146 153 135  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad41= modelSpace.newElement('FourNodeQuad', [n126.tag, n146.tag, n153.tag, n135.tag])
quad41.thickness= thick1
#element quad 42 146 170 176 153  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad42= modelSpace.newElement('FourNodeQuad', [n146.tag, n170.tag, n176.tag, n153.tag])
quad42.thickness= thick1
#element quad 43 170 193 198 176  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad43= modelSpace.newElement('FourNodeQuad', [n170.tag, n193.tag, n198.tag, n176.tag])
quad43.thickness= thick1
#element quad 44 193 217 227 198  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad44= modelSpace.newElement('FourNodeQuad', [n193.tag, n217.tag, n227.tag, n198.tag])
quad44.thickness= thick1
#element quad 45 217 245 252 227  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad45= modelSpace.newElement('FourNodeQuad', [n217.tag, n245.tag, n252.tag, n227.tag])
quad45.thickness= thick1
#element quad 46 245 273 280 252  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad46= modelSpace.newElement('FourNodeQuad', [n245.tag, n273.tag, n280.tag, n252.tag])
quad46.thickness= thick1
#element quad 47 273 303 309 280  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad47= modelSpace.newElement('FourNodeQuad', [n273.tag, n303.tag, n309.tag, n280.tag])
quad47.thickness= thick1
#element quad 48 303 334 339 309  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad48= modelSpace.newElement('FourNodeQuad', [n303.tag, n334.tag, n339.tag, n309.tag])
quad48.thickness= thick1
#element quad 49 334 367 373 339  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad49= modelSpace.newElement('FourNodeQuad', [n334.tag, n367.tag, n373.tag, n339.tag])
quad49.thickness= thick1
#element quad 50 367 397 404 373  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad50= modelSpace.newElement('FourNodeQuad', [n367.tag, n397.tag, n404.tag, n373.tag])
quad50.thickness= thick1
#element quad 51 135 153 164 144  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad51= modelSpace.newElement('FourNodeQuad', [n135.tag, n153.tag, n164.tag, n144.tag])
quad51.thickness= thick1
#element quad 52 153 176 189 164  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad52= modelSpace.newElement('FourNodeQuad', [n153.tag, n176.tag, n189.tag, n164.tag])
quad52.thickness= thick1
#element quad 53 176 198 210 189  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad53= modelSpace.newElement('FourNodeQuad', [n176.tag, n198.tag, n210.tag, n189.tag])
quad53.thickness= thick1
#element quad 54 198 227 237 210  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad54= modelSpace.newElement('FourNodeQuad', [n198.tag, n227.tag, n237.tag, n210.tag])
quad54.thickness= thick1
#element quad 55 227 252 263 237  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad55= modelSpace.newElement('FourNodeQuad', [n227.tag, n252.tag, n263.tag, n237.tag])
quad55.thickness= thick1
#element quad 56 252 280 292 263  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad56= modelSpace.newElement('FourNodeQuad', [n252.tag, n280.tag, n292.tag, n263.tag])
quad56.thickness= thick1
#element quad 57 280 309 316 292  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad57= modelSpace.newElement('FourNodeQuad', [n280.tag, n309.tag, n316.tag, n292.tag])
quad57.thickness= thick1
#element quad 58 309 339 348 316  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad58= modelSpace.newElement('FourNodeQuad', [n309.tag, n339.tag, n348.tag, n316.tag])
quad58.thickness= thick1
#element quad 59 339 373 381 348  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad59= modelSpace.newElement('FourNodeQuad', [n339.tag, n373.tag, n381.tag, n348.tag])
quad59.thickness= thick1
#element quad 60 373 404 407 381  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad60= modelSpace.newElement('FourNodeQuad', [n373.tag, n404.tag, n407.tag, n381.tag])
quad60.thickness= thick1
#element quad 61 144 164 173 158  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad61= modelSpace.newElement('FourNodeQuad', [n144.tag, n164.tag, n173.tag, n158.tag])
quad61.thickness= thick1
#element quad 62 164 189 196 173  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad62= modelSpace.newElement('FourNodeQuad', [n164.tag, n189.tag, n196.tag, n173.tag])
quad62.thickness= thick1
#element quad 63 189 210 223 196  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad63= modelSpace.newElement('FourNodeQuad', [n189.tag, n210.tag, n223.tag, n196.tag])
quad63.thickness= thick1
#element quad 64 210 237 248 223  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad64= modelSpace.newElement('FourNodeQuad', [n210.tag, n237.tag, n248.tag, n223.tag])
quad64.thickness= thick1
#element quad 65 237 263 274 248  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad65= modelSpace.newElement('FourNodeQuad', [n237.tag, n263.tag, n274.tag, n248.tag])
quad65.thickness= thick1
#element quad 66 263 292 301 274  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad66= modelSpace.newElement('FourNodeQuad', [n263.tag, n292.tag, n301.tag, n274.tag])
quad66.thickness= thick1
#element quad 67 292 316 333 301  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad67= modelSpace.newElement('FourNodeQuad', [n292.tag, n316.tag, n333.tag, n301.tag])
quad67.thickness= thick1
#element quad 68 316 348 362 333  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad68= modelSpace.newElement('FourNodeQuad', [n316.tag, n348.tag, n362.tag, n333.tag])
quad68.thickness= thick1
#element quad 69 348 381 390 362  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad69= modelSpace.newElement('FourNodeQuad', [n348.tag, n381.tag, n390.tag, n362.tag])
quad69.thickness= thick1
#element quad 70 381 407 416 390  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad70= modelSpace.newElement('FourNodeQuad', [n381.tag, n407.tag, n416.tag, n390.tag])
quad70.thickness= thick1
#element quad 71 158 173 191 171  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad71= modelSpace.newElement('FourNodeQuad', [n158.tag, n173.tag, n191.tag, n171.tag])
quad71.thickness= thick1
#element quad 72 173 196 212 191  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad72= modelSpace.newElement('FourNodeQuad', [n173.tag, n196.tag, n212.tag, n191.tag])
quad72.thickness= thick1
#element quad 73 196 223 234 212  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad73= modelSpace.newElement('FourNodeQuad', [n196.tag, n223.tag, n234.tag, n212.tag])
quad73.thickness= thick1
#element quad 74 223 248 254 234  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad74= modelSpace.newElement('FourNodeQuad', [n223.tag, n248.tag, n254.tag, n234.tag])
quad74.thickness= thick1
#element quad 75 248 274 284 254  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad75= modelSpace.newElement('FourNodeQuad', [n248.tag, n274.tag, n284.tag, n254.tag])
quad75.thickness= thick1
#element quad 76 274 301 312 284  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad76= modelSpace.newElement('FourNodeQuad', [n274.tag, n301.tag, n312.tag, n284.tag])
quad76.thickness= thick1
#element quad 77 301 333 341 312  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad77= modelSpace.newElement('FourNodeQuad', [n301.tag, n333.tag, n341.tag, n312.tag])
quad77.thickness= thick1
#element quad 78 333 362 377 341  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad78= modelSpace.newElement('FourNodeQuad', [n333.tag, n362.tag, n377.tag, n341.tag])
quad78.thickness= thick1
#element quad 79 362 390 403 377  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad79= modelSpace.newElement('FourNodeQuad', [n362.tag, n390.tag, n403.tag, n377.tag])
quad79.thickness= thick1
#element quad 80 390 416 423 403  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad80= modelSpace.newElement('FourNodeQuad', [n390.tag, n416.tag, n423.tag, n403.tag])
quad80.thickness= thick1
#element quad 81 171 191 203 185  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad81= modelSpace.newElement('FourNodeQuad', [n171.tag, n191.tag, n203.tag, n185.tag])
quad81.thickness= thick1
#element quad 82 191 212 225 203  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad82= modelSpace.newElement('FourNodeQuad', [n191.tag, n212.tag, n225.tag, n203.tag])
quad82.thickness= thick1
#element quad 83 212 234 250 225  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad83= modelSpace.newElement('FourNodeQuad', [n212.tag, n234.tag, n250.tag, n225.tag])
quad83.thickness= thick1
#element quad 84 234 254 275 250  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad84= modelSpace.newElement('FourNodeQuad', [n234.tag, n254.tag, n275.tag, n250.tag])
quad84.thickness= thick1
#element quad 85 254 284 299 275  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad85= modelSpace.newElement('FourNodeQuad', [n254.tag, n284.tag, n299.tag, n275.tag])
quad85.thickness= thick1
#element quad 86 284 312 329 299  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad86= modelSpace.newElement('FourNodeQuad', [n284.tag, n312.tag, n329.tag, n299.tag])
quad86.thickness= thick1
#element quad 87 312 341 358 329  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad87= modelSpace.newElement('FourNodeQuad', [n312.tag, n341.tag, n358.tag, n329.tag])
quad87.thickness= thick1
#element quad 88 341 377 384 358  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad88= modelSpace.newElement('FourNodeQuad', [n341.tag, n377.tag, n384.tag, n358.tag])
quad88.thickness= thick1
#element quad 89 377 403 409 384  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad89= modelSpace.newElement('FourNodeQuad', [n377.tag, n403.tag, n409.tag, n384.tag])
quad89.thickness= thick1
#element quad 90 403 423 432 409  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad90= modelSpace.newElement('FourNodeQuad', [n403.tag, n423.tag, n432.tag, n409.tag])
quad90.thickness= thick1
#element quad 91 185 203 220 200  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad91= modelSpace.newElement('FourNodeQuad', [n185.tag, n203.tag, n220.tag, n200.tag])
quad91.thickness= thick1
#element quad 92 203 225 243 220  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad92= modelSpace.newElement('FourNodeQuad', [n203.tag, n225.tag, n243.tag, n220.tag])
quad92.thickness= thick1
#element quad 93 225 250 268 243  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad93= modelSpace.newElement('FourNodeQuad', [n225.tag, n250.tag, n268.tag, n243.tag])
quad93.thickness= thick1
#element quad 94 250 275 290 268  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad94= modelSpace.newElement('FourNodeQuad', [n250.tag, n275.tag, n290.tag, n268.tag])
quad94.thickness= thick1
#element quad 95 275 299 314 290  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad95= modelSpace.newElement('FourNodeQuad', [n275.tag, n299.tag, n314.tag, n290.tag])
quad95.thickness= thick1
#element quad 96 299 329 343 314  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad96= modelSpace.newElement('FourNodeQuad', [n299.tag, n329.tag, n343.tag, n314.tag])
quad96.thickness= thick1
#element quad 97 329 358 371 343  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad97= modelSpace.newElement('FourNodeQuad', [n329.tag, n358.tag, n371.tag, n343.tag])
quad97.thickness= thick1
#element quad 98 358 384 401 371  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad98= modelSpace.newElement('FourNodeQuad', [n358.tag, n384.tag, n401.tag, n371.tag])
quad98.thickness= thick1
#element quad 99 384 409 420 401  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad99= modelSpace.newElement('FourNodeQuad', [n384.tag, n409.tag, n420.tag, n401.tag])
quad99.thickness= thick1
#element quad 100 409 432 436 420  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad100= modelSpace.newElement('FourNodeQuad', [n409.tag, n432.tag, n436.tag, n420.tag])
quad100.thickness= thick1
#element quad 101 200 220 239 218  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad101= modelSpace.newElement('FourNodeQuad', [n200.tag, n220.tag, n239.tag, n218.tag])
quad101.thickness= thick1
#element quad 102 220 243 259 239  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad102= modelSpace.newElement('FourNodeQuad', [n220.tag, n243.tag, n259.tag, n239.tag])
quad102.thickness= thick1
#element quad 103 243 268 282 259  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad103= modelSpace.newElement('FourNodeQuad', [n243.tag, n268.tag, n282.tag, n259.tag])
quad103.thickness= thick1
#element quad 104 268 290 307 282  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad104= modelSpace.newElement('FourNodeQuad', [n268.tag, n290.tag, n307.tag, n282.tag])
quad104.thickness= thick1
#element quad 105 290 314 335 307  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad105= modelSpace.newElement('FourNodeQuad', [n290.tag, n314.tag, n335.tag, n307.tag])
quad105.thickness= thick1
#element quad 106 314 343 364 335  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad106= modelSpace.newElement('FourNodeQuad', [n314.tag, n343.tag, n364.tag, n335.tag])
quad106.thickness= thick1
#element quad 107 343 371 389 364  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad107= modelSpace.newElement('FourNodeQuad', [n343.tag, n371.tag, n389.tag, n364.tag])
quad107.thickness= thick1
#element quad 108 371 401 413 389  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad108= modelSpace.newElement('FourNodeQuad', [n371.tag, n401.tag, n413.tag, n389.tag])
quad108.thickness= thick1
#element quad 109 401 420 431 413  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad109= modelSpace.newElement('FourNodeQuad', [n401.tag, n420.tag, n431.tag, n413.tag])
quad109.thickness= thick1
#element quad 110 420 436 445 431  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad110= modelSpace.newElement('FourNodeQuad', [n420.tag, n436.tag, n445.tag, n431.tag])
quad110.thickness= thick1
#element quad 111 218 239 253 241  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad111= modelSpace.newElement('FourNodeQuad', [n218.tag, n239.tag, n253.tag, n241.tag])
quad111.thickness= thick1
#element quad 112 239 259 277 253  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad112= modelSpace.newElement('FourNodeQuad', [n239.tag, n259.tag, n277.tag, n253.tag])
quad112.thickness= thick1
#element quad 113 259 282 306 277  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad113= modelSpace.newElement('FourNodeQuad', [n259.tag, n282.tag, n306.tag, n277.tag])
quad113.thickness= thick1
#element quad 114 282 307 327 306  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad114= modelSpace.newElement('FourNodeQuad', [n282.tag, n307.tag, n327.tag, n306.tag])
quad114.thickness= thick1
#element quad 115 307 335 350 327  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad115= modelSpace.newElement('FourNodeQuad', [n307.tag, n335.tag, n350.tag, n327.tag])
quad115.thickness= thick1
#element quad 116 335 364 379 350  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad116= modelSpace.newElement('FourNodeQuad', [n335.tag, n364.tag, n379.tag, n350.tag])
quad116.thickness= thick1
#element quad 117 364 389 406 379  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad117= modelSpace.newElement('FourNodeQuad', [n364.tag, n389.tag, n406.tag, n379.tag])
quad117.thickness= thick1
#element quad 118 389 413 422 406  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad118= modelSpace.newElement('FourNodeQuad', [n389.tag, n413.tag, n422.tag, n406.tag])
quad118.thickness= thick1
#element quad 119 413 431 438 422  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad119= modelSpace.newElement('FourNodeQuad', [n413.tag, n431.tag, n438.tag, n422.tag])
quad119.thickness= thick1
#element quad 120 431 445 451 438  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad120= modelSpace.newElement('FourNodeQuad', [n431.tag, n445.tag, n451.tag, n438.tag])
quad120.thickness= thick1
#element quad 121 241 253 278 260  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad121= modelSpace.newElement('FourNodeQuad', [n241.tag, n253.tag, n278.tag, n260.tag])
quad121.thickness= thick1
#element quad 122 253 277 302 278  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad122= modelSpace.newElement('FourNodeQuad', [n253.tag, n277.tag, n302.tag, n278.tag])
quad122.thickness= thick1
#element quad 123 277 306 325 302  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad123= modelSpace.newElement('FourNodeQuad', [n277.tag, n306.tag, n325.tag, n302.tag])
quad123.thickness= thick1
#element quad 124 306 327 346 325  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad124= modelSpace.newElement('FourNodeQuad', [n306.tag, n327.tag, n346.tag, n325.tag])
quad124.thickness= thick1
#element quad 125 327 350 374 346  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad125= modelSpace.newElement('FourNodeQuad', [n327.tag, n350.tag, n374.tag, n346.tag])
quad125.thickness= thick1
#element quad 126 350 379 399 374  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad126= modelSpace.newElement('FourNodeQuad', [n350.tag, n379.tag, n399.tag, n374.tag])
quad126.thickness= thick1
#element quad 127 379 406 419 399  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad127= modelSpace.newElement('FourNodeQuad', [n379.tag, n406.tag, n419.tag, n399.tag])
quad127.thickness= thick1
#element quad 128 406 422 434 419  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad128= modelSpace.newElement('FourNodeQuad', [n406.tag, n422.tag, n434.tag, n419.tag])
quad128.thickness= thick1
#element quad 129 422 438 447 434  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad129= modelSpace.newElement('FourNodeQuad', [n422.tag, n438.tag, n447.tag, n434.tag])
quad129.thickness= thick1
#element quad 130 438 451 456 447  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad130= modelSpace.newElement('FourNodeQuad', [n438.tag, n451.tag, n456.tag, n447.tag])
quad130.thickness= thick1
#element quad 131 260 278 304 281  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad131= modelSpace.newElement('FourNodeQuad', [n260.tag, n278.tag, n304.tag, n281.tag])
quad131.thickness= thick1
#element quad 132 278 302 322 304  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad132= modelSpace.newElement('FourNodeQuad', [n278.tag, n302.tag, n322.tag, n304.tag])
quad132.thickness= thick1
#element quad 133 302 325 345 322  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad133= modelSpace.newElement('FourNodeQuad', [n302.tag, n325.tag, n345.tag, n322.tag])
quad133.thickness= thick1
#element quad 134 325 346 370 345  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad134= modelSpace.newElement('FourNodeQuad', [n325.tag, n346.tag, n370.tag, n345.tag])
quad134.thickness= thick1
#element quad 135 346 374 394 370  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad135= modelSpace.newElement('FourNodeQuad', [n346.tag, n374.tag, n394.tag, n370.tag])
quad135.thickness= thick1
#element quad 136 374 399 415 394  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad136= modelSpace.newElement('FourNodeQuad', [n374.tag, n399.tag, n415.tag, n394.tag])
quad136.thickness= thick1
#element quad 137 399 419 428 415  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad137= modelSpace.newElement('FourNodeQuad', [n399.tag, n419.tag, n428.tag, n415.tag])
quad137.thickness= thick1
#element quad 138 419 434 443 428  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad138= modelSpace.newElement('FourNodeQuad', [n419.tag, n434.tag, n443.tag, n428.tag])
quad138.thickness= thick1
#element quad 139 434 447 454 443  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad139= modelSpace.newElement('FourNodeQuad', [n434.tag, n447.tag, n454.tag, n443.tag])
quad139.thickness= thick1
#element quad 140 447 456 463 454  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad140= modelSpace.newElement('FourNodeQuad', [n447.tag, n456.tag, n463.tag, n454.tag])
quad140.thickness= thick1
#element quad 141 281 304 326 308  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad141= modelSpace.newElement('FourNodeQuad', [n281.tag, n304.tag, n326.tag, n308.tag])
quad141.thickness= thick1
#element quad 142 304 322 347 326  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad142= modelSpace.newElement('FourNodeQuad', [n304.tag, n322.tag, n347.tag, n326.tag])
quad142.thickness= thick1
#element quad 143 322 345 369 347  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad143= modelSpace.newElement('FourNodeQuad', [n322.tag, n345.tag, n369.tag, n347.tag])
quad143.thickness= thick1
#element quad 144 345 370 392 369  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad144= modelSpace.newElement('FourNodeQuad', [n345.tag, n370.tag, n392.tag, n369.tag])
quad144.thickness= thick1
#element quad 145 370 394 408 392  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad145= modelSpace.newElement('FourNodeQuad', [n370.tag, n394.tag, n408.tag, n392.tag])
quad145.thickness= thick1
#element quad 146 394 415 426 408  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad146= modelSpace.newElement('FourNodeQuad', [n394.tag, n415.tag, n426.tag, n408.tag])
quad146.thickness= thick1
#element quad 147 415 428 441 426  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad147= modelSpace.newElement('FourNodeQuad', [n415.tag, n428.tag, n441.tag, n426.tag])
quad147.thickness= thick1
#element quad 148 428 443 452 441  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad148= modelSpace.newElement('FourNodeQuad', [n428.tag, n443.tag, n452.tag, n441.tag])
quad148.thickness= thick1
#element quad 149 443 454 462 452  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad149= modelSpace.newElement('FourNodeQuad', [n443.tag, n454.tag, n462.tag, n452.tag])
quad149.thickness= thick1
#element quad 150 454 463 469 462  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad150= modelSpace.newElement('FourNodeQuad', [n454.tag, n463.tag, n469.tag, n462.tag])
quad150.thickness= thick1
#element quad 151 308 326 353 336  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad151= modelSpace.newElement('FourNodeQuad', [n308.tag, n326.tag, n353.tag, n336.tag])
quad151.thickness= thick1
#element quad 152 326 347 378 353  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad152= modelSpace.newElement('FourNodeQuad', [n326.tag, n347.tag, n378.tag, n353.tag])
quad152.thickness= thick1
#element quad 153 347 369 395 378  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad153= modelSpace.newElement('FourNodeQuad', [n347.tag, n369.tag, n395.tag, n378.tag])
quad153.thickness= thick1
#element quad 154 369 392 411 395  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad154= modelSpace.newElement('FourNodeQuad', [n369.tag, n392.tag, n411.tag, n395.tag])
quad154.thickness= thick1
#element quad 155 392 408 425 411  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad155= modelSpace.newElement('FourNodeQuad', [n392.tag, n408.tag, n425.tag, n411.tag])
quad155.thickness= thick1
#element quad 156 408 426 440 425  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad156= modelSpace.newElement('FourNodeQuad', [n408.tag, n426.tag, n440.tag, n425.tag])
quad156.thickness= thick1
#element quad 157 426 441 449 440  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad157= modelSpace.newElement('FourNodeQuad', [n426.tag, n441.tag, n449.tag, n440.tag])
quad157.thickness= thick1
#element quad 158 441 452 459 449  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad158= modelSpace.newElement('FourNodeQuad', [n441.tag, n452.tag, n459.tag, n449.tag])
quad158.thickness= thick1
#element quad 159 452 462 467 459  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad159= modelSpace.newElement('FourNodeQuad', [n452.tag, n462.tag, n467.tag, n459.tag])
quad159.thickness= thick1
#element quad 160 462 469 474 467  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad160= modelSpace.newElement('FourNodeQuad', [n462.tag, n469.tag, n474.tag, n467.tag])
quad160.thickness= thick1
#element quad 161 336 353 380 363  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad161= modelSpace.newElement('FourNodeQuad', [n336.tag, n353.tag, n380.tag, n363.tag])
quad161.thickness= thick1
#element quad 162 353 378 398 380  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad162= modelSpace.newElement('FourNodeQuad', [n353.tag, n378.tag, n398.tag, n380.tag])
quad162.thickness= thick1
#element quad 163 378 395 414 398  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad163= modelSpace.newElement('FourNodeQuad', [n378.tag, n395.tag, n414.tag, n398.tag])
quad163.thickness= thick1
#element quad 164 395 411 427 414  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad164= modelSpace.newElement('FourNodeQuad', [n395.tag, n411.tag, n427.tag, n414.tag])
quad164.thickness= thick1
#element quad 165 411 425 439 427  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad165= modelSpace.newElement('FourNodeQuad', [n411.tag, n425.tag, n439.tag, n427.tag])
quad165.thickness= thick1
#element quad 166 425 440 448 439  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad166= modelSpace.newElement('FourNodeQuad', [n425.tag, n440.tag, n448.tag, n439.tag])
quad166.thickness= thick1
#element quad 167 440 449 457 448  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad167= modelSpace.newElement('FourNodeQuad', [n440.tag, n449.tag, n457.tag, n448.tag])
quad167.thickness= thick1
#element quad 168 449 459 465 457  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad168= modelSpace.newElement('FourNodeQuad', [n449.tag, n459.tag, n465.tag, n457.tag])
quad168.thickness= thick1
#element quad 169 459 467 472 465  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad169= modelSpace.newElement('FourNodeQuad', [n459.tag, n467.tag, n472.tag, n465.tag])
quad169.thickness= thick1
#element quad 170 467 474 478 472  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad170= modelSpace.newElement('FourNodeQuad', [n467.tag, n474.tag, n478.tag, n472.tag])
quad170.thickness= thick1
#element quad 171 363 380 405 387  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad171= modelSpace.newElement('FourNodeQuad', [n363.tag, n380.tag, n405.tag, n387.tag])
quad171.thickness= thick1
#element quad 172 380 398 418 405  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad172= modelSpace.newElement('FourNodeQuad', [n380.tag, n398.tag, n418.tag, n405.tag])
quad172.thickness= thick1
#element quad 173 398 414 429 418  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad173= modelSpace.newElement('FourNodeQuad', [n398.tag, n414.tag, n429.tag, n418.tag])
quad173.thickness= thick1
#element quad 174 414 427 442 429  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad174= modelSpace.newElement('FourNodeQuad', [n414.tag, n427.tag, n442.tag, n429.tag])
quad174.thickness= thick1
#element quad 175 427 439 450 442  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad175= modelSpace.newElement('FourNodeQuad', [n427.tag, n439.tag, n450.tag, n442.tag])
quad175.thickness= thick1
#element quad 176 439 448 458 450  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad176= modelSpace.newElement('FourNodeQuad', [n439.tag, n448.tag, n458.tag, n450.tag])
quad176.thickness= thick1
#element quad 177 448 457 464 458  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad177= modelSpace.newElement('FourNodeQuad', [n448.tag, n457.tag, n464.tag, n458.tag])
quad177.thickness= thick1
#element quad 178 457 465 470 464  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad178= modelSpace.newElement('FourNodeQuad', [n457.tag, n465.tag, n470.tag, n464.tag])
quad178.thickness= thick1
#element quad 179 465 472 477 470  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad179= modelSpace.newElement('FourNodeQuad', [n465.tag, n472.tag, n477.tag, n470.tag])
quad179.thickness= thick1
#element quad 180 472 478 481 477  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad180= modelSpace.newElement('FourNodeQuad', [n472.tag, n478.tag, n481.tag, n477.tag])
quad180.thickness= thick1
#element quad 181 387 405 424 412  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad181= modelSpace.newElement('FourNodeQuad', [n387.tag, n405.tag, n424.tag, n412.tag])
quad181.thickness= thick1
#element quad 182 405 418 433 424  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad182= modelSpace.newElement('FourNodeQuad', [n405.tag, n418.tag, n433.tag, n424.tag])
quad182.thickness= thick1
#element quad 183 418 429 444 433  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad183= modelSpace.newElement('FourNodeQuad', [n418.tag, n429.tag, n444.tag, n433.tag])
quad183.thickness= thick1
#element quad 184 429 442 453 444  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad184= modelSpace.newElement('FourNodeQuad', [n429.tag, n442.tag, n453.tag, n444.tag])
quad184.thickness= thick1
#element quad 185 442 450 460 453  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad185= modelSpace.newElement('FourNodeQuad', [n442.tag, n450.tag, n460.tag, n453.tag])
quad185.thickness= thick1
#element quad 186 450 458 466 460  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad186= modelSpace.newElement('FourNodeQuad', [n450.tag, n458.tag, n466.tag, n460.tag])
quad186.thickness= thick1
#element quad 187 458 464 471 466  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad187= modelSpace.newElement('FourNodeQuad', [n458.tag, n464.tag, n471.tag, n466.tag])
quad187.thickness= thick1
#element quad 188 464 470 475 471  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad188= modelSpace.newElement('FourNodeQuad', [n464.tag, n470.tag, n475.tag, n471.tag])
quad188.thickness= thick1
#element quad 189 470 477 479 475  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad189= modelSpace.newElement('FourNodeQuad', [n470.tag, n477.tag, n479.tag, n475.tag])
quad189.thickness= thick1
#element quad 190 477 481 483 479  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad190= modelSpace.newElement('FourNodeQuad', [n477.tag, n481.tag, n483.tag, n479.tag])
quad190.thickness= thick1
#element quad 191 412 424 437 430  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad191= modelSpace.newElement('FourNodeQuad', [n412.tag, n424.tag, n437.tag, n430.tag])
quad191.thickness= thick1
#element quad 192 424 433 446 437  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad192= modelSpace.newElement('FourNodeQuad', [n424.tag, n433.tag, n446.tag, n437.tag])
quad192.thickness= thick1
#element quad 193 433 444 455 446  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad193= modelSpace.newElement('FourNodeQuad', [n433.tag, n444.tag, n455.tag, n446.tag])
quad193.thickness= thick1
#element quad 194 444 453 461 455  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad194= modelSpace.newElement('FourNodeQuad', [n444.tag, n453.tag, n461.tag, n455.tag])
quad194.thickness= thick1
#element quad 195 453 460 468 461  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad195= modelSpace.newElement('FourNodeQuad', [n453.tag, n460.tag, n468.tag, n461.tag])
quad195.thickness= thick1
#element quad 196 460 466 473 468  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad196= modelSpace.newElement('FourNodeQuad', [n460.tag, n466.tag, n473.tag, n468.tag])
quad196.thickness= thick1
#element quad 197 466 471 476 473  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad197= modelSpace.newElement('FourNodeQuad', [n466.tag, n471.tag, n476.tag, n473.tag])
quad197.thickness= thick1
#element quad 198 471 475 480 476  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad198= modelSpace.newElement('FourNodeQuad', [n471.tag, n475.tag, n480.tag, n476.tag])
quad198.thickness= thick1
#element quad 199 475 479 482 480  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad199= modelSpace.newElement('FourNodeQuad', [n475.tag, n479.tag, n482.tag, n480.tag])
quad199.thickness= thick1
#element quad 200 479 483 484 482  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad200= modelSpace.newElement('FourNodeQuad', [n479.tag, n483.tag, n484.tag, n482.tag])
quad200.thickness= thick1
#element quad 201 88 92 75 72  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad201= modelSpace.newElement('FourNodeQuad', [n88.tag, n92.tag, n75.tag, n72.tag])
quad201.thickness= thick1
#element quad 202 92 93 79 75  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad202= modelSpace.newElement('FourNodeQuad', [n92.tag, n93.tag, n79.tag, n75.tag])
quad202.thickness= thick1
#element quad 203 93 98 83 79  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad203= modelSpace.newElement('FourNodeQuad', [n93.tag, n98.tag, n83.tag, n79.tag])
quad203.thickness= thick1
#element quad 204 98 105 84 83  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad204= modelSpace.newElement('FourNodeQuad', [n98.tag, n105.tag, n84.tag, n83.tag])
quad204.thickness= thick1
#element quad 205 105 115 95 84  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad205= modelSpace.newElement('FourNodeQuad', [n105.tag, n115.tag, n95.tag, n84.tag])
quad205.thickness= thick1
#element quad 206 115 125 107 95  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad206= modelSpace.newElement('FourNodeQuad', [n115.tag, n125.tag, n107.tag, n95.tag])
quad206.thickness= thick1
#element quad 207 125 139 122 107  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad207= modelSpace.newElement('FourNodeQuad', [n125.tag, n139.tag, n122.tag, n107.tag])
quad207.thickness= thick1
#element quad 208 139 150 134 122  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad208= modelSpace.newElement('FourNodeQuad', [n139.tag, n150.tag, n134.tag, n122.tag])
quad208.thickness= thick1
#element quad 209 150 166 148 134  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad209= modelSpace.newElement('FourNodeQuad', [n150.tag, n166.tag, n148.tag, n134.tag])
quad209.thickness= thick1
#element quad 210 166 182 167 148  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad210= modelSpace.newElement('FourNodeQuad', [n166.tag, n182.tag, n167.tag, n148.tag])
quad210.thickness= thick1
#element quad 211 182 199 186 167  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad211= modelSpace.newElement('FourNodeQuad', [n182.tag, n199.tag, n186.tag, n167.tag])
quad211.thickness= thick1
#element quad 212 199 221 202 186  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad212= modelSpace.newElement('FourNodeQuad', [n199.tag, n221.tag, n202.tag, n186.tag])
quad212.thickness= thick1
#element quad 213 221 244 224 202  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad213= modelSpace.newElement('FourNodeQuad', [n221.tag, n244.tag, n224.tag, n202.tag])
quad213.thickness= thick1
#element quad 214 244 267 249 224  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad214= modelSpace.newElement('FourNodeQuad', [n244.tag, n267.tag, n249.tag, n224.tag])
quad214.thickness= thick1
#element quad 215 267 291 276 249  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad215= modelSpace.newElement('FourNodeQuad', [n267.tag, n291.tag, n276.tag, n249.tag])
quad215.thickness= thick1
#element quad 216 291 315 298 276  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad216= modelSpace.newElement('FourNodeQuad', [n291.tag, n315.tag, n298.tag, n276.tag])
quad216.thickness= thick1
#element quad 217 315 344 328 298  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad217= modelSpace.newElement('FourNodeQuad', [n315.tag, n344.tag, n328.tag, n298.tag])
quad217.thickness= thick1
#element quad 218 344 372 359 328  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad218= modelSpace.newElement('FourNodeQuad', [n344.tag, n372.tag, n359.tag, n328.tag])
quad218.thickness= thick1
#element quad 219 372 400 386 359  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad219= modelSpace.newElement('FourNodeQuad', [n372.tag, n400.tag, n386.tag, n359.tag])
quad219.thickness= thick1
#element quad 220 400 421 410 386  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad220= modelSpace.newElement('FourNodeQuad', [n400.tag, n421.tag, n410.tag, n386.tag])
quad220.thickness= thick1
#element quad 221 72 75 59 58  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad221= modelSpace.newElement('FourNodeQuad', [n72.tag, n75.tag, n59.tag, n58.tag])
quad221.thickness= thick1
#element quad 222 75 79 64 59  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad222= modelSpace.newElement('FourNodeQuad', [n75.tag, n79.tag, n64.tag, n59.tag])
quad222.thickness= thick1
#element quad 223 79 83 67 64  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad223= modelSpace.newElement('FourNodeQuad', [n79.tag, n83.tag, n67.tag, n64.tag])
quad223.thickness= thick1
#element quad 224 83 84 70 67  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad224= modelSpace.newElement('FourNodeQuad', [n83.tag, n84.tag, n70.tag, n67.tag])
quad224.thickness= thick1
#element quad 225 84 95 80 70  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad225= modelSpace.newElement('FourNodeQuad', [n84.tag, n95.tag, n80.tag, n70.tag])
quad225.thickness= thick1
#element quad 226 95 107 89 80  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad226= modelSpace.newElement('FourNodeQuad', [n95.tag, n107.tag, n89.tag, n80.tag])
quad226.thickness= thick1
#element quad 227 107 122 103 89  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad227= modelSpace.newElement('FourNodeQuad', [n107.tag, n122.tag, n103.tag, n89.tag])
quad227.thickness= thick1
#element quad 228 122 134 118 103  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad228= modelSpace.newElement('FourNodeQuad', [n122.tag, n134.tag, n118.tag, n103.tag])
quad228.thickness= thick1
#element quad 229 134 148 132 118  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad229= modelSpace.newElement('FourNodeQuad', [n134.tag, n148.tag, n132.tag, n118.tag])
quad229.thickness= thick1
#element quad 230 148 167 149 132  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad230= modelSpace.newElement('FourNodeQuad', [n148.tag, n167.tag, n149.tag, n132.tag])
quad230.thickness= thick1
#element quad 231 167 186 172 149  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad231= modelSpace.newElement('FourNodeQuad', [n167.tag, n186.tag, n172.tag, n149.tag])
quad231.thickness= thick1
#element quad 232 186 202 192 172  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad232= modelSpace.newElement('FourNodeQuad', [n186.tag, n202.tag, n192.tag, n172.tag])
quad232.thickness= thick1
#element quad 233 202 224 213 192  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad233= modelSpace.newElement('FourNodeQuad', [n202.tag, n224.tag, n213.tag, n192.tag])
quad233.thickness= thick1
#element quad 234 224 249 235 213  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad234= modelSpace.newElement('FourNodeQuad', [n224.tag, n249.tag, n235.tag, n213.tag])
quad234.thickness= thick1
#element quad 235 249 276 257 235  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad235= modelSpace.newElement('FourNodeQuad', [n249.tag, n276.tag, n257.tag, n235.tag])
quad235.thickness= thick1
#element quad 236 276 298 283 257  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad236= modelSpace.newElement('FourNodeQuad', [n276.tag, n298.tag, n283.tag, n257.tag])
quad236.thickness= thick1
#element quad 237 298 328 313 283  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad237= modelSpace.newElement('FourNodeQuad', [n298.tag, n328.tag, n313.tag, n283.tag])
quad237.thickness= thick1
#element quad 238 328 359 342 313  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad238= modelSpace.newElement('FourNodeQuad', [n328.tag, n359.tag, n342.tag, n313.tag])
quad238.thickness= thick1
#element quad 239 359 386 375 342  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad239= modelSpace.newElement('FourNodeQuad', [n359.tag, n386.tag, n375.tag, n342.tag])
quad239.thickness= thick1
#element quad 240 386 410 402 375  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad240= modelSpace.newElement('FourNodeQuad', [n386.tag, n410.tag, n402.tag, n375.tag])
quad240.thickness= thick1
#element quad 241 58 59 48 45  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad241= modelSpace.newElement('FourNodeQuad', [n58.tag, n59.tag, n48.tag, n45.tag])
quad241.thickness= thick1
#element quad 242 59 64 51 48  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad242= modelSpace.newElement('FourNodeQuad', [n59.tag, n64.tag, n51.tag, n48.tag])
quad242.thickness= thick1
#element quad 243 64 67 54 51  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad243= modelSpace.newElement('FourNodeQuad', [n64.tag, n67.tag, n54.tag, n51.tag])
quad243.thickness= thick1
#element quad 244 67 70 61 54  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad244= modelSpace.newElement('FourNodeQuad', [n67.tag, n70.tag, n61.tag, n54.tag])
quad244.thickness= thick1
#element quad 245 70 80 68 61  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad245= modelSpace.newElement('FourNodeQuad', [n70.tag, n80.tag, n68.tag, n61.tag])
quad245.thickness= thick1
#element quad 246 80 89 77 68  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad246= modelSpace.newElement('FourNodeQuad', [n80.tag, n89.tag, n77.tag, n68.tag])
quad246.thickness= thick1
#element quad 247 89 103 86 77  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad247= modelSpace.newElement('FourNodeQuad', [n89.tag, n103.tag, n86.tag, n77.tag])
quad247.thickness= thick1
#element quad 248 103 118 102 86  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad248= modelSpace.newElement('FourNodeQuad', [n103.tag, n118.tag, n102.tag, n86.tag])
quad248.thickness= thick1
#element quad 249 118 132 121 102  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad249= modelSpace.newElement('FourNodeQuad', [n118.tag, n132.tag, n121.tag, n102.tag])
quad249.thickness= thick1
#element quad 250 132 149 140 121  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad250= modelSpace.newElement('FourNodeQuad', [n132.tag, n149.tag, n140.tag, n121.tag])
quad250.thickness= thick1
#element quad 251 149 172 159 140  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad251= modelSpace.newElement('FourNodeQuad', [n149.tag, n172.tag, n159.tag, n140.tag])
quad251.thickness= thick1
#element quad 252 172 192 174 159  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad252= modelSpace.newElement('FourNodeQuad', [n172.tag, n192.tag, n174.tag, n159.tag])
quad252.thickness= thick1
#element quad 253 192 213 195 174  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad253= modelSpace.newElement('FourNodeQuad', [n192.tag, n213.tag, n195.tag, n174.tag])
quad253.thickness= thick1
#element quad 254 213 235 222 195  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad254= modelSpace.newElement('FourNodeQuad', [n213.tag, n235.tag, n222.tag, n195.tag])
quad254.thickness= thick1
#element quad 255 235 257 247 222  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad255= modelSpace.newElement('FourNodeQuad', [n235.tag, n257.tag, n247.tag, n222.tag])
quad255.thickness= thick1
#element quad 256 257 283 272 247  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad256= modelSpace.newElement('FourNodeQuad', [n257.tag, n283.tag, n272.tag, n247.tag])
quad256.thickness= thick1
#element quad 257 283 313 300 272  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad257= modelSpace.newElement('FourNodeQuad', [n283.tag, n313.tag, n300.tag, n272.tag])
quad257.thickness= thick1
#element quad 258 313 342 332 300  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad258= modelSpace.newElement('FourNodeQuad', [n313.tag, n342.tag, n332.tag, n300.tag])
quad258.thickness= thick1
#element quad 259 342 375 365 332  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad259= modelSpace.newElement('FourNodeQuad', [n342.tag, n375.tag, n365.tag, n332.tag])
quad259.thickness= thick1
#element quad 260 375 402 391 365  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad260= modelSpace.newElement('FourNodeQuad', [n375.tag, n402.tag, n391.tag, n365.tag])
quad260.thickness= thick1
#element quad 261 45 48 37 35  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad261= modelSpace.newElement('FourNodeQuad', [n45.tag, n48.tag, n37.tag, n35.tag])
quad261.thickness= thick1
#element quad 262 48 51 39 37  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad262= modelSpace.newElement('FourNodeQuad', [n48.tag, n51.tag, n39.tag, n37.tag])
quad262.thickness= thick1
#element quad 263 51 54 43 39  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad263= modelSpace.newElement('FourNodeQuad', [n51.tag, n54.tag, n43.tag, n39.tag])
quad263.thickness= thick1
#element quad 264 54 61 49 43  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad264= modelSpace.newElement('FourNodeQuad', [n54.tag, n61.tag, n49.tag, n43.tag])
quad264.thickness= thick1
#element quad 265 61 68 55 49  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad265= modelSpace.newElement('FourNodeQuad', [n61.tag, n68.tag, n55.tag, n49.tag])
quad265.thickness= thick1
#element quad 266 68 77 65 55  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad266= modelSpace.newElement('FourNodeQuad', [n68.tag, n77.tag, n65.tag, n55.tag])
quad266.thickness= thick1
#element quad 267 77 86 78 65  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad267= modelSpace.newElement('FourNodeQuad', [n77.tag, n86.tag, n78.tag, n65.tag])
quad267.thickness= thick1
#element quad 268 86 102 90 78  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad268= modelSpace.newElement('FourNodeQuad', [n86.tag, n102.tag, n90.tag, n78.tag])
quad268.thickness= thick1
#element quad 269 102 121 108 90  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad269= modelSpace.newElement('FourNodeQuad', [n102.tag, n121.tag, n108.tag, n90.tag])
quad269.thickness= thick1
#element quad 270 121 140 124 108  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad270= modelSpace.newElement('FourNodeQuad', [n121.tag, n140.tag, n124.tag, n108.tag])
quad270.thickness= thick1
#element quad 271 140 159 145 124  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad271= modelSpace.newElement('FourNodeQuad', [n140.tag, n159.tag, n145.tag, n124.tag])
quad271.thickness= thick1
#element quad 272 159 174 165 145  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad272= modelSpace.newElement('FourNodeQuad', [n159.tag, n174.tag, n165.tag, n145.tag])
quad272.thickness= thick1
#element quad 273 174 195 188 165  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad273= modelSpace.newElement('FourNodeQuad', [n174.tag, n195.tag, n188.tag, n165.tag])
quad273.thickness= thick1
#element quad 274 195 222 211 188  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad274= modelSpace.newElement('FourNodeQuad', [n195.tag, n222.tag, n211.tag, n188.tag])
quad274.thickness= thick1
#element quad 275 222 247 236 211  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad275= modelSpace.newElement('FourNodeQuad', [n222.tag, n247.tag, n236.tag, n211.tag])
quad275.thickness= thick1
#element quad 276 247 272 262 236  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad276= modelSpace.newElement('FourNodeQuad', [n247.tag, n272.tag, n262.tag, n236.tag])
quad276.thickness= thick1
#element quad 277 272 300 289 262  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad277= modelSpace.newElement('FourNodeQuad', [n272.tag, n300.tag, n289.tag, n262.tag])
quad277.thickness= thick1
#element quad 278 300 332 317 289  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad278= modelSpace.newElement('FourNodeQuad', [n300.tag, n332.tag, n317.tag, n289.tag])
quad278.thickness= thick1
#element quad 279 332 365 349 317  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad279= modelSpace.newElement('FourNodeQuad', [n332.tag, n365.tag, n349.tag, n317.tag])
quad279.thickness= thick1
#element quad 280 365 391 382 349  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad280= modelSpace.newElement('FourNodeQuad', [n365.tag, n391.tag, n382.tag, n349.tag])
quad280.thickness= thick1
#element quad 281 35 37 28 24  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad281= modelSpace.newElement('FourNodeQuad', [n35.tag, n37.tag, n28.tag, n24.tag])
quad281.thickness= thick1
#element quad 282 37 39 30 28  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad282= modelSpace.newElement('FourNodeQuad', [n37.tag, n39.tag, n30.tag, n28.tag])
quad282.thickness= thick1
#element quad 283 39 43 33 30  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad283= modelSpace.newElement('FourNodeQuad', [n39.tag, n43.tag, n33.tag, n30.tag])
quad283.thickness= thick1
#element quad 284 43 49 41 33  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad284= modelSpace.newElement('FourNodeQuad', [n43.tag, n49.tag, n41.tag, n33.tag])
quad284.thickness= thick1
#element quad 285 49 55 46 41  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad285= modelSpace.newElement('FourNodeQuad', [n49.tag, n55.tag, n46.tag, n41.tag])
quad285.thickness= thick1
#element quad 286 55 65 56 46  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad286= modelSpace.newElement('FourNodeQuad', [n55.tag, n65.tag, n56.tag, n46.tag])
quad286.thickness= thick1
#element quad 287 65 78 69 56  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad287= modelSpace.newElement('FourNodeQuad', [n65.tag, n78.tag, n69.tag, n56.tag])
quad287.thickness= thick1
#element quad 288 78 90 81 69  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad288= modelSpace.newElement('FourNodeQuad', [n78.tag, n90.tag, n81.tag, n69.tag])
quad288.thickness= thick1
#element quad 289 90 108 96 81  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad289= modelSpace.newElement('FourNodeQuad', [n90.tag, n108.tag, n96.tag, n81.tag])
quad289.thickness= thick1
#element quad 290 108 124 114 96  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad290= modelSpace.newElement('FourNodeQuad', [n108.tag, n124.tag, n114.tag, n96.tag])
quad290.thickness= thick1
#element quad 291 124 145 136 114  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad291= modelSpace.newElement('FourNodeQuad', [n124.tag, n145.tag, n136.tag, n114.tag])
quad291.thickness= thick1
#element quad 292 145 165 155 136  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad292= modelSpace.newElement('FourNodeQuad', [n145.tag, n165.tag, n155.tag, n136.tag])
quad292.thickness= thick1
#element quad 293 165 188 175 155  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad293= modelSpace.newElement('FourNodeQuad', [n165.tag, n188.tag, n175.tag, n155.tag])
quad293.thickness= thick1
#element quad 294 188 211 201 175  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad294= modelSpace.newElement('FourNodeQuad', [n188.tag, n211.tag, n201.tag, n175.tag])
quad294.thickness= thick1
#element quad 295 211 236 226 201  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad295= modelSpace.newElement('FourNodeQuad', [n211.tag, n236.tag, n226.tag, n201.tag])
quad295.thickness= thick1
#element quad 296 236 262 251 226  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad296= modelSpace.newElement('FourNodeQuad', [n236.tag, n262.tag, n251.tag, n226.tag])
quad296.thickness= thick1
#element quad 297 262 289 279 251  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad297= modelSpace.newElement('FourNodeQuad', [n262.tag, n289.tag, n279.tag, n251.tag])
quad297.thickness= thick1
#element quad 298 289 317 310 279  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad298= modelSpace.newElement('FourNodeQuad', [n289.tag, n317.tag, n310.tag, n279.tag])
quad298.thickness= thick1
#element quad 299 317 349 340 310  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad299= modelSpace.newElement('FourNodeQuad', [n317.tag, n349.tag, n340.tag, n310.tag])
quad299.thickness= thick1
#element quad 300 349 382 376 340  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad300= modelSpace.newElement('FourNodeQuad', [n349.tag, n382.tag, n376.tag, n340.tag])
quad300.thickness= thick1
#element quad 301 24 28 19 16  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad301= modelSpace.newElement('FourNodeQuad', [n24.tag, n28.tag, n19.tag, n16.tag])
quad301.thickness= thick1
#element quad 302 28 30 21 19  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad302= modelSpace.newElement('FourNodeQuad', [n28.tag, n30.tag, n21.tag, n19.tag])
quad302.thickness= thick1
#element quad 303 30 33 25 21  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad303= modelSpace.newElement('FourNodeQuad', [n30.tag, n33.tag, n25.tag, n21.tag])
quad303.thickness= thick1
#element quad 304 33 41 31 25  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad304= modelSpace.newElement('FourNodeQuad', [n33.tag, n41.tag, n31.tag, n25.tag])
quad304.thickness= thick1
#element quad 305 41 46 40 31  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad305= modelSpace.newElement('FourNodeQuad', [n41.tag, n46.tag, n40.tag, n31.tag])
quad305.thickness= thick1
#element quad 306 46 56 50 40  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad306= modelSpace.newElement('FourNodeQuad', [n46.tag, n56.tag, n50.tag, n40.tag])
quad306.thickness= thick1
#element quad 307 56 69 62 50  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad307= modelSpace.newElement('FourNodeQuad', [n56.tag, n69.tag, n62.tag, n50.tag])
quad307.thickness= thick1
#element quad 308 69 81 71 62  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad308= modelSpace.newElement('FourNodeQuad', [n69.tag, n81.tag, n71.tag, n62.tag])
quad308.thickness= thick1
#element quad 309 81 96 85 71  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad309= modelSpace.newElement('FourNodeQuad', [n81.tag, n96.tag, n85.tag, n71.tag])
quad309.thickness= thick1
#element quad 310 96 114 104 85  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad310= modelSpace.newElement('FourNodeQuad', [n96.tag, n114.tag, n104.tag, n85.tag])
quad310.thickness= thick1
#element quad 311 114 136 127 104  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad311= modelSpace.newElement('FourNodeQuad', [n114.tag, n136.tag, n127.tag, n104.tag])
quad311.thickness= thick1
#element quad 312 136 155 147 127  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad312= modelSpace.newElement('FourNodeQuad', [n136.tag, n155.tag, n147.tag, n127.tag])
quad312.thickness= thick1
#element quad 313 155 175 169 147  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad313= modelSpace.newElement('FourNodeQuad', [n155.tag, n175.tag, n169.tag, n147.tag])
quad313.thickness= thick1
#element quad 314 175 201 194 169  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad314= modelSpace.newElement('FourNodeQuad', [n175.tag, n201.tag, n194.tag, n169.tag])
quad314.thickness= thick1
#element quad 315 201 226 216 194  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad315= modelSpace.newElement('FourNodeQuad', [n201.tag, n226.tag, n216.tag, n194.tag])
quad315.thickness= thick1
#element quad 316 226 251 246 216  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad316= modelSpace.newElement('FourNodeQuad', [n226.tag, n251.tag, n246.tag, n216.tag])
quad316.thickness= thick1
#element quad 317 251 279 271 246  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad317= modelSpace.newElement('FourNodeQuad', [n251.tag, n279.tag, n271.tag, n246.tag])
quad317.thickness= thick1
#element quad 318 279 310 305 271  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad318= modelSpace.newElement('FourNodeQuad', [n279.tag, n310.tag, n305.tag, n271.tag])
quad318.thickness= thick1
#element quad 319 310 340 337 305  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad319= modelSpace.newElement('FourNodeQuad', [n310.tag, n340.tag, n337.tag, n305.tag])
quad319.thickness= thick1
#element quad 320 340 376 366 337  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad320= modelSpace.newElement('FourNodeQuad', [n340.tag, n376.tag, n366.tag, n337.tag])
quad320.thickness= thick1
#element quad 321 16 19 13 11  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad321= modelSpace.newElement('FourNodeQuad', [n16.tag, n19.tag, n13.tag, n11.tag])
quad321.thickness= thick1
#element quad 322 19 21 14 13  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad322= modelSpace.newElement('FourNodeQuad', [n19.tag, n21.tag, n14.tag, n13.tag])
quad322.thickness= thick1
#element quad 323 21 25 20 14  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad323= modelSpace.newElement('FourNodeQuad', [n21.tag, n25.tag, n20.tag, n14.tag])
quad323.thickness= thick1
#element quad 324 25 31 26 20  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad324= modelSpace.newElement('FourNodeQuad', [n25.tag, n31.tag, n26.tag, n20.tag])
quad324.thickness= thick1
#element quad 325 31 40 32 26  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad325= modelSpace.newElement('FourNodeQuad', [n31.tag, n40.tag, n32.tag, n26.tag])
quad325.thickness= thick1
#element quad 326 40 50 42 32  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad326= modelSpace.newElement('FourNodeQuad', [n40.tag, n50.tag, n42.tag, n32.tag])
quad326.thickness= thick1
#element quad 327 50 62 53 42  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad327= modelSpace.newElement('FourNodeQuad', [n50.tag, n62.tag, n53.tag, n42.tag])
quad327.thickness= thick1
#element quad 328 62 71 66 53  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad328= modelSpace.newElement('FourNodeQuad', [n62.tag, n71.tag, n66.tag, n53.tag])
quad328.thickness= thick1
#element quad 329 71 85 82 66  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad329= modelSpace.newElement('FourNodeQuad', [n71.tag, n85.tag, n82.tag, n66.tag])
quad329.thickness= thick1
#element quad 330 85 104 97 82  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad330= modelSpace.newElement('FourNodeQuad', [n85.tag, n104.tag, n97.tag, n82.tag])
quad330.thickness= thick1
#element quad 331 104 127 120 97  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad331= modelSpace.newElement('FourNodeQuad', [n104.tag, n127.tag, n120.tag, n97.tag])
quad331.thickness= thick1
#element quad 332 127 147 142 120  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad332= modelSpace.newElement('FourNodeQuad', [n127.tag, n147.tag, n142.tag, n120.tag])
quad332.thickness= thick1
#element quad 333 147 169 163 142  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad333= modelSpace.newElement('FourNodeQuad', [n147.tag, n169.tag, n163.tag, n142.tag])
quad333.thickness= thick1
#element quad 334 169 194 190 163  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad334= modelSpace.newElement('FourNodeQuad', [n169.tag, n194.tag, n190.tag, n163.tag])
quad334.thickness= thick1
#element quad 335 194 216 215 190  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad335= modelSpace.newElement('FourNodeQuad', [n194.tag, n216.tag, n215.tag, n190.tag])
quad335.thickness= thick1
#element quad 336 216 246 238 215  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad336= modelSpace.newElement('FourNodeQuad', [n216.tag, n246.tag, n238.tag, n215.tag])
quad336.thickness= thick1
#element quad 337 246 271 269 238  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad337= modelSpace.newElement('FourNodeQuad', [n246.tag, n271.tag, n269.tag, n238.tag])
quad337.thickness= thick1
#element quad 338 271 305 296 269  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad338= modelSpace.newElement('FourNodeQuad', [n271.tag, n305.tag, n296.tag, n269.tag])
quad338.thickness= thick1
#element quad 339 305 337 331 296  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad339= modelSpace.newElement('FourNodeQuad', [n305.tag, n337.tag, n331.tag, n296.tag])
quad339.thickness= thick1
#element quad 340 337 366 360 331  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad340= modelSpace.newElement('FourNodeQuad', [n337.tag, n366.tag, n360.tag, n331.tag])
quad340.thickness= thick1
#element quad 341 11 13 8 5  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad341= modelSpace.newElement('FourNodeQuad', [n11.tag, n13.tag, n8.tag, n5.tag])
quad341.thickness= thick1
#element quad 342 13 14 9 8  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad342= modelSpace.newElement('FourNodeQuad', [n13.tag, n14.tag, n9.tag, n8.tag])
quad342.thickness= thick1
#element quad 343 14 20 15 9  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad343= modelSpace.newElement('FourNodeQuad', [n14.tag, n20.tag, n15.tag, n9.tag])
quad343.thickness= thick1
#element quad 344 20 26 22 15  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad344= modelSpace.newElement('FourNodeQuad', [n20.tag, n26.tag, n22.tag, n15.tag])
quad344.thickness= thick1
#element quad 345 26 32 29 22  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad345= modelSpace.newElement('FourNodeQuad', [n26.tag, n32.tag, n29.tag, n22.tag])
quad345.thickness= thick1
#element quad 346 32 42 38 29  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad346= modelSpace.newElement('FourNodeQuad', [n32.tag, n42.tag, n38.tag, n29.tag])
quad346.thickness= thick1
#element quad 347 42 53 52 38  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad347= modelSpace.newElement('FourNodeQuad', [n42.tag, n53.tag, n52.tag, n38.tag])
quad347.thickness= thick1
#element quad 348 53 66 63 52  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad348= modelSpace.newElement('FourNodeQuad', [n53.tag, n66.tag, n63.tag, n52.tag])
quad348.thickness= thick1
#element quad 349 66 82 76 63  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad349= modelSpace.newElement('FourNodeQuad', [n66.tag, n82.tag, n76.tag, n63.tag])
quad349.thickness= thick1
#element quad 350 82 97 94 76  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad350= modelSpace.newElement('FourNodeQuad', [n82.tag, n97.tag, n94.tag, n76.tag])
quad350.thickness= thick1
#element quad 351 97 120 117 94  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad351= modelSpace.newElement('FourNodeQuad', [n97.tag, n120.tag, n117.tag, n94.tag])
quad351.thickness= thick1
#element quad 352 120 142 137 117  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad352= modelSpace.newElement('FourNodeQuad', [n120.tag, n142.tag, n137.tag, n117.tag])
quad352.thickness= thick1
#element quad 353 142 163 160 137  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad353= modelSpace.newElement('FourNodeQuad', [n142.tag, n163.tag, n160.tag, n137.tag])
quad353.thickness= thick1
#element quad 354 163 190 183 160  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad354= modelSpace.newElement('FourNodeQuad', [n163.tag, n190.tag, n183.tag, n160.tag])
quad354.thickness= thick1
#element quad 355 190 215 208 183  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad355= modelSpace.newElement('FourNodeQuad', [n190.tag, n215.tag, n208.tag, n183.tag])
quad355.thickness= thick1
#element quad 356 215 238 232 208  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad356= modelSpace.newElement('FourNodeQuad', [n215.tag, n238.tag, n232.tag, n208.tag])
quad356.thickness= thick1
#element quad 357 238 269 265 232  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad357= modelSpace.newElement('FourNodeQuad', [n238.tag, n269.tag, n265.tag, n232.tag])
quad357.thickness= thick1
#element quad 358 269 296 294 265  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad358= modelSpace.newElement('FourNodeQuad', [n269.tag, n296.tag, n294.tag, n265.tag])
quad358.thickness= thick1
#element quad 359 296 331 323 294  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad359= modelSpace.newElement('FourNodeQuad', [n296.tag, n331.tag, n323.tag, n294.tag])
quad359.thickness= thick1
#element quad 360 331 360 357 323  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad360= modelSpace.newElement('FourNodeQuad', [n331.tag, n360.tag, n357.tag, n323.tag])
quad360.thickness= thick1
#element quad 361 5 8 4 3  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad361= modelSpace.newElement('FourNodeQuad', [n5.tag, n8.tag, n4.tag, n3.tag])
quad361.thickness= thick1
#element quad 362 8 9 7 4  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad362= modelSpace.newElement('FourNodeQuad', [n8.tag, n9.tag, n7.tag, n4.tag])
quad362.thickness= thick1
#element quad 363 9 15 12 7  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad363= modelSpace.newElement('FourNodeQuad', [n9.tag, n15.tag, n12.tag, n7.tag])
quad363.thickness= thick1
#element quad 364 15 22 18 12  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad364= modelSpace.newElement('FourNodeQuad', [n15.tag, n22.tag, n18.tag, n12.tag])
quad364.thickness= thick1
#element quad 365 22 29 27 18  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad365= modelSpace.newElement('FourNodeQuad', [n22.tag, n29.tag, n27.tag, n18.tag])
quad365.thickness= thick1
#element quad 366 29 38 36 27  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad366= modelSpace.newElement('FourNodeQuad', [n29.tag, n38.tag, n36.tag, n27.tag])
quad366.thickness= thick1
#element quad 367 38 52 47 36  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad367= modelSpace.newElement('FourNodeQuad', [n38.tag, n52.tag, n47.tag, n36.tag])
quad367.thickness= thick1
#element quad 368 52 63 60 47  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad368= modelSpace.newElement('FourNodeQuad', [n52.tag, n63.tag, n60.tag, n47.tag])
quad368.thickness= thick1
#element quad 369 63 76 74 60  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad369= modelSpace.newElement('FourNodeQuad', [n63.tag, n76.tag, n74.tag, n60.tag])
quad369.thickness= thick1
#element quad 370 76 94 91 74  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad370= modelSpace.newElement('FourNodeQuad', [n76.tag, n94.tag, n91.tag, n74.tag])
quad370.thickness= thick1
#element quad 371 94 117 111 91  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad371= modelSpace.newElement('FourNodeQuad', [n94.tag, n117.tag, n111.tag, n91.tag])
quad371.thickness= thick1
#element quad 372 117 137 133 111  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad372= modelSpace.newElement('FourNodeQuad', [n117.tag, n137.tag, n133.tag, n111.tag])
quad372.thickness= thick1
#element quad 373 137 160 156 133  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad373= modelSpace.newElement('FourNodeQuad', [n137.tag, n160.tag, n156.tag, n133.tag])
quad373.thickness= thick1
#element quad 374 160 183 179 156  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad374= modelSpace.newElement('FourNodeQuad', [n160.tag, n183.tag, n179.tag, n156.tag])
quad374.thickness= thick1
#element quad 375 183 208 206 179  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad375= modelSpace.newElement('FourNodeQuad', [n183.tag, n208.tag, n206.tag, n179.tag])
quad375.thickness= thick1
#element quad 376 208 232 230 206  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad376= modelSpace.newElement('FourNodeQuad', [n208.tag, n232.tag, n230.tag, n206.tag])
quad376.thickness= thick1
#element quad 377 232 265 258 230  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad377= modelSpace.newElement('FourNodeQuad', [n232.tag, n265.tag, n258.tag, n230.tag])
quad377.thickness= thick1
#element quad 378 265 294 288 258  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad378= modelSpace.newElement('FourNodeQuad', [n265.tag, n294.tag, n288.tag, n258.tag])
quad378.thickness= thick1
#element quad 379 294 323 320 288  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad379= modelSpace.newElement('FourNodeQuad', [n294.tag, n323.tag, n320.tag, n288.tag])
quad379.thickness= thick1
#element quad 380 323 357 354 320  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad380= modelSpace.newElement('FourNodeQuad', [n323.tag, n357.tag, n354.tag, n320.tag])
quad380.thickness= thick1
#element quad 381 3 4 2 1  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad381= modelSpace.newElement('FourNodeQuad', [n3.tag, n4.tag, n2.tag, n1.tag])
quad381.thickness= thick1
#element quad 382 4 7 6 2  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad382= modelSpace.newElement('FourNodeQuad', [n4.tag, n7.tag, n6.tag, n2.tag])
quad382.thickness= thick1
#element quad 383 7 12 10 6  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad383= modelSpace.newElement('FourNodeQuad', [n7.tag, n12.tag, n10.tag, n6.tag])
quad383.thickness= thick1
#element quad 384 12 18 17 10  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad384= modelSpace.newElement('FourNodeQuad', [n12.tag, n18.tag, n17.tag, n10.tag])
quad384.thickness= thick1
#element quad 385 18 27 23 17  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad385= modelSpace.newElement('FourNodeQuad', [n18.tag, n27.tag, n23.tag, n17.tag])
quad385.thickness= thick1
#element quad 386 27 36 34 23  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad386= modelSpace.newElement('FourNodeQuad', [n27.tag, n36.tag, n34.tag, n23.tag])
quad386.thickness= thick1
#element quad 387 36 47 44 34  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad387= modelSpace.newElement('FourNodeQuad', [n36.tag, n47.tag, n44.tag, n34.tag])
quad387.thickness= thick1
#element quad 388 47 60 57 44  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad388= modelSpace.newElement('FourNodeQuad', [n47.tag, n60.tag, n57.tag, n44.tag])
quad388.thickness= thick1
#element quad 389 60 74 73 57  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad389= modelSpace.newElement('FourNodeQuad', [n60.tag, n74.tag, n73.tag, n57.tag])
quad389.thickness= thick1
#element quad 390 74 91 87 73  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad390= modelSpace.newElement('FourNodeQuad', [n74.tag, n91.tag, n87.tag, n73.tag])
quad390.thickness= thick1
#element quad 391 91 111 110 87  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad391= modelSpace.newElement('FourNodeQuad', [n91.tag, n111.tag, n110.tag, n87.tag])
quad391.thickness= thick1
#element quad 392 111 133 129 110  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad392= modelSpace.newElement('FourNodeQuad', [n111.tag, n133.tag, n129.tag, n110.tag])
quad392.thickness= thick1
#element quad 393 133 156 154 129  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad393= modelSpace.newElement('FourNodeQuad', [n133.tag, n156.tag, n154.tag, n129.tag])
quad393.thickness= thick1
#element quad 394 156 179 177 154  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad394= modelSpace.newElement('FourNodeQuad', [n156.tag, n179.tag, n177.tag, n154.tag])
quad394.thickness= thick1
#element quad 395 179 206 204 177  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad395= modelSpace.newElement('FourNodeQuad', [n179.tag, n206.tag, n204.tag, n177.tag])
quad395.thickness= thick1
#element quad 396 206 230 228 204  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad396= modelSpace.newElement('FourNodeQuad', [n206.tag, n230.tag, n228.tag, n204.tag])
quad396.thickness= thick1
#element quad 397 230 258 255 228  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad397= modelSpace.newElement('FourNodeQuad', [n230.tag, n258.tag, n255.tag, n228.tag])
quad397.thickness= thick1
#element quad 398 258 288 287 255  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad398= modelSpace.newElement('FourNodeQuad', [n258.tag, n288.tag, n287.tag, n255.tag])
quad398.thickness= thick1
#element quad 399 288 320 318 287  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad399= modelSpace.newElement('FourNodeQuad', [n288.tag, n320.tag, n318.tag, n287.tag])
quad399.thickness= thick1
#element quad 400 320 354 351 318  $thick1 PlaneStrain 1 0.0 0.0 $xWgt1 $yWgt1
quad400= modelSpace.newElement('FourNodeQuad', [n320.tag, n354.tag, n351.tag, n318.tag])
quad400.thickness= thick1
#puts "Finished creating all soil elements..."
lmsg.log("Finished creating all soil elements...")

# create list of permanent elements with connectivities for post-processing
#set eleFile [open SolidElementInfo.dat w]
eleFile= list()
#puts $eleFile "       1       109       130       131       112"
eleFile.append(quad1)
#puts $eleFile "       2       130       152       157       131"
eleFile.append(quad2)
#puts $eleFile "       3       152       178       180       157"
eleFile.append(quad3)
#puts $eleFile "       4       178       205       207       180"
eleFile.append(quad4)
#puts $eleFile "       5       205       229       231       207"
eleFile.append(quad5)
#puts $eleFile "       6       229       256       261       231"
eleFile.append(quad6)
#puts $eleFile "       7       256       286       293       261"
eleFile.append(quad7)
#puts $eleFile "       8       286       319       321       293"
eleFile.append(quad8)
#puts $eleFile "       9       319       352       355       321"
eleFile.append(quad9)
#puts $eleFile "      10       352       383       385       355"
eleFile.append(quad10)
#puts $eleFile "      11       112       131       138       116"
eleFile.append(quad11)
#puts $eleFile "      12       131       157       161       138"
eleFile.append(quad12)
#puts $eleFile "      13       157       180       181       161"
eleFile.append(quad13)
#puts $eleFile "      14       180       207       209       181"
eleFile.append(quad14)
#puts $eleFile "      15       207       231       233       209"
eleFile.append(quad15)
#puts $eleFile "      16       231       261       266       233"
eleFile.append(quad16)
#puts $eleFile "      17       261       293       295       266"
eleFile.append(quad17)
#puts $eleFile "      18       293       321       324       295"
eleFile.append(quad18)
#puts $eleFile "      19       321       355       356       324"
eleFile.append(quad19)
#puts $eleFile "      20       355       385       388       356"
eleFile.append(quad20)
#puts $eleFile "      21       116       138       143       119"
eleFile.append(quad21)
#puts $eleFile "      22       138       161       162       143"
eleFile.append(quad22)
#puts $eleFile "      23       161       181       187       162"
eleFile.append(quad23)
#puts $eleFile "      24       181       209       214       187"
eleFile.append(quad24)
#puts $eleFile "      25       209       233       240       214"
eleFile.append(quad25)
#puts $eleFile "      26       233       266       270       240"
eleFile.append(quad26)
#puts $eleFile "      27       266       295       297       270"
eleFile.append(quad27)
#puts $eleFile "      28       295       324       330       297"
eleFile.append(quad28)
#puts $eleFile "      29       324       356       361       330"
eleFile.append(quad29)
#puts $eleFile "      30       356       388       393       361"
eleFile.append(quad30)
#puts $eleFile "      31       119       143       146       126"
eleFile.append(quad31)
#puts $eleFile "      32       143       162       170       146"
eleFile.append(quad32)
#puts $eleFile "      33       162       187       193       170"
eleFile.append(quad33)
#puts $eleFile "      34       187       214       217       193"
eleFile.append(quad34)
#puts $eleFile "      35       214       240       245       217"
eleFile.append(quad35)
#puts $eleFile "      36       240       270       273       245"
eleFile.append(quad36)
#puts $eleFile "      37       270       297       303       273"
eleFile.append(quad37)
#puts $eleFile "      38       297       330       334       303"
eleFile.append(quad38)
#puts $eleFile "      39       330       361       367       334"
eleFile.append(quad39)
#puts $eleFile "      40       361       393       397       367"
eleFile.append(quad40)
#puts $eleFile "      41       126       146       153       135"
eleFile.append(quad41)
#puts $eleFile "      42       146       170       176       153"
eleFile.append(quad42)
#puts $eleFile "      43       170       193       198       176"
eleFile.append(quad43)
#puts $eleFile "      44       193       217       227       198"
eleFile.append(quad44)
#puts $eleFile "      45       217       245       252       227"
eleFile.append(quad45)
#puts $eleFile "      46       245       273       280       252"
eleFile.append(quad46)
#puts $eleFile "      47       273       303       309       280"
eleFile.append(quad47)
#puts $eleFile "      48       303       334       339       309"
eleFile.append(quad48)
#puts $eleFile "      49       334       367       373       339"
eleFile.append(quad49)
#puts $eleFile "      50       367       397       404       373"
eleFile.append(quad50)
#puts $eleFile "      51       135       153       164       144"
eleFile.append(quad51)
#puts $eleFile "      52       153       176       189       164"
eleFile.append(quad52)
#puts $eleFile "      53       176       198       210       189"
eleFile.append(quad53)
#puts $eleFile "      54       198       227       237       210"
eleFile.append(quad54)
#puts $eleFile "      55       227       252       263       237"
eleFile.append(quad55)
#puts $eleFile "      56       252       280       292       263"
eleFile.append(quad56)
#puts $eleFile "      57       280       309       316       292"
eleFile.append(quad57)
#puts $eleFile "      58       309       339       348       316"
eleFile.append(quad58)
#puts $eleFile "      59       339       373       381       348"
eleFile.append(quad59)
#puts $eleFile "      60       373       404       407       381"
eleFile.append(quad60)
#puts $eleFile "      61       144       164       173       158"
eleFile.append(quad61)
#puts $eleFile "      62       164       189       196       173"
eleFile.append(quad62)
#puts $eleFile "      63       189       210       223       196"
eleFile.append(quad63)
#puts $eleFile "      64       210       237       248       223"
eleFile.append(quad64)
#puts $eleFile "      65       237       263       274       248"
eleFile.append(quad65)
#puts $eleFile "      66       263       292       301       274"
eleFile.append(quad66)
#puts $eleFile "      67       292       316       333       301"
eleFile.append(quad67)
#puts $eleFile "      68       316       348       362       333"
eleFile.append(quad68)
#puts $eleFile "      69       348       381       390       362"
eleFile.append(quad69)
#puts $eleFile "      70       381       407       416       390"
eleFile.append(quad70)
#puts $eleFile "      71       158       173       191       171"
eleFile.append(quad71)
#puts $eleFile "      72       173       196       212       191"
eleFile.append(quad72)
#puts $eleFile "      73       196       223       234       212"
eleFile.append(quad73)
#puts $eleFile "      74       223       248       254       234"
eleFile.append(quad74)
#puts $eleFile "      75       248       274       284       254"
eleFile.append(quad75)
#puts $eleFile "      76       274       301       312       284"
eleFile.append(quad76)
#puts $eleFile "      77       301       333       341       312"
eleFile.append(quad77)
#puts $eleFile "      78       333       362       377       341"
eleFile.append(quad78)
#puts $eleFile "      79       362       390       403       377"
eleFile.append(quad79)
#puts $eleFile "      80       390       416       423       403"
eleFile.append(quad80)
#puts $eleFile "      81       171       191       203       185"
eleFile.append(quad81)
#puts $eleFile "      82       191       212       225       203"
eleFile.append(quad82)
#puts $eleFile "      83       212       234       250       225"
eleFile.append(quad83)
#puts $eleFile "      84       234       254       275       250"
eleFile.append(quad84)
#puts $eleFile "      85       254       284       299       275"
eleFile.append(quad85)
#puts $eleFile "      86       284       312       329       299"
eleFile.append(quad86)
#puts $eleFile "      87       312       341       358       329"
eleFile.append(quad87)
#puts $eleFile "      88       341       377       384       358"
eleFile.append(quad88)
#puts $eleFile "      89       377       403       409       384"
eleFile.append(quad89)
#puts $eleFile "      90       403       423       432       409"
eleFile.append(quad90)
#puts $eleFile "      91       185       203       220       200"
eleFile.append(quad91)
#puts $eleFile "      92       203       225       243       220"
eleFile.append(quad92)
#puts $eleFile "      93       225       250       268       243"
eleFile.append(quad93)
#puts $eleFile "      94       250       275       290       268"
eleFile.append(quad94)
#puts $eleFile "      95       275       299       314       290"
eleFile.append(quad95)
#puts $eleFile "      96       299       329       343       314"
eleFile.append(quad96)
#puts $eleFile "      97       329       358       371       343"
eleFile.append(quad97)
#puts $eleFile "      98       358       384       401       371"
eleFile.append(quad98)
#puts $eleFile "      99       384       409       420       401"
eleFile.append(quad99)
#puts $eleFile "     100       409       432       436       420"
eleFile.append(quad100)
#puts $eleFile "     201        88        92        75        72"
eleFile.append(quad201)
#puts $eleFile "     202        92        93        79        75"
eleFile.append(quad202)
#puts $eleFile "     203        93        98        83        79"
eleFile.append(quad203)
#puts $eleFile "     204        98       105        84        83"
eleFile.append(quad204)
#puts $eleFile "     205       105       115        95        84"
eleFile.append(quad205)
#puts $eleFile "     206       115       125       107        95"
eleFile.append(quad206)
#puts $eleFile "     207       125       139       122       107"
eleFile.append(quad207)
#puts $eleFile "     208       139       150       134       122"
eleFile.append(quad208)
#puts $eleFile "     209       150       166       148       134"
eleFile.append(quad209)
#puts $eleFile "     210       166       182       167       148"
eleFile.append(quad210)
#puts $eleFile "     211       182       199       186       167"
eleFile.append(quad211)
#puts $eleFile "     212       199       221       202       186"
eleFile.append(quad212)
#puts $eleFile "     213       221       244       224       202"
eleFile.append(quad213)
#puts $eleFile "     214       244       267       249       224"
eleFile.append(quad214)
#puts $eleFile "     215       267       291       276       249"
eleFile.append(quad215)
#puts $eleFile "     216       291       315       298       276"
eleFile.append(quad216)
#puts $eleFile "     217       315       344       328       298"
eleFile.append(quad217)
#puts $eleFile "     218       344       372       359       328"
eleFile.append(quad218)
#puts $eleFile "     219       372       400       386       359"
eleFile.append(quad219)
#puts $eleFile "     220       400       421       410       386"
eleFile.append(quad220)
#puts $eleFile "     221        72        75        59        58"
eleFile.append(quad221)
#puts $eleFile "     222        75        79        64        59"
eleFile.append(quad222)
#puts $eleFile "     223        79        83        67        64"
eleFile.append(quad223)
#puts $eleFile "     224        83        84        70        67"
eleFile.append(quad224)
#puts $eleFile "     225        84        95        80        70"
eleFile.append(quad225)
#puts $eleFile "     226        95       107        89        80"
eleFile.append(quad226)
#puts $eleFile "     227       107       122       103        89"
eleFile.append(quad227)
#puts $eleFile "     228       122       134       118       103"
eleFile.append(quad228)
#puts $eleFile "     229       134       148       132       118"
eleFile.append(quad229)
#puts $eleFile "     230       148       167       149       132"
eleFile.append(quad230)
#puts $eleFile "     231       167       186       172       149"
eleFile.append(quad231)
#puts $eleFile "     232       186       202       192       172"
eleFile.append(quad232)
#puts $eleFile "     233       202       224       213       192"
eleFile.append(quad233)
#puts $eleFile "     234       224       249       235       213"
eleFile.append(quad234)
#puts $eleFile "     235       249       276       257       235"
eleFile.append(quad235)
#puts $eleFile "     236       276       298       283       257"
eleFile.append(quad236)
#puts $eleFile "     237       298       328       313       283"
eleFile.append(quad237)
#puts $eleFile "     238       328       359       342       313"
eleFile.append(quad238)
#puts $eleFile "     239       359       386       375       342"
eleFile.append(quad239)
#puts $eleFile "     240       386       410       402       375"
eleFile.append(quad240)
#puts $eleFile "     241        58        59        48        45"
eleFile.append(quad241)
#puts $eleFile "     242        59        64        51        48"
eleFile.append(quad242)
#puts $eleFile "     243        64        67        54        51"
eleFile.append(quad243)
#puts $eleFile "     244        67        70        61        54"
eleFile.append(quad244)
#puts $eleFile "     245        70        80        68        61"
eleFile.append(quad245)
#puts $eleFile "     246        80        89        77        68"
eleFile.append(quad246)
#puts $eleFile "     247        89       103        86        77"
eleFile.append(quad247)
#puts $eleFile "     248       103       118       102        86"
eleFile.append(quad248)
#puts $eleFile "     249       118       132       121       102"
eleFile.append(quad249)
#puts $eleFile "     250       132       149       140       121"
eleFile.append(quad250)
#puts $eleFile "     251       149       172       159       140"
eleFile.append(quad251)
#puts $eleFile "     252       172       192       174       159"
eleFile.append(quad252)
#puts $eleFile "     253       192       213       195       174"
eleFile.append(quad253)
#puts $eleFile "     254       213       235       222       195"
eleFile.append(quad254)
#puts $eleFile "     255       235       257       247       222"
eleFile.append(quad255)
#puts $eleFile "     256       257       283       272       247"
eleFile.append(quad256)
#puts $eleFile "     257       283       313       300       272"
eleFile.append(quad257)
#puts $eleFile "     258       313       342       332       300"
eleFile.append(quad258)
#puts $eleFile "     259       342       375       365       332"
eleFile.append(quad259)
#puts $eleFile "     260       375       402       391       365"
eleFile.append(quad260)
#puts $eleFile "     261        45        48        37        35"
eleFile.append(quad261)
#puts $eleFile "     262        48        51        39        37"
eleFile.append(quad262)
#puts $eleFile "     263        51        54        43        39"
eleFile.append(quad263)
#puts $eleFile "     264        54        61        49        43"
eleFile.append(quad264)
#puts $eleFile "     265        61        68        55        49"
eleFile.append(quad265)
#puts $eleFile "     266        68        77        65        55"
eleFile.append(quad266)
#puts $eleFile "     267        77        86        78        65"
eleFile.append(quad267)
#puts $eleFile "     268        86       102        90        78"
eleFile.append(quad268)
#puts $eleFile "     269       102       121       108        90"
eleFile.append(quad269)
#puts $eleFile "     270       121       140       124       108"
eleFile.append(quad270)
#puts $eleFile "     271       140       159       145       124"
eleFile.append(quad271)
#puts $eleFile "     272       159       174       165       145"
eleFile.append(quad272)
#puts $eleFile "     273       174       195       188       165"
eleFile.append(quad273)
#puts $eleFile "     274       195       222       211       188"
eleFile.append(quad274)
#puts $eleFile "     275       222       247       236       211"
eleFile.append(quad275)
#puts $eleFile "     276       247       272       262       236"
eleFile.append(quad276)
#puts $eleFile "     277       272       300       289       262"
eleFile.append(quad277)
#puts $eleFile "     278       300       332       317       289"
eleFile.append(quad278)
#puts $eleFile "     279       332       365       349       317"
eleFile.append(quad279)
#puts $eleFile "     280       365       391       382       349"
eleFile.append(quad280)
#puts $eleFile "     281        35        37        28        24"
eleFile.append(quad281)
#puts $eleFile "     282        37        39        30        28"
eleFile.append(quad282)
#puts $eleFile "     283        39        43        33        30"
eleFile.append(quad283)
#puts $eleFile "     284        43        49        41        33"
eleFile.append(quad284)
#puts $eleFile "     285        49        55        46        41"
eleFile.append(quad285)
#puts $eleFile "     286        55        65        56        46"
eleFile.append(quad286)
#puts $eleFile "     287        65        78        69        56"
eleFile.append(quad287)
#puts $eleFile "     288        78        90        81        69"
eleFile.append(quad288)
#puts $eleFile "     289        90       108        96        81"
eleFile.append(quad289)
#puts $eleFile "     290       108       124       114        96"
eleFile.append(quad290)
#puts $eleFile "     291       124       145       136       114"
eleFile.append(quad291)
#puts $eleFile "     292       145       165       155       136"
eleFile.append(quad292)
#puts $eleFile "     293       165       188       175       155"
eleFile.append(quad293)
#puts $eleFile "     294       188       211       201       175"
eleFile.append(quad294)
#puts $eleFile "     295       211       236       226       201"
eleFile.append(quad295)
#puts $eleFile "     296       236       262       251       226"
eleFile.append(quad296)
#puts $eleFile "     297       262       289       279       251"
eleFile.append(quad297)
#puts $eleFile "     298       289       317       310       279"
eleFile.append(quad298)
#puts $eleFile "     299       317       349       340       310"
eleFile.append(quad299)
#puts $eleFile "     300       349       382       376       340"
eleFile.append(quad300)
#puts $eleFile "     301        24        28        19        16"
eleFile.append(quad301)
#puts $eleFile "     302        28        30        21        19"
eleFile.append(quad302)
#puts $eleFile "     303        30        33        25        21"
eleFile.append(quad303)
#puts $eleFile "     304        33        41        31        25"
eleFile.append(quad304)
#puts $eleFile "     305        41        46        40        31"
eleFile.append(quad305)
#puts $eleFile "     306        46        56        50        40"
eleFile.append(quad306)
#puts $eleFile "     307        56        69        62        50"
eleFile.append(quad307)
#puts $eleFile "     308        69        81        71        62"
eleFile.append(quad308)
#puts $eleFile "     309        81        96        85        71"
eleFile.append(quad309)
#puts $eleFile "     310        96       114       104        85"
eleFile.append(quad310)
#puts $eleFile "     311       114       136       127       104"
eleFile.append(quad311)
#puts $eleFile "     312       136       155       147       127"
eleFile.append(quad312)
#puts $eleFile "     313       155       175       169       147"
eleFile.append(quad313)
#puts $eleFile "     314       175       201       194       169"
eleFile.append(quad314)
#puts $eleFile "     315       201       226       216       194"
eleFile.append(quad315)
#puts $eleFile "     316       226       251       246       216"
eleFile.append(quad316)
#puts $eleFile "     317       251       279       271       246"
eleFile.append(quad317)
#puts $eleFile "     318       279       310       305       271"
eleFile.append(quad318)
#puts $eleFile "     319       310       340       337       305"
eleFile.append(quad319)
#puts $eleFile "     320       340       376       366       337"
eleFile.append(quad320)
#puts $eleFile "     321        16        19        13        11"
eleFile.append(quad321)
#puts $eleFile "     322        19        21        14        13"
eleFile.append(quad322)
#puts $eleFile "     323        21        25        20        14"
eleFile.append(quad323)
#puts $eleFile "     324        25        31        26        20"
eleFile.append(quad324)
#puts $eleFile "     325        31        40        32        26"
eleFile.append(quad325)
#puts $eleFile "     326        40        50        42        32"
eleFile.append(quad326)
#puts $eleFile "     327        50        62        53        42"
eleFile.append(quad327)
#puts $eleFile "     328        62        71        66        53"
eleFile.append(quad328)
#puts $eleFile "     329        71        85        82        66"
eleFile.append(quad329)
#puts $eleFile "     330        85       104        97        82"
eleFile.append(quad330)
#puts $eleFile "     331       104       127       120        97"
eleFile.append(quad331)
#puts $eleFile "     332       127       147       142       120"
eleFile.append(quad332)
#puts $eleFile "     333       147       169       163       142"
eleFile.append(quad333)
#puts $eleFile "     334       169       194       190       163"
eleFile.append(quad334)
#puts $eleFile "     335       194       216       215       190"
eleFile.append(quad335)
#puts $eleFile "     336       216       246       238       215"
eleFile.append(quad336)
#puts $eleFile "     337       246       271       269       238"
eleFile.append(quad337)
#puts $eleFile "     338       271       305       296       269"
eleFile.append(quad338)
#puts $eleFile "     339       305       337       331       296"
eleFile.append(quad339)
#puts $eleFile "     340       337       366       360       331"
eleFile.append(quad340)
#puts $eleFile "     341        11        13         8         5"
eleFile.append(quad341)
#puts $eleFile "     342        13        14         9         8"
eleFile.append(quad342)
#puts $eleFile "     343        14        20        15         9"
eleFile.append(quad343)
#puts $eleFile "     344        20        26        22        15"
eleFile.append(quad344)
#puts $eleFile "     345        26        32        29        22"
eleFile.append(quad345)
#puts $eleFile "     346        32        42        38        29"
eleFile.append(quad346)
#puts $eleFile "     347        42        53        52        38"
eleFile.append(quad347)
#puts $eleFile "     348        53        66        63        52"
eleFile.append(quad348)
#puts $eleFile "     349        66        82        76        63"
eleFile.append(quad349)
#puts $eleFile "     350        82        97        94        76"
eleFile.append(quad350)
#puts $eleFile "     351        97       120       117        94"
eleFile.append(quad351)
#puts $eleFile "     352       120       142       137       117"
eleFile.append(quad352)
#puts $eleFile "     353       142       163       160       137"
eleFile.append(quad353)
#puts $eleFile "     354       163       190       183       160"
eleFile.append(quad354)
#puts $eleFile "     355       190       215       208       183"
eleFile.append(quad355)
#puts $eleFile "     356       215       238       232       208"
eleFile.append(quad356)
#puts $eleFile "     357       238       269       265       232"
eleFile.append(quad357)
#puts $eleFile "     358       269       296       294       265"
eleFile.append(quad358)
#puts $eleFile "     359       296       331       323       294"
eleFile.append(quad359)
#puts $eleFile "     360       331       360       357       323"
eleFile.append(quad360)
#puts $eleFile "     361         5         8         4         3"
eleFile.append(quad361)
#puts $eleFile "     362         8         9         7         4"
eleFile.append(quad362)
#puts $eleFile "     363         9        15        12         7"
eleFile.append(quad363)
#puts $eleFile "     364        15        22        18        12"
eleFile.append(quad364)
#puts $eleFile "     365        22        29        27        18"
eleFile.append(quad365)
#puts $eleFile "     366        29        38        36        27"
eleFile.append(quad366)
#puts $eleFile "     367        38        52        47        36"
eleFile.append(quad367)
#puts $eleFile "     368        52        63        60        47"
eleFile.append(quad368)
#puts $eleFile "     369        63        76        74        60"
eleFile.append(quad369)
#puts $eleFile "     370        76        94        91        74"
eleFile.append(quad370)
#puts $eleFile "     371        94       117       111        91"
eleFile.append(quad371)
#puts $eleFile "     372       117       137       133       111"
eleFile.append(quad372)
#puts $eleFile "     373       137       160       156       133"
eleFile.append(quad373)
#puts $eleFile "     374       160       183       179       156"
eleFile.append(quad374)
#puts $eleFile "     375       183       208       206       179"
eleFile.append(quad375)
#puts $eleFile "     376       208       232       230       206"
eleFile.append(quad376)
#puts $eleFile "     377       232       265       258       230"
eleFile.append(quad377)
#puts $eleFile "     378       265       294       288       258"
eleFile.append(quad378)
#puts $eleFile "     379       294       323       320       288"
eleFile.append(quad379)
#puts $eleFile "     380       323       357       354       320"
eleFile.append(quad380)
#puts $eleFile "     381         3         4         2         1"
eleFile.append(quad381)
#puts $eleFile "     382         4         7         6         2"
eleFile.append(quad382)
#puts $eleFile "     383         7        12        10         6"
eleFile.append(quad383)
#puts $eleFile "     384        12        18        17        10"
eleFile.append(quad384)
#puts $eleFile "     385        18        27        23        17"
eleFile.append(quad385)
#puts $eleFile "     386        27        36        34        23"
eleFile.append(quad386)
#puts $eleFile "     387        36        47        44        34"
eleFile.append(quad387)
#puts $eleFile "     388        47        60        57        44"
eleFile.append(quad388)
#puts $eleFile "     389        60        74        73        57"
eleFile.append(quad389)
#puts $eleFile "     390        74        91        87        73"
eleFile.append(quad390)
#puts $eleFile "     391        91       111       110        87"
eleFile.append(quad391)
#puts $eleFile "     392       111       133       129       110"
eleFile.append(quad392)
#puts $eleFile "     393       133       156       154       129"
eleFile.append(quad393)
#puts $eleFile "     394       156       179       177       154"
eleFile.append(quad394)
#puts $eleFile "     395       179       206       204       177"
eleFile.append(quad395)
#puts $eleFile "     396       206       230       228       204"
eleFile.append(quad396)
#puts $eleFile "     397       230       258       255       228"
eleFile.append(quad397)
#puts $eleFile "     398       258       288       287       255"
eleFile.append(quad398)
#puts $eleFile "     399       288       320       318       287"
eleFile.append(quad399)
#puts $eleFile "     400       320       354       351       318"
eleFile.append(quad400)
#close $eleFile
#-----------------------------------------------------------------------------
#  6. CREATE BEAM NODES AND FIXITIES
#-----------------------------------------------------------------------------
#model BasicBuilder -ndm 2 -ndf 3
nodes= modelSpace.getNodeHandler()
nodes.numDOFs= 3

# define beam nodes
#node       99       0.000      0.250
n99= modelSpace.newNodeXY( 0.000, 0.250)
#node      100       0.000     -0.250
n100= modelSpace.newNodeXY( 0.000, -0.250)
#node      101       0.000      0.750
n101= modelSpace.newNodeXY( 0.000, 0.750)
#node      106       0.000      1.250
n106= modelSpace.newNodeXY( 0.000, 1.250)
#node      113       0.000      1.750
n113= modelSpace.newNodeXY( 0.000, 1.750)
#node      123       0.000      2.250
n123= modelSpace.newNodeXY( 0.000, 2.250)
#node      128       0.000      2.750
n128= modelSpace.newNodeXY( 0.000, 2.750)
#node      141       0.000      3.250
n141= modelSpace.newNodeXY( 0.000, 3.250)
#node      151       0.000      3.750
n151= modelSpace.newNodeXY( 0.000, 3.750)
#node      168       0.000      4.250
n168= modelSpace.newNodeXY( 0.000, 4.250)
#node      184       0.000      4.750
n184= modelSpace.newNodeXY( 0.000, 4.750)
#node      197       0.000      5.250
n197= modelSpace.newNodeXY( 0.000, 5.250)
#node      219       0.000      5.750
n219= modelSpace.newNodeXY( 0.000, 5.750)
#node      242       0.000      6.250
n242= modelSpace.newNodeXY( 0.000, 6.250)
#node      264       0.000      6.750
n264= modelSpace.newNodeXY( 0.000, 6.750)
#node      285       0.000      7.250
n285= modelSpace.newNodeXY( 0.000, 7.250)
#node      311       0.000      7.750
n311= modelSpace.newNodeXY( 0.000, 7.750)
#node      338       0.000      8.250
n338= modelSpace.newNodeXY( 0.000, 8.250)
#node      368       0.000      8.750
n368= modelSpace.newNodeXY( 0.000, 8.750)
#node      396       0.000      9.250
n396= modelSpace.newNodeXY( 0.000, 9.250)
#node      417       0.000      9.750
n417= modelSpace.newNodeXY( 0.000, 9.750)
#node      435       0.000     10.250
n435= modelSpace.newNodeXY( 0.000, 10.250)
#puts "Finished creating all -ndf 3 beam nodes..."
lmsg.log("Finished creating all beam nodes...")
# create list of beam nodes and locations for post-processing
#set bNodeInfo [open NodesInfo3.dat w]
bNodeInfo= list()

#puts $bNodeInfo "      99       0.000      0.250"
bNodeInfo.append(n99)
#puts $bNodeInfo "     100       0.000     -0.250"
bNodeInfo.append(n100)
#puts $bNodeInfo "     101       0.000      0.750"
bNodeInfo.append(n101)
#puts $bNodeInfo "     106       0.000      1.250"
bNodeInfo.append(n106)
#puts $bNodeInfo "     113       0.000      1.750"
bNodeInfo.append(n113)
#puts $bNodeInfo "     123       0.000      2.250"
bNodeInfo.append(n123)
#puts $bNodeInfo "     128       0.000      2.750"
bNodeInfo.append(n128)
#puts $bNodeInfo "     141       0.000      3.250"
bNodeInfo.append(n141)
#puts $bNodeInfo "     151       0.000      3.750"
bNodeInfo.append(n151)
#puts $bNodeInfo "     168       0.000      4.250"
bNodeInfo.append(n168)
#puts $bNodeInfo "     184       0.000      4.750"
bNodeInfo.append(n184)
#puts $bNodeInfo "     197       0.000      5.250"
bNodeInfo.append(n197)
#puts $bNodeInfo "     219       0.000      5.750"
bNodeInfo.append(n219)
#puts $bNodeInfo "     242       0.000      6.250"
bNodeInfo.append(n242)
#puts $bNodeInfo "     264       0.000      6.750"
bNodeInfo.append(n264)
#puts $bNodeInfo "     285       0.000      7.250"
bNodeInfo.append(n285)
#puts $bNodeInfo "     311       0.000      7.750"
bNodeInfo.append(n311)
#puts $bNodeInfo "     338       0.000      8.250"
bNodeInfo.append(n338)
#puts $bNodeInfo "     368       0.000      8.750"
bNodeInfo.append(n368)
#puts $bNodeInfo "     396       0.000      9.250"
bNodeInfo.append(n396)
#puts $bNodeInfo "     417       0.000      9.750"
bNodeInfo.append(n417)
#puts $bNodeInfo "     435       0.000     10.250"
bNodeInfo.append(n435)
#close $bNodeInfo
#

# fix the base node of the sheetpile in the vertical direction
#fix   100   0 1 0
modelSpace.fixNode('F0F', n100.tag)
#puts "Finished creating all -ndf 3 boundary conditions..."
lmsg.log("Finished creating all boundary conditions...")

#-----------------------------------------------------------------------------
#  7. CREATE BEAM MATERIALS
#-----------------------------------------------------------------------------
#

# beam properties
#set thick      0.5
thick = 0.5
#set area       0.5
area = 0.5
#set I          9.75e-4
I = 9.75e-4
#set beamE      200000000
beamE = 200000000
#set numIntPts  3
numIntPts = 3
#set transTag   1
transTag = 1
#set secTag     1
secTag = 1


# geometric transformation
lin= preprocessor.getTransfCooHandler.newLinearCrdTransf2d("lin")
modelSpace.setDefaultCoordTransf(lin)


# beam section
#section Elastic  $secTag $beamE $area $I
scc= typical_materials.defElasticSection2d(preprocessor, "scc",A= area,E= beamE,I= I)
modelSpace.setDefaultMaterial(scc)


#puts "Finished creating all beam materials..."
lmsg.log("Finished creating all beam materials...")
#-----------------------------------------------------------------------------
#  8. CREATE BEAM ELEMENTS
#-----------------------------------------------------------------------------

#element dispBeamColumn 401 100 99  $numIntPts $secTag $transTag
beam401= modelSpace.newElement('ElasticBeam2d', [n100.tag, n99.tag])
#element dispBeamColumn 402 99  101 $numIntPts $secTag $transTag
beam402= modelSpace.newElement('ElasticBeam2d', [n99.tag, n101.tag])
#element dispBeamColumn 403 101 106 $numIntPts $secTag $transTag
beam403= modelSpace.newElement('ElasticBeam2d', [n101.tag, n106.tag])
#element dispBeamColumn 404 106 113 $numIntPts $secTag $transTag
beam404= modelSpace.newElement('ElasticBeam2d', [n106.tag, n113.tag])
#element dispBeamColumn 405 113 123 $numIntPts $secTag $transTag
beam405= modelSpace.newElement('ElasticBeam2d', [n113.tag, n123.tag])
#element dispBeamColumn 406 123 128 $numIntPts $secTag $transTag
beam406= modelSpace.newElement('ElasticBeam2d', [n123.tag, n128.tag])
#element dispBeamColumn 407 128 141 $numIntPts $secTag $transTag
beam407= modelSpace.newElement('ElasticBeam2d', [n128.tag, n141.tag])
#element dispBeamColumn 408 141 151 $numIntPts $secTag $transTag
beam408= modelSpace.newElement('ElasticBeam2d', [n141.tag, n151.tag])
#element dispBeamColumn 409 151 168 $numIntPts $secTag $transTag
beam409= modelSpace.newElement('ElasticBeam2d', [n151.tag, n168.tag])
#element dispBeamColumn 410 168 184 $numIntPts $secTag $transTag
beam410= modelSpace.newElement('ElasticBeam2d', [n168.tag, n184.tag])
#element dispBeamColumn 411 184 197 $numIntPts $secTag $transTag
beam411= modelSpace.newElement('ElasticBeam2d', [n184.tag, n197.tag])
#element dispBeamColumn 412 197 219 $numIntPts $secTag $transTag
beam412= modelSpace.newElement('ElasticBeam2d', [n197.tag, n219.tag])
#element dispBeamColumn 413 219 242 $numIntPts $secTag $transTag
beam413= modelSpace.newElement('ElasticBeam2d', [n219.tag, n242.tag])
#element dispBeamColumn 414 242 264 $numIntPts $secTag $transTag
beam414= modelSpace.newElement('ElasticBeam2d', [n242.tag, n264.tag])
#element dispBeamColumn 415 264 285 $numIntPts $secTag $transTag
beam415= modelSpace.newElement('ElasticBeam2d', [n264.tag, n285.tag])
#element dispBeamColumn 416 285 311 $numIntPts $secTag $transTag
beam416= modelSpace.newElement('ElasticBeam2d', [n285.tag, n311.tag])
#element dispBeamColumn 417 311 338 $numIntPts $secTag $transTag
beam417= modelSpace.newElement('ElasticBeam2d', [n311.tag, n338.tag])
#element dispBeamColumn 418 338 368 $numIntPts $secTag $transTag
beam418= modelSpace.newElement('ElasticBeam2d', [n338.tag, n368.tag])
#element dispBeamColumn 419 368 396 $numIntPts $secTag $transTag
beam419= modelSpace.newElement('ElasticBeam2d', [n368.tag, n396.tag])
#element dispBeamColumn 420 396 417 $numIntPts $secTag $transTag
beam420= modelSpace.newElement('ElasticBeam2d', [n396.tag, n417.tag])
#element dispBeamColumn 421 417 435 $numIntPts $secTag $transTag
beam421= modelSpace.newElement('ElasticBeam2d', [n417.tag, n435.tag])
#puts "Finished creating all beam elements..."
lmsg.log("Finished creating all beam elements...")

# create list of beam elements with connectivities for post-processing
#set beamInfo [open beamElementInfo.dat w]
beamInfo= list()

#puts $beamInfo " 401 100 99 "
beamInfo.append(beam401)
#puts $beamInfo " 402 99 101 "
beamInfo.append(beam402)
#puts $beamInfo " 403 101 106 "
beamInfo.append(beam403)
#puts $beamInfo " 404 106 113 "
beamInfo.append(beam404)
#puts $beamInfo " 405 113 123 "
beamInfo.append(beam405)
#puts $beamInfo " 406 123 128 "
beamInfo.append(beam406)
#puts $beamInfo " 407 128 141 "
beamInfo.append(beam407)
#puts $beamInfo " 408 141 151 "
beamInfo.append(beam408)
#puts $beamInfo " 409 151 168 "
beamInfo.append(beam409)
#puts $beamInfo " 410 168 184 "
beamInfo.append(beam410)
#puts $beamInfo " 411 184 197 "
beamInfo.append(beam411)
#puts $beamInfo " 412 197 219 "
beamInfo.append(beam412)
#puts $beamInfo " 413 219 242 "
beamInfo.append(beam413)
#puts $beamInfo " 414 242 264 "
beamInfo.append(beam414)
#puts $beamInfo " 415 264 285 "
beamInfo.append(beam415)
#puts $beamInfo " 416 285 311 "
beamInfo.append(beam416)
#puts $beamInfo " 417 311 338 "
beamInfo.append(beam417)
#puts $beamInfo " 418 338 368 "
beamInfo.append(beam418)
#puts $beamInfo " 419 368 396 "
beamInfo.append(beam419)
#puts $beamInfo " 420 396 417 "
beamInfo.append(beam420)
#puts $beamInfo " 421 417 435 "
beamInfo.append(beam421)


#-----------------------------------------------------------------------------
#  9. CREATE CONTACT MATERIAL FOR BEAM CONTACT ELEMENTS
#-----------------------------------------------------------------------------

# two-dimensional contact material
#nDMaterial ContactMaterial2D  2  0.1 1000.0 0.0 0.0
contactMat= typical_materials.defContactMaterial2D(preprocessor= preprocessor, name= 'contactMat', mu= 0.1, G= 1000.0, c= 0.0, t= 0.0)
#

#puts "Finished creating all contact materials..."
lmsg.log("Finished creating all contact materials...")

#-----------------------------------------------------------------------------
#  10. CREATE BEAM CONTACT ELEMENTS
#-----------------------------------------------------------------------------
#

# set gap and force tolerances for beam contact elements
#set gapTol    1.0e-10
gapTol = 1.0e-10
#set forceTol  1.0e-10
forceTol = 1.0e-10

# define beam contact elements
#element BeamContact2D 1001  100  99  88 1001  2 $thick $gapTol $forceTol
modelSpace.setDefaultMaterial(contactMat)
# define beam contact elements
#element BeamContact2D 1001  100  99  88 1001  2 $thick $gapTol $forceTol
contact1001= modelSpace.newElement('BeamContact2d', [100, 99, 88, lagrangeNodes[1001].tag]); contact1001.gapTolerance= gapTol; contact1001.width= thick; contact1001.forceTolerance= forceTol
#element BeamContact2D 1002  100  99 109 1002  2 $thick $gapTol $forceTol
contact1002= modelSpace.newElement('BeamContact2d', [100, 99, 109, lagrangeNodes[1002].tag]); contact1002.width= thick; contact1002.gapTolerance= gapTol; contact1002.forceTolerance= forceTol 
#element BeamContact2D 1003   99 101  92 1003  2 $thick $gapTol $forceTol
contact1003= modelSpace.newElement('BeamContact2d', [99, 101, 92, lagrangeNodes[1003].tag]); contact1003.width= thick; contact1003.gapTolerance= gapTol; contact1003.forceTolerance= forceTol 
#element BeamContact2D 1004   99 101 112 1004  2 $thick $gapTol $forceTol
contact1004= modelSpace.newElement('BeamContact2d', [99, 101, 112, lagrangeNodes[1004].tag]); contact1004.width= thick; contact1004.gapTolerance= gapTol; contact1004.forceTolerance= forceTol 
#element BeamContact2D 1005  101 106  93 1005  2 $thick $gapTol $forceTol
contact1005= modelSpace.newElement('BeamContact2d', [101, 106, 93, lagrangeNodes[1005].tag]); contact1005.width= thick; contact1005.gapTolerance= gapTol; contact1005.forceTolerance= forceTol 
#element BeamContact2D 1006  101 106 116 1006  2 $thick $gapTol $forceTol
contact1006= modelSpace.newElement('BeamContact2d', [101, 106, 116, lagrangeNodes[1006].tag]); contact1006.width= thick; contact1006.gapTolerance= gapTol; contact1006.forceTolerance= forceTol 
#element BeamContact2D 1007  106 113  98 1007  2 $thick $gapTol $forceTol
contact1007= modelSpace.newElement('BeamContact2d', [106, 113, 98, lagrangeNodes[1007].tag]); contact1007.width= thick; contact1007.gapTolerance= gapTol; contact1007.forceTolerance= forceTol 
#element BeamContact2D 1008  106 113 119 1008  2 $thick $gapTol $forceTol
contact1008= modelSpace.newElement('BeamContact2d', [106, 113, 119, lagrangeNodes[1008].tag]); contact1008.width= thick; contact1008.gapTolerance= gapTol; contact1008.forceTolerance= forceTol 
#element BeamContact2D 1009  113 123 105 1009  2 $thick $gapTol $forceTol
contact1009= modelSpace.newElement('BeamContact2d', [113, 123, 105, lagrangeNodes[1009].tag]); contact1009.width= thick; contact1009.gapTolerance= gapTol; contact1009.forceTolerance= forceTol 
#element BeamContact2D 1010  113 123 126 1010  2 $thick $gapTol $forceTol
contact1010= modelSpace.newElement('BeamContact2d', [113, 123, 126, lagrangeNodes[1010].tag]); contact1010.width= thick; contact1010.gapTolerance= gapTol; contact1010.forceTolerance= forceTol 
#element BeamContact2D 1011  123 128 115 1011  2 $thick $gapTol $forceTol
contact1011= modelSpace.newElement('BeamContact2d', [123, 128, 115, lagrangeNodes[1011].tag]); contact1011.width= thick; contact1011.gapTolerance= gapTol; contact1011.forceTolerance= forceTol 
#element BeamContact2D 1012  123 128 135 1012  2 $thick $gapTol $forceTol
contact1012= modelSpace.newElement('BeamContact2d', [123, 128, 135, lagrangeNodes[1012].tag]); contact1012.width= thick; contact1012.gapTolerance= gapTol; contact1012.forceTolerance= forceTol 
#element BeamContact2D 1013  128 141 125 1013  2 $thick $gapTol $forceTol
contact1013= modelSpace.newElement('BeamContact2d', [128, 141, 125, lagrangeNodes[1013].tag]); contact1013.width= thick; contact1013.gapTolerance= gapTol; contact1013.forceTolerance= forceTol 
#element BeamContact2D 1014  128 141 144 1014  2 $thick $gapTol $forceTol
contact1014= modelSpace.newElement('BeamContact2d', [128, 141, 144, lagrangeNodes[1014].tag]); contact1014.width= thick; contact1014.gapTolerance= gapTol; contact1014.forceTolerance= forceTol 
#element BeamContact2D 1015  141 151 139 1015  2 $thick $gapTol $forceTol
contact1015= modelSpace.newElement('BeamContact2d', [141, 151, 139, lagrangeNodes[1015].tag]); contact1015.width= thick; contact1015.gapTolerance= gapTol; contact1015.forceTolerance= forceTol 
#element BeamContact2D 1016  141 151 158 1016  2 $thick $gapTol $forceTol
contact1016= modelSpace.newElement('BeamContact2d', [141, 151, 158, lagrangeNodes[1016].tag]); contact1016.width= thick; contact1016.gapTolerance= gapTol; contact1016.forceTolerance= forceTol 
#element BeamContact2D 1017  151 168 150 1017  2 $thick $gapTol $forceTol
print('A1')
contact1017= modelSpace.newElement('BeamContact2d', [151, 168, 150, lagrangeNodes[1017].tag]); contact1017.width= thick; contact1017.gapTolerance= gapTol; contact1017.forceTolerance= forceTol 
#element BeamContact2D 1018  151 168 171 1018  2 $thick $gapTol $forceTol
print('A2')
contact1018= modelSpace.newElement('BeamContact2d', [151, 168, 171, lagrangeNodes[1018].tag]); contact1018.width= thick; contact1018.gapTolerance= gapTol; contact1018.forceTolerance= forceTol 
#element BeamContact2D 1019  168 184 166 1019  2 $thick $gapTol $forceTol
contact1019= modelSpace.newElement('BeamContact2d', [168, 184, 166, lagrangeNodes[1019].tag]); contact1019.width= thick; contact1019.gapTolerance= gapTol; contact1019.forceTolerance= forceTol 
#element BeamContact2D 1020  168 184 185 1020  2 $thick $gapTol $forceTol
contact1020= modelSpace.newElement('BeamContact2d', [168, 184, 185, lagrangeNodes[1020].tag]); contact1020.width= thick; contact1020.gapTolerance= gapTol; contact1020.forceTolerance= forceTol 
#element BeamContact2D 1021  184 197 182 1021  2 $thick $gapTol $forceTol
contact1021= modelSpace.newElement('BeamContact2d', [184, 197, 182, lagrangeNodes[1021].tag]); contact1021.width= thick; contact1021.gapTolerance= gapTol; contact1021.forceTolerance= forceTol 
#element BeamContact2D 1022  184 197 200 1022  2 $thick $gapTol $forceTol
contact1022= modelSpace.newElement('BeamContact2d', [184, 197, 200, lagrangeNodes[1022].tag]); contact1022.width= thick; contact1022.gapTolerance= gapTol; contact1022.forceTolerance= forceTol 
#element BeamContact2D 1023  197 219 199 1023  2 $thick $gapTol $forceTol
print('B1')
contact1023= modelSpace.newElement('BeamContact2d', [197, 219, 199, lagrangeNodes[1023].tag]); contact1023.width= thick; contact1023.gapTolerance= gapTol; contact1023.forceTolerance= forceTol 
#element BeamContact2D 1024  197 219 218 1024  2 $thick $gapTol $forceTol
print('B2')
contact1024= modelSpace.newElement('BeamContact2d', [197, 219, 218, lagrangeNodes[1024].tag]); contact1024.width= thick; contact1024.gapTolerance= gapTol; contact1024.forceTolerance= forceTol 
#element BeamContact2D 1025  219 242 221 1025  2 $thick $gapTol $forceTol
contact1025= modelSpace.newElement('BeamContact2d', [219, 242, 221, lagrangeNodes[1025].tag]); contact1025.width= thick; contact1025.gapTolerance= gapTol; contact1025.forceTolerance= forceTol 
#element BeamContact2D 1026  219 242 241 1026  2 $thick $gapTol $forceTol
contact1026= modelSpace.newElement('BeamContact2d', [219, 242, 241, lagrangeNodes[1026].tag]); contact1026.width= thick; contact1026.gapTolerance= gapTol; contact1026.forceTolerance= forceTol 
#element BeamContact2D 1027  242 264 244 1027  2 $thick $gapTol $forceTol
contact1027= modelSpace.newElement('BeamContact2d', [242, 264, 244, lagrangeNodes[1027].tag]); contact1027.width= thick; contact1027.gapTolerance= gapTol; contact1027.forceTolerance= forceTol 
#element BeamContact2D 1028  242 264 260 1028  2 $thick $gapTol $forceTol
contact1028= modelSpace.newElement('BeamContact2d', [242, 264, 260, lagrangeNodes[1028].tag]); contact1028.width= thick; contact1028.gapTolerance= gapTol; contact1028.forceTolerance= forceTol 
#element BeamContact2D 1029  264 285 267 1029  2 $thick $gapTol $forceTol
contact1029= modelSpace.newElement('BeamContact2d', [264, 285, 267, lagrangeNodes[1029].tag]); contact1029.width= thick; contact1029.gapTolerance= gapTol; contact1029.forceTolerance= forceTol 
#element BeamContact2D 1030  264 285 281 1030  2 $thick $gapTol $forceTol
contact1030= modelSpace.newElement('BeamContact2d', [264, 285, 281, lagrangeNodes[1030].tag]); contact1030.width= thick; contact1030.gapTolerance= gapTol; contact1030.forceTolerance= forceTol 
#element BeamContact2D 1031  285 311 291 1031  2 $thick $gapTol $forceTol
print('C1')
contact1031= modelSpace.newElement('BeamContact2d', [285, 311, 291, lagrangeNodes[1031].tag]); contact1031.width= thick; contact1031.gapTolerance= gapTol; contact1031.forceTolerance= forceTol 
#element BeamContact2D 1032  285 311 308 1032  2 $thick $gapTol $forceTol
print('C2')
contact1032= modelSpace.newElement('BeamContact2d', [285, 311, 308, lagrangeNodes[1032].tag]); contact1032.width= thick; contact1032.gapTolerance= gapTol; contact1032.forceTolerance= forceTol 
#element BeamContact2D 1033  311 338 315 1033  2 $thick $gapTol $forceTol
contact1033= modelSpace.newElement('BeamContact2d', [311, 338, 315, lagrangeNodes[1033].tag]); contact1033.width= thick; contact1033.gapTolerance= gapTol; contact1033.forceTolerance= forceTol 
#element BeamContact2D 1034  311 338 336 1034  2 $thick $gapTol $forceTol
contact1034= modelSpace.newElement('BeamContact2d', [311, 338, 336, lagrangeNodes[1034].tag]); contact1034.width= thick; contact1034.gapTolerance= gapTol; contact1034.forceTolerance= forceTol 
#element BeamContact2D 1035  338 368 344 1035  2 $thick $gapTol $forceTol
contact1035= modelSpace.newElement('BeamContact2d', [338, 368, 344, lagrangeNodes[1035].tag]); contact1035.width= thick; contact1035.gapTolerance= gapTol; contact1035.forceTolerance= forceTol 
#element BeamContact2D 1036  338 368 363 1036  2 $thick $gapTol $forceTol
contact1036= modelSpace.newElement('BeamContact2d', [338, 368, 363, lagrangeNodes[1036].tag]); contact1036.width= thick; contact1036.gapTolerance= gapTol; contact1036.forceTolerance= forceTol 
#element BeamContact2D 1037  368 396 372 1037  2 $thick $gapTol $forceTol
contact1037= modelSpace.newElement('BeamContact2d', [368, 396, 372, lagrangeNodes[1037].tag]); contact1037.width= thick; contact1037.gapTolerance= gapTol; contact1037.forceTolerance= forceTol 
#element BeamContact2D 1038  368 396 387 1038  2 $thick $gapTol $forceTol
contact1038= modelSpace.newElement('BeamContact2d', [368, 396, 387, lagrangeNodes[1038].tag]); contact1038.width= thick; contact1038.gapTolerance= gapTol; contact1038.forceTolerance= forceTol 
#element BeamContact2D 1039  396 417 400 1039  2 $thick $gapTol $forceTol
contact1039= modelSpace.newElement('BeamContact2d', [396, 417, 400, lagrangeNodes[1039].tag]); contact1039.width= thick; contact1039.gapTolerance= gapTol; contact1039.forceTolerance= forceTol 
#element BeamContact2D 1040  396 417 412 1040  2 $thick $gapTol $forceTol
contact1040= modelSpace.newElement('BeamContact2d', [396, 417, 412, lagrangeNodes[1040].tag]); contact1040.width= thick; contact1040.gapTolerance= gapTol; contact1040.forceTolerance= forceTol 
#element BeamContact2D 1041  417 435 421 1041  2 $thick $gapTol $forceTol
contact1041= modelSpace.newElement('BeamContact2d', [417, 435, 421, lagrangeNodes[1041].tag]); contact1041.width= thick; contact1041.gapTolerance= gapTol; contact1041.forceTolerance= forceTol 
#element BeamContact2D 1042  417 435 430 1042  2 $thick $gapTol $forceTol
contact1042= modelSpace.newElement('BeamContact2d', [417, 435, 430, lagrangeNodes[1042].tag]); contact1042.width= thick; contact1042.gapTolerance= gapTol; contact1042.forceTolerance= forceTol 
#puts "Finished creating all beam-contact elements..."
lmsg.log("Finished creating all beam-contact elements...")#
