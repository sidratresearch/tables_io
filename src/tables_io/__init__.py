"""tables_io is a library of functions for input, output and conversion of tabular data formats"""

try:
    from ._version import version
except:  # pylint: disable=bare-except   #pragma: no cover
    version = "unknown"

from .lazy_modules import *

from .table_dict import TableDict

from . import convert as conv

from . import io_utils

from .utils import concat_utils

from .utils import slice_utils

# Exposing the primary functions and interfaces for tables_io

convert_table = conv.conv_table.convertObj

convertObj = conv.conv_table.convertObj
"""This function is being deprecated, please see `convert_table` instead"""

convert = conv.conv_tabledict.convert

writeNative = io_utils.write.write_native
"""This function is being deprecated, please see `write_native` instead"""

write_native = io_utils.write.write_native

write = io_utils.write.write

readNative = io_utils.read.read_native
"""This function is being deprecated, please see `read_native` instead"""

read_native = io_utils.read.read_native

read = io_utils.read.read

io_open = io_utils.read.io_open

iterator_native = io_utils.iterator.iteratorNative

iteratorNative = io_utils.iterator.iteratorNative
"""This function is being deprecated, please see `iterator_native` instead"""

iterator = io_utils.iterator.iterator

concat_table = concat_utils.concatObjs

concatObjs = concat_utils.concatObjs
"""This function is being deprecated, please see `concat_table` instead"""

concat = concat_utils.concat
# TODO: Does this work on only single table or a table_dict?

slice_table = slice_utils.sliceObj

sliceObj = slice_utils.sliceObj
"""This function is being deprecated, please see `slice_table` instead"""

sliceObjs = slice_utils.sliceObjs
# TODO: Should this even exist?

check_columns = io_utils.read.check_columns
