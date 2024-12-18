import OOP.Cell as cell
import numpy as np
#import General.Constants as consts

# Create stringer dictionary
strDes = {
    "t": 0.002,         # Thickness of the stringer [m]
    "w": 0.01,          # Width of the stringer base [m]
    "h": 0.05,          # Height of the stringer [m]
    "spacing": 0.2      # Spacing between adjacent stringers [m] 
}

# MOI of individual stringers (used for local buckling)
def moi_stringer(strDes):
    """
    Calculates the moment of inertia (MOI) of a single stringer based on its geometry.
    
    Parameters:
        strDes (dict): Dictionary containing stringer design parameters:
            - "t": Thickness of the stringer [m]
            - "w": Width of the stringer base [m]
            - "h": Height of the stringer [m]
            - "spacing": Spacing between adjacent stringers [m] (optional)
    
    Returns:
        float: Moment of inertia (MOI) [m^4].
    """
    t = strDes["t"]  # Thickness [m]
    w = strDes["w"]  # Width [m]
    h = strDes["h"]  # Height [m]

    x_bar = (h*t+w**2)/(2*(h+w))
    y_bar = (h**2/2+w*h)/(h+w)
    
    I_xx_str = (t*h**3)/12 + t*h*(h/2-y_bar)**2 + w*t**3/12 + t*w*(h-y_bar)**2
    I_yy_str = (h*t**3)/12 + t*h*(t/2-x_bar)**2 + (t*w**3)/12 + t*w*(w/2-x_bar)**2
    
    return I_xx_str, I_yy_str, x_bar, y_bar


# MOI of skin and stringers (used for global buckling)
def moi_panel(cell:cell.Cell, strDes, nPoints=10):
    """
    Calculates the moment of inertia (MOI) of all stringers placed along a line, evaluated at multiple spanwise positions.

    Parameters:
        stringerDesign (dict): Dictionary containing stringer geometry parameters:
            - "t": Thickness of the stringer [m]
            - "w": Width of the stringer base [m]
            - "h": Height of the stringer [m]
            - "spacing": Spacing between adjacent stringers [m] (optional)
        cellObj (Cell): An instance of the Cell class, used for geometry and spanwise properties.
        nPoints (int): Number of spanwise positions to evaluate (default is 10).

    Returns:
        list: List of MOI values for all stringers at each spanwise position.
    """
    t = strDes["t"]  # Thickness [m]
    w = strDes["w"]  # Width [m]
    h = strDes["h"]  # Height [m]
    # Generate nPoints spanwise positions (normalized from 0 to 1)
    spanwise_positions = np.linspace(0, 1, nPoints)
    
    # Initialize lists to store MOI values at each position
    I_xx_values = []
    I_yy_values = []
    
    for pos in spanwise_positions:
        # Get the actual spanwise location using the Cell class
        spanwise_location = cell.spanwisePos(pos)
        
        # Example: For simplicity, assume the line is between point1 and point2 (you can adjust this)
        # Point1 and Point2 represent the start and end of the line in 2D space (e.g., leading edge of the wingbox)
        point1 = (spanwise_location, 0)  # Start of the line (e.g., spanwise_location, 0)
        point2 = (spanwise_location, 1)  # End of the line (e.g., spanwise_location, 1)
        
        # Get the positions of stringers along the line using the function _stringers_along_a_line
        stringer_positions = cell._stringers_along_a_line(point1, point2, stringerN=10, stringerWidth=w)

        # Calculate the centroid coordinates of the line (the midpoint of point1 and point2)
        x_centroid = (point1[0] + point2[0]) / 2
        y_centroid = (point1[1] + point2[1]) / 2  # This will likely be zero, but we calculate it for clarity.
        
        # Calculate the MOI for each stringer at the given position
        I_xx = 0
        I_yy = 0
        for position in stringer_positions:
            # Calculate MOI for the current stringer 
            I_xx_str, I_yy_str, x_bar_str, y_bar_str = moi_stringer(strDes)

            # Parallel axis controbution
            I_xx = I_xx_str + (h*t+w*t-t**2) * (h-y_bar_str)**2 
            I_yy = I_yy_str + (h*t+w*t-t**2) * (x_centroid-x_bar_str)**2 
            
        # Save the MOI and spanwise location
        I_xx_values.append({
            "spanwise_location": spanwise_location,
            "I_xx": I_xx
        })
        I_yy_values.append({
            "spanwise_location": spanwise_location,
            "I_yy": I_yy
        })
    
    return I_xx, I_yy