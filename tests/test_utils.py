""" Unit tests for the fileIO module """

import sys
import unittest

import numpy as np
import pytest

from tables_io import types
from tables_io.utils import array_utils
from tables_io.lazy_modules import apTable, lazyImport, pd
from tests.helpers.utilities import check_deps


def test_check_deps():
    bad_module = lazyImport("this_does_not_exist")
    assert not check_deps([bad_module])


def test_array_length():
    """Test the pandas reading"""
    assert array_utils.array_length(4) == 0
    assert array_utils.array_length(np.ones(5)) == 5
    assert array_utils.array_length(np.ones((5, 5, 5))) == 5
    assert array_utils.array_length([3, 4, 4]) == 3


def test_force_to_pandasable():
    """Test the force_to_pandasable function"""
    rv = np.random.uniform(size=100)
    assert array_utils.force_to_pandables(4) == 4
    assert np.allclose(array_utils.force_to_pandables(rv), rv)
    try:
        array_utils.force_to_pandables(rv, 95)
    except ValueError:
        pass
    else:
        raise ValueError(
            "Failed to catch array length mismatch in arrayUtils.forceToPandables"
        )
    rv2d = rv.reshape(10, 10)
    rv2d_check = np.vstack(array_utils.force_to_pandables(rv2d))
    assert np.allclose(rv2d, rv2d_check)

    rv3d = rv.reshape(10, 2, 5)
    rv3d_check = np.vstack(array_utils.force_to_pandables(rv3d)).reshape(rv3d.shape)
    assert np.allclose(rv3d, rv3d_check)


def test_slice_dict():
    """Test the slice_dict method"""
    test_data = dict(
        scalar=np.random.uniform(size=10),
        vector=np.random.uniform(size=100).reshape(10, 10),
        mat=np.random.uniform(size=1000).reshape(10, 10, 10),
    )
    sliced = array_utils.slice_dict(test_data, 1)
    assert np.allclose(sliced["scalar"], test_data["scalar"][1])
    assert np.allclose(sliced["vector"], test_data["vector"][1])
    assert np.allclose(sliced["mat"], test_data["mat"][1])

    mask = np.zeros((10), bool)
    mask[1] = True
    mask[4] = True
    sliced = array_utils.slice_dict(test_data, mask)
    assert np.allclose(sliced["scalar"], test_data["scalar"][mask])
    assert np.allclose(sliced["vector"], test_data["vector"][mask])
    assert np.allclose(sliced["mat"], test_data["mat"][mask])


def test_print_dict_shape():
    """Test the print_dict_shape method"""
    test_data = dict(
        scalar=np.random.uniform(size=10),
        vector=np.random.uniform(size=100).reshape(10, 10),
        mat=np.random.uniform(size=1000).reshape(10, 10, 10),
    )
    array_utils.print_dict_shape(test_data)


def test_concatenateDicts():
    """Test the print_dict_shape method"""
    test_data = dict(
        scalar=np.random.uniform(size=10),
        vector=np.random.uniform(size=100).reshape(10, 10),
        mat=np.random.uniform(size=1000).reshape(10, 10, 10),
    )
    od = array_utils.concatenate_dicts([test_data, test_data])
    assert np.allclose(od["scalar"][0:10], test_data["scalar"])
    assert np.allclose(od["vector"][0:10], test_data["vector"])
    assert np.allclose(od["mat"][0:10], test_data["mat"])
    assert np.allclose(od["scalar"][10:], test_data["scalar"])
    assert np.allclose(od["vector"][10:], test_data["vector"])
    assert np.allclose(od["mat"][10:], test_data["mat"])


def test_getInit():
    test_data = dict(
        scalar=np.random.uniform(size=10),
        vector=np.random.uniform(size=100).reshape(10, 10),
        mat=np.random.uniform(size=1000).reshape(10, 10, 10),
    )

    dd = array_utils.get_initialization_for_ODict(test_data)
    assert dd["scalar"][0] == (10,)
    assert dd["vector"][0] == (10, 10)
    assert dd["mat"][0] == (10, 10, 10)
    dd = array_utils.get_initialization_for_ODict(test_data, 12)
    assert dd["scalar"][0] == (12,)
    assert dd["vector"][0] == (12, 10)
    assert dd["mat"][0] == (12, 10, 10)


def test_types():
    """Test the typing functions"""
    assert not types.is_table_like(4)
    assert types.is_table_like(dict(a=np.ones(4)))
    assert not types.is_table_like(dict(a=np.ones(4), b=np.ones(5)))
    assert not types.is_tabledict_like(4)
    assert not types.is_tabledict_like(dict(a=np.ones(4)))
    assert types.is_tabledict_like(dict(data=dict(a=np.ones(4))))
    try:
        types.file_type("xx.out")
    except KeyError:
        pass
    else:
        raise KeyError("Failed to catch unknown fileType")


@pytest.mark.skipif(not check_deps([apTable, pd]), reason="Missing an IO package")
def test_type_finders():
    """Test the utils that identify apTables and data frames"""
    import pandas as pd
    from astropy.table import Table

    class DataFrameSub(pd.DataFrame):
        pass

    class TableSub(Table):
        pass

    d1 = pd.DataFrame()
    d2 = DataFrameSub()
    t1 = Table()
    t2 = TableSub()

    assert types.is_dataframe(d1)
    assert types.is_dataframe(d2)
    assert not types.is_dataframe(t1)
    assert not types.is_dataframe(t2)
    assert not types.is_dataframe({})
    assert not types.is_dataframe(77)

    assert not types.is_ap_table(d1)
    assert not types.is_ap_table(d2)
    assert types.is_ap_table(t1)
    assert types.is_ap_table(t2)
    assert not types.is_ap_table({})
    assert not types.is_ap_table(77)


def test_lazy_load():
    """Test that the lazy import works"""
    noModule = lazyImport("thisModuleDoesnotExist")
    try:
        noModule.d
    except ImportError:
        pass
    else:
        raise ImportError("lazyImport failed")


@unittest.skipIf("wave" in sys.modules, "Wave module already imported")
def test_lazy_load2():
    """A second test that the lazy import works"""
    # I picked an obscure python module that is unlikely
    # to be loaded by anything else.

    wave = lazyImport("wave")
    # should not be loaded yet
    assert "wave" not in sys.modules

    # should trigger load
    assert "WAVE_FORMAT_PCM" in dir(wave)
    assert wave.sys == sys

    assert "wave" in sys.modules
