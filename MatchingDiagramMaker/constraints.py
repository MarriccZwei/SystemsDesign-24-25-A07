import numpy as np
import acparams
import thrustLapse
import ISA
import math

#here be the list of all constraint functions
constraints = []

#min T/W constraint - used for UAVS which need a large TWR due to their highly suboptimal aerodynamics
'''TestConstraint-Do not uncomment for offcial use'''
'''def TWconstraint(WSaxis):
    return WSaxis, np.zeros(len(WSaxis))+acparams.TMIN

constraints.append(TWconstraint)'''

def StallSpeedconstraint(WSaxis): #here we need to start using the adsee book xd, just to demo a v line now
    return np.zeros(len(WSaxis))+acparams.VSTALL**2*1.225/2*acparams.CLMAX, WSaxis

constraints.append(StallSpeedconstraint)

'''TestConstraint-Do not uncomment for offcial use'''
'''def TestLinFunConstraint(WSaxis):
    return WSaxis, np.sqrt(WSaxis)/WSaxis

constraints.append(TestLinFunConstraint)'''

'''Climb gradient calculations'''
def climb_gradient_general(WSaxis, density, nEngines, nEnginesInoper, massFraction, gradient, thrustLapse): #do not append this one directly to constraints!!!
    #the expression for T/W is divided into subterms, as it is quite a big one
    #the subterm names are arbitrary
    situationFraction = nEngines*massFraction/thrustLapse/(nEngines-nEnginesInoper)
    gradientFraction = gradient*gradient*density/2/WSaxis/massFraction
    innerSqrt = (acparams.CD_0*np.pi*acparams.ASPECT*acparams.OSWALD)**0.5
    freeTerm = 4*acparams.CD_0/np.pi/acparams.ASPECT/acparams.OSWALD
    return situationFraction*np.sqrt(gradientFraction*innerSqrt+freeTerm)

def TakeOffFieldLength(WSaxis):
    return np.zeros(len(WSaxis)) + (1.15*thrustLapse*np.sqrt(WSaxis/(acparams.TAKEOFF_LENGTH*acparams.K_T*acparams.RHO_LAND*acparams.g*np.pi*acparams.ASPECT*acparams.OSWALD)) + 44/acparams.TAKEOFF_LENGTH)

def LandingFieldLengthConstraint(WSaxis):
    return np.zeros(len(WSaxis)) + ((acparams.LAND_LENGTH*acparams.RHO_LAND*acparams.CLMAX_LAND)/(acparams.BETA_LAND*acparams.CLFL*2))

def CruiseSpeedConstraint(WSaxis):
    crmf = acparams.BETA_CRUISE
    cr_density = ISA.density(acparams.CRUISE_ALTITUDE)
    Vcr = math.sqrt(287*1.4*ISA.temperature(acparams.CRUISE_ALTITUDE))*acparams.MACH_CRUISE
    return WSaxis, (crmf/thrustLapse.thrustLapse(0,0))*( (acparams.CD_0*0.5*cr_density*Vcr*Vcr)/(acparams.BETA_CRUISE*WSaxis) + (acparams.BETA_CRUISE*WSaxis)/(math.pi()*acparams.ASPECT*0.5*acparams.OSWALD*cr_density*Vcr*Vcr) )

if __name__ == "__main__":
    print(climb_gradient_general(np.linspace(0, 40000, 100), 1.225, 2, 1, 0.9, 0.03, 0.5))