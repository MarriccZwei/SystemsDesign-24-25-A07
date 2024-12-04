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

# Function to calculate the chord at an arbitrary spanwise location z
'z - spanwise location'
'c_r - root chord'
'tr - taper ratio'
'b - wingspan'
def chord(z, c_r, tr, b):
    c = c_r - c_r * (1 - tr) * (z / (b/2))
    return c 

# Function to calculate the moments of inertia for the wingbox
def calculate_moments_of_inertia(chord_length, sparLocs, t_f, t_s, t_m, t_str, A_str):
    upperCoords, lowerCoords = wingbox(chord_length, sparLocs, plot=False)
    
    # Calculate segment dimensions based on the wingbox coordinates
    L1 = upperCoords[1][0] - lowerCoords[1][0]  # m
    L2 = upperCoords[1][2] - lowerCoords[1][2]  # m
    L3 = upperCoords[1][1] - lowerCoords[1][1]  # m
    x = upperCoords[0][1] - upperCoords[0][0] # m

    # Calculate the segments and stringers based on the dimensions
    segments, alpha = get_segments(L1, L2, L3, x, t_f, t_s, t_m)
    stringersUS, stringersLS, num_upper_stringers, num_lower_stringers = get_stringers(L1, x, t_str, A_str, alpha)
    
    # Calculate the centroid of the cross-section
    x_bar, y_bar = centroid(segments, stringersUS, stringersLS)
    
    # Calculate the moments of inertia
    I_xx, I_yy, I_xy = MOI(segments, stringersUS, stringersLS, x_bar, y_bar, alpha)
    
    return I_xx, I_yy, I_xy , x_bar, y_bar, num_upper_stringers, num_lower_stringers, L2

# Set the initial conditions for the wing
c_r = 9.17  # Root chord length (in meters)
tr = 0.1  # Taper ratio
b = 49.81  # Wingspan (in meters)
t_f = 0.005 # thickness flanges (in meters) 
t_s = 0.005 # thickness front and back spars (in meters) 
t_m = 0.005 # thickness reinforcement spar(s) (in meters) 
t_str = 0.001 # thickness stringers (in meters)
A_str = 0.0006 # area stringers (in m^2)
sparLocs = [0.4]  # Reinforcement spar location(s) 

# Specify the z value where sparLocs changes to None
z_spar_change = b / 4  # Middle of half wingspan (in meters)


# Loop through spanwise locations from 0 to b/2 and calculate moments of inertia
num_points = 100  # Number of points along the span to calculate moments of inertia
z_values = np.linspace(0, b / 2, num_points)  # Array of spanwise locations (z)

# Prepare lists to store the moments of inertia and centroid coordinates
I_xx_values = []
I_yy_values = []
I_xy_values = []
x_bar_values = []
y_bar_values = []
L2_values = []

# Loop over each spanwise location
for z in z_values:
    # Calculate chord length at the current spanwise location
    current_chord = chord(z, c_r, tr, b)
    
    # Determine the sparLocs for the current z value
    current_sparLocs = None if z >= z_spar_change else sparLocs
    
    # Call wingbox to get coordinates
    upperCoords, lowerCoords = wingbox(current_chord, sparLocs=current_sparLocs, plot=False)
    
    # Calculate segment dimensions based on the wingbox coordinates
    L1 = upperCoords[1][0] - lowerCoords[1][0]  # Always included
    x = upperCoords[0][1] - upperCoords[0][0]  # Always included
    
    # Eliminate L2 if z >= z_spar_change
    if z >= z_spar_change:
        L2 = 0
    else:
        L2 = upperCoords[1][2] - lowerCoords[1][2]  # Include L2 if z < z_spar_change
    
    # Always calculate L3
    L3 = upperCoords[1][1] - lowerCoords[1][1]
    
    # Calculate the segments and stringers based on the dimensions
    segments, alpha = get_segments(L1, L2, L3, x, t_f, t_s, t_m)
    stringersUS, stringersLS, num_upper_stringers, num_lower_stringers = get_stringers(L1, x, t_str, A_str, alpha)
    
    # Calculate the centroid of the cross-section
    x_bar, y_bar = centroid(segments, stringersUS, stringersLS)
    
    # Calculate the moments of inertia
    I_xx, I_yy, I_xy = MOI(segments, stringersUS, stringersLS, x_bar, y_bar, alpha)
    
    # Append the results to the lists
    I_xx_values.append(I_xx)
    I_yy_values.append(I_yy)
    I_xy_values.append(I_xy)
    x_bar_values.append(x_bar)
    y_bar_values.append(y_bar)
    L2_values.append(L2)

    # Print results for each z location
    print(f"z = {z:.2f} m: I_xx = {I_xx:.6f}, I_yy = {I_yy:.6f}, I_xy = {I_xy:.1f}, x centroid = {x_bar:.3f}, y centroid = {y_bar:.3f}, L2 = {L2:.3f}")

# Plot the moments of inertia along the span
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