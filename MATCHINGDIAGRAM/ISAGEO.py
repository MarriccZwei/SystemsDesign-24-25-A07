import numpy as np
def temperature(alt, dT=0):
    if alt <= 11000:
        t = 288.15+dT-0.0065*alt
    else: t =288.15+dT-0.0065*11000
    return t

def pressure(alt):
    if alt <= 11000:
        p = 101325*(1+(-0.0065*alt)/288.15)**(-9.81/(-0.0065*287))
    else: 
        ptp = 101325*(1+(-0.0065*11000)/288.15)**(-9.81/(-0.0065*287))
        p = ptp * np.exp(-9.81*(alt-11000)/(287*temperature(alt)))
    return p

def density(alt, dT=0):
    rho = pressure(alt)/(287*temperature(alt, dT))
    return rho

def speedOfSound(alt, dT=0):
    a= np.sqrt(1.4*287*temperature(alt, dT))
    return a

if __name__ == "__main__":
    altit = 1600
    dT = 15
    print(temperature(altit, dT))
    print(pressure(altit))
    print(density(altit, dT))