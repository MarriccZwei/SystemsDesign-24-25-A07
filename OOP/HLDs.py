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

from OOP import Planform

"The representation of HLD/Ailerons subsubsystems stored in a normalized y(b/2) form. Contains methods that allow, for an input Planform, to check whether it meets the manouvering requirements"
class HLDs():
    def __init__(self, aileronStartyPerbHalf, aileronEndyPerbHalf, flapStartyPerbHalf, flapEndyPerbHalf, krugerStartyPerbHalf, krugerEndyPerbHalf, 
                 aileronCfC = 0.3, flapCfC = 0.35, krugerCfC=0.15, aileronDefl=25, aileronDiff = 0.75, flapMaxDdefl=40):
        self.aileronDefl = aileronDefl #aileron Deflection [deg]
        self.aileronDiff = aileronDiff #aileron Deflection - Differential defl. down as a pfraction of defl. up
        self.flapMaxDdefl = flapMaxDdefl #flap Deflection [deg]
        
        """spar locations"""
        self.frontSparLoc = krugerCfC+0.05
        self.backSparLoc = 1-0.05-flapCfC

        '''flapped chord ratios'''
        self.aileronCfC = aileronCfC
        self.flapCfC = flapCfC
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
    
    '''The area of movable surfaces themselves'''
    def Smovable(self, planform:Planform.Planform):
        """!!!SYMMETRICAL PLANFORMS ONLY!!!"""
        S_movable = 0

        #contribution of Kruger Flaps
        cStartKruger = planform.chord_spanwise(self.krugerStartyPerbHalf) #the base of the trapezoid - chord at kruger start
        cEndKruger = planform.chord_spanwise(self.krugerEndyPerbHalf) #the base of the trapezoid - chord at kruger start
        HKruger = self.krugerEnd(planform.b)-self.krugerStart(planform.b) #trapezoid Height - the difference is sapnwise locations
        S_movable += HKruger*(cEndKruger+cStartKruger)*self.krugerCfC #two times the trapezoid area for 2 sides of the wing, that's why the 0.5 is missing - mulled by cfc to get just the movable area

        #contribution of TE Flaps
        cStartFlap = planform.chord_spanwise(self.flapStartyPerbHalf) #the base of the trapezoid - chord at kruger start
        cEndFlap = planform.chord_spanwise(self.flapEndyPerbHalf) #the base of the trapezoid - chord at kruger start
        HFlap = self.krugerEnd(planform.b)-self.flapStart(planform.b) #trapezoid Height - the difference is sapnwise locations
        S_movable += HFlap*(cEndFlap+cStartFlap)*self.flapCfC #two times the trapezoid area for 2 sides of the wing, that's why the 0.5 is missing - mulled by cfc to get just the movable area

        #contribution of ailerons
        cStartAileron = planform.chord_spanwise(self.aileronStartyPerbHalf) #the base of the trapezoid - chord at kruger start
        cEndAileron = planform.chord_spanwise(self.aileronEndyPerbHalf) #the base of the trapezoid - chord at kruger start
        HAileron = self.krugerEnd(planform.b)-self.aileronStart(planform.b) #trapezoid Height - the difference is sapnwise locations
        S_movable += HAileron*(cEndAileron+cStartAileron)*self.aileronCfC #two times the trapezoid area for 2 sides of the wing, that's why the 0.5 is missing - mulled by cfc to get just the movable area

        return S_movable

    #aileron Surface
    def Saileron(self, planform:Planform.Planform):
        cStartAileron = planform.chord_spanwise(self.aileronStartyPerbHalf) #the base of the trapezoid - chord at kruger start
        cEndAileron = planform.chord_spanwise(self.aileronEndyPerbHalf) #the base of the trapezoid - chord at kruger start
        HAileron = self.krugerEnd(planform.b)-self.aileronStart(planform.b) #trapezoid Height - the difference is sapnwise locations
        return HAileron*(cEndAileron+cStartAileron)*self.aileronCfC #two times the trapezoid area for 2 sides of the wing, that's why the 0.5 is missing - mulled by cfc to get just the movable area


    '''Sizing Movable Surfaces for an existing planform, given deflections and design constraints'''
    @classmethod
    def autosize(cls, planform:Planform.Planform, radiusFuselage, aileronCfC = 0.3, flapCfC = 0.35, krugerCfC=0.15, aileronDefl=25, aileronDiff = 0.75, flapMaxDdefl=40):
        '''working out the y/(b/2) fractions'''
        aileronFlapMargin = 0.3 #metres between
        ailerongWingTipMargin = 0.1 #fraction 0.5 metres source ALBERT
        krugerWingTipMargin = 0.1 #fraction

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

        integral2 = integrate.quad(lambda y: y**2*planform.chord_spanwise(y/halfSpan), 0, halfSpan)[0]
        pCL = -(4*(c.DCLALPHA+c.CD0))/(planform.S*planform.b**2)*integral2
        
        aileronEndyPerbHalf = 1-ailerongWingTipMargin

        dAlphaDeltaCLC = (2*c.DCLALPHA*tau)/(planform.S*planform.b)

        requiredIntegral1 = -(20*pCL)/(dAlphaDeltaCLC*deltaAlpha*((2*c.VAPPROACH)/planform.b))
        
        integral1 = 0
        b1 = aileronEndyPerbHalf*halfSpan
        b2 = aileronEndyPerbHalf*halfSpan
        while integral1 < requiredIntegral1:
            b1 = b1-0.1
            integral1 = integrate.quad(lambda y: y*planform.chord_spanwise(y/halfSpan), b1, b2)[0]

        aileronStartyPerbHalf = b1/halfSpan

        krugerEndyPerbHalf = 1-krugerWingTipMargin
        flapEndyPerbHalf = (b1-aileronFlapMargin)/halfSpan
        flapStartyPerbHalf = radiusFuselage/halfSpan

        deltaCCf = 0.6
        cPrimeC = 1 + deltaCCf*flapCfC
        deltaClFlaps = 1.3*cPrimeC

        areaFlaps = (fun.partialSurface(flapEndyPerbHalf*halfSpan, planform)-fun.partialSurface(radiusFuselage, planform))*2
        deltaCLFlaps = 0.9*deltaClFlaps*areaFlaps/planform.S*np.cos(planform.sweep_at_c_fraction(backSparLoc))

        deltaClKruger = 0.3
        cleanCLMax = maxCL(c.CLMAXAIRFOIL, planform, c.LANDMACH)
        print(cleanCLMax)
        deltaCLKruger = c.ULTIMATECL-cleanCLMax-deltaCLFlaps

        areaKruger = (deltaCLKruger*planform.S)/(0.9*deltaClKruger*np.cos(planform.sweep_at_c_fraction(frontSparLoc)))
        areaBegin = fun.partialSurface(krugerEndyPerbHalf*halfSpan, planform)-0.5*areaKruger
        krugerBegin = 0
        area = 0
        while area < areaBegin:
            krugerBegin = krugerBegin+0.1
            area = fun.partialSurface(krugerBegin, planform)

        flapStartyPerbHalf = radiusFuselage/halfSpan
        krugerStartyPerbHalf = krugerBegin/halfSpan
        
        '''Returning the sized Movable Surfaces'''
        return cls(aileronStartyPerbHalf, aileronEndyPerbHalf, flapStartyPerbHalf, flapEndyPerbHalf, krugerStartyPerbHalf, krugerEndyPerbHalf, 
                   aileronCfC, flapCfC, krugerCfC, aileronDefl, aileronDiff, flapMaxDdefl)
    
    def alphaMax(self, planform:Planform.Planform, cLalpha, CLreqToff, cLreqLand):
        """the maximum angle of attack for the scrape angle - CLalpha must be in per degree!!!"""
        #landing
        alpha0L = c.DELTAALPHA0LLANDING*(self.flapSflapped(planform))/planform.S+c.ALPHAZEROLIFT
        deltaCflapPerC = 0.6*self.flapCfC
        cPrime1 = planform.chord_spanwise(self.flapStartyPerbHalf)*deltaCflapPerC
        cPrime2 = planform.chord_spanwise(self.flapEndyPerbHalf)*deltaCflapPerC
        halfSpanflapped = (self.flapEndyPerbHalf-self.flapStartyPerbHalf)*planform.b/2
        deltaS = (cPrime1+cPrime2)*halfSpanflapped # no divided by 2 cuz symmetric planform
        cLalphaPrime = (1+deltaS/planform.S)*cLalpha #cl alph change due to wing area increase
        landingAlphaMax = alpha0L+cLreqLand/cLalphaPrime

        #takeoff
        alpha0L = c.DELTAALPHA0LTAKEOFF*(self.flapSflapped(planform))/planform.S+c.ALPHAZEROLIFT
        deltaCflapPerC = 0.6*self.flapCfC
        cPrime1 = planform.chord_spanwise(self.flapStartyPerbHalf)*deltaCflapPerC
        cPrime2 = planform.chord_spanwise(self.flapEndyPerbHalf)*deltaCflapPerC
        halfSpanflapped = (self.flapEndyPerbHalf-self.flapStartyPerbHalf)*planform.b/2
        deltaS = (cPrime1+cPrime2)*halfSpanflapped # no divided by 2 cuz symmetric planform
        cLalphaPrime = (1+deltaS/planform.S)*cLalpha #cl alph change due to wing area increase
        takeoffAlphaMax = alpha0L+CLreqToff/cLalphaPrime

        return max(takeoffAlphaMax, landingAlphaMax)
        

