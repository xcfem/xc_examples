# -*- coding: utf-8 -*-
''' Tabulate: example of use.'''

from __future__ import division
from __future__ import print_function

# LaTeX output
from tabulate import tabulate

__author__= "Luis Claudio Pérez Tato (LCPT"
__copyright__= "Copyright 2022, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"


# Results dictionary (normally created by XC).
results= [["Roll Number","Student name","Marks"],
            [1,"Sasha",34],
            [2,"Richard",36],
            [3,"Judy",20],
            [4,"Lori",39],
            [5,"Maggie",40]]

print('LaTeX output:')
print(tabulate(results, headers='firstrow', tablefmt='latex'))
