if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
import General.Constants as consts

import General.Constants as consts
from OOP import Planform as pf
import numpy as np
# def wingskin_mass(total_ribs_mass, wing_mass, root_chord, tip_chord, length):
#     wingskin_mass = wing_mass - total_ribs_mass
#     k = (wing_mass - total_ribs_mass)/((tip_chord-root_chord)*(2- length))
#     wingskin_shear_linear = -2*k*(tip_chord-root_chord)/length
#     wingskin_shear_consant = 2*k*(tip_chord-root_chord)/length
#     return  wingskin_shear_linear , wingskin_shear_consant

#we will obtain surface area ratio between the wingboxand ribs, and use it as an estimator
#for mass ratio between spars and ribs 
#wingboxArea = 123.969 #measured from CATIA

#planform is the Wing, mWing is the Class II weight estimate [kg], wingboxArea is the surface area of the wingbox measured in CATIA
#ribsPerb2 is how many ribs are along the span, wingBoxA2c2 is the area coefficient of the airfoil
def wing_weight_distr_est(planform:pf.Planform, mWing:float, wingboxArea:float, ribsPerb2:int=30, wingBoxA2c2:float=.038):
    '''Gives a "Class-II.5 estimate of the wing mass distr, looking at the linear (wgbox) and parabolic (rib)" weighs'''

    #find the area of the ribs
    ribPoses = np.linspace(0, planform.b/2, ribsPerb2)
    ribChords = np.array([planform.chord_spanwise(2*ribPos/planform.b) for ribPos in ribPoses])
    ribAreas = np.square(ribChords)*wingBoxA2c2 #ribAreas
    totalRibArea = np.sum(ribAreas)

    #rib and wgbox area fractions #AF means Area fraction
    totalArea = wingboxArea+totalRibArea
    wgboxAF = wingboxArea/totalArea
    ribsAF = totalRibArea/totalArea

    #masses of wingbox and ribs subgroups
    #estimated using total area
    wgboxMass = wgboxAF*mWing
    ribsMass = ribsAF*mWing
    
    #estimation of mass per ribs as a fraction of rib area taken by a certain rib
    ribMasses = ribAreas/totalRibArea*ribsMass
    #preparing the return value for point loads
    ribPtLoads = [(ribPoses[i], ribMasses[i]*consts.G) for i in range(ribsPerb2)]

    #estimation of wing distributed span function skin
    #proportionality constant between the wgbox area per span and chord length
    dArea2chord = wingboxArea*4/planform.b/(planform.cr+planform.ct)
    dMass2chord = dArea2chord/wingboxArea*wgboxMass #d mass per unit chord
    #preparing the reutrn lambda
    distrWeight = lambda pos:dMass2chord*planform.chord_spanwise(2*pos/planform.b)*consts.G

    #the distr Weight is coming from the wingbox, the point loads are coming from the ribs
    return distrWeight, ribPtLoads

def wingMassParabolic(planform:pf.Planform, mWing):
    #a constant describing dMass/db over chord^2
    dmassc2sb = 1.5*mWing*planform.b/planform.cr/(1-planform.TR)/(1-planform.TR**3)
    return lambda pos:planform.chord_spanwise(2*pos/planform.b)**2*dmassc2sb*consts.G

def fuel_in_wing_weight_est(planform:pf.Planform, wingBoxA2c2:float=.038, safetyFactor=1.5):
    '''returns a weight distribution resulting from the presence of fuel in the wing'''

    return lambda pos:planform.chord_spanwise(2*pos/planform.b)**2*wingBoxA2c2*consts.G*consts.KEROSENEDENSITY/safetyFactor


def engine_zpos(span):
    L = span/2
    engine_zpos = 0.3*L
    return engine_zpos

def engine_xpos_func(root_chord):
    engine_xpos = (1/2)*root_chord
    return engine_xpos  


def engine_shear(engine_mass, engine_zpos):
    return (engine_zpos, engine_mass*9.81)


def engine_torque(engine_thrust, sweep_angle, engine_zpos):
    torque = np.sin(sweep_angle)*engine_thrust*consts.engine_y_offset_from_wing
    return (engine_zpos , torque)

def engine_bending(engine_thrust, sweep_angle, engine_zpos):
    bending_moment = np.cos(sweep_angle)*engine_thrust*consts.engine_y_offset_from_wing
    return (engine_zpos , bending_moment)

if __name__ == "__main__":
    testPlanform = pf.Planform(251.34, 9.7, 0.1, 28.5, 2.15, False)
    mWing = 22963 #kg
    wingboxArea = 123.969 #measured from CATIA
    distrWeight, ptWeights = wing_weight_distr_est(testPlanform, mWing, wingboxArea)
    print(f"rib positions and masses: {ptWeights}")
    wgboxWeight = 0
    for pos in range(24):
        wgboxWeight+= distrWeight(pos)
    print(f"wgbox weight{wgboxWeight}")
    ribweights = 0
    for pt in ptWeights:
        ribweights += pt[1]
    print(f"wing weight summed: {wgboxWeight+ribweights}, vs. initial wing weight: {mWing*consts.G}")
    print(f"Percent difference {1-(wgboxWeight+ribweights)/mWing/consts.G}")