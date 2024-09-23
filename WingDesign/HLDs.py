import numpy as np
from math import tan, cos

targetDeltaCL = 1.9

deltaFlap = 50
flapFactor = 0.35

surface = 409
sweepLE = 0.5487971935252399
sweepTE = 0.3

cRoot = 8.12

def deltaCl(delta, factor):
    dcCf = 0.01*delta + 0.4
    return 1.6 * (1+factor*dcCf)

def flapSurface():
    return targetDeltaCL*surface/(0.9*deltaCl(deltaFlap, flapFactor)*cos(sweepTE))

a = tan(sweepTE)-0.5*tan(sweepTE)-0.5*tan(sweepLE)
coeff = np.array([2*a, 2*cRoot, -1*flapSurface()])
roots = np.polynomial.polynomial.polyroots(coeff)
print(roots)





