"""Base RTD Class and Error."""
import numpy as np
from scipy.integrate import cumtrapz

from rtdpy.const import DTTOL


class RTDInputError(Exception):
    """Errors for RTD inputs."""
    pass


class RTD:
    """
    Base class for RTD analysis

    Child classes must implement:
        exitage
            The exitage function evaluated at each time point
    """
    def __init__(self, dt, time_end):
        if dt <= 0:
            raise RTDInputError
        self._dt = dt

        if time_end <= 0:
            raise RTDInputError
        self._time_end = time_end

        self._exitage = None

    @property
    def exitage(self):
        """Exit age distribution for RTD"""
        return self._exitage

    @property
    def exitage_norm(self):
        """Normalized Exit Age Distribtion for RTD"""
        return self.exitage / self.integral()

    @property
    def stepresponse(self):
        """Step respose of RTD"""
        return cumtrapz(self.exitage, self.time, initial=0)

    @property
    def stepresponse_norm(self):
        """Normalized step respose of RTD"""
        return cumtrapz(self.exitage_norm, self.time, initial=0)

    @property
    def dt(self):
        """Time step for RTD"""
        return self._dt

    @property
    def time_end(self):
        """Last time point for RTD"""
        return self._time_end

    @property
    def time(self):
        """
        Time points for exitage function.
        """
        return np.arange(0, self.time_end, self.dt)

    def integral(self):
        """
        Integral of RTD.
        """
        return np.trapz(self.exitage, self.time)

    def mrt(self):
        """
        Mean residence time of RTD.
        """
        return np.trapz(self.exitage * self.time, self.time)

    def sigma(self):
        """
        Variance of RTD.
        """
        tbar = self.mrt()
        return np.trapz(self.exitage*(self.time - tbar)**2, self.time)

    def output(self, inputtime, inputsignal):
        """
        Convolves input signal with RTD

        Parameters
        ----------
        inputtime : ndarray
            Times of input signal, which must have same `dt` as RTD.  Size m
        inputsignal : ndarray
            Input signal. Size n

        Returns
        -------
        outputsignal : ndarrary
            Output signal at same `dt`.  Size m + n -1
        """
        dt = np.diff(inputtime)
        udt = np.unique(dt)
        adt = np.average(dt)

        if (np.amax(udt) - np.amin(udt)) / adt > DTTOL:
            raise RTDInputError('input signal time does not have constant dt')

        if (adt-self.dt) / self.dt > DTTOL:
            print('time dt:' + str(adt))
            print('rtd dt:' + str(self.dt))
            raise RTDInputError('Cinput signal time dt does not match RTD dt')

        return np.convolve(inputsignal, self.exitage, mode='full') * self.dt

    def funnelplot(self, times, disturbances):
        """
        Return maximum output signal due to square disturbances.

        Uses method from [Garcia]_ .
        Also returns meshgrid for times and disturbance inputs
        for ease of plotting.

        Parameters
        ----------
        times : array_like, size m
            Times to determine funnelplot
        disturbances : array_like, size n
            Disturbance magnitudes

        Returns
        -------
        x : 2D meshgrid size (mxn)
            times
        y : 2D meshgrid size (mxn)
            disturbances
        response : 2D meshgrid size (mxn)
            maximum response at (x,y)

        References
        ----------
        .. [Garcia] Garcia-Munoz S., Butterbaugh A., Leavesley I.,
                    Manley L.F., Slade D., Bermingham S. (2018)
                    A flowhseet model for the development of a continuous process for
                    pharmaceutical tablets: An industrial perspective.
                    "AIChE Journal", 64(2), 511-525.
        """
        n = times.size
        m = disturbances.size

        response = np.zeros((m, n))
        for i, itime in enumerate(times):
            for j, jdisturbance in enumerate(disturbances):

                # input signal is a square disturbance of magnitude
                # jdisturbance and length itime
                inputsignal = np.zeros(self. time.size)
                inputsignal[self.time < itime] = jdisturbance

                # generate time stamps for generating output signal from RTD
                t = np.arange(0, self.time.size) * self.dt
                tmp = self.output(t, inputsignal)

                # store whichever deviation is largest
                if abs(np.amax(tmp)) > abs(np.amin(tmp)):
                    response[j, i] = np.amax(tmp)
                else:
                    response[j, i] = np.amin(tmp)

        x, y = np.meshgrid(times, disturbances)
        return x, y, response

    def frequencyresponse(self, omegas):
        """
        Parameters
        ----------
        omegas : ndarray
            frequencies at which to evaluate magnitude response

        Returns
        -------
        magnitude : ndarray
            frequency magnitude response at omegas
        """

        exitage = self.exitage
        series = np.arange(exitage.size)
        dt = self.dt
        mag = np.zeros(omegas.size)
        for i, omega in enumerate(omegas):
            mag[i] = dt * np.abs(
                np.sum(exitage * np.exp(-1 * 1j * series * omega * dt)))

        return mag
