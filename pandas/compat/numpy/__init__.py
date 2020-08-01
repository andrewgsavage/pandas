""" support numpy compatibility across versions """

from distutils.version import LooseVersion
import re

import numpy as np

from pandas.core.dtypes.common import is_extension_array_dtype

# numpy versioning
_np_version = np.__version__
_nlv = LooseVersion(_np_version)
_np_version_under1p16 = _nlv < LooseVersion("1.16")
_np_version_under1p17 = _nlv < LooseVersion("1.17")
_np_version_under1p18 = _nlv < LooseVersion("1.18")
_np_version_under1p19 = _nlv < LooseVersion("1.19")
_np_version_under1p20 = _nlv < LooseVersion("1.20")
_is_numpy_dev = ".dev" in str(_nlv)


if _nlv < "1.15.4":
    raise ImportError(
        "this version of pandas is incompatible with numpy < 1.15.4\n"
        f"your numpy version is {_np_version}.\n"
        "Please upgrade numpy to >= 1.15.4 to use this pandas version"
    )


_tz_regex = re.compile("[+-]0000$")


def tz_replacer(s):
    if isinstance(s, str):
        if s.endswith("Z"):
            s = s[:-1]
        elif _tz_regex.search(s):
            s = s[:-5]
    return s


def np_datetime64_compat(s, *args, **kwargs):
    """
    provide compat for construction of strings to numpy datetime64's with
    tz-changes in 1.11 that make '2015-01-01 09:00:00Z' show a deprecation
    warning, when need to pass '2015-01-01 09:00:00'
    """
    s = tz_replacer(s)
    return np.datetime64(s, *args, **kwargs)


def np_array_datetime64_compat(arr, *args, **kwargs):
    """
    provide compat for construction of an array of strings to a
    np.array(..., dtype=np.datetime64(..))
    tz-changes in 1.11 that make '2015-01-01 09:00:00Z' show a deprecation
    warning, when need to pass '2015-01-01 09:00:00'
    """
    # is_list_like
    if hasattr(arr, "__iter__") and not isinstance(arr, (str, bytes)):
        arr = [tz_replacer(s) for s in arr]
    else:
        arr = tz_replacer(arr)

    return np.array(arr, *args, **kwargs)


def np_issubclass_compat(unique_dtype, dtypes_set):
    if (issubclass(unique_dtype.type, tuple(dtypes_set))  # type: ignore
        or (
            np.number in dtypes_set
            and is_extension_array_dtype(unique_dtype)
            and unique_dtype._is_numeric
    )):
        return True
    return False

__all__ = [
    "np",
    "_np_version",
    "_np_version_under1p16",
    "_np_version_under1p17",
    "_is_numpy_dev",
]
