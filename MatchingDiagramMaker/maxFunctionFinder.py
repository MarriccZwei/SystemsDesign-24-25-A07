import numpy as np
import constraints

#returns (W/S, function 1, function 2)
def maxFunctionFinder():
    allFunctions = [] #constains lists of the values of each function for all values of W/S
    maxFunction = [] #contains a list of the index of the function with the biggest value at each W/S
    WSaxis = np.linspace(1, 10000, 10000)
    i=0
    for constraint in constraints.constraints: 
        allFunctions.append(constraint(WSaxis)[1]) #writes values to allFunctions
        #print(constraint(WSaxis))
        i=i+1
    for j in range(10000): #finds the functions with the biggest value at each W/S
        biggest = 0
        maxFunction.append(0)
        for k in range(len(constraints.constraints)):
            if allFunctions[k][j] > biggest and allFunctions[k][j] <=2:
                maxFunction[j] = k
                biggest = allFunctions[k][j]
    #print("Maximum functions index list")
    #print(maxFunction)

    crossPoints = []
    for m in range(len(maxFunction)-1):# finds all crossover points and which functions cross, then writes it to list "crossPoints"
        if maxFunction[m] != maxFunction[m+1]:
            cross = (m+1, maxFunction[m], maxFunction[m+1]) #W/S co-ord and the indexes of the two functions
            crossPoints.append(cross)
    print(crossPoints)
    return(crossPoints)