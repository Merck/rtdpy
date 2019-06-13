import numpy as np

from rtdpy.rtd import RTD, RTDInputError


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
        b Zusatz parameter. ``b>0``
    c : scalar
        c Zusatz parameter. ``c>0``
        Mean residence time only defined for ``c>1``.
        Variance only defined for ``c>2``.
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

        if b <= 0:
            raise RTDInputError("b less than zero")
        self._b = b

        if c <= 0:
            raise RTDInputError("c less than zero")
        self._c = c

        self._a = self._calc_a()

        self._exitage = self._calc_exitage()

    def _calc_exitage(self):
        """equation for exit age function"""
        time_safe = np.clip(self.time, np.finfo(float).eps, None)
        output = self.a * time_safe**(-self.c-1) \
            * self.b**(self.c + 1) \
            * np.exp((self.b**self.c * time_safe**(-1 * self.c) - 1)
                     * (-self.c - 1) / self.c)
        return output

    def _calc_a(self):
        """Calculate a to normalize rtd"""
        return (1 + self.c) / (self.b * np.exp(1 + 1 / self.c))

    @property
    def a(self):
        """a parameter that normalizes RTD to 1"""
        return self._a

    @property
    def b(self):
        """b parameter"""
        return self._b

    @property
    def c(self):
        """c parameter"""
        return self._c

    def __repr__(self):
        """Returns representation of object"""
        return ("Zusatz(b={}, c={}, dt={}, time_end={})".format(
            self.b, self.c, self.dt, self.time_end))
