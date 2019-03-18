import numpy as np

from rtdpy.rtd import RTD, RTDInputError


class Elist(RTD):
    """
    Create RTD model from a list of Rtd objects.  Combinations of models
    are convolved together. [1]_

    Parameters
    ----------
        elist : list
            List of Rtd objects.
            All objects must have same `dt` and `time_end`.

    References
    ----------
    .. [1] Levenspiel O. (1999) "Chemical Reaction Engineering: Third Edition"
           John Wiley & Sons, Inc.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> import rtdpy
    >>> a = rtdpy.Ncstr(tau=1, n=1, dt=.01, time_end=15)
    >>> b = rtdpy.Pfr(tau=10, dt=.01, time_end=15)
    >>> c = rtdpy.Elist([a, b])
    >>> plt.plot(a.time, a.exitage, label="CSTR")
    >>> plt.plot(b.time, b.exitage, label="PFR")
    >>> plt.ylim(0, 1.1)
    >>> plt.title('Original RTD models')
    >>> plt.xlabel('Time')
    >>> plt.ylabel('Exit Age Function')
    >>> plt.legend()
    >>> plt.figure()
    >>> plt.plot(c.time, c.exitage)
    >>> plt.xlabel('Time')
    >>> plt.ylabel('Exit Age Function')
    >>> plt.title('Combination of models')
    >>> plt.show()
    """

    def __init__(self, elist):
        self._index = 0
        self._elist = None

        dt = self.get_elist_dt(elist)

        time_end = self.get_elist_time_end(elist)

        super().__init__(dt=dt, time_end=time_end)

        self.elist = elist

    @property
    def elist(self):
        return self._elist

    @elist.setter
    def elist(self, elist):

        self._elist = elist

        exitage = self.elist[0].exitage
        for idx, item in enumerate(self._elist[1:]):
            exitage = np.convolve(item.exitage, exitage) * self.dt
            exitage = exitage[:len(self.time) or None]
        self._exitage = exitage

    @staticmethod
    def get_elist_dt(elist):

        if any([not isinstance(item, RTD) for item in elist]):
            raise RTDInputError('item in list not an RTD class')

        dts = [item.dt for item in elist]
        if len(set(dts)) == 1:
            dt = dts[0]
        else:
            raise RTDInputError('RTDs have inconsistent dt in Elist')
        return dt

    @staticmethod
    def get_elist_time_end(elist):

        if any([not isinstance(item, RTD) for item in elist]):
            raise RTDInputError('item in list not an RTD class')

        time_ends = [item.time_end for item in elist]
        if len(set(time_ends)) == 1:
            time_end = time_ends[0]
        else:
            raise RTDInputError('RTDs have inconsistent dt in Elist')
        return time_end

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        try:
            result = self.elist[self._index]
        except IndexError:
            raise StopIteration
        self._index += 1
        return result
