import os

import bson

import simple_bson

DATA = {
    "bytes": os.urandom(42)
}


def test_encode():
    assert simple_bson.dumps(DATA) == bson.BSON.encode(DATA)


def test_decode():
    assert simple_bson.loads(simple_bson.dumps(DATA)) == DATA
