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
    S = dataDict["S"]
    TSFC = dataDict["TSFC"]
    CLdes = dataDict["CLDesign"]
    MTOM = dataDict["MTOM"]

V_cruise = M_CR*(ISA.temperature(np.round(H_CR))*287*1.4)**0.5

'''Drag estimate'''
#0.73 to be changed later to design cl!!!
Cdmisc = 0.002/(1+2.5*(cc.M_dd(CLdes, sweepLE, tc=0.1)-M_CR)/0.05)
betterOswald = 1/(0.0075*AR*np.pi+1/.97)
C_D = Cd_0 + CLdes*CLdes/np.pi/AR/betterOswald + Cdmisc
#D = C_D*ISA.density(np.round(H_CR))*0.5*V_cruise*V_cruise*S
D = 0.825*C_D/CLdes *MTOM*9.81*1.1

SAR = V_cruise/D/TSFC

print(f"Vcruise: {V_cruise}")
print(f"Cdmisc: {Cdmisc}")
print(f"C_D: {C_D}")
print(f"D: {D}")
print(f"oswald: {betterOswald}")
print(f"sweep oswald term: {(np.cos(sweepLE)**0.15)}")

print(f"\nSAR: {SAR}")


