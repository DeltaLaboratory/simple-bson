import warnings

class TypeSignature:
    double = b"\0x01"
    string = b"\0x02"
    document = b"\0x03"
    array = b"\0x04"
    binary = b"\0x05"
    bool = b"\0x08"
    null = b"\0x0A"
    int32 = b"\0x10"
    uint64 = b"\0x11"
    int64 = b"\0x12"


class EncodeError(Exception):
    pass


class DecodeError(Exception):
    pass


def dummy_function(text: str):
    warnings.warn(f"call {text} directly will ignored.", Warning)
