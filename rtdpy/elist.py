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
        """Elist model."""

        self._index = 0  # to make iterable

        self._validate_rtd(elist)
        dt = self._get_elist_dt(elist)
        time_end = self._get_elist_time_end(elist)

        super().__init__(dt=dt, time_end=time_end)

        self._elist = elist
        self._exitage = self._calc_exitage()

    @property
    def elist(self):
        """List of RTD objects."""
        return self._elist

    def _calc_exitage(self):
        """
        Create system exit age function.

        Loop all RTD models and convolve them together.
        Truncate length of exit age function to keep same time_end.
        """
        exitage = self.elist[0].exitage
        for item in self.elist[1:]:
            exitage = np.convolve(item.exitage, exitage) * self.dt
            exitage = exitage[:len(self.time) or None]
        return exitage

    @staticmethod
    def _validate_rtd(elist):
        """Validate that all models in elist are RTD models."""
        if any([not isinstance(item, RTD) for item in elist]):
            raise RTDInputError('item in list not an RTD class')

    @staticmethod
    def _get_elist_dt(elist):
        """Validate that all dts are the same and return dt."""
        dts = [item.dt for item in elist]
        if len(set(dts)) == 1:
            dt = dts[0]
        else:
            raise RTDInputError('RTDs have inconsistent dt in Elist')
        return dt

    @staticmethod
    def _get_elist_time_end(elist):
        """Validate that all time_ends are the same and return time_end."""

        time_ends = [item.time_end for item in elist]
        if len(set(time_ends)) == 1:
            time_end = time_ends[0]
        else:
            raise RTDInputError('RTDs have inconsistent time_end in Elist')
        return time_end

    def __iter__(self):
        """Enable iteration."""
        self._index = 0
        return self

    def __next__(self):
        """Implement iteration."""
        try:
            result = self.elist[self._index]
        except IndexError:
            raise StopIteration
        self._index += 1
        return result

    def __repr__(self):
        """Representation of object."""
        return ("Elist(elist={})".format(self.elist))
