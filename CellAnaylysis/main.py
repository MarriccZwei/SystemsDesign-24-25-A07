if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
    import matplotlib.pyplot
import CellAnaylysis.cellOperations as cop
import OOP.Planform as pf
import numpy as np
import General.Constants as c
import matplotlib.pyplot as plt

'''Planform Parameters from WP3'''
planform =pf.Planform(251.3429147793505, 9.872642920666417, 0.1, 28.503510117080133, 2.1496489882919865, False)
halfspan = planform.b/2
mWing = 22962.839350654576
mEngine = 3554.759960907367/2 #divide by two as we are looking at the half-span only
thrust = 91964.80101516769
wgboxArea = 123.969 #[m^2] measured in CATIA

'''Defining initial design parameters'''
plot = True #do we want to plot

"""VARS"""
t = 0.008
"rib spacing"
#the rib stations required due to the subsystem presence - do not change!
#the 0.6 halfspan does not correspond to subsystem - it is there to model the point when skin buckling changes significance
#you can change 
ribStations = [0, 3.3, 3.9, 5.1, c.ENGINESPANWISEPOS*halfspan, 0.425*halfspan, 17.62, 17.92, 22.42, halfspan]

#change this, the columns left as zeros are there for a reason - the spacing between the enforced spars is just small.
ribBetweenCounts = [5, 0, 2, 4, 5, 8, 0,7, 2] #amount of ribs between the ribs from ribStations

#generating rib positions
ribPoses = [0] #this is intentional to account for the rib at root
for i in range(len(ribBetweenCounts)):
    #+2 accounts for the first and the last rib, then the 1st rib is removed, so indeed you end up with 1 side rib plus the between rib count
    ribPoses+=np.linspace(ribStations[i], ribStations[i+1], ribBetweenCounts[i]+2).tolist()[1:]

midsCoffIdx = sum(ribBetweenCounts[:4])+5-1 #the selected and the enforced ribs up to the engine rib, -1 to account for indexing

"wingboxDesigns"
#design with index 0 is design option 1, etc.
stringerDesign = {'w':0.10, 'h':0.10, 't':0.009, 'sb':0.15, 'st':0.15}

#same indexing as stringerDesign
thicknesses = {'f':t, 'r':t, 'b':t, 't':t}

#mid spar persence and position
midSpar = None

'''Dividing the wing into the cells'''
cells = cop.cell_distr(planform, ribPoses
                        , stringerDesign, thicknesses, midsCoffIdx, midSpar)
margins_of_safety = cop.mofs(cells, plot=True)

#plotting mofs
if plot:
    plt.subplot(232)
    plt.plot(margins_of_safety[0], margins_of_safety[1])
    plt.plot([0, 25], [1, 1])
    plt.title("Tensile strength failure margin of Safety")
    plt.axis([0, 25, 0, 10])

    plt.subplot(233)
    plt.plot(margins_of_safety[0], margins_of_safety[2])
    plt.plot([0, 25], [1, 1])
    plt.title("Compressive strength failure margin of safety")
    plt.axis([0, 25, 0, 10])

    plt.subplot(234)
    plt.plot(margins_of_safety[0], margins_of_safety[3])
    plt.plot([0, 25], [1, 1])
    plt.title("Stringer column buckling margin of safety")
    plt.axis([0, 25, 0, 10])

    plt.subplot(235)
    plt.plot(margins_of_safety[0], margins_of_safety[4])
    plt.plot([0, 25], [1, 1])
    plt.title("Spar shear buckling margin of safety")
    plt.axis([0, 25, 0, 10])

    plt.subplot(236)
    plt.plot(margins_of_safety[0], margins_of_safety[5])
    plt.plot([0, 25], [1, 1])
    plt.title("Skin buckling margin of safety")
    plt.axis([0, 25, 0, 10])

    plt.show()
    print(min(margins_of_safety[4]))

'''TODO Add a code that computes the mass of the design!'''