import numpy as np
from math import tan, cos, radians, sqrt

# Target DeltaCL when landing, with CL-max in clean configuration (1.6)
targetDeltaCL = 0.9

# Flap deflection suggested in ADSEE II Lecture 3
deltaFlap = 50  # [deg]

# This value can be between 0.35 and 0.40
flapFactor = 0.35


surface = 409  # Total wing surface
sweepLE = radians(31)
sweepTE = radians(19)

cRoot = 8.12  # [m]

# Calculates the AIRFOIL DeltaCl
def deltaCl(delta, factor):
    dcCf = 0.01*delta + 0.4

    return 1.6 * (1+factor*dcCf)

# Calculates the required flap surface. ATTENTION: Flap surface is not the area of the flaps itself! See ADSEE II Lecture 3 slides
def flapSurface():
    return ((targetDeltaCL*surface)/(0.9*deltaCl(deltaFlap, flapFactor)*cos(sweepTE)))


# ABC formula for calculation of spanwise position of flaps (they start at the root)
a = tan(sweepTE)-0.5*tan(sweepTE)-0.5*tan(sweepLE)
b = cRoot
c = -0.5*flapSurface()
y = (-b+sqrt(b**2 -4*a*c))/(2*a)


print('Flap Surface: ', round(flapSurface(), 1), '[m^2]')
print('Flap Lenght Spanwise: ', round(y, 1), '[m]')





