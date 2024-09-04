

import numpy as np
import acparams
import ISA
import thrustLapse
def ClimbRate(W_S):
    beta = acparams.BETA_CRUISE
    altitude = acparams.CRUISE_ALTITUDE
    alpha_T = thrustLapse.thrustLapse(altitude, acparams.MACH_CRUISE)
    # c to be moved to acparams
    c = 5.3
    rho = ISA.density(altitude)
    C_D0 = acparams.CD_0
    AR = acparams.ASPECT
    e = acparams.OSWALD


    term1 = beta/alpha_T
    
    term2 = c**2/(beta*W_S)

    term3 = rho/2

    term4 = np.sqrt(C_D0*np.pi*AR*e)

    term5 = 2*np.sqrt(C_D0/(np.pi*AR*e))
    
       # Calculate the thrust-to-weight ratio
    T_W_ratio = term1*(np.sqrt(term2*term3*term4)+term5)
    
    return T_W_ratio





