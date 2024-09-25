import json
import os
import ISA
import numpy as np
with open(os.getcwd()+"/Protocols/main.json") as jsonMain:
    dataDict = json.loads(jsonMain.readline())
    S = dataDict["S"]
    Cf = dataDict["Cf"]
    Cr = dataDict["Cr"]
    sweepHalfC = dataDict["sweepC/2"]
    M_CR = dataDict["Mcruise"]
    H_CR = dataDict["Hcruise"]
    WS = dataDict["W/S"]
    sweepQuarterC = dataDict["sweep"]

def cd0_constraint(Cf, Sw, cr, wFus):
    cd0max = Cf*(2-cr*wFus/Sw)
    #print(cd0max)
    return (cd0max-0.0035)/0.0018

def shock_wave_constraint(M_CR, sweepHalfC, WS):
    gamma = 1.4
    p_CR = ISA.pressure(int(round(H_CR)))
    CL_CR = 2*WS/gamma/p_CR/M_CR/M_CR
    print(CL_CR)
    return (np.cos(sweepHalfC)**3*(0.935-(M_CR+0.03)*np.cos(sweepHalfC))-0.115*CL_CR**1.5)/np.cos(sweepHalfC)**2

def clmax_constraint(CL_CRUISE, sweepQuarterC):
    return 1.1*CL_CRUISE/np.sqrt(sweepQuarterC)

print(cd0_constraint(Cf, S, Cr, 7))
print(shock_wave_constraint(M_CR, sweepHalfC, WS))
print(clmax_constraint(1, sweepQuarterC))
