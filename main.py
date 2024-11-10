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
#from ClassI import refAcData
#from ClassI import pointFinder
#from ClassI import maxFunctionFinder

import ClassIV.clFunctions as clFuns
from ClassIV import cruiseConditions as crCond

import ClassII.weightEst as wEstII
import ClassII.LoadFactor as loadF
import ClassII.dragEst as dragEst

import CG_LG_EMP.CG as cg
import CG_LG_EMP.EMP as emp
import CG_LG_EMP.LG as lg

from MATCHINGDIAGRAM.main import MatchingDiagram

'''obtaining Initial values from main.json'''
with open(os.getcwd()+"\\Protocols\\main.json") as mainJson:
    jsonDict = json.loads(''.join(mainJson.readlines()))

    oswald = jsonDict["Oswald"]
    Cd0 = jsonDict["Cd0"]
    Mcruise = jsonDict["Mcruise"]
    CLdes = jsonDict["CLDesign"]
    mMTO = jsonDict["MTOM"]
    mOE = jsonDict["OEM"]
    aspect = jsonDict["AR"]
    ClmaxLand = jsonDict["CLmaxLand"]
    sweep = jsonDict["sweep"]
    taper = jsonDict["tr"]
    dihedral = jsonDict["dihedral"]
    fusD = jsonDict["Dfus"]
    mEmp = jsonDict["mEmpenage"]
    mLG = jsonDict["mLandingGear"]
    mNacelle = jsonDict["mNacelle"]

