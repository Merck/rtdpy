# rtdpy

Residence Time Distribution modeling in Python.

[https://merck.github.com/rtdpy](https://merck.github.com/rtdpy)

## A simple example
Create a family of tanks in series (N-CSTRs) and analyze them
```python
for n in [1, 2, 5, 10, 100]:
    a = rtdpy.Ncstr(tau=1, n=n, dt=.001, time_end=5)
    plt.plot(a.time, a.exitage, label="n={}".format(n))
plt.legend()
plt.xlabel('Time')
plt.ylabel('Exit Age Function')
plt.title('Impulse Responses')
```

![N-Cstr RTDs](images/ncstr.png?raw=true "N-Cstr RTDs")

## Installation
```bash
pip install rtdpy
```

Author: Matthew Flamm

Email: <matthew.flamm@merck.com>

