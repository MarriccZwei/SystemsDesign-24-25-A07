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
import Deflections.MoISpanwise as ms

def combined_shear_load(fuelFraction, planform:pf.Planform, mWing, engineMass, wgboxArea):
    #aerodynamics loads imported from xflr
    aerodynamicShear = lambda pos: -xfi.NormalperSpan(pos) #to account for the fact that lift is negative in our coord system

    #wing structure self-weight
    distrWeightShear, ribPtLoads = il.wing_weight_distr_est(planform, mWing, wgboxArea)

    #fuel weight
    fuelWeightshear = il.fuel_in_wing_weight_est(planform, fuelFraction)
    
    #engine weight
    engineWeightShear = il.engine_shear(engineMass, consts.ENGINESPANWISEPOS*planform.b/2)

    #the complete distributed shear load
    def distrShear(pos):
        valWgWeight = distrWeightShear(pos)
        valFuWeight = fuelWeightshear(pos)
        valAeWeight = aerodynamicShear(pos)
        return valWgWeight+valFuWeight+valAeWeight

    #the complete list of point forces
    pointShearLoads = ribPtLoads+[engineWeightShear]

    return distrShear, pointShearLoads

def interpolatedI(I, halfspan):
    return lambda pos:np.interp(pos, np.linspace(0, halfspan, len(I)), I)

def cumulated_torque(planform:pf.Planform, Tengine, mEngine):
    pitchinMomentDistr = lambda pos:-xfi.MomperSpan(pos)*np.cos(planform.sweepC4)
    intXbar = interpolatedI(ms.x_bar_values, planform.b/2)
    CgdistEngStruct = consts.ENGINEXWRTLEMAC+np.tan(planform.sweepLE)*(consts.ENGINESPANWISEPOS-planform.YMAC)+intXbar(consts.ENGINESPANWISEPOS)-consts.NACELLELEN/2
    engineTorque = il.engine_torque(Tengine, planform.sweepC4, consts.ENGINESPANWISEPOS*planform.b/2, mEngine, CgdistEngStruct)

    #torque due to shear offset
    intXbar = interpolatedI(ms.x_bar_values, planform.b/2)
    def liftShearTorque(pos):
        chord = planform.chord_spanwise(pos/planform.b*2)
        CgC4dist = 0.2*chord+intXbar(pos)-0.25*chord
        return -CgC4dist*xfi.LiftperSpan(pos)

    torqueDistr = lambda pos:liftShearTorque(pos)+pitchinMomentDistr(pos)
    return torqueDistr, [engineTorque]

if __name__ == "__main__":
    #wp3 values
    planform =pf.Planform(251.3429147793505, 9.872642920666417, 0.1, 28.503510117080133, 2.1496489882919865, False)
    halfspan = planform.b/2
    mWing = 22962.839350654576
    mEngine = 3554.759960907367/2 #divide by two as we are looking at the half-span only
    thrust = 91964.80101516769
    wgboxArea = 123.969 #[m^2] measured in CATIA

    


