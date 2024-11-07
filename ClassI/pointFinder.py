import numpy as np
#import acparams
from ClassI import constraints
import matplotlib.pyplot as plt

# 0 Stall
# 1 Climb gradient I
# 2 Climb gradient II: Electric Boogaloo
# 3 Climb gradient III: Revenge of the CLmax
# 4 Climb gradient IV: The Climb Rate Strikes Back
# 5 Climb gradient V: Climbier Gradients
# 6 TO dist
# 7  Land dist
# 8 Cruise speed
# 9 Climb rate

def pointFinder(constraints, line1, line2, lowerBound=0, upperBound=10000):#upper and lower bounds are optional and do not *need* to be specified
    if lowerBound<0:
        lowerBound = 0
    if upperBound>10000:
        upperBound = 10000
    l1vert = False
    l2vert = False
    if line1 == 0 or line1 == 7:#handles cases where line 1 is vertical
        print(":3")
        l1vert = True
    if line2 == 0 or line2 == 7:#handles cases where line 2 is vertical
        print(":3")
        l2vert = True
    
    #constants from main (WL = wing loading)
    maxWL = 10000
    WLres = 10000
    
    intxInterval = np.linspace(1, maxWL, WLres)
    f = constraints[line1](intxInterval)
    g = constraints[line2](intxInterval)

    if l1vert == True:
        intx = f[0][0]
        intx = int(intx)
        inty = g[1][intx]
    
    elif l2vert == True:
        intx = g[0][0]
        intx = int(intx)
        inty = f[1][intx]
    
    else:
        h =[]
        for i in range(WLres):
            h.append(f[1][i] - g[1][i])
        stop = False
        j=lowerBound-1
        while j<upperBound and stop == False:
            j=j+1
            if abs(h[j] - h[j+1]) > abs(h[j]):
                stop = True
        
        intx = j
        if l1vert == True:
            inty = g[1][intx]
        else:
            inty = f[1][intx]
    if intx > 8500:
        pointName = "W/S: " + str(intx) + ", T/W: " + str(int(inty*10000)/10000) + "↘"
        plt.text(intx, inty, pointName, horizontalalignment = 'right', verticalalignment = 'bottom')
    else:
        pointName = "↙ W/S: " + str(intx) + ", T/W: " + str(int(inty*100)/100)
        plt.text(intx, inty, pointName, horizontalalignment = 'left', verticalalignment = 'bottom')
    plt.plot(intx, inty, '+r')
    return intx, inty