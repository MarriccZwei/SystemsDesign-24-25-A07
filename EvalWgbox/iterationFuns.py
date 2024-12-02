'''The single iteration of the design'''
import Loads.WingSBT as wsbt
import Loads.InertialLoads as il
import OOP.Planform as pf
import Loads.SBTdiagrams as sbt
import General.Constants as consts
import Loads.XFLRimport as xfi
import numpy as np

def calculate_deformations(fuelFraction:float, planform:pf.Planform, mWing:float, mEngine:float, wgboxArea:float, thrust:float):
    '''The shear diagram'''
    halfspan = planform.b/2
    distrShear, pointShearLoads = wsbt.combined_shear_load(0.7, planform, mWing, mEngine, wgboxArea)
    diagramMaker = sbt.SBTdiagramMaker(plot=False, accuracy=1000)
    poses, loads =diagramMaker.shear_diagram(distrShear, pointShearLoads, halfspan)

    '''The bending diagram'''
    engineBendingMoment = il.engine_bending(thrust, planform.sweepC4, consts.ENGINESPANWISEPOS*halfspan)
    poses, loads =diagramMaker.bending_diagram(distrShear, pointShearLoads, lambda pos:xfi.MomperSpan(pos)*(-np.sin(planform.sweepC4)), [engineBendingMoment], halfspan)

    '''The torque diagram'''
    distTorque, pointTorques = wsbt.cumulated_torque(planform, thrust, mEngine)
    poses, loads = diagramMaker.torque_diagram(distTorque, pointTorques, halfspan)

    '''Moment of Inertia'''
    

    