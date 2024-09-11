from math import sqrt, pi, exp, log
import matplotlib.pyplot as plt
import numpy as np

#weights
M_pl_max = 49442 #maximum payload
M_pl_des = 27669
Mf_oe = 0.473 #operational empty mass fraction (M_oe/M_mtow) avg of the similar aircraft

#variables used for C_d0 calculations, based on equation 6.15 from the adsee reader
wet_wing_area = 6.2 #wetted area to wing area ratio found in the ADSEE book
C_f = 0.0026 #skin friction coeff found in the ADSEE book

#variables used to calculate oswald factor, based on equation 6.17
eff_span = 0.97 #span efficiency found in the ADSEE book
D_par = 0.0075 #lift dependent parasite drag found in the ADSEE book
 
AR = 9.28375 #aspect ratio using the average of the reference aircraft

B = 8.25
TSFC = 22*B**-0.19
e_spec = 43.5 *10**6 #specific energy for kerosene, value found in the ADSEE book
g = 9.81 #gravitational acceleration constant
h_cr = 11887.2 #cruise altitude [m]
v_cr = 241.9 #cruise speed [m/s]
F_con = 0.05 #fraction of fuel used for contingency 
R_div = 370000 #diversion range of aircraft
t_e = 45 * 60 #loiter time
R_nom = 13797000 #design mission range
eff_eng = v_cr / (TSFC * e_spec)*10**6 #0.379 #engine efficiency based on equation 6.23 in the ADSEE book

Cd_0 = C_f * wet_wing_area #zero lift drag calculation

e = 1/(pi * AR * D_par + (1/eff_span)) #oswald factor

L_D = 0.5 * sqrt((pi * AR * e)/Cd_0) #lift to drag ratio

#calculations of equivalent range
R_lost = (1/0.7) * L_D * (h_cr + (v_cr**2)/(2*g)) #lost range 
R_eq = (R_nom + R_lost) * (1 + F_con) + 1.2 * R_div + v_cr * t_e #equivalent range
R_aux = R_eq - R_nom #auxilary range

Mf_ec = 1 - exp((-R_eq) / (eff_eng * (e_spec / g) * L_D)) #fuel mass fraction

M_mto = (M_pl_des)/(1 - Mf_ec - Mf_oe) #maximum take-off mass
M_ec = Mf_ec * M_mto #fuel mass
M_oe = Mf_oe * M_mto #operating empty mass

M_f = M_mto - M_oe - M_pl_max 

R_ferry = eff_eng * L_D * (e_spec / g) * log((M_oe + M_ec)/(M_oe)) - R_aux  #ferry range
R_harm = eff_eng * L_D * (e_spec / g) * log((M_oe + M_pl_max + M_f)/(M_oe + M_pl_max)) - R_aux #harmonic range


#plot
ds = 50000 #step size [m]
M_pl_list = [] #naming of Mass payload list
curve_one_der = (M_pl_max - M_pl_des)/(R_nom - R_harm) #kg / 500 km
curve_two_der = (M_pl_des)/(R_ferry - R_nom) #kg / 500 km
M_pl = M_pl_max #placeholder for the payload mass to append to the lists
R_list = [] #np.arange(0,18000000,ds)
R = 0 #placeholder for the range to append to the lists


#generates the payload mass for the R_0 part of the curve
for i in range(0, int(R_harm), ds):
    M_pl_list.append(M_pl) 
    R += ds
    R_list.append(R/1000)




#generates the payload mass for the R_1 part of the curve
for i in range(0, int(R_nom - R_harm), ds):
    M_pl = M_pl - curve_one_der * ds
    M_pl_list.append(M_pl)
    R += ds
    R_list.append(R/1000)


#generates the payload mass for the R_2 part of the curve
for i in range(0, int(R_ferry - R_nom), ds):
    M_pl = M_pl - curve_two_der * ds
    M_pl_list.append(M_pl)
    R += ds
    R_list.append(R/1000)

print("maximum payload [kg]:")
print(M_pl_max)
print()
print("Harmonic range [km]:")
print(R_harm/1000)
print()
print("design payload [kg]:")
print(M_pl_des)
print()
print("nominal range [km]:")
print(R_nom/1000)
print()
print("ferry mass [kg]:")
print(M_mto - M_pl_des)
print()
print("ferry range [km]:")
print(R_ferry/1000)
print()
print("maximum take-off weight [kg]:")
print(M_f)


plt.plot(R_list, M_pl_list)
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)
plt.xlabel("range [km]", fontsize=18)
plt.ylabel("payload [kg]", fontsize=18)
plt.title("payload range diagram", fontsize=25)
plt.grid(visible=True, which="major", axis="both")
plt.xlim(0)
plt.ylim(0)
plt.show()