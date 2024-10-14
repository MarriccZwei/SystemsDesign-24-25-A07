if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING

import OOP.Planform as pf
import General.Constants as consts

'''A subfunction finding a change in load factor for a certain case'''
def delta_n_situation(planform:pf.Planform, clalpha, WS, speed, uhat, rho):
    muG = 2*WS/( rho*clalpha*consts.G*planform.MAC) #the \mu_g formula from the formula sheet
    K = 0.88*muG/(5.3+muG) #the K formula from the formula sheet
    u = K*uhat
    return  rho*speed*clalpha*u/2/WS #the delta N formula from the formula sheet

'''Finding the ultimate load factor'''
#cL_alpha in the radian form, mass for the most constraining situation, for now ffels like landing mass
def n_ult(planform:pf.Planform, clalpha, MTOW, sf = 1.5):
    WSTO = consts.G*MTOW/planform.S
    deltaNs = list() #a list of load factor from considered conditions
    
    #cruise condition
    deltaNs.append(delta_n_situation(planform, clalpha, (0.95+0.7)/2*WSTO, consts.CRUISEVELOCITY, consts.CRUISEUHAT, consts.CRUISEDENSITY))

    #landing at SL condition (maximum aoa)
    deltaNs.append(delta_n_situation(planform, clalpha, 0.7*WSTO, consts.VAPPROACH, consts.LANDINUHAT, consts.SLDENSITY))

    #After all the situations have been considered
    deltaN = max(deltaNs)

    #Adding the nominal Load Factor and multiplying by the safety factor
    return 1.5*(consts.NMAXNOMINAL+deltaN)
