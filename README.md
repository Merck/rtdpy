# rtdpy

Residence Time Distribution modeling in Python.

[https://merck.github.com/rtdpy](https://merck.github.com/rtdpy)

## A simple example
Create a family of tanks in series (N-CSTRs) and analyze them
```python
import matplotlib.pyplot as plt
import rtdpy
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

## Issues/Requests/Contributions
See [CONTRIBUTING.md](CONTRIBUTING.md)

## Testing
Tests are written using `pytest`. `numpy` and `scipy` must also be installed in the environment if using `pytest` directly. `tox` can also be used to test against Python versions 3.5, 3.6, and 3.7.

It is recommended to use a virtual environment for developing/testing:

```bash
cd rtdpy_repo_path
python3 -m venv .venv
source .venv/bin/activate
pip install numpy scipy pytest

# run all tests
pytest
```

Author: Matthew Flamm

Email: <matthew.flamm@merck.com>
