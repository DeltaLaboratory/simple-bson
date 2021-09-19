import typing

from . import encoder, decoder


def dumps(document: typing.Dict) -> bytes:
    return encoder.encode_document(document)


def loads(document: bytes) -> typing.Dict:
    return decoder.decode_root_document(document)
