import json
import os
import ISA
import numpy as np
import CruiseConditions as cc
with open(os.getcwd()+"/Protocols/main.json") as jsonMain:
    dataDict = json.loads(jsonMain.readline())
    sweepLE = dataDict["sweepLE"]
    Cd_0 = dataDict["Cd0"]
    AR = dataDict["AR"]
    oswald = dataDict["Oswald"]
    M_CR = dataDict["Mcruise"]
    H_CR = dataDict["Hcruise"]
    WS = dataDict["W/S"]
    sweepQuarterC = dataDict["sweep"]
    MTOM = dataDict["MTOM"]
    TSFC = dataDict["TSFC"]

V_cruise = M_CR*(ISA.temperature(np.round(H_CR))*287*1.4)**0.5

'''Drag estimate'''
#0.73 to be changed later to design cl!!!
Cdmisc = 0.002/(1+2.5*(cc.M_dd(0.73, sweepLE, tc=0.1)-M_CR)/0.05)
C_D = Cd_0 + 0.73*0.73/np.pi/AR/oswald + Cdmisc
D = C_D/0.73*1.1*MTOM

SAR = V_cruise/D/TSFC

print(f"Vcruise: {V_cruise}")
print(f"Cdmisc: {Cdmisc}")
print(f"C_D: {C_D}")

print(f"\nSAR: {SAR}")


