import struct

from .etc import dummy_function, TypeSignature, EncodeError

encoders = {}


def register(input_type):
    def decorator(function):
        if input_type in encoders:
            dummy_function(function.__name__)
            return
        for types in input_type:
            encoders[types] = function
        return

    return decorator


def encode_element_name(name: (str, bytes)) -> bytes:
    if isinstance(name, str):
        name = name.encode("utf-8")
    if b"\x00" in name:
        raise EncodeError("NUL cannot in name")
    return name + b"\x00"


def encode_element(name: (str, bytes), element) -> bytes:
    encoder = encoders.get(type(element))
    if encoder is None:
        raise EncodeError(f"Cannot find encoder : {type(element)}")
    return encoder(name, element)


def root_encoder(dictionary):
    buffer = bytearray()
    for key in dictionary.keys():
        if type(key) not in (bytes, str):
            key = str(key)
        buffer.extend(encode_element(key, dictionary[key]))
    return struct.pack(f"<i{len(buffer)}sb", len(buffer) + 5, buffer, 0)


@register((str,))
def encode_string(name: (str, bytes), value: str) -> bytes:
    value = value.encode("utf-8")
    return TypeSignature.string + encode_element_name(name) + struct.pack(f"<i{len(value)}sb", len(value) + 1, value, 0)


@register((bool,))
def encode_bool(name: (str, bytes), value: bool) -> bytes:
    return TypeSignature.bool + encode_element_name(name) + struct.pack("<b", value)


@register((None,))
def encode_null(name: (str, bytes), value: None) -> bytes:
    return TypeSignature.null + encode_element_name(name)


@register((int,))
def encode_int(name: (str, bytes), value: int) -> bytes:
    if -2147483648 <= value <= 2147483647:
        return TypeSignature.int32 + encode_element_name(name) + struct.pack("<i", value)
    elif -9223372036854775808 <= value <= 9223372036854775807:
        return TypeSignature.int64 + encode_element_name(name) + struct.pack("<q", value)
    elif 0 <= value <= 18446744073709551615:
        return TypeSignature.uint64 + encode_element_name(name) + struct.pack("<Q", value)
    else:
        raise EncodeError("bson only support -9223372036854775808 ~ 18446744073709551615 (int32, int64, uint64)")


@register((float,))
def encode_double(name: (str, bytes), value: float) -> bytes:
    return TypeSignature.double + encode_element_name(name) + struct.pack("<d", value)


@register((bytes,))
def encode_binary(name: (str, bytes), value: bytes) -> bytes:
    return TypeSignature.binary + encode_element_name(name) + struct.pack("<ib", len(value), 0) + value


@register((list, tuple))
def encode_list(name: (str, bytes), value: (set, list)) -> bytes:
    buffer = bytearray()
    for index, element in enumerate(value):
        buffer.extend(encode_element(str(index), element))
    return TypeSignature.array + encode_element_name(name) + struct.pack(f"<i{len(buffer)}sb", len(buffer),
                                                                         buffer, 0)


@register((dict,))
def encode_dict(name: (str, bytes), value: dict) -> bytes:
    buffer = bytearray()
    for key in value.keys():
        if type(key) not in (bytes, str):
            key = str(key)
        buffer.extend(encode_element(key, value[key]))
    return TypeSignature.document + encode_element_name(name) + struct.pack(f"<i{len(buffer)}sb", len(buffer),
                                                                            buffer, 0)
