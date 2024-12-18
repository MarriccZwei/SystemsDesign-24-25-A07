if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
import numpy as np
from Deflections.wingbox import wingbox

# Function to define the segments of the cross-section
'L_i spars of the wingbox'
'x upper segment of the wingbox'
'd bottom segment of the wingbox'
't_f, t_s, t_m are the thicknesses of the different segments'

def get_segments(L1, L2, L3, x, t_f, t_s, t_m):
    alpha = np.arctan((L1 - L3) / x)
    d = x / np.cos(alpha)

    segments = {
        # Express the position of a segment with the wingbox dimensions in variable form
        "x": {"i": x/2, "j": t_f/2, "length": x, "thickness": t_f},
        "L1": {"i": 0, "j": L1/2, "length": L1, "thickness": t_s},
        "L2": {"i": x/2, "j": L2/2, "length": L2, "thickness": t_m},
        "L3": {"i": x, "j": L3/2, "length": L3, "thickness": t_s},
        "d": {"i": x/2, "j": (L1 - ((d/2) * np.sin(alpha))), "length": d, "thickness": t_f},
    }
    return segments, alpha

# Function to define the sringers of the cross-section
'h_str is the height of the stringer'
'w_str is the width of the stringer'
't_str is the thickness of the stringer'
'stringer_hor_spacing is the horizontal spacing between stringers'
def get_stringers(L1, x, t_str, h_str, w_str, alpha, stringer_hor_spacing):
    total_length = x  # Total length of wingbox upper surface

    # Generate i-coordinates for stringers (equally spaced)
    i_values = np.arange(0, total_length, stringer_hor_spacing)  # i-positions of stringers

    # Generate j-coordinates for lower surface stringers
    j_values = (L1 - np.tan(alpha) * i_values)  # Linear variation with slope (since j increases with x along the surface)

    # Create dictionaries for upper and lower surface stringers
    # SAME SPACING ASSUMED OVER UPPER AND LOWER SURFACE!!!  
    stringersUS = {
        f"stringer{i+1}": {"i": i_value, "j": t_str/2, "height": h_str, "width": w_str}  
        for i, i_value in enumerate(i_values)
    }

    stringersLS = {
        f"stringer{i+1}": {"i": i_value, "j": j_value, "height": h_str, "width": w_str}
        for i, (i_value, j_value) in enumerate(zip(i_values, j_values))
    }

    # Number of stringers
    num_upper_stringers = len(stringersUS)
    num_lower_stringers = len(stringersLS)

    return stringersUS, stringersLS, num_upper_stringers, num_lower_stringers

# Function to determine the centroid of the wingbox cross-section
'W.r.t to the top left corner of the wingbox'
def centroid(segments, stringersUS, stringersLS):
    # Calculating the weighted sum of the x and y coordinates
    total_x = sum(segment["i"] * segment["length"] * segment["thickness"] for segment in segments.values()) + sum(stringer["i"] * stringer["height"] * stringer["width"] for stringer in stringersUS.values()) + sum(stringer["i"] * stringer["height"] * stringer["width"] for stringer in stringersLS.values())
    total_y = sum(segment["j"] * segment["length"] * segment["thickness"] for segment in segments.values()) + sum(stringer["j"] * stringer["height"] * stringer["width"] for stringer in stringersUS.values()) + sum(stringer["j"] * stringer["height"] * stringer["width"] for stringer in stringersLS.values())
    total_A = sum(segment["length"] * segment["thickness"] for segment in segments.values()) + sum(stringer["height"] * stringer["width"] for stringer in stringersUS.values()) + sum(stringer["height"] * stringer["width"] for stringer in stringersLS.values())

    x_bar = total_x / total_A
    y_bar = total_y / total_A

    return x_bar, y_bar

