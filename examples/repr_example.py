#!/usr/bin/env python3
import ctypes
import ctypes_utils
from ctypes_utils import NiceHexFieldRepr
from ctypes import c_uint32, c_uint8, BigEndianStructure
import enum


class NTPMode(enum.IntEnum):
    MODE_UNSPEC = 0
    MODE_ACTIVE = 1
    MODE_PASSIVE = 2
    MODE_CLIENT = 3
    MODE_SERVER = 4
    MODE_BROADCAST = 5
    MODE_CONTROL = 6
    MODE_PRIVATE = 7


class NTPLeap(enum.IntEnum):
    LEAP_NOWARNING = 0x0
    LEAP_ADDSECOND = 0x1
    LEAP_DELSECOND = 0x2
    LEAP_NOTINSYNC = 0x3


class NTPPacket(BigEndianStructure, NiceHexFieldRepr):
    __packed__ = True
    _fields_ = [
        ("leap_indicator", c_uint8, 2),
        ("version_number", c_uint8, 3),
        ("mode", c_uint8, 3),
        ("stratum", c_uint8),
        ("poll", c_uint8),
        ("precision", c_uint8),
        ("rootDelay", c_uint32),
        ("rootDispersion", c_uint32),
        ("refId", c_uint32),
        ("refTm_s", c_uint32),
        ("refTm_f", c_uint32),
        ("origTm_s", c_uint32),
        ("origTm_f", c_uint32),
        ("rxTm_s", c_uint32),
        ("rxTm_f", c_uint32),
        ("txTm_s", c_uint32),
        ("txTm_f", c_uint32),
    ]
    __repr_map__ = {
        "leap_indicator": lambda a: NTPLeap(a).name,
        "mode": lambda a: NTPMode(a).name
    }


bytevals = bytearray(bytes.fromhex('d30203fa00010000000100000000' + ('00'*8)*3 + '00'*6 + 'deadbeef'))
packet = NTPPacket()
ctypes_utils.write_into_ctype(packet, bytevals)

print(packet)

print(bytevals)
