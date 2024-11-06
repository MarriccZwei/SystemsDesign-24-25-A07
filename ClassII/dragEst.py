if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING

import numpy as np
import General.Constants as consts

def Reynolds(rho, l, M):
    k = 0.634*10**(-5) #smooth paint assumption
    return min(rho*l*M*consts.CRUISESOUNDSPEED/consts.CRUISEVISCOSITY, 44.62*(l/k)**1.053*M)

def Cf(Reynolds, laminarFraction, M):
    return laminarFraction*1.328/np.sqrt(Reynolds)+(1-laminarFraction)*.455/(np.log10(Reynolds))**2.58/(1+0.144*M**2)**0.65

def FFfus(L, D): #add other parameters
    f = L/D
    return 1+60/f**3+f/400

def FFwing(tcmaxpos, tc, M, sweepAtmaxT): #use the sweep formula to calculate sweep_m
    return (1+.6/tcmaxpos*tc+100*tc**4)*(1.34*M**.18*np.cos(sweepAtmaxT)**.28)

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


