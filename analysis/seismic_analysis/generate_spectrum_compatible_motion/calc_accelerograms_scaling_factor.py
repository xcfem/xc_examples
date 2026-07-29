# Calculate the scaling factor to be applied to all induvidual seismic motion components accordinng to EN 1998-2:2005, ap. 3.2.3
import numpy as np
from misc_utils import log_messages as lmsg
import matplotlib.pyplot as plt
# Data
targetSpectrumFname='./target_horiz_spectrum.csv'
pairsSpectrumFnames=[
    ['output/horiz_accel/motion1/motion1_spec.csv','output/horiz_accel/motion2/motion2_spec.csv'],
    ['output/horiz_accel/motion3/motion3_spec.csv','output/horiz_accel/motion4/motion4_spec.csv'],
    ['output/horiz_accel/motion5/motion5_spec.csv','output/horiz_accel/motion6/motion6_spec.csv']
    ]
##
# List of sspectrum-mathched ynthetic acceleration files to which apply the scale factor
syntheticAccelFnames=['output/horiz_accel/motion1/motion1_acc.csv','output/horiz_accel/motion2/motion2_acc.csv','output/horiz_accel/motion3/motion3_acc.csv','output/horiz_accel/motion4/motion4_acc.csv','output/horiz_accel/motion5/motion5_acc.csv','output/horiz_accel/motion6/motion6_acc.csv']

def load_two_col_csv(path):
    data = np.loadtxt(path, delimiter=",", skiprows=1)
    return data[:, 0], data[:, 1]

def get_spectrum(spectrCSVfile,order=False):
    '''Return the periods and acceleration of the spectrum

    ;param spectrCSVfile: CSV file with header row, columns: period(s), Sa(g).
    :param order: True if it is required to order the fields by period (defaults to False)
    '''
    T_espectr,Sa_spectr=load_two_col_csv(spectrCSVfile)
    if order:
        order= np.argsort(T_espectr)
        T_espectr,Sa_spectr=T_espectr[order],Sa_spectr[order]
    return T_espectr,Sa_spectr

def calc_SRSS_spectrum_of_a_pair(spectr1CSVfile,spectr2CSVfile,order=False):
    '''Return the periods and acceleration of the pair of motions and ant SRSS spectrum generated
    with them (taking the square root of the sum of squares  of each component)
    

    ;param spectrCSVfile, spectr2CSVfile: CSVs spectrum file with header row, columns: period(s), Sa(g).
    :param order: True if it is required to order the fields by period (defaults to False)
    '''
    T1,Sa1=get_spectrum(spectr1CSVfile,order)
    T2,Sa2=get_spectrum(spectr2CSVfile,order)
    if len(T1) != len(T2):
        lmsg.error("number of periods in "+spectr1CSVfile+" doesn't match those of "+spectr2CSVfile)
        exit(1)
    Sa_SRSS=np.hypot(Sa1,Sa2)
    return T1,Sa1,Sa2,Sa_SRSS

def calc_Sa_mean_spectrum(lstSaSpectra):
    ''' Return the mean acceleration form a list of spectral accelerations

    :param lstSaSpectra: list of 
    '''
    Sa_mean=np.mean(lstSaSpectra,axis=0)
    return Sa_mean

# target spectrum (EC8)
T_target,Sa_target=get_spectrum(targetSpectrumFname,order=True)
Sa_target1_3=1.3*Sa_target
# pair 1
file1Pair=pairsSpectrumFnames[0][0]
file2Pair=pairsSpectrumFnames[0][1]
T,Sa1,Sa2,Sa_SRSS_pair1=calc_SRSS_spectrum_of_a_pair(file1Pair,file2Pair)
plt.figure(figsize=(10, 10))
plt.plot(T,Sa1,label="Espectro 1",color="blue", linewidth=2)
plt.plot(T,Sa2,label="Espectro 2",color="red", linewidth=2)
plt.plot(T,Sa_SRSS_pair1,label="Espectro SRSS",color="green", linewidth=2)
plt.title('Espectros de acelerogramas 1 y 2 y espectro SRSS') 
plt.xlabel("T [s]")
plt.ylabel("Sa [g]")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend(loc="upper right", fontsize=11)
plt.show()

# pair 2
file1Pair=pairsSpectrumFnames[1][0]
file2Pair=pairsSpectrumFnames[1][1]
T,Sa1,Sa2,Sa_SRSS_pair2=calc_SRSS_spectrum_of_a_pair(file1Pair,file2Pair)
plt.figure(figsize=(10, 10))
plt.plot(T,Sa1,label="Espectro 3",color="blue", linewidth=2)
plt.plot(T,Sa2,label="Espectro 4",color="red", linewidth=2)
plt.plot(T,Sa_SRSS_pair2,label="Espectro SRSS",color="green", linewidth=2)
plt.title('Espectros de acelerogramas 3 y 4 y espectro SRSS') 
plt.xlabel("T [s]")
plt.ylabel("Sa [g]")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend(loc="upper right", fontsize=11)
plt.show()
# pair 3
file1Pair=pairsSpectrumFnames[2][0]
file2Pair=pairsSpectrumFnames[2][1]
T,Sa1,Sa2,Sa_SRSS_pair3=calc_SRSS_spectrum_of_a_pair(file1Pair,file2Pair)
plt.figure(figsize=(10, 10))
plt.plot(T,Sa1,label="Espectro 4",color="blue", linewidth=2)
plt.plot(T,Sa2,label="Espectro 5",color="red", linewidth=2)
plt.plot(T,Sa_SRSS_pair3,label="Espectro SRSS",color="green", linewidth=2)
plt.title('Espectros de acelerogramas 4 y 5 y espectro SRSS') 
plt.xlabel("T [s]")
plt.ylabel("Sa [g]")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend(loc="upper right", fontsize=11)
plt.show()

# mean spectrum
Sa_mean=calc_Sa_mean_spectrum([Sa_SRSS_pair1,Sa_SRSS_pair2,Sa_SRSS_pair3])
plt.figure(figsize=(10, 10))
plt.plot(T,Sa_mean,label="Espectro medio",color="blue", linewidth=2)
plt.plot(T,Sa_target,label="Espectro EC8",color="red", linewidth=2)
plt.plot(T,Sa_target1_3,label="Espectro EC8 * 1.3",color="green", linewidth=2)
plt.xlabel("T [s]")
plt.ylabel("Sa [g]")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend(loc="upper right", fontsize=11)
plt.show()
  

        
    
        
    
    
    
    
    
    
    
    

