---
layout: docs
title:  Creating source streams in Python
description:  Learn how to develop a source stream in Python by using the the Python Application API
---

**Important:** The Python Application API is currently an alpha release.

# Python sources

## Overview

The function `Topology.source` declares a source stream, one that brings external data into your Streams application.
A source stream is the start of a streaming graph.

The `source` function is passed an application function that returns an [iterable](https://docs.python.org/3/glossary.html#term-iterable).
The function is called when the application is submitted and an [iterator](https://docs.python.org/3/glossary.html#term-iterator)
is obtained from the returned iterable.

The runtime then iterates through the available data by repeatably calling [__next__](https://docs.python.org/3/library/stdtypes.html#iterator.__next__)
and each returned item that is not `None` is submitted as a tuple for downstream processing.

When or if the iterator throws a `StopException` then no more tuples appear on the source stream. Note that typically
in streaming applications streams are infinite so that the iterator never ends.

Having only a single source method may seem limiting as there are other types of sources such as event based or polling that don't seem to
fit the `iterable` model. However, the power of Python comes to the rescue!

## Simple iterable sources

Examples of iterables include all sequence types (such as [list](https://docs.python.org/3/library/stdtypes.html#list)) so that they
can be returned directly by the function passed to `source()`.

````
# Returns a finite iterable resulting in a stream containing only two tuples.
def helloWorld():
   return ["hello", "world!"]
````

## Itertools

The Python module [itertools](https://docs.python.org/3/library/itertools.html) implements a number of iterator building blocks
which can therefore be used with `source`.

### Infinite counting sequence

The function [count()](https://docs.python.org/3/library/itertools.html#itertools.count) can be used to provide an infinite stream
that is a numeric sequence, for example this uses the default start of 0 and step of 1 to produce a stream of `1,2,3,4,5,...`.

````
import itertools
def infinite_sequence():
    return itertools.count()
````

### Infinite repeating sequence

The function [repeat()](https://docs.python.org/3/library/itertools.html#itertools.repeat) produces an iterator that repeats the same value,
either for a limited number of times or infiinte.

````
import itertools
# Infinite sequence of tuples with value A
def repeat_sequence():
    return itertools.repeat("A")
````

## Yield
A blocking source is one where a function is called that blocks until it has a value available to return. In a streaming paradigm
the method needs to be repeatably called fetching a new value each time.
