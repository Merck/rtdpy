import numpy as np
import pytest

import rtdpy as rtd


rtol = 1e-3
atol = 1e-5

DT = 0.001
TIME_END = 10


def analytic_mrt(tau):
    return tau


def analytic_sigma2(tau, pe):
    return tau**2*(2/pe-2/pe**2*(1-np.exp(-pe)))


def test_failures():
    with pytest.raises(rtd.RTDInputError):
        rtd.AD_cc(tau=-1, peclet=1, dt=DT, time_end=TIME_END)
    with pytest.raises(rtd.RTDInputError):
        rtd.AD_cc(tau=1, peclet=-1, dt=DT, time_end=TIME_END)
    with pytest.raises(rtd.RTDInputError):
        rtd.AD_cc(tau=1, peclet=1, dt=-1, time_end=TIME_END)
    with pytest.raises(rtd.RTDInputError):
        rtd.AD_cc(tau=1, peclet=1, dt=DT, time_end=-1)


@pytest.mark.parametrize("tau", [1, 1.5])
def test_tau(tau):
    pecletr = 100
    a = rtd.AD_cc(tau=tau, peclet=pecletr, dt=DT, time_end=TIME_END)
    assert(np.isclose(a.integral(), 1, rtol=rtol, atol=atol))
    assert(np.isclose(a.mrt(), analytic_mrt(tau), rtol=rtol*10, atol=atol))
    assert(np.isclose(a.sigma(), analytic_sigma2(tau, pecletr),
                      rtol=rtol*10, atol=atol))


@pytest.mark.parametrize("pecletr", [0.1, 1, 10, 100])
def test_pecletr(pecletr):
    tau = 1
    a = rtd.AD_cc(tau=tau, peclet=pecletr, dt=DT, time_end=TIME_END)
    assert(np.isclose(a.integral(), 1, rtol=rtol, atol=atol))
    assert(np.isclose(a.mrt(), analytic_mrt(tau), rtol=rtol*10, atol=atol))
    assert(np.isclose(a.sigma(), analytic_sigma2(tau, pecletr),
                      rtol=rtol*10, atol=atol))


@pytest.mark.xfail
@pytest.mark.parametrize("pecletr", [1000])
def test_high_pecletr_default(pecletr):
    tau = 1
    a = rtd.AD_cc(tau=tau, peclet=pecletr, dt=DT, time_end=TIME_END)
    assert(np.isclose(a.integral(), 1, rtol=rtol, atol=atol))
    assert(np.isclose(a.mrt(), analytic_mrt(tau), rtol=rtol*10, atol=atol))
    assert(np.isclose(a.sigma(), analytic_sigma2(tau, pecletr),
                      rtol=rtol*10, atol=atol))


@pytest.mark.parametrize("pecletr", [1000])
def test_high_pecletr_adjusted(pecletr):
    tau = 1
    nx = 300
    a = rtd.AD_cc(tau=tau, peclet=pecletr, dt=DT, time_end=TIME_END, nx=nx)
    assert(np.isclose(a.integral(), 1, rtol=rtol, atol=atol))
    assert(np.isclose(a.mrt(), analytic_mrt(tau), rtol=rtol*10, atol=atol))
    assert(np.isclose(a.sigma(), analytic_sigma2(tau, pecletr),
                      rtol=rtol*10, atol=atol))


@pytest.mark.parametrize("pecletr", [1])
def test_low_pecletr(pecletr):
    tau = 1
    time_end = 20
    a = rtd.AD_cc(tau=tau, peclet=pecletr, dt=DT, time_end=time_end)
    assert(np.isclose(a.integral(), 1, rtol=rtol*1, atol=atol*10))
    assert(np.isclose(a.mrt(), analytic_mrt(tau), rtol=rtol*10, atol=atol))
    assert(np.isclose(a.sigma(), analytic_sigma2(tau, pecletr),
                      rtol=rtol*10, atol=atol))


def test_repr():
    a = rtd.AD_cc(tau=1, peclet=100, dt=DT, time_end=TIME_END)
    b = eval("rtd."+repr(a))
    assert np.isclose(a.integral(), b.integral(), rtol=rtol, atol=atol)
    assert np.isclose(a.mrt(), b.mrt(), rtol=rtol, atol=atol)
    assert np.isclose(a.sigma(), b.sigma(), rtol=rtol, atol=atol)
