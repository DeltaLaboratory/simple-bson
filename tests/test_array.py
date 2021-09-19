import pytest

import simple_bson
import bson

DATA = {
    "array": [index for index in range(10000)]
}


def test_array():
    assert simple_bson.dumps(DATA) == bson.BSON.encode(DATA)
