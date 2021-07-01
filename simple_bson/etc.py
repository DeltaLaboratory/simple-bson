import warnings


class TypeSignature:
    double = b"\x01"
    string = b"\x02"
    document = b"\x03"
    array = b"\x04"
    binary = b"\x05"
    bool = b"\x08"
    null = b"\x0A"
    int32 = b"\x10"
    uint64 = b"\x11"
    int64 = b"\x12"


class EncodeError(Exception):
    pass


class DecodeError(Exception):
    pass


def dummy_function(text: str):
    warnings.warn(f"call {text} directly will ignored.", Warning)


def get_data_and_view(data):
    if isinstance(data, (bytes, bytearray)):
        return data, memoryview(data)
    view = memoryview(data)
    return view.tobytes(), view
