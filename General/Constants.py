# import sys
# import os
# sys.path.insert(1, os.getcwd())
from General import ISA

"""NATURAL CONSTANTS"""
G = 9.81 #to uniformize the assumed value

"""WEIGHT ESTIMATION"""
NMAXNOMINAL = 2.5 #because we definitely are the big aircraft
CRUISEUHAT = 37.5 #value read for the graph, subject to scrutiny
LANDINUHAT = 65 #value read for the graph, subject to scrutiny

"""GENERAL"""
VSTALL = 75 #This is maybe a bit high for the stall speed
VAPPROACH = 1.23*VSTALL
ULTIMATECL = 2.5


"""TAKEOFF"""
TAKEOFFMACH = VAPPROACH/ISA.speedOfSound(0)

"""CRUISE"""
CRUISEALTITUDE = 11887.2
CRUISEMACH = 0.82
CRUISEVELOCITY = CRUISEMACH*ISA.speedOfSound(CRUISEALTITUDE)
CRUISEDENSITY = ISA.density(CRUISEALTITUDE)

"""LAND"""
LANDMACH = VAPPROACH/ISA.speedOfSound(0)
SLDENSITY = ISA.density(0)

"""DIVERT"""
DIVERSIONRANGE = 370#km
LOITERTIME = 45#min
CONTINGENCYFUELFRACTION = 0.05

"""AIRFOIL"""
CLMAXAIRFOIL = 1.6
ALPHAZEROLIFT = -1.66 #DEGREE
THICKNESSTOCHORD = 0.1
CD0 = 0.009
DCLALPHA = 0.111 #PER DEGREE

"""HIGH LIFT DEVICES"""
TAKEOFFHLDDEPLOYMENT = 0.6




