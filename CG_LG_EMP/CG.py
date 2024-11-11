import numpy as np
import matplotlib.pyplot as plt

# Wing Group
# Distances measured from LEMAC
# all mass fractions
def X_wcg(m_wing, m_prop, MAC, x_prop):
    sum_XM = m_wing*0.4*MAC + m_prop*x_prop
    sum_M = m_wing + m_prop
    x_wcg = sum_XM/sum_M
    return x_wcg

# Fuselage Group
# Distances measured from nose tip
# all mass fractions
def X_fcg(m_fus,m_emp, m_fe, l_fus):
    sum_XM = m_fus*0.4*l_fus + m_emp*0.9*l_fus + m_fe*0.4*l_fus
    sum_M = m_fus + m_emp + m_fe
    x_fcg = sum_XM/sum_M
    return x_fcg


def x_lemac(X_fcg, MAC, m_wing, m_prop, m_fus, m_emp, m_fe,oew_cg_wrt_mac,w_cg_wrt_mac):
    M_W = m_wing + m_prop 
    x_lemac = X_fcg + MAC*( w_cg_wrt_mac*((m_wing+m_prop)/(m_fus+m_emp+m_fe))) - oew_cg_wrt_mac*MAC*(1+((m_wing+m_prop)/(m_fus+m_emp+m_fe)))
    return x_lemac

# OE, P, F x_distances
def xcg_f(lemac,MAC):
    xcg_f = (2*lemac + MAC)/2
    return xcg_f

def xcg_oe(lemac,MAC):
    xcg_oe = lemac +0.2*MAC
    return xcg_oe

# xcg_payload should be given from fuselage as middle of passanger cabin

## Loading diagram

# x-axis x_cg of different mass fraction combinations
def xcg_oe_p(mf_oe, mf_p, xcg_oe, xcg_p):
    xcg_oe_p = (mf_oe*xcg_oe + mf_p*xcg_p)/(mf_oe+mf_p)
    return xcg_oe_p

def xcg_oe_f(mf_oe,mf_f,xcg_oe,xcg_f):
    xcg_oe_f = (mf_oe*xcg_oe + mf_f*xcg_f)/(mf_oe+mf_f)
    return xcg_oe_f

def xcg_oe_p_f(mf_oe,mf_p,mf_f,xcg_oe,xcg_p,xcg_f):
    xcg_oe_p_f = (mf_oe*xcg_oe + mf_p*xcg_p +mf_f*xcg_f)/(mf_oe+mf_p+mf_f)
    return xcg_oe_p_f

# plotting of loading diagram
def loadingdiagram(xcg_oe, xcg_oe_p, xcg_oe_f,xcg_oe_p_f,mf_oe,mf_p,mf_f):

# Coordinates of the four points (fuselage station, mass fraction)
    points = [(xcg_oe, mf_oe), (xcg_oe_f, mf_oe+mf_f), (xcg_oe_p, mf_oe+mf_p), (xcg_oe_p_f, mf_oe+mf_p+mf_f )]

# Split points into X and Y coordinates
    x_vals = [point[0] for point in points]
    y_vals = [point[1] for point in points]

# To close the shape, append the first point at the end
    x_vals.append(points[0][0])
    y_vals.append(points[0][1])

# Create the plot
    plt.plot(x_vals, y_vals, 'o-', color='blue')  # 'o-' plots points with lines
    
# Set custom limits for x and y axes
    plt.xlim(9.0, 12.0)  # Set x-axis range from 9.0 to 12.0
    plt.ylim(0.0, 1.2)   # Set y-axis range from 0.0 to 1.2

# Labels and title
    plt.xlabel('Fuselage station, X (m)')
    plt.ylabel('Mass Fraction, M (~)')
    plt.title('Class I Loading Diagram')

# Show the plot
    plt.grid(True)
    plt.show()

def cg(xcg_oe,xcg_oe_p,xcg_oe_f,xcg_oe_p_f):
    cg = max(xcg_oe,xcg_oe_p,xcg_oe_f,xcg_oe_p_f)
    return cg
