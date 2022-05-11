#!/usr/bin/env python3
from ctypes import sizeof, memmove, byref, c_ubyte, cast, POINTER


def write_into_ctype(ctype, bytevals):
    """
    Write bytes directly into an instance of a ctype.
    Copy byte values from bytevals into the current backing of
    the object. If the bytevals buffer is smaller than the size
    of the ctype, the write will be unsuccessful.
    """
    sizeof_self = sizeof(ctype)
    mutable_bytevals = bytearray(bytevals)
    backing_class = (c_ubyte * sizeof_self)

    # temporary backing that will hold the values
    temp_backing = backing_class.from_buffer(mutable_bytevals)
    memmove(byref(ctype), temp_backing, sizeof_self)


def cast_ctype_from_bytearray(ctype, byte_array, offset=0):
    """
    Cast ctype from bytearray. Modifications made to ctype instance
    will be observable in bytearray. If ctype is an instance
    of a ctype instead of the type itself, the type will be assumed
    to be of the same type as the instance, but modifications
    made to the instance `ctype` will not be observable in
    byte_array.
    """
    if not hasattr(ctype, '__bases__'):
        ctype = type(ctype)
    byte_array = bytearray(byte_array)
    memory = (c_ubyte*len(byte_array)).from_buffer(byte_array, offset)
    return cast(memory, POINTER(ctype)).contents
    # previous implementation was smaller, but could not effectively
    # perform casts on normal ctypes base types, e.g. c_uint32
    # return ((ctype*1).from_buffer(byte_array, offset))[0]


def ctype_struct_as_dict(ctype):
    """
    Return a dictionary representation of the given ctype
    instance
    """
    return {k: getattr(ctype, k) for k, v in ctype._fields_}


def is_zeroed_ctype(ctype):
    """
    Check if the provided ctype either has a size of 0 or
    contains only zeroes.
    """
    if sizeof(ctype) == 0:
        return True
    type_bytes = bytes(ctype)
    if len(set(type_bytes)) == 1 and type_bytes[0] == 0:
        return True
    return False


def get_non_zero_ctype_entries(ctype, byte_array, offset=0):
    """
    Get the entries of an array of structs/ctypes from the given
    bytearray that is known to end with a
    zeroed-out struct/ctype instance. Changes made to returned structs
    will reflect in the bytearray unless it is an instance of `bytes`
    """
    if not hasattr(ctype, '__bases__'):
        ctype = type(ctype)

    byte_array = bytearray(byte_array)
    table_entries = []
    while True:
        entry = cast_ctype_from_bytearray(ctype, byte_array, offset)
        offset += sizeof(entry)
        if is_zeroed_ctype(entry):
            break
        table_entries.append(entry)
    return table_entries


def copy_ctype(ctype):
    """
    Byte level copy constructor
    """
    sizeof_self = sizeof(ctype)
    new_backing_class = (c_ubyte * sizeof_self)
    new_backing = new_backing_class.from_buffer_copy(ctype)

    new_instance_ptr = cast(new_backing, POINTER(ctype.__class__))
    return new_instance_ptr.contents
