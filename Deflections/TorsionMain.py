if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
import matplotlib.pyplot as plt
import Loads.WingSBT as wsbt
from OOP.Planform import Planform
import numpy as np
from Deflections import MoISpanwise as center
from Deflections.Torsion import graphs
import Loads.SBTdiagrams as sbt

thrust = 91964.80101516769
mEngine = 3554.759960907367/2
wing = Planform(251.3429147793505, 9.872642920666417, 0.1, 28.503510117080133, 2.1496489882919865, False)
halfspan = wing.b/2
zAxis = np.linspace(0, wing.b/2)
diagramMaker = sbt.SBTdiagramMaker(plot=False, accuracy=256-1)
distTorque, pointTorques = wsbt.cumulated_torque(wing, thrust, mEngine)
distTorque, pointTorques = wsbt.cumulated_torque(wing, thrust, mEngine)
posesT, loadsT = diagramMaker.torque_diagram(distTorque, pointTorques, halfspan)
xBars = center.x_bar_values
yBars = center.y_bar_values
zPos = center.z_values


number = 2


if number == 1:
    """Design one"""
    thicknesses = [(7,7,7,7)]
    spars = None
    cutoff = None
    Js, thetas = graphs(wing, thicknesses,loadsT, posesT, xBars, yBars, zPos, zAxis, cutoff, spars)

if number == 2:
    """Design two"""
    thicknesses = [(12,6,12,6)]
    spars = None
    cutoff = None
    Js, thetas = graphs(wing, thicknesses,loadsT, posesT, xBars, yBars, zPos, zAxis, cutoff, spars)

if number == 3:
    """Design Three"""
    thicknesses = [(11,4,11,4), (11,4,11,4)]
    spars = [0.4]
    cutoff = 0.3*halfspan
    Js, thetas = graphs(wing, thicknesses,loadsT, posesT, xBars, yBars, zPos, zAxis, cutoff, spars)

plt.figure(figsize=(8, 8))

plt.subplot(2,1, 1)
plt.plot(zAxis, Js)
plt.xlabel("Spanwize location: z [m]")
plt.ylabel("Torsional Stiffness: J [m^4]")
plt.title("Stiffness distribution")
plt.grid(True)

plt.subplot(2,1,2)
plt.plot(zAxis, thetas)
plt.xlabel("Spanwize location: z [m]")
plt.ylabel("Angle of twist: θ [degrees]")
plt.title("Twist distribution")
plt.grid(True)

plt.suptitle(f"Stiffness and twist diagram design {number}")
plt.subplots_adjust(hspace=0.5)



plt.show()
