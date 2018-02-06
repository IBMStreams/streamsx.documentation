---
layout: docs
title:  3.0 Developing with an IBM Streams installation
description: To get started with the Python Application API, use the example of reading data from a temperature sensor and printing the output to the screen.
weight:  30
published: true
tag: py16
prev:
  file: python-appapi-devguide-2
  title: 2.0 Developing for the IBM Streaming Analytics service
next:
  file: python-appapi-devguide-4
  title: 4.0 Common Streams operations
---

Follow the steps in this tutorial to get started with the Python Application API by creating an application that reads data from a temperature sensor and prints the output to the screen.

This tutorial requires a local installation of IBM Streams. Familiarity with Python is recommended.

## About streaming analytics applications

Streaming analytics applications are intended to run indefinitely because they meet the need for real-time data processing. (This is in contrast to applications created for the Apache Hadoop framework, which are intended to terminate when a batch of data is successfully processed.) For example, consider a company whose product scans temperature sensors across the world to determine weather patterns and trends. Because there is always a temperature, there is a perpetual need to process data. The application that processes the data must be able to run for an indefinite amount of time.

The application must also be scalable. If the number of temperature sensors doubles, the application must double the speed at which it processes data to ensure that analysis is available in a timely manner.

## 3.1 Setting up your environment
Before you can create your first Python application with the Python Application API and a local version of IBM Streams, you must complete the following setup tasks. These steps assume that you are installing Python 3.5 from Anaconda on a Linux workstation.

