if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    import unittest
    # ONLY FOR TESTING

import numpy as np
from matplotlib import pyplot as plt
from General import ISA
from General import Constants
from ClassIV import flappedWing as fw
from OOP.Planform import Planform

class LoadChart():
    def __init__(self, altitude,mass, planform:Planform, nmin=1):
        cltakeoff = Constants.TAKEOFFCL
        clclean = fw.CLClean(planform, onlymax=True)
        S = planform.S
        self.altitude = altitude
        rho = ISA.density(altitude)
        mach = ISA.speedOfSound(altitude)
        self.weight = mass
        self.nmax = 2.1 + 24000/(self.weight*2.204623+10000)
        self.nmin = nmin
        
        g=9.81
        vso = (2*mass*g/rho/S/clclean)**0.5
        self.vso = round(vso)
        
        vs1 = (2*mass*g/rho/S/cltakeoff)**0.5
        self.vs1 = round(vs1)
        
        self.va = round(self.vs1 * (self.nmax)**0.5)
        
        vc=Constants.CRUISEVELOCITY
        self.vc = round(vc)
        self.vd = round(vc + 0.05*mach)
        self.vf = round(min(1.8*self.vs1, 1.8*self.vso))

    def positiveLoadCurve(self):
        curveLimit = int((self.nmax)**0.5 * self.vs1)
        lowSpeed = np.linspace(0,curveLimit,curveLimit)
        curve = lowSpeed*lowSpeed/self.vs1/self.vs1
        highSpeed = np.linspace(curveLimit+1,self.vd, self.vd -curveLimit +1)
        flat = np.ones(self.vd - curveLimit +1)*self.nmax
        flat[-1]=0

        chart = np.concatenate((curve,flat))
        speed = np.concatenate((lowSpeed,highSpeed))

        return chart, speed
    
    def flapsLoadCurve(self):
        curveLimit = round(min(int(2**0.5 * self.vso),self.vf))
        lowSpeed = np.linspace(0,curveLimit,curveLimit)
        curve = lowSpeed*lowSpeed/self.vso/self.vso
        if curveLimit <= self.vf:
            highSpeed = np.linspace(curveLimit+1,self.vf, self.vf -curveLimit +1)
            flat = np.ones(self.vf - curveLimit +1)*2
        else: 
            print("FAIL")
            highSpeed = lowSpeed[-1]
            flat = np.zeros(1)
        print(self.vf*self.vf/self.vs1/self.vs1)
        if self.vf*self.vf/self.vs1/self.vs1 <2:
            print("DROP")
            flat[-1] = self.vf*self.vf/self.vs1/self.vs1
        chart = np.concatenate((curve,flat))
        speed = np.concatenate((lowSpeed,highSpeed))
        return chart, speed

    def negativeLoadCurve(self):
        curveLimit = int((self.nmin)**0.5 * self.vs1)
        lowSpeed = np.linspace(0,curveLimit,curveLimit)
        curve = lowSpeed*lowSpeed/self.vs1/self.vs1*(-1)

        highSpeed = np.linspace(curveLimit+1,self.vc, self.vc -curveLimit +1)
        flat = np.ones(self.vc - curveLimit +1)*self.nmin*(-1)
        
        reallyHighSpeed = np.linspace(self.vc+1, self.vd, self.vd - self.vc + 1)
        linear = np.linspace(-1*self.nmin, 0, self.vd - self.vc + 1)

        chart = np.concatenate((curve,flat, linear))
        speed = np.concatenate((lowSpeed,highSpeed, reallyHighSpeed))

        return chart, speed

    def oneGeeLines(self):
        speed = np.linspace(0,self.vd, self.vd)
        line = np.ones(self.vd)
        negLine = line*(-1)

        return  line, speed, negLine

    def plotVN(self, number = 0, plot = True):
        colourList = ["black", "xkcd:red", "xkcd:orange", 'xkcd:yellow', "xkcd:neon green", "xkcd:green", "xkcd:sky blue", "xkcd:bright blue", "xkcd:indigo", "xkcd:purple", "xkcd:violet", "xkcd:light purple", "xkcd:pink"]
        if number > len(colourList):
            number = 0
        colourChoice = colourList[number]
        u = self.flapsLoadCurve()
        w = self.positiveLoadCurve()
        x = self.negativeLoadCurve()
        y = self.oneGeeLines()
        
        plt.plot(y[1],y[0], "xkcd:slate")
        plt.plot(u[1],u[0], colourChoice)
        plt.plot(w[1],w[0], colourChoice)
        plt.plot(x[1],x[0], colourChoice)

        if plot:
            plt.show()

testPF = Planform(400, 10, 0.3, 0.3, 0)

for i in range(11):
    altitude = i*1000
    testCase = LoadChart(altitude,180000, testPF)
    testCase.plotVN(i, plot=False)
    del testCase
plt.show()