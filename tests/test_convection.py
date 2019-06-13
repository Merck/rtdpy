import numpy as np
import pytest

import rtdpy as rtd

rtol = 1e-3
atol = 1e-5

DT = 0.0025
TIME_END = 300


def analytical_mrt(tau):
    return tau

# only mrt has an analytical solution for E
# mrt doesn't have value for E* or E**
# variance does not a value for any

def test_failures():
    with pytest.raises(rtd.RTDInputError):
        rtd.Convection(tau=-1, dt=DT, time_end=TIME_END)
    with pytest.raises(rtd.RTDInputError):
        rtd.Convection(tau=1, dt=-1, time_end=TIME_END)
    with pytest.raises(rtd.RTDInputError):
        rtd.Convection(tau=1, dt=DT, time_end=-1)


@pytest.mark.parametrize("tau", [1, 1.5, 2, 10])
def test_convection(tau):
    """
    Test integral and MRT.

    Convection model requires a lot of precision for integral to converge.
    Convection model also requires a long time for mean to converge.
    """
    dt = tau/2000
    time_end = tau * 500
    a = rtd.Convection(tau=tau, dt=dt, time_end=time_end)
    assert(np.isclose(a.integral(), 1, rtol=rtol, atol=atol))
    assert(np.isclose(a.mrt(), analytical_mrt(tau), rtol=rtol, atol=atol))


def test_convection_points():
    """Manually test specific points for E, E*, and E**."""
    a = rtd.Convection(tau=1, dt=DT, time_end=TIME_END)

    times    =      [ 1/4,  1/2,    1,    2,     4]
    e_values =      [   0,    4,  1/2, 1/16, 1/128]     
    estar_values =  [   0,    2,  1/2,  1/8,  1/32]
    estar2_values = [   0,    1,  1/2,  1/4,   1/8]

    for t, e, estar, estar2 in zip(
            times, e_values, estar_values, estar2_values):
        assert np.isclose(np.interp(t, a.time, a.exitage), e)
        assert np.isclose(np.interp(t, a.time, a.exitage_star), estar)
        assert np.isclose(np.interp(t, a.time, a.exitage_star2), estar2)

@pytest.mark.parametrize("dt", [-1, 0])
def test_negative_dt_error(dt):
    with pytest.raises(rtd.RTDInputError):
        rtd.Convection(tau=1, dt=dt, time_end=1)


@pytest.mark.parametrize("time_end", [-1, 0])
def test_negative_time_end_error(time_end):
    with pytest.raises(rtd.RTDInputError):
        rtd.Convection(tau=1, dt=1, time_end=time_end)


@pytest.mark.parametrize("tau", [-1, 0])
def test_negative_tau_error(tau):
    with pytest.raises(rtd.RTDInputError):
        rtd.Convection(tau=tau, dt=1, time_end=1)


def test_repr():
    a = rtd.Convection(tau=1, dt=DT, time_end=TIME_END)
    b = eval("rtd."+repr(a))
    assert np.isclose(a.integral(), b.integral(), rtol=rtol, atol=atol)
    assert np.isclose(a.mrt(), b.mrt(), rtol=rtol, atol=atol)
    assert np.isclose(a.sigma(), b.sigma(), rtol=rtol, atol=atol)
