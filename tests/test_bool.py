import pytest

import simple_bson
import bson

DATA = {
    "bool": [True, False]
}


def test_bool():
    assert simple_bson.dumps(DATA) == bson.BSON.encode(DATA)
