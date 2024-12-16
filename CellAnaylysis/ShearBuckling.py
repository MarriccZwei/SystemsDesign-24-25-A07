import numpy as np

def crit_shear_stress(t, b, k_s, v, E):
    tau_crit = ((np.pi**2*k_s*E)*(t/b)**2/(12*(1-v**2)))
    return tau_crit


def max_shear_stress(V, A, k_v):
    tau_avg_shear = V/sum(A)
    tau_max_shear = k_v * tau_avg_shear
    return tau_max_shear