if __name__ == "__main__":
    class Test_Planform(unittest.TestCase):
        def test_flappedSurface(self): #based on WP2 design
            testPlanform = Planform.Planform(478.4, 9.873, 0.1, 28.5, 2.15, False)
            testHLDs = HLDs(26/(68.7/2), 34/(68.7/2), 2.95/(68.7/2), 25.7/(68.7/2), 5/(68.7/2), 34/(68.7/2))
            self.assertLess(359, testHLDs.flapSflapped(testPlanform))
            self.assertGreater(360, testHLDs.flapSflapped(testPlanform))

        def test_autosize(self):
            testPlanform = Planform.Planform(478.4, 9.873, 0.1, 28.5, 2.15, False)
            testHLDsOld = HLDs(26/(68.7/2), 34/(68.7/2), 2.95/(68.7/2), 25.7/(68.7/2), 5/(68.7/2), 34/(68.7/2))
            testHLDsNew = HLDs.autosize(testPlanform, 2.95)
            print(f"Old Aileron Spanwise loc: [{testHLDsOld.aileronStart(testPlanform.b)}, {testHLDsOld.aileronEnd(testPlanform.b)}]")
            print(f"Old Flap Spanwise loc: [{testHLDsOld.flapStart(testPlanform.b)}, {testHLDsOld.flapEnd(testPlanform.b)}]")
            print(f"Old Kruger Spanwise loc: [{testHLDsOld.krugerStart(testPlanform.b)}, {testHLDsOld.krugerEnd(testPlanform.b)}]")
            print()
            print(f"New Aileron Spanwise loc: [{testHLDsNew.aileronStart(testPlanform.b)}, {testHLDsNew.aileronEnd(testPlanform.b)}]")
            print(f"New Flap Spanwise loc: [{testHLDsNew.flapStart(testPlanform.b)}, {testHLDsNew.flapEnd(testPlanform.b)}]")
            print(f"New Kruger Spanwise loc: [{testHLDsNew.krugerStart(testPlanform.b)}, {testHLDsNew.krugerEnd(testPlanform.b)}]")

        def test_alphaStall(self):
            testPlanform = Planform.Planform(478.4, 9.873, 0.1, 28.5, 2.15, False)
            testHLDsNew = HLDs.autosize(testPlanform, 2.95)
            print(f"alpha for ClMax: {testHLDsNew.alphaMax(testPlanform, 0.1, 1.8, 2.5)}")

    unittest.main()