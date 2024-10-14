if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING

import unittest
import numpy as np

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
    def autosize(cls, planform:Planform, aileronCfC = 0.3, flapCfC = 0.35, krugerCfC=0.15, aileronDefl=25, aileronDiff = 0.75, flapMaxDdefl=40):
        '''working out the y/(b/2) fractions'''
        #<!TOD!>
        aileronStartyPerbHalf = 0
        aileronEndyPerbHalf = 0
        flapStartyPerbHalf = 0
        flapEndyPerbHalf = 0
        krugerStartyPerbHalf = 0
        krugerEndyPerbHalf = 0

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

        def test_autosize(self):
            testPlanform = Planform.Planform(478.4, 9.873, 0.1, 28.5, 2.15, False)
            testHLDsOrg = HLDs(26/(68.7/2), 34/(68.7/2), 2.95/(68.7/2), 25.7/(68.7/2), 5/(68.7/2), 34/(68.7/2))
            testHLDs = HLDs.autosize(testPlanform)
            print(f"Ailerons range: [{testHLDs.aileronStartyPerbHalf}, {testHLDs.aileronEndyPerbHalf}]")
            print(f"Ailerons range: [{testHLDsOrg.aileronStartyPerbHalf}, {testHLDsOrg.aileronEndyPerbHalf}]")
    
    unittest.main()
