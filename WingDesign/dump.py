import json
import os
import numpy as np
import planform
import HLDs
import stallConditions
import rollRate
import CLdesign
import CruiseConditions

with open(os.getcwd()+"/Protocols/main.json") as mainJson:
    jsonDict = json.loads(''.join(mainJson.readlines()))
    jsonDict["b"] = planform.b
    jsonDict["tr"] = planform.TaperRatio
    jsonDict["sweep"] = planform.QuarterSweep
    jsonDict["MAC"]=planform.MACList[0]
    jsonDict["XMAC"]=planform.MACList[1]
    jsonDict["YLEMAC"]=planform.MACList[2]
    jsonDict["sweepC/2"] = planform.SweepList[0]
    jsonDict["sweepLE"]=planform.SweepList[1]
    jsonDict["sweepTE"] = planform.SweepList[2]
    jsonDict["dihedral"] = planform.dihedral
    jsonDict["Cr"] = planform.CList[0]
    jsonDict["Ct"] = planform.CList[1]
    #jsonDict["bEndHLD"] = HLDs.y
    jsonDict["CLmaxClean"] = stallConditions.maxCL(1.69, '64a210')
    #jsonDict["CLmaxTO"] = stallConditions.maxCL(1.5, '64a210')[1]
    #jsonDict["CLmaxLand"] = stallConditions.maxCL(1.5, '64a210')[2]
    jsonDict["rollRate"] = rollRate.rollRate(7, 15, 0.25, 80, 10, 0.75)
    jsonDict["CLDesign"] = CLdesign.cL
    jsonDict["UltimateCL"] = 2.5
    jsonDict["Incidence"] = CruiseConditions.alphaTrim(-1.25)
    jsonDict["AR"] = planform.AR


with open(os.getcwd()+"/Protocols/main.json", 'w') as mainJson:
    mainJson.write(json.dumps(jsonDict))