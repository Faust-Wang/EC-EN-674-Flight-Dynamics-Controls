# tools based on Beard
from math import cos,sin,asin,atan2
import numpy as np

def Euler2Quaternion(phi, theta, psi):
    e0 = cos(psi/2.)*cos(theta/2.)*cos(phi/2.)+sin(psi/2.)*sin(theta/2.)*sin(phi/2.)
    e1 = cos(psi/2.)*cos(theta/2.)*sin(phi/2.)-sin(psi/2.)*sin(theta/2.)*cos(phi/2.)
    e2 = cos(psi/2.)*sin(theta/2.)*cos(phi/2.)+sin(psi/2.)*cos(theta/2.)*sin(phi/2.)
    e3 = sin(psi/2.)*cos(theta/2.)*cos(phi/2.)-cos(psi/2.)*sin(theta/2.)*sin(phi/2.)
    e = np.array([e0, e1, e2, e3])
    return e

def Quaternion2Euler(e):
    e0 = e[0]
    e1 = e[1]
    e2 = e[2]
    e3 = e[3]
    phi = atan2(2*(e0*e1+e2*e3),(e0**2+e3**2-e1**2-e2**2))
    theta = asin(2*(e0*e2-e1*e3))
    psi = atan2(2*(e0*e3+e1*e2),(e0**2+e1**2-e2**2-e3**2))
    return phi, theta, psi