# import sys
# import os
# sys.path.insert(1, os.getcwd())

import General.ISA as ISA

CRUISEALTITUDE = 11887.2
CRUISEMACH = 0.82
CRUISEVELOCITY = CRUISEMACH*ISA.speedOfSound(CRUISEALTITUDE)
CRUISEDENSITY = ISA.density(CRUISEALTITUDE)
