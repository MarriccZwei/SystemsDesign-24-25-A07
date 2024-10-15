if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING

from math import cos
from General import Constants as c
from ClassIV.clFunctions import maxCL, dCLdAlpha
from OOP.Planform import Planform
from OOP.HLDs import HLDs

def CLClean(planform: Planform, alpha=0, mach=c.LANDMACH, onlymax=False):
    if onlymax: return maxCL(c.CLMAXAIRFOIL, planform, mach)
    else:
        dCda = dCLdAlpha(mach, planform)
        cL = dCda*(alpha-c.ALPHAZEROLIFT)
        return cL


def CLLand(planform: Planform, hld: HLDs, alpha, onlymax=False):
    cPrimeC = 1+c.DELTACCFLAND*hld.flapcfC
    if onlymax:
        cleanMax = CLClean(planform)
        deltaCLFlapped = 0.9*c.FLAPFACTOR*cPrimeC*hld.flapSflapped/planform.S*cos(planform.sweep_at_c_fraction(hld.backSparLoc))
        deltaCLKruger = 0.9*c.KRUGERDELTACL*hld.krugerSflapped/planform.S*cos(planform.sweep_at_c_fraction(hld.frontSparLoc))
        return cleanMax+deltaCLFlapped+deltaCLKruger
    else:
        dCLdAlphaClean = dCLdAlpha(c.LANDMACH, planform)
        deltaAlpha = c.DELTAALPHA0LLANDING*hld.flapSflapped(planform)/planform.S*cos(planform.sweep_at_c_fraction(hld.backSparLoc))
        sPrimeS = 1+(hld.flapSflapped(planform)/planform.S)*(cPrimeC-1)
        dCLdAlphaLand = sPrimeS*dCLdAlphaClean
        cl = dCLdAlphaLand*(alpha-c.ALPHAZEROLIFT+deltaAlpha)
        return cl
    
def CLTakeOff(planform: Planform, hld: HLDs, alpha, onlymax=False):
    cPrimeC = 1+c.DELTACCFTAKEOFF*hld.flapcfC
    if onlymax:
        cleanMax = CLClean(planform)
        deltaCLFlapped = 0.9*c.FLAPFACTOR*c.TAKEOFFHLDDEPLOYMENT*cPrimeC*hld.flapSflapped/planform.S*cos(planform.sweep_at_c_fraction(hld.backSparLoc))
        deltaCLKruger = 0.9*c.KRUGERDELTACL*c.TAKEOFFHLDDEPLOYMENT*hld.krugerSflapped/planform.S*cos(planform.sweep_at_c_fraction(hld.frontSparLoc))
        return cleanMax+deltaCLFlapped+deltaCLKruger
    else:
        dCLdAlphaClean = dCLdAlpha(c.LANDMACH, planform)
        deltaAlpha = c.DELTAALPHA0LTAKEOFF*hld.flapSflapped(planform)/planform.S*cos(planform.sweep_at_c_fraction(hld.backSparLoc))
        sPrimeS = 1+(hld.flapSflapped(planform)/planform.S)*(cPrimeC-1)
        dCLdAlphaTakeOff = sPrimeS*dCLdAlphaClean
        cl = dCLdAlphaTakeOff*(alpha-c.ALPHAZEROLIFT+deltaAlpha)
        return cl