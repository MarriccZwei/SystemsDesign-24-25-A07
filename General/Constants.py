# import sys
# import os
# sys.path.insert(1, os.getcwd())

from General import ISA

"""TAKEOFF"""
TAKEOFFMACH = 0.2
TAKEOFFLENGTH = 2790#meters
TAKEOFFDENSITY = 1.225

"""CRUISE"""
CRUISEALTITUDE = 11887.2
CRUISEMACH = 0.82
CRUISEVELOCITY = CRUISEMACH*ISA.speedOfSound(CRUISEALTITUDE)
CRUISEDENSITY = ISA.density(CRUISEALTITUDE)
CRUISETEMPERATURE = ISA.temperature(CRUISEALTITUDE)

DESIGNRANGE = 13797#km
FERRYRANGE = 15811#km
MAXPAYLOADRANGE = 13983#km

"""LAND"""
LANDMACH = 0.2
LANDLENGTH = 1856#meters
LANDDENSITY = 1.225

"""AIRFOIL"""
CLMAXAIRFOIL = 1.6
THICKNESSTOCHORD = 0.1

"""HIGH LIFT DEVICES"""
TAKEOFFHLDDEPLOYMENT = 0.6
KRUGERFLAPS = True
SINGLESLOTFLAPS = True

"""PAYLOAD"""
MAXPAYLOAD = 49442#kg
DESIGNPAYLOAD = 27669#kg

"""MISC CONSTANTS"""
G = 9.81
KT = 0.85#used for TO length matching diagram, assumed from reader
CLFL = 0.45#constant given by CS25