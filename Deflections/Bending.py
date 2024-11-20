if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
import numpy as np
import matplotlib.pyplot as plt
from Deflections.wingbox import wingbox
from Deflections.MoI import get_segments
from Deflections.MoI import get_stringers
from Deflections.MoI import centroid
from Deflections.MoI import MOI

#Function to calculate the chord at an arbitrary spanwise location z
'z - spanwise location'
'c_r - root chord'
'tr - taper ratio'
'b - wingspan'
def chord(z, c_r, tr, b):
    c = c_r - c_r * (1 - tr) * (z / (b/2))
    return c 

#Function to calculate the moments of inertia for the wingbox
def calculate_moments_of_inertia(chord_length, sparLocs, t, A):
    upperCoords, lowerCoords = wingbox(chord_length, sparLocs=sparLocs, plot=False)
    
    #Calculate segment dimensions based on the coordinates
    L1 = upperCoords[1][0] - lowerCoords[1][0]  # m
    L2 = upperCoords[1][2] - lowerCoords[1][2]  # m
    L3 = upperCoords[1][3] - lowerCoords[1][3]  # m
    L4 = upperCoords[1][1] - lowerCoords[1][1]  # m
    x1 = upperCoords[0][2] - upperCoords[0][0]  # m
    x2 = upperCoords[0][3] - upperCoords[0][2]  # m
    x3 = upperCoords[0][1] - upperCoords[0][3]  # m

    #Calculate the segments and stringers based on the dimensions
    segments, alpha = get_segments(L1, L2, L3, L4, x1, x2, x3, t)
    stringers = get_stringers(L1, L2, L3, L4, x1, x2, x3, t, A)
    
    #Calculate the centroid of the cross-section
    x_bar, y_bar = centroid(segments, stringers)
    
    #Calculate the moments of inertia
    I_xx, I_yy, I_xy = MOI(segments, stringers, x_bar, y_bar, alpha)
    
    return I_xx, I_yy, I_xy

#Set the initial conditions for the wing
c_r = 9.17  # Root chord length (in meters)
tr = 0.1  # Taper ratio
b = 49.81  # Wingspan (in meters)
t = 0.002 #m
A = 0.003 #m^2 
sparLocs = [0.3, 0.4]  # Spar locations (as fractions of the chord)

# Loop through spanwise locations from 0 to b/2 and calculate moments of inertia
num_points = 50  # Number of points along the span to calculate moments of inertia
z_values = np.linspace(0, b / 2, num_points)  # Array of spanwise locations (z)

# Prepare lists to store the moments of inertia
I_xx_values = []
I_yy_values = []
I_xy_values = []

# Loop over each spanwise location
for z in z_values:
    # Calculate chord length at the current spanwise location
    current_chord = chord(z, c_r, tr, b)
    
    # Calculate the moments of inertia for the current spanwise location
    I_xx, I_yy, I_xy = calculate_moments_of_inertia(current_chord, sparLocs, t, A)
    
    # Append the results to the lists
    I_xx_values.append(I_xx)
    I_yy_values.append(I_yy)
    I_xy_values.append(I_xy)
    
    # Optionally, print or plot the results for each z location
    print(f"z = {z:.2f} m: I_xx = {I_xx:.3f}, I_yy = {I_yy:.3f}, I_xy = {I_xy:.3f}")

# After the loop, you can analyze or plot the results
# Example: Plot the moments of inertia along the span
plt.figure(figsize=(10, 6))
plt.plot(z_values, I_xx_values, label="I_xx", color='r')
plt.plot(z_values, I_yy_values, label="I_yy", color='g')
plt.plot(z_values, I_xy_values, label="I_xy", color='b')
plt.xlabel("Spanwise Location (z) [m]")
plt.ylabel("Moments of Inertia")
plt.title("Moments of Inertia along the Wing Span")
plt.legend()
plt.grid(True)
plt.show()