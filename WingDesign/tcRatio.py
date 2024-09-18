import json
import os
from math import pi
with open(os.getcwd()+"/Protocols/main.json") as jsonMain:
    dataDict = json.loads(jsonMain.readline())
    S = dataDict["S"]
    Cf = dataDict["Cf"]

def cd0_constraint(Cf, Sw, cr, wFus):
    cd0max = Cf*(2-cr*wFus/Sw)
    return (cd0max-0.0035)/0.0018
