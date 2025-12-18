"""init file for rtdpy"""
from .arbitrary import Arbitrary
from .ncstr import Ncstr
from .pfr import Pfr
from .ad_oo import AD_oo
from .elist import Elist
from .zusatz import Zusatz
from .ad_cc import AD_cc
from .ad_hi_peclet import AD_hi_peclet
from .convection import Convection
from .rtd import RTDInputError, RTD

try:
    from ._version import __version__
except ImportError:
    __version__ = "unknown"
