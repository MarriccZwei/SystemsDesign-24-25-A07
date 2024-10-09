import numpy as np

"The representation of anything that can be called a wing that is tail, rudder, pylon and wing"
class Planform():
    def __init__(self, S, AR, TR, sweepC4, dihedral, radians=True, symmetric = True):
        '''UNPACKING'''
        self.S = S #wing surface
        self.AR = AR #aspect ratio
        self.TR = TR #taper ratio

        #sweep @ c/4
        if radians:
            self.sweepC4 = sweepC4
        else:
            self.sweepC4 = np.radians(sweepC4)
        self.dihedral = dihedral

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
        self.sweepLE = np.arctan(np.tan(sweepC4)+0.25*self.cr/self.b*(1-TR)) #sweep @ LE

        '''MAC PROPERTIES'''
        self.MAC, self.YMAC, self.XLEMAC = self._MAC(self.sweepLE, self.b, self.cr, self.ct)

    """Use this to get sweep angles other than LE and C/4"""
    #xc is the x/c fraction at which you want the sweep, set radians to False if you want a degree output
    def sweepAtCfraction(self, xc, radians=True):
        radianSweep = np.arctan(np.tan(self.sweepC4)-xc*self.planforms*self.cr/self.b*(1-self.TR))
        if radians:
            return radianSweep
        else:
            np.degrees(radianSweep)
    
    def _MAC(self, LambdaLE, b, CRoot, CTip): #imported code
        TaperRatio = CTip/CRoot

        MAC = 2/3 * CRoot * ((1+TaperRatio + TaperRatio**2)/(1+TaperRatio))
        YMAC = (b/6) * ((1 + 2*TaperRatio) / (1 + TaperRatio))
        XLEMAC = YMAC * np.tan(LambdaLE)

        return [MAC, YMAC, XLEMAC]