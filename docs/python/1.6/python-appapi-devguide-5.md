---
layout: docs
title: "5.0 API features: User-defined parallelism"
description: "A parallel region enables the application to use multiple channels to run operations (such as filtering or transforming data) concurrently."
weight:  50
published: true
tag: py16
prev:
  file: python-appapi-devguide-4
  title: 4.0 Common streams operations
next:
  file: python-appapi-devguide-6
  title: 6.0 The Python REST API
---

If a particular portion of your graph is causing congestion because the application needs additional throughput at that point, you can define a **parallel region** in your graph. A parallel region enables the application to use multiple channels to run operations (such as filtering or transforming data) concurrently.

In a previous example, you created a topology and defined a pseudo temperature source. In this example, you want to convert all of the source tuples from Celsius to Kelvin.

To achieve this, add a function called `convertToKelvin()` to the application you created in an earlier section.

Your application is contained in two files.

The following code is in the 'temperature_sensor.py' file:

~~~~~~
from streamsx.topology.topology import Topology
import streamsx.topology.context
import temperature_sensor_functions
import random

def readings():
    while True:
        yield random.gauss(0.0, 1.0)

def convertToKelvin(tuple) :
    return tuple +  273.15

def main():
    topo = Topology("temperature_sensor")
    source = topo.source(temperature_sensor_functions.readings)
    kelvin = source.map(temperature_sensor_functions.convertToKelvin)
    kelvin.sink(print)
    streamsx.topology.context.submit("STANDALONE", topo)

if __name__ == '__main__':
    main()
~~~~~~


Converting a temperature reading from Celsius to Kelvin is not a resource-intensive task. However, you can use this example to see how using a parallel region can help distribute processing across resources when an operation is resource-intensive or inefficient and is causing a bottleneck in your application.

To parallelize an operation, invoke `.parallel()` on a `Stream` object where you want to process data in parallel.

**Restriction:** You can't nest parallelism. If you invoke `parallel()` on a `Stream` object that is already parallelized, your application will throw an exception.

To end parallel processing, invoke `.end_parallel()` on the parallelized `Stream` object. When you invoke `end_parallel()`, subsequent operations on the `Stream` object that is returned by `end_parallel()` are not processed in parallel. For example, if you call `.end_parallel()` on the `kelvin` `Stream` object before you call `sink(print)`, the `sink(print)` function is not processed in parallel.

The previous example is replaced with the following code:

~~~~~~
def main():
    topo = Topology("temperature_sensor")
    source = topo.source(temperature_sensor_functions.readings)
    kelvin = source.parallel(4).map(temperature_sensor_functions.convertToKelvin)
    end = kelvin.end_parallel()
    end.sink(print)
    streamsx.topology.context.submit("STANDALONE", topo)
~~~~~~

Any operations that are performed on the parallelized `Stream` object occur in parallel to the degree that is specified in the `.parallel()` function. In this example, you specified 4, which means that four channels process the data in the parallel region on the graph.
