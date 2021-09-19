import pytest

import simple_bson
import bson

DATA = {
    "int32": 0000,
    "int64": 9223372036854775807
}


def test_int():
    assert simple_bson.dumps(DATA) == bson.BSON.encode(DATA)
