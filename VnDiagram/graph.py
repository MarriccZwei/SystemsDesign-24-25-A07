import numpy as np
from matplotlib import pyplot as plt
class LoadChart():
    def __init__(self, altitude,mass):
        self.altitude = altitude
        self.weight = mass
        self.nmax = 2.1 + 24000/(self.weight*2.204623+10000)
        self.nmin = 1.5
        self.vso = 60
        self.vs1 = 85
        self.va = int(self.vs1 * (self.nmax)**0.5)
        self.vc = 230
        self.vd = 245
        self.vf = 75

    def positiveLoadCurve(self):
        curveLimit = int((self.nmax)**0.5 * self.vso)
        lowSpeed = np.linspace(0,curveLimit,curveLimit)
        curve = lowSpeed*lowSpeed/self.vso/self.vso
        highSpeed = np.linspace(curveLimit+1,self.vd, self.vd -curveLimit +1)
        flat = np.ones(self.vd - curveLimit +1)*self.nmax
        flat[-1]=0

        chart = np.concatenate((curve,flat))
        speed = np.concatenate((lowSpeed,highSpeed))

        return chart, speed
    
    def flapsLoadCurve(self):
        pass

    def negativeLoadCurve(self):
        curveLimit = int((self.nmin)**0.5 * self.vso)
        lowSpeed = np.linspace(0,curveLimit,curveLimit)
        curve = lowSpeed*lowSpeed/self.vso/self.vso*(-1)

        highSpeed = np.linspace(curveLimit+1,self.vc, self.vc -curveLimit +1)
        flat = np.ones(self.vc - curveLimit +1)*self.nmin*(-1)
        
        reallyHighSpeed = np.linspace(self.vc+1, self.vd, self.vd - self.vc + 1)
        linear = np.linspace(-1*self.nmin, 0, self.vd - self.vc + 1)

        chart = np.concatenate((curve,flat, linear))
        speed = np.concatenate((lowSpeed,highSpeed, reallyHighSpeed))

        return chart, speed

testCase = LoadChart(11000,180000)
x = testCase.positiveLoadCurve()
y= testCase.negativeLoadCurve()
plt.plot(x[1],x[0])
plt.plot(y[1],y[0])
plt.show()