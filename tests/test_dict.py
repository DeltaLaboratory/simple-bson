import pytest

import simple_bson
import bson

DATA = {
    "string": "호에엥",
    "array": ["호에엥"],
    "int32": 2147483647,
    "float": 0.128,
    "bool": [True, False],
    "bytes": "호에엥".encode("utf8")
}


def test_main():
    assert simple_bson.dump(DATA) == bson.BSON.encode(DATA)


if __name__ == "__main__":
    print()
    print(simple_bson.dump(DATA))
    print(bson.BSON.encode(DATA))
