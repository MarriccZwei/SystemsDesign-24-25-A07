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
for i in range(20): #later change to a while with a counter and convergence condition

    '''Class I weight est. Based on mass fractions and Cd/AR values from class II'''
    #Class I assesment of the engine tsfc TODO; change tsfc to a constant once we have an engine and manage the 10^6 factor
    tsfc = wEstI.TSFC(consts.BYPASS) #thrust-specific fuel consumption
    eta_engine = wEstI.engineEfficiency(tsfc) #engine efficiency
    
    #Class I aerodynamic calculations TODO - add cdmisc once we have it and change AR to effective AR
    CDcruise = Cd0+CLdes**2/np.pi/aspect/oswald #cruise drag coefficient as given by the current value of aerodynamic parameters
    ld = CLdes/CDcruise #lift over drag ratio
     
    #Class I range and weight calculations
    Requivalent = wEstI.Req(ld) #equivalent range
    Rauxiliary = wEstI.Raux(ld) #auxiliary range

    MFfuel = wEstI.MFfuel(ld, tsfc) #fuel mass fraction
    MFoe = mOE/mMTO #operating empty weight mass fraction
    mMTO = wEstI.mtom(MFoe, ld, tsfc) #first overwriting of mtom
    mFe = consts.FXTEQPTMF*mMTO #fixed equipment mass

    Mfuel = wEstI.Mfuel(MFoe, ld, tsfc) #fuel mass
    mOE = MFoe*mMTO #updating the OEM
    Rferry = wEstI.Rferry(MFoe, ld, tsfc) #ferry range
    Rharm = wEstI.Rferry(MFoe, ld, tsfc) #harmonic range
    print(f"MTOM:{mMTO}")


    '''Matching Diagram. Figuring out a design point'''
    '''This is the new matching diagram code all it only takes this as argumanets as this should probably be included in the itteration.
    The last argumeent is if the diagram should actual be plot or not.'''
    constraints, constraintNames, point = MatchingDiagram(aspect, consts.BETA_LAND, consts.BETA_CRUISE, ClmaxLand, oswald, Cd0, False) 
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
    #print(newCLDes)
    if abs(1-newCLDes/CLdes)>0.01:
        CLdes = newCLDes
        continue

    #choose leading edge sweep based on mach drag divergence
    Mdd = crCond.dragDivergenceMach(planform, WSselected, Mfuel, 0.935)
    #print(Mdd)
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
    fuselage = fus.Fuselage(consts.DEQUIVALENT, consts.LNC, consts.LFUS-consts.LNC-consts.LTC, consts.LTC)
    clAlph = clFuns.dCLdAlpha(consts.CRUISEMACH, planform, True) #cL-Alpha of the wing
    hlds = hld.HLDs.autosize(planform, fuselage.D/2) #using the autosize mechanic of the high lift devicesw
    alphaMax = hlds.alphaMax(planform, np.radians(clAlph), consts.TAKEOFFCL, consts.ULTIMATECL) #landing/takeoff maximum aoa to get the scrape angle ! radians to convert from per radian to per degree

    mOEClassI = mOE
    '''Class II weight'''
    #mDes = (.95+.7)/2*mMTO #design mass due to fuel burn in flight Uncomment if needed
    mGross = mMTO #gross weight -add the 5% of fuel for toff
    nult = loadF.n_ult(planform, clAlph, mMTO) #ultimate load factor for the wing
    mWing = wEstII.wing_mass(planform, mGross, nult, consts.THICKNESSTOCHORD, hlds.Smovable(planform)) #class II weight estimation on the wing
    print(f"mWing: {mWing} mWingFraction: {mWing/mMTO}")

    #fuselage weight est.
    mFus = wEstII.fus_mass(planform, fuselage, mGross, nult)
    print(f"mFus: {mFus}, mFus/mMTO: {mFus/mMTO}")

    #empenage - landing gear - cg nested estimation
    xCgPrevious = 0 #will be used to compare the cg between iterations
    for j in range(10): #after 10 empenage lg iterations, we just give up if there is no convergence - TODO throw an error in such a case
        #masses of tail and landing gear from previous iterations
        #cg calc 
        #fixed equipment mass taken from Roskam values
        cgWingGroup = cg.X_wcg(mWing, mNacelle, planform.MAC, consts.ENGINEXWRTLEMAC)
        cgFusGroup = cg.X_fcg(mFus, mEmp, mFe, fuselage.L)

        xLemac = cg.x_lemac(cgFusGroup, planform.MAC, mWing, mNacelle, mFus, mEmp, mFe, consts.OEWCGWRTLEMACPERMAC, consts.OEWCGWRTLEMACPERMAC) #TODO the 0.4 MAC uncertain - consult the person responsible for CG
        print(xLemac)
        xC4MAC = xLemac + planform.MAC/4 #x pos. of C/4 MAC
        #possible cg position - OE, Fuel+OE, OE+Payload, FUEL+OE+Payload
        xCgPay = consts.LN+(consts.LFUS-consts.LT-consts.LN)/2 #cg payload at half of the cabin -
        xOe = cg.xcg_oe(xLemac, planform.MAC) #OE
        xF = cg.xcg_oe_f(mOE/mMTO, Mfuel/mMTO, xOe, xLemac+consts.WNGCGWRTLEMACPERMAC*planform.MAC) #fuel + OE
        xP = cg.xcg_oe_p(mOE/mMTO, consts.MAXPAYLOAD/mMTO, xOe, xCgPay) #the Payload+OE case
        xOePF = cg.xcg_oe_p_f(mOE/mMTO, consts.MAXPAYLOAD/mMTO, Mfuel/mMTO, xOe, xCgPay, xLemac+consts.OEWCGWRTLEMACPERMAC*planform.MAC) #everything case, again unsure of what the fuel cg is and does it concide with wing cg - TODO

        cgMostConstraining = cg.cg(xOe, xP, xF, xOePF) #the most constraining cg choice
        cgLeastConstraining = min(xOe, xP, xF, xOePF) #the forwardmost cg 
        print(f"The most constraining cg location is: {cgMostConstraining}")

        #comparing cgs to see if iteration necessary and saving the cg values before next iteration
        if abs(1-xCgPrevious/cgMostConstraining)<.01:
            break #exits the loop

        xCgPrevious=cgMostConstraining #if we did not manage to exit the loop

        #tail
        Sh, Sv = emp.S_tail(consts.VHTAIL, planform.S, planform.MAC, consts.XH, consts.VVTAIL, planform.b, consts.XV, cgMostConstraining)
        horizontalTail = pf.Planform(Sh, consts.ARHTAIL, consts.TRHTAIL, consts.SWEEPHT, planform.dihedral)
        verticalTail = pf.Planform(Sv, consts.ARVTAIL, consts.TRVTAIL, consts.SWEEPVT, 0, symmetric=False)
        bh, bv = emp.b_tail(consts.ARHTAIL, Sh, consts.ARVTAIL, Sv)
        crh, crv = emp.c_r_tail(Sh, consts.TRHTAIL, bh, Sv, consts.TRVTAIL, bv)
        cth, ctv = emp.c_t_tail(consts.TRHTAIL, crh, consts.TRVTAIL, crv)
        mach, macv = emp.mac_tail(crh, crv, consts.TRHTAIL, consts.TRVTAIL)

        #tail mass est.
        massHtail = wEstII.tail_mass(mGross, nult, horizontalTail, consts.XH-xC4MAC, consts.CTRLSURFAREAFRAC*horizontalTail.S)
        clAlphaVtail = clFuns.dCLdAlpha(consts.CRUISEMACH, verticalTail)
        massVtail = wEstII.rudder_mass(mGross, nult, verticalTail, consts.XV-xC4MAC, consts.TCR)
        print(f"happens, old mEmp: {mEmp}")
        mEmp = massHtail+massVtail #upditing the empenage mass value
        print(f"happens, new mEmp: {mEmp}")

        #lg - dimensions
        mainPoint = lg.P_MW(consts.LT, mMTO, consts.NWM)
        hLG = lg.z_MLG(cgMostConstraining, fuselage.L1+fuselage.L2, alphaMax, consts.AbsorberStroke)
        nosePoint = lg.P_NW(mMTO, consts.NWN, consts.LT)
        P = lg.P_N(consts.LF, mMTO) # total load for nose gear
        P_n = lg.P_n(mMTO, mainPoint, consts.NSTRUTS) 
        xMLG = lg.l_m(alphaMax, cgMostConstraining, hLG+fuselage.D/2) #main landing gear x position
        xNLG = lg.l_n(mMTO, xMLG, P_n, cgMostConstraining) #nose landing gear x position
        z_t = lg.z_t(planform.b, planform.dihedral, hLG) # hieght of wing tip
        z_n = lg.z_n(hLG, planform.b, planform.dihedral, consts.DNACELLE) # height of engine base
        #y_TIPOVER = lg.y_MLG_to(xNLG, xMLG, hLG+(consts.DEQUIVALENT/3) , consts.psi) # tipover constraint lateral
        y_WTIP = lg.y_MLG_tc(planform.b, z_t, consts.phi) #wing tip lateral constraint
        y_ENG = lg.y_MLG_ec(planform.b, z_n, consts.phi) #engine lateral constraint

        #lg-weight estimations
        mLG, mMLG, mNLG = wEstII.lg_mass(mMTO, consts.BETA_LAND, hLG, hLG, consts.NWM, consts.NWN, consts.NSTRUTS, consts.VSTALL)
        #print(f"landing gear mass: {mLG}; landing gear height: {hLG}")
    
    #engine group
    mNacelle = wEstII.nacelle_mass(consts.NACELLELEN, consts.DNACELLE, nult, consts.ENGINEMASS, 2, np.pi*consts.DNACELLE*consts.NACELLELEN)
    wire2enginesLen = 2*(consts.ENGINESPANWISEPOS*planform.b/2+xLemac)
    mEngineCtrl = wEstII.engine_controls_mass(2, wire2enginesLen) #mass of engine controls
    starterMass = wEstII.starter_mass(2, consts.ENGINEMASS) #engine starter mass
    mEngGroup = starterMass+mEngineCtrl+mNacelle

    #fuels system masses
    Vfuel = Mfuel/.95/consts.KEROSENEDENSITY #gross fuel = Mfuel/.95
    massFuelSys = wEstII.fuel_system_mass(Vfuel, consts.FUELTANKSN)

    # #electronics system masses
    areaCtrlSurfaces = consts.CTRLSURFAREAFRAC*(horizontalTail.S+verticalTail.S)+hlds.Smovable(planform)
    estMwingGroup = mWing+mNacelle+Mfuel+massFuelSys #estimated full wing group mass
    Izz = ((mMTO-estMwingGroup)*fuselage.L**2+estMwingGroup*planform.b**2)/12 #assume 2 rods crossing at COM
    print(f"IZZ: {Izz}")
    mFc = wEstII.flight_control_mass(areaCtrlSurfaces, Izz)
    #APU not included
    mInstruments = wEstII.instruments_mass(2, 2, fuselage.L, planform.b)
    mHydraulics = wEstII.hydraulics_mass(fuselage.L,planform.b)
    mElectrical = wEstII.electrical_mass(wire2enginesLen,2)
    mAvionics = wEstII.avionics_mass()
    mElectronics = mAvionics+mElectrical+mHydraulics+mInstruments+mFc

    #mass other subsystems
    mFurnishings = wEstII.furnish_mass(2,consts.MAXPAYLOAD,fuselage.Sw)
    Vfus = np.pi/4*fuselage.D**2*fuselage.L #a very rough estimate of the fuselage volume
    mAirconditioning = wEstII.aircon_mass(consts.NPAX, Vfus)
    mAntiIce = wEstII.anti_ice_mass(mGross)
    mHandling = wEstII.handling_mass(mGross)
    mApu = wEstII.apu_installed_mass(200)
    mOther = mHandling+mAntiIce+mAirconditioning+mFurnishings+mApu+massFuelSys
    #mOther = 0.12*mMTO

    oldOEM = mOE #OEM from class I - for convergence check at the end of the loop
    mOE = mLG+mWing+mEmp+mFus+mOther+mEngGroup+mElectronics #getting the new OEM
    mFe = mOther+mElectronics
    
        

    print()

    print(f"Design point: {WSselected}, {TWselected}")
    print(f"Wing Surface and ClDes: {S}, {CLdes}")
    print(f"Wing Aspect Ration and Taper Ratiom, Sweep: {planform.AR}, {planform.TR}, {planform.sweepC4}")
    print(f"Mach Drag Divergence: {Mdd}")
    print(f"ScrapeAngle {alphaMax}")
    print(f"nult: {nult}, MTOM: {mMTO}")
    print("\n-------------------------------------------------------------")
    print(f"Iter {i}, MTOM: {mMTO}:")
    print(f"Wing Mass: {mWing}kg, MF: {mWing/mMTO}")
    print(f"Fuselage Mass: {mFus}kg, MF: {mFus/mMTO}")
    print(f"Empenage Mass: {mEmp}kg, MF: {mEmp/mMTO}")
    print(f"LG Mass: {mLG}kg, MF: {mLG/mMTO}")
    print(f"Engine Group Mass: {mEngGroup}kg, MF: {mEngGroup/mMTO}")
    print(f"Other Mass: {mOther+mElectronics}kg, MF: {(mOther+mElectronics)/mMTO}")
    print(f"OEM/MTOM: {mOE/mMTO}")
    print(f"H Tail Surface: {horizontalTail.S}, Vert. Tail Surface: {verticalTail.S}")
    print(f"H Tail Span: {bh}, Vert. Tail Span: {bv}")
    print(f"H Tail root chord: {crh}, Vert. Tail root chord: {crv}")
    print(f"H Tail tip chord: {cth}, Vert. Tail tip chord: {ctv}")
    print(f"H Tail mac chord: {mach}, Vert. Tail mac chord: {macv}")
    print(f"CG most aft position {cgMostConstraining}, cg forwardmost {cgLeastConstraining}, oswald: {oswald}, Cd0: {Cd0}, aspect: {planform.AR}")
    print(f"Scrape Angle {alphaMax} deg, span: {planform.b}")
    print(f"Fuselage dimensions: D: {fuselage.D}m, L: {fuselage.L}, L_NC: {fuselage.L1}, L_UNCURVED: {fuselage.L2}, L_TC: {fuselage.L3}")
    print(f"Fuselage Dimensions L_N: {consts.LN}m, L_CABIN: {fuselage.L-consts.LN-consts.LT}m, L_T: {consts.LT}")
    print("-------------------------------------------------------------\n")
    print(f"X pos MLG: {xMLG}")
    print(f"X pos NLG: {xNLG}")
    print(f"h LG: {hLG}")
    print(f"MLG point load: {mainPoint}")
    print(f"NLG point load: {nosePoint}")
    print(f"height of wing tip : {z_t}")
    print(f"height of engine base: {z_n}")
    #print(f"Tipover pos: {y_TIPOVER}")
    print(f"Wing Tip pos: {y_WTIP}")
    print(f"ENG pos: {y_ENG}")



    #re-assigning the MTOM
    #mMTO = (mOE+consts.DESIGNPAYLOAD)/(1-MFfuel)
    '''Fuselage & fuel Volume Calculations'''

    '''Class II Drag'''
    #At this point your planform and fuselage variables will be your final planform and fuselage
    #Use the functions from Class II Drag estimations to do the drag estimation for Planform and the fuselage for cruise conditions
    #Empenage to be added later, but will be done as two other planforms for the tail and the rudder
    #Thus, it would be extra nice to make a fuction that estimates drag using the Class II drag est for any planform
    #It would be just coupling a few functions from ClassII.dragEst.py into a single function - for typical values, us the slides from lift 7 drag estimations
    #The Planform and Fuselage Classes have built-in wetted Surface Functions/Properties

    Cdo = dragEst.Cdo(consts.CRUISEDENSITY, consts.CRUISEMACH, CLdes, consts.THICKNESSTOCHORD, planform, fuselage, hlds, S, xNLG, hLG, ka = 0.935)
    aspectEffective = dragEst.ARe(planform.AR) #effective aspect ratio
    oswald = dragEst.Oswald(aspectEffective) #new oswald efficiency factor
    Cdi = CLdes*CLdes/np.pi/aspectEffective/oswald #induced drag coefficient
    Cdo += dragEst.PlanformCdo(consts.CRUISEDENSITY, consts.CRUISEMACH, consts.THICKNESSTOCHORD, horizontalTail)*horizontalTail.S/planform.S #horizontal tail contribution
    Cdo += dragEst.PlanformCdo(consts.CRUISEDENSITY, consts.CRUISEMACH, consts.THICKNESSTOCHORD, verticalTail)*verticalTail.S/planform.S #horizontal tail contribution
    Cdi += dragEst.TailCdi(planform, CLdes, horizontalTail, consts.XH, cgMostConstraining, xLemac)*horizontalTail.S/planform.S #trim drag
    Cd = Cdo + Cdi #drag coefficient
    D = .5*consts.CRUISEDENSITY*consts.CRUISEVELOCITY**2*Cd*S #the drag force experienced by the aircraft during cruise
    print(f"Cd, cd0, Cdi: {Cd}, {Cdo}, {Cdi}") #zero-lift drag coefficient (includes wave drag coefficient)
    print(f"Drag [N]: {D}")

    Cd0 = Cdo


    if abs((mOE-oldOEM)/mOE)<0.01:
        print(f"OEM: {mOE}, old OEM: {oldOEM}; diff: {(mOE-oldOEM)/mOE}")
        print("~~CONVERGED~~")
        break
    # else:
    print(f"OEM: {mOE}, old OEM: {oldOEM}; diff: {(mOE-oldOEM)/mOE}")

