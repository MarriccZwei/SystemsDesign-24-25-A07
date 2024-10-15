if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING

from math import sqrt, pi, tan
from General import Constants as c
from ClassIV.clFunctions import maxCL, dCLdAlpha
from OOP.Planform import Planform
from OOP.HLDs import HLDs

def CLClean(planform: Planform, alpha, mach, onlymax=False):
    if onlymax: return maxCL(c.CLMAXAIRFOIL, planform, mach)
    else:
        dCda = dCLdAlpha(mach, planform)
        cL = dCda*(alpha-c.ALPHAZEROLIFT)
        return cL


def CLLand(planform: Planform, hld: HLDs, alpha, onlymax=False):
    dCLdALPHACLEAN = dCLdAlpha(c.LANDMACH, planform)
    sPrimeS = 1+(hld.flapSflapped(planform)/planform.S)