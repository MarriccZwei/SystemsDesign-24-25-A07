import numpy as np


# Wing Group
# Distances measured from LEMAC
def X_wcg(m_wing, m_prop, MAC, x_prop):
    sum_XM = m_wing*0.4*MAC + m_prop*x_prop
    sum_M = m_wing + m_prop
    x_wcg = sum_XM/sum_M
    return X_wcg

# Fuselage Group
# Distances measured from nose tip
def X_fcg(m_fus,m_emp, m_fe, l_fus):
    sum_XM = m_fus*0.4*l_fus + m_emp*0.9*l_fus + m_fe*0.4*l_fus
    sum_M = m_fus + m_emp + m_fe
    x_fcg = sum_XM/sum_M
    return X_fcg


def x_lemac(X_fcg, MAC, m_wing, m_prop, m_fus, m_emp, m_fe):
    M_W = m_wing + m_prop 
    x_lemac = X_fcg + MAC*( 0.4*((m_wing+m_prop)/(m_fus+m_emp+m_fe)) - 0.25*MAC*(1+((m_wing+m_prop)/(m_fus+m_emp+m_fe))))
    return x_lemac

def xcg_fuel(lemac,MAC)
    xcg_fuel = (2*lemac + MAC)2
    return xcg_fuel
