import json
import math
import rollIntegral

def tau(chordRatio): #this is an approximation of the chart in the slides; it is not perfectly accurate, especially for x<0.2
    x = chordRatio #aileron chord / total chord
    if x<0.05:
        return x*4
    elif x<0.4:
        return (x*4/3) + (2 * 0.2 / 3)
    elif x<0.4:
        return x - 0.2
    elif x<0.7:
        return (2 * x / 3) + (10 / 3)

#b1 and b2 are the spanwise locations of the start + end of the aileron
def rollRate(b1, b2, chordRatio, deflection = 10, diffRatio = 1):
    if diffRatio != 1:
        deflection = 0.5 * (1 + diffRatio)

    clalpha = 0.08 #TODO change
    
    mainData = json.load(open("Protocols/main.json"))
    area = mainData["S"]
    cd0 = mainData["Cd0"]
    moment =24404723 #TODO: change
    span = math.sqrt( mainData["S"] * mainData["AR"] )

    Clda = 2 * clalpha * tau(chordRatio) / (area * span) * rollIntegral.Integral1(b1,b2)[0] #TODO multiply by integral (b1, b2){ c(y) * y}dy
    Clp = -4 * (clalpha + cd0) / (area * span * span) * rollIntegral.Integral2()[0]#TODO multiply by integral (0, b/2){ c(y) * y2}dy
    rate = -1 * Clda/Clp * deflection * 2 * moment / span
    print(rate)
    return rate

rollRate(7, 17, 0.33)