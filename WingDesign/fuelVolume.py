import json
import os
import numpy as np

def fuel_volume(A2c2, b, cr, tr, safetyFactor=1.3):
    return A2c2*b/safetyFactor*cr*cr/3*(1+tr+tr*tr)

if __name__ == "__main__":
    with open(os.getcwd()+"/Protocols/main.json") as mainJson:
        jsonDict = json.loads(''.join(mainJson.readlines()))
        cr = jsonDict["Cr"]
        tr = jsonDict["tr"]
        b = jsonDict["b"]
    
    volumeCoeffs = np.array([0.038])
    Volumes = fuel_volume(volumeCoeffs, b, cr, tr)

    print(Volumes)