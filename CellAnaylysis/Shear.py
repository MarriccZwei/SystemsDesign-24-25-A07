import numpy as np

def crit_shear_stress(t, b, k_s, v, E):
    tau_crit = ((np.pi**2*k_s*E)*(t/b)**2/(12*(1-v**2)))
    return tau_crit

def boom1(t,b,sigma_ratio):
    boom = (t*b/6)*(2+sigma_ratio)
    return boom

def sigma_ratio1(y1,y2):
    sigma_ratio = y2/y1
    return sigma_ratio


def ideal_Ixx(Bft,Bmt,Brt,Bfb,Bmb,Brb,yft,ymt,yrt,yfb,ymb,yrb):
    Ixx = Bft*yft**2 + Bmt*ymt**2 + Brt*yrt**2 + Bfb*yfb**2 + Bmb*ymb**2 + Brb*yrb**2
    return Ixx
    
def delta_q(V, Ixx, B, y):
    q = (V*B*y)/Ixx
    return q


def shearcalc():
    if 