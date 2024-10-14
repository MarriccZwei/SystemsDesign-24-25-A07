if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING

import numpy as np

def Reynolds(rho, l, M, paint):
    pass

def Cf(M, Reynolds, laminarFraction):
    pass

def FFfus(L, D): #add other parameters
    pass

def FFwing(tcmaxpos, tc, M): #use the sweep formula to calculate sweep_m
    pass

def SwFus(D, L1, L2, L3): #Wetted Surface Fuselage
    term1 = (1 / (3 * L1**2))
    term2 = ((4 * L1**2 + D**2 / 4)**1.5) - (D**3 / 8)
    term3 = -D
    term4 = 4 * L2
    term5 = 2 * np.sqrt(L3**2 + D**2 / 4)
    term6 = np.pi/4*D
    return term6*(term1*term2+term3+term4+term5)

SwWing = lambda S:2*1.07*S #Wetted Surface of any Wing Planform (can be a tail or pylon or wing)

ARe = lambda AR: AR+0.04 #effective aspect ratio for square wing tips

Oswald = lambda ARe:1/(0.0075*ARe*np.pi+1/.97) #the working formula - USE THE ARe

CDi = lambda CL, ARe: CL**2/ARe/np.pi/Oswald(ARe) #induced drag coefficient

def Cdmisc(M, ka, CL, sweepLE, tc, Mcr = 0.6): #to change the Mcr value
    Mdd = ka/np.cos(sweepLE) -tc/np.cos(sweepLE)**2 - CL/np.cos(sweepLE)**3
    if M < Mcr:
        Cdmisc = 0
    elif Mcr <= M <= Mdd:
        Cdmisc = 0.002*(1 +2.5((Mdd - M)/0.05))**-1
    else:
        Cdmisc = 0.002*(1 +2.5((M - Mdd)/0.05))**2.5
    return Cdmisc


