# Contributing guidelines

Any contributions including bug reports, feature requests, additional RTD models,
additional RTD analysis functionality, documentation clarification, etc. are welome.

Bug reports and feature requests can be placed in
[Issues](https://github.com/Merck/rtdpy/issues). For bug reports, please provide
code examples, error messages, and version information about numpy, scipy,
rtdpy, and Python.  PRs for code contributions can be made
[here](https://github.com/Merck/rtdpy/pulls).

```python
import sys, scipy, numpy, rtdpy
print(scipy.__version__, numpy.__version__, rtdpy.__version__, sys.version_info)
```

## Implementing a new RTD model

See [NCstr model](https://github.com/Merck/rtdpy/blob/main/rtdpy/ncstr.py)
for a simple example.

* The base RTD class should be inherited, i.e. `class NewRTD(RTD):`. The RTD
  class `__init__` method should be called first to setup the time attributes.
* Input parameters should be checked for bounds, e.g. the number of tanks in
  NCstr is required to be greater than 0.  Invalid inputs should raise
  `RTDInputError`.
* Input parameters should be accessible via a method decorated with property.
* A `__repr__` method should be defined to allow for easy inspection of models.

## Implementing a new RTD analysis functionality

* The new functionality should be a method of the base RTD class. This allows all
  functionality to be available for all RTD models.
* Only instance attribute/methods defined in the base RTD class should be accessed
  by methods in the base RTD class.

## Documentation changes/additions/deletions

* All API documentation is done in the class/method docstrings.
* The tutorial documentation is written in
  [index.rst](https://github.com/Merck/rtdpy/blob/main/source/index.rst).
* The requirements for building the documentation with sphinx are in
  requirements_docs.txt.
