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
from Deflections.wingbox import wingbox
import OOP.Planform as pf
class Wingbox():
    def __init__(self, tFlange, tSpar, tMids, stiffArea, planform:pf.Planform,  accuracy:int = 256, midSpar:bool = False, midSparPos = 0.5, cutMidSpar = 10):
        self.tSkin = tFlange
        self.tSpar = tSpar
        self.midSpar = midSpar

        if midSpar:
            self.tMidSpar = tMids
            self.posMidSpar = midSparPos
            self.cutoff = cutMidSpar
        else:
            self.tMidSpar = 0
            self.posMidSpar = 0
            self.cutoff = 0
        
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

    def section_properties(self):
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
            I_xx, I_yy, I_xy , x_bar, y_bar, num_upper_stringers, num_lower_stringers, l2 = moispan.calculate_moments_of_inertia(self.planform.chord_spanwise(pos*2/self.planform.b), [0.4], self.tSkin, self.tSpar, self.tMidSpar, 0.005, 0.0006)
            mois.append(I_xx)
            xBars.append(x_bar)
            yBars.append(y_bar)
        return np.array(mois), np.array(xBars), np.array(yBars)

    def torstiff(self):
        
        pass

    def thicknesses(self, pos):
        if pos>=self.cutoff:
            return [(1000*self.tSkin, 1000*self.tSpar, 1000*self.tSkin, 1000*self.tSpar)]
        else:
            return [(1000*self.tSkin, 1000*self.tMidSpar, 1000*self.tSkin, 1000*self.tSpar), (1000*self.tSkin, 1000*self.tSpar, 1000*self.tSkin, 1000*self.tMidSpar)]
    
    def xBars(self):
        return moi.centroid()

    def yBars(self):
        pass

    def sparHeight(self,z):
        if self.midspar and self.cutoff>=z:
            sparLocs = [self.posMidSpar]
        
        upperCoords, lowerCoords = wingbox(self.planform.chord_spanwise(z), sparLocs, plot=False)
        h1 = upperCoords
        L1 = upperCoords[1][0] - lowerCoords[1][0]
        L2 = upperCoords[1][2] - lowerCoords[1][2]
        x = upperCoords[0][1] - upperCoords[0][0]
        pass
   
    def volume(self):
        if self.midSpar:
            sparLocs = [self.posMidSpar]
        else:
            sparLocs = []
        
        upperCoords, lowerCoords = wingbox(self.chord(self.b/4), sparLocs, plot=False)#uses cross-section at b/4
        h1 = upperCoords[1][0] - lowerCoords[1][0]
        h2 = upperCoords[1][1] - lowerCoords[1][1]

        skinTop= np.sqrt( (upperCoords[0][1] - upperCoords[0][0])**2 + (upperCoords[1][1] - upperCoords[1][0])**2 )#upper skin length
        skinBottom = np.sqrt( (lowerCoords[0][1] - lowerCoords[0][0])**2 + (lowerCoords[1][1] - lowerCoords[1][0])**2 )#upper skin length

        spar1vol = self.tSpar * h1 * self.b / 2 / np.cos(self.planform.sweep_at_c_fraction(self.frontSparPos))#front spar
        spar2vol = self.tSpar * h2 * self.b / 2 / np.cos(self.planform.sweep_at_c_fraction(self.rearSparPos))#aft spar
        spar3vol = 0
        if self.midSpar:
            h3 = upperCoords[1][2] - lowerCoords[1][2]
            spar3vol = self.tSpar * h3 * self.b / 2 / np.cos(self.planform.sweep_at_c_fraction(self.posMidSpar))#mid spar
        skinVol = (skinTop+skinBottom)*self.b/4*self.tSkin
        #stiffVol = (self.nStiffBot+self.nStiffTop)*self.stiffArea *self.b / 2 / np.cos(self.planform.sweep_at_c_fraction(self.rearSparPos))
        stiffVol=0
        volume = spar1vol+spar2vol+spar3vol+skinVol+stiffVol
        return volume