"""Slicing functions for tables_io"""

from collections import OrderedDict


from .array_utils import slice_dict
from ..types import NUMPY_DICT, table_type


# I F. Generic `slice`
def slice_obj(obj, the_slice):
    """
    Slice a `table-like` objects

    Parameters
    ----------
    obj :  `table_like`
        Table like object to slice

    the_slice: `slice`
        Slice to make

    Returns
    -------
    tab : `table-like`
        The slice of the table
    """
    tType = table_type(obj)
    if tType is NUMPY_DICT:
        return slice_dict(obj, the_slice)
    return obj[the_slice]


def slice_objs(odict, the_slice):
    """Slice many `table-like` objects

    Parameters
    ----------
    odict :  `table_like`
       Objects to slice

    the_slice: `slice`
        Slice to make


    Returns
    -------
    odict : tableDict-like
        The sliced tables
    """
    return OrderedDict([(k, slice_obj(v, the_slice)) for k, v in odict.items()])
