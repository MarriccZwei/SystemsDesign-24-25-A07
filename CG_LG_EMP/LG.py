import numpy as np
from math import log, sqrt, tan, sin

#tire pressure in kg/cm^2
def p_tire(LCN):
    p_tire = (1/100)*(430*log(LCN) - 680)
    return p_tire

#static load per main landing gear wheel in kg
#NWM is the total number of MLG wheels
def P_MW(MTOM,NWM):
    P_MW = 0.92 * (MTOM/NWM)
    return P_MW

#static load per nose landing gear wheel in kg 
#NWN is the total number of NLG wheels
def P_NW(MTOM,NWN):
    P_NW = 0.08 * (MTOM/NWN)
    return P_NW

def l_n(MTOM, P_NW, l_m):
    l_n = l_m * ((MTOM/P_NW) -1)
    return l_n

def z_MLG(cg, TC, TailScrape):
    z_MLG = tan(np.radians(TailScrape)) * (TC - cg)
    return z_MLG

# Minimum MLG dist from centreline to avoid laterap tip over
# l_n nose gear position (from nose), l_m main gear position (from nose)
# z_cg height of cg relaitve to ground, psi assumed to be <= 55 deg
def y_MLG_to(l_n, l_m, z_cg, psi):
    y_MLG_to = (l_n + l_m)/(sqrt(((l_n**2 * tan(psi)**2)/(z_cg**2)-1)))
    return y_MLG_to

def z_t(b, dihedral):
    z_t = 2.44 + (b/2) * sin(dihedral)
    return z_t

def z_n(b, dihedral):
    z_n = 2.44 + (1/3) * (b/2) * sin(dihedral)
    return z_n

# Minimum MLG dist from centreline to ensure sufficient wing tip clearance
# b span, z_t height of wing tip wrt ground, phi angle between MLG and wing tip >5 deg
def y_MLG_tc(b, z_t, phi):
    y_MLG_tc = (b/2) - ((z_t)/tan(phi))
    return y_MLG_tc

# Minimum MLG dist from centreline to ensure sufficient engine tip clearance
# b span, z_n height of engine wrt ground, psi angle between MLG and engine >5 deg
def y_MLG_ec(y_e, z_n, psi):
    y_MLG_ec = y_e - ((z_n)/(tan(psi)))
    return y_MLG_ec


#if __name__ == "__main__":




