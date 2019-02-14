"""
compute_ss_model
    - Chapter 5 assignment for Beard & McLain, PUP, 2012
    - Update history:
        2/4/2019 - RWB
"""
import sys
sys.path.append('..')
import numpy as np
from scipy.optimize import minimize
from tools.tools import Euler2Quaternion, Quaternion2Euler
#from tools.transfer_function import transfer_function
import parameters.aerosonde_parameters as MAV
from parameters.simulation_parameters import ts_simulation as Ts
import control.matlab as ctrl

def compute_tf_model(mav, trim_state, trim_input):
    # trim values

    mav._state = trim_state
    mav._update_velocity_data()

    state_euler = euler_state(trim_state)
    # extract the states
    pn = state_euler.item(0)
    pe = state_euler.item(1)
    pd = state_euler.item(2)
    u = state_euler.item(3)
    v = state_euler.item(4)
    w = state_euler.item(5)
    phi = state_euler.item(6)
    theta = state_euler.item(7)
    psi = state_euler.item(8)
    p = state_euler.item(9)
    q = state_euler.item(10)
    r = state_euler.item(11)
    #  inputs
    delta_a = trim_input.item(0)
    delta_e = trim_input.item(1)
    delta_r = trim_input.item(2)
    delta_t = trim_input.item(3)



    a_phi_1 = -0.5*MAV*mav._Va**2*MAV.S_wing*MAV.b*MAV.C_p_p*MAV.b/(2.*mav._Va)
    a_phi_2 = 0.5*MAV.rho*mav._Va**2*MAV.S_wing*MAV.b*MAV.C_p_delta_a
    d_phi_1 = q*np.sin(phi)*np.tan(theta) + r*np.cos(phi)*np.tan(theta)
    d_dot_phi_1 = 0.0 #help
    d_phi_2 = MAV.gamma1*p*q - MAV.gamma2*q*r + \
        0.5*MAV.rho*mav._Va**2*MAV.S_wing*MAV.b*(MAV.C_p_0+MAV.C_p_beta*beta-MAV.C_p_p*MAV.b*d_phi_1/(2.*Va)+MAV.C_p_r*MAV.b*r/(2.*Va)+MAV.C_p_delta_r*delta_r) + d_dot_phi_1
    T_phi_delta_a = ctrl.tf([a_phi2*(delta_a+d_phi_2/a_phi_2)],[1 a_phi_2,0])

    T_chi_phi = ctrl.tf([],[])

    return T_phi_delta_a, T_chi_phi, T_theta_delta_e, T_h_theta, T_h_Va, T_Va_delta_t, T_Va_theta, T_beta_delta_r

def compute_ss_model(mav, trim_state, trim_input):
     return A_lon, B_lon, A_lat, B_lat

def euler_state(x_quat):
    # convert state x with attitude represented by quaternion
    # to x_euler with attitude represented by Euler angles
    x_euler = np.zeros((12,1))
    phi,theta,psi = Quaternion2Euler(x_quat[6:10])
    x_euler[0:6] = x_quat[0:6]
    x_euler[6] = phi
    x_euler[7] = theta
    x_euler[8] = psi
    x_euler[9:12] = x_quat[10:13]
     return x_euler

def quaternion_state(x_euler):
    # convert state x_euler with attitude represented by Euler angles
    # to x_quat with attitude represented by quaternions
    phi = x_euler[6]
    theta = x_euler[7]
    psi = x_euler[8]
    e0, e1, e2, e3 = Euler2Quaternion(phi,theta,psi)
    x_quat = x_euler.copy()
    x_quat[6] = e0
    x_quat[7] = e1
    x_quat[8] = e2
    x_quat = np.insert(x_quat,9,[e3],axis=0)
    return x_quat

def f_euler(mav, x_euler, input):
    # return 12x1 dynamics (as if state were Euler state)
    # compute f at euler_state
    return f_euler_

def df_dx(mav, x_euler, input):
    # take partial of f_euler with respect to x_euler
    return A

def df_du(mav, x_euler, delta):
    # take partial of f_euler with respect to delta
    return B

def dT_dVa(mav, Va, delta_t):
    # returns the derivative of motor thrust with respect to Va
    return dThrust

def dT_ddelta_t(mav, Va, delta_t):
    # returns the derivative of motor thrust with respect to delta_t
    return dThrust
