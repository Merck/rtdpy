"""Closed-closed axial dispersion model"""
import numpy as np
from scipy import integrate

from rtdpy.rtd import RTD, RTDInputError
from rtdpy.ad_cc_funcs import dudt, jac


class AD_cc(RTD):
    """
    Create Axial Dispersion with closed-closed boundary conditions
    Residence Time Distribution (RTD) model. [1]_ [2]_

    Solution of equation

    .. math::

        \\frac{\\partial C}{\\partial \\theta}
        = \\frac{1}{Pe}\\frac{\\partial^2 C}{\\partial z^2}
        - \\frac{\\partial C}{\\partial z}

    where :math:`\\theta = t/\\tau` is dimensionless time,
    :math:`z` is dimensionless length, and an impulse input at z=0
    with Danckwerts BCs

    .. math::

        E(t) = C(z=1, t)\\\\
        C_{in} = \\delta(t)\\\\
        C_{in} = C\\rvert_{z=0}
        - \\frac{1}{Pe}\\frac{\\partial C}{\\partial z}\\biggr\\rvert_{z=0}\\\\
        \\frac{\\partial C}{\\partial z} = 0, z=1

    and initial conditions

    .. math::

        C=0 \\text{ for } t=0

    The inpulse input is approximated by a fast exponential.

    Parameters
    ----------
    tau : scalar
        L/U or mean residence time.
        ``tau>0``
    peclet : scalar
        Reactor Peclet number (L*U/D).
        ``peclet>0``
    dt : scalar
        Time step for RTD.
        ``dt>0``
    time_end : scalar
        End time for RTD.
        ``time_end>0``

    Other Parameters
    ----------------
    nx : optional
        Number of points to discretize 1D PDE. Default is 200.
    a : optional
        Rate at which to introduce material.
        The inverse of a is the approximate amount of time to resolve the
        impulse input. Default is 10000.
    rtol : optional
        Relative tolerance to use in ODE solver. Default is 1e-5
    atol : optional
        Absolute tolerance to use in ODE solver. Default is 1e-10.
    max_step : optional
        Maximum time step size (dimensionless) to use in ODE solver.
        Default is 0.01.

    References
    ----------
    .. [1] Pearson J.R.A. (1959) A note on the "Danckwerts" boundary conditions
           for continuous flow reactors. "Chemical Engineering Science", 6,
           281-284.
    .. [2] Danckwerts P.V. (1953) Continuous flow systems: Distribution of
           Residence Times. "Chemical Engineering Science", 2, 1-13.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> import rtdpy
    >>> for pe in [10, 100]:
    ...     a = rtdpy.AD_cc(tau=1, peclet=pe, dt=.01, time_end=3)
    ...     plt.plot(a.time, a.exitage, label=f"peclet={pe}")
    >>> plt.xlabel('Time')
    >>> plt.ylabel('Exit Age Function')
    >>> plt.legend()
    >>> plt.show()
    """

    def __init__(self, tau, peclet, dt, time_end, nx=200, a=10000, rtol=1e-5,
                 atol=1e-10, max_step=0.01):
        """Axial Dispersion closed-closed model"""
        super().__init__(dt, time_end)

        self._tau = tau
        self._peclet = None
        self._pde_result = None

        self.nx = nx
        self.a = a
        self.rtol = rtol
        self.atol = atol
        self.max_step = max_step

        if tau <= 0:
            raise RTDInputError('tau less than zero')
        self._tau = tau

        if peclet <= 0:
            raise RTDInputError('peclet less than zero')
        self._peclet = peclet

        self._pde_result = self._calc_pde(self.time_end / self.tau)
        self._exitage = self._calc_exitage()

    def _calc_pde(self, t_max):
        """Calculate the dimensionless pde result."""

        t_span = (0, t_max)
        x = np.linspace(0, 1, self.nx)
        u0 = np.zeros(self.nx)
        h = x[1] - x[0]
        j = jac(0, 0, self.peclet, h, self.nx, self.a)

        sol = integrate.solve_ivp(
            fun=lambda t, y: dudt(t, y, self.peclet, h, self.nx, self.a),
            jac=j, t_span=t_span, y0=u0, method="BDF", dense_output=True,
            rtol=self.rtol, atol=self.atol, max_step=self.max_step)
        return sol

    def _calc_exitage(self):
        """Calculate exit age from dimensionless result."""
        output = self._pde_result.sol(self.time / self.tau)[-1] / self.tau
        return output

    @property
    def peclet(self):
        """Peclet number."""
        return self._peclet

    @property
    def tau(self):
        """Tau"""
        return self._tau

    def __repr__(self):
        """Representation of object"""
        return ("AD_cc(tau={}, peclet={}, dt={}, time_end={}, nx={}, a={}"
                + ", rtol={}, atol={}, max_step={})").format(
                    self.tau, self.peclet, self.dt, self.time_end, self.nx,
                    self.a, self.rtol, self.atol, self.max_step)
