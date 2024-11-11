if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING

import numpy as np
from math import sqrt
from General import Constants as c
from ClassIV.clFunctions import clDesign, dCLdAlpha
from General.generalFunctions import readExcelFile
from OOP.Planform import Planform

def alphaTrim(planform: Planform, wingloading, weightFuel):
    Cl0Alpha = c.ALPHAZEROLIFT
    designCL = clDesign(wingloading, weightFuel, planform)
    alpha = designCL/(dCLdAlpha(c.CRUISEMACH, planform) + Cl0Alpha)
    return alpha


def criticalMach(planform: Planform, wingloading, weightfuel):
    file = "cpAirfoil.xlsx"
    alpha = round(alphaTrim(planform, wingloading, weightfuel), 1)
    reynolds = '9e+06'
    alpha = str(alpha) + '0'
    df = readExcelFile(file)
    column = f'NACA64A210-Re={reynolds}-Alpha={alpha}-'
    cpList = df[column].tolist()
    cpList.sort()
    cpMin = cpList[0]
    m = 1/(sqrt(1-cpMin)*np.cos(planform.sweepLE))
    return m

def dragDivergenceMach(planform: Planform, wingLoading, weightFuel, ka = 0.935, streamwise=False):
    CLcruise = clDesign(wingLoading, weightFuel, planform)
    sweepLE = planform.sweepLE
    
    if streamwise: tc = c.THICKNESSTOCHORD*np.cos(sweepLE)
    else: tc = c.THICKNESSTOCHORD

    term1 = ka/np.cos(sweepLE)
    term2 = tc/np.cos(sweepLE)**2
    term3 = CLcruise/(10*(np.cos(sweepLE)**3))
    return term1 - term2 - term3