Simple-Bson
========================

Introduction
------------
simple-bson is a simple and lightweight bson implementation (current 7.89KiB)

Usage
------------
.. code-block:: python
    import simple_bson as bson
    a = bson.dumps({"Answer to life the universe and everything": 42})
    b = bson.loads(a)
    print(b)