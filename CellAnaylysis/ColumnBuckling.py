import OOP.Cell as cell
import numpy as np
import General.Constants as consts

<<<<<<< HEAD
def crit_buckling_stress (cell:cell.Cell, tip = False):

=======
def crit_buckling_stress (cell:Cell, tip = False):
    """
    Calculates the critical buckling stress of the skin and stringers based on its geometry.
    
    Returns:
        list: Critical buckling stress [N/m].
    """
#
>>>>>>> recovery2
    #  Choosing the constant depending on the cell we are evaluating
    if tip:
        K = 0.25
    else:
        K = 4.

    #  Area of the stringer
    Area = cell.stringerDesign["t"]*cell.stringerDesign["w"] + cell.stringerDesign["t"]*cell.stringerDesign["h"] - (cell.stringerDesign["t"])**2

    #  Column Buckiling Formula
    sigma_buckling = (K * np.pi**2 * consts.E_MODULUS * cell.sectionProperties["ixx"]) / ((cell.zLen)**2 * Area) 

    return(sigma_buckling)
    