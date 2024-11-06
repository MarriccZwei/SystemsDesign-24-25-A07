if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING

import unittest
import numpy as np

"A representation of the fuselage lengths"
class Fuselage():
    def __init__(self, D, L1, L2, L3):
        self.D = D #fuselage equivalent diameter
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3
    
    '''the total length of the fuselage, made this way so it updates together with other values'''
    @property
    def L(self):
        return self.L1+self.L2+self.L3
    
    def SwFus(self): #Wetted Surface Fuselage
        term1 = (1 / (3 * self.L1**2))
        term2 = ((4 * self.L1**2 + self.D**2 / 4)**1.5) - (self.D**3 / 8)
        term3 = -self.D
        term4 = 4 * self.L2
        term5 = 2 * np.sqrt(self.L3**2 + self.D**2 / 4)
        term6 = np.pi/4*self.D
        return term6*(term1*term2+term3+term4+term5)

if __name__ == "__main__":
    class TestFuselage(unittest.TestCase):
        def test_L(self):
            fus = Fuselage(1,2,3,4) #plen :) - 'tis just a test case to see if the property operator works
            self.assertEqual(9, fus.L)
            fus.L1+=1
            self.assertEqual(10, fus.L)

    unittest.main()