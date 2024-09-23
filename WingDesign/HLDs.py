import numpy as np
from math import tan, cos, radians, sqrt

targetDeltaCL = 0.9

deltaFlap = 50
flapFactor = 0.35

surface = 409
sweepLE = radians(31)
sweepTE = radians(19)

cRoot = 8.12

def deltaCl(delta, factor):
    dcCf = 0.01*delta + 0.4

    return 1.6 * (1+factor*dcCf)

def flapSurface():
    return ((targetDeltaCL*surface)/(0.9*deltaCl(deltaFlap, flapFactor)*cos(sweepTE)))

print(flapSurface())
a = tan(sweepTE)-0.5*tan(sweepTE)-0.5*tan(sweepLE)
b = cRoot
c = -0.5*flapSurface()
y = (-b+sqrt(b**2 -4*a*c))/(2*a)
print(y)





