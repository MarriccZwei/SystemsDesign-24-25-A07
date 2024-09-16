from math import tan, pi

def MAC(LambdaLE, LambdaTEin, LambdaTEout, b, bk, CRoot, CTip, SGiven):
    bo = b - bk #finds the wing span of the outer wing
    CMid = CRoot + 0.5*bk*(tan(LambdaTEin) - tan(LambdaLE)) #finds the chord length at the kink of the wing
    SIn = 0.5*bk*(CRoot-(bk/4)*tan(LambdaLE) + (bk/4)*tan(LambdaTEin)) #area of the inner part of the wing

    SOut = bo/2 * (CTip + (bo/4)*tan(LambdaLE) - (bo/4)*tan(LambdaTEout)) #area of the outer part of the wing
    S = SIn + SOut #total wing area

    if not abs(S - SGiven) <= 1:
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