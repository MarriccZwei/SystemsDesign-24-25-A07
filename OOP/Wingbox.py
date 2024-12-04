if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING

import unittest
import numpy as np
from Deflections import MoI as moi
from Deflections import MoISpanwise as moispan
from Deflections import Torsion as torsion
import Planform as pf
class Wingbox():
    def __init__(self, thicknessList:list, nStiffTop:int, nStiffBot:int, stiffArea, planform:pf.Planform,  accuracy:int = 256, midSpar:bool = False, midSparPos = 0.5, cutMidSpar = 10):
        self.tSkin = thicknessList[0]
        self.tFrontSpar = thicknessList[3]
        
        if midSpar:
            self.tRearSpar = thicknessList[5]
            self.tMidSpar =thicknessList[1]
            self.posMidSpar = midSparPos
            self.cutoff = cutMidSpar
        else:
            self.tRearSpar = thicknessList[1]
        
        self.nStiffTop = nStiffTop
        self.nStiffBot = nStiffBot
        self.stiffArea = stiffArea
        self. accuracy = accuracy
        self.b = planform.b
        self.cr = planform.cr
        self.tr = planform.TR
        self.frontSparPos = 0.2
        self.rearSparPos = 0.6
        self.positions = np.linspace(0,self.b/2, accuracy)
    
    def chord(self,z):
        c = self.cr - self.tr * (1 - self.tr) * (z / (self.b/2))
        return c 

    def centroid(self, z):
        pass

    def ixx(self):
        m = moispan.calculate_moments_of_inertia()

        chords = np.linspace(0, self.b/2, self.accuracy)
        mois = np.zeros(self.accuracy)

        i=0
        for k in mois:
            mois[i] = moispan.calculate_moments_of_inertia(chords[i], [0.2,0.6], self.tTop)
        pass

    def torstiff(self):
        
        pass

    def thicknesses(self):
        thicks = []
        for i in self.positions:
            if i>self.cutoff:
                thicks.append( (self.tSkin,self.tSpar,self.tSkin,self.tSpar,0,0,0) )
            else:
                thicks.append( (self.tSkin,self.tMidSpar,self.tSkin,self.tSpar,self.tSkin,self.tSpar,self.tSkin) )
        return thicks
    
    def xBars(self):
        pass

    def ybars(self):
        pass