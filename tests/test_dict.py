import pytest

import simple_bson
import bson


def test_main():
    assert simple_bson.dump({"Text": "Hello"}) == bson.BSON.encode({"Text": "Hello"})


if __name__ == "__main__":
    print()
    print(simple_bson.dump({"Text": "TXT", "Array": [1234, 1234, 1234, 1234, 12345, 1234, 1234]}))
    print(bson.BSON.encode({"Text": "TXT", "Array": [1234, 1234, 1234, 1234, 12345, 1234, 1234]}))
