# rtdpy

Residence Time Distribution modeling in Python.

[https://merck.github.com/rtdpy](https://merck.github.com/rtdpy)

[![DOI](https://joss.theoj.org/papers/10.21105/joss.01621/status.svg)](https://doi.org/10.21105/joss.01621)

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
Tests are written using `pytest`. `numpy` and `scipy` must also be installed in the environment if using `pytest` directly. `tox` can also be used to test against Python versions 3.5, 3.6, and 3.7. See [pytest documentation](https://docs.pytest.org/en/latest/) for how to use and interpret pytest results.

It is recommended to use a virtual environment for developing/testing.

```bash
git clone https://github.com/Merck/rtdpy.git  # or use your forked repo
cd rtdpy
python3 -m venv .venv
source .venv/bin/activate
pip install -e .  # will also install numpy and scipy dependencies
pip install pytest tox

# run all tests
pytest

# run tests and style check for Python versions 3.5, 3.6, and 3.7, if available.
tox
```

Author: Matthew Flamm

Email: <matthew.flamm@merck.com>
