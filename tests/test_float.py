import random

import pytest

import simple_bson
import bson

DATA = {
    "float": [random.random() for _ in range(10000)]
}


def test_float():
    assert simple_bson.dump(DATA) == bson.BSON.encode(DATA)
