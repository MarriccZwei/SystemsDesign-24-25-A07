if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING

from math import pi
from interpolatedLoads import pos_loadcase, neg_loadcase
import OOP.Cell as cell
import OOP.Planform as pf
import matplotlib.pyplot as plt
import scipy.interpolate as si

K_data_unsorted = [[0.7723396840415656,14.839244412502758], #list of coordinates of K graph
[0.7876282837892491,14.3654933267152],
[0.8028517147400543,13.86958484998897],
[0.8176710991502133,13.236300549442973],
[0.8356967883667917,12.747847383079637],
[0.8569157486304141,12.399793872711228],
[0.8803504479879035,11.859779154257666],
[0.9120224832708287,11.284521150452239],
[0.9578318028899183,10.789377320942716],
[1.043220305146518,10.51678058818663],
[1.1516177372876681,10.50472001617766],
[1.2003813756985808,10.068732075887933],
[1.2575735118391056,9.662495863666447],
[1.3231463552581992,9.269762626158174],
[1.4221290685436427,8.89263514320906],
[1.5548561848527465,8.644854688304289],
[1.6297134095337888,8.572873579858813],
[1.7715294007142068,8.579373081200826],
[1.8727252463416426,8.38752309452901],
[1.9706852439747404,8.229859789782338],
[2.07875248754504,8.105535103684096],
[2.1703189917457166,8.042834031914113],
[2.2369301913284065,8.00314189002868],
[2.3702916172604604,7.971026706926981],
[2.4619319794309327,7.933437344887494],
[2.570012256760607,7.8135441369769865],
[2.678235905443415,7.742397189131557],
[2.7699588147565994,7.732873855614386],
[2.8784692061456725,7.759219427899113],
[2.970296385533863,7.785147919883819],
[3.0618003276895362,7.701175752812711],
[3.1782178664331937,7.580013925656299],
[3.261487948332598,7.532466771453786],
[3.3865772816475475,7.523777598536661],
[3.5368478380763286,7.56889178432238],
[3.6369818667732923,7.583211541289806],
[3.711847780627252,7.514184751636153],
[3.836719884619274,7.431637608923454],
[3.9283993480678725,7.407342681447169],
[4.070206650075374,7.410887863997358],
[4.161999072771896,7.42499908081477],
[4.270613734235974,7.486796478601372],
[4.370704317068351,7.486344641609682],
[4.4623316454794475,7.44432380138246],
[4.5707030101018455,7.42340027299802],
[4.654119070106258,7.42548567449813],
[4.787636901150821,7.446548229649244],
[4.8628330035756315,7.489785554084866]]

K_data_x = [] #list where all x-coords are entered
K_data_y = [] #list where all y_coords are entered

for i in range(len(K_data_unsorted)): #sorts both x and y coordinates from unsorted list into corresponding lists
    K_data_x.append(K_data_unsorted[i][0])
    K_data_y.append(K_data_unsorted[i][1])

#interpolation
def interpolateKs():
    f = si.CubicSpline(K_data_x, K_data_y)
    return(f)

#
#plt.plot(K_data_x, K_data_y) #plots the data
#plt.show()

def max_skin_buckling(thickness, length, width, E, v): #function that calculates the skin buckling in a certain section, thickness in mm, length of the plate in mm, width of the plate in mm, v is the poisson ratio, E is the youngs modulus
    a_over_b = length/width #width over length, used to find an approximate K
    if a_over_b > 4.9:
        k = 9.5567
    else:
        k = interpolateKs()(a_over_b)

    critical_stress = (k*pi**2*E)/(12*(1-v**2))*(thickness/width)**2
    return critical_stress

def MOS_skin_buckling(Sigma_applied, thickness, length, width): #margin of safety of skin panel
    E = 72.4e9
    v = 0.33
    Sigma_max = max_skin_buckling(thickness, length, width, E, v)
    S_factor = Sigma_max/Sigma_applied
    return S_factor

'''def maxStress(endPos, startPos):
    n = 5    #increment of distance that you want to use
    dZ = (endPos-startPos)/n
    MxPos = []
    MxNeg = []
    spanwisePos = []
    i = 0
    #for i in range(n):
    #MxPos.append(pos_loadcase(startPos + i * dZ))
    #MxNeg.append(neg_loadcase(startPos + i* dZ))
    spanwisePos.append(i)
    return spanwisePos'''

    

'''def Spanwise_MOS(cell:cell.Cell):
    YMax = cell.wingboxLengths("f")/2
    MOIxx = cell.sectionProperties("ixx")
    MxPos = pos_loadcase(cell.startPos)

    SigmaAppliedPos = MxPos*YMax/MOIxx
'''
'''if __name__ == "__main__": #tests
    planform =pf.Planform(251.3429147793505, 9.872642920666417, 0.1, 28.503510117080133, 2.1496489882919865, False)
    halfspan = planform.b/2
    mWing = 22962.839350654576
    mEngine = 3554.759960907367/2 #divide by two as we are looking at the half-span only
    thrust = 91964.80101516769
    wgboxArea = 123.969 #[m^2] measured in CATIA

    cell1 = cell.Cell(planform, 10, 11, {'w':0.05, 'h':0.05, 't':0.005, 'st':0.1, 'sb':0.13}, {'f':0.006, 'b':0.011, 'r':0.006, 't':0.011})

    print(maxStress(10, 11))
    print(pos_loadcase(1))'''