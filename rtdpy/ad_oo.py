import numpy as np
from rtdpy.rtd import RTD, RTDInputError


class AD_oo(RTD):
    """
    Create Axial Dispersion with open-open boundary conditions
    Residence Time Distribution (RTD) model. [1]_

    .. math::

        E(t) = \\frac{\\sqrt{Pe}}{\\tau\\sqrt{4\\pi\\theta}}
        \\text{exp}\\left[\\frac{-Pe \\left(1-\\theta\\right)^2}
        {4\\theta}\\right]\\\\
        \\theta = t/\\tau

    Parameters
    ----------
    tau : scalar
        L/U, not the mean residence time, see tau_oo.
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

    Notes
    -----
    The mean residence time for an open-open system is not tau.
    Mean residence time is :math:`\\tau_{oo} = (1+2/Pe)*\\tau`.

    References
    ----------
    .. [1] Levenspiel O., Smith W.K. (1957) Notes on the diffusion-type model
           for the longitudinal mixing of fluids in flow.
           "Chemical Engineering Science", 6, 227-233

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> import rtdpy
    >>> for pe in [10, 100]:
    ...     a = rtdpy.AD_oo(tau=1, peclet=pe, dt=.01, time_end=3)
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
        theta_safe = np.clip(self.theta, np.finfo(float).eps, None)
        output = (1 / self.tau
                  / np.sqrt(4. * np.pi * theta_safe / self.peclet)
                  * np.exp(
                      -(1. - theta_safe) ** 2
                      / (4. * theta_safe / self.peclet)))
        return output

    @property
    def theta(self):
        """Dimensionless time."""
        return self.time / self.tau

    @property
    def peclet(self):
        """Peclet number."""
        return self._peclet

    @property
    def tau(self):
        """Tau."""
        return self._tau

    @property
    def tau_oo(self):
        """
        Mean Residence Time for open-open system.  Not tau for open-open.

        .. math:

            tau_oo = (1 + 2/Pe) tau
        """
        return (1. + 2. / self.peclet) * self.tau

    def __repr__(self):
        """Returns representation of object"""
        return ("AD_oo(tau={}, peclet={}, dt={}, time_end={})".format(
            self.tau, self.peclet, self.dt, self.time_end))
