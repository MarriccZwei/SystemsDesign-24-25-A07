if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
from math import sqrt, pi, exp, log
from General import Constants

def TSFC(bypass):
    return(22 * bypass**(-0.19))

def engineEfficiency(TSFC):
    Constants.CRUISEVELOCITY / (TSFC* Constants.SPECIFICENERGY)* (10**6)

def Rlost(L_D):
    return  (1/0.7) * L_D * (Constants.CRUISEALTITUDE + (Constants.CRUISEVELOCITY**2)/(2*Constants.G))

def Req(L_D):
     R_nom  = Constants.DESIGNRANGE*1000
     R_lost = Rlost(L_D)
     F_con = Constants.CONTINGENCYFUELFRACTION
     R_div = Constants
     return ((R_nom + R_lost) * (1 + F_con) + 1.2 * R_div + Constants.CRUISEVELOCITY * Constants.LOITERTIME)

def Raux(L_D):
    return Req(L_D) - Constants.DESIGNRANGE

def MFfuel(L_D, TSFC):
     return (1 - exp(-Req(L_D) / (engineEfficiency(TSFC) * (Constants.SPECIFICENERGY/ Constants.G) * L_D)))

def mtom(MFoe, L_D, TSFC):
    return (Constants.MAXPAYLOAD)/(1 - MFfuel(L_D, TSFC) - MFoe)

def Moe(MFoe, L_D, TSFC):
    return MFoe * mtom(MFoe, L_D, TSFC)

def Mfuel(MFoe, L_D, TSFC):
    return mtom(MFoe, L_D, TSFC) - MFoe*mtom(MFoe, L_D, TSFC) - Constants.MAXPAYLOAD

def Rferry(MFoe, L_D, TSFC):
    return (engineEfficiency(TSFC) * L_D * (Constants.SPECIFICENERGY/ Constants.G) * log((Moe(MFoe, L_D, TSFC) + Mfuel(MFoe, L_D, TSFC))/(Moe(MFoe, L_D, TSFC))) - Raux(L_D))

def Rharm(MFoe, L_D, TSFC):
    return (engineEfficiency(TSFC) * L_D * (Constants.SPECIFICENERGY/ Constants.G) * log(Constants.MAXPAYLOAD + (Moe(MFoe, L_D, TSFC) + Mfuel(MFoe, L_D, TSFC))/(Moe(MFoe, L_D, TSFC))) - Raux(L_D))

def oswald(AR, D_par = 0.0075, eff_span = 0.97):
    return (1/(pi * AR * D_par + (1/eff_span)))