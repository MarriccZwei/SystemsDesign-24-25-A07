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
    def __init__(self, tFlange, tSpar, tMids, nStiffTop:int, nStiffBot:int, stiffArea, planform:pf.Planform,  accuracy:int = 256, midSpar:bool = False, midSparPos = 0.5, cutMidSpar = 10):
        self.tSkin = tFlange
        self.tSpar = tSpar
        
        if midSpar:
            self.tRearSpar = tSpar
            self.tMidSpar = tMids
            self.posMidSpar = midSparPos
            self.cutoff = cutMidSpar
        
        self.nStiffTop = nStiffTop
        self.nStiffBot = nStiffBot
        self.stiffArea = stiffArea
        self. accuracy = accuracy
        self.b = planform.b
        self.cr = planform.cr
        self.tr = planform.TR
        self.planform = planform
        self.frontSparPos = 0.2
        self.rearSparPos = 0.6
        self.positions = np.linspace(0,self.b/2, accuracy)
    
    def chord(self,z):
        c = self.cr - self.tr * (1 - self.tr) * (z / (self.b/2))
        return c 

    def centroid(self, z):
        pass

    def sectio_properties(self):
        #m = moispan.calculate_moments_of_inertia()

        #chords = np.linspace(0, self.b/2, self.accuracy)
        # mois = np.zeros(self.accuracy)

        # i=0
        # for k in mois:
        #     mois[i] = moispan.calculate_moments_of_inertia(chords[i], [0.2,0.6], self.tSkin)
        mois = list()
        xBars = list()
        yBars = list()
        for pos in self.positions:
            I_xx, I_yy, I_xy , x_bar, y_bar, num_upper_stringers, num_lower_stringers = moispan.calculate_moments_of_inertia(self.planform.chord_spanwise(pos), [0.4], self.tSkin, self.tFrontSpar, self.tMidSpar, 0.005, 0.0006)
            mois.append(I_xx)
            xBars.append(x_bar)
            yBars.append(y_bar)
        return np.array(mois), np.array(x_bar), np.array(y_bar)

    def torstiff(self):
        
        pass

    def thicknesses(self, pos):
        if pos>self.cutoff:
            return [(self.tSkin, self.tSpar, self.tSkin, self.tSpar)]
        else:
            return [(self.tSkin, self.tMidSpar, self.tSkin, self.tSpar), (self.tSkin, self.tSpar, self.tSkin, self.tMidSpar)]
    
    def xBars(self):
        return moi.centroid()

    def yBars(self):
        pass