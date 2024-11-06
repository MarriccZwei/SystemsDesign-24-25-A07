import json
import os
import numpy as np
import matplotlib.pyplot as plt

import General.Constants as consts
import OOP.Planform as pf
import OOP.HLDs as hld
import OOP.Fuselage as fus

import ClassI.pitchUpConstraint as puc
import ClassI.weightEstimation as wEstI
import ClassI.constraints as constr

import ClassIV.clFunctions as clFuns

import ClassII.weightEst as wEstII
import ClassII.LoadFactor as loadF
import ClassII.dragEst as dragEst

'''obtaining Initial values from main.json'''
with open(os.getcwd()+"/ClassI/output.json") as mainJson:
    jsonDict = json.loads(''.join(mainJson.readlines()))

    oswald = jsonDict["Oswald"]
    Cd0 = jsonDict["Cd0"]
    Mcruise = jsonDict["Mcruise"]
    CLdes = jsonDict["CLDesign"]
    mMTO = jsonDict["MTOM"]
    mOE = jsonDict["OEM"]
    aspect = jsonDict["AR"]
    ClmaxLand = jsonDict["CLmaxLand"]

'''Iteration loop'''
for i in range(1): #later change to a while with a counter and convergence condition

    '''Class I weight est. Based on mass fractions and Cd/AR values from class II'''
    #Class I assesment of the engine tsfc TODO; change tsfc to a constant once we have an engine and manage the 10^6 factor
    tsfc = wEstI.TSFC(consts.BYPASS) #thrust-specific fuel consumption
    eta_engine = wEstI.engineEfficiency(tsfc) #engine efficiency
    
    #Class I aerodynamic calculations TODO - add cdmisc once we have it and change AR to effective AR
    CDcruise = Cd0+CLdes**2/np.pi/aspect/oswald #cruise drag coefficient as given by the current value of aerodynamic parameters
    ld = CLdes/CDcruise #lift over drag ratio
     
    #Class I range and weight calculations
    Requivaleng = wEstI.Req(ld) #equivalent range
    Rauxiliary = wEstI.Raux(ld) #auxiliary range
    Mfuel = wEstI.Mfuel(tsfc, ld) #fuel mass fraction
    MFoe = mOE/mMTO #operating empty weight mass fraction
    mMTO = wEstI.mtom(MFoe, ld, tsfc) #first overwriting of mtom
    Rferry = wEstI.Rferry(MFoe, ld, tsfc) #ferry range
    Rharm = wEstI.Rferry(MFoe, ld, tsfc) #harmonic range


    '''Matching Diagram. Figuring out a design point'''
    constraints, constraintNames = constr.prepare_Constraint_List(aspect, oswald, Cd0, ClmaxLand) #obtaining constraints

    #generating constraints
    WSmax = 10000
    TWmax = 1
    WSres = 1000
    WSaxis = np.linspace(0, WSmax, WSres+1)
    plt.axis((0, WSmax, 0, TWmax))
    i=0
    shading = 0.5 # change as needed 
    for constraint in constraints: 
        plt.plot(*constraint(WSaxis),label=constraintNames[i])
        plt.fill_between(constraint(WSaxis)[0], constraint(WSaxis)[1], 0, alpha=shading)
        i=i+1
    plt.legend()
    plt.show()

    '''Wing Planform Design'''

    '''Aileron design'''

    '''HLD Design'''

    '''Fuselage & fuel Volume Calculations'''

    '''Tail and Cg and lg subloop'''

    '''Class II Drag'''

    '''Class II weight'''

    '''Repeat the Iteration loop until your class I and class II estimations converge'''

'''Final SAR Calculation'''