
import numpy as np
import ISA
import thrustLapse

def ClimbRate(W_S):
    beta = acparams.BETA_CRUISE
    altitude = acparams.CRUISE_ALTITUDE
    
    c = acparams.ROC_CRUISE_ALT
    rho = ISA.density(altitude)
    C_D0 = acparams.CD_0
    AR = acparams.ASPECT
    e = acparams.OSWALD

    CLopt = (3*np.pi*AR*e*C_D0)
    mach = np.sqrt((W_S*2/rho/CLopt)/(1.4*287*ISA.temperature(altitude)))

    alpha_T = thrustLapse.thrustLapseNP(altitude, mach)

    term1 = beta/alpha_T
    
    term2 = c**2/(beta*W_S)

    term3 = rho/2

    term4 = np.sqrt(C_D0*np.pi*AR*e)

    term5 = 4*C_D0/(np.pi*AR*e)
    
    # Calculate the thrust-to-weight ratio
    rootedTerm = (term2*term3*term4)+term5
    print(f"sqrt part {np.sqrt((term2*term3*term4)+term5)}")
    print(f"term5 {term5}")
    T_W_ratio = term1*np.sqrt((term2*term3*term4)+term5)
    
    
    return W_S, T_W_ratio


