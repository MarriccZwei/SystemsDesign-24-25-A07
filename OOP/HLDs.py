if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING

import unittest
import numpy as np
import scipy.integrate as integrate
from General import Constants as c
from General import generalFunctions as fun
from ClassIV.clFunctions import maxCL

import Planform

"The representation of HLD/Ailerons subsubsystems stored in a normalized y(b/2) form. Contains methods that allow, for an input Planform, to check whether it meets the manouvering requirements"
class HLDs():
    def __init__(self, aileronStartyPerbHalf, aileronEndyPerbHalf, flapStartyPerbHalf, flapEndyPerbHalf, krugerStartyPerbHalf, krugerEndyPerbHalf, 
                 aileronCfC = 0.3, flapCfC = 0.35, krugerCfC=0.15, aileronDefl=25, aileronDiff = 0.75, flapMaxDdefl=40):
        self.aileronDefl = aileronDefl #aileron Deflection [deg]
        self.aileronDiff = aileronDiff #aileron Deflection - Differential defl. down as a pfraction of defl. up
        self.flapMaxDdefl = flapMaxDdefl #flap Deflection [deg]
        
        '''flapped chord ratios'''
        self.aileronCfC = aileronCfC
        self.flapcfC = flapCfC
        self.krugerCfC = krugerCfC

        '''Positions of Movable Devices expressed in y/(b/2) notation'''
        self.aileronStartyPerbHalf =aileronStartyPerbHalf
        self.aileronEndyPerbHalf = aileronEndyPerbHalf
        self.flapStartyPerbHalf = flapStartyPerbHalf
        self.flapEndyPerbHalf = flapEndyPerbHalf
        self.krugerStartyPerbHalf = krugerStartyPerbHalf
        self.krugerEndyPerbHalf = krugerEndyPerbHalf

        '''Positions of Movable Devices from root for a given span in [m]'''
        self.aileronStart = lambda span:self.aileronStartyPerbHalf*span/2
        self.aileronEnd = lambda span:self.aileronEndyPerbHalf*span/2
        self.flapStart = lambda span:self.flapStartyPerbHalf*span/2
        self.flapEnd = lambda span:self.flapEndyPerbHalf*span/2
        self.krugerStart = lambda span:self.krugerStartyPerbHalf*span/2
        self.krugerEnd = lambda span:self.krugerEndyPerbHalf*span/2


    '''Wing Surface Flapped by ailerons'''
    def aileronSflapped(self, planform:Planform.Planform):
        """!!!SYMMETRICAL PLANFORMS ONLY!!!"""
        cStart = planform.chord_spanwise(self.aileronStartyPerbHalf) #the base of the trapezoid - chord at aileron start
        cEnd = planform.chord_spanwise(self.aileronEndyPerbHalf) #the base of the trapezoid - chord at aileron start
        H = self.aileronEnd(planform.b)-self.aileronStart(planform.b) #trapezoid Height - the difference is sapnwise locations
        return H*(cEnd+cStart) #two times the trapezoid area for 2 sides of the wing, that's why the 0.5 is missing


    '''Wing Surface Flapped by flaps'''
    def flapSflapped(self, planform:Planform.Planform):
        """!!!SYMMETRICAL PLANFORMS ONLY!!!"""
        cStart = planform.chord_spanwise(self.flapStartyPerbHalf) #the base of the trapezoid - chord at flap start
        cEnd = planform.chord_spanwise(self.flapEndyPerbHalf) #the base of the trapezoid - chord at flap start
        H = self.flapEnd(planform.b)-self.flapStart(planform.b) #trapezoid Height - the difference is sapnwise locations
        return H*(cEnd+cStart) #two times the trapezoid area for 2 sides of the wing, that's why the 0.5 is missing


    '''Wing Surface Flapped by kruger flaps'''
    def krugerSflapped(self, planform:Planform.Planform):
        """!!!SYMMETRICAL PLANFORMS ONLY!!!"""
        cStart = planform.chord_spanwise(self.krugerStartyPerbHalf) #the base of the trapezoid - chord at kruger start
        cEnd = planform.chord_spanwise(self.krugerEndyPerbHalf) #the base of the trapezoid - chord at kruger start
        H = self.krugerEnd(planform.b)-self.krugerStart(planform.b) #trapezoid Height - the difference is sapnwise locations
        return H*(cEnd+cStart) #two times the trapezoid area for 2 sides of the wing, that's why the 0.5 is missing

    
    '''Sizing Movable Surfaces for an existing planform, given deflections and design constraints'''
    @classmethod
    def autosize(cls, planform:Planform.Planform, radiusFuselage, aileronCfC = 0.3, flapCfC = 0.35, krugerCfC=0.15, aileronDefl=25, aileronDiff = 0.75, flapMaxDdefl=40):
        '''working out the y/(b/2) fractions'''
        aileronFlapMargin = 0.3 #metres between
        wingtipMargin = 0.1 #fraction

        frontSparLoc = krugerCfC+0.05
        backSparLoc = 1-0.05-flapCfC

        #<!TOD!>
        deltaAlpha = 0.5 * (1 + aileronDiff)*aileronDefl
        
        x = aileronCfC
        if x<0.05:
            tau = x*4
        elif x<0.4:
            tau = (x*4/3) + (2 * 0.2 / 3)
        elif x<0.4:
            tau = x - 0.2
        elif x<0.7:
            tau = (2 * x / 3) + (10 / 3)
        
        halfSpan = planform.b/2

        integral2 = integrate.quad(lambda y: y**2*planform.chord_spanwise(y/halfSpan), 0, halfSpan)
        pCL = -(4*(c.DCLALPHA+c.CD0))/(planform.S*planform.b**2)*integral2
        
        aileronStartyPerbHalf = 1-wingtipMargin

        dAlphaDeltaCLC = (2*c.DCLALPHA*tau)/(planform.S*planform.b)

        requiredIntegral1 = -(20*pCL)/(dAlphaDeltaCLC*deltaAlpha*((2*c.VMANUEVER)/planform.b))
        
        integral1 = 0
        b1 = aileronStartyPerbHalf*halfSpan
        b2 = aileronStartyPerbHalf*halfSpan
        while integral1 < requiredIntegral1:
            b1 = b1-0.1
            integral1 = integrate.quad(lambda y: y*planform.chord_spanwise(y/halfSpan), b1, b2)

        aileronEndyPerbHalf = b1/halfSpan

        krugerEndyPerbHalf = 1-wingtipMargin
        flapEndyPerbHalf = (b1-aileronFlapMargin)/halfSpan
        deltaClKruger = 0.3
        areaKruger = (fun.partialSurface(krugerEndyPerbHalf*halfSpan)-fun.partialSurface(radiusFuselage))*2
        deltaCLKruger = 0.9*deltaClKruger*areaKruger/planform.S*np.cos(planform.sweep_at_c_fraction(frontSparLoc))
        cleanCLMax = maxCL(c.CLMAXAIRFOIL, planform, c.LANDMACH)
        deltaCLFlaps = c.ULTIMATECL-cleanCLMax-deltaCLKruger
        
        deltaCCf = 0.6
        cPrimeC = 1 + deltaCCf*flapCfC
        deltaClFlaps = 1.3*cPrimeC

        areaFlaps = (deltaCLFlaps*planform.S)/(0.9*deltaClFlaps*np.cos(planform.sweep_at_c_fraction(backSparLoc)))
        areaBegin = fun.partialSurface(flapEndyPerbHalf*halfSpan, planform)-0.5*areaFlaps
        flapsBegin = flapEndyPerbHalf*halfSpan
        area = 0
        while area < areaBegin:
            flapsBegin = flapsBegin-0.1
            area = fun.partialSurface(flapsBegin, planform)

        krugerStartyPerbHalf = radiusFuselage/halfSpan
        flapStartyPerbHalf = flapsBegin/halfSpan
        
        '''Returning the sized Movable Surfaces'''
        return cls(aileronStartyPerbHalf, aileronEndyPerbHalf, flapStartyPerbHalf, flapEndyPerbHalf, krugerStartyPerbHalf, krugerEndyPerbHalf, 
                   aileronCfC, flapCfC, krugerCfC, aileronDefl, aileronDiff, flapMaxDdefl)
    

if __name__ == "__main__":
    class Test_Planform(unittest.TestCase):
        def test_flappedSurface(self): #based on WP2 design
            testPlanform = Planform.Planform(478.4, 9.873, 0.1, 28.5, 2.15, False)
            testHLDs = HLDs(26/(68.7/2), 34/(68.7/2), 2.95/(68.7/2), 25.7/(68.7/2), 5/(68.7/2), 34/(68.7/2))
            self.assertLess(359, testHLDs.flapSflapped(testPlanform))
            self.assertGreater(360, testHLDs.flapSflapped(testPlanform))

    unittest.main()