import numpy as np

def crit_shear_stress_skin(k_c,E,v,t,b):
    tau_crit = (((np.pi**2)*k_c*E)/(12*(1-v**2)))*((t)/(b))**2
    return tau_crit
print("sth")