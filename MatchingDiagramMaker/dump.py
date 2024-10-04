import main
import json
import acparams
import weightEstimation
import os

#We will have to disconnect class I estimations later on

with open(os.getcwd()+"/Protocols/main.json") as mainJson:
    jsonDict = json.loads(''.join(mainJson.readlines()))

    #design point
    jsonDict["W/S"] = main.WSselected
    jsonDict["T/W"] = main.TWselected

    #weights
    jsonDict["MTOM"] = weightEstimation.M_mto
    jsonDict["OEM"] = weightEstimation.M_oe
    jsonDict["MFUEL"] = weightEstimation.M_f
    jsonDict["MDESPAY"] = weightEstimation.M_pl_des
    jsonDict["MMAXPAY"] = weightEstimation.M_pl_max

    #wing parameters
    jsonDict["AR"] = weightEstimation.AR
    jsonDict["S"] = weightEstimation.M_mto*acparams.g/main.WSselected

    #engine parameters
    jsonDict["THRUST"] = weightEstimation.M_mto*acparams.g*main.TWselected

    #aerodynamic parameters (Class I)
    jsonDict["OSwald"] = weightEstimation.e
    jsonDict["Cf"] = weightEstimation.C_f
    jsonDict["Cd0"] = weightEstimation.Cd_0


    print(jsonDict)

with open(os.getcwd()+"/Protocols/main.json", 'w') as mainJson:
    mainJson.write(json.dumps(jsonDict))