# Function to calculate the MOI of the wingbox
'About the centroid of the wingbox'
def MOI(segments, stringersUS, stringersLS, x_bar, y_bar, alpha, t_str, h_str, w_str):
    # Initialize moments of inertia (about the centroidal axes)
    I_xx = 0  # Moment of inertia about the x-axis (centroidal)
    I_yy = 0  # Moment of inertia about the y-axis (centroidal)
    I_xy = 0  # Moment of inertia about the xy-axis (product of inertia)
    'I_xy is assumed 0 since the horizontal axis going through the centroid is a principal axis'

    # Calculate distance from wall centroid to section centroid
    'Upper segment'
    for segment in list(segments.values())[:1]:
        dx = segment["i"] - x_bar
        dy = segment["j"] - y_bar

        # Moment of inertia of each segment about its own centroid
        'The higher order contributions of the thickness t are neglected'
        I_xx_segment = 0
        I_yy_segment = (segment["thickness"] * segment["length"]**3) / 12

        # Parallel Axis Theorem contribution
        I_xx += I_xx_segment + segment["length"] * segment["thickness"] * dy**2
        I_yy += I_yy_segment + segment["length"] * segment["thickness"] * dx**2

    'Spars'
    for segment in list(segments.values())[1:4]:
        dx = segment["i"] - x_bar
        dy = segment["j"] - y_bar

        # Moment of inertia of each segment about its own centroid
        'The higher order contributions of the thickness t are neglected'
        I_xx_segment = (segment["thickness"] * segment["length"]**3) / 12
        I_yy_segment = 0

        # Parallel Axis Theorem contribution
        I_xx += I_xx_segment + segment["length"] * segment["thickness"] * dy**2
        I_yy += I_yy_segment + segment["length"] * segment["thickness"] * dx**2

    
    'Lower segment'
    for segment in list(segments.values())[4:]:
        dx = segment["i"] - x_bar
        dy = segment["j"] - y_bar

        # Moment of inertia of each segment about its own centroid
        'The higher order contributions of the thickness t are neglected'
        I_xx_segment = (segment["thickness"] * segment["length"]**3 * (np.sin(alpha))**2) / 12
        I_yy_segment = (segment["thickness"] * segment["length"]**3 * (np.cos(alpha))**2) / 12

        # Parallel Axis Theorem contribution
        I_xx += I_xx_segment + segment["length"] * segment["thickness"] * dy**2
        I_yy += I_yy_segment + segment["length"] * segment["thickness"] * dx**2
        
    'Stringers upper surface'
    for stringer in stringersUS.values():
        dx = stringer["i"] - x_bar
        dy = stringer["j"] - y_bar

        # Moment of inertia of each stringer about its own centroid
        'The higher order contributions of the thickness t are neglected'
        # Calculate centroid of stringer
        x_bar_str = (t_str*h_str + w_str**2) / (2*(h_str + w_str)) 
        y_bar_str = ((h_str**2)/2) / (h_str + w_str)

        I_xx_stringer = (t_str*h_str**3)/12 + t_str*h_str*(h_str/2-y_bar_str)**2 + (w_str * t_str**3)/12 + t_str*w_str*(h_str-y_bar_str)**2
        I_yy_stringer = (h_str*t_str**3)/12 + t_str*h_str*(t_strS/2-x_bar_str)**2 + (t_str*w_str**3)/12 + t_str*w_str*(w_str/2-x_bar_str)**2

        # Parallel Axis Theorem contribution
        I_xx += I_xx_stringer + stringer["height"] * stringer["width"] * dy**2
        I_yy += I_yy_stringer + stringer["height"] * stringer["width"] * dx**2

    for stringer in stringersLS.values():
        dx = stringer["i"] - x_bar
        dy = stringer["j"] - y_bar

        # Moment of inertia of each stringer about its own centroid
        'The higher order contributions of the thickness t are neglected'
        # Calculate centroid of stringer
        x_bar_str = w_str**2 / (2*(h_str + w_str)) 
        y_bar_str = ((h_str**2)/2) / (h_str + w_str)

        I_xx_stringer = (t_str*h_str**3)/12 + t_str*h_str*(h_str/2-y_bar_str) **2 + t_str*w_str*(h_str-y_bar_str)**2
        I_yy_stringer = t_str*h_str*x_bar_str**2 + (t_str*w_str**3)/12 + t_str*w_str*(w_str/2-x_bar_str)**2

        # Parallel Axis Theorem contribution
        I_xx += I_xx_stringer + stringer["height"] * stringer["width"] * dy**2
        I_yy += I_yy_stringer + stringer["height"] * stringer["width"] * dx**2

    return I_xx, I_yy, I_xy

# # Test
# # Call wingbox function
# chord = 0.917  #tip chord
# sparLocs = [0.4]  # Reinforcement Spar locations

# upperCoords, lowerCoords = wingbox(chord, sparLocs=sparLocs, plot=False)
# 'W.r.t to LE, in order FS, RS, middle spars'
# print("Upper Wing Box Coordinates:", upperCoords)
# print("Lower Wing Box Coordinates:", lowerCoords)

# L1 = upperCoords[1][0] - lowerCoords[1][0] # m
# #L2 = upperCoords[1][2] - lowerCoords[1][2] # m
# L2 = 0 #m
# L3 = upperCoords[1][1] - lowerCoords[1][1] # m
# x = upperCoords[0][1] - upperCoords[0][0] # m
# t_f = 0.005 # m 
# t_s = 0.005 # m 
# t_m = 0.005 # m 
# t_str = 0.001 # m
# A_str = 0.0006 # m^2 (assumed)
# print(L1, L2, L3, x)

# segments, alpha = get_segments(L1, L2, L3, x, t_f, t_s, t_m)
# stringersUS, stringersLS, num_upper_stringers, num_lower_stringers = get_stringers(L1, x, t_str, A_str, alpha)
# x_bar, y_bar = centroid(segments, stringersUS, stringersLS)
# I_xx, I_yy, I_xy = MOI(segments, stringersUS, stringersLS, x_bar, y_bar, alpha)
# print(f"CG @ tip = {x_bar, y_bar}")
# print(f"I_xx, I_yy, I_xy @ MAC = {I_xx, I_yy, I_xy}")
# print("Number of Upper Surface Stringers @ MAC:", num_upper_stringers)
# print("Number of Lower Surface Stringers @ MAC:", num_lower_stringers)


