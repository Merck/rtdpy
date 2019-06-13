"""PFR model."""

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

        if tau <= 0:
            raise RTDInputError("tau less than 0")
        if tau >= self.time[-1]:
            raise RTDInputError(
                "PFR lag is at or beyond end of supplied time")
        self._tau = tau

        self._exitage = self._calc_exitage()

    def _calc_exitage(self):
        """Calculate exitage."""

        a = np.zeros_like(self.time)
        idx = np.nonzero(self.time <= self.tau)
        idxfirst = idx[0][-1]
        if idxfirst == self.time.size:
            raise RTDInputError('PFR lag is at end of supplied time')

        a[idxfirst] = (self.time[idxfirst + 1] - self.tau) / self.dt / self.dt
        a[idxfirst + 1] = (self.tau - self.time[idxfirst]) / self.dt / self.dt
        return a

    @property
    def tau(self):
        """Tau. L/U"""
        return self._tau

    def __repr__(self):
        """Representation of object"""
        return ("Pfr(tau={}, dt={}, time_end={})".format(
            self.tau, self.dt, self.time_end))
