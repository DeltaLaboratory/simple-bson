import struct
import typing
import collections.abc
import io

from .etc import TypeSignature, DecodeError

decoders = {}


def register(decode_type: collections.abc.Sequence) -> typing.Callable:
    """
    simple decorator for type dispatch
    """

    def decorator(function):
        if decode_type in decoders:
            return function
        for types in decode_type:
            decoders[struct.unpack("<b", types)[0]] = function
        return function

    return decorator


def read_name(stream: io.BytesIO):
    buffer = bytearray()
    while True:
        buffer.extend(stream.read(1))
        if buffer[-1] == 0:
            return buffer[0:-1].decode("utf-8")


def read_length(stream: io.BytesIO):
    return struct.unpack("<i", stream.read(4))[0]


def decode_element(stream: io.BytesIO):
    element_type = struct.unpack("<b", stream.read(1))[0]
    try:
        return decoders[element_type](stream)
    except LookupError:
        raise DecodeError(f"No decoder for : signature {element_type}")


def decode_root_document(document: bytes):
    if document[-1] != 0:
        raise DecodeError("Invalid Document : Bad EOD")
    document = io.BytesIO(document[0:-1])
    read_length(document)
    result = {}
    while document.getbuffer().nbytes != 0:
        result[read_name(document)] = decode_element(document)
    return result


@register((TypeSignature.document,))
def decode_document(stream: io.BytesIO) -> dict:
    document = io.BytesIO(stream.read(read_length(stream)))
    result = {}
    while document.getbuffer().nbytes != 0:
        result[read_name(document)] = decode_element(document)
    return result


@register((TypeSignature.array,))
def decode_array(stream: io.BytesIO) -> list:
    document = io.BytesIO(stream.read(read_length(stream)))
    result = []
    while document.getbuffer().nbytes != 0:
        read_name(document)
        result.append(decode_element(document))
    return result


@register((TypeSignature.string,))
def decode_string(stream: io.BytesIO) -> str:
    return stream.read(read_length(stream) - 1).decode("utf-8")


@register((TypeSignature.bool,))
def decode_bool(stream: io.BytesIO) -> bool:
    return bool(struct.unpack("<b", stream.read(1))[0])


@register((TypeSignature.int32,))
def decode_int32(stream: io.BytesIO) -> int:
    return struct.unpack("<i", stream.read(4))[0]


@register((TypeSignature.int64,))
def decode_int64(stream: io.BytesIO) -> int:
    return struct.unpack("<q", stream.read(8))[0]


@register((TypeSignature.uint64,))
def decode_uint64(stream: io.BytesIO) -> int:
    return struct.unpack("<Q", stream.read(8))[0]


@register((TypeSignature.double,))
def decode_float(stream: io.BytesIO) -> float:
    return struct.unpack("<d", stream.read(8))[0]


@register((TypeSignature.null,))
def decode_none(stream: io.BytesIO) -> None:
    return None


@register((TypeSignature.binary,))
def decode_binary(stream: io.BytesIO) -> bytes:
    return stream.read(struct.unpack("<i", stream.read(5))[0])
