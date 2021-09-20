import bson

import simple_bson

DATA = {
    "array": [index for index in range(42)]
}


def test_encode():
    assert simple_bson.dumps(DATA) == bson.BSON.encode(DATA)


def test_decode():
    assert simple_bson.loads(simple_bson.dumps(DATA)) == DATA
