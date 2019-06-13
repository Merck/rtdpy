"""Axial Dispersion high peclet number assumption."""
import numpy as np
from rtdpy.rtd import RTD, RTDInputError


class AD_hi_peclet(RTD):
    """
    Create Axial Dispersion with small amount of Dispersion (Pe>100)
    Residence Time Distribution (RTD) model. [1]_

    .. math::

        E(t) = \\frac{\\sqrt{Pe}}{2\\tau\\sqrt{\\pi}}
        \\text{exp}\\left[-\\frac{Pe \\left(1-t/\\tau\\right)^2}
        {4}\\right]

    Parameters
    ----------
    tau : scalar
        L/U.  Mean residence time.
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

    References
    ----------
    .. [1] Levenspiel O. (1999) "Chemical Reaction Engineering: Third Edition"
           John Wiley & Sons, Inc.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> import rtdpy
    >>> for pe in [100, 1000]:
    ...     a = rtdpy.AD_hi_peclet(tau=1, peclet=pe, dt=.01, time_end=3)
    ...     plt.plot(a.time, a.exitage, label=f"peclet={pe}")
    >>> plt.xlabel('Time')
    >>> plt.ylabel('Exit Age Function')
    >>> plt.legend()
    >>> plt.show()
    """

    def __init__(self, tau, peclet, dt, time_end):
        super().__init__(dt, time_end)

        if tau <= 0:
            raise RTDInputError('tau less than zero')
        self._tau = tau

        if peclet <= 0:
            raise RTDInputError('peclet less than zero')
        self._peclet = peclet

        self._exitage = self._calc_exitage()

    def _calc_exitage(self):
        """Calculate exitage."""
        theta_safe = np.clip(self.theta, np.finfo(float).eps, None)
        output = 1 / self.tau \
            / np.sqrt(4. * np.pi / self.peclet) \
            * np.exp(-(1. - theta_safe) ** 2
                     / (4. / self.peclet))
        return output

    @property
    def theta(self):
        """Dimensionless Time."""
        return self.time / self.tau

    @property
    def peclet(self):
        """Peclet Number"""
        return self._peclet

    @property
    def tau(self):
        """Mean residence time, Tau."""
        return self._tau

    def __repr__(self):
        """Representation of object"""
        return ("AD_hi_peclet(tau={}, peclet={}, dt={}, time_end={})".format(
            self.tau, self.peclet, self.dt, self.time_end))
