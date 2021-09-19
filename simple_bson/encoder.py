import struct
import typing
import collections.abc

from .etc import TypeSignature, EncodeError

encoders = {}


def register(input_type: collections.abc.Sequence) -> typing.Callable:
    """
    simple decorator for type dispatch
    """

    def decorator(function):
        if input_type in encoders:
            return function
        for types in input_type:
            encoders[types] = function
        return function

    return decorator


def encode_element_name(name: str) -> bytes:
    if isinstance(name, str):
        name = name.encode("utf-8")
    if b"\x00" in name:
        raise EncodeError("null contained in name")
    return name + b"\x00"


def encode_element(name: str, element) -> bytes:
    encoder = encoders.get(type(element))
    if encoder is None:
        raise EncodeError(f"No encoder for : {type(element)}")
    return encoder(name, element)


def encode_document(document):
    buffer = b"".join([encode_element(key, document[key]) for key in document.keys()])
    return struct.pack(f"<i{len(buffer)}sb", len(buffer) + 5, buffer, 0)


@register((str,))
def encode_string(name: str, value: str) -> bytes:
    value = value.encode("utf-8")
    return TypeSignature.string + encode_element_name(name) + struct.pack(f"<i{len(value)}sb", len(value) + 1, value, 0)


@register((bool,))
def encode_bool(name: str, value: bool) -> bytes:
    return TypeSignature.bool + encode_element_name(name) + struct.pack("<b", value)


@register((None,))
def encode_null(name: str, value: None) -> bytes:
    return TypeSignature.null + encode_element_name(name)


@register((int,))
def encode_int(name: str, value: int) -> bytes:
    if -1 << 31 <= value <= 1 << 31:
        return TypeSignature.int32 + encode_element_name(name) + struct.pack("<i", value)
    elif -1 << 63 <= value <= 1 << 63:
        return TypeSignature.int64 + encode_element_name(name) + struct.pack("<q", value)
    elif 0 <= value <= (1 << 64) - 1:
        return TypeSignature.uint64 + encode_element_name(name) + struct.pack("<Q", value)
    else:
        raise EncodeError("bson only support (-1 << 63) ~ (1 << 64) - 1 (int32, int64, uint64)")


@register((float,))
def encode_double(name: str, value: float) -> bytes:
    return TypeSignature.double + encode_element_name(name) + struct.pack("<d", value)


@register((bytes,))
def encode_binary(name: str, value: bytes) -> bytes:
    return TypeSignature.binary + encode_element_name(name) + struct.pack("<ib", len(value), 0) + value


@register((list, tuple))
def encode_list(name: str, value: (set, list)) -> bytes:
    buffer = b"".join([encode_element(str(index), element) for index, element in enumerate(value)])
    return TypeSignature.array + encode_element_name(name) + struct.pack(f"<i{len(buffer)}sb", len(buffer) + 5,
                                                                         buffer, 0)


@register((dict,))
def encode_dict(name: str, value: dict) -> bytes:
    buffer = bytearray()
    for key in value.keys():
        if type(key) not in (bytes, str):
            key = str(key)
        buffer.extend(encode_element(key, value[key]))
    return TypeSignature.document + encode_element_name(name) + struct.pack(f"<i{len(buffer)}sb", len(buffer) + 5,
                                                                            buffer, 0)
