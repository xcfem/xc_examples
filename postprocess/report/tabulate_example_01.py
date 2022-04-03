# -*- coding: utf-8 -*-
''' Tabulate: example of use.'''

from __future__ import division
from __future__ import print_function

# LaTeX output
import pandas as pd
from tabulate import tabulate

__author__= "Luis Claudio Pérez Tato (LCPT"
__copyright__= "Copyright 2022, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"


# Results dictionary (normally created by XC).
results= {'LC1': {'Mzd': 1391.4318318392045, 'CL': 1.0, 'bendingCF': 0.3355785487268503, 'Vyd': 1579.377788693762, 'shearCF': 0.2813839619030194}, 'LC2': {'Mzd': 2603.80542201508, 'CL': 1.0, 'bendingCF': 0.6825790532838286, 'Vyd': 2955.51126221916, 'shearCF': 0.5265576573037858}, 'LC3': {'Mzd': 393.5454719379738, 'CL': 1.0, 'bendingCF': 0.07415103328108452, 'Vyd': 446.70314635411324, 'shearCF': 0.07958520248636769}, 'LC4': {'Mzd': 1618.184387624687, 'CL': 1.0, 'bendingCF': 0.30489499419421856, 'Vyd': 1836.758669267522, 'shearCF': 0.3272392679687267}}

print('LaTeX output:')
df = pd.DataFrame(results)
print(tabulate(df.T, headers='keys', tablefmt='latex'))
