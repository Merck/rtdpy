"""Define PDE for closed-closed Axial Dispersion model."""
import numpy as np


def diff_eq(u, pe, h):
    """
    Basic difference equation.

    1/pe d^2C/dz^2 - dC/dz
    """
    return (1 / pe / h**2 * (u[0] - 2 * u[1] + u[2])
            - 1 / (2 * h) * (u[2] - u[0]))


def dudt(t, u, pe, h, n, a):
    """
    Define PDE equation for AD closed-closed

    dC/dTheta = 1/Pe d^2C/dz^2 - dC/dz

    BC's Danckwerts:

    * Upstream BC: -Cin = 1/Pe dC/dz - C  (z=0)
      * Impulse for Cin is approximated by an exponential with parameter a>>1
    * Downstream BC: dC/dz = 0 (z=1)
    """
    tmp = np.empty_like(u)
    # Finite difference equations for dimensionless equation
    for j in range(1, n - 1):
        tmp[j] = diff_eq(u[j-1:j+2], pe, h)

    # Ghost node approach for setting upstream boundary condition
    u_us = pe * 2 * h * a * np.exp(-a * t) + u[1] - pe * 2 * h * u[0]
    tmp[0] = diff_eq([u_us, u[0], u[1]], pe, h)

    # Ghost node approach for seeting downstream boundary condition
    u_ds = u[n-2]
    tmp[n-1] = diff_eq([u[n-2], u[n-1], u_ds], pe, h)
    return tmp


def jac(t, u, pe, h, n, a):
    """
    Define Jacobian for AD closed-closed
    """
    tmp = np.zeros([n, n])

    for i in range(n - 2):
        j = i + 1
        tmp[j, j - 1] = 1 / pe / h ** 2 + 1 / (2 * h)
        tmp[j, j] = -2 / pe / h ** 2
        tmp[j, j + 1] = 1 / pe / h ** 2 - 1 / (2 * h)

    # Upstream node with ghost node
    tmp[0, 0] = 1 / pe / h ** 2 * (-2 - pe * 2 * h) - pe
    tmp[0, 1] = 2 / pe / h ** 2

    # Downstream node with ghost node
    tmp[n - 1, n - 1] = -2 / pe / h ** 2
    tmp[n - 1, n - 2] = 2 / pe / h ** 2
    return tmp
