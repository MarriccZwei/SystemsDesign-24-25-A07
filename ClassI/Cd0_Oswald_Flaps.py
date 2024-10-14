import numpy as np
import os

def Cd0_Oswald_flaps(flap_defl, normal_e, Cd0, lg_deflected):
    
     
    change_e = 0.0026 * flap_defl # Formula for change in efficiency with flaps
    change_Cd0_flaps = 0.0013 * flap_defl # Formula for change in Cd0 with flaps
    change_Cd0_lg = 0.025  # Worst case scenario

    total_e = normal_e + change_e
    total_Cd0 = change_Cd0_flaps + change_Cd0_lg + Cd0

    if lg_deflected == True:  # Condition if the landing gear is extended or not
        total_Cd0 += change_Cd0_lg

    #print('Total Oswald efficiency: ', round(total_e, 2))
    #print('Total Cd0: ', round(total_Cd0, 2))

    return total_Cd0, total_e


def V2(): #calculate V2
    Cd0TO, eTO = Cd0_Oswald_flaps(5, acparams.OSWALD, acparams.CD_0, True)
    CLopt = np.sqrt(np.pi*acparams.ASPECT*eTO*Cd0TO)
    V2 = np.sqrt(8650*2/1.225/CLopt)
    print(V2)


