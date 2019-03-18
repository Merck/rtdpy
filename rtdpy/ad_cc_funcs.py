"""Define PDE for closed-closed Axial Dispersion model
"""
import numpy as np


def dudt(t, u, pe, h, n, a):
    """
    Define PDE equation for AD closed-closed
    """
    tmp = np.empty_like(u)
    for j in range(1, n - 1):
        tmp[j] = 1 / pe / h ** 2 * (u[j + 1] - 2 * u[j] + u[j - 1])\
            - 1 / (2 * h) * (u[j + 1] - u[j - 1])

    u0 = pe * 2 * h * a * np.exp(-a * t) + u[1] - pe * 2 * h * u[0]

    tmp[0] = 1 / pe / h ** 2 * (u[1] - 2 * u[0] + u0)\
        - 1 / (2 * h) * (u[1] - u0)

    tmp[n - 1] = 2 / pe / h ** 2 * (u[n - 2] - u[n - 1])
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

    tmp[0, 0] = 1 / pe / h ** 2 * (-2 - pe * 2 * h) - pe
    tmp[0, 1] = 2 / pe / h ** 2
    tmp[n - 1, n - 1] = -2 / pe / h ** 2
    tmp[n - 1, n - 2] = 2 / pe / h ** 2
    return tmp
