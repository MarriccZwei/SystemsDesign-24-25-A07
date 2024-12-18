if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
import OOP.Cell as cell
from typing import Iterable, List
import OOP.Planform as pf
import numpy as np
from General import Constants as c
from ShearBuckling import torsion
import matplotlib.pyplot as plt
import scipy.integrate as integrate

def calculateDeltaTwist(loads, cell:cell.Cell, posEnd = 1):
    torques = loads['Tz']
    zStart = cell.startPos
    zEnd = cell.endPos
    length =zEnd-zStart
    def _integrant(z):
        return torsion(cell.wingbox((z-zStart)/length),torques(z))[-1][0]
    theta, error = integrate.quad(_integrant, zStart, cell.spanwisePos(posEnd))
    return theta


def cell_distr(planform, ribposes, stringerDesign, wingBoxThicknesses, cutoffidx, midSpar):
    '''A function that creates a distribution of the cells'''
    cells:List[cell.Cell] = list()
    for i in range(1, len(ribposes)):
        if i > cutoffidx:
            midSpar = None
        cells.append(cell.Cell(planform, ribposes[i-1], ribposes[i], stringerDesign, wingBoxThicknesses, midSpar))
    return cells

def mofs(cells:List[cell.Cell], plot=False):
    '''A function that conducts the analysis of each of the 6 failure modes'''

if __name__ == "__main__":
    planform =pf.Planform(251.3429147793505, 9.872642920666417, 0.1, 28.503510117080133, 2.1496489882919865, False)
    halfspan = planform.b/2
    mWing = 22962.839350654576
    mEngine = 3554.759960907367/2 #divide by two as we are looking at the half-span only
    thrust = 91964.80101516769
    wgboxArea = 123.969 #[m^2] measured in CATIA

    ribposes = np.linspace(0, c.ENGINESPANWISEPOS*halfspan, 11).tolist() +np.linspace(c.ENGINESPANWISEPOS*halfspan+1, halfspan, 19).tolist()
    distr = cell_distr(planform, ribposes, {'w':0.05, 'h':0.05, 't':0.005, 'st':0.1, 'sb':0.13}, {'f':0.004, 'b':0.012, 'r':0.004, 't':0.012, 'm':0.004}, 10, 0.4)
    for celli in distr:
        print(f"cell start: {celli.startPos}, cell end: {celli.endPos}")
    poses = [celli.startPos for celli in distr]
    ixxs = [celli.sectionProperties(0)["ixx"] for celli in distr]
    plt.plot(poses, ixxs)
    plt.show()
