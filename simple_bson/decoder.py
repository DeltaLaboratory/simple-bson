import struct

from .etc import dummy_function, TypeSignature, DecodeError

decoders = {}


def register(decode_type):
    def decorator(function):
        if decode_type in decoders:
            dummy_function(function.__name__)
            return
        for types in decode_type:
            decoders[types] = function
        return

    return decorator


def read_document(document: bytes):
    return document.split(b"\x00")[0], b"\x00".join(document.split(b"\x00")[1:-1])


def decode_element(buffer):
    pass


def decode_element_name(buffer):
    pass


@register((TypeSignature.string,))
def decode_string(value: bytes) -> str:
    return value.decode("utf-8")


@register((TypeSignature.bool,))
def decode_bool(value: bytes) -> bool:
    return struct.unpack("<b", value)


@register((TypeSignature.int32,))
def decode_int32(value: bytes) -> int:
    return struct.unpack("<i", value)


@register((TypeSignature.int64,))
def decode_int64(value: bytes) -> int:
    return struct.unpack("<q", value)


@register((TypeSignature.uint64,))
def decode_uint64(value: bytes) -> int:
    return struct.unpack("<Q", value)


@register((TypeSignature.double,))
def decode_float(value: bytes) -> float:
    return struct.unpack("<d", value)


@register((TypeSignature.null,))
def decode_none(value: bytes) -> None:
    return None


@register((TypeSignature.binary,))
def decode_binary(value: bytes) -> bytes:
    return value
