# import sys
# import os
# sys.path.insert(1, os.getcwd())
from General import ISA

"""NATURAL CONSTANTS"""
G = 9.81 #to uniformize the assumed value
GAMMA = 1.4

"""WEIGHT ESTIMATION"""
MAXPAYLOAD = 49442
DESIGNPAYLOAD = 27669

MAXPAYLOADRANGE = 13983
DESIGNRANGE = 13797
FERRYRANGE = 15811

NMAXNOMINAL = 2.5 #because we definitely are the big aircraft
CRUISEUHAT = 37.5*0.3048 #value read for the graph, subject to scrutiny #converted from ft
LANDINUHAT = 65*0.3048 #value read for the graph, subject to scrutiny #converted from ft

SVTAIL = 100 #THIS VALUE IS WRONG, WHEN CALCULATED PLUG HERE: vertical tail area
SHTAIL = 100 #THIS VALUE IS WRONG, WHEN CALCULATED PLUG HERE: horizontal tail area
FW = 100 #THIS VALUE IS WRONG, WHEN CALCULATED PLUG HERE: fuselage widht at horizontal tail intersection
LT = 10 #THIS VALUE IS WRONG, WHEN CALCULATED PLUG HERE: tail lenght
SWEEPHT = 0.18 # THIS VALUE IS WRONG, WHEN CALCULATED PLUG HERE: horizontal tail sweep RADIANS!!!
SE = 10 # THIS VALUE IS WRONG, WHEN CALCULATED PLUG HERE: Elevator area
ARHTAIL = 5 # THIS VALUE IS WRONG, WHEN CALCULATED PLUG HERE: horizontal tail Aspect Ratio
BH = 10 # # THIS VALUE IS WRONG, WHEN CALCULATED PLUG HERE: horizontal tail span

KDOOR = 1.12  # Constant for amount of cargo doors, check Raymer weight estimation
KLG = 1.  # Constant depending on Landing gear attachement, if it i fuselage mounted the constant equals 1.12, otherwise = 1.0
KUHT = 1.143  # unit horizontal tail, check raymer to change

FXTEQPTMF = 0.1 #fixed equipment mass fraction
OEWCGWRTLEMACPERMAC = 0.25 #OEW xCg wrt xLEMAC as a fraction of MAC chord (a design choice)

"""GENERAL"""
VSTALL = 60 #This is maybe a bit high for the stall landing speed 
VAPPROACH = 1.23*VSTALL
ULTIMATECL = 2.5


"""TAKEOFF"""
TAKEOFFMACH = VAPPROACH/ISA.speedOfSound(0)
TAKEOFFCL = 1.8
KT = 0.85 #assumed from reader
TAKEOFFLENGTH = 2790  # [m]

"""CRUISE"""
CRUISEALTITUDE = 11887.2
CRUISEMACH = 0.82
CRUISEVELOCITY = CRUISEMACH*ISA.speedOfSound(CRUISEALTITUDE)
CRUISEDENSITY = ISA.density(CRUISEALTITUDE)
BETA_CRUISE = (0.95+0.7)/2
CRUISEROC = 2 # [m/s]
CRUISESOUNDSPEED = ISA.speedOfSound(CRUISEALTITUDE)
CRUISEVELOCITY = CRUISEMACH*CRUISESOUNDSPEED
CRUISEVISCOSITY = 0.00001432

"""LAND"""
LANDMACH = VAPPROACH/ISA.speedOfSound(0)
BETA_LAND = 0.7
LANDDENSITY = 1.25
LANDLENGTH = 1856 # [m] (Class I weight estimation)

"""SEALEVEL"""
SLDENSITY = ISA.density(0)
SLTEMPERATURE = ISA.temperature(0)
SLPRESSURE = ISA.pressure(0)

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

"""'MATCHINGDIAGRAM"""
CLFL = 0.45
LANDINGDISTANCE = 1856
TAKEOFFDISTANCE = 2790
THETABREAK = 1.07
CLIMBRATE = 2
CLIMBRATEALTITUDE = CRUISEALTITUDE

"""ENGINE"""
SPECIFICENERGY = 43500000
BYPASS = 12 #Probably has to change
ENGINEXWRTLEMAC = 2 #position of engine CG w.r.t. xLEMAC of the wing - has to be read off the cad drawing

'''FUSELAGE'''
DEQUIVALENT = 5.306295
LFUS = 60.69367942857143
LN = 4
LNC = 9.551331
LT = 12.735108
LTC = 15.918885

'''LG'''
NWN = 2 #2 wheels for the nose landing gear
NWM = 4*4 #4 wheels per 4 struts on the main landing gear
NSTRUTS = 4 #4 struts of the main landing gear