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
import OOP.Wingbox as wb
import Loads.XFLRimport as xfi

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
    # print(f"I_xx fun of {4}, {IxxFun(4)}")
    # print(f"M fun of {4}, {intBendFun(4)}")

    return lambda pos:itg.quad(firstDeriv, 0, pos)[0]

if __name__ == "__main__":
    shearFun, shearPts = wsbt.combined_shear_load(1, planform, mWing, mEngine, wgboxArea)
    diagramMaker = sbt.SBTdiagramMaker(256)
    engineBendingMoment = il.engine_bending(thrust, planform.sweepC4, c.ENGINESPANWISEPOS*halfspan)
    poses, loads =diagramMaker.bending_diagram(shearFun, shearPts, lambda pos:xfi.MomperSpan(pos)*(-np.sin(planform.sweepC4)), [engineBendingMoment], halfspan)
    engineBendingMoment = il.engine_bending(thrust, planform.sweepC4, c.ENGINESPANWISEPOS*halfspan)
    poses, loads =diagramMaker.bending_diagram(shearFun, shearPts, lambda pos:xfi.MomperSpan(pos)*(-np.sin(planform.sweepC4)), [engineBendingMoment], halfspan)

    '''Constant thickness, big stiffeners wingbox'''
    wingbox1 = wb.Wingbox(0.007, 0.007, 0, 0.002, planform)
    ixx1, ibars1, ybars1 = wingbox1.section_properties()

    '''Fat Flange, small stiffeners'''
    wingbox2 = wb.Wingbox(0.012, 0.006, 0, 0.001, planform)
    ixx2, ibars2, ybars2 = wingbox2.section_properties()

    '''Reinforcement Spar'''
    wingbox3 = wb.Wingbox(0.011, 0.004, 0.004, 0.0011, planform)
    ixx3, ibars3, ybars3 = wingbox3.section_properties()

    deflfun = integrate_bending_defl(poses, loads, ixx2, planform.b)
    print(f"deflection at {halfspan}: {deflfun(halfspan)}")
    # defls = list()
    # for pos in poses:
    #     defls.append(deflfun(pos))
    #     print(pos)

    # plt.plot(poses, defls)
    # plt.show()