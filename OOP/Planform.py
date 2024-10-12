if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING

import unittest
import numpy as np

"The representation of anything that can be called a wing that is tail, rudder, pylon and wing"
class Planform():
    def __init__(self, S, AR, TR, sweepC4, dihedral, radians=True, symmetric = True):
        '''UNPACKING'''
        self.S = S #wing surface
        self.AR = AR #aspect ratio
        self.TR = TR #taper ratio

        #sweep @ c/4 and dihedral
        if radians:
            self.sweepC4 = sweepC4
            self.dihedral = dihedral
        else:
            self.sweepC4 = np.radians(sweepC4)
            self.dihedral = np.radians(dihedral)

        #determines whether the planform is one sided (rudder) or symmetric (tail)
        if symmetric:
            self.planforms = 2
        else:
            self.planforms = 1

        '''BASIC PLANFORM CALCS'''
        self.b = np.sqrt(AR*S) #span
        self.cr = 2*S/(1+TR)/self.b #root chord
        self.ct = TR*self.cr #tip chord
        self.cavg = S/self.b #average chord
        self.sweepLE = np.arctan(np.tan(self.sweepC4)+0.25*self.planforms*self.cr/self.b*(1-TR)) #sweep @ LE

        '''MAC PROPERTIES'''
        self.MAC, self.YMAC, self.XLEMAC = self._MAC(self.sweepLE, self.b, self.cr, self.ct)


    """Use this to get sweep angles other than LE and C/4"""
    #xc is the x/c fraction at which you want the sweep, set radians to False if you want a degree output
    def sweep_at_c_fraction(self, xc, radians=True):
        radianSweep = np.arctan(np.tan(self.sweepLE)-xc*self.planforms*self.cr/self.b*(1-self.TR))
        if radians:
            return radianSweep
        else:
            return np.degrees(radianSweep)


    def _MAC(self, LambdaLE, b, CRoot, CTip): #imported code
        TaperRatio = CTip/CRoot

        MAC = 2/3 * CRoot * ((1+TaperRatio + TaperRatio**2)/(1+TaperRatio))
        YMAC = (b/6) * ((1 + 2*TaperRatio) / (1 + TaperRatio))
        XLEMAC = YMAC * np.tan(LambdaLE)

        return [MAC, YMAC, XLEMAC]
    
#=======================================================================================================

'''TESTS'''   
if __name__ == "__main__":
    class Test_Planform(unittest.TestCase):
        testPlanform = Planform(478.4, 9.873, 0.1, 28.5, 2.15, False)

        def test_sweep_at_c_fraction(self): #testing sweep calculator with the WP2 iteration
            #sweep at LE
            self.assertGreater(32.1, self.testPlanform.sweep_at_c_fraction(0, False))
            self.assertLess(32, self.testPlanform.sweep_at_c_fraction(0, False))
            #sweep at TE
            self.assertGreater(16.5, self.testPlanform.sweep_at_c_fraction(1, False))
            self.assertLess(16.4, self.testPlanform.sweep_at_c_fraction(1, False))
            #sweep at C/2
            self.assertGreater(24.8, self.testPlanform.sweep_at_c_fraction(0.5, False))
            self.assertLess(24.7, self.testPlanform.sweep_at_c_fraction(0.5, False))
    

    unittest.main()
