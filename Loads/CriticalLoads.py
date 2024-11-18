import numpy as np

# Code to be used in determining the critical load cases as determined from SBT sections
# Two critical loads will be determined, one corresponding to the positive load factor and one for the negative load factor
# data from the inertial loads and aerodynamic loads will be extrapolated 

# defining the maximum positive load factor given a range of possible values and an equation given by EASA
# where MTOM is given in lbs, if the computed value of MaxPosLF is less than 2.5 the selected value shall be 2.5
def MaxPosLF(mTOM):
    MaxPosLF = 2.1 + ((24000)/ ((mTOM/0.454) + 10000))
    if MaxPosLF < 2.5:
        MaxPosLF = 2.5
    else: 
        MaxPosLF = 2.1 + ((24000)/ ((mTOM/0.454) + 10000))
    return MaxPosLF

# defining the minimum negative load factor given a minimum value stated by EASA
# Assumed value since there is only a lower limit of -1 and most arbitrary safety factors are 1.5
def MinNegLF():
    MinNegLF = -1.5
    return MinNegLF

# critical shear load for max positive LF
def CritShear_PosLF(MaxPosLF, ):

    return CritShear_PosLF

# critical shear load for min negative LF
def CritShear_NegLF(MinNegLF, ):

    return CritShear_NegLF

# critical bending moment load for max positive LF
def CritMom_PosLF(MaxPosLF, ):

    return CritMom_PosLF

# critical bending moment load for min negative LF
def CritMom_NegLF(minPosLF, ):

    return CritMom_NegLF

# critical torque load for max positive LF
def CritTor_PosLF(MaxPosLF, ):

    return CritTor_PosLF

# critical torque load for min negative LF
def CritTor_NegLF(minPosLF, ):

    return CritTor_NegLF

