from OOP.Planform import Planform 

class FlexibleWingBox():
    def __init__(self, planform:Planform, location, tUpperSkin, tLowerSkin, tFrontSpar,tRearSpar, tMidSpar):
        self.tUpperSkin = tUpperSkin
        self.tLowerSkin = tLowerSkin
        self.tFrontSpar = tFrontSpar
        self.tRearSpar = tRearSpar
        self.tMidSpar = tMidSpar

    def wingBoxThicknesses(self):
        dic = {
            'f' = self.tFrontSpar,
            'm' = self.tMidSpar,
            'r' = self.tRearSpar,
            't' = self.tUpperSkin,
            'b' = self.tLowerSkin,
            
        }