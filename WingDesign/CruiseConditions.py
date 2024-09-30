import os
import json
import numpy as np

with open(os.getcwd()+"/Protocols/main.json") as mainJson:
    jsonDict = json.loads(''.join(mainJson.readlines()))
    AR = jsonDict["AR"]
    sweepHalfC = jsonDict["sweepC/2"]
    Mcruise = jsonDict["Mcruise"]

def datcom_cLalpha(AR, mach, sweepHalfC):
    beta =(1- mach*mach)**0.5
    sqrtPart = (4+(1+(np.tan(sweepHalfC)/beta)**2)*(AR*beta/0.95)**2)**0.5

    clAlpha = 2*np.pi*AR/(2+sqrtPart)
    return clAlpha

def M_dd(CLcruise, sweepLE, ka = 0.935, tc = 0.1):
    term1 = ka/np.cos(sweepLE)
    term2 = tc/np.cos(sweepLE)**2
    term3 = CLcruise/10/(np.cos(sweepLE)**3)
    return term1 - term2 - term3

if __name__ == "__main__":
    print(AR)
    print(Mcruise)
    print(sweepHalfC)
    print()
    print(np.pi*datcom_cLalpha(AR, Mcruise, sweepHalfC)/180)

