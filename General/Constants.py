# import sys
# import os
# sys.path.insert(1, os.getcwd())
from General import ISA

"""NATURAL CONSTANTS"""
G = 9.81 #to uniformize the assumed value

"""WEIGHT ESTIMATION"""
MAXPAYLOAD = 49442
DESIGNPAYLOAD = 27669

MAXPAYLOADRANGE = 13983
DESIGNRANGE = 13797
FERRYRANGE = 15811

NMAXNOMINAL = 2.5 #because we definitely are the big aircraft
CRUISEUHAT = 37.5*0.3048 #value read for the graph, subject to scrutiny #converted from ft
LANDINUHAT = 65*0.3048 #value read for the graph, subject to scrutiny #converted from ft
SVTAIL = 100 #THIS VALUE IS WRONG, WHEN CALCULATED PLUG HERE
FW = 100 #THIS VALUE IS WRONG, WHEN CALCULATED PLUG HERE: fuselage widht at horizontal tail intersection
LT = 10 ##THIS VALUE IS WRONG, WHEN CALCULATED PLUG HERE: tail lenght
KDOOR = 1.12  # Constant for amount of cargo doors, check Raymer weight estimation
KLG = 1.  # Constant depending on Landing gear attachement, if it i fuselage mounted the constant equals 1.12, otherwise = 1.0
KUHT = 1.143  # unit horizontal tail, check raymer to change

"""GENERAL"""
VSTALL = 75 #This is maybe a bit high for the stall landing speed 
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
DELTACCFLAND = 0.6
DELTACCFTAKEOFF = 0.48
FLAPFACTOR = 1.3
KRUGERDELTACL = 0.3
DELTAALPHA0LLANDING = -15
DELTAALPHA0LTAKEOFF = -10

"""PROPULSION"""
SPECIFICENERGY = 43500000#J/kg, spec eng of the fuel