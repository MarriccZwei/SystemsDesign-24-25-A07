if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
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
"rib spacing"
nRibsBefore = [11, 11, 11] #number of ribs before the engine at at the engine
nRibsAfter = [19, 19, 19] #number of ribs strictly after the engine
midsCoffIdx = list()
ribPoses = list()
#assembling the rib spacing lists
for i in range(3):
    ribPoses.append(np.linspace(0, c.ENGINESPANWISEPOS*halfspan, nRibsBefore[i]).tolist() + np.linspace(c.ENGINESPANWISEPOS*halfspan, halfspan, nRibsAfter[i]+1).tolist()[1:])
    midsCoffIdx.append(nRibsBefore-1) #we always cut the midspar at the engine rib, we substract 1 due to array indices starting from 0
#ribPoses[0] corresponds to design option 1, etc. same for midsCoffIdx

"wingboxDesigns"
#design with index 0 is design option 1, etc.
stringerDesigns = [
    {'w':0.1, 'h':0.1, 't':0.01, 'sb':0.12, 'st':0.17},
    {'w':0.1, 'h':0.1, 't':0.006, 'sb':0.12, 'st':0.17},
    {'w':0.1, 'h':0.1, 't':0.007, 'sb':0.12, 'st':0.17}
]
#same indexing as stringerDesign
thicknesses = [
    {'f':0.007, 'r':0.007, 'b':0.007, 't':0.007},
    {'f':0.006, 'r':0.006, 'b':0.012, 't':0.012},
    {'f':0.004, 'r':0.004, 'b':0.011, 't':0.011, 'm':0.004}
]

'''Dividing the wing into the cells'''
for i in range(3):
    cells = cop.cell_distr(planform, ribPoses, str)
    margins_of_safety = cop.mofs(cells, plot=True)

'''Analyze the results... somehow'''