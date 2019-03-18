import numpy as np
import pytest

import rtdpy

rtol = 1e-3
atol = 1e-5

DT = 0.005
TIME_END = 200


def test_exitage_norm():
    a = rtdpy.Ncstr(n=1, tau=1, dt=DT, time_end=TIME_END)
    assert np.allclose(a.exitage_norm, a.exitage, rtol=rtol, atol=atol)


def test_exitage_norm_clipped():
    a = rtdpy.Ncstr(n=1, tau=1, dt=DT, time_end=2)
    assert not np.isclose(a.integral(), 1, rtol=rtol, atol=atol)
    assert np.isclose(np.trapz(a.exitage_norm, a.time), 1,
                      rtol=rtol, atol=atol)


@pytest.mark.parametrize("tau", [0.5, 5])
@pytest.mark.parametrize("n", [1, 2, 10])
def test_frequency_response(tau, n):
    def analytical_response(tau, n, omegas):
        return 1 / np.sqrt(1 + (omegas * tau / n)**2)**n

    a = rtdpy.Ncstr(tau=tau, n=n, dt=.001, time_end=100)
    omegas = np.logspace(-2, 2, 100)
    mag = a.frequencyresponse(omegas)

    assert np.allclose(mag, analytical_response(tau, n, omegas),
                       rtol=rtol, atol=atol)


def test_funnelplot():
    a = rtdpy.Ncstr(tau=1, n=1, dt=.001, time_end=10)
    x, y, response = a.funnelplot(times=np.array([1]), disturbances=np.array([1]))
    x2, y2 = np.meshgrid([1], [1])
    assert x == x2
    assert y == y2

    inputtime = a.time
    inputsignal = np.zeros(inputtime.size)
    inputsignal[inputtime < 1] = 1

    outputsignal = a.output(inputtime, inputsignal)

    assert response[0, 0] == np.amax(outputsignal)
