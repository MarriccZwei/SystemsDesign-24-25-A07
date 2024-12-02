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

def Veas(v, rho):
    return v*(rho/1.225)**0.5

class LoadChart():
    def __init__(self, altitude,mass, planform:Planform, nmin=1):
        cltakeoff = Constants.TAKEOFFCL
        clclean = fw.CLClean(planform, onlymax=True)
        S = planform.S
        self.altitude = altitude
        rho = ISA.density(altitude)
        mach = ISA.speedOfSound(altitude)
        self.weight = mass
        #self.nmax = min(max(2.1 + 24000/(self.weight*2.204623+10000),2.5),3.8)
        self.nmax = min(max(4.2,2.5),3.8)
        self.nmin = nmin
        
        g=9.81
        self.vs1 = round(Veas((2*mass*g/rho/S/clclean)**0.5,rho))
        
        self.vso = round(Veas((2*mass*g/rho/S/cltakeoff)**0.5,rho))
        
        self.va = round(Veas(self.vs1 * (self.nmax)**0.5, rho))
        self.vc = round(Veas(Constants.CRUISEVELOCITY,rho))
        self.vd = round(Veas(Constants.CRUISEVELOCITY + 0.05*mach, rho))
        self.vf = round(min(1.8*self.vs1, 1.8*self.vso))

    def positiveLoadCurve(self):
        curveLimit = int((self.nmax)**0.5 * self.vs1)
        if curveLimit >self.vd:
            curveLimit = self.vd
            lowSpeed = np.linspace(0,curveLimit,curveLimit)
            curve = lowSpeed*lowSpeed/self.vs1/self.vs1
            flat = np.zeros(1)
            highSpeed =np.ones(1)*self.vd
            endSpeed = np.ones(1)*self.vd
            endN = np.zeros(1)
        else: 
            lowSpeed = np.linspace(0,curveLimit,curveLimit)
            curve = lowSpeed*lowSpeed/self.vs1/self.vs1
            highSpeed = np.linspace(curveLimit+1,self.vd, self.vd -curveLimit +1)
            flat = np.ones(self.vd - curveLimit +1)*self.nmax
            endSpeed = np.ones(1)*self.vd
            endN = np.zeros(1)

        chart = np.concatenate((curve,flat,endN))
        speed = np.concatenate((lowSpeed,highSpeed,endSpeed))

        return chart, speed
    
    def flapsLoadCurve(self):
        curveLimit = int(min(int(2**0.5 * self.vso),self.vf))
        lowSpeed = np.linspace(0,curveLimit,curveLimit)
        curve = lowSpeed*lowSpeed/self.vso/self.vso
        if curveLimit <= self.vf:
            highSpeed = np.linspace(curveLimit+1,self.vf, self.vf -curveLimit +1)
            flat = np.ones(self.vf - curveLimit +1)*2
        else: 
            print("FAIL")
            highSpeed = lowSpeed[-1]
            flat = np.zeros(1)
        #print(self.vf*self.vf/self.vs1/self.vs1)
        if self.vf*self.vf/self.vs1/self.vs1 <2:
            print("DROP")
            flat[-1] = self.vf*self.vf/self.vs1/self.vs1
        chart = np.concatenate((curve,flat))
        speed = np.concatenate((lowSpeed,highSpeed))
        return chart, speed

    def negativeLoadCurve(self):
        curveLimit = round((self.nmin)**0.5 * self.vs1)
        lowSpeed = np.linspace(0,curveLimit,curveLimit)
        curve = lowSpeed*lowSpeed/self.vs1/self.vs1*(-1)
        if curveLimit >self.vc:
            curveLimit = self.vc-1
        highSpeed = np.linspace(curveLimit+1,self.vc, self.vc -curveLimit +1)
        flat = np.ones(self.vc - curveLimit +1)*self.nmin*(-1)
        
        reallyHighSpeed = np.linspace(self.vc+1, self.vd, self.vd - self.vc + 1)
        linear = np.linspace(-1*self.nmin, 0, self.vd - self.vc + 1)

        chart =    np.concatenate((curve,flat, linear))
        speed = np.concatenate((lowSpeed,highSpeed, reallyHighSpeed))

        return chart, speed

    def oneGeeLines(self):
        speed = np.linspace(0,self.vd, self.vd)
        line = np.ones(self.vd)
        negLine = line*(-1)

        return  line, speed, negLine

    def criticalLoadCases(self): #returns a list of critical load cases as: Speed (0), Weight (1), load factor (2), altitude (3)
        maxFlaps = [round(min(int(2**0.5 * self.vso),self.vf)), self.weight, 2 , self.altitude]
        maxVA = [round((self.nmax)**0.5 * self.vs1), self.weight, self.nmax, self.altitude]
        maxVD = [self.vd, self.weight, self.nmax, self.altitude]
        minVA = [round((self.nmin)**0.5 * self.vs1), self.weight, (-1)*self.nmin, self.altitude]
        minVC = [self.vc, self.weight, (-1)*self.nmin, self.altitude]

        cll = []
        cll.append(maxFlaps)
        cll.append(maxVA)
        cll.append(maxVD)
        cll.append(minVA)
        cll.append(minVC)

        return cll
    
    def printCLL(self):
        x = self.criticalLoadCases()
        for i in x:
            print("---------------------------")
            print("Critical Load Case:")
            print("Speed: "+str(i[0])+"m/s")
            print("Weight: "+str(i[1])+"kg")
            print("Load Factor: "+str(i[2]))
            print("Altitude: "+str(i[3])+"m")
            print()

    def plotVN(self, number = 0, plot = True):
        #colourList = ["black", "xkcd:red", "xkcd:orange", 'xkcd:yellow', "xkcd:neon green", "xkcd:green", "xkcd:sky blue", "xkcd:bright blue", "xkcd:indigo", "xkcd:purple", "xkcd:violet", "xkcd:light purple", "xkcd:pink"]
        colourList = ["black", "xkcd:red", "xkcd:pink", 'xkcd:green', "xkcd:spring green", "xkcd:blue", "xkcd:cerulean", "xkcd:purple", "xkcd:hot pink"]
        if number >= len(colourList):
            number = 0
        colourChoice = colourList[number]
        u = self.flapsLoadCurve()
        w = self.positiveLoadCurve()
        x = self.negativeLoadCurve()
        y = self.oneGeeLines()
        
        title = "Mass: "+str(self.weight) + "kg, altitude: "+ str(self.altitude) +"m"
        
        #plt.plot(y[1],y[0], "xkcd:slate")
        #plt.plot(y[1],y[2], "xkcd:slate")
        plt.plot(u[1],u[0], colourChoice, label=title)
        plt.plot(w[1],w[0], colourChoice)
        plt.plot(x[1],x[0], colourChoice)

        if plot:
            plt.show()

