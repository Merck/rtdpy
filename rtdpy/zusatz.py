import numpy as np

from rtdpy.rtd import RTD


class Zusatz(RTD):
    """
    Create Zusatz Residence Time Distribution (RTD) model. [1]_
    Parameter a is chosen such that the integral is 1.

    .. math::

        E(t) = a t^{-c-1} b^{c+1}
        \\text{exp}\\left[\\left(b^c t^{-c} -1\\right)\\frac{-c-1}{c}\\right]
        \\\\a = \\frac{1+c}{b\\, \\text{exp}\\left[1+1/c\\right]}

    Parameters
    ----------
    b : scalar
        b Zusatz parameter
    c : scalar
        c Zusatz parameter
    dt : scalar
        Time step for RTD. ``dt>0``
    time_end : scalar
        End time for RTD. ``time_end>0``

    References
    ----------
    .. [1] Poulesquen A., et al. (2003) A study of residence time distribution
           in co-rotating twin-screw extruders.  Part II: Experimental
           validation. "Polymer Engineering and Science", 43(12), 1849-1862.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> import rtdpy
    >>> for c in [3, 7]:
    >>>     a = rtdpy.Zusatz(b=25, c=c, dt=.01, time_end=100)
    >>>     plt.plot(a.time, a.exitage, label=f"c={c}")
    >>> plt.xlabel('Time')
    >>> plt.ylabel('Exit Age Function')
    >>> plt.legend()
    >>> plt.show()
    """
    def __init__(self, b, c, dt, time_end):
        super().__init__(dt, time_end)

        self._a = None
        self._b = None
        self._c = None

        self.b = b
        self.c = c

    def _calc_exitage(self):
        """equation for exit age function"""
        try:
            time_safe = np.clip(self.time, np.finfo(float).eps, None)
            output = self.a * time_safe**(-self.c-1) \
                * self.b**(self.c + 1) \
                * np.exp((self.b**self.c * time_safe**(-1 * self.c) - 1)
                         * (-self.c - 1) / self.c)
        except TypeError:
            output = None
        return output

    def _calc_a(self):
        """calculate a to normalize rtd"""
        try:
            output = (1 + self.c) / (self.b * np.exp(1 + 1 / self.c))
        except TypeError:
            output = None
        return output

    @property
    def a(self):
        """a parameter that normalizes RTD to 1"""
        return self._a

    @property
    def b(self):
        """b parameter"""
        return self._b

    @b.setter
    def b(self, b):
        # TODO: check for limits on input parameters
        self._b = b
        self._a = self._calc_a()
        self._exitage = self._calc_exitage()

    @property
    def c(self):
        """c parameter"""
        return self._c

    @c.setter
    def c(self, c):
        # TODO: check for limits on input parameters
        self._c = c
        self._a = self._calc_a()
        self._exitage = self._calc_exitage()
