if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING

import OOP.Planform as pf
import OOP.Fuselage as fus
import numpy as np
import General.Constants as const

def wing_mass(planform:pf.Planform, Mdes, nult, tc, movableArea): #from Raymer
    Mdeslb = Mdes/0.4536 #to pounds-mass because the formula is in freedom units
    Swft2 = planform.S/0.3048/0.3048 #to ft^2
    movableAreaft2 = movableArea/0.3048/0.3048 #to ft^2

    weightTerm = (Mdeslb*nult)**0.557
    wingSurfaceTerm = Swft2**0.649*planform.AR**0.5
    wingChordTerm = tc**(-.4)*(1+planform.TR)^0.1
    sweepTerm = movableAreaft2**0.1/np.cos(planform.sweepC4)

    #the returned value in lb mass
    returnlb = 0.0051*weightTerm*wingSurfaceTerm*wingChordTerm*sweepTerm 
    return 0.4536*returnlb #the returned value in kg


def fus_mass(planform:pf.Planform, fuselage:fus.Fuselage, Mdes, nult): #the fuselage mass
    # Convertions
    Mdeslb = Mdes/0.4536 #to pounds-mass
    L_ft = fuselage.L / 0.3048  # meters to feet
    D_ft = fuselage.D / 0.3048  # meters to feet

    # Import constants from constants.py file
    K_door = const.KDOOR
    K_lg = const.KLG
    S_f = planform.Sw

    # Calculate some terms in order to simplify the big equation
    weightTerm = (Mdeslb*nult)**0.5
    k_w_s = 0.75 * (1+2*planform.TR)/(1+planform.TR) * (planform.b * np.tan(planform.sweepC4/L_ft))
    K = 0.3280 * K_door * K_lg  # This is the constant in the big equation
    
    returnlb = K * weightTerm * L_ft**0.25 * S_f**0.302 * (1+k_w_s)**0.04 * (L_ft/D_ft)**0.10  # Formula rom Raymer
    return 0.4536*returnlb # Returns fuselage mass in kg

# TODO do the vertical tail mass and add both as the output, dont forget to change units
def tail_mass(Mdes, nult, planform:pf.Planform):
    Mdeslb = Mdes/0.4536 #to pounds-mass
    K_uht = const.KUHT
    F_w_ft = const.FW /0.3048
    S_ht_ft = const.SVTAIL / (0.3048)**2
    L_t_ft = const.LT / 0.3048
    K_y = 0.3 * L_t_ft
    sweep_ht = const.SWEEPHT
    S_e_ft = const.SE / (0.3048)**2
    S_ht_ft = const.SHTAIL / (0.3048)**2
    b_h = const.BH
    A_h = const.ARHTAIL
    t_to_c_root = const.THICKNESSTOCHORD

    factor1 = (1+F_w_ft/b_h)**(-0.25)
    factor2 = K_y**0.704 * np.cos(sweep_ht)**(-1.)
    factor3 = (1+S_e_ft/S_ht_ft)**0.1

    mass_horizontal_lb = 0.0379 * K_uht * factor1 * Mdeslb**0.639 * nult * S_ht_ft**0.75 * L_t_ft**(-1.) * factor2 * A_h**0.166 * factor3 
    mass_horizontal_kg = 0.4536*mass_horizontal_lb
    return mass_horizontal_kg 

def lg_mass():
    pass