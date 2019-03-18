# rtdpy

Residence Time Distribution modeling in Python.

[https://merck.github.com/rtdpy](https://merck.github.com/rtdpy)

## A simple example
Create a family of tanks in series (N-CSTRs) and analyze them
```python
for n in [1, 2, 5, 10, 100]:
    a = rtdpy.Ncstr(tau=1, n=n, dt=.001, time_end=3)
    print(a.mrt())  # Mean Residence Time
    print(a.sigma()) # Variance
    plt.plot(a.time, a.exitage)
```

## Installation
```bash
pip install rtdpy
```
