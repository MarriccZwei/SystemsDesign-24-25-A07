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
dihedral = PE.Dihedral(QuarterSweep)

test = PE.PitchUp(TaperRatio, QuarterSweep, AR)
if test:
    print("your aircraft matches stability conditions")
else:
    print("your aircraft does NOT meet the stability conditions ")

print()
print("Wingspan: ")
print(str(b), "[m]")
print("Root Chord: ")
print(str(CList[0]), "[m]")
print("Tip Chord: ")
print(str(CList[1]), "[m]")
print("Quarter Chord Sweep:")
print(str(QuarterSweep * 180 / pi), "[deg]")
print("dihedral angle")
print(str(dihedral * 180 / pi), "[deg]")
print("MAC:")
print(str(MACList[0]), "[m]")
print("XMAC:")
print(str(MACList[1]), "[m]")
print("YLEMAC:")
print(str(MACList[2]), "[m]")
print("Taper Ratio:")
print(str(TaperRatio), "[-]")
print("half chord Sweep:")
print(str(SweepList[0] * 180 / pi), "[deg]")
print("Leading Edge Sweep:")
print(str(SweepList[1] * 180 / pi), "[deg]")