if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING

import Deflections.MoISpanwise as ms
import Loads.WingSBT as wsbt
import Loads.SBTdiagrams as sbt
import OOP.Planform as pf
import numpy as np
import scipy.integrate as itg
from General import Constants as c
import matplotlib.pyplot as plt
import Loads.InertialLoads as il

#wp3 values - to be updated later
planform =pf.Planform(251.3429147793505, 9.872642920666417, 0.1, 28.503510117080133, 2.1496489882919865, False)
halfspan = planform.b/2
mWing = 22962.839350654576
mEngine = 3554.759960907367/2 #divide by two as we are looking at the half-span only
thrust = 91964.80101516769
wgboxArea = 123.969 #[m^2] measured in CATIA

def interpolated_intBendMoment(poses, intBendMoment):
    return lambda pos:np.interp(pos, poses, intBendMoment)

#poses - positions #bending moment
def integrate_bending_defl(poses, intBendMoment, IxxValues, span):
    intBendFun = interpolated_intBendMoment(poses, intBendMoment) #interpolate internal bending moment
    IxxFun = lambda pos:np.interp(pos, np.linspace(0, span/2, len(IxxValues)), IxxValues) #interpolate Ixx
    secondDeriv = lambda pos:-intBendFun(pos)/c.E_MODULUS/IxxFun(pos)
    firstDeriv = lambda pos:itg.quad(secondDeriv, 0, pos)[0]

    return lambda pos:itg.quad(firstDeriv, 0, pos)[0]

if __name__ == "__main__":
    shearFun, shearPts = wsbt.combined_shear_load(0.9, planform, mWing, mEngine, wgboxArea)
    diagramMaker = sbt.SBTdiagramMaker(10)
    engineBendingMoment = il.engine_bending(thrust, planform.sweepC4, c.ENGINESPANWISEPOS*halfspan)
    poses, loads =diagramMaker.bending_diagram(shearFun, shearPts, lambda pos:0, [engineBendingMoment], halfspan)

    deflfun = integrate_bending_defl(poses, loads, ms.I_xx_values, planform.b)
    defls = list()
    for pos in poses:
        defls.append(deflfun(pos))
        print(pos)

    plt.plot(poses, defls)
    plt.show()