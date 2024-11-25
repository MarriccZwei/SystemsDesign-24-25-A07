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

def combined_shear_load(fuelFraction):
    #aerodynamics loads imported from xflr
    aerodynamicShear = xfi.LiftperSpan

    #copy pasted from wp3 values
    mwing = 22962.839350654576
    planform =pf.Planform(251.3429147793505, 9.872642920666417, 0.1, 28.503510117080133, 2.1496489882919865, False)
    wgboxArea = 123.969 #[m^2] measured in CATIA

    #wing structure self-weight
    distrWeightShear, ribPtLoads = il.wing_weight_distr_est(planform, mwing, wgboxArea)

    #fuel weight
    fuelWeightshear = il.fuel_in_wing_weight_est(planform, fuelFraction)
    
    #engine weight
    engineMass = 3554.759960907367/2 #from wp3, divide by two as we are looking at the half-span only
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

if __name__ == "__main__":
    distrShear, pointShearLoads = combined_shear_load(0.7)
    diagramMaker = sbt.SBTdiagramMaker(plot=True, accuracy=1000)
    poses, loads =diagramMaker.shear_diagram(distrShear, pointShearLoads, 25)
    x = 10.2
    loadx = np.interp(x, poses, loads)
    print(loadx)