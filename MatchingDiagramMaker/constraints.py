import numpy as np
import acparams

#here be the list of all constraint functions
constraints = []

#min T/W constraint - used for UAVS which need a large TWR due to their highly suboptimal aerodynamics
def TWconstraint(WSaxis):
    return WSaxis, np.zeros(len(WSaxis))+acparams.TMIN

constraints.append(TWconstraint)

def StallSpeedconstraint(WSaxis): #here we need to start using the adsee book xd, just to demo a v line now
    return np.zeros(len(WSaxis))+acparams.TMIN, WSaxis

constraints.append(StallSpeedconstraint)

if __name__ == "__main__":
    print(TWconstraint(np.linspace(0, 10,11)))