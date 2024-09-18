from math import acos, sqrt

def MaxSweep(W, Clmax, S, VTO, RhoTO): #maximum quarter chord sweep angle based on take-off considerations
    SweepMax = acos((sqrt((2*W)/(Clmax*RhoTO*S))) / (VTO))
    return SweepMax

def SweepEst(MCruise): #estimate of quarter chord sweep angle based on ADSEE reader
    SweepEst = acos((1.1)/(MCruise + 0.5))
    return SweepEst
