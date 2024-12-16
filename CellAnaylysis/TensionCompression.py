import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Define constants
#t_skin = 0.02  # Skin thickness in meters (example value)
material_strength_tension = 350e6  # Ultimate tensile strength in Pa (example value)
material_strength_compression = 300e6  # Ultimate compressive strength in Pa (example value)


def calculateStress(Moments, Momentlocations, cell, x):
    Ixx, centroid = cell.calculatesectionProperties() #Ixx and centroid
    Moment_interp = interp1d(Momentlocations, Moments, kind='linear') # Interpolate the bending moment distribution
    moment = Moment_interp(x)
    wingbox = cell.wingbox() #Crossectional area
    wingboxcoords = wingbox.wingboxcoords() #Coordinates of the cornes of the crossection

    # Calculate y_upper and y_lower based on the centroid and wingbox coordinates
    y_coords = [coord[1] for coord in wingboxcoords]  # Extract y-coordinates of corners
    y_lower = max(y_coords) - centroid  # Distance from centroid to the top
    y_upper = centroid - min(y_coords)  # Distance from centroid to the bottom

    # Calculate bending stresses
    maxstress = moment * y_upper / Ixx  # Maximum stress at the upper skin
    minstress = moment * y_lower / Ixx  # Minimum stress at the lower skin

    return maxstress,minstress



# Plot the spanwise bending moment distribution
plt.figure(figsize=(10, 6))
plt.plot(x_fine, M_x / 1e6, label='Bending Moment (MN·m)')
plt.title("Spanwise Bending Moment Distribution")
plt.xlabel("Spanwise Position (m)")
plt.ylabel("Bending Moment (MN·m)")
plt.grid(True)
plt.legend()
plt.show()

# Plot the spanwise stress distribution
plt.figure(figsize=(10, 6))
plt.plot(x_fine, sigma_upper / 1e6, label='Upper Skin Stress (MPa)', color='red')
plt.plot(x_fine, sigma_lower / 1e6, label='Lower Skin Stress (MPa)', color='blue')
plt.title("Spanwise Stress Distribution Due to Bending")
plt.xlabel("Spanwise Position (m)")
plt.ylabel("Stress (MPa)")
plt.axhline(material_strength_tension / 1e6, color='green', linestyle='--', label='Tensile Strength (MPa)')
plt.axhline(-material_strength_compression / 1e6, color='purple', linestyle='--', label='Compressive Strength (MPa)')
plt.grid(True)
plt.legend()
plt.show()

# Print some critical points
print(f"Maximum bending moment: {np.max(M_x) / 1e6:.2f} MN·m")
print(f"Maximum stress in upper skin: {np.max(sigma_upper) / 1e6:.2f} MPa")
print(f"Maximum stress in lower skin: {np.min(sigma_lower) / 1e6:.2f} MPa")
