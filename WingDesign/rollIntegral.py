from math import tan, atan, radians
import scipy.integrate as integrate


cRoot = 8
cTip = 3
span = 20

# non kink vars
sweepLE = radians(45)

# kink vars
kSweep1LE = radians(45)
kSweep2LE = radians(30)
kSweepTE = radians(10)
yKink = 6
deltaLE = 1
deltaTE = 2


def c(y, b, LE, TE, cT):
    return (0.5*b*tan(LE) + cT - y*tan(LE) - (0.5*b-y)*tan(TE))

def f1(y, b, LE, TE, cT):
    return y*c(y, b, LE, TE, cT)

def f2(y, b, LE, TE, cT):
    return y**2 * c(y, b, LE, TE, cT)

def trailingSweep(LE, cT, cR, b):
    return atan(tan(LE)+(cT-cR)/(0.5*b))

def Integral1(b1, b2):
    sweepTE = trailingSweep(sweepLE, cTip, cRoot, span)
    return integrate.quad(lambda y: f1(y, span, sweepLE, sweepTE, cTip), b1, b2)



print(Integral1(8, 9.5))