import numpy as np
from OOP.Planform import Planform


''' Skin Friction '''
def sf_lam(Re):
    sf_lam = (1.328/np.sqrt(Re))
    return sf_lam

def sf_turb(Re, M):
    sf_turb = 0.455 / (((np.log10(Re))**2.58)*(1 + 0.144*(M**2))**0.65)
    return sf_turb

# Wing Skin Friction
# civil jet - wing 10% laminar - fus 5% laminar
def wing_tail_sf(sf_lam, sf_turb, winglam_ratio = 0.1):
    wing_tail_sf = winglam_ratio*sf_lam + (1 - winglam_ratio)*sf_turb
    return wing_tail_sf

# Fuslege Skin Friction
def fus_sf(sf_lam, sf_turb, fuslam_ratio = 0.05):
    fus_sf = fuslam_ratio*sf_lam + (1 - fuslam_ratio)*sf_turb
    return fus_sf


''' Form Factor '''

# Wing and Tail Form Factor

# sweep angle at maximum thickness, need leading edge sweep, root chord, span, position of maximum thickness, taper ratio
def Lambda_m(Lambda_LE, C_r, b, x_c, tr):
    Lambda_m = np.arctan( np.tan(Lambda_LE) - x_c*((2*C_r)/b)*(1-tr))
    return Lambda_m

def Wing_Tail_FF(x_c_m, t_c, M, Lambda_m):
    
    first_term = 1 + (0.6 / x_c_m) * t_c + 100 * (t_c**4)
    
    second_term = 1.34 * M**0.18 * (np.cos(np.radians(Lambda_m))**0.28)
    
    Wing_Tail_FF = first_term * second_term
    
    return Wing_Tail_FF

# Fuselage Form Factor

def fineness_ratio(l_fus , d):
    fineness_ratio = l_fus/d
    return fineness_ratio

def fus_FF(f):
    fus_FF = 1 + 60/(f**3) + f/400
    return fus_FF

'''' Interference factor '''

# Tail IF conventional tail IF = 1.05

''' Wetted Area '''

# Wing wetted area
def wing_wetted(S)
    wing_wetted = 1.07*2*S
    return wing_wetted

# Horizontal tail wtted area

def htail_wetted(S_htail)
    htail_wetted = 1.05*2*S_htail
    return htail_wetted

# Vertical tail wtted area

def vtail_wetted(S_vtail)
    vtail_wetted = 1.05*2*S_vtail
    return vtail_wetted

# Fuselage wetted area
# D is fuselage diameter, L1, L2 and L3 is nose-cone, midsection and tail-cone lengths respectively
def fus_Sw(D, L1, L2, L3):
    term1 = (1 / (3 * L1**2))
    term2 = ((4 * L1**2 + D**2 / 4)**1.5) - (D**3 / 8)
    term3 = -D
    term4 = 4 * L2
    term5 = 2 * np.sqrt(L3**2 + D**2 / 4)
    
    fus_Sw = (np.pi * D / 4) * (term1 * term2 + term3 + term4 + term5)
    
    return fus_Sw

''' Miscelenous Drag '''
# Include Wave Drag,  Excrescence/Leakege and Upsweep/base area