def runVNdiagram(plot = False, massList = [66300,115742,185548]):
    testPF = Planform(251,9.87,0.1,28.5, 2.15, radians = False)
    critList = []
    i =1

    for m in massList:
        
        altitude = 0
        testCase = LoadChart(altitude,m, testPF)
        critList = critList + (testCase.criticalLoadCases())
        if plot == True:
            testCase.plotVN(i, plot=False)
        #testCase.printCLL()
        del testCase
        i=i+1

        #plt.legend()
        #plt.show()

        altitude = Constants.CRUISEALTITUDE
        testCase = LoadChart(altitude,m, testPF)
        critList = critList + (testCase.criticalLoadCases())
        if plot == True:
            testCase.plotVN(i, plot=False)
        del testCase
        i=i+1

        #plt.legend()
        #plt.show()
        
    if plot == True:
        plt.legend()
        plt.show()
    
    spdList = ["V-minFlaps", 'Va', 'Vd', 'V-minNim', 'Vc']
    altList = ["sea level", "cruise altitude"]
    weightList = ["OEW", "OEW + max payload", "MTOW"]
    s = 0
    a = 0
    w = 0
    c=0
    print("<====== Begin critical load cases ======> ")
    
    for k in critList:
        s = c%5
        w=int(c/10)%3
        a=int(c/5)%2
        print(f"Case {c+1}: {k} \t {spdList[s]}, {weightList[w]}, {altList[a]}")
        c=c+1
    
    print("<====== End critical load cases ======> ")
    return critList

#runVNdiagram(plot = True)