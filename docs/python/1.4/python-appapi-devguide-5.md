---
layout: docs
title: "4.0 API features: User-defined parallelism"
description: "A parallel region enables the application to use multiple channels to run operations (such as filtering or transforming data) concurrently."
weight:  50
published: true
tag: py14
prev:
  file: python-appapi-devguide-4
  title: 3.0 Common streams operations
---

If a particular portion of your graph is causing congestion because the application needs additional throughput at that point, you can define a **parallel region** in your graph. A parallel region enables the application to use multiple channels to run operations (such as filtering or transforming data) concurrently.

In the [Developing your first application](../python-appapi-devguide-3/) section, you created a topology and defined a pseudo temperature source. In this example, you want to convert all of the source tuples from Celsius to Kelvin.

To achieve this, add a function called `convertToKelvin()` to the application you created in the [Developing your first application](../python-appapi-devguide-3/) section.

Your application should look like this:

The following code should be in the temperature_sensor.py file:

~~~~~~
from streamsx.topology.topology import Topology
import streamsx.topology.context
import temperature_sensor_functions

def main():
    topo = Topology("temperature_sensor")
    source = topo.source(temperature_sensor_functions.readings)
    kelvin = source.map(temperature_sensor_functions.convertToKelvin)
    kelvin.sink(print)
    streamsx.topology.context.submit("STANDALONE", topo.graph)

if __name__ == '__main__':
    main()
~~~~~~

The following code should be in the temperature_sensor_functions.py file:

~~~~~~
import random

def readings():
    while True:
        yield random.gauss(0.0, 1.0)

def convertToKelvin(tuple) :
        return tuple +  273.15
~~~~~~

Converting a temperature reading from Celsius to Kelvin is not a resource-intensive task. However, you can use this example to see how using a parallel region can help distribute processing across resources when an operation is resource-intensive or inefficient and is causing a bottleneck in your application.

To parallelize an operation, invoke `.parallel()` on a `Stream` where you want to process data in parallel.

**Restriction:** Nested parallelism is not supported. You cannot invoke `parallel()` on a `Stream` that is already parallelized. If you do, your application will throw an exception.

To end parallel processing, invoke `.end_parallel()` on the parallelized `Stream`. When you invoke `end_parallel()` subsequent operations on the `Stream` that is returned by `end_parallel()` are not processed in parallel. For example, call `.end_parallel()` on the `kelvin` `Stream` before you call `sink(print)`.

The above example becomes:

~~~~~~
def main():
    topo = Topology("temperature_sensor")
    source = topo.source(temperature_sensor_functions.readings)
    kelvin = source.parallel(4).map(temperature_sensor_functions.convertToKelvin)
    end = kelvin.end_parallel()
    end.sink(print)
          streamsx.topology.context.submit("STANDALONE", topo.graph)
~~~~~~

Any operations that are performed on the parallelized `Stream` occur in parallel to the degree that is specified in the `.parallel()` function. In the example above, you specified 4, which means that four channels process the data in the parallel region on the graph.
