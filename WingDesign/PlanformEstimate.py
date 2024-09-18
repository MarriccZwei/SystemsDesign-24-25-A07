from math import pi, sqrt, atan, tan, acos, e

def LambdaFinder(b, CTip, CRoot, LambdaQuarter): #finds all useful sweep angles based on quarter chord, for a single trapezoid wing
    Ltot = 0.25*(CRoot + 3*CTip) + 0.5*b*tan(LambdaQuarter) #total length of the wing
    L1 = Ltot - 0.5*(CRoot + CTip)
    L2 = Ltot - CTip
    L3 = Ltot - CRoot
    LambdaHalf = atan(2*L1/b)
    LambdaLE = atan(2*L2/b)
    LambdaTE = atan(2*L3/b)
    return [LambdaHalf, LambdaLE, LambdaTE]

def DATCOM(A, M, LambdaQuarter): #estimate of the reduction of lift slope
    LambdaHalf = LambdaFinder(LambdaQuarter)[0]
    CLAlpha = ((2 * pi * A)/(2 + sqrt( 4 + (A*sqrt(1-M)/0.95)**2) * (1 + (atan(LambdaHalf)**2)/(1-M) ))) #equation found in the ADSEE slides, L1
    return CLAlpha

def MAC(LambdaLE, LambdaTE, b, CRoot, CTip):
    S = 0.5 * b * (CRoot - (b/4)*tan(LambdaLE) + (b/4)*tan(LambdaTE))
    TaperRatio = CTip/CRoot

    MAC = 2/3 * CRoot * ((1+TaperRatio + TaperRatio**2)/(1+TaperRatio))
    YMAC = (b/6) * ((1 + 2*TaperRatio) / (1 + TaperRatio))
    XLEMAC = YMAC * tan(LambdaLE)

    return [MAC, YMAC, XLEMAC]


#print(LambdaHalf * (180/pi))
def SweepEst(MCruise): #estimate of quarter chord sweep angle based on ADSEE reader
    SweepEst = acos((1.16)/(MCruise + 0.5))
    return SweepEst

def TaperRatioEst(LambdaQuarter):
    TaperRatio = -0.0083* (LambdaQuarter * 180 / pi) + 0.4597
    return TaperRatio

def WingSpan(AspectRatio, S):
    b = sqrt(AspectRatio*S)
    return b

def RootAndTipChord(S, Taper, b):
    Cr = (2*S)/((1+Taper)*b)
    Ct = Taper*Cr
    return [Cr, Ct]

def Dihedral(QuarterSweep):
    dihedral = 3 - 0.1 * (QuarterSweep * 180 / pi) + 2 # plus two for low wing config
    return (dihedral * pi / 180)

def PitchUp(TaperRatio, QuarterSweep, AR):
    PitchUp = 17.7 * (2-TaperRatio) * e ** (-0.043 * (QuarterSweep * 180 / pi))
    if PitchUp <= AR:
        return True
    else:
        return False


#def MAC(LambdaLE, LambdaTEin, LambdaTEout, b, bk, CRoot, CTip, SGiven):
    bo = b - bk #finds the wing span of the outer wing
    CMid = CRoot + 0.5*bk*(tan(LambdaTEin) - tan(LambdaLE)) #finds the chord length at the kink of the wing
    SIn = 0.5*bk*(CRoot-(bk/4)*tan(LambdaLE) + (bk/4)*tan(LambdaTEin)) #area of the inner part of the wing

    SOut = bo/2 * (CTip + (bo/4)*tan(LambdaLE) - (bo/4)*tan(LambdaTEout)) #area of the outer part of the wing
    S = SIn + SOut #total wing area

    if not abs(S - SGiven) <= 1: #checks if the given total area equals the calculated area
        print("the wing planform is not correct")

    TaperRatio_in = CMid/CRoot #finds the taper ratio of the inner part of the planform
    TaperRatio_out = CTip/CMid #finds the taper ratio of the outer part of the planform

    MACIn = 2/3 * CRoot * ((1 + TaperRatio_in + TaperRatio_in**2) / (1 + TaperRatio_in)) #mean aerodynamic chord of the inner part of the wing
    MACOut = 2/3 * CMid * ((1 + TaperRatio_out + TaperRatio_out**2) / (1 + TaperRatio_out)) #mean aerodynamic chord of the outer part of the wing
    MAC = ((SIn * MACIn + SOut * MACOut) / S) #Mean aerodynamic chord of the wing

    YMACIn = (bk/6) * ((1 + 2*TaperRatio_in) / (1+ TaperRatio_in)) #finds the length to the inner MAC from the center line
    YMACOut = (bo/6) * ((1+2*TaperRatio_out) / (1 + TaperRatio_out)) #finds the length to the outer MAC from the Middle chord
    YMAC = ((YMACIn * SIn + (0.5*bk + YMACOut)*SOut)/S)
    XLEMAC = ((YMACIn * tan(LambdaLE) * SIn + (0.5*bk*tan(LambdaLE) + YMACOut * tan(LambdaLE)) * SOut)/S) #finds the length to the leading edge of the MAC from the LE of the root chord

    return [MAC, XLEMAC, YMAC] #returns the three important variables