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


test = False
if test == True:
    from interpolatedLoads import pos_loadcase, neg_loadcase
    from maximumStresses import MaxAxialStress



#cnsts
v = 0.33 #poisson ratio
E = 72.4e9 #young modulus
k_s = 10 #assumption for now TODO input it


def crit_shear_stress(k_s):
    v = 0.33 #poisson ratio
    E = 72.4e9 #young modulus
    tau_crit = []
    webs = ['f', 'r', 'm']
    if webs[2] == None:
        webs = webs[:-1]
    for i in webs:
        t = FlexBox.thicknesses(i) #thickness of the web [m]
        b = FlexBox.length(i) #highest b gives lowest tau_critical, so the front spar 'f' [m]
        tau_crit = ((np.pi**2*k_s*E)*(t/b)**2/(12*(1-v**2)))
    return tau_crit # returns list of critical shear stress for front, rear and mid(if used) spar web

#formula test
# print(crit_shear_stress(4, 150, 10, 0.33, 72.4e9))


def max_shear_stress(V, A):
    k_v = 1.5
    A = 1
    V = pos_loadcase()
    tau_avg_shear = V/sum(A)
    tau_max_shear = k_v * tau_avg_shear
    return tau_max_shear
    
# print(SBT.combined_shear_load())