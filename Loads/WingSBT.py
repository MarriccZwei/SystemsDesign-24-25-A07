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

def combined_shear_load_negative(fuelFraction, planform:pf.Planform, mWing, engineMass, wgboxArea):
    #aerodynamics loads imported from xflr
    aerodynamicShear = lambda pos: -xfi.NormalperSpanNeg(pos) #to account for the fact that lift is negative in our coord system

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
        return -CgC4dist*xfi.NormalperSpan(pos)

    torqueDistr = lambda pos:liftShearTorque(pos)+pitchinMomentDistr(pos)
    return torqueDistr, [engineTorque]

def cumulated_torque_neg(planform:pf.Planform, Tengine, mEngine):
    pitchinMomentDistr = lambda pos:-xfi.MomperSpanNeg(pos)*np.cos(planform.sweepC4)
    intXbar = interpolatedI(ms.x_bar_values, planform.b/2)
    CgdistEngStruct = consts.ENGINEXWRTLEMAC+np.tan(planform.sweepLE)*(consts.ENGINESPANWISEPOS-planform.YMAC)+intXbar(consts.ENGINESPANWISEPOS)-consts.NACELLELEN/2
    engineTorque = il.engine_torque(Tengine, planform.sweepC4, consts.ENGINESPANWISEPOS*planform.b/2, mEngine, CgdistEngStruct)

    #torque due to shear offset
    intXbar = interpolatedI(ms.x_bar_values, planform.b/2)
    def liftShearTorque(pos):
        chord = planform.chord_spanwise(pos/planform.b*2)
        CgC4dist = 0.2*chord+intXbar(pos)-0.25*chord
        return -CgC4dist*xfi.NormalperSpanNeg(pos)

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

    
    # '''The shear diagram'''
    # halfspan = planform.b/2
    # distrShear, pointShearLoads = combined_shear_load(1, planform, mWing, mEngine, wgboxArea)
    # diagramMaker = sbt.SBTdiagramMaker(plot=True, accuracy=1000)
    # posesV, loadsV =diagramMaker.shear_diagram(distrShear, pointShearLoads, halfspan)

    # '''The bending diagram'''
    # engineBendingMoment = il.engine_bending(thrust, planform.sweepC4, consts.ENGINESPANWISEPOS*halfspan)
    # posesM, loadsM =diagramMaker.bending_diagram(distrShear, pointShearLoads, lambda pos:xfi.MomperSpan(pos)*(-np.sin(planform.sweepC4)), [engineBendingMoment], halfspan)

    # '''The torque diagram'''
    # distTorque, pointTorques = cumulated_torque(planform, thrust, mEngine)
    # posesT, loadsT = diagramMaker.torque_diagram(distTorque, pointTorques, halfspan)

    # '''The shear diagram for negative n'''
    # distrShear, pointShearLoads = combined_shear_load_negative(1, planform, mWing, mEngine, wgboxArea)
    # posesV, loadsV =diagramMaker.shear_diagram(distrShear, pointShearLoads, halfspan)

    # '''The bending for negative n'''
    # engineBendingMoment = il.engine_bending(thrust, planform.sweepC4, consts.ENGINESPANWISEPOS*halfspan)
    # posesM, loadsM =diagramMaker.bending_diagram(distrShear, pointShearLoads, lambda pos:xfi.MomperSpanNeg(pos)*(-np.sin(planform.sweepC4)), [engineBendingMoment], halfspan)
    
    # '''The torque for negative n'''
    # distTorque, pointTorques = cumulated_torque_neg(planform, thrust, mEngine)
    # posesT, loadsT = diagramMaker.torque_diagram(distTorque, pointTorques, halfspan)


    '''Engine Moment Arm'''
    intXbar = interpolatedI(ms.x_bar_values, planform.b/2)
    print(consts.ENGINEXWRTLEMAC+np.tan(planform.sweepLE)*(consts.ENGINESPANWISEPOS-planform.YMAC)+intXbar(consts.ENGINESPANWISEPOS)-consts.NACELLELEN/2)