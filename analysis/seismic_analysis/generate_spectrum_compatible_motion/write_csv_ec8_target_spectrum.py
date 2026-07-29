import numpy as np
from actions.quake import ec8_seismic as accsis
import matplotlib.pyplot as plt


# Datos Viaducto Manzanil
nPeriods=250
periods=np.linspace(0.005, 4,nPeriods)
a_gR=0.239 # horizontal acceleration (g) in soil type A
K=1 # contriburtion coefficient (Azores-Gibraltar)
impClass='III' # importance class
soilTyp='B' # soil type according to AN/UNE-EN 1998-1, table AN/1 (Table 3.1)
v_s30=575 # [m/s] average speed (m/s) of the shear waves in the first 30 m of the ground [AN/UNE-EN 1998-1, tabla AN/1 (Tabla 3.1)]
# end data

# Horizontal spectrum
Sa_horiz= accsis.ec8_like_target_horiz_spectrum_type1(periods, a_gR,K,soilTyp,v_s30,impClass,eta=1)
# Vertical spectrum
Sa_vert= accsis.ec8_like_target_vertical_spectrum_type1(periods, a_gR,K,soilTyp,v_s30,impClass,eta=1)
'''
# Write csv file period - horizontal accelerations
f=open('target_horiz_spectrum.csv','w')
for T, a in zip(periods,Sa_horiz):
    f.write(str(T)+','+str(a)+'\n')
f.close()
'''
# Write csv file period - vertical accelerations
f=open('target_vertical_spectrum.csv','w')
for T, a in zip(periods,Sa_vert):
    f.write(str(T)+','+str(a)+'\n')
f.close()
    

'''
# check parameters
[S, T_B,T_C,T_D]=accsis.get_param_horiz_spectrum_type1(a_gR,K,soilTyp,v_s30,impClass)
compValues=[1.05,0.06,0.29,2] # OK
'''
'''
# Plot horizontal spectrum
plt.figure(figsize=(10,5))

plt.plot(periods,Sa_horiz)
plt.ylabel('Sa (g)', {'fontstyle':'italic','size':14})
plt.xlabel('T (s)', {'fontstyle':'italic','size':14})
plt.legend()
plt.grid()
plt.yticks(fontsize = 14)
plt.xticks(fontsize = 14)
plt.title('Horizontal response spectrum EN 1998-1:',
          {'fontstyle':'italic','size':18});
plt.show()
# Plot vertical spectrum
plt.figure(figsize=(10,5))

plt.plot(periods,Sa_vert)
plt.ylabel('Sa (g)', {'fontstyle':'italic','size':14})
plt.xlabel('T (s)', {'fontstyle':'italic','size':14})
plt.legend()
plt.grid()
plt.yticks(fontsize = 14)
plt.xticks(fontsize = 14)
plt.title('Vertical response spectrum EN 1998-1:',
          {'fontstyle':'italic','size':18});
plt.show()
'''




