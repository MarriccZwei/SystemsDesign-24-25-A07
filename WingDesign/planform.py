import PlanformEstimate as PE
import json
import os
from math import pi
with open(os.getcwd()+"/Protocols/main.json") as jsonMain:
    dataDict = json.loads(jsonMain.readline())
S = dataDict["S"]
M = 0.82
AR = dataDict["AR"]
QuarterSweep = PE.SweepEst(M)
TaperRatio = PE.TaperRatioEst(QuarterSweep)
b = PE.WingSpan(AR, S)

CList = PE.RootAndTipChord(S, TaperRatio, b)

SweepList = PE.LambdaFinder(b, CList[1], CList[0], QuarterSweep)

MACList = PE.MAC(SweepList[1], SweepList[2], b, CList[0], CList[1])

print(QuarterSweep)
print(b)
print(CList)
print(QuarterSweep)
print(MACList)