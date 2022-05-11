#!/usr/bin/env python3
import sys
from ctypes import Array, Structure, Union

_array_type = type(Array)


# borrowed from ctypes  to force unions nested within
# non-native endian structs to work correctly
def _other_endian(typ):
    """Return the type with the 'other' byte order.  Simple types like
    c_int and so on already have __ctype_be__ and __ctype_le__
    attributes which contain the types, for more complicated types
    arrays and structures are supported.
    """
    # check _OTHER_ENDIAN attribute (present if typ is primitive type)
    if hasattr(typ, _OTHER_ENDIAN):
        return getattr(typ, _OTHER_ENDIAN)
    # if typ is array
    if isinstance(typ, _array_type):
        return _other_endian(typ._type_) * typ._length_
    # if typ is structure
    if issubclass(typ, Structure):
        return typ

    if issubclass(typ, Union):
        return typ
    raise TypeError("This type does not support other endian: %s" % typ)


class _swapped_meta(type(Structure), type(Union)):
    def __setattr__(self, attrname, value):
        if attrname == "_fields_":
            fields = []
            for desc in value:
                name = desc[0]
                typ = desc[1]
                rest = desc[2:]
                fields.append((name, _other_endian(typ)) + rest)
            value = fields
        super().__setattr__(attrname, value)


################################################################

# Note: The Structure metaclass checks for the *presence* (not the
# value!) of a _swapped_bytes_ attribute to determine the bit order in
# structures containing bit fields.

if sys.byteorder == "little":
    _OTHER_ENDIAN = "__ctype_be__"

    LittleEndianStructure = Structure

    class BigEndianStructure(Structure, metaclass=_swapped_meta):
        """Structure with big endian byte order"""
        __slots__ = ()
        _swappedbytes_ = None

    NonNativeStructure = BigEndianStructure

elif sys.byteorder == "big":
    _OTHER_ENDIAN = "__ctype_le__"

    BigEndianStructure = Structure

    class LittleEndianStructure(Structure, metaclass=_swapped_meta):
        """Structure with little endian byte order"""
        __slots__ = ()
        _swappedbytes_ = None

    NonNativeStructure = LittleEndianStructure

from .byte_manipulation import write_into_ctype, cast_ctype_from_bytearray, ctype_struct_as_dict, is_zeroed_ctype, get_non_zero_ctype_entries, copy_ctype
from .repr import NiceHexFieldRepr
