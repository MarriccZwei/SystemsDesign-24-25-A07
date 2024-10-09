from math import acos, degrees, radians, exp

cruiseMach = 0.82 #TODO 

def sweep (mach):
    return degrees(acos(1.16/(mach+0.5)))

def taper():
    return 0.2*(2-radians(sweep(cruiseMach)))

print(sweep(cruiseMach))
print(taper())