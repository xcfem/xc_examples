# -*- coding: utf-8 -*-
from materials.ec2 import EC2_materials
import math

# Data
concr=EC2_materials.C30 # type of concrete 
concr.cemType='N'   #cement class
RH=70                   #ambient relative humidity(%)

Ac=10*0.25 # area of concrete cross-section [m2]
u=2*(10+0.25)   # perimenter of the concrete cross-section exposed to drying [m]
ts=1       # age of concrete [days] when drying shrinkage begins
tinf=100*365 # age of the concrete t infinite

t_calc=[t for t in range(1,90,14)]
t_calc+=[t for t in range(100,1000,100)] # calculation at concrete ages [days]
t_calc+=[tinf]
#  End data
h0=2*Ac/u 
total_drying_shr=concr.getShrEpscd(tinf,ts,RH,h0) 
drying_shr=[concr.getShrEpscd(t,ts,RH,h0) for t in t_calc]
drying_shr_perc=[drShr/total_drying_shr*100 for drShr in drying_shr]

total_autog_shr=concr.getShrEpsca(tinf)
autog_shr=[concr.getShrEpsca(t) for t in t_calc]
autog_shr_perc=[autShr/total_autog_shr*100 for autShr in autog_shr]

total_combined_shr=total_drying_shr+total_autog_shr
combined_shr=[drying_shr[i]+autog_shr[i] for i in range(len(t_calc))]
combined_shr_perc=[combinedShr/total_combined_shr*100 for combinedShr in combined_shr]

table_drying=str()
table_autog=str()
table_total=str()

for i in range(len(t_calc)):
    table_drying+=str(t_calc[i]) + ' & ' + str(round(drying_shr[i]*1e3,4)) + ' & ' + str(round(drying_shr_perc[i],1)) + ' \\\\ \n'
    table_autog+=str(t_calc[i]) + ' & ' + str(round(autog_shr[i]*1e3,4)) + ' & ' + str(round(autog_shr_perc[i],1)) + ' \\\\ \n'
    table_total+=str(t_calc[i]) + ' & ' + str(round(combined_shr[i]*1e3,4)) + ' & ' + str(round(combined_shr_perc[i],1)) + ' \\\\ \n'



   

