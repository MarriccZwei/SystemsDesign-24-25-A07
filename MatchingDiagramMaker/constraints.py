import numpy as np
import acparams

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
def climb_gradient_general(WSaxis, density, nEngines, massFraction, gradient, thrustLapse): #do not append this one directly to constraints!!!
    situationFraction = nEngines*massFraction/thrustLapse/(nEngines-1)
    gradientFraction = gradient*gradient*density/2/WSaxis/massFraction
    innerSqrt = (acparams.CD0*np.pi*acparams.ASPECT*acparams.OSWALD)**0.5
    freeTerm = 4*acparams.CD0/np.pi/acparams.ASPECT/acparams.OSWALD
    return situationFraction*np.sqrt(gradientFraction*innerSqrt+freeTerm)


if __name__ == "__main__":
    pass