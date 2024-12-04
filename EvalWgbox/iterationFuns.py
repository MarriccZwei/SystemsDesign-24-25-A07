'''The single iteration of the design'''
import Loads.WingSBT as wsbt
import Loads.InertialLoads as il
import OOP.Planform as pf
import Loads.SBTdiagrams as sbt
import General.Constants as consts
import Loads.XFLRimport as xfi
import numpy as np
import Deflections.BendingDeflection as bd
import Deflections.Torsion as tr

def calculate_deformations(wgBox, fuelFraction:float, planform:pf.Planform, mWing:float, mEngine:float, wgboxArea:float, thrust:float):
    '''The shear diagram'''
    halfspan = planform.b/2
    distrShear, pointShearLoads = wsbt.combined_shear_load(0.7, planform, mWing, mEngine, wgboxArea)
    diagramMaker = sbt.SBTdiagramMaker(plot=False, accuracy=wgBox.accuracy)
    #posesV, loadsV =diagramMaker.shear_diagram(distrShear, pointShearLoads, halfspan)

    '''The bending diagram'''
    engineBendingMoment = il.engine_bending(thrust, planform.sweepC4, consts.ENGINESPANWISEPOS*halfspan)
    posesM, loadsM =diagramMaker.bending_diagram(distrShear, pointShearLoads, lambda pos:xfi.MomperSpan(pos)*(-np.sin(planform.sweepC4)), [engineBendingMoment], halfspan)

    '''The torque diagram'''
    distTorque, pointTorques = wsbt.cumulated_torque(planform, thrust, mEngine)
    posesT, loadsT = diagramMaker.torque_diagram(distTorque, pointTorques, halfspan)

    '''Bending Deflection'''
    maxBendDefl = bd.integrate_bending_defl(posesM, loadsM, wgBox.Ixx, planform.b)

    '''Twisting'''
    maxTorsionalDefl = tr.twist(planform, wgBox.thicknesses(), halfspan, loadsT, posesT, wgBox.xBars, wgBox.yBars, posesT, wgBox.cutoff)

    return maxBendDefl, maxTorsionalDefl
    

def size_constbox(wgBoxInitial, reqBendDefl, reqTorsionalDefl, dthickness, planform:pf.Planform, mWing:float, mEngine:float, wgboxArea:float, thrust:float):
    wgBox = wgBoxInitial #creating the wingbox that will be altered in the process
    wgBox4givenCutout = list() #list of wing boxes for different spar cutout locations, index+1 means cutout pos
    for i in range(1, 20):
        for j in range(20):
            maxBendDefl, maxTorsionalDefl = calculate_deformations(wgBox, 0, planform, mWing, mEngine, wgboxArea, thrust)
            bendingSatisfied = maxBendDefl<reqBendDefl
            torsionSatisfied = maxTorsionalDefl<reqTorsionalDefl
            if bendingSatisfied and torsionSatisfied:
                wgBox4givenCutout.append(wgBox)
                break
            else:
                '''Increment the flange , midspar and spar thicknesses'''
            if j==19:
                wgBox4givenCutout.append(None) #to mark it has not been calculated
    masses = [box.Volume for box in wgBox4givenCutout] #obtainingWingBox masses
    minmass = min(masses)
    iopt = masses.index(minmass)
    return wgBox4givenCutout[iopt]


#wing box initial should not have middle spars, the same thickness on top and bottom, same thickness of the 2 spars, wgBox initial shouldn't meet the reqs
def size_rectbox(wgBoxInitial, reqBendDefl, reqTorsionalDefl, dthickness, planform:pf.Planform, mWing:float, mEngine:float, wgboxArea:float, thrust:float):
    wgBox = wgBoxInitial #creating the wingbox that will be altered in the process
    for i in range(20):
        maxBendDefl, maxTorsionalDefl = calculate_deformations(wgBox, 0, planform, mWing, mEngine, wgboxArea, thrust)
        bendingSatisfied = maxBendDefl<reqBendDefl
        torsionSatisfied = maxTorsionalDefl<reqTorsionalDefl
        if bendingSatisfied and torsionSatisfied: #when the wingbox meets the requirements
            return wgBox
        if not torsionSatisfied: #when the torsion req is not met
            '''!Re create the wingBox with a spar thickness greater by dthickness!'''
        if not bendingSatisfied: #when the bending req is not met
            '''!Re create the wingBox with a flange thickness greater by dthickness!'''

    raise ValueError("Couldn't size the wingbox for this load!")

def size_complexbox(wgBoxInitial, reqBendDefl, reqTorsionalDefl, dthickness, planform:pf.Planform, mWing:float, mEngine:float, wgboxArea:float, thrust:float):
    wgBox = wgBoxInitial #creating the wingbox that will be altered in the process
    for i in range(20):
        maxBendDefl, maxTorsionalDefl = calculate_deformations(wgBox, 0, planform, mWing, mEngine, wgboxArea, thrust)
        bendingSatisfied = maxBendDefl<reqBendDefl
        torsionSatisfied = maxTorsionalDefl<reqTorsionalDefl
        if bendingSatisfied and torsionSatisfied: #when the wingbox meets the requirements
            return wgBox
        if not torsionSatisfied: #when the torsion req is not met
            '''!Re create the wingBox with a spar thickness greater by dthickness!'''
        if not bendingSatisfied: #when the bending req is not met
            '''!Re create the wingBox with a flange thickness greater by dthickness, we will need to size the thickness between the mid and the side spars!'''

    raise ValueError("Couldn't size the wingbox for this load!")
