from math import floor, ceil
M_pl = 27669

def CrossSection(M_pl):

    N_pax = floor(M_pl/105)
    N_sa = 0.45*N_pax**0.5

    if N_sa - floor(N_sa) >0.5:
        N_sa = ceil(N_sa)
        print("N_sa is rounded up")
    else:
        N_sa = floor(N_sa)
        print("N_sa is rounded down")
    
    n_aisle = 2

    w_aisle = 51
    w_clearance = 2
    #next dimensions are based on economy class and long range
    w_seat = 44
    w_armrest = 5

    w_cabin = N_sa * w_seat + (N_sa + n_aisle + 1) * w_armrest + n_aisle * w_aisle + 2 * w_clearance
    w_floor = w_cabin - 2* (w_armrest + w_clearance)
    w_headroom = w_floor - w_seat

    h_armrest = 65
    h_shoulder = 105
    h_headroom = 140
    h_floor = 20


    return [w_cabin, w_floor, w_headroom, N_pax, N_sa]

def CabinLen(N_pax, N_sa):
    l_cabin = 1.17*(N_pax/N_sa)
    return l_cabin

cross = CrossSection(M_pl)
# print(CrossSection(M_pl))
l_cabin = CabinLen(cross[3], cross[4])

r_1inner = 2.387
r_2inner = 2.314
df_inner = r_1inner + r_2inner
df_outer = 1.045* df_inner + 0.084
t_wall = (df_outer - df_inner)/2

w_fus = 2.387*2+2*t_wall
h_fus = 5.2475 +2*t_wall
d_fus = (w_fus+h_fus)/2

l_n = 4
l_nc = 1.8 * d_fus #1.8 as value
l_tc = 3.0 * d_fus #3.0 as value
l_t = 0.8 * l_tc #0.8 as value

l_fus = l_cabin + l_n + l_t

#value for emre <3
xcg_p = l_n + 0.5*l_cabin


print(l_fus)