'''Final HLDs, planform 'n stuff'''
print("========================")
print(f"wingS: {planform.S}, span:{planform.b}, Root Chord: {planform.cr}, Tip Chord: {planform.ct}, Quarter chord sweep [deg]: {np.degrees(planform.sweepC4)}")
print(f"xLECRPlanform: {xLemac-planform.YMAC*np.tan(planform.sweepLE)}, Incidence angle:{consts.ALPHAZEROLIFT+np.degrees(CLdes/clAlph)}, Dihedral [deg]: {np.degrees(planform.dihedral)}, Taper Ratio: {planform.TR}, aspect ratio: {planform.AR}")
print()
print(f"TE flap spanwise location: [{hlds.flapStart(planform.b)}, {hlds.flapEnd(planform.b)}], Kruger spanwise loc: [{hlds.krugerStart(planform.b)}, {hlds.krugerEnd(planform.b)}], Aileron spanwise loc [{hlds.aileronStart(planform.b)}, {hlds.aileronEnd(planform.b)}]")
print()
print(f"Fuselage dimensions: D: {fuselage.D}m, L: {fuselage.L}, L_NC: {fuselage.L1}, L_UNCURVED: {fuselage.L2}, L_TC: {fuselage.L3}")
print(f"Fuselage Dimensions L_N: {consts.LN}m, L_CABIN: {fuselage.L-consts.LN-consts.LT}m, L_T: {consts.LT}")
print()
print(f"horizontal Tail: S: {horizontalTail.S}, span:{horizontalTail.b}, Root Chord: {horizontalTail.cr}, Tip Chord: {horizontalTail.ct}, Quarter chord sweep [deg]: {np.degrees(horizontalTail.sweepC4)}, Dihedral [deg]: {np.degrees(horizontalTail.dihedral)}, Taper Ratio: {horizontalTail.TR}, aspect ratio: {horizontalTail.AR}, xPos: {consts.XH}")
print()
print(f"vertical Tail: S: {verticalTail.S}, span:{verticalTail.b}, Root Chord: {verticalTail.cr}, Tip Chord: {verticalTail.ct}, Quarter chord sweep [deg]: {np.degrees(verticalTail.sweepC4)}, Taper Ratio: {verticalTail.TR}, aspect ratio: {verticalTail.AR}, xPos: {consts.XV}")
print("Next to that add: HLD deflections (at toff and landing), hldTypes, airfoils for all 3 planforms, landing gear dimensions")
print(f"design point WS: {WSselected} N/m2, TWR: {TWselected} ")