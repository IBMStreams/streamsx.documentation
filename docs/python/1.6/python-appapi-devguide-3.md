---
layout: docs
title:  Create your first application with an IBM Streams installation
description: To get started with the Python Application API, use the example of reading data from a temperature sensor and printing the output to the screen.
weight:  30
published: true
tag: py16
prev:
  file: python-appapi-devguide-2b
  title: Create an application for IBM Cloud Private for Data
next:
  file: python-appapi-devguide-4
  title: Common Streams transforms
---

Follow the steps in this tutorial to get started with the Python Application API by creating an application that reads data from a temperature sensor and prints the output.

This tutorial requires a local installation of IBM Streams. Familiarity with Python is recommended.


## Setting up your environment
Before you can create your first Python application with a local version of IBM Streams, you must complete the following setup tasks. These steps assume that you are installing Python 3.6 from Anaconda on a Linux workstation.

1. Install the Streams Python package, `streamsx`,  from PyPi:

    `pip install streamsx`

1. Install version 4.2 or later of IBM Streams or the IBM Streams Quick Start Edition:

    * [IBM Streams Version 4.3.0 installation documentation](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.install.doc/doc/installstreams-container.html)

    * [IBM Streams Quick Start Edition Version 4.3.0 installation documentation](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.qse.doc/doc/installtrial-container.html)

1. (IBM Streams only, doesn't apply to the Quick Start Edition) If necessary, install a supported version of Python.  Python 3.5, 3.6 and 3.7 are supported. Python 2.7 support is currently deprecated.
**Important:** Python 3.6 is required to build application bundles that can be submitted to your IBM Streaming Analytics service.

    You can choose from one of these options:
   * *(Recommended)* [Anaconda](https://www.anaconda.com/distribution/#download-section)

   * CPython: [https://www.python.org](https://www.python.org)

     If you build Python from source, remember to pass `--enable-shared` as a parameter to  `configure`.  After installation, set the `LD_LIBRARY_PATH` environment variable to `Python_Install>/lib`.

1. Streams also includes a version of the `streamsx` package, so to make sure you are using the latest version of streamsx and not the one bundled with Streams, you should either:

   - Remove the `PYTHONPATH` environment variable, e.g `unset PYTHONPATH`
   - Or, make sure that `PYTHONPATH` does not include a path ending with `com.ibm.streamsx.topology/opt/python/package`.  

   **Tip**: Add the `unset PYTHONPATH` line to your `home-directory/.bashrc` shell initialization file. Otherwise, you'll have to enter the command every time you start IBM Streams.

1. Set the `PYTHONHOME` application environment variable on your Streams instance by entering the following `streamtool` command on the command line:

        streamtool setproperty -i <INSTANCE_ID> -d <DOMAIN_ID> --application-ev PYTHONHOME=<path_to_python_install>

     For example, if using the Quick Start Edition:

       streamtool setproperty -i StreamsInstance -d StreamsDomain --application-ev PYTHONHOME=/opt/pyenv/versions/3.5.1 --embeddedzk

     You can also set the environment variable from the Streams Console in your service.



## Creating a topology object
The first component of your application is a `Topology` object.

Include the following code in a file called `temperature_sensor.py` file (the main module):

~~~~~~ python
from streamsx.topology.topology import Topology
topo = Topology("temperature_sensor")
~~~~~~

A streaming analytics application is a directed flow graph that specifies how data is generated and processed. The `Topology` object contains information about the structure of the directed flow graph.


## Defining a data source
The `Topology` object also includes functions to define your data sources. In this application, the data source is a simulated temperature sensor. The readings are obtained by defining a Python generator function (`random.gauss()`) that returns an iterator of random numbers. However, you can use a live data source instead.

Include the following code in a file called `temperature_sensor.py`:

~~~~~~ python
import random
def readings():
    while True:
       yield {"id": "sensor_1", "value": random.gauss(0.0, 1.0)}

~~~~~~

The `Topology.source()` function takes as input a zero-argument callable object, such as a function or an instance of a callable class, that returns an iterable of tuples. In this example, the input to `source` is the `readings()` function.  The `source` function calls the `readings()` function, which returns a generator object.  The `source` function gets the iterator from the generator object and repeatedly calls the `next()` function on the iterator to get the next tuple, which returns new random temperature readings each time.

## Creating a `Stream` object
The `Topology.source()` function produces a `Stream` object, which is a potentially infinite flow of tuples in an application. Because a streaming analytics application can run indefinitely, there is no upper limit to the number of tuples that can flow over a `Stream` object.  

**Tip:** Tuples flow over a `Stream` object one at a time and are processed by subsequent data transforms. Transforms are discussed in more detail in the [Common Streams transforms](../python-appapi-devguide-4/) section of this guide. A tuple can be any Python object that is serializable by using the pickle module.

Also include the following code in the `temperature_sensor.py` file:

~~~~~~ python
source = topo.source(readings)
~~~~~~


## Generating output
After you obtain the data, you are ready to produce output. In our case we will just print the data to standard output using the `for_each` transform.

Include the following code in the `temperature_sensor.py` file:

~~~~~~ python
source.for_each(print)
~~~~~~

In this example, the `for_each` function calls the built-in `print()` function for each tuple it receives.

To send a Stream to an external system such as a file or database, implement a callable that takes a tuple as an argument, and pass the callable to `for_each`.



## Submitting the application
After you define the application, you can submit it by using the `streamsx.topology.context` module. When you submit the application, use the `submit()` function from the `streamsx.topology.context` module and pass the context type and the topology graph object as parameters to the function.

Include the following code in the `temperature_sensor.py` file:

~~~~~~ python
streamsx.topology.context.submit("STANDALONE", topo)
~~~~~~

## The complete application

The following code is in the `temperature_sensor.py` file:

~~~~~~ python
from streamsx.topology.topology import Topology
import streamsx.topology.context
import random

def readings():
    while True:
        yield {"id": "sensor_1", "value": random.gauss(0.0, 1.0)}

def main():
    topo = Topology("temperature_sensor")
    source = topo.source(readings)
    source.for_each(print)
    streamsx.topology.context.submit("STANDALONE", topo)

if __name__ == '__main__':
    main()
~~~~~~

## Running the application
To run the sample application, enter the following command on the command line:

~~~~~~ python
python3 temperature_sensor.py
~~~~~~

Enter `Ctrl-C` to stop the application.

## Sample output
The contents of your output will look something like this:

~~~~~~
...
{"id": "sensor_1", "value":1.6191338426594375}
{"id": "sensor_1", "value":-0.3088492294198733}
{"id": "sensor_1", "value":0.43973191574979087}
{"id": "sensor_1", "value":-1.0249371132740133}
...
~~~~~~

## Conclusion

You've created a very simple Streams Python application that creates a source `Stream` of data using `Topology.source()` and prints that `Stream`.  Typically, you would not just print the source `Stream`, but would process the data on the `Stream` using the various transformations. These are discussed in section 4, [Common Streams transforms](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-4).
