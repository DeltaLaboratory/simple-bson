Simple-Bson
========================

[![CI](https://github.com/DeltaLaboratory/simple-bson/actions/workflows/CI.yml/badge.svg)](https://github.com/DeltaLaboratory/simple-bson/actions/workflows/CI.yml)

Introduction
------------
simple-bson is a simple and lightweight bson implementation (current 7.89KiB)

Usage
------------

.. sourcecode:: python

   >>> import simple_bson as bson
   >>> a = bson.dumps({"Answer to life the universe and everything": 42})
   >>> b = bson.loads(a)
   >>> b
   {"Answer to life the universe and everything": 42}