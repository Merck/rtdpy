import numpy as np
import pytest

import rtdpy as rtd

rtol = 1e-3
atol = 1e-5

DT = 0.001
TIME_END = 200


def analytic_mrt(tau):
    return tau


def analytic_sigma2(tau, peclet):
    return tau**2 * 2. / peclet


def test_failures():
    with pytest.raises(rtd.RTDInputError):
        rtd.AD_hi_peclet(tau=-1, peclet=1, dt=DT, time_end=TIME_END)
    with pytest.raises(rtd.RTDInputError):
        rtd.AD_hi_peclet(tau=1, peclet=-1, dt=DT, time_end=TIME_END)
    with pytest.raises(rtd.RTDInputError):
        rtd.AD_hi_peclet(tau=1, peclet=1, dt=-1, time_end=TIME_END)
    with pytest.raises(rtd.RTDInputError):
        rtd.AD_hi_peclet(tau=1, peclet=1, dt=DT, time_end=-1)


@pytest.mark.parametrize("peclet", [100, 1000])
@pytest.mark.parametrize("tau", [1, 10])
def test1(tau, peclet):
    a = rtd.AD_hi_peclet(tau=tau, peclet=peclet, dt=DT, time_end=TIME_END)
    assert(np.isclose(a.integral(), 1, rtol=rtol, atol=atol))
    assert(np.isclose(a.mrt(), analytic_mrt(tau),
                      rtol=rtol, atol=atol))
    assert(np.isclose(a.sigma(), analytic_sigma2(tau, peclet),
                      rtol=rtol, atol=atol))


@pytest.mark.parametrize("peclet", [200, 1000])
def test_AD_equivalence(peclet):
    # closed-closed and open-open are approximately equal at high peclet
    # starting around Pe=100
    time_end = 10
    dt = .001
    tau = 1
    nx = 300

    a = rtd.AD_cc(tau=tau, peclet=peclet, dt=dt, time_end=time_end, nx=nx)
    b = rtd.AD_hi_peclet(tau=tau, peclet=peclet, dt=dt, time_end=time_end)
    c = rtd.AD_hi_peclet(tau=tau, peclet=peclet, dt=dt, time_end=time_end)

    assert(np.isclose(a.integral(), b.integral(), rtol=rtol, atol=atol))
    assert(np.isclose(a.mrt(), b.mrt(), rtol=1e-2, atol=atol))
    assert(np.isclose(a.sigma(), b.sigma(), rtol=5e-2, atol=atol))

    assert(np.isclose(a.integral(), c.integral(), rtol=rtol, atol=atol))
    assert(np.isclose(a.mrt(), c.mrt(), rtol=1e-2, atol=atol))
    assert(np.isclose(a.sigma(), c.sigma(), rtol=5e-2, atol=atol))


def test_repr():
    a = rtd.AD_hi_peclet(tau=1, peclet=100, dt=DT, time_end=TIME_END)
    b = eval("rtd."+repr(a))
    assert np.isclose(a.integral(), b.integral(), rtol=rtol, atol=atol)
    assert np.isclose(a.mrt(), b.mrt(), rtol=rtol, atol=atol)
    assert np.isclose(a.sigma(), b.sigma(), rtol=rtol, atol=atol)
