
def tau(chordRatio): #this is an approximation of the chart in the slides; it is not perfectly accurate, especially for x<0.2
    x = chordRatio
    if x<0.05:
        return x*4
    elif x<0.4:
        return (x*4/3) + (2 * 0.2 / 3)
    elif x<0.4:
        return x - 0.2
    elif x<0.7:
        return (2 * x / 3) + (10 / 3)
    
def rollRate(b1, b2, chordRatio, span, moment, clalpha, cd0, deflection = 10, diffRatio = 1):
    if diffRatio != 1:
        deflection = 0.5 * (1 + diffRatio)
    
    span = 50 #TEMPORTARY
    moment = 10000 #TEMPORARY
    area = 100 #TEMPORARY

    Clda = 2 * cl_alpha * tau(chordRatio) / (area * span) #TODO multiply by integral (b1,b2){ c(y) * y}dy

    Clp = -4 * (clalpha + cd0) / (area * span * span) #TODO multiply by integral (b1,b2){ c(y) * y}dy
    rate = -1 * Clda/Clp * deflection * 2 * moment / span
    print(":3")
    return rate