
def tau(chordRatio):
    x = chordRatio
    if x<0.05:
        return x*4
    elif x<0.4:
        return (x*4/3) + (2 * 0.2 / 3)
    elif x<0.7:
        return x - 0.2
        
def rollRate(b1, b2, chordRatio, span, moment, clalpha, deflection, diffRatio):
    span = 50 #TEMPORTARY
    moment = 10000 #TEMPORARY
    area = 100 #TEMPORARY


    Clda = 2 * cl_alpha * tau / (area * span)

    Clp = 

    da = 
    rate = -1 * Clda/Clp * da * 2 * moment / span
    print(":3")