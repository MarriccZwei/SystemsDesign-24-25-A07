import numpy as np
from math import log, sqrt, tan, sin, pi

#tire pressure in kg/cm^2
def p_tire(LCN):
    p_tire = (1/100)*(430*log(LCN) - 680)
    return p_tire

#static load per main landing gear wheel in kg
#NWM is the total number of MLG wheels
def P_MW(LT, mTOM,NWM):
    P_MW = LT * (mTOM/NWM)
    return P_MW

#static load per nose landing gear wheel in kg 
#NWN is the total number of NLG wheels
def P_NW(mTOM,NWN, LT):
    P_NW = LT * (mTOM/NWN)
    return P_NW

# TC is the Length from the nose of the aircraft to the start of the tail cone
def TC(LFUS, LTC, cg):
    TC = LFUS - (LTC + cg)
    return TC

# z_MLG is the height of the main landing gear wrt the ground
#TC is the longitudinal position of the tail cone wrt the nose
# cg is the most aft longitudinal position of the centre of grav wrt the nose
def z_MLG(cg, TC, TailScrape, AbsorberStroke):
    z_MLG = tan(np.radians(TailScrape)) * (TC - cg) + AbsorberStroke
    return z_MLG

# approximation of the z position of the cg 
def z_cg(z_MLG, DEQUIVALENT):
    z_cg = z_MLG + (DEQUIVALENT/3)
    return z_cg

# l_m is the longitudinal location of the main landing gear wrt the nose 
# cg is the most aft location 
# height of cg wrt to ground is assumed to be MLG height + FusDiameter/2
def l_m(Tailscrape, cg, z_cg):
    l_m = (z_cg *  tan(np.radians(Tailscrape))) + cg
    return l_m

def P_M(mMTO, LF):
    P_M = LF * mMTO
    return P_M

def P_N(LF, mMTO):
    P_N = mMTO * (1- LF)
    return P_N

def P_n(mMTO, P_MW, NSTRUT):
    P_n = mMTO - P_MW * NSTRUT
    return P_n
    

# l_n is the longitudinal position of the nose gear wrt the nose
def l_n(mMTO, l_m, P_n, cg):
    l_n = (((mMTO)/(P_n)) -1) * (l_m - cg)
    return l_n

# Minimum MLG dist from centreline to avoid laterap tip over
# l_n nose gear position (from nose), l_m main gear position (from nose)
# z_cg height of cg relaitve to ground, psi assumed to be <= 55 deg
def y_MLG_to(l_n, l_m, z_cg, psi):
    y_MLG_to = ((l_n + l_m)/(sqrt(((((l_n)**2 * (tan(np.radians(psi)))**2)/(z_cg)**2))- 1)))
    return y_MLG_to

# z_t is the height of the wing tip wrt the ground 
def z_t(b, dihedral, z_MLG):
    z_t = z_MLG + (b/2) * sin(dihedral)
    return z_t

# z_n is the height of the engine wrt the ground 
# d_eng is the diameter of the engine 
def z_n(z_MLG, b, dihedral, DNACELLE):
    z_n = z_MLG + ((1/3) * (b/2) * sin(dihedral)) - DNACELLE
    return z_n

# Minimum MLG dist from centreline to ensure sufficient wing tip clearance
# b span, z_t height of wing tip wrt ground, phi angle between MLG and wing tip >5 deg
def y_MLG_tc(b, z_t, phi):
    y_MLG_tc = (b/2) - ((z_t)/ tan(np.radians(phi)))
    return y_MLG_tc

# Minimum MLG dist from centreline to ensure sufficient engine tip clearance
# b span, z_n height of engine wrt ground, phi angle between MLG and engine >5 deg
# y_n is the lateral location of the centerline of the engine approx 1/3(b/2)
def y_MLG_ec(b, z_n, phi):
    y_MLG_ec = ((1/3) * (b/2)) - ((z_n)/(tan(np.radians(phi))))
    return y_MLG_ec

# calculating the maximum value of the three conditions for the final lateral placement of MLG
def y_MLG(y_MLG_to, y_MLG_tc, y_MLG_ec):
    y_MLG = max(y_MLG_to, y_MLG_tc, y_MLG_ec)
    return y_MLG
# if __name__ == "__main__":

