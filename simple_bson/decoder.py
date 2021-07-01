import struct

from .etc import dummy_function, TypeSignature, DecodeError

decoders = {}


def register(input_type):
    def decorator(function):
        if input_type in decoders:
            dummy_function(function.__name__)
            return
        for types in input_type:
            decoders[types] = function
        return

    return decorator


def decode_element():
    pass
