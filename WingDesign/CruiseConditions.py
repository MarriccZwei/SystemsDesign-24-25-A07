import os
import json
import numpy as np
import pandas as pd
import math

zeroLiftAlpha = -2

with open(os.getcwd()+"/Protocols/main.json") as mainJson:
    jsonDict = json.loads(''.join(mainJson.readlines()))
    AR = jsonDict["AR"]
    sweepHalfC = jsonDict["sweepC/2"]
    sweepLE = jsonDict["sweepLE"]
    Mcruise = jsonDict["Mcruise"]
    clDesign = jsonDict["CLDesign"]

def readExcelFile():
    cpDataExcelPath = os.path.join(os.getcwd(), 'cpAirfoil.xlsx')
    cpDataFrame = pd.read_excel(cpDataExcelPath)
    return cpDataFrame

def datcom_cLalpha(AR, mach, sweepHalfC):
    beta =(1- mach*mach)**0.5
    sqrtPart = (4+(1+(np.tan(sweepHalfC)/beta)**2)*(AR*beta/0.95)**2)**0.5

    clAlpha = 2*np.pi*AR/(2+sqrtPart)
    return clAlpha

def M_dd(CLcruise, sweepLE, ka = 0.935, tc = 0.1):
    term1 = ka/np.cos(sweepLE)
    term2 = tc/np.cos(sweepLE)**2
    term3 = CLcruise/(10*(np.cos(sweepLE)**3))
    return term1 - term2 - term3

def alphaTrim(Cl0Alpha):
    alpha = clDesign/(np.pi*datcom_cLalpha(AR, Mcruise, sweepHalfC)/180) + Cl0Alpha
    return alpha

def crM():
    alpha = round(alphaTrim(zeroLiftAlpha), 1)
    reynolds = '9e+06'
    alpha = str(alpha) + '0'
    df = readExcelFile()
    column = f'NACA64A210-Re={reynolds}-Alpha={alpha}-'
    cpList = df[column].tolist()
    cpList.sort()
    cpMin = cpList[0]
    print(f"Cp: {cpMin}")
    m = 1/(math.sqrt(1-cpMin)*math.cos(sweepLE))
    return m


if __name__ == "__main__":
    #print(AR)
    print(f'Mach cruise: {Mcruise}')
    #print(sweepHalfC)
    #print()
    #print(np.pi*datcom_cLalpha(AR, Mcruise, sweepHalfC)/180)
    
    print(f'Trim angle: {alphaTrim(zeroLiftAlpha)}')
    print(f'Critical Mach {crM()}')
    print(f'Drag divegence {M_dd(.75, sweepLE)}')

