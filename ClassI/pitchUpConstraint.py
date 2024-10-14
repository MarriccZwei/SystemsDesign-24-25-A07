#INP: MACH
#OUT: taper, sweep, aspect

if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())

import json
from General import Constants
from math import acos, degrees, radians, exp

testMach = Constants.CRUISEMACH

def sweep(mach):#from ADSEE I reader
    return (acos(1.16/(mach+0.5)))

def taper(mach):#from ADSEE I reader
    return 0.2*(2-(sweep(mach)))

def aspect(mach):
    return 17.7 * (2 - taper(mach)) * exp(-0.043 * sweep(mach))

def sweepTaperAspect(mack):
    return sweep(testMach),taper(testMach),aspect(testMach)