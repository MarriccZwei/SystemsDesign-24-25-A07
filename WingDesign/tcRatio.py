import json
import os
from math import pi
with open(os.getcwd()+"/Protocols/main.json") as jsonMain:
    dataDict = json.loads(jsonMain.readline())
    S = dataDict["S"]
    Cf = dataDict["Cf"]
    Cr = dataDict["Cr"]

def cd0_constraint(Cf, Sw, cr, wFus):
    cd0max = Cf*(2-cr*wFus/Sw)
    print(cd0max)
    return (cd0max-0.0035)/0.0018

print(cd0_constraint(Cf, S, Cr, 7))
