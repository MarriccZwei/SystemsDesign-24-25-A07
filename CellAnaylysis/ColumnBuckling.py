if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
from OOP.Cell import Cell
from CellAnaylysis.MoiStringerSkinAxis import moi_panel
import numpy as np
import General.Constants as consts
import OOP.Planform as pf

def crit_buckling_stress (cell:Cell, tip = False):
    """
    Calculates the critical buckling stress of the skin and stringers based on its geometry.
    
    Returns:
        list: Critical buckling stress [N/m].
    """

    #  Choosing the constant depending on the cell we are evaluating
    if tip:
        K = 0.25
    else:
        K = 4.

    #  Area of the stringer
    Area = cell.stringerDesign["t"]*cell.stringerDesign["w"] + cell.stringerDesign["t"]*cell.stringerDesign["h"] - (cell.stringerDesign["t"])**2

    # Length if stringer for testing
    Len = 10 #m

    #  Column Buckling Formula
    
    sigma_buckling_values = []
    I_xx_values, I_yy_values = moi_panel(cell, cell.stringerDesign, nPoints=10) # idk why it wants me to include the 2nd argument
    for ixx_dict in I_xx_values:
        ixx = ixx_dict["I_xx"] 
        sigma_buckling = (K * np.pi**2 * consts.E_MODULUS *ixx) / (Len**2 * Area) 
        sigma_buckling_values.append(sigma_buckling)

    return(sigma_buckling_values)
    
# # Test
# planform = pf.Planform(251.3429147793505, 9.872642920666417, 0.1, 28.503510117080133, 2.1496489882919865, False)

# # Stringer dictionary
# stringerDesign = {
#     "t": 0.002,         # Thickness of the stringer [m]
#     "w": 0.03,          # Width of the stringer base [m]
#     "h": 0.04,          # Height of the stringer [m]
#     "sb": 0.2,      # Spacing between bottom stringers [m]
#     "st": 0.2      # Spacing between top stringers [m] 
# }

# # Wingbox thicknesses dictionary
# wingboxThicknesses = {
#     "f": 0.001, # Thickness of front spar [m]
#     "t": 0.001, # Thickness of top surface [m]
#     "m": 0.001, # Thickness of middle spar [m]
#     "b": 0.001, # Thickness of bottom surface [m]
#     "r": 0.001 # Thickness of middle spar [m]
# }

# cell = Cell(planform, 10, 11, stringerDesign, wingboxThicknesses, midSpar=None)
# sigma_buckling_values = crit_buckling_stress(cell, tip = False)
# print(sigma_buckling_values)