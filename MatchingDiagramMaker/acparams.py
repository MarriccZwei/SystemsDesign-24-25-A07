#here be all the aircraft parameters needed for the matching diagram
#such as e.g. skin friction coefficient
#in the form of python variables
#if u don't use a var, don't change it

TMIN=0.7
CLMAX = 1.2
VSTALL = 5 # [m/s]
CLMAX_LAND = 2.2 
LAND_LENGTH = 1500 # [m]
RHO_LAND = 1.225 # [kg/m^3]
BETA_LAND = 0.9 # Landing mass fraction
CLFL = 0.45 # CS-25 specification
K_T = 0.85 #  assumed from reader
TAKEOFF_LENGTH = 2790  # [m]
H_2 = 11  # air distance assumed from reader [m]
g = 9.81 # [m/s]
CRUISE_ALTITUDE = 12000 # [m]
MACH_CRUISE = 0.82
BETA_CRUISE = 0.95
CD_0 = 0.01 # to be changed
ASPECT = 10 # to be changed
OSWALD = 0.8 # to be changed