1. Install version 4.0.1 or later of IBM Streams or IBM Streams Quick Start Edition:

    * [IBM Streams Version 4.2.1 installation documentation](http://www.ibm.com/support/knowledgecenter/SSCRJU_4.2.1/com.ibm.streams.install.doc/doc/installstreams-container.html)

    * [IBM Streams Quick Start Edition Version 4.2.1 installation documentation](http://www.ibm.com/support/knowledgecenter/SSCRJU_4.2.1/com.ibm.streams.qse.doc/doc/installtrial-container.html)

1. Ensure that you configure the IBM Streams product environment variable by entering the following command on the command line:

        source product-installation-root-directory/4.n.n.n/bin/streamsprofile.sh

    **Tip:** Add the source command to your `home-directory/.bashrc` shell initialization file. Otherwise, you must enter the command every time you start IBM Streams. For example, if the product is installed in the `/home/streamsadmin/InfoSphere_Streams/4.2.1.0` directory, add the following line to your `.bashrc` file:

        source /home/streamsadmin/InfoSphere_Streams/4.2.1.0/bin/streamsprofile.sh

1. If necessary, install the Python Application API.
    * IBM Streams 4.2 or later: The Python Application API is included at `$STREAMS_INSTALL/toolkits/com.ibm.streamsx.topology`, so no installation is necessary.
    * IBM Streams 4.1.1 or earlier, or to upgrade to the latest version of the IBM Streams Topology toolkit:
        1. Download the latest version of the toolkit from the streamsx.topology [Releases page](https://github.com/Ibmstreams/streamsx.topology/releases) on GitHub.
        1. After the toolkit is downloaded, extract it to your file system.
 <br><br>

1. (IBM Streams only, doesn't apply to the Quick Start Edition) If necessary, install a supported version of Python. Python 2.7 and Python 3.5 are supported. **Important:** Python 3.5 is required to build application bundles with the Python Application API that can be submitted to your IBM Streaming Analytics service.

    You can choose from one of these options:
   * *(Recommended)* Anaconda: [https://www.continuum.io/downloads](https://www.continuum.io/downloads)

   * CPython: [https://www.python.org](https://www.python.org)

     If you build Python from source, remember to pass `--enable-shared` as a parameter to  `configure`.  After installation, set the `LD_LIBRARY_PATH` environment variable to `Python_Install>/lib`.

1. Include the fully qualified path of the `com.ibm.streamsx.topology/opt/python/packages` directory in the `PYTHONPATH` environment variable. For example, enter the following command on the command line:

        export PYTHONPATH=/home/myuser/download/com.ibm.streamsx.topology/opt/python/packages:$PYTHONPATH
1. Set the `PYTHONHOME` application environment variable on your Streams instance by entering the following `streamtool` command on the command line:

        streamtool setproperty -i <INSTANCE_ID> -d <DOMAIN_ID> --application-ev PYTHONHOME=<path_to_python_install>

     For example, if using the Quick Start Edition:

       streamtool setproperty -i StreamsInstance -d StreamsDomain --application-ev PYTHONHOME=/opt/pyenv/versions/3.5.1 --embeddedzk

     You can also set the environment variable from the Streams Console in your service.



## 3.2 Creating a topology object
The first component of your application is a `Topology` object.

Include the following code in a file called `temperature_sensor.py` file (the main module):

~~~~~~ python
from streamsx.topology.topology import Topology
topo = Topology("temperature_sensor")
~~~~~~

A streaming analytics application is a directed flow graph that specifies how data is generated and processed. The `Topology` object contains information about the structure of the directed flow graph.


## 3.3 Defining a data source
The `Topology` object also includes functions to define your data sources. In this application, the data source is a simulated temperature sensor. The readings are obtained by defining a Python generator function (`random.gauss()`) that returns an iterator of random numbers. However, you can use a live data source instead.

Include the following code in a file called `temperature_sensor.py`:

~~~~~~ python
import random
def readings():
    while True:
        yield random.gauss(0.0, 1.0)
~~~~~~

The `Topology.source()` function takes as input a zero-argument callable object, such as a function or an instance of a callable class, that returns an iterable of tuples. In this example, the input to `source` is the `readings()` function.  The `source` function calls the `readings()` function, which returns a generator object.  The `source` function gets the iterator from the generator object and repeatedly calls the `next()` function on the iterator to get the next tuple, which returns new random temperature readings each time.

## 3.4 Creating a `Stream` object
The `Topology.source()` function produces a `Stream` object, which is a potentially infinite flow of tuples in an application. Because a streaming analytics application can run indefinitely, there is no upper limit to the number of tuples that can flow over a `Stream` object.  

**Tip:** Tuples flow over a `Stream` object one at a time and are processed by subsequent data operations. Operations are discussed in more detail in the [Common Streams operations](../python-appapi-devguide-4/) section of this guide. A tuple can be any Python object that is serializable by using the pickle module.

Also include the following code in the `temperature_sensor.py` file:

~~~~~~ python
source = topo.source(readings)
~~~~~~


## 3.5 Printing to output
After you obtain the data, print it to standard output by using the `sink` operation, which terminates the stream.

Include the following code in the `temperature_sensor.py` file:

~~~~~~ python
source.sink(print)
~~~~~~

The `Stream.sink()` operation takes as input a callable object that takes a single tuple as an argument and returns no value. The callable object is invoked with each tuple. In this example, the `sink` operation calls the built-in `print()` function with the tuple as its argument.  

**Tip:** The `print()` function is useful, but if your application needs to output to a file, you must implement a custom sink operator.


## 3.6 Submitting the application
After you define the application, you can submit it by using the `streamsx.topology.context` module. When you submit the application, use the `submit()` function from the `streamsx.topology.context` module and pass the context type and the topology graph object as parameters to the function.

Include the following code in the `temperature_sensor.py` file:

~~~~~~ python
streamsx.topology.context.submit("STANDALONE", topo)
~~~~~~

## 3.7 The complete application

The following code is in the `temperature_sensor.py` file:

~~~~~~ python
from streamsx.topology.topology import Topology
import streamsx.topology.context
import random

def readings():
    while True:
        yield random.gauss(0.0, 1.0)

def main():
    topo = Topology("temperature_sensor")
    source = topo.source(readings)
    source.sink(print)
    streamsx.topology.context.submit("STANDALONE", topo)

if __name__ == '__main__':
    main()
~~~~~~

## 3.8 Running the application
To run the sample application, enter the following command on the command line:

~~~~~~ python
python3 temperature_sensor.py
~~~~~~

Enter `Ctrl-C` to stop the application.

## 3.9 Sample output
The contents of your output will look something like this:

~~~~~~
...
1.6191338426594375
-0.3088492294198733
0.43973191574979087
-1.0249371132740133
-0.3151212021333815
-0.6787283449628287
-0.11907886745291935
-0.24096558784475972
...
~~~~~~
