if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
import json
import os

from General import Constants
import pitchUpConstraint

#We will have to disconnect class I estimations later on

with open(os.getcwd()+"/ClassI/output.json") as mainJson:
    jsonDict = json.loads(''.join(mainJson.readlines()))

    star = pitchUpConstraint.sweepTaperAspect(Constants.CRUISEMACH)
    jsonDict["sweep"] = star[0]
    jsonDict["TR"] = star[1]
    jsonDict["AR"] = star[2]

    

    print(jsonDict)

"""
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
    jsonDict["TSFC"] = weightEstimation.TSFC

    #aerodynamic parameters (Class I)
    jsonDict["Oswald"] = weightEstimation.e
    jsonDict["Cf"] = weightEstimation.C_f
    jsonDict["Cd0"] = weightEstimation.Cd_0"""

with open(os.getcwd()+"/ClassI/output.json", "w") as mainJson:
    mainJson.write(json.dumps(jsonDict))