import json
import os
from math import pi
with open(os.getcwd()+"/Protocols/main.json") as jsonMain:
    dataDict = json.loads(jsonMain.readline())
    S = dataDict["S"]

def