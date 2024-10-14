if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())

from General import Constants
from math import acos, degrees, radians, exp

testMach = Constants.CRUISEMACH

def sweep(mach):
    return degrees(acos(1.16/(mach+0.5)))

def taper(mach):
    return 0.2*(2-radians(sweep(mach)))

def aspect(mach):
    return 17.7 * (2 - taper(mach)) * exp(-0.043 * sweep(mach))

print(sweep(testMach))
print(taper(testMach))
print(aspect(testMach))