if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING

import OOP.Planform as pf
import OOP.FlexBox as fb
from typing import Dict
import numpy as np

class Cell:
    '''The representation of the wingbox between 2 ribs'''
    #startPos, endPos - spanwise location [m] from root, stringerDesign: the design decisions of the stringers, as a dict
    #wgboxThicknesses: the 'f', 'm', 'r', ... dict format 
    def __init__(self, planform:pf.Planform, startPos:float, endPos:float, stringerDesign:Dict[str,float], wingboxThicknesses:Dict[str,float],  midSpar=None):
        #saving the constructor parameters
        self.planform = planform
        self.startPos = startPos
        self.endPos = endPos
        self.stringerDesign = stringerDesign
        self.wingboxThicknesses = wingboxThicknesses
        self.midSpar = midSpar
        self.zLen = endPos-startPos
        
        #creation of inboard and outboard flex boxes
        self.inboardFrame = fb.FlexBox(startPos, planform, wingboxThicknesses, midSpar)
        self.outboardFrame = fb.FlexBox(endPos, planform, wingboxThicknesses, midSpar)

        #creation of the edges dictionary
        def multipleDictsAddIB(dict, spar, skin):
            dict[spar+'i'+skin]=self.inboardFrame.coords[spar+skin]
            dict[spar+skin+'i']=self.inboardFrame.coords[spar+skin]
            dict[skin+spar+'i']=self.inboardFrame.coords[spar+skin]
            dict[skin+'i'+spar]=self.inboardFrame.coords[spar+skin]
            dict['i'+skin+spar]=self.inboardFrame.coords[spar+skin]
            dict['i'+spar+skin]=self.inboardFrame.coords[spar+skin]

        self.edges = dict()
        multipleDictsAddIB(self.edges, 'f', 't')
        multipleDictsAddIB(self.edges, 'f', 'b')
        multipleDictsAddIB(self.edges, 'f', 't')
        multipleDictsAddIB(self.edges, 'f', 't')


    def spanwisePos(self, position):
        return self.startPos+position*(self.endPos-self.startPos)

    def wingbox(self, position):
        return fb.FlexBox(self.spanwisePos(position), self.planform, self.wingboxThicknesses, self.midSpar)
    
    def stringers(self, position):
        wingbox = self.wingbox(position)

    def _stringers_along_a_line(self, point1, point2, stringerN, stringerWidth):
        L = np.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2) #point to point distance
        xdistRatio = (point2[0]-point1[0])/L #point to point distance in x - a scaling factor for projections
        ydistRatio = (point2[1]-point1[1])/L #point to point distance in y - a scaling factor for projections

        #the ending term is the x coordinate of the second point, minus the x distance resulting from the last stringer width
        xPositions = np.linspace(point1[0], point2[0]-xdistRatio*stringerWidth, stringerN)
        yPositions = np.linspace(point1[1], point2[1]-ydistRatio*stringerWidth, stringerN)
        
        #converting the lists of coordinates into list of tuples containing the coords of each stringer
        stringerPositions = list()
        for i in range(stringerN):
            stringerPositions.append((xPositions[i], yPositions[i]))

        return stringerPositions

if __name__ == "__main__": #tests
    planform =pf.Planform(251.3429147793505, 9.872642920666417, 0.1, 28.503510117080133, 2.1496489882919865, False)
    halfspan = planform.b/2
    mWing = 22962.839350654576
    mEngine = 3554.759960907367/2 #divide by two as we are looking at the half-span only
    thrust = 91964.80101516769
    wgboxArea = 123.969 #[m^2] measured in CATIA

    cell1 = Cell(planform, 10, 11, {}, {})
    print(cell1._stringers_along_a_line((1, 1), (-1, -1), 10, 0.01))
    print(cell1.edges)
