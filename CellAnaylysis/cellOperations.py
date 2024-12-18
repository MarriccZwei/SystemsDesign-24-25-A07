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
import matplotlib.pyplot as plt
import TensionCompression as tc
import ColumnBuckling as cb
import ShearBuckling as sb

def cell_distr(planform, ribposes, stringerDesign, wingBoxThicknesses, cutoffidx, midSpar):
    '''A function that creates a distribution of the cells'''
    cells:List[cell.Cell] = list()
    for i in range(1, len(ribposes)):
        if i > cutoffidx:
            midSpar = None
        cells.append(cell.Cell(planform, ribposes[i-1], ribposes[i], stringerDesign, wingBoxThicknesses, midSpar))
    return cells


def mofs(cells:List[cell.Cell], plot=False, yieldSF=1.1, fractureSF=1.5, colBucklSF=1, shearBucklSF=1, skinBucklSF=1):
    '''A function that conducts the analysis of each of the 5 failure modes
    Returns a list of arrays: cell start positions, array of each of the failure modes margins of safety
    0 - positions
    1 - tensile yield strength
    2- compressive yield strength
    3 - column buckling of stringers
    4 - shear buckling of spars
    5 - skin buckling
    Use the safety factors defaults to specify the safety factors (upon which mofs are calculated)]'''
    ncells = len(cells)
    returnedList = [np.zeros(ncells)]*6

    for i in range(ncells):
        #0. cell start position
        returnedList[0][i] = cells[i].startPos

        #1 and 2. tensile and compressive stress
        tensileStress, compressiveStress, bendingMoment = tc.tensionCompressionStresses()
        returnedList[1][i] = min(c.YIELD_SIGMA/tensileStress/yieldSF, c.ULTIMATE_SIGMA/tensileStress/fractureSF)
        returnedList[2][i] = min(c.YIELD_SIGMA/compressiveStress/yieldSF, c.ULTIMATE_SIGMA/tensileStress/fractureSF)

        #3. column buckling of stringers
        if i == ncells-1: #accounting for the boundary conditions
            colBucklCritStress = cb.crit_buckling_stress(cells[i], True)
        else:
            colBucklCritStress = cb.crit_buckling_stress(cells[i], True)
        #since we always have a stringer at maximum stress position, so we will reuse compressiveStress
        returnedList[3][i] = colBucklCritStress/compressiveStress/colBucklSF

        #4. shearBucklSF
        critTau = sb.crit_shear_stress(cells[i])
        


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
