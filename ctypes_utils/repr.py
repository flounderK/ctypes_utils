#!/usr/bin/env python3

import _ctypes
import enum


class NiceHexFieldRepr:
    """
    Class to insert a readable and customizeable repr for
    subclasses
    """
    def __repr__(self):
        repr_map = None
        if hasattr(self, '__repr_map__'):
            repr_map = self.__repr_map__

        ret = []
        for x in self._fields_:
            k, v = x[:2]
            attr = getattr(self, k)
            if repr_map is not None and k in repr_map.keys():
                rep_func = repr_map.get(k)
                ret.append("%s: %s" % (k, rep_func(attr)))
            elif issubclass(v, _ctypes._SimpleCData):
                ret.append("%s: %#x" % (k, attr))
            else:
                ret.append("%s: %s" % (k, bytes(attr)))
        return "\n".join(ret)


def gen_enum_flags_repr(enum_flag_class):
    """
    Generate a repr function that will display human readable
    enum flag values. Useful in __repr_map__ fields
    """
    def inner(attr_val):
        members, uncovered = enum._decompose(enum_flag_class, attr_val)
        member_repr = '|'.join([i.name for i in members])
        rep = "%s: %#x" % (member_repr, attr_val)
        return rep
    return inner
