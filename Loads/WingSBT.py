if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
import General.Constants as consts
import Loads.SBTdiagrams as sbt
import Loads.InertialLoads as il
import Loads.XFLRimport as xfi
import OOP.Planform as pf
import numpy as np

def combined_shear_load(fuelFraction, planform:pf.Planform, mWing, engineMass, wgboxArea):
    #aerodynamics loads imported from xflr
    aerodynamicShear = xfi.LiftperSpan

    #wing structure self-weight
    distrWeightShear, ribPtLoads = il.wing_weight_distr_est(planform, mWing, wgboxArea)

    #fuel weight
    fuelWeightshear = il.fuel_in_wing_weight_est(planform, fuelFraction)
    
    #engine weight
    engineWeighShear = il.engine_shear(engineMass, consts.ENGINESPANWISEPOS*planform.b/2)

    #the complete distributed shear load
    def distrShear(pos):
        valWgWeight = distrWeightShear(pos)
        valFuWeight = fuelWeightshear(pos)
        valAeWeight = aerodynamicShear(pos)
        return valWgWeight+valFuWeight+valAeWeight

    #the complete list of point forces
    pointShearLoads = ribPtLoads+[engineWeighShear]

    return distrShear, pointShearLoads


def cumulated_torque(planform:pf.Planform, Tengine, mEngine):
    pitchinMomentDistr = lambda pos:-xfi.MomperSpan(pos)
    engineTorque = il.engine_torque(Tengine, planform.sweepC4, consts.ENGINESPANWISEPOS*planform.b/2, mEngine, consts.ENGINEXWRTLEMAC+planform.MAC/4-consts.NACELLELEN/2)

    return pitchinMomentDistr, [engineTorque]

if __name__ == "__main__":
    #wp3 values
    planform =pf.Planform(251.3429147793505, 9.872642920666417, 0.1, 28.503510117080133, 2.1496489882919865, False)
    halfspan = planform.b/2
    mWing = 22962.839350654576
    mEngine = 3554.759960907367/2 #divide by two as we are looking at the half-span only
    thrust = 91964.80101516769
    wgboxArea = 123.969 #[m^2] measured in CATIA

    '''The shear diagram'''
    distrShear, pointShearLoads = combined_shear_load(0.7, planform, mWing, mEngine, wgboxArea)
    diagramMaker = sbt.SBTdiagramMaker(plot=True, accuracy=1000)
    poses, loads =diagramMaker.shear_diagram(distrShear, pointShearLoads, halfspan)
    #interpolate the shear diagram
    x = 10.2
    loadx = np.interp(x, poses, loads)
    print(loadx)

    '''The bending diagram'''
    engineBendingMoment = il.engine_bending(thrust, planform.sweepC4, consts.ENGINESPANWISEPOS*halfspan)
    poses, loads =diagramMaker.bending_diagram(distrShear, pointShearLoads, lambda pos:0, [engineBendingMoment], halfspan)

    '''The torque diagram'''
    distTorque, pointTorques = cumulated_torque(planform, thrust, mEngine)
    poses, loads = diagramMaker.torque_diagram(distTorque, pointTorques, halfspan)
