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
    S_ht_ft = planform.S / (0.3048**2)
    L_t_ft = tailLength / 0.3048
    K_y = 0.3 * L_t_ft
    sweep_ht = planform.sweepC4
    S_e_ft = elevatorArea / (0.3048**2)
    b_h = planform.b
    A_h = planform.AR

    factor1 = (1+F_w_ft/b_h)**(-0.25)
    factor2 = K_y**0.704 * np.cos(sweep_ht)**(-1)
    factor3 = (1+S_e_ft/S_ht_ft)**0.1

    mass_horizontal_lb = 0.0379 * K_uht * factor1 * Mdeslb**0.639 * nult * S_ht_ft**0.75 * L_t_ft**(-1.) * factor2 * A_h**0.166 * factor3 
    mass_horizontal_kg = 0.4536*mass_horizontal_lb
    return mass_horizontal_kg 

def rudder_mass(Mdes, nult, planform:pf.Planform, tailLength, tcRudder): #make sure to use the asymmetric planform
    Mdeslb = Mdes/0.4536 #to pounds-mass
    S_vt_ft = planform.S / (0.3048**2)
    L_t_ft = tailLength / 0.3048
    K_z = L_t_ft
    sweep_vt = planform.sweepC4
    A_v = planform.AR

    mass_vertical_lb = 0.0026*Mdeslb**0.556*nult**0.536*L_t_ft**(-.5)*S_vt_ft**0.5*K_z**0.875/np.cos(sweep_vt)*A_v**0.35*tcRudder**(-.5)
    mass_vertical_kg = 0.4536*mass_vertical_lb
    return mass_vertical_kg 

'''Landing Gear mass Estimation'''
#verify it's 2.5!!!
def lg_mass(MTOM, landingMassFraction, mlgLength, nlgLength, mlgNwheels, nlgNwheels, 
mlgStrokeStrutsN, Vstall, loadFactorTouchdown = 2.5): 
    MTOMlb = MTOM/0.4536
    MLlb = MTOMlb*landingMassFraction
    Nl = 1.5 * loadFactorTouchdown

    WMLGlb = 0.0106*MLlb**0.888*Nl**(.25)*mlgLength**0.4*mlgNwheels**0.321*mlgStrokeStrutsN**(-.5)*Vstall**0.1
    WNLGlb = 0.032*MLlb**0.646*Nl**(0.2)*nlgLength**0.5*nlgNwheels*0.45
    return 0.4536*(WMLGlb+WNLGlb), 0.4536*WMLGlb, 0.4536*WNLGlb #returns the lgmass as a whole pluss component masses

'''nacelle group mass'''
def nacelle_mass(Nlt, Nw, Nz, Wen, Nen, Sn):
    Kng = 1.017
    Nltft = Nlt /0.3048
    Nwft = Nw / 0.3048
    Weclb = 2.331*(Wen*2.204623)**0.901*1.18
    Snft = Sn/(0.30348**2)

    return 0.4536*(0.6724*Kng*Nltft**0.1*Nwft**0.294*Nz**0.119*Weclb**0.611*Nen**0.984*Snft**0.224)

'''engine controls mass'''
def engine_controls_mass(Nen,Lec):
    Lecft = Lec/0.3048

    return 0.4536*(5*Nen + 0.8*Lecft)

'''starter pneumatic mass'''
def starter_mass(Nen, Wen):
    Wenlb = 2.204623 * Wen

    return 0.4536*(49.19*(Nen*Wenlb/1000)**0.541)

'''fuel system mass'''
def fuel_system_mass(Vt, Nt):
    Vtgal = Vt * 264.1721

    return 0.4536*(2.405*Vtgal**0.606/2*Nt**0.5)

'''flight control mass'''
def flight_control_mass(Scs,Iy,Nf=6,Nm=1):#Nf and Nm are assumptions, idk what they should be
    Scsft = Scs/(0.3048**2)
    Iylb = Iy * 23.7304

    return 0.4536*(145.9*Nf**0.554/(1+Nm/Nf)*Scsft**0.2*(Iylb/(10**6))**0.07)

'''APU installed mass'''
def apu_installed_mass(Wapu_uninstalled):
    return 2.2 * Wapu_uninstalled

'''instruments mass'''
def instruments_mass(Nc, Nen, Lf, Bw):
    Lfft = Lf /0.3048
    Bwft = Bw /0.3048

    return 0.4536*(4.509*Nc**0.541*Nen*(Lfft+Bwft)**0.5)

'''hydraulics mass'''
def hydraulics_mass(Lf, Bw, Nf=6):
    Lfft = Lf /0.3048
    Bwft = Bw /0.3048

    return 0.4536*(0.2673*Nf*(Lfft+Bwft)**0.937)

'''electrical systems mass'''
def electrical_mass(La, Nen, Rkva = 50):#Rkva is between 40 and 60 for transport a/c
    Laft = La /0.3048
    
    return 0.4536*(7.291*Rkva**0.782*Laft**0.346*Nen**0.1)

'''avionics mass'''
def avionics_mass(Wuav=500):
    Wuavlb = Wuav * 2.204623

    return 0.4536*(1.73*Wuavlb**0.983)

'''furnishings mass'''
def furnish_mass(Nc, Wc, Sf):
    Wclbs = Wc*2.204623
    Sfft = Sf/(0.30348**2)

    return 0.4536*(0.0577*Nc**0.1*Wclbs**0.393*Sfft**0.75)

'''air conditioning mass'''
def aircon_mass(Np, Vpr, Wuav=500):
    Vprft = Vpr/(0.3048**3)
    Wuavlb = Wuav *2.204623

    return 0.4536*(62.36*Np**0.25*(Vprft/1000)**0.604*Wuavlb**0.1)

'''anti-ice system mass'''
def anti_ice_mass(Wdg):
    return 0.002*Wdg

'''handling gear mass'''
def handling_mass(Wdg):
    return 3*10**(-4)*Wdg
#kg to pounds: x 2.204623
#m to feet: /0.3048
#m3 to gals: *264.1721