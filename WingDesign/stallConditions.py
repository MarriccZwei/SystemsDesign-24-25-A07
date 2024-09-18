
def maxCL(airfoil, LEsweep, clmax2d, mach = 0.0):
    tc = ( airfoil/100 - int(airfoil/100) )
    if str(airfoil)[2] == '4':
        sharpness = 19.3 * tc
    elif str(airfoil)[2] == '5':
        sharpness = 21.3 * tc
    x = LEsweep
    
    if sharpness <= 1.5: #line 1.4-
        cl_cl = (-3 * 10**(-8) * x**3) + (8 * 10**(-5) * x*x) + 0.0019 * x + 0.9
    
    elif sharpness <= 1.7: #line 1.6
        cl_cl = (-7 * 10**(-7) * x**3) + (0.0001 * x*x) + 0.0009 * x + 0.9

    elif sharpness <= 1.9: #line 1.8
        cl_cl = (-4 * 10**(-10) * x**3) + (0.00002 * x*x) + 0.0012 * x + 0.9
    
    elif sharpness <= 2.1: #line 2.0
        cl_cl = (-3 * 10**(-6) * x*x) - (0.0004 * x) + 0.9
    
    elif sharpness <= 2.3: #line 2.2
        cl_cl = (-2 * 10**(-7) * x**3) - (6 * 10**(-5) * x*x) + 0.00006 * x + 0.9

    elif sharpness < 2.5: #line 2.4
        cl_cl = (-5 * 10**(-7) * x**3) - (2 * 10**(-5) * x*x) - 0.0017 * x + 0.9002

    elif sharpness >= 2.5: #line 2.5+
        cl_cl = (-2 * 10**(-6) * x**3) + (0.0001 * x*x) - 0.0048 * x + 0.9

    if mach <= 0.2:
        deltaCL = 0
    else:
        deltaCL = sharpness / 24 * 0.82

    maxCLtrue = cl_cl * clmax2d + deltaCL
    print(":3")

def stallAlpha(airfoil):
    
    print(":3")