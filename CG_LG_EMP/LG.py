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

def TC(LFUS, LTC):
    TC = LFUS - LTC
    return TC

# z_MLG is the height of the main landing gear wrt the ground
#TC is the longitudinal position of the tail cone wrt the nose
# cg is the most aft longitudinal position of the centre of grav wrt the nose
def z_MLG(cg, TC, TailScrape, AbsorberStroke):
    z_MLG = tan(np.radians(TailScrape)) * (TC - cg) + AbsorberStroke
    return z_MLG

# l_m is the longitudinal location of the main landing gear wrt the nose 
# cg is the most aft location 
# height of cg wrt to ground is assumed to be MLG height + FusDiameter/2
def l_m(Tailscrape, cg, z_MLG, DEQUIVALENT):
    l_m = (tan(np.radians(Tailscrape)) * (z_MLG + (DEQUIVALENT/2))) + cg
    return l_m

# l_n is the longitudinal position of the nose gear wrt the nose
def l_n(MTOM, P_NW, l_m):
    l_n = l_m * ((MTOM/P_NW) -1)
    return l_n

# Minimum MLG dist from centreline to avoid laterap tip over
# l_n nose gear position (from nose), l_m main gear position (from nose)
# z_cg height of cg relaitve to ground, psi assumed to be <= 55 deg
def y_MLG_to(l_n, l_m, z_cg, psi):
    y_MLG_to = (l_n + l_m)/(sqrt(((l_n**2 * tan(np.radians(psi))**2)/(z_cg**2)-1)))
    return y_MLG_to

# z_t is the height of the wing tip wrt the ground 
def z_t(b, dihedral, z_MLG):
    z_t = z_MLG + (b/2) * sin(np.radians(dihedral))
    return z_t

# z_n is the height of the engine wrt the ground 
# d_eng is the diameter of the engine 
def z_n(b, dihedral, d_eng):
    z_n = (1/3) * (b/2) * sin(np.radians(dihedral)) - d_eng
    return z_n

# Minimum MLG dist from centreline to ensure sufficient wing tip clearance
# b span, z_t height of wing tip wrt ground, phi angle between MLG and wing tip >5 deg
def y_MLG_tc(b, z_t, phi):
    y_MLG_tc = (b/2) - ((z_t)/tan(np.radians(phi)))
    return y_MLG_tc

# Minimum MLG dist from centreline to ensure sufficient engine tip clearance
# b span, z_n height of engine wrt ground, phi angle between MLG and engine >5 deg
# y_n is the lateral location of the centerline of the engine approx 1/3(b/2)
def y_MLG_ec(y_n, z_n, phi):
    y_MLG_ec = y_n - ((z_n)/(tan(np.radians(phi))))
    return y_MLG_ec

# if __name__ == "__main__":

