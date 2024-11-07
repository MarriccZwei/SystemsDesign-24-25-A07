import numpy as np
from General import ISA
from ClassI import thrustLapse
import General.Constants as consts

#betaCruise is the cruise mass fraction
def ClimbRate(W_S, oswald, betaCrusie, rocCruise, CD0, AR):
    beta = betaCrusie
    altitude = consts.CRUISEALTITUDE
    
    c = rocCruise
    rho = ISA.density(altitude)
    C_D0 = CD0
    AR = AR
    e = oswald

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


