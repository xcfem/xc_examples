import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('../')
import accelerograms_scaling_factor as asf

# Data
targetSpectrumFname='../target_horiz_spectrum.csv'
path='../output/horiz_accel/'
pairsSpectrumFnames=[
    [path+'motion1/motion1_spec.csv',path+'motion2/motion2_spec.csv'],
    [path+'motion3/motion3_spec.csv',path+'motion4/motion4_spec.csv'],
    [path+'motion5/motion5_spec.csv',path+'motion6/motion6_spec.csv']
    ]
T1=1.282 # fundamental period of the bridge
factor_target=1.3 # for horizontal motion = 1.3, for vertical motion = 0.9 EC8 ap. 3.2.3
## List of sspectrum-mathched ynthetic acceleration files to which apply the scale factor
syntheticAccelFnames=[path+'motion1/motion1_acc.csv',path+'motion2/motion2_acc.csv',path+'motion3/motion3_acc.csv',path+'motion4/motion4_acc.csv',path+'motion5/motion5_acc.csv',path+'motion6/motion6_acc.csv']
# En ddata 

# target spectrum (EC8)
T_target,Sa_target=asf.read_time_accel_CSVfile(targetSpectrumFname,order=True)
Sa_target_scal=factor_target*Sa_target
# pair 1
file1Pair=pairsSpectrumFnames[0][0]
file2Pair=pairsSpectrumFnames[0][1]
T,Sa1,Sa2,Sa_SRSS_pair1=asf.calc_SRSS_spectrum_of_a_pair(file1Pair,file2Pair)
plt.figure(figsize=(10, 10))
plt.plot(T,Sa1,label="Espectro 1",color="blue", linewidth=2)
plt.plot(T,Sa2,label="Espectro 2",color="red", linewidth=2)
plt.plot(T,Sa_SRSS_pair1,label="Espectro SRSS",color="green", linewidth=2)
plt.title('Espectros de acelerogramas 1 y 2 y espectro SRSS') 
plt.xlabel("T [s]")
plt.ylabel("Sa [g]")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend(loc="upper right", fontsize=11)
plt.savefig(path+'figures/spectr_pair1.png')
plt.show()

# pair 2
file1Pair=pairsSpectrumFnames[1][0]
file2Pair=pairsSpectrumFnames[1][1]
T,Sa1,Sa2,Sa_SRSS_pair2=asf.calc_SRSS_spectrum_of_a_pair(file1Pair,file2Pair)
plt.figure(figsize=(10, 10))
plt.plot(T,Sa1,label="Espectro 3",color="blue", linewidth=2)
plt.plot(T,Sa2,label="Espectro 4",color="red", linewidth=2)
plt.plot(T,Sa_SRSS_pair2,label="Espectro SRSS",color="green", linewidth=2)
plt.title('Espectros de acelerogramas 3 y 4 y espectro SRSS') 
plt.xlabel("T [s]")
plt.ylabel("Sa [g]")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend(loc="upper right", fontsize=11)
plt.savefig(path+'figures/spectr_pair2.png')
plt.show()
# pair 3
file1Pair=pairsSpectrumFnames[2][0]
file2Pair=pairsSpectrumFnames[2][1]
T,Sa1,Sa2,Sa_SRSS_pair3=asf.calc_SRSS_spectrum_of_a_pair(file1Pair,file2Pair)
plt.figure(figsize=(10, 10))
plt.plot(T,Sa1,label="Espectro 4",color="blue", linewidth=2)
plt.plot(T,Sa2,label="Espectro 5",color="red", linewidth=2)
plt.plot(T,Sa_SRSS_pair3,label="Espectro SRSS",color="green", linewidth=2)
plt.title('Espectros de acelerogramas 4 y 5 y espectro SRSS') 
plt.xlabel("T [s]")
plt.ylabel("Sa [g]")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend(loc="upper right", fontsize=11)
plt.savefig(path+'figures/spectr_pair3.png')
plt.show()

# mean spectrum
Sa_mean=asf.calc_Sa_mean_spectrum([Sa_SRSS_pair1,Sa_SRSS_pair2,Sa_SRSS_pair3])
'''
plt.figure(figsize=(10, 10))
plt.plot(T,Sa_mean,label="Espectro medio",color="blue", linewidth=2)
plt.plot(T,Sa_target,label="Espectro EC8",color="orange", linewidth=2)
plt.plot(T,Sa_target_scal,label="Espectro EC8 *"+ str(factor_target),color="green", linewidth=2)
plt.xlabel("T [s]")
plt.ylabel("Sa [g]")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend(loc="upper right", fontsize=11)
plt.show()
'''  
# Scaling factor calculation
scFactor=asf.calc_scaling_factor(T_target,Sa_target,Sa_mean,T1,factor_target)
print('scaling factor=',round(scFactor,3))        
    
plt.figure(figsize=(10, 10))
plt.plot(T,Sa_mean,label="Espectro medio",color="blue", linewidth=2)
plt.plot(T,Sa_target,label="Espectro EC8",color="orange", linewidth=2)
plt.plot(T,Sa_target_scal,label="Espectro EC8 *"+ str(factor_target),color="green", linewidth=2)
plt.plot(T,scFactor*Sa_mean,label="Espectro escalado",color="red", linewidth=2)
plt.xlabel("T [s]")
plt.ylabel("Sa [g]")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend(loc="upper right", fontsize=11)
plt.savefig(path+'figures/spectr_scaled.png')
plt.show()
       
# Scale all accelerograms with scFactor
for accFname in syntheticAccelFnames:
    outputFileName=accFname.replace('acc.csv','scaling_acc.csv')
    t,accel=asf.read_time_accel_CSVfile(accFname,order=True)
    scaling_accel=scFactor*accel
    np.savetxt(outputFileName,
               np.column_stack([t, scaling_accel]),
               delimiter=",", header="period_s,Sa_g", comments="")
    
