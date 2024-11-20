if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
import numpy as np
from Deflections.wingbox import wingbox

#Function to define the segments of the cross-section
'L_i variables are vertical segments of the wingbox'
'x_i variables are horizontal segments of the wingbox'
'd_i variables are angled segments of the wingbox'
't is the thickness of the segments'

def get_segments_root(L1, L2, L3, L4, x1, x2, x3, t):
    alpha = np.arctan((L1 - L4)  / (x1 + x2 + x3))
    d1 = x1 / np.cos(alpha)
    d2 = x2 / np.cos(alpha)
    d3 = x3 / np.cos(alpha)
    segments = {
         #Express the position of a segment with the wingbox dimensions in variable form
        "x1": {"i": x1/2, "j": t/2, "length": x1, "thickness": t},
        "x2": {"i": x1 + x2/2, "j": t/2, "length": x2, "thickness": t},
        "x3": {"i": x1 + x2 + x3/2, "j": t/2, "length": x3, "thickness": t},
        "L1": {"i": t/2, "j": L1/2, "length": L1, "thickness": t},
        "L2": {"i": x1, "j": L2/2, "length": L2, "thickness": t},
        "L3": {"i": x1 + x2, "j": L3/2, "length": L3, "thickness": t},
        "L4": {"i": x1 + x2 + x3, "j": L4/2, "length": L4, "thickness": t},
        "d1": {"i": x1/2, "j": L1 - (d1/2) * np.sin(alpha), "length": d1, "thickness": t},
        "d2": {"i": x1 + x2/2, "j": L2 - (d2/2) * np.sin(alpha), "length": d2, "thickness": t},
        "d3": {"i": x1 + x2 + x3/2, "j": L3 - (d3/2) * np.sin(alpha), "length": d3, "thickness": t}
    }
    return segments, alpha

#Function to define the sringers of the cross-section
'A is the point area of a stringer'
def get_stringers(L1, L2, L3, L4, x1, x2, x3, t, A):
    stringers ={
        #Express the position of a stringer with the wingbox dimensions in variable form
        #Random fractions(not yet determined)
        "stringer1": {"i": 1/10 * (x1 + x2 + x3), "j": 1/10 * (L1), "area": A}
    }
    return stringers

#Function to determine the centroid of the wingbox cross-section
'W.r.t to the top left corner of the wingbox'
def centroid(segments, stringers):

    #Calculating the weighted sum of the x and y coordinates
    total_x = sum(segment["i"] * segment["length"] * segment["thickness"] for segment in segments.values()) + sum(stringer["i"] * stringer["area"] for stringer in stringers.values())
    total_y = sum(segment["j"] * segment["length"] * segment["thickness"] for segment in segments.values()) + sum(stringer["j"] * stringer["area"] for stringer in stringers.values())
    total_A = sum(segment["length"] * segment["thickness"] for segment in segments.values()) + sum(stringer["area"] for stringer in stringers.values())

    x_bar = total_x / total_A
    y_bar = total_y / total_A

    return x_bar, y_bar

#Function to calculate the MOI of the wingbox
def MOI(segments, stringers, x_bar, y_bar, alpha):
    # Initialize moments of inertia (about the centroidal axes)
    I_xx = 0  # Moment of inertia about the x-axis (centroidal)
    I_yy = 0  # Moment of inertia about the y-axis (centroidal)
    I_xy = 0  # Moment of inertia about the xy-axis (product of inertia)
    'I_xy is assumed 0 since the horizontal axis going through the centroid is a principal axis'

    #Calculate distance from wall centroid to section centroid
    'Horizontal segments'
    for segment in list(segments.values())[:3]:
        dx = segment["i"] - x_bar
        dy = segment["j"] - y_bar

        #Moment of inertia of each segment about its own centroid
        'The higher order contributions of the thickness t are neglected'
        I_xx_segment = 0
        I_yy_segment = (t * segment["length"]**3) / 12

        # Parallel Axis Theorem contribution
        I_xx += I_xx_segment + segment["length"] * segment["thickness"] * dy**2
        I_yy += I_yy_segment + segment["length"] * segment["thickness"] * dx**2

    'Vertical segments'
    for segment in list(segments.values())[3:7]:
        dx = segment["i"] - x_bar
        dy = segment["j"] - y_bar

        #Moment of inertia of each segment about its own centroid
        'The higher order contributions of the thickness t are neglected'
        I_xx_segment = (t * segment["length"]**3) / 12
        I_yy_segment = 0

        # Parallel Axis Theorem contribution
        I_xx += I_xx_segment + segment["length"] * segment["thickness"] * dy**2
        I_yy += I_yy_segment + segment["length"] * segment["thickness"] * dx**2

    
    'Angled segments'
    for segment in list(segments.values())[7:]:
        dx = segment["i"] - x_bar
        dy = segment["j"] - y_bar

        #Moment of inertia of each segment about its own centroid
        'The higher order contributions of the thickness t are neglected'
        I_xx_segment = (t * segment["length"]**3 * (np.sin(alpha))**2) / 12
        I_yy_segment = (t * segment["length"]**3 * (np.cos(alpha))**2) / 12

        # Parallel Axis Theorem contribution
        I_xx += I_xx_segment + segment["length"] * segment["thickness"] * dy**2
        I_yy += I_yy_segment + segment["length"] * segment["thickness"] * dx**2

    return I_xx, I_yy

#Test
L1 = 0.6 #m
L2 = 0.5 #m
L3 = 0.4 #m
L4 = 0.3 #m
x1 = 1 #m
x2 = 2 #m
x3 = 1 #m
t = 0.001 #m
A = 0.01 #m^2
segments, alpha = get_segments_root(L1, L2, L3, L4, x1, x2, x3, t)
stringers = get_stringers(L1, L2, L3, L4, x1, x2, x3, t, A)
x_bar, y_bar = centroid(segments, stringers)
I_xx, I_yy = MOI(segments, stringers, x_bar, y_bar, alpha)
print(f"CG = {x_bar, y_bar}")
print(f"I_xx, I_yy = {I_xx, I_yy}")


