if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING

import OOP.Planform as pf
import numpy as np

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

def fus_mass(): #the fuselage mass
    pass

def tail_mass():
    pass

def lg_mass():
    pass