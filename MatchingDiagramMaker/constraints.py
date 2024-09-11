import numpy as np
import acparams
import thrustLapse
import ISA
import math
import Cd0_Oswald_Flaps
import ClimbRate

#here be the list of all constraint functions
constraints = []
constraintNames = []

#min T/W constraint - used for UAVS which need a large TWR due to their highly suboptimal aerodynamics
'''TestConstraint-Do not uncomment for offcial use'''
'''def TWconstraint(WSaxis):
    return WSaxis, np.zeros(len(WSaxis))+acparams.TMIN

constraints.append(TWconstraint)'''

def StallSpeedconstraint(WSaxis): #here we need to start using the adsee book xd, just to demo a v line now
    return np.zeros(len(WSaxis))+1/acparams.BETA_CRUISE*acparams.VSTALL**2*1.225/2*acparams.CLMAX, WSaxis

constraints.append(StallSpeedconstraint)
constraintNames.append("Minimum speed requirement")

'''TestConstraint-Do not uncomment for offcial use'''
'''def TestLinFunConstraint(WSaxis):
    return WSaxis, np.sqrt(WSaxis)/WSaxis

constraints.append(TestLinFunConstraint)'''

'''Climb gradient calculations'''
def climb_gradient_general(WSaxis, nEngines, nEnginesInoper, massFraction, gradient, flapDefl, lgDefl): #do not append this one directly to constraints!!!
    Cd0, oswald = Cd0_Oswald_Flaps.Cd0_Oswald_flaps(flapDefl, acparams.OSWALD, acparams.CD_0, lgDefl)
    #the expression for T/W is divided into subterms, as it is quite a big one
    #the subterm names are arbitrary
    optCl = (Cd0*np.pi*acparams.ASPECT*oswald)**0.5
    speed = (WSaxis*2/acparams.RHO_LAND/optCl)**0.5
    mach = speed/340
    situationFraction = nEngines*massFraction/(nEngines-nEnginesInoper)/thrustLapse.thrustLapseNP(0, mach)
    freeTerm = 2*(Cd0/np.pi/acparams.ASPECT/oswald)**0.5
    '''print(f"sf: {situationFraction}")
    print(f"ft: {freeTerm}")
    print(f"cd0: {Cd0}")
    print(f"pi: {np.pi}")
    print(f"asp: {acparams.ASPECT}")
    print(f"os: {oswald}")'''
    return WSaxis, np.zeros(len(WSaxis))+situationFraction*(gradient+freeTerm)

constraints.append(lambda WSaxis : climb_gradient_general(WSaxis, 2, 0, 1, 0.032, 30, True))
constraintNames.append("Climb gradient requirement CS 25.119")
constraints.append(lambda WSaxis : climb_gradient_general(WSaxis, 2, 1, 1, 0, 15, True))
constraintNames.append("Climb gradient requirement CS 25.121a")
constraints.append(lambda WSaxis : climb_gradient_general(WSaxis, 2, 1, 1, 0.024, 15, False))
constraintNames.append("Climb gradient requirement CS 25.121b")
constraints.append(lambda WSaxis : climb_gradient_general(WSaxis, 2, 1, 1, 0.012, 0, False))
constraintNames.append("Climb gradient requirement CS 25.121c")
constraints.append(lambda WSaxis : climb_gradient_general(WSaxis, 2, 0, 0.92, 0.021, 30, True))
constraintNames.append("Climb gradient requirement CS 25.121d")

def TakeOffFieldLength(WSaxis):
    return WSaxis, np.zeros(len(WSaxis))+(1.15*thrustLapse.thrustLapse(0, 0)*np.sqrt(WSaxis/(acparams.TAKEOFF_LENGTH*acparams.K_T*acparams.RHO_LAND*acparams.g*np.pi*acparams.ASPECT*acparams.OSWALD)) + 44/acparams.TAKEOFF_LENGTH)

constraints.append(TakeOffFieldLength)
constraintNames.append("Take-off distance requirement")

def LandingFieldLengthConstraint(WSaxis):
    return np.zeros(len(WSaxis))+((acparams.LAND_LENGTH*acparams.RHO_LAND*acparams.CLMAX_LAND)/(acparams.BETA_LAND*acparams.CLFL*2)), WSaxis

constraints.append(LandingFieldLengthConstraint)
constraintNames.append("Landing distance requirement")

def CruiseSpeedConstraint(WSaxis):
    crmf = acparams.BETA_CRUISE
    cr_density = ISA.density(acparams.CRUISE_ALTITUDE)
    Vcr = math.sqrt(287*1.4*ISA.temperature(acparams.CRUISE_ALTITUDE))*acparams.MACH_CRUISE
    return WSaxis, (crmf/thrustLapse.thrustLapse(acparams.CRUISE_ALTITUDE,acparams.MACH_CRUISE))*( (acparams.CD_0*0.5*cr_density*Vcr*Vcr)/(acparams.BETA_CRUISE*WSaxis) + (acparams.BETA_CRUISE*WSaxis)/(math.pi*acparams.ASPECT*0.5*acparams.OSWALD*cr_density*Vcr*Vcr) )

constraints.append(CruiseSpeedConstraint)
constraintNames.append("Cruise speed requirement")

constraints.append(ClimbRate.ClimbRate)
constraintNames.append("Rate of climb requirement")

if __name__ == "__main__":
    print(climb_gradient_general(np.linspace(0, 10000, 100), 2, 0, 1, 0.032, 3, True))