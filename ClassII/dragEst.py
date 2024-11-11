if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    import unittest
    # ONLY FOR TESTING

import numpy as np
import General.Constants as consts
import OOP.Planform as pf
import OOP.Fuselage as fus

#reynolds number formula, l is length, rho - ambient air density, M- mach number
def Reynolds(rho, l, M):
    k = 0.634*10**(-5) #smooth paint assumption
    return min(rho*l*M*consts.CRUISESOUNDSPEED/consts.CRUISEVISCOSITY, 44.62*(l/k)**1.053*M)

#friction coefficient formula laminarFraction is a fraction of the object experiencing laminar flow (take from the slides), M is the mach number
def Cf(Reynolds, laminarFraction, M):
    return laminarFraction*1.328/np.sqrt(Reynolds)+(1-laminarFraction)*.455/(np.log10(Reynolds))**2.58/(1+0.144*M**2)**0.65

#form factor fuselage; L - fuselage length, D - fuselage equivalent diameter
def FFfus(L, D):
    f = L/D
    return 1+60/f**3+f/400

#form factor for planforms - tcmaxpos is the max. thickness position 0.38sth measure in CAD on the airfoil
#tc is max.thickness-to-chord ratio, M is mach number and sweepAtmaxT is sweep at the max thickness line of the wing
def FFwing(tcmaxpos, tc, M, sweepAtmaxT): #use the sweep formula from planform to calculate sweep_m
    return (1+.6/tcmaxpos*tc+100*tc**4)*(1.34*M**.18*np.cos(sweepAtmaxT)**.28)

ARe = lambda AR: AR+0.04 #effective aspect ratio for square wing tips

Oswald = lambda ARe:1/(0.0075*ARe*np.pi+1/.97) #the working formula - USE THE ARe

CDi = lambda CL, ARe: CL**2/ARe/np.pi/Oswald(ARe) #induced drag coefficient

#The wave drag coefficient - M is the mach number, ka is technology constant (we use 0.87), CL is lift coefficient,
#tc is max.thickness-to-chord ratio, Mcr is the critical mach number value
def Cdmisc(M, ka, CL, sweepLE, tc, Mcr = 0.6): #to change the Mcr value to the real one
    Mdd = ka/np.cos(sweepLE) -tc/np.cos(sweepLE)**2 - CL/10/np.cos(sweepLE)**3
    if M < Mcr:
        Cdmisc = 0
    elif Mcr <= M <= Mdd:
        Cdmisc = 0.002*(1 +2.5*((Mdd - M)/0.05))**-1
    else:
        Cdmisc = 0.002*(1 +2.5*((M - Mdd)/0.05))**2.5
    return Cdmisc

def Cdo(rho, mach, CLdes, tcMax, planForm:pf.Planform, fuseLage:fus.Fuselage, Sref, Mcr = 0.6, tcMaxPos=0.38, ka=0.87):
    sweepMaxTc = planForm.sweep_at_c_fraction(0.38)
    sum = 0
    
    #wing calculations
    length = planForm.MAC
    lamFrac = 0.1
    FF = FFwing(tcMaxPos, tcMax, mach, sweepMaxTc)
    CF = Cf(Reynolds(rho, length, mach), lamFrac, mach)
    IF = 1
    Swet = planForm.Sw
    sum += CF*FF*IF*Swet

    length = fuseLage.L
    FF = FFfus(fuseLage.L,fuseLage.D)
    CF = Cf(Reynolds(rho, length, mach), lamFrac, mach)
    IF = 1
    Swet = fuseLage.Sw
    sum += (CF*FF*IF*Swet)

    Cdmiscellaneous = Cdmisc(mach, ka, CLdes, planForm.sweepLE, tcMax, Mcr)

    return sum/Sref + Cdmiscellaneous

# if __name__ == "__main__":
#     class TestDragEst(unittest.TestCase):
#         def test_Cd0(self):
#             print(f"Cd0 for a typical input: {Cdo(consts.CRUISEDENSITY, consts.CRUISEMACH, 0.6, consts.THICKNESSTOCHORD, pf.Planform(360, 9, 0.4, 30, 0), fus.Fuselage(5, 11, 30, 15), 360)}")
    
#     unittest.main()