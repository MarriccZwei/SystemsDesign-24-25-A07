if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
import numpy as np
import scipy as sp
from scipy import interpolate
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from OOP import Cell
from OOP.FlexBox import FlexBox
from General import Constants as c


from interpolatedLoads import pos_loadcase, neg_loadcase


Ks_data_unsorted = [[1.0091484479320676, 15.032487640377036],
[1.016997390249054, 14.557738502239232],
[1.0513018325535106, 14.056354868850171],
[1.0989414220099736, 13.5009504648507],
[1.1596297661963866, 13.000068018200238],
[1.2265560953257175, 12.6349892781837],
[1.3133777480247875, 12.229582905236327],
[1.426547503553056, 11.838245560022482],
[1.552873410969546, 11.460726649172862],
[1.6924986664852848, 11.042754808707762],
[1.8783315493472044, 10.61209220404028],
[2.0506860888460894, 10.28972173396292],
[2.275593637792344, 10.04976068333232],
[2.579652892384468, 9.811303192917515],
[2.863423033826525, 9.762419586377744],
[3.008606092282798, 9.738040431450184],
[3.1538607488445862, 9.68652559453277],
[3.3914590619932206, 9.63676491120045],
[3.7610484826571495, 9.562374479571272],
[4.077726903346138, 9.541253038444603],
[4.33496994669521, 9.546139609145943],
[4.677960671160641, 9.552655036747728],
[4.935203714509714, 9.557541607449068]
]

Ks_data_x = [] #x coord ks
Ks_data_y = [] #y coord ks
for i in range(len(Ks_data_unsorted)): #sorting
    Ks_data_x.append(Ks_data_unsorted[i][0])
    Ks_data_y.append(Ks_data_unsorted[i][1])


# plt.plot(Ks_data_x, Ks_data_y) #plots the data
# plt.show()

#cnsts
v = c.POISSON_RATIO
E = c.E_MODULUS

#LOADS pos and neg case
load_pos = pos_loadcase()
load_neg = neg_loadcase()


#interpolation
def interpolate():
    f = sp.interpolate.interp1d(Ks_data_x,Ks_data_y,kind='cubic',fill_value="interpolate")
    return(f)


def crit_shear_stress(cell:Cell.Cell):
    tau_crit = []
    webs = ['f', 'r', 'm']
    if cell.midSpar == None:
        webs = webs[:-1]
    for i in webs:
        t = cell.wingboxThicknesses[i] #thickness of the web [m]
        b = cell.edges[i+"i"]
        #k_s determination
        a_over_b = cell.edges[i+'t']/b
        k_s = interpolate()(a_over_b)
        if a_over_b > 4.9:
            k_s = 9.5567
        tau_crit_case = ((np.pi**2*k_s*E)*(t/b)**2/(12*(1-v**2))) #tau_crit for front rear (and mid)
        tau_crit.append(tau_crit_case)
    return tau_crit # returns list of critical shear stress for front, rear and mid(if used) spar web

#formula test
# print(crit_shear_stress(4, 150, 10, 0.33, 72.4e9))



#torsion contribution to shear flow - by kaj 
def torsion(FlexBox: FlexBox, torque):
    areas = FlexBox.totalArea
    lengths = FlexBox.lengths
    thicknesses = FlexBox.thicknesses
    g = c.G_MODULUS

    if FlexBox.midSpar != None:

        areaFactor1 = 1/(2*areas['front'])
        q1Cell1 = areaFactor1*(lengths['f']/(g*thicknesses['f'])+lengths['b']/(g*thicknesses['b'])+lengths['m']/(g*thicknesses['m'])+lengths['t']/(g*thicknesses['t']))
        q2Cell1 = areaFactor1*(-lengths['m']/(g*thicknesses['m']))
        areaFactor2 = 1/(2*areas['back'])
        q2Cell2 = areaFactor2*(lengths['f']/(g*thicknesses['f'])+lengths['b']/(g*thicknesses['b'])+lengths['m']/(g*thicknesses['m'])+lengths['t']/(g*thicknesses['t']))
        q1Cell2 = areaFactor2*(-lengths['m']/(g*thicknesses['m']))
        matrix = np.array([[2*1/areaFactor1,2*1/areaFactor2,0],
                            [q1Cell1,q2Cell1,-1],
                            [q1Cell2,q2Cell2,-1]])
        rhs = np.array([[torque],
                        [0],
                        [0]])

        solution = np.linalg.solve(matrix,rhs)
        torsionDict = {
            'q1': solution[0][0],
            'q2': solution[1][0],
            'twist': solution[2][0]
        }

    else:
        area = areas['total']
        q = torque/(2*area)
        twist = torque/(g*FlexBox.polarMoment)
        torsionDict = {
            'q1': q,
            'twist': twist
        }
    return torsionDict




def max_shear_stress(cell:Cell.Cell):
    k_v = 1.5 #factor 1.5 to take max from average TODO can be changed

    A = cell.edges['f'+"i"] * cell.wingboxThicknesses['f'] + cell.edges['r'+"i"] * cell.wingboxThicknesses['r']
    if cell.midSpar != None:
        A += cell.edges['m'+"i"] * cell.wingboxThicknesses['m']

    V_pos = load_pos["Vy"](cell.spanwisePos(0.0)) #taken from code structure document
    V_neg = load_neg["Vy"](cell.spanwisePos(0.0)) #at zero as the shear would be the highest there per cell

    tau_max_shear_pos = abs(k_v * V_pos/A) #V/A is the avg shear stress    and output is shear per web
    tau_max_shear_neg = abs(k_v * V_neg/A) #V/A is the avg shear stress

    #total max shear stress including torsion
    if cell.midSpar == None:
        tau_totalposf = torsion('q1') * cell.wingboxThicknesses('f') + tau_max_shear_pos
        tau_totalposr = torsion('q2') * cell.wingboxThicknesses('r') + tau_max_shear_pos
        tau_max_pos = [tau_totalposf, tau_totalposr] # no mid spar positive load case
        tau_totalnegf = torsion('q1') * cell.wingboxThicknesses('f') + tau_max_shear_neg
        tau_totalnegr = torsion('q2') * cell.wingboxThicknesses('r') + tau_max_shear_neg
        tau_max_neg = [tau_totalnegf, tau_totalnegr] #no mid spar negative load case
    else:
        tau_totalposf = torsion('q1') * cell.wingboxThicknesses('f') + tau_max_shear_pos
        tau_totalposr = torsion('q2') * cell.wingboxThicknesses('r') + tau_max_shear_pos
        tau_totalposm = abs(torsion('q2')-torsion('q1')) * cell.wingboxThicknesses('m') + tau_max_shear_pos
        tau_max_pos = [tau_totalposf, tau_totalposr, tau_totalposm] # with mid spar positive load case
        tau_totalnegf = torsion('q1') * cell.wingboxThicknesses('f') + tau_max_shear_neg
        tau_totalnegr = torsion('q2') * cell.wingboxThicknesses('r') + tau_max_shear_neg
        tau_totalnegm = abs(torsion('q2')-torsion('q1')) * cell.wingboxThicknesses('m') + tau_max_shear_neg
        tau_max_neg = [tau_totalnegf, tau_totalnegr, tau_totalnegm] #with mid spar negative load case


    return tau_max_pos, tau_max_neg
    
