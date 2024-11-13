# import sys
# import os
# sys.path.insert(1, os.getcwd())
from General import ISA
import numpy as np

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

VHTAIL = 0.87
VVTAIL = 0.065
XH = 55 # horizontal tail x w.r.t nose
XV = 50 # vertical tail x w.r.t nose
SWEEPHT = np.radians(36) #  horizontal tail sweep RADIANS!!!
SWEEPVT = np.radians(40) #  vertical tail sweep RADIANS!!!
ARHTAIL = 4 #  horizontal tail Aspect Ratio
ARVTAIL = 1.8 #  vertical tail Aspect Ratio
TRHTAIL = 0.3 # horizontal tail taper ratio
TRVTAIL = 0.3 # vertical tail taper ratio
TCH = .09 #thickness to chord for the horizontal tail
TCR = .09 #thickness to chord for the vertical tail

KDOOR = 1.12  # Constant for amount of cargo doors, check Raymer weight estimation
KLG = 1.  # Constant depending on Landing gear attachement, if it i fuselage mounted the constant equals 1.12, otherwise = 1.0
KUHT = 1. # unit horizontal tail, check raymer to change

FXTEQPTMF = 0.1 #fixed equipment mass fraction
OEWCGWRTLEMACPERMAC = 0.25 #OEW xCg wrt xLEMAC as a fraction of MAC chord (a design choice)
WNGCGWRTLEMACPERMAC = 0.4 #Wing xCg wrt xLEMAC as a fraction of MAC chord (a design choice)
FUELTANKSN = 8
CTRLSURFAREAFRAC = 0.33 #fraction of rudder/elevator area to vert. tail/ hor. tail area

"""GENERAL"""
VSTALL = 58 #This is maybe a bit high for the stall landing speed 
VAPPROACH = 1.23*VSTALL
ULTIMATECL = 2.5
KEROSENEDENSITY = 795 # [kg/m^3] ; fuel density

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
CRUISEROC = 0.5 # [m/s]
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
CM = -0.04

"""HIGH LIFT DEVICES"""
TAKEOFFHLDDEPLOYMENT = 0.6
DELTACCFLAND = 0.6
DELTACCFTAKEOFF = 0.48
FLAPFACTOR = 1.3
KRUGERDELTACL = 0.3
DELTAALPHA0LLANDING = -15
DELTAALPHA0LTAKEOFF = -10
TODEFLECTION = 15
LADEFELCTION = 40

"""'MATCHINGDIAGRAM"""
LANDINGDISTANCE = 1856
LANDINGALTITUDE = 0
TAKEOFFDISTANCE = 2790
TAKEOFFALTITUDE = 0
THETABREAK = 1.07


"""ENGINE"""
SPECIFICENERGY = 43500000
BYPASS = 9.6 #Probably has to change
ENGINEXWRTLEMAC = 2 #position of engine CG w.r.t. xLEMAC of the wing - has to be read off the cad drawing
ENGINEMASS = 7550 #[kg]; engin mass
NACELLELEN = 5.812 #[m] ; nacelle legth
DINLET = 3 #[m] ; inled diameter
DNACELLE = DINLET+0.06*0.65*NACELLELEN+0.03 # in [m] used for class II weight
ENGINESPANWISEPOS = 0.3 #as a fraction of halfspan

'''FUSELAGE'''
DEQUIVALENT = 5.306295
LFUS = 60.69367942857143
LN = 4
LNC = 9.551331
LT = 12.735108
LTC = 15.918885
UPSWEEP = 4
ABASE = 2
AMAX = 24.1
NPAX = 263
FW = 0.5*DEQUIVALENT # fuselage widht at horizontal tail intersection

'''LG'''
NWN = 2 #2 wheels for the nose landing gear
NWM = 2*6 #6 wheels per 2 struts on the main landing gear
NSTRUTS = 2 # per main landing gear
HEIGHTMAIN = 1.143 #m
HEIGHTFRONT = 1.0922 #m
WWHEELMAIN = 42.545*10**-2 #m
WWHEELFRONT = 31.75*10**-2 #m
WSTRUT = 20*10^-2 #m
TailScrape = 10 # degrees 
AbsorberStroke = 0.3 # m
phi = 9 # degrees
psi = 55 # degrees
LF = 0.90 # LOAD FACTOR MLG
