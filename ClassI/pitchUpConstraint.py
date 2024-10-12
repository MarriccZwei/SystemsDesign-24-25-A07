from math import acos, degrees, radians, exp

testMach = 0.82 #TODO delete

def sweep(mach):
    return degrees(acos(1.16/(mach+0.5)))

def taper(mach):
    return 0.2*(2-radians(sweep(mach)))

def aspect(mach):
    return 17.7 * (2 - taper(mach)) * exp(-0.043 * sweep(mach))

print(sweep(testMach))
print(taper(testMach))
print(aspect(testMach))