if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    import matplotlib.pyplot as plt
    # ONLY FOR TESTING

import numpy as np
import General.Constants as consts
import Loads.SBTdiagrams as sbt
import Loads.InertialLoads as il
import Loads.WingSBT as wsbt
import Loads.XFLRimport as xfi
import OOP.Planform as pf
import scipy.interpolate as sip

def pos_loadcase():
    planform =pf.Planform(251.3429147793505, 9.872642920666417, 0.1, 28.503510117080133, 2.1496489882919865, False)
    halfspan = planform.b/2
    mWing = 22962.839350654576
    mEngine = 3554.759960907367/2 #divide by two as we are looking at the half-span only
    thrust = 91964.80101516769
    wgboxArea = 123.969 #[m^2] measured in CATIA

    
    '''The shear diagram'''
    halfspan = planform.b/2
    distrShear, pointShearLoads = wsbt.combined_shear_load(1, planform, mWing, mEngine, wgboxArea)
    diagramMaker = sbt.SBTdiagramMaker(plot=False, accuracy=1000)
    posesV, loadsV =diagramMaker.shear_diagram(distrShear, pointShearLoads, halfspan)

    '''The bending diagram'''
    engineBendingMoment = il.engine_bending(thrust, planform.sweepC4, consts.ENGINESPANWISEPOS*halfspan)
    posesM, loadsM =diagramMaker.bending_diagram(distrShear, pointShearLoads, lambda pos:xfi.MomperSpan(pos)*(-np.sin(planform.sweepC4)), [engineBendingMoment], halfspan)

    '''The torque diagram'''
    distTorque, pointTorques = wsbt.cumulated_torque(planform, thrust, mEngine)
    posesT, loadsT = diagramMaker.torque_diagram(distTorque, pointTorques, halfspan)

    load_dict = {
    "Mx": sip.CubicSpline(posesM,loadsM),  
    "Vy": sip.CubicSpline(posesV,loadsV),     
    "Tz": sip.CubicSpline(posesT,loadsT)   
    }

    return load_dict

def neg_loadcase():
    planform =pf.Planform(251.3429147793505, 9.872642920666417, 0.1, 28.503510117080133, 2.1496489882919865, False)
    halfspan = planform.b/2
    mWing = 22962.839350654576
    mEngine = 3554.759960907367/2 #divide by two as we are looking at the half-span only
    thrust = 91964.80101516769
    wgboxArea = 123.969 #[m^2] measured in CATIA

    diagramMaker = sbt.SBTdiagramMaker(plot=False, accuracy=1000)
    '''The shear diagram for negative n'''
    distrShear, pointShearLoads = wsbt.combined_shear_load_negative(1, planform, mWing, mEngine, wgboxArea)
    posesnV, loadsnV =diagramMaker.shear_diagram(distrShear, pointShearLoads, halfspan)

    '''The bending for negative n'''
    engineBendingMoment = il.engine_bending(thrust, planform.sweepC4, consts.ENGINESPANWISEPOS*halfspan)
    posesnM, loadsnM =diagramMaker.bending_diagram(distrShear, pointShearLoads, lambda pos:xfi.MomperSpanNeg(pos)*(-np.sin(planform.sweepC4)), [engineBendingMoment], halfspan)
    
    '''The torque for negative n'''
    distTorque, pointTorques = wsbt.cumulated_torque_neg(planform, thrust, mEngine)
    posesnT, loadsnT = diagramMaker.torque_diagram(distTorque, pointTorques, halfspan)

    load_dict = {
    "Mx": sip.CubicSpline(posesnM,loadsnM),  
    "Vy": sip.CubicSpline(posesnV,loadsnV),     
    "Tz": sip.CubicSpline(posesnT,loadsnT) 
    }

    return load_dict

if __name__ == "__main__":
    planform =pf.Planform(251.3429147793505, 9.872642920666417, 0.1, 28.503510117080133, 2.1496489882919865, False)
    halfspan = planform.b/2
    mWing = 22962.839350654576
    mEngine = 3554.759960907367/2 #divide by two as we are looking at the half-span only
    thrust = 91964.80101516769
    wgboxArea = 123.969 #[m^2] measured in CATIA

    res = 100
    poses = np.linspace(0, halfspan, res)
    shearMinus = np.zeros(res)
    shearPlus = np.zeros(100)
    bendingMinus = np.zeros(100)
    bendingPlus = np.zeros(100)
    torqueMinus = np.zeros(100)
    torquePlus = np.zeros(100)
    loadsMinus = neg_loadcase()
    loadsPlus = pos_loadcase()
    for i in range(res):
        position = i*halfspan/res
        shearMinus[i] = loadsMinus["Vy"](position)
        shearPlus[i] = loadsPlus["Vy"](position)
        bendingMinus[i] = loadsMinus["Mx"](position)
        bendingPlus[i] = loadsPlus["Mx"](position)
        torqueMinus[i] = loadsMinus["Vy"](position)
        torquePlus[i] = loadsPlus["Vy"](position)

    #plots
    plt.subplot(321)
    plt.plot(poses, shearMinus)
    plt.subplot(322)
    plt.plot(poses, shearPlus)
    plt.subplot(323)
    plt.plot(poses, bendingMinus)
    plt.subplot(324)
    plt.plot(poses, bendingPlus)
    plt.subplot(325)
    plt.plot(poses, torqueMinus)
    plt.subplot(326)
    plt.plot(poses, torquePlus)
    plt.show()