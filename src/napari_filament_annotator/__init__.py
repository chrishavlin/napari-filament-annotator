try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

from ._sample_data import load_sample_image
from ._widget import Annotator
from ._writer import write_multiple, write_single_image

__all__ = (
    "write_single_image",
    "write_multiple",
    "load_sample_image",
    "Annotator",
)
