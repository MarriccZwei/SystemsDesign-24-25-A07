from math import tan, pi

def MACCalculation(LambdaLE, LambdaTEin, LambdaTEout, b, bk, bo, CRoot, CTip, SGiven):
    CMid = CRoot + 0.5*bk*(tan(LambdaTEin) - tan(LambdaLE))
    SIn = 0.5*bk*(CRoot-(bk/4)*tan(LambdaLE) + (bk/4)*tan(LambdaTEin)) #area of the inner part of the wing

    SOut = bo/2 * (CTip + (bo/4)*tan(LambdaLE) - (bo/4)*tan(LambdaTEout)) #area of the outer part of the wing
    S = SIn + SOut #total wing area

    if not abs(S - SGiven) <= 1:
        print("the wing planform is not correct")

    TaperRatio_in = CMid/CRoot 
    TaperRatio_out = CTip/CMid

    MACIn = 2/3 * CRoot * ((1 + TaperRatio_in + TaperRatio_in**2) / (1 + TaperRatio_in)) #mean aerodynamic cord of the inner part of the wing
    MACOut = 2/3 * CMid * ((1 + TaperRatio_out + TaperRatio_out**2) / (1 + TaperRatio_out)) #mean aerodynamic cord of the outer part of the wing
    MAC = ((SIn * MACIn + SOut * MACOut) / S) #Mean aerodynamic chord of the wing

    YMACIn = (bk/6) * ((1 + 2*TaperRatio_in) / (1+ TaperRatio_in))
    YMACOut = (bo/6) * ((1+2*TaperRatio_out) / (1 + TaperRatio_out))

    XLEMAC = ((YMACIn * tan(LambdaLE) * SIn + (0.5*bk*tan(LambdaLE) + YMACOut * tan(LambdaLE)) * SOut)/S)

    YMAC = ((YMACIn * SIn + (0.5*bk + YMACOut)*SOut)/S)

    print(MAC)
    print(XLEMAC)
    print(YMAC)


#variables to find the area of the wing
#LambdaLE = 33.69 * (pi/180)#sweep angle of the leading edge of the wing
#LambdaTEin = 9.4623222 * (pi/180)#sweep angle of the trailing edge of the inner wing
#LambdaTEout = 26.565 * (pi/180)#sweep angle of the trailing edge of the outer wing

#b = 16 # total wing span
#bk = 3*2 #wing span of the inner part of the wing
#bo = b - bk #wing span of the outer part of the wing
#CRoot = 3 #root chord length

#CTip = 0.75 #tip chord length

#SGiven = 51.26

#MACCalculation(LambdaLE, LambdaTEin, LambdaTEout, b, bk, bo, CRoot, CTip, SGiven)


