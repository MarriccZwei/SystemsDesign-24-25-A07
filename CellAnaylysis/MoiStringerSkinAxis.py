if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
from OOP.Cell import Cell
import OOP.Planform as pf
import numpy as np
#import General.Constants as consts

# Stringer dictionary
stringerDesign = {
    "t": 0.002,         # Thickness of the stringer [m]
    "w": 0.03,          # Width of the stringer base [m]
    "h": 0.04,          # Height of the stringer [m]
    "sb": 0.2,      # Spacing between bottom stringers [m]
    "st": 0.2      # Spacing between top stringers [m] 
}

# MOI of individual stringers (used for local buckling)
def moi_stringer(stringerDesign):
    """
    Calculates the moment of inertia (MOI) of a single stringer based on its geometry.
    
    Returns:
        float: Moment of inertia (MOI) [m^4].
    """
    t = stringerDesign["t"]  # Thickness [m]
    w = stringerDesign["w"]  # Width [m]
    h = stringerDesign["h"]  # Height [m]

    x_bar = (h*t+w**2)/(2*(h+w))
    y_bar = (h**2/2+w*h)/(h+w)
    
    I_xx_str = (t*h**3)/12 + t*h*(h/2-y_bar)**2 + w*t**3/12 + t*w*(h-y_bar)**2
    I_yy_str = (h*t**3)/12 + t*h*(t/2-x_bar)**2 + (t*w**3)/12 + t*w*(w/2-x_bar)**2
    
    return I_xx_str, I_yy_str, x_bar, y_bar


# MOI of skin and stringers (used for global buckling)
def moi_panel(cell:Cell, stringerDesign, nPoints=10):
    """
    Calculates the moment of inertia (MOI) of all stringers placed along a line, evaluated at multiple spanwise positions.

    Returns:
        list: List of MOI values for all stringers at each spanwise position.
    """
    t = stringerDesign["t"]  # Thickness [m]
    w = stringerDesign["w"]  # Width [m]
    h = stringerDesign["h"]  # Height [m]
    # Generate nPoints spanwise positions (normalized from 0 to 1)
    spanwise_positions = np.linspace(0, 1, nPoints)
    
    # Initialize lists to store MOI values at each position
    I_xx_values = []
    I_yy_values = []
    
    for pos in spanwise_positions:
      
        spanwise_location = cell.spanwisePos(pos)
      
        point1 = (spanwise_location, 0)  # Start of the line (e.g., spanwise_location, 0)
        point2 = (spanwise_location, 1)  # End of the line (e.g., spanwise_location, 1)
        
        stringer_positions = cell._stringers_along_a_line(point1, point2, stringerN=10, stringerWidth=w)

        # Calculate the centroid coordinates of the line (the midpoint of point1 and point2)
        x_centroid = (point1[0] + point2[0]) / 2
        y_centroid = (point1[1] + point2[1]) / 2  
        
        
        I_xx_pan = 0
        I_yy_pan = 0
        for x_pos, y_pos in stringer_positions: 
            I_xx_str, I_yy_str, x_bar_str, y_bar_str = moi_stringer(stringerDesign)

            # Parallel axis controbution
            I_xx_pan = I_xx_str + (h*t+w*t-t**2) * (h-y_bar_str)**2 
            I_yy_pan = I_yy_str + (h*t+w*t-t**2) * (x_centroid-x_pos)**2 
            
        I_xx_values.append({
            "spanwise_location": spanwise_location,
            "I_xx": I_xx_pan
        })
        I_yy_values.append({
            "spanwise_location": spanwise_location,
            "I_yy": I_yy_pan
        })
    
    return I_xx_values, I_yy_values

# Test
# I_xx_str, I_yy_str, x_bar_str, y_bar_str = moi_stringer(stringerDesign)
# print(I_xx_str, I_yy_str, x_bar_str,y_bar_str)

# planform =pf.Planform(251.3429147793505, 9.872642920666417, 0.1, 28.503510117080133, 2.1496489882919865, False)
# halfspan = planform.b/2
# mWing = 22962.839350654576
# mEngine = 3554.759960907367/2 #divide by two as we are looking at the half-span only
# thrust = 91964.80101516769
# wgboxArea = 123.969 #[m^2] measured in CATIA

# wingboxThicknesses = {
#     "f": 0.001, #m
#     "t": 0.001, #m
#     "m": 0.001, #m
#     "b": 0.001, #m
#     "r": 0.001 #m
# }

# cell = Cell(planform, 10, 11, stringerDesign, wingboxThicknesses, midSpar=None)
# I_xx_values, I_yy_values = moi_panel(cell, stringerDesign, nPoints=10)
# print(I_xx_values, I_yy_values)