import numpy as np
import matplotlib.pyplot as plt

# Function to calculate horizontal tail area
def S_hor(V_h, S, MAC, x_h):
    S_h = ( V_h * S * MAC ) / x_h
    return S_h

# Function to calculate vertical tail area
def S_vert(V_v, S, MAC, b, x_v):
    S_v = ( V_v * S * b) / x_v
    return S_v

# Function to calculate span of horizontal tail 
def b_hor_tail(AR_hor_t, S_hor_tail AR_vert_t, S_vert_tail):
    b_h = np.sqrt( AR_hor_tail * S_hor_tail)
    return b_h

# Function to calculate span of vertical tail 
def b_vert_tail(AR_vert_t, S_vert_tail):
    b_v = np.sqrt( AR_vert_tail * S_vert_tail)
    return b_v

def c_r_hor_tail( S_hor_tail, taper_hor_tail, b_hor):
    c_rh = ( 2 * S_hor_tail ) / ( ( 1 + taper_hor_tail ))