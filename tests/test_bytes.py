import random

import pytest

import simple_bson
import bson

DATA = {
    "bytes": [random.randbytes(16), 100000]
}


def test_bytes():
    assert simple_bson.dump(DATA) == bson.BSON.encode(DATA)
