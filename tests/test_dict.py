import pytest

import simple_bson
import bson

DATA = {
    "string": "Lorem Ipsum",
    "int32": 42,
    "int64": 9223372036854775807,
    "bytes": "Lorem Ipsum".encode("utf-8"),
    "array": [],
    "bool": [True, False],
    "float": 0.42
}


def test_main():
    assert simple_bson.dumps(DATA) == bson.BSON.encode(DATA)
