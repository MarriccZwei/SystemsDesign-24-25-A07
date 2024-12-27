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
import TensionCompression as tc
import ColumnBuckling as cb
import interpolatedLoads as ld
import ShearBuckling as sb
import interpolatedLoads as il
import SkinBuckling as sk

def calculateDeltaTwist(loads, cell:cell.Cell, posEnd = 1):
    zStart = cell.startPos
    zEnd = cell.endPos
    length =zEnd-zStart
    def _integrant(z):
        return torsion(cell.wingbox((z-zStart)/length),loads(z)['Tz'])['twist']
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


def mofs(cells:List[cell.Cell], plot=False, yieldSF=1.1, fractureSF=1.5, colBucklSF=1, shearBucklSF=1, skinBucklSF=1):
    '''A function that conducts the analysis of each of the 5 failure modes
    Returns a list of arrays: cell start positions, array of each of the failure modes margins of safety
    0 - positions
    1 - tensile yield strength
    2- compressive yield strength
    3 - column buckling of stringers
    4 - shear buckling of spars
    5 - skin buckling
    Use the safety factors defaults to specify the safety factors (upon which mofs are calculated)]
    There is one plot for the margin of safety both in the positive and negative load factor - the most constraining one is plotted.'''
    ncells = len(cells)
    poses = list()
    tensile = list()
    compressive = list()
    columnB = list()
    shearB = list()
    skinB = list()
    loads_pos = il.pos_loadcase()
    loads_neg = il.neg_loadcase()

    for i in range(ncells):
        #0. cell start position
        poses.append(cells[i].startPos)

        #1 and 2. tensile and compressive stress
        normalStresses = tc.tensionCompressionStresses(cells[i], loads_neg, loads_pos)
        # tensile.append(min(c.YIELD_SIGMA/normalStresses['p+']/yieldSF, c.ULTIMATE_SIGMA/normalStresses['p+']/1)) #1 is for nult nmax correction
        # compressive.append(min(c.YIELD_SIGMA/normalStresses['p-']/yieldSF, c.ULTIMATE_SIGMA/normalStresses['p-']/1))#1 is for nult nmax correction
        tensile.append(c.ULTIMATE_SIGMA/normalStresses['p+'])
        compressive.append(c.ULTIMATE_SIGMA/normalStresses['p-'])

        #3. column buckling of stringers
        if i == ncells-1: #accounting for the boundary conditions
            colBucklCritStress = min(cb.crit_buckling_stress(cells[i], True)) #only works when our stringers are same
        else:
            colBucklCritStress = min(cb.crit_buckling_stress(cells[i], True))
        #since we always have a stringer at maximum stress position, so we will reuse compressiveStress
        columnB.append(colBucklCritStress/normalStresses['p-']/colBucklSF)

        #4. shearBucklSF
        critTau = sb.crit_shear_stress(cells[i])
        appliedTauPos, appliedTauNeg = sb.max_shear_stress(cells[i], loads_neg, loads_pos)
        #the most critical shear stress
        prevmof = 100 #previous margin of safety
        for j in range(len(critTau)): #the len can be 2 or 3, depends on whether you have a midspar or not
            newmof = min(abs(critTau[j])/abs(appliedTauNeg[j]/shearBucklSF), abs(critTau[j])/abs(appliedTauPos[j]/shearBucklSF)) #the more constraining of the two
            if newmof<prevmof: #updating the margin of safety if this one is most constraining
                prevmof = newmof
        shearB.append(prevmof) #now that the most costraining mof for this mode is determined, we can add it

        #5. skinBuckling
        skinB.append(min(sk.MOS_skin_buckling(normalStresses['p-'], cells[i].wingboxThicknesses['b'], cells[i].edges['fb'], cells[i].edges['ob'])/skinBucklSF,
                                 sk.MOS_skin_buckling(normalStresses['n-'], cells[i].wingboxThicknesses['t'], cells[i].edges['ft'],cells[i].edges['ot'])/skinBucklSF))
        
    return (poses, tensile, compressive, columnB, shearB, skinB)



if __name__ == "__main__":
    planform =pf.Planform(251.3429147793505, 9.872642920666417, 0.1, 28.503510117080133, 2.1496489882919865, False)
    halfspan = planform.b/2
    mWing = 22962.839350654576
    mEngine = 3554.759960907367/2 #divide by two as we are looking at the half-span only
    thrust = 91964.80101516769
    wgboxArea = 123.969 #[m^2] measured in CATIA

    ribposes = np.linspace(0, c.ENGINESPANWISEPOS*halfspan, 11).tolist() +np.linspace(c.ENGINESPANWISEPOS*halfspan+1, halfspan, 19).tolist()
    distr = cell_distr(planform, ribposes, {'w':0.05, 'h':0.05, 't':0.005, 'st':0.1, 'sb':0.13}, {'f':0.004, 'b':0.012, 'r':0.004, 't':0.012, 'm':0.004}, 10, 0.4)
    totalTwist = 0
    for celli in distr:
        print(f"cell start: {celli.startPos}, cell end: {celli.endPos}")
        delta = calculateDeltaTwist(ld.pos_loadcase, celli)
        print(f"The deltatwist at cell is {delta}")
        totalTwist += delta
    print(np.rad2deg(totalTwist))
    poses = [celli.startPos for celli in distr]
    ixxs = [celli.sectionProperties(0)["ixx"] for celli in distr]
    plt.plot(poses, ixxs)
    plt.show()
