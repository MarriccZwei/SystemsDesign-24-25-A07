if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    import unittest
    # ONLY FOR TESTING

import numpy as np
import scipy as sp
from scipy import interpolate
import matplotlib.pyplot as plt

from General import ISA
import VnDiagram.graph as Vn
from OOP.Planform import Planform

# Constants
TR = 0.1
Cr = 9.174
Halfspan = 49.81384193430594/2
S = 251.3429147793505

transposed = list(zip(*Vn.runVNdiagram()))
V, mass, loadf, altitude = [list(group) for group in transposed]

def C_Lcalc(S, V, mass, loadf, altitude):
    CL_dlst = []
    CheckMaxlst = []
    qlst = []
    for i in range(len(V)):
        q = 0.5 * ISA.density(altitude[i]) * (V[i])**2
        CL_dt = (loadf [i] * mass [i] *9.80665)/(q*S)
        CheckMax = q * CL_dt
        CL_dlst.append(CL_dt)
        CheckMaxlst.append(CheckMax)
        qlst.append(q)
        i+=1
    CL_d = CL_dlst[CheckMaxlst.index(max(CheckMaxlst))]
    q_d = qlst[CheckMaxlst.index(max(CheckMaxlst))]
    return(CL_d, q_d)

print(C_Lcalc(S, V, mass, loadf, altitude))


# File path
txt_a0 = "Loads\MainWing_a=0.00_v=10.00ms.txt"
txt_a10 = "Loads\MainWing_a=10.00_v=10.00ms.txt"

#FROM TXT FILES
CL_0 = 0.132396
CL_10 = 0.964418
Cm_0 = -0.179106
Cm_10 = -1.13864
Cd_0 = 0.000566
Cd_10 = 0.029426

# --- certain load factor 𝑛, weight 𝑊, freestream velocity 𝑉 and density (dependent on altitude) ρ. The required lift coefficient 
# then follows simply from these values. FILL IN THOSE VALUES HERE!
q = C_Lcalc(S, V, mass, loadf, altitude)[1]
CL_d = C_Lcalc(S, V, mass, loadf, altitude)[0]
Cm_d = -0.5


def filetolist(txt):
    # Load data, skipping the header and footer lines to extract the table
    data = np.genfromtxt(
    txt,
    skip_header=40,  # Skip the first 40 
    max_rows=19,     # max rows
    usecols=(0, 3, 5, 6, 1)  # Columns: y, Cl, Cd, Cm
    )
    ylst = data[:, 0].tolist()
    Cllst = data[:, 1].tolist()
    Cdlst = data[:, 2].tolist()
    Cmlst = data[:, 3].tolist()
    Chord = data[:, 4].tolist()
    return(ylst,Cllst,Cdlst,Cmlst,Chord)


def interpolate(ylst,cnst):
    f = sp.interpolate.interp1d(ylst,cnst,kind='cubic',fill_value="extrapolate")
    return(f)


#Chord calculation
def Cy(y):
    Cy = Cr - Cr * (1-TR) * (y/Halfspan)
    return Cy



# --   chord interpolation .... --
# def chord(ylst,Chord):
#     c = sp.interpolate.interp1d(ylst,Chord,kind='linear',fill_value="extrapolate")
#     return(c)
# print(chord((filetolist(txt_a10)[0]),(filetolist(txt_a10)[4]))(20))

#  --    TEST TO PLOT    --
# step = 0.1
# ytab=[]
# cltab=[]

# for i in range(24):
#     cl = interpolate((filetolist(txt_a10)[0]),(filetolist(txt_a10)[1]))(i)
#     i = i + step

#     ytab.append(i)
#     cltab.append(cl)

# # Plot the sine and cosine lines in a graph
# plt.plot(ytab, cltab)

# plt.title('test')
# plt.xlabel('y')
# plt.ylabel('cl')    

# plt.show()




#C_l * c * q lift per unit span
def LiftperSpan(y):
    Lprime = Cy(y) * LiftCoef(y)[0] * q
    return Lprime

def DragperSpan(y):
    Dprime = Cy(y) * interpolate((filetolist(txt_a10)[0]),(filetolist(txt_a10)[2]))(y) * q
    return Dprime

def MomperSpan(y):
    Mprime = Cy(y)**2 * MomCoef(y) * q
    return Mprime


#Lift coef distribution and Angle of attack degrees
def LiftCoef(y):
    Alpha_d = ((CL_d - CL_0)/(CL_10 - CL_0)) * 10
    CL_dy = interpolate((filetolist(txt_a0)[0]),(filetolist(txt_a0)[1]))(y) + ((CL_d - CL_0)/(CL_10 - CL_0)) * (interpolate((filetolist(txt_a10)[0]),(filetolist(txt_a10)[1]))(y) - interpolate((filetolist(txt_a0)[0]),(filetolist(txt_a0)[1]))(y))
    return CL_dy, Alpha_d

#pitching moment coef distribution and Angle of attack degrees

def MomCoef(y):
    Cm_dy = interpolate((filetolist(txt_a0)[0]),(filetolist(txt_a0)[3]))(y) + ((Cm_d - Cm_0)/(Cm_10 - Cm_0)) * (interpolate((filetolist(txt_a10)[0]),(filetolist(txt_a10)[3]))(y) - interpolate((filetolist(txt_a0)[0]),(filetolist(txt_a0)[3]))(y))
    return Cm_dy


step = 0.05 
ytab=[]
cltab=[]

for i in range(24):
    cl = LiftperSpan(i)
    i = i + step

    ytab.append(i)
    cltab.append(cl)

# Plot
plt.plot(ytab, cltab)

plt.title('Lift over Span')
plt.xlabel('y')
plt.ylabel('cnst')    #  What is cnst???

plt.show()