from math import pi, cos, sqrt, acos, degrees, atan, tan, exp
import CruiseConditions as cc
import itertools
import numpy as np

"""Constants"""
wet_wing_area = 6.2
C_f = 0.0026
CLDesign = 0.7166
wingArea = 478.4128045201612
mCruise = 0.82
tsfc = 14.491608875351323
vcruise = mCruise*295.070
rho = 0.316406

quarterSweep = acos(1.16/(mCruise+0.5))

#tr = -0.0083*degrees(quarterSweep)+0.4597

#pitchup = 17.7*(2-tr)*exp(-0.043*degrees(quarterSweep))

def sar(ar, tr):
    pu = 17.7*(2-tr)*exp(-0.043*degrees(quarterSweep))
    if ar > pu:
        return 0
    b = sqrt(ar*wingArea)
    cRoot = (2*wingArea)/(b*(1+tr))
    leSweep = atan(tan(quarterSweep)+0.5*cRoot/b*(1-tr))

    Cdmisc = 0.002/(1+2.5*(cc.M_dd(0.72, leSweep, tc=0.1)-mCruise)/0.05)
    #oswald = 4.61*(1-0.045*ar**0.68)*(cos(leSweep))**0.15-3.1
    oswald = 1/(pi*ar*0.0075+1/0.97)
    cd0 = wet_wing_area*C_f
    cd = cd0+(CLDesign**2)/(pi*ar*oswald)+Cdmisc
    d = 0.5*rho*(vcruise**2)*wingArea*cd
    r = vcruise/(d*tsfc)
    return r

ars = np.linspace(9, 15, 1000)
trs = np.linspace(0.1, 0.2, 2000)
combs = list(itertools.product(ars, trs))



optimal = 0
for pair in combs:
    r = sar(pair[0], pair[1])
    if r > optimal:
        optimal = r
        ar = pair[0]
        tr = pair[1]

print(optimal)
print(ar)
print(tr)
# b = sqrt(ar*wingArea)
# cRoot = (2*wingArea)/(b*(1+tr))
# leSweep = atan(tan(quarterSweep)+0.5*cRoot/b*(1-tr))
# Cdmisc = 0.002/(1+2.5*(cc.M_dd(0.72, leSweep, tc=0.1)-mCruise)/0.05)
# #oswald = 4.61*(1-0.045*ar**0.68)*(cos(leSweep))**0.15-3.1
# oswald = 1/(pi*ar*0.0075+1/0.97)
# cd0 = wet_wing_area*C_f
# cd = cd0+(CLDesign**2)/(pi*ar*oswald)+Cdmisc
# d = 0.5*rho*(vcruise**2)*wingArea*cd
# print(b)
# print(cRoot)
# print(leSweep)
# print(d)


# steps = 0.01
# current = 0
# sr = 0
# while current < pitchup-steps:
#     current = current + steps
#     r = sar(current)
#     if r > sr: 
#         ar = current
#         sr = r

# print(sr, current)


