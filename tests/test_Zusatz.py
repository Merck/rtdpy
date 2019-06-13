import numpy as np
import pytest
from scipy import special

import rtdpy as rtd

rtol = 1e-3
atol = 1e-5

DT = 0.05
TIME_END = 60000


def mrt(b, c):
    return b * (c / (1 + c))**(-1 / c) * special.gamma((-1 + c) / c)


def sigma2(b, c):
    return b**2 * (c / (1 + c))**(-2 / c)\
            * (special.gamma((-2 + c) / c) - special.gamma((-1 + c) / c)**2)


# TODO: test inputs are in valid range


@pytest.mark.parametrize("b", [50, 100])
@pytest.mark.parametrize("c", [3, 5, 7])
def test1(b, c):
    a = rtd.Zusatz(b, c, dt=DT, time_end=TIME_END)
    assert(np.isclose(a.integral(), 1, rtol=rtol, atol=atol))
    assert(np.isclose(a.mrt(), mrt(b, c), rtol=rtol, atol=atol))
    assert(np.isclose(a.sigma(), sigma2(b, c), rtol=rtol*10, atol=atol))


def test_repr():
    a = rtd.Zusatz(b=50, c=5, dt=DT, time_end=TIME_END)
    b = eval("rtd."+repr(a))
    assert np.isclose(a.integral(), b.integral(), rtol=rtol, atol=atol)
    assert np.isclose(a.mrt(), b.mrt(), rtol=rtol, atol=atol)
    assert np.isclose(a.sigma(), b.sigma(), rtol=rtol, atol=atol)


@pytest.mark.parametrize("b", [-1, 0])
def test_negative_tau_error(b):
    with pytest.raises(rtd.RTDInputError):
        rtd.Zusatz(b=b, c=5, dt=1, time_end=1)


@pytest.mark.parametrize("c", [-1, 0])
def test_negative_n_error(c):
    with pytest.raises(rtd.RTDInputError):
        rtd.Zusatz(b=5, c=c, dt=1, time_end=1)
