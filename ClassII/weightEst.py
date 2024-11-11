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
    wingChordTerm = tc**(-.4)*(1+planform.TR)**0.1
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
    S_f = fuselage.Sw

    # Calculate some terms in order to simplify the big equation
    weightTerm = (Mdeslb*nult)**0.5
    k_w_s = 0.75 * (1+2*planform.TR)/(1+planform.TR) * (planform.b * np.tan(planform.sweepC4/L_ft))
    K = 0.3280 * K_door * K_lg  # This is the constant in the big equation
    
    returnlb = K * weightTerm * L_ft**0.25 * S_f**0.302 * (1+k_w_s)**0.04 * (L_ft/D_ft)**0.10  # Formula rom Raymer
    return 0.4536*returnlb # Returns fuselage mass in kg

# TODO do the vertical tail mass and add both as the output, dont forget to change units
def tail_mass(Mdes, nult, planform:pf.Planform, tailLength, elevatorArea):
    Mdeslb = Mdes/0.4536 #to pounds-mass
    K_uht = const.KUHT
    F_w_ft = const.FW /0.3048
    S_ht_ft = planform.S / (0.3048)**2
    L_t_ft = tailLength / 0.3048
    K_y = 0.3 * L_t_ft
    sweep_ht = planform.sweepC4
    S_e_ft = elevatorArea / (0.3048)**2
    b_h = planform.b
    A_h = planform.AR

    factor1 = (1+F_w_ft/b_h)**(-0.25)
    factor2 = K_y**0.704 * np.cos(sweep_ht)**(-1.)
    factor3 = (1+S_e_ft/S_ht_ft)**0.1

    mass_horizontal_lb = 0.0379 * K_uht * factor1 * Mdeslb**0.639 * nult * S_ht_ft**0.75 * L_t_ft**(-1.) * factor2 * A_h**0.166 * factor3 
    mass_horizontal_kg = 0.4536*mass_horizontal_lb
    return mass_horizontal_kg 

def rudder_mass(Mdes, nult, planform:pf.Planform, tailLength, tcRudder): #make sure to use the asymmetric planform
    Mdeslb = Mdes/0.4536 #to pounds-mass
    S_vt_ft = planform.S / (0.3048)**2
    L_t_ft = tailLength / 0.3048
    K_z = L_t_ft
    sweep_vt = planform.sweepC4
    A_v = planform.AR

    mass_vertical_lb = 0.0026*Mdeslb**0.556*nult**0.536*L_t_ft**(-.5)*S_vt_ft**0.5*K_z**0.875/np.cos(sweep_vt)*A_v**0.35*tcRudder**(-.5)
    mass_vertical_kg = 0.4536*mass_vertical_lb
    return mass_vertical_kg 

'''Landing Gear mass Estimation'''
#verify it's 2.5!
def lg_mass(MTOM, landingMassFraction, mlgLength, nlgLength, mlgNwheels, nlgNwheels, 
mlgStrokeStrutsN, Vstall, loadFactorTouchdown = 2.5): 
    MTOMlb = MTOM/0.4536
    MLlb = MTOMlb*landingMassFraction
    Nl = 1.5 * loadFactorTouchdown

    WMLGlb = 0.0106*MLlb**0.888*Nl**(.25)*mlgLength**0.4*mlgNwheels**0.321*mlgStrokeStrutsN**(-.5)*Vstall**0.1
    WNLGlb = 0.032*MLlb**0.646*Nl**(0.2)*nlgLength**0.5*nlgNwheels*0.45
    return 0.4536*(WMLGlb+WNLGlb), 0.4536*WMLGlb, 0.4536*WNLGlb #returns the lgmass as a whole pluss component masses