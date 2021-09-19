import os

import pytest

import simple_bson
import bson

DATA = {
    "bytes": [os.urandom(16), 100000]
}


def test_bytes():
    assert simple_bson.dumps(DATA) == bson.BSON.encode(DATA)
