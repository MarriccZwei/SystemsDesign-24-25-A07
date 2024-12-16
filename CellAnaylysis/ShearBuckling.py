if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from OOP import Cell
from OOP import FlexBox

import Loads.WingSBT as SBT


#cnsts
v = 0.33
E = 72.4e9
k_s = 10 #assumption for now



def crit_shear_stress(t, b, k_s, v, E):
    tau_crit = ((np.pi**2*k_s*E)*(t/b)**2/(12*(1-v**2)))
    return tau_crit

print(crit_shear_stress(4, 150, 10, 0.33, 72.4e9))



def max_shear_stress(V, A, k_v):
    V = SBT.combined_shear_load()
    tau_avg_shear = V/sum(A)
    tau_max_shear = k_v * tau_avg_shear
    return tau_max_shear\
    
# print(SBT.combined_shear_load())