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
    pass

SwWing = lambda S:2*1.07*S #Wetted Surface of any Wing Planform (can be a tail or pylon or wing)

ARe = lambda AR: AR+0.04 #effective aspect ratio for square wing tips

Oswald = lambda ARe:1/(0.0075*ARe*np.pi+1/.97) #the working formula - USE THE ARe

CDi = lambda CL, ARe: CL**2/ARe/np.pi/Oswald(ARe) #induced drag coefficient

def Cdmisc(M, ka, CL, Mcr = 0.6): #to change the Mcr value
    pass

