if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from OOP import Cell
from OOP import FlexBox

# Define constants
#t_skin = 0.02  # Skin thickness in meters (example value)
material_strength_tension = 485e6  # Ultimate tensile strength in Pa (example value)
material_strength_compression = 485e6  # Ultimate compressive strength in Pa (example value)

#TODO: iontegrate this with the calculateStress function
def axialStress(MomentX:float, MOIxx:float, MOIyy:float, MOIxy:float, FrontSparLen:float, CentroidX:float, Chord:float): 
    Y = FrontSparLen/2 #location of maximum axial stress will likely be at the front spar
    X = CentroidX*Chord
    Denominator = MOIxx*MOIyy - MOIxy**2
    MaxStress = MomentX*((MOIyy*Y - MOIxy*X)/(Denominator))

#TODO change the function name
#TODO make the function more felxible (able to take any x and y as inputs)
def tensionCompressionStresses(Moments, Momentlocations, cell:Cell.Cell, z):
    Ixx, centroid = cell.sectionProperties(z)["ixx"], cell.sectionProperties(z)["centroid"] #Ixx and centroid
    Moment_interp = interp1d(Momentlocations, Moments, kind='linear') # Interpolate the bending moment distribution
    moment = Moment_interp(z)
    wingbox = cell.wingbox(z) #FlexBox object
    wingboxcoords = wingbox.coords() #Coordinates of the cornes of the crossection --> dictionary
    
    # Calculate y_upper and y_lower based on the centroid and wingbox coordinates
    y_coords = [coord[1] for coord in wingboxcoords]  # Extract y-coordinates of corners
    y_lower = max(y_coords) - centroid[1]  # Distance from centroid to the top
    y_upper = centroid[1] - min(y_coords)  # Distance from centroid to the bottom

    # Calculate bending stresses
    maxstress = moment * y_upper / Ixx  # Maximum stress at the upper skin
    minstress = moment * y_lower / Ixx  # Minimum stress at the lower skin

    return maxstress,minstress,moment

def plotTCgraph(Moments, Momentlocations):
    listCells=[]
    interval = 0.05#[m]
    minStressList=[]
    maxStressList = []
    momentList=[]
    zList=[]
    safetyListmax=[]
    safetyListmin=[]
    z = 0
    for c in listCells:
        while z<c.endPos:
            zList.append(z)
            x = axialMomentStress(Moments, Momentlocations, c, z)
            minStressList.append(x[1])
            maxStressList.append(x[0])
            momentList.append(x[2])
            safetyListmin.append(x[1]/material_strength_compression)
            safetyListmax.append(x[0]/material_strength_tension)
            z = z+interval

    #Plot the spanwise bending moment distribution
    plt.figure(figsize=(10, 6))
    plt.plot(zList, momentList / 1e6, label='Bending Moment (MN·m)')
    plt.title("Spanwise Bending Moment Distribution")
    plt.xlabel("Spanwise Position (m)")
    plt.ylabel("Bending Moment (MN·m)")
    plt.grid(True)
    plt.legend()
    plt.show()

    # Plot the spanwise stress distribution
    plt.figure(figsize=(10, 6))
    plt.plot(zList, maxStressList / 1e6, label='Upper Skin Stress (MPa)', color='red')
    plt.plot(zList, minStressList / 1e6, label='Lower Skin Stress (MPa)', color='blue')
    plt.title("Spanwise Stress Distribution Due to Bending")
    plt.xlabel("Spanwise Position (m)")
    plt.ylabel("Stress (MPa)")
    plt.axhline(material_strength_tension / 1e6, color='green', linestyle='--', label='Tensile Strength (MPa)')
    plt.axhline(-material_strength_compression / 1e6, color='purple', linestyle='--', label='Compressive Strength (MPa)')
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(zList, safetyListmax, label='Upper Skin Safety Margin', color='red')
    plt.plot(zList, safetyListmin, label='Lower Skin Safety Margin', color='blue')
    plt.title("Spanwise Safety Margin")
    plt.xlabel("Spanwise Position (m)")
    plt.ylabel("[-]]")
    plt.axhline(-1, color='green', linestyle='--', label='')
    plt.axhline(1, color='purple', linestyle='--', label='')
    plt.grid(True)
    plt.legend()
    plt.show()


    # Print some critical points
    print(f"Maximum bending moment: {np.max(momentList) / 1e6:.2f} MN·m")
    print(f"Maximum stress in upper skin: {np.max(maxStressList) / 1e6:.2f} MPa")
    print(f"Maximum stress in lower skin: {np.min(minStressList) / 1e6:.2f} MPa")