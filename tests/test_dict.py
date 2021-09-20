import bson

import simple_bson

DATA = {
    "string": "Lorem Ipsum",
    "int32": 42,
    "int64": 9223372036854775807,
    "bytes": "Lorem Ipsum".encode("utf-8"),
    "array": [],
    "bool": [True, False],
    "float": 0.42
}


def test_encode():
    assert simple_bson.dumps(DATA) == bson.BSON.encode(DATA)


def test_decode():
    assert simple_bson.loads(simple_bson.dumps(DATA)) == DATA
