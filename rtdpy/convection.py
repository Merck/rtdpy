import numpy as np

from rtdpy.rtd import RTD, RTDInputError


class Convection(RTD):
    """
    Create pure convection model for laminar flow in a pipe. [1]_

    The true RTD curve is given by :math:`E(t)` for a flux-based introduction
    of material and a flux-based measurment. If only one of introduction or
    measurement is planar, then the apparent RTD is given by :math:`E^*(t)`.
    If both introduction and measurement are planar, then the apparent RTD
    is given by :math:`E^{**}(t)`.

    .. math::

        \\begin{align*}
        E(t) &= \\frac{\\tau^2}{2t^3} & \\text{for } t\\geq\\frac{\\tau}{2}\\\\
        E^*(t) &= \\frac{\\tau}{2t^2} & \\text{for } t\\geq\\frac{\\tau}{2}\\\\
        E^{**}(t) &= \\frac{\\tau}{2t} & \\text{for } t\\geq\\frac{\\tau}{2}
        \\end{align*}

    * :math:`E(t)` is Convection.exitage
    * :math:`E^*(t)` is Convection.exitage_star
    * :math:`E^{**}(t)` is Convection.exitage_star2

    Parameters
    ----------
    tau : scalar
        Mean residence time of true RTD.
    dt : scalar
        Time step for RTD. ``dt>0``
    time_end : scalar
        End time for RTD. ``time_end>0``

    References
    ----------
    .. [1] Levenspiel O. (1999) "Chemical Reaction Engineering: Third Edition"
           John Wiley & Sons, Inc.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> import rtdpy
    >>> a = rtdpy.Convection(tau=1, dt=.01, time_end=2)
    >>> plt.plot(a.time, a.exitage, label='E')
    >>> plt.plot(a.time, a.exitage_star, label='E*')
    >>> plt.plot(a.time, a.exitage_star2, label='E**')
    >>> plt.xlabel('Time')
    >>> plt.ylabel('Exit Age Function')
    >>> plt.legend()
    >>> plt.show()
    """

    def __init__(self, tau, dt, time_end):
        super().__init__(dt, time_end)

        if tau <= 0:
            raise RTDInputError("tau less than zero")
        self._tau = tau

        self._exitage = self._calc_exitage()
        self._exitage_star = self._calc_exitage_star()
        self._exitage_star2 = self._calc_exitage_star2()

    def _calc_exitage(self):
        """Calculte exit age function."""
        time_safe = np.clip(self.time, np.finfo(np.float).eps, None)
        output = self.tau**2 / (2 * time_safe**3)
        mintime = self.tau / 2
        output[self.time < mintime] = 0.
        return output

    def _calc_exitage_star(self):
        """Calculte exit age function."""
        time_safe = np.clip(self.time, np.finfo(np.float).eps, None)
        output = self.tau / (2 * time_safe**2)
        mintime = self.tau/2
        output[self.time < mintime] = 0.
        return output

    @property
    def exitage_star(self):
        """Planar-Flux or Flux-Planar exitage."""
        return self._exitage_star

    def _calc_exitage_star2(self):
        """Calculte exit age function."""
        time_safe = np.clip(self.time, np.finfo(np.float).eps, None)
        output = 1. / (2 * time_safe)
        mintime = self.tau/2
        output[self.time < mintime] = 0.
        return output

    @property
    def exitage_star2(self):
        """Planar-Planar exitage."""
        return self._exitage_star2

    @property
    def tau(self):
        """Mean Residence Time of **all** tanks combined."""
        return self._tau

    def __repr__(self):
        """Representation of object."""
        return ("Convection(tau={}, dt={}, time_end={})".format(
            self.tau, self.dt, self.time_end))
