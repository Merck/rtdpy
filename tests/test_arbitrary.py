import numpy as np
import pytest

import rtdpy as rtd

rtol = 1e-3
atol = 1e-5

DT = 0.005
TIME_END = 200


def test_failures():
    with pytest.raises(rtd.RTDInputError):
        rtd.Arbitrary(fun=1, dt=DT, time_end=TIME_END)


def test_arbitrary():
    ncstr_model = rtd.Ncstr(n=1, tau=10, dt=DT, time_end=TIME_END)
    def fun(t):
        return np.interp(t, ncstr_model.time, ncstr_model.exitage)
    arbitrary_model = rtd.Arbitrary(fun, dt=DT, time_end=TIME_END)

    assert(np.isclose(arbitrary_model.integral(), 1, rtol=rtol, atol=atol))
    assert(np.isclose(arbitrary_model.mrt(), 10, rtol=rtol, atol=atol))
    assert(np.isclose(arbitrary_model.sigma(), 100,
                      rtol=rtol, atol=atol))


def test_repr():
    ncstr_model = rtd.Ncstr(n=1, tau=10, dt=DT, time_end=TIME_END)
    def fun(t):
        return np.interp(t, ncstr_model.time, ncstr_model.exitage)
    a = rtd.Arbitrary(fun=fun, dt=DT, time_end=TIME_END)
    # object repr includes fun object and cannot be directly regenerated
    assert(repr(a))
