import numpy as np
import pytest

import rtdpy as rtd

rtol = 1e-3
atol = 1e-5

DT = 0.005
TIME_END = 200


def analytical_mrt(tau):
    return tau


def analytical_sigma(n, tau):
    return tau ** 2 / n


def test_failures():
    with pytest.raises(rtd.RTDInputError):
        rtd.Ncstr(tau=-1, n=1, dt=DT, time_end=TIME_END)
    with pytest.raises(rtd.RTDInputError):
        rtd.Ncstr(tau=1, n=-1, dt=DT, time_end=TIME_END)
    with pytest.raises(rtd.RTDInputError):
        rtd.Ncstr(tau=1, n=1, dt=-1, time_end=TIME_END)
    with pytest.raises(rtd.RTDInputError):
        rtd.Ncstr(tau=1, n=1, dt=DT, time_end=-1)


@pytest.mark.parametrize("tau", [1, 1.5, 2, 10])
@pytest.mark.parametrize("n", [1, 1.5, 2, 10])
def test_ncstr(n, tau):
    a = rtd.Ncstr(n=n, tau=tau, dt=DT, time_end=TIME_END)
    assert(np.isclose(a.integral(), 1, rtol=rtol, atol=atol))
    assert(np.isclose(a.mrt(), analytical_mrt(tau), rtol=rtol, atol=atol))
    assert(np.isclose(a.sigma(), analytical_sigma(n, tau),
                      rtol=rtol, atol=atol))


@pytest.mark.parametrize("dt", [-1, 0])
def test_negative_dt_error(dt):
    with pytest.raises(rtd.RTDInputError):
        rtd.Ncstr(n=1, tau=1, dt=dt, time_end=1)


@pytest.mark.parametrize("time_end", [-1, 0])
def test_negative_time_end_error(time_end):
    with pytest.raises(rtd.RTDInputError):
        rtd.Ncstr(n=1, tau=1, dt=1, time_end=time_end)


@pytest.mark.parametrize("tau", [-1, 0])
def test_negative_tau_error(tau):
    with pytest.raises(rtd.RTDInputError):
        rtd.Ncstr(n=1, tau=tau, dt=1, time_end=1)


@pytest.mark.parametrize("n", [-1, 0])
def test_negative_n_error(n):
    with pytest.raises(rtd.RTDInputError):
        rtd.Ncstr(n=n, tau=1, dt=1, time_end=1)


def test_repr():
    a = rtd.Ncstr(n=2, tau=1, dt=DT, time_end=TIME_END)
    b = eval("rtd."+repr(a))
    assert np.isclose(a.integral(), b.integral(), rtol=rtol, atol=atol)
    assert np.isclose(a.mrt(), b.mrt(), rtol=rtol, atol=atol)
    assert np.isclose(a.sigma(), b.sigma(), rtol=rtol, atol=atol)