'''Iteration loop'''
for i in range(4): #later change to a while with a counter and convergence condition

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
    MFoe = mOE/mMTO #operating empty weight mass fraction
    Mfuel = wEstI.Mfuel(MFoe, ld, tsfc) #fuel mass
    mMTO = wEstI.mtom(MFoe, ld, tsfc) #first overwriting of mtom
    mOE = MFoe*mMTO #updating the OEM
    Rferry = wEstI.Rferry(MFoe, ld, tsfc) #ferry range
    Rharm = wEstI.Rferry(MFoe, ld, tsfc) #harmonic range
    print(f"MTOM:{mMTO}")


    '''Matching Diagram. Figuring out a design point'''
    '''This is the new matching diagram code all it only takes this as argumanets as this should probably be included in the itteration.
    The last argumeent is if the diagram should actual be plot or not.'''
    constraints, constraintNames, point = MatchingDiagram(aspect, consts.BETA_LAND, consts.BETA_CRUISE, ClmaxLand, oswald, Cd0, True) 
    WSselected  = point[0]
    TWselected = point[1]
    #constr.prepare_Constraint_List(aspect, oswald, Cd0, ClmaxLand) #obtaining constraints
    # #generating constraints
    # WSmax = 10000
    # TWmax = 1
    # WSres = 1000
    # WSaxis = np.linspace(0, WSmax, WSres+1)
    # plt.axis((0, WSmax, 0, TWmax))
    # i=0
    # shading = 0.5 # change as needed 
    # for constraint in constraints: 
    #     plt.plot(*constraint(WSaxis),label=constraintNames[i])
    #     plt.fill_between(constraint(WSaxis)[0], constraint(WSaxis)[1], 0, alpha=shading)
    #     i=i+1
    # plt.legend()

    # crossOverEvents = maxFunctionFinder.maxFunctionFinder(constraints)
    # for point in crossOverEvents:
    #     print(point)
    #     print(point[1], point[2], point[0]-100, point[0]+100)
    # #pointFinder.pointFinder(point[1], point[2], point[0]-100, point[0]+100)
    # WSselected, TWselected = pointFinder.pointFinder(constraints, crossOverEvents[-1][2], 0, crossOverEvents[-1][0]-100)

    # loadingPointsList = refAcData.generateLoadingPoints()
    # for i, point in enumerate(loadingPointsList):
    #     plt.plot(point[0], point[1], 'r+')
    #     plt.text(point[0] + 30, point[1] + 0.005, i+1) #Hard coded numbers are offset of labels.
    # plt.xlabel("Wing Loading, [N/m^2]")
    # plt.ylabel("Thrust-Weight Ratio, [-]")
    # plt.show()

    '''Wing Planform Design'''
    S = consts.G*mMTO/WSselected #wing surface
    planform = pf.Planform(S, aspect, taper, sweep, dihedral) #current planform

    #updating the design lift coefficient and re-iterating if necessary
    newCLDes = crCond.clDesign(WSselected, Mfuel, planform)
    print(newCLDes)
    if abs(1-newCLDes/CLdes)>0.01:
        CLdes = newCLDes
        continue

    #choose leading edge sweep based on mach drag divergence
    Mdd = crCond.dragDivergenceMach(planform, WSselected, Mfuel, 0.935)
    print(Mdd)
    while  Mdd< consts.CRUISEMACH:
        Mdd = crCond.dragDivergenceMach(planform, WSselected, Mfuel, 0.935)
        planform.change_sweep(planform.sweepC4+0.1)
        sweep = planform.sweepC4

    #choose taper ratio that matches the aspect ratio and sweep to avoid pitchup constraint
    while taper>0.1 and planform.AR>17.7 * (2 - taper) * np.exp(-0.043 * planform.sweepC4):
        taper -= 0.05
    
    if planform.AR>17.7 * (2 - taper) * np.exp(-0.043 * planform.sweepC4):
        aspect = 17.7 * (2 - taper) * np.exp(-0.043 * planform.sweepC4)
        sweep = planform.sweepC4
        continue #if we cannot satisfy pitchup constraint we enforce another class I estimation with a satisfactory aspect ratio

    planform = pf.Planform(S, aspect, taper, sweep, dihedral) #updating planform

    
    '''HLD Design'''
    hlds = hld.HLDs.autosize(planform, fusD/2) #using the autosize mechanic of the high lift devicesw

    '''Class II weight'''
    mDes = (.95+.7)/2*mMTO #design mass due to fuel burn in flight
    clAlph = clFuns.dCLdAlpha(consts.CRUISEMACH, planform, True) #cL-Alpha of the wing
    nult = loadF.n_ult(planform, clAlph, mMTO) #ultimate load factor for the wing
    mWing = wEstII.wing_mass(planform, mDes, nult, consts.THICKNESSTOCHORD, hlds.Smovable(planform)) #class II weight estimation on the wing
    print(f"mWing: {mWing} mWingFraction: {mWing/mMTO}")

    #fuselage weight est.
    fuselage = fus.Fuselage(consts.DEQUIVALENT, consts.LNC, consts.LFUS-consts.LNC-consts.LTC, consts.LTC)
    mFus = wEstII.fus_mass(planform, fuselage, mDes, nult)
    print(f"mFus: {mFus}, mFus/mMTO: {mFus/mMTO}")

    #empenage - landing gear - cg nested estimation
    xCgPrevious = 0 #will be used to compare the cg between iterations
    for i in range(10): #after 10 empenage lg iterations, we just give up if there is no convergence - TODO throw an error in such a case
        #masses of tail and landing gear from previous iterations
        #cg calc I
        mFe = consts.FXTEQPTMF*mMTO #fixed equipment mass taken from Roskam values
        cgWingGroup = cg.X_wcg(mWing, mNacelle, planform.MAC, consts.ENGINEXWRTLEMAC)
        cgFusGroup = cg.X_fcg(mFus, mEmp, mFe, fuselage.L)

        xLemac = cg.x_lemac(cgFusGroup, planform.MAC, mWing, mNacelle, mFus, mEmp, mFe, consts.OEWCGWRTLEMACPERMAC, 0.4) #TODO the 0.4 MAC uncertain - consult the person responsible for CG
        print(xLemac)
        #possible cg position - OE, Fuel+OE, OE+Payload, FUEL+OE+Payload
        xCgPay = consts.LN+(consts.LFUS-consts.LT-consts.LN)/2 #cg payload at half of the cabin -
        xOe = cg.xcg_oe(xLemac, planform.MAC) #OE
        xF = cg.xcg_oe_f(mOE/mMTO, Mfuel/mMTO, xOe, xLemac+0.4*planform.MAC) #fuel + OE
        xP = cg.xcg_oe_p(mOE/mMTO, consts.MAXPAYLOAD/mMTO, xOe, xCgPay) #the Payload+OE case
        xOePF = cg.xcg_oe_p_f(mOE/mMTO, consts.MAXPAYLOAD/mMTO, Mfuel/mMTO, xOe, xCgPay, xLemac+0.4*planform.MAC) #everything case, again unsure of what the fuel cg is and does it concide with wing cg - TODO

        cgMostConstraining = cg.cg(xOe, xP, xF, xOePF) #the most constraining cg choice
        print(f"The most constraining cg location is: {cgMostConstraining}")

        #tail

        #lg - dimensions
        mainWheelPressure = lg.P_MW(mMTO, consts.NWM)
        lMainStrut = lg.z_t(planform.b, planform.dihedral)
        noseWheelPressure = lg.P_NW(mMTO, consts.NWN)
        lNoseStrut= lg.z_n(planform.b, planform.dihedral)

        #lg-weight estimations
        mLG, mMLG, mNLG = wEstII.lg_mass(mMTO, consts.BETA_LAND, lMainStrut, lNoseStrut, consts.NWM, consts.NWN, consts.NSTRUTS, consts.VSTALL)

        #comparing cgs to see if iteration necessary and saving the cg values before next iteration
        if abs(1-xCgPrevious/cgMostConstraining)<.01:
            break #exits the loop
        
        xCgPrevious=cgMostConstraining #if we did not manage to exit the loop

    print()

    print(f"Design point: {WSselected}, {TWselected}")
    print(f"Wing Surface and ClDes: {S}, {CLdes}")
    print(f"Wing Aspect Ration and Taper Ratiom, Sweep: {planform.AR}, {planform.TR}, {planform.sweepC4}")
    print(f"Mach Drag Divergence: {Mdd}")
    '''Fuselage & fuel Volume Calculations'''

    '''Class II Drag'''
    #At this point your planform and fuselage variables will be your final planform and fuselage
    #Use the functions from Class II Drag estimations to do the drag estimation for Planform and the fuselage for cruise conditions
    #Empenage to be added later, but will be done as two other planforms for the tail and the rudder
    #Thus, it would be extra nice to make a fuction that estimates drag using the Class II drag est for any planform
    #It would be just coupling a few functions from ClassII.dragEst.py into a single function - for typical values, us the slides from lift 7 drag estimations
    #The Planform and Fuselage Classes have built-in wetted Surface Functions/Properties


    '''Repeat the Iteration loop until your class I and class II estimations converge'''

'''Final SAR Calculation'''