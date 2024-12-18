if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
    import matplotlib.pyplot as plt

import OOP.Planform as pf
import OOP.FlexBox as fb
from typing import Dict, List, Tuple
import numpy as np
import General.Constants as c

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
        self.inboardFrame = fb.FlexBox(planform, wingboxThicknesses, startPos, midSpar)
        self.outboardFrame = fb.FlexBox(planform, wingboxThicknesses, endPos, midSpar)

        #creation of the edges dictionary
        def multipleDictsAdd(dict, spar, skin):
            dict[spar+'i'+skin]=self.inboardFrame.coords[spar+skin]
            dict[spar+skin+'i']=self.inboardFrame.coords[spar+skin]
            dict[skin+spar+'i']=self.inboardFrame.coords[spar+skin]
            dict[skin+'i'+spar]=self.inboardFrame.coords[spar+skin]
            dict['i'+skin+spar]=self.inboardFrame.coords[spar+skin]
            dict['i'+spar+skin]=self.inboardFrame.coords[spar+skin]

            dict[spar+'o'+skin]=self.outboardFrame.coords[spar+skin]
            dict[spar+skin+'o']=self.outboardFrame.coords[spar+skin]
            dict[skin+spar+'o']=self.outboardFrame.coords[spar+skin]
            dict[skin+'o'+spar]=self.outboardFrame.coords[spar+skin]
            dict['o'+skin+spar]=self.outboardFrame.coords[spar+skin]
            dict['o'+spar+skin]=self.outboardFrame.coords[spar+skin]

        self.vertices = dict()
        multipleDictsAdd(self.vertices, 'f', 't')
        multipleDictsAdd(self.vertices, 'f', 'b')
        if self.midSpar != None:
            multipleDictsAdd(self.vertices, 'm', 't')
            multipleDictsAdd(self.vertices, 'm', 'b')
        multipleDictsAdd(self.vertices, 'r', 't')
        multipleDictsAdd(self.vertices, 'r', 'b')

        #creation of the edges dictionary
        self.edges = dict()

        def lenAppend(dict, element):
            dict['i'+element] = self.inboardFrame.lengths[element]
            dict[element+'i'] = self.inboardFrame.lengths[element]
            dict['o'+element] = self.outboardFrame.lengths[element]
            dict[element+'o'] = self.outboardFrame.lengths[element]

        lenAppend(self.edges, 'f')
        if self.midSpar != None: lenAppend(self.edges, 'm') 
        lenAppend(self.edges, 'r')
        lenAppend(self.edges, 't')
        lenAppend(self.edges, 'b')

        #inboard to outboard distances along the skin
        def inboutb_lenAppend(dict, surf1):
            #intersect with bottom skin
            vertex1 = self.vertices["o"+surf1+'b']
            vertex2 = self.vertices["i"+surf1+'b']
            distance = np.sqrt((vertex1[0]-vertex2[0])**2-(vertex1[1]-vertex2[1])**2)
            dict[surf1+'b'] = distance
            dict['b'+surf1] = distance
            #intersect with top skin
            vertex1 = self.vertices["o"+surf1+'t']
            vertex2 = self.vertices["i"+surf1+'t']
            distance = np.sqrt((vertex1[0]-vertex2[0])**2-(vertex1[1]-vertex2[1])**2)
            dict[surf1+'t'] = distance
            dict['t'+surf1] = distance
        
        inboutb_lenAppend(self.edges, 'f')
        inboutb_lenAppend(self.edges, 'r')
        if self.midSpar != None: 
            inboutb_lenAppend(self.edges, 'm') #if there is a midspar

        #calculating the amount of stringers
        averageLenTop = (self.edges['it']+self.edges['ot'])/2
        averageLenBot = (self.edges['ib']+self.edges['ob'])/2
        #obtained by dividing the length available for stringers by stringer spacing
        self.stringerNumTop = int((averageLenTop-stringerDesign['w'])/stringerDesign['st'])
        self.stringerNumBot = int((averageLenBot-stringerDesign['w'])/stringerDesign['sb'])
        self.stringerNum = self.stringerNumTop+self.stringerNumBot #total number of stringers
        #since we only use one type of stringer, the area of 1 stringer is:
        self.stringerArea = stringerDesign['t']*(stringerDesign['w']+stringerDesign['h']-stringerDesign['t'])

        #Assessing the cell materialVolume (without rib contributions)
        self.materialVolume = self.stringerNum*self.zLen*self.stringerArea #stringer contributions
        
        def sheet_volume(spar): #defining sheet contribution
            return (self.edges[spar+'o']+self.edges[spar+'i'])*self.zLen/2*self.wingboxThicknesses[spar]
        #evaluating sheet contributions
        self.materialVolume += sheet_volume('f')+sheet_volume('r') #main spars
        if self.midSpar != None: #midspar (if present)
            self.materialVolume += sheet_volume('m')
        self.materialVolume += sheet_volume('t')+sheet_volume('r') #skins

        #Cell weight estimation (without rib contributions)
        self.mass = c.DENSITY*self.materialVolume
        self.weight = c.G*self.mass
        

    def spanwisePos(self, position):
        return self.startPos+position*(self.endPos-self.startPos)

    def wingbox(self, position):
        return fb.FlexBox(self.planform, self.wingboxThicknesses, self.spanwisePos(position), self.midSpar)
    
    #returns the lists of stringer positions on top and on the bottom of the wingbox
    def _stringer_positions(self, position):
        wingbox = self.wingbox(position)
        wbpts = wingbox.coords
        if self.midSpar==None:
            stringerPosTop = self._stringers_along_a_line(wbpts['ft'], wbpts['rt'], self.stringerNumTop, self.stringerDesign['w'])
            stringerPosBot = self._stringers_along_a_line(wbpts['fb'], wbpts['rb'], self.stringerNumBot, self.stringerDesign['w'])
        else:
            #we need to determin the nyumber of stringers to go before and after the mid spar
            #we do it via a ratio of subcell top length to total top length
            wblns = wingbox.lengths
            nStrBefroreMTop = int(round(wblns['ft']/wblns['t']*self.stringerNumTop))
            nStrAfterMTop = int(round(wblns['rt']/wblns['t']*self.stringerNumTop))
            nStrBefroreMBot = int(round(wblns['fb']/wblns['b']*self.stringerNumBot))
            nStrAfterMBot = int(round(wblns['rb']/wblns['b']*self.stringerNumBot))
            #creating the stringer position list assuming equally spaced stringers in each subcell
            stringerPosTop = self._stringers_along_a_line(wbpts['ft'], wbpts['mt'], nStrBefroreMTop, self.stringerDesign['w'])+self._stringers_along_a_line(wbpts['mt'], wbpts['rt'], nStrAfterMTop, self.stringerDesign['w'])
            stringerPosBot = self._stringers_along_a_line(wbpts['fb'], wbpts['mb'], nStrBefroreMBot, self.stringerDesign['w'])+ self._stringers_along_a_line(wbpts['mb'], wbpts['rb'], nStrAfterMBot, self.stringerDesign['w'])
        return stringerPosTop, stringerPosBot

    def sectionProperties(self, position):
        '''Returns a dictionary of section properties, such as moment of inertia "ixx" or centroid "xbar"/"ybar"
        Taking into account the wingbox sheets and stringers'''
        wingbox = self.wingbox(position)
        wbvertices = wingbox.coords
        wbt = wingbox.thicknesses

        #getting positions and moments of Area
        strPosesTop, strPosesBot = self._stringer_positions(position)
        strPoses = strPosesBot+strPosesTop #positions of all stringers, cuz we simply sum it for computing the moment of area
        wbareaMx = wingbox.centroidComponent[0]
        wbareaMy = wingbox.centroidComponent[1]

        #getting centroid properties - stringer treated as pt areas
        strAreaMomentX, strAreaMomentY = 0, 0
        for pos in strPoses:
            strAreaMomentX += self.stringerArea*pos[0]
            strAreaMomentY += self.stringerArea*pos[1]
        #xbar and ybar expressions have a common denominator - sum of areas
        denominator = wingbox.areas["tot"]+self.stringerNum*self.stringerArea
        xbar = (wbareaMx+strAreaMomentX)/denominator
        ybar = (wbareaMy+strAreaMomentY)/denominator
        
        #moments of inertia
        def moicontrib(point1:Tuple[float,float], point2:Tuple[float,float], thickness:float, ixx_contr:List[float], iyy_contr:List[float]): #sheet contributions
            midpoint = ((point1[0]+point2[0])/2,(point1[1]+point2[1])/2)
            xdist = point1[0]-point2[0]
            ydist = point1[1]-point2[1]
            L = np.sqrt(xdist**2+ydist**2) #point to point distance
            ixx_contr.append(L*thickness*ydist**2/12 + L*thickness*(midpoint[1]-ybar)**2)
            iyy_contr.append(L*thickness*xdist**2/12 + L*thickness*(midpoint[0]-xbar)**2)
        
        sheetcontribsX, sheetcontribsY = list(), list() #moment contributions from sheets
        moicontrib(wbvertices["ft"], wbvertices["fb"], wbt["f"], sheetcontribsX, sheetcontribsY) #front spar
        moicontrib(wbvertices["rt"], wbvertices["rb"], wbt["r"], sheetcontribsX, sheetcontribsY) #rear spar
        moicontrib(wbvertices["ft"], wbvertices["rt"], wbt["t"], sheetcontribsX, sheetcontribsY) #top skin
        moicontrib(wbvertices["rb"], wbvertices["fb"], wbt["b"], sheetcontribsX, sheetcontribsY) #bottom skin
        if self.midSpar != None: #midSpar contribution
            moicontrib(wbvertices["ft"], wbvertices["fb"], wbt["f"], sheetcontribsX, sheetcontribsY)
        ixx, iyy = sum(sheetcontribsX), sum(sheetcontribsY) #summing to obtain moments of inertia

        #stringer contributions - parallel axis only
        for pos in strPoses:
            ixx += self.stringerArea*(pos[1]-ybar)**2
            iyy += self.stringerArea*(pos[0]-xbar)**2

        return {'xbar': xbar, 'ybar': ybar, 'ixx': ixx, 'iyy': iyy}


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
    
    def stringers(self, position):
        '''Returns a dictionary of stringer positions and properties'''
        strPosesTop, strPosesBot = self._stringer_positions(position)
        strPoses = strPosesTop+strPosesBot
        widthSideSegment = self.stringerDesign['w']-self.stringerDesign['t']
        #2*rectangle, 2*parallel axis
        iBucklAxis = self.stringerDesign['t']**3*widthSideSegment/12+self.stringerDesign['t']*widthSideSegment*self.stringerDesign['t']**2/4
        + self.stringerDesign['t']*self.stringerDesign['h']**3/12+self.stringerDesign['t']*self.stringerDesign['h']**3/4 #not necessarily thin walled
        return{'p':strPoses, 'pb':strPosesBot, 'pt':strPosesTop, 'A':self.stringerArea, 't':self.stringerDesign['t'], 'h':self.stringerDesign['h'], 
               'ib':iBucklAxis, 'n':self.stringerNum, 'nb':self.stringerNumBot, 'nt':self.stringerNumTop} #all stringer information in 1 splace

if __name__ == "__main__": #tests
    planform =pf.Planform(251.3429147793505, 9.872642920666417, 0.1, 28.503510117080133, 2.1496489882919865, False)
    halfspan = planform.b/2
    mWing = 22962.839350654576
    mEngine = 3554.759960907367/2 #divide by two as we are looking at the half-span only
    thrust = 91964.80101516769
    wgboxArea = 123.969 #[m^2] measured in CATIA

    cell1 = Cell(planform, 10, 11, {'w':0.05, 'h':0.05, 't':0.005, 'st':0.1, 'sb':0.13}, {'f':0.006, 'b':0.011, 'r':0.006, 't':0.011})
    print(cell1._stringers_along_a_line((1, 1), (-1, -1), 10, 0.01))
    print(cell1.spanwisePos(0.5))
    print(cell1.edges)

    cell2 = Cell(planform, 20, 21.3, {'w':0.05, 'h':0.05, 't':0.005, 'st':0.1, 'sb':0.13}, {'f':0.004, 'b':0.012, 'r':0.004, 't':0.012, 'm':0.004}, 0.4)

    def plotcell(cell1:Cell, mids:bool, row:int):
        row-=1 #to get zero at first raw to make the numeration align
        plt.subplot(2, 3, 3*row+1)
        plt.plot([cell1.vertices["ift"][0], cell1.vertices["irt"][0], cell1.vertices["irb"][0], cell1.vertices["ifb"][0], cell1.vertices["ift"][0]],
                [cell1.vertices["ift"][1], cell1.vertices["irt"][1], cell1.vertices["irb"][1], cell1.vertices["ifb"][1], cell1.vertices["ift"][1]])
        if mids: plt.plot([cell1.vertices["imt"][0], cell1.vertices["imb"][0]], [cell1.vertices["imt"][1], cell1.vertices["imb"][1]])
        stringers = cell1.stringers(0)
        sectionProperties = cell1.sectionProperties(0)
        plt.plot(sectionProperties["xbar"], sectionProperties["ybar"], 'bx')
        for point in stringers['p']: plt.plot(point[0], point[1], 'rx')
        plt.title("Inboard")
        plt.subplot(2, 3, 3*row+2)
        plt.plot([cell1.vertices["oft"][0], cell1.vertices["ort"][0], cell1.vertices["orb"][0], cell1.vertices["ofb"][0], cell1.vertices["oft"][0]],
                [cell1.vertices["oft"][1], cell1.vertices["ort"][1], cell1.vertices["orb"][1], cell1.vertices["ofb"][1], cell1.vertices["oft"][1]])
        if mids: plt.plot([cell1.vertices["omt"][0], cell1.vertices["omb"][0]], [cell1.vertices["omt"][1], cell1.vertices["omb"][1]])
        sectionProperties = cell1.sectionProperties(1)
        plt.plot(sectionProperties["xbar"], sectionProperties["ybar"], 'bx')
        stringers = cell1.stringers(1)
        for point in stringers['p']: plt.plot(point[0], point[1], 'rx')
        plt.title("Outboard")
        plt.subplot(2, 3, 3*row+3)
        plt.plot([cell1.spanwisePos(0), cell1.spanwisePos(0), cell1.spanwisePos(1), cell1.spanwisePos(1), cell1.spanwisePos(0)],
                [cell1.vertices["ift"][1], cell1.vertices["ifb"][1], cell1.vertices["ofb"][1], cell1.vertices["oft"][1], cell1.vertices["ift"][1]])
        plt.plot([cell1.spanwisePos(0), cell1.spanwisePos(0), cell1.spanwisePos(1), cell1.spanwisePos(1), cell1.spanwisePos(0)],
                [cell1.vertices["irt"][1], cell1.vertices["irb"][1], cell1.vertices["orb"][1], cell1.vertices["ort"][1], cell1.vertices["irt"][1]])
        plt.title("Side View")
    plotcell(cell1, False, 1)
    plotcell(cell2, True, 2)
    sps1, sps2 = cell1.sectionProperties(0.3), cell2.sectionProperties(0.3)
    print(f"@0.3 of cell: cell1 ixx: {sps1["ixx"]}, cell1 iyy:{sps1["iyy"]}, cell2 ixx: {sps2["ixx"]}, cell21 iyy:{sps2["iyy"]}")
    plt.show()
