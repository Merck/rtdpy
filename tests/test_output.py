import numpy as np
import pytest

import rtdpy

rtol = 1e-3
atol = 1e-3

DT = 0.005
TIME_END = 200


def test_fail_nonconstant_dt():
    a = rtdpy.Ncstr(n=1, tau=10, dt=DT, time_end=TIME_END)
    inputtime = a.time
    inputtime[-1] = inputtime[-1] + DT
    inputsignal = np.zeros(inputtime.size)
    inputsignal[inputtime > 10] = 1
    with pytest.raises(rtdpy.RTDInputError):
        a.output(inputtime, inputsignal)


def test_fail_nonmatching_dt():
    a = rtdpy.Ncstr(n=1, tau=10, dt=DT, time_end=TIME_END)
    inputtime = a.time * 10
    inputsignal = np.zeros(inputtime.size)
    inputsignal[inputtime > 10] = 1
    with pytest.raises(rtdpy.RTDInputError):
        a.output(inputtime, inputsignal)


def test_step_output():
    # test that a CSTR convolved with a step input signal
    # is the same as a CSTR+PFR stepresponse
    a = rtdpy.Ncstr(n=1, tau=10, dt=DT, time_end=TIME_END)
    b = rtdpy.Pfr(tau=10, dt=DT, time_end=TIME_END)
    c = rtdpy.Elist([a, b])

    inputtime = a.time
    inputsignal = np.zeros(inputtime.size)
    inputsignal[inputtime > 10] = 1

    outputsignal = a.output(inputtime, inputsignal)[:inputtime.size]

    assert np.allclose(outputsignal, c.stepresponse, rtol=rtol, atol=atol)
