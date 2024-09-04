def thrustlapse(altitude, mach):
    GAMMA = 1.4
    SLpressure = 101325
    SLtemp = 288.15
    thetaBreak = 1.07 #between 1.06 and 1.08, can be changed

    #TODO: get pressure and temp from ISA via altitude

    totalTemp = temperature*(1+ (GAMMA-1)/2*mach*mach)#total temperature accounting for transsonic effects
    totalPressure = pressure*(1+ (GAMMA-1)/2*mach*mach)**(GAMMA/(GAMMA-1))#total pressure accounting for transsonic effects
    delta = totalPressure/SLpressure#useful constant
    theta = totalTemp/SLtemp#useful constant

    if theta > thetaBreak:
        thrustLapse = 0
    
    return(0)