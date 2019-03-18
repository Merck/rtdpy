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
        L/U, not the mean residence time, see tau_oo
    peclet : scalar
        Reactor Peclet number (L*U/D)
    dt : scalar
        Time step for RTD.
        ``dt>0``
    time_end : scalar
        End time for RTD.
        ``time_end>0``

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
    ...     plt.plot(a.time, a.exitage, label="peclet={}".format(pe))
    >>> plt.xlabel('Time')
    >>> plt.ylabel('Exit Age Function')
    >>> plt.legend()
    >>> plt.show()
    """

    def __init__(self, tau, peclet, dt, time_end):
        super().__init__(dt, time_end)

        self._peclet = None
        self._theta = None
        self._tau_oo = None
        self._tau = None

        self.tau = tau
        self.peclet = peclet

    def _calc_exitage(self):
        try:
            theta_safe = np.clip(self.theta, np.finfo(float).eps, None)
            output = 1 / self.tau \
                / np.sqrt(4. * np.pi * theta_safe / self.peclet) \
                * np.exp(-(1. - theta_safe) ** 2
                         / (4. * theta_safe / self.peclet))

        except AttributeError:
            output = None
        except TypeError:
            output = None
        return output

    def _calc_theta(self):
        try:
            output = self.time / self.tau
        except (AttributeError, TypeError):
            output = None
        return output

    def _calc_tau_oo(self):
        try:
            output = (1. + 2. / self.peclet) * self.tau
        except TypeError:
            output = None
        return output

    @property
    def theta(self):
        return self._theta

    @property
    def peclet(self):
        return self._peclet

    @peclet.setter
    def peclet(self, peclet):
        if peclet <= 0:
            raise RTDInputError('peclet less than zero')
        self._peclet = peclet
        self._tau_oo = self._calc_tau_oo()
        self._theta = self._calc_theta()
        self._exitage = self._calc_exitage()

    @property
    def tau(self):
        return self._tau

    @tau.setter
    def tau(self, tau):
        if tau <= 0:
            raise RTDInputError('tau less than zero')
        self._tau = tau
        self._tau_oo = self._calc_tau_oo()
        self._theta = self._calc_theta()
        self._exitage = self._calc_exitage()

    @property
    def tau_oo(self):
        """
        Mean Residence Time for open-open system is different than L/U
        """
        return self._tau_oo
