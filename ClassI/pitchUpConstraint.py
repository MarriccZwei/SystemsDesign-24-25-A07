if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())

from General import Constants
from math import acos, degrees, radians, exp

def sweep(mach):#from ADSEE I reader
    return (acos(1.16/(mach+0.5)))

def taper(mach):#from ADSEE I reader
    return 0.2*(2-(sweep(mach)))

def aspect(mach):
    return 17.7 * (2 - taper(mach)) * exp(-0.043 * sweep(mach))

def enforceAspectRatio(taper, sweep):
    return 17.7 * (2 - taper) * exp(-0.043 * sweep)

def sweepTaperAspect(mack):
    return sweep(mack),taper(mack),aspect(mack)