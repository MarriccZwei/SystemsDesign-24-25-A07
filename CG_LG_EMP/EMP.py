import numpy as np
import matplotlib.pyplot as plt

# Function to calculate horizontal and vertical tail area
def S_tail(V_h, S, MAC, x_h, V_v, b, x_v, x_aftcg):
    S_h = ( V_h * S * MAC ) / (x_h-x_aftcg)
    S_v = ( V_v * S * b) / (x_v-x_aftcg)
    return S_h, S_v

# Function to calculate span of horizontal and vertical tail 
def b_tail(AR_hor_t, S_hor_tail, AR_vert_t, S_vert_tail):
    b_h = np.sqrt( AR_hor_t * S_hor_tail)
    b_v = np.sqrt( AR_vert_t * S_vert_tail)
    return b_h, b_v

# Function to calculate root chord horizontal and vertical tail
def c_r_tail(S_hor_tail, taper_hor_tail, b_hor, S_vert_tail, taper_vert_tail, b_vert):
    c_rh = ( 2 * S_hor_tail ) / ( ( 1 + taper_hor_tail ) * b_hor)
    c_rv = ( 2 * S_vert_tail ) / ( ( 1 + taper_vert_tail ) * b_vert)
    return c_rh, c_rv

# Function to calculate tip chord horizontal and vertical tail  
def c_t_tail(taper_hor_tail, c_root_hor, taper_vert_tail, c_root_vert):
    c_th =  taper_hor_tail * c_root_hor
    c_tv = taper_vert_tail * c_root_vert
    return c_th, c_tv

# Function to calculate MAC horziontal and verrtical tail
def mac_tail(c_root_hor, c_root_vert, taper_hor_tail, taper_vert_tail): 
    MAC_h = (2/3) * c_root_hor * (( 1 + taper_hor_tail + taper_hor_tail **2 ) / ( 1 + taper_hor_tail ))
    MAC_v = (2/3) * c_root_vert * (( 1 + taper_vert_tail + taper_vert_tail **2 ) / ( 1 + taper_vert_tail ))
    return MAC_h, MAC_v