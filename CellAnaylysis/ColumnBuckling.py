import OOP.Cell as cell
import numpy as np
import General.Constants as consts

def crit_buckling_stress (cell:cell.Cell, tip = False):

    if tip:
        K = 0.25
    else:
        K = 4.

    sigma_buckling = K * np.pi**2 * consts.E_MODULUS * cell.sectionProperties[ixx]
    #TODO Find out how to put I in here, how to handle constant K and finish the formula
    return(sigma_buckling)
    