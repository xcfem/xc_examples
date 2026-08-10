# Functions to calculate the scaling factor to be applied to all induvidual seismic motion components accordinng to EN 1998-2:2005, ap. 3.2.3
import numpy as np
from misc_utils import log_messages as lmsg
import bisect

def load_two_col_csv(path):
    data = np.loadtxt(path, delimiter=",", skiprows=1)
    return data[:, 0], data[:, 1]

def read_time_accel_CSVfile(twoColCSVfile,order=True):
    '''Return the periods and acceleration of the spectrum

    ;param 2colCSVfile: CSV file with header row, columns: period(s), Sa(g).
    :param order: True if it is required to order the fields by period (defaults to True)
    '''
    time,accel=load_two_col_csv(twoColCSVfile)
    if order:
        order= np.argsort(time)
        time,accel=time[order],accel[order]
    return time,accel

def calc_SRSS_spectrum_of_a_pair(spectr1CSVfile,spectr2CSVfile,order=False):
    '''Return the periods and acceleration of the pair of motions and ant SRSS spectrum generated
    with them (taking the square root of the sum of squares  of each component)
    

    ;param spectrCSVfile, spectr2CSVfile: CSVs spectrum file with header row, columns: period(s), Sa(g).
    :param order: True if it is required to order the fields by period (defaults to False)
    '''
    T1,Sa1=read_time_accel_CSVfile(spectr1CSVfile,order)
    T2,Sa2=read_time_accel_CSVfile(spectr2CSVfile,order)
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

def calc_scaling_factor(periods,Sa_target,Sa_mean,T1,factor_target):
    '''Return the scaling factor to be applied to all induvidual seismic motion components accordinng to EN 1998-2:2005, ap. 3.2.3

    :param periods: periods of the spectra
    :param Sa_target: accelerations of the target spectrum
    :param Sa_mean: accelerations of the mean spectrum
    :param T1: fundamental period
    :param factor_target: factor applied to Sa in target spectrum to compare accelerations. For horizontal motion factor_target=1.3, for vertical motion factor_target=0.9 
    '''
    Tmin=0.2*T1
    Tmax=1.5*T1
    firsIndex=bisect.bisect_left(periods,Tmin)
    lastIndex=bisect.bisect_right(periods,Tmax)
    Sa_target_scal=factor_target*Sa_target
    scalFactorsLst=[Sa_target_scal[i]/Sa_mean[i] for i in range(firsIndex,lastIndex+1)]
    scalFactor=max(scalFactorsLst)
    return scalFactor
                 
 
