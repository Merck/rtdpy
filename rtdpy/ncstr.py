import numpy as np
from scipy import special

from rtdpy.rtd import RTD, RTDInputError


class Ncstr(RTD):
    """
    Create N CSTR in series (N-CSTR) AKA Tank in Series
    Residence Time Distribution (RTD) model. [1]_

    .. math::

        E(t) = \\frac{1}{\\tau}\\left(\\frac{t}{\\tau}\\right)^{n-1}
        \\frac{n^n}{\\left(n-1\\right)!}
        \\text{exp}\\left[\\frac{-nt}{\\tau}\\right]

    Parameters
    ----------
    tau : scalar
        Mean residence time of **all** CSTRs. ``tau>0``
    n : scalar
        Number of CSTRs. Can be a real number ``n>0``
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
    >>> for n in [1, 2, 10]:
    ...     a = rtdpy.Ncstr(tau=1, n=n, dt=.01, time_end=3)
    ...     plt.plot(a.time, a.exitage, label="n={}".format(n))
    >>> plt.xlabel('Time')
    >>> plt.ylabel('Exit Age Function')
    >>> plt.legend()
    >>> plt.show()
    """

    def __init__(self, n, tau, dt, time_end):
        super().__init__(dt, time_end)
        self._n = None
        self._tau = None

        self.n = n
        self.tau = tau

    def _calc_exitage(self):
        """calculte exit age function"""
        try:
            output = (self.time / self.tau) ** (self.n - 1) / self.tau \
                * self.n ** self.n / special.gamma(self.n) \
                * np.exp(-self.time * self.n / self.tau)
        except (AttributeError, TypeError):
            output = None
        return output

    @property
    def n(self):
        """Number of CSTRS in series"""
        return self._n

    @n.setter
    def n(self, n):
        if n <= 0:
            raise RTDInputError("n less than zero")
        self._n = n
        self._exitage = self._calc_exitage()

    @property
    def tau(self):
        """Mean Residence Time of **all** tanks combined"""
        return self._tau

    @tau.setter
    def tau(self, tau):
        if tau <= 0:
            raise RTDInputError("tau less than zero")
        self._tau = tau
        self._exitage = self._calc_exitage()

    def __repr__(self):
        """Returns representation of object"""
        return ("Ncstr(n={}, tau={}, dt={}, time_end={})".format(
            self.n, self.tau, self.dt, self.time_end))
