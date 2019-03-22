import numpy as np
import pytest

import rtdpy as rtd


rtol = 1e-3
atol = 1e-5

DT = 0.005
TIME_END = 200


def analytical_mrt(tau):
    return tau


def analytical_sigma():
    return 0


def test_failures():
    with pytest.raises(rtd.RTDInputError):
        rtd.Pfr(tau=-1, dt=DT, time_end=TIME_END)
    with pytest.raises(rtd.RTDInputError):
        rtd.Pfr(tau=1, dt=-1, time_end=TIME_END)
    with pytest.raises(rtd.RTDInputError):
        rtd.Pfr(tau=1, dt=DT, time_end=-1)


@pytest.mark.parametrize("tau", [1, 1.5, np.pi, 10])
def test1(tau):
    a = rtd.Pfr(tau=tau, dt=DT, time_end=TIME_END)
    assert(np.isclose(a.integral(), 1, rtol=rtol, atol=atol))
    assert(np.isclose(a.mrt(), analytical_mrt(tau), rtol=rtol, atol=atol))
    assert(np.isclose(a.sigma(), analytical_sigma(), rtol=rtol, atol=atol))


def test_endtau():
    with pytest.raises(rtd.RTDInputError):
        rtd.Pfr(200, dt=DT, time_end=TIME_END)


def test_repr():
    a = rtd.Pfr(tau=10, dt=DT, time_end=TIME_END)
    b = eval("rtd."+repr(a))
    assert np.isclose(a.integral(), b.integral(), rtol=rtol, atol=atol)
    assert np.isclose(a.mrt(), b.mrt(), rtol=rtol, atol=atol)
    assert np.isclose(a.sigma(), b.sigma(), rtol=rtol, atol=atol)
