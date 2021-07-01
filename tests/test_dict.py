import pytest

import simple_bson
import bson

DATA = {
    "string": "호에엥",
    "int32": 0000,
    "int64": 9223372036854775807,
    "bytes": "호에엥".encode("utf-8"),
    "array": [],
    "bool": [True, False],
    "float": 0.009223372036854775807
}


def test_main():
    assert simple_bson.dump(DATA) == bson.BSON.encode(DATA)
