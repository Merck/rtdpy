import numpy as np
import pytest

import rtdpy as rtd

rtol = 1e-3
atol = 1e-5

DT = 0.005
TIME_END = 200


def analytical_mrt(tau_cstr, tau_pfr):
    return tau_cstr + tau_pfr


def analytical_sigma(n, tau_cstr):
    return tau_cstr ** 2 / n


def test_fail_w_nonRTD():
    a = rtd.Ncstr(n=1, tau=1, dt=DT, time_end=TIME_END)
    with pytest.raises(rtd.RTDInputError):
        rtd.Elist([a, 'NCstr'])


def test_fail_w_dt():
    a = rtd.Ncstr(n=1, tau=1, dt=DT, time_end=TIME_END)
    b = rtd.Ncstr(n=1, tau=1, dt=DT*2, time_end=TIME_END)
    with pytest.raises(rtd.RTDInputError):
        rtd.Elist([a, b])


def test_fail_w_time_end():
    a = rtd.Ncstr(n=1, tau=1, dt=DT, time_end=TIME_END)
    b = rtd.Ncstr(n=1, tau=1, dt=DT, time_end=TIME_END*2)
    with pytest.raises(rtd.RTDInputError):
        rtd.Elist([a, b])


def test_iteration():
    a = rtd.Ncstr(n=1, tau=1, dt=DT, time_end=TIME_END)
    b = rtd.Pfr(tau=1, dt=DT, time_end=TIME_END)
    c = rtd.Elist([a, b])
    elist = [c, b, a]
    d = rtd.Elist(elist)
    for i, j in zip(elist, d):
        assert i == j


@pytest.mark.parametrize("tau_cstr", [10])
@pytest.mark.parametrize("tau_pfr", [1, 10, 50])
def test1(tau_cstr, tau_pfr):
    n = 1
    a = rtd.Ncstr(n=n, tau=tau_cstr, dt=DT, time_end=TIME_END)
    b = rtd.Pfr(tau=tau_pfr, dt=DT, time_end=TIME_END)
    c = rtd.Elist([a, b])
    assert len(c.time) == len(c.exitage)
    assert(np.isclose(c.integral(), 1, rtol=rtol, atol=atol))
    assert(np.isclose(c.mrt(),
                      analytical_mrt(tau_cstr=tau_cstr, tau_pfr=tau_pfr),
                      rtol=rtol, atol=atol))
    assert(np.isclose(c.sigma(), analytical_sigma(n=n, tau_cstr=tau_cstr),
                      rtol=rtol, atol=atol))


def test_listoflist():
    n = 1
    tau_cstr = 10
    tau_pfr = 1
    a = rtd.Ncstr(n=n, tau=tau_cstr, dt=DT, time_end=TIME_END)
    b = rtd.Pfr(tau=tau_pfr, dt=DT, time_end=TIME_END)
    c = rtd.Elist([a, b])
    d = rtd.Elist([c, c])
    assert len(d.time) == len(d.exitage)
    assert(np.isclose(d.integral(), 1, rtol=rtol, atol=atol))
    assert(np.isclose(d.mrt(), 22, rtol=rtol, atol=atol))
    assert(np.isclose(d.sigma(), 200, rtol=rtol, atol=atol))


@pytest.mark.parametrize("n", [10, 20, 30])
def test_lotsoflist_1(n):
    time_end = (n+1) * 10 + np.sqrt((n+1) * 10**2) * 4
    dt = DT
    E = []
    for i in range(n):
        E.append(rtd.Ncstr(n=1, tau=10, dt=dt, time_end=time_end))
    f = rtd.Elist(E)

    assert f.time.size == f.exitage.size
    assert np.isclose(f.integral(), 1, rtol=rtol*10, atol=atol)
    assert np.isclose(f.mrt(), (i+1) * 10, rtol=rtol*10, atol=atol)
    assert np.isclose(f.sigma(), (i+1) * 10 ** 2, rtol=rtol*10, atol=atol)


def test_repr():
    from rtdpy import Ncstr # noqa needed for eval of repr
    a1 = rtd.Ncstr(n=2, tau=1, dt=DT, time_end=TIME_END)
    a = rtd.Elist([a1, a1])
    b = eval("rtd."+repr(a))
    assert np.isclose(a.integral(), b.integral(), rtol=rtol, atol=atol)
    assert np.isclose(a.mrt(), b.mrt(), rtol=rtol, atol=atol)
    assert np.isclose(a.sigma(), b.sigma(), rtol=rtol, atol=atol)
