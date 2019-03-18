import numpy as np

from rtdpy.rtd import RTD, RTDInputError


class Pfr(RTD):
    """
    Create Plug Flow Reactor (PFR) Residence Time Distribution (RTD) model.
    [1]_

    .. math::

        E(t) = \\delta\\left(t-\\tau\\right)

    Parameters
    ----------
    tau : scalar
        Mean residence time of PFR. ``tau>0``
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
    >>> a = rtdpy.Pfr(tau=1, dt=.01, time_end=3)
    >>> plt.plot(a.time, a.exitage)
    >>> plt.xlabel('Time')
    >>> plt.ylabel('Exit Age Function')
    >>> plt.show()
    """
    def __init__(self, tau, dt, time_end):
        super().__init__(dt, time_end)
        self._tau = None
        self._exitage = None

        self.tau = tau

    def _calc_exitage(self):
        try:
            t = self.time
            if self.tau >= self.time[-1]:
                raise RTDInputError(
                    'PFR lag is at or beyond end of supplied time')

            a = np.zeros(t.size)
            idx = np.nonzero(t <= self.tau)
            idxfirst = idx[0][-1]
            if idxfirst == t.size:
                raise RTDInputError('PFR lag is at end of supplied time')

            a[idxfirst] = (t[idxfirst + 1] - self.tau) / self.dt / self.dt
            a[idxfirst + 1] = (self.tau - t[idxfirst]) / self.dt / self.dt

            output = a
        except AttributeError:
            output = None
        return output

    @property
    def tau(self):
        return self._tau

    @tau.setter
    def tau(self, tau):
        if tau <= 0:
            raise RTDInputError("tau less than 0")
        self._tau = tau
        self._exitage = self._calc_exitage()
