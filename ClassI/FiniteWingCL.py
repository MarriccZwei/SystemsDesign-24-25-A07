from math import pi, sqrt, atan, tan

def DATCOM(A, M, LambdaHalf):
    CLAlpha = ((2 * pi * A)/(2 + sqrt( 4 + (A*sqrt(1-M)/0.95)**2) * (1 + (atan(LambdaHalf)**2)/(1-M) )))

b = 10
CTip = 1.6
CRoot = 4
LambdaQuarter = 30 * (pi/180)

Ltot = CTip + 0.5* (0.5*(CTip - CRoot) - b*tan(LambdaQuarter))

L1 = Ltot - 0.5*(CRoot + CTip)

LambdaHalf = atan(2*L1/b)
print(Ltot)