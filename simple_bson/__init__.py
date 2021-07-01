from . import encoder


def dump(dictionary):
    return encoder.root_encoder(dictionary)
