import weightEstimation as we

#here be all the aircraft parameters needed for the matching diagram
#such as e.g. skin friction coefficient
#in the form of python variables
#if u don't use a var, don't change it

#Propulsion constants
BYPASS = 10 #pls keep between 5 and 15

#Aerodynamics + wing form constants
TMIN=0.7
CLMAX = 2.5 #est. equal to the highrer of the other cls
CD_0 = we.Cd_0 # linked to previous assignments
ASPECT = we.AR # linked to previous assignments
OSWALD = we.e # linked to previous assignments

#Takeoff constants
TAKEOFF_LENGTH = 2790  # [m]
CLMAX_TAKEOFF = 1.8

#Cruise constants
CRUISE_ALTITUDE = 12000 # [m]
MACH_CRUISE = 0.82
BETA_CRUISE = 0.95
ROC_CRUISE_ALT = 1 # [m/s]

#Landing constants
VSTALL = 75 # [m/s]
CLMAX_LAND = 2.5 # estimation
LAND_LENGTH = 1856 # [m] (Class I weight estimation)
RHO_LAND = 1.225 # [kg/m^3]
BETA_LAND = 0.73 # Landing mass fraction (estimation from reference aircraft)

#Misc. constants
CLFL = 0.45 # CS-25 specification
K_T = 0.85 #  assumed from reader
H_2 = 11  # air distance assumed from reader [m]
g = 9.81 # [m/s]