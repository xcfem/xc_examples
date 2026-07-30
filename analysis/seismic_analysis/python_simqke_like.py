import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from scipy.constants import g
from actions.quake import response_spectrum as rs

# 1. Initial parameters.
dt= 0.01            # Time step.
duracion= 40.0      # Total duration of the record.
t= np.arange(0, duracion, dt)
npts= len(t)

# 2. Generar ruido blanco
np.random.seed()#42)
ruido= np.random.normal(0, 1, npts)

# 3. Aplicar una envolvente (ej. Modelo de Jennings et al., 1968)
# Divide la señal en fases: subida, constante y decaimiento
t1, t2= 5.0, 15.0
env= np.zeros_like(t)
env[(t >= 0) & (t < t1)]= (t[(t >= 0) & (t < t1)] / t1)**2
env[(t >= t1) & (t < t2)]= 1.0
env[t >= t2]= np.exp(-0.1 * (t[t >= t2] - t2))

# Plot the envelope.
plt.figure(figsize=(10, 4))
plt.plot(t, env, color='k', linewidth=0.5)
plt.title('Envelope')
plt.xlabel('Time (s)')
plt.ylabel('Acceleration (m/s^2)')
plt.grid(True)
plt.tight_layout()
plt.show()

senal_modulada= ruido * env

# 4. Filtrar en el dominio de la frecuencia (Filtro Pasa-banda)
# Simula las frecuencias dominantes del sismo (ej. 0.1 Hz a 10 Hz)
fs= 1.0 / dt
b, a= butter(4, [0.1 / (fs / 2), 10.0 / (fs / 2)], btype='band')
aceleracion= filtfilt(b, a, senal_modulada)

# Escalar para que el PGA (Peak Ground Acceleration) sea, por ejemplo, 0.3g (aprox. 2.94 m/s^2)
pga_deseado= 0.3*g
pga_actual= np.max(np.abs(aceleracion))
aceleracion= aceleracion * (pga_deseado / pga_actual)

# 5. Visualizar el acelerograma sintético
plt.figure(figsize=(10, 4))
plt.plot(t, aceleracion, color='k', linewidth=0.5)
plt.title('Acelerograma Sintético Generado con Python')
plt.xlabel('Tiempo (s)')
plt.ylabel('Aceleración (m/s^2)')
plt.grid(True)
plt.tight_layout()
plt.show()

# 6. Compute the response spectrum.
## Define a period range below
T_min= 0.00001
T_max= 5
dtF= dt # time step for input data.
dT= dtF # time step for analysis.
Fy= 1e16 # yielding strength.
alpha= .01 # strain-hardening ratio.
                              
# a list of damping ratios to be included
zeta_list= np.array([0.02, 0.03, 0.05])

data_frame= rs.compute_response_spectrum(accelerations= list(aceleracion), dtA= dtF, dt= None, zLst= zeta_list, T_min= T_min, T_max= T_max, Fy= Fy, alpha= alpha, silent= False)

import matplotlib.pyplot as plt
## Plot accelerogram.
plt.figure(figsize=(15,3))
plt.plot(t, aceleracion, color='k')

plt.ylabel('$\\ddot{d_g} (g)$', {'size':14})
plt.xlabel('Time (s)', {'fontstyle':'italic','size':13})

plt.grid()
plt.yticks(fontsize= 14)
plt.xticks(fontsize= 14)
# plt.xlim([0.0, aceleracion[-1]]);
plt.show()

## Displacment -----------
plt.figure(figsize=(14,5))

[plt.plot(data_frame[z]['T'], data_frame[z]['SD'],
          label=('$\\zeta$ = '+str(z))) for z in zeta_list]

plt.ylabel('Relative displacement (m)', {'fontstyle':'italic','size':14})
plt.xlabel('Period (s)', {'fontstyle':'italic','size':14})
plt.legend()
plt.grid()
plt.yticks(fontsize = 14)
plt.xticks(fontsize = 14)
plt.title('Relative displacement response spectrum',
          {'fontstyle':'italic','size':18});
plt.show()

# Velocity ------------
plt.figure(figsize=(14,5))

[plt.plot(data_frame[z]['T'], data_frame[z]['SV'],
          label=('$\\zeta$ = '+str(z))) for z in zeta_list]

plt.ylabel('Relative velocity (m/s)', {'fontstyle':'italic','size':14})
plt.xlabel('Period (s)', {'fontstyle':'italic','size':14})
plt.legend()
plt.grid()
plt.yticks(fontsize = 14)
plt.xticks(fontsize = 14)
plt.title('Relative veloctiy response spectrum', 
          {'fontstyle':'italic','size':18});
plt.show()

# Acceleration ------------
plt.figure(figsize=(14,5))

[plt.plot(data_frame[z]['T'], np.array(data_frame[z]['SA'])/g,
          label=('$\\zeta$ = '+str(z))) for z in zeta_list]

plt.ylabel('Relative acceleration (g)', {'fontstyle':'italic','size':14})
plt.xlabel('Period (s)', {'fontstyle':'italic','size':14})
plt.legend()
plt.grid()
plt.yticks(fontsize = 14)
plt.xticks(fontsize = 14)
plt.title('Relative acceleration response spectrum',
          {'fontstyle':'italic','size':18});
plt.show()

# True acceleration ------------
plt.figure(figsize=(14,5))

[plt.plot(data_frame[z]['T'], np.array(data_frame[z]['STA'])/g,
          label=('$\\zeta$ = '+str(z))) for z in zeta_list]

plt.ylabel('True acceleration (g)', {'fontstyle':'italic','size':14})
plt.xlabel('Period (s)', {'fontstyle':'italic','size':14})
plt.legend()
plt.grid()
plt.yticks(fontsize = 14)
plt.xticks(fontsize = 14)
plt.title('True acceleration response spectrum',
          {'fontstyle':'italic','size':18});
plt.show()
