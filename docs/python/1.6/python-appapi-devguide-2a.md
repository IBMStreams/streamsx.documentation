---
layout: docs
title:  2.0 Developing for the IBM Streaming Analytics service
description:  Learn how to deploy a Python application in the IBM Streaming Analytics service on IBM Bluemix, without installing IBM Streams.
weight: 25
published: true
tag: py16
prev:
  file: python-appapi-devguide-2
  title: 1.0 Installing Python APIs
next:
  file: python-appapi-devguide-3
  title: 3.0 Developing with an IBM Streams install
---

Follow the steps in this tutorial to get started with the Python Application API by creating an application that reads data from a temperature sensor and prints the output to the screen. The application runs as a job in your Streaming Analytics instance.

The Streaming Analytics service is built on IBM Streams technology. You don't need a local version of IBM Streams to build Python applications for the service.

This tutorial requires a Python 3.5 environment. Familiarity with Python is recommended.

## About streaming analytics applications 

Streaming analytics applications are intended to run indefinitely because they meet the need for real-time data processing. (Unlike applications created for the Apache Hadoop framework, which are intended to terminate when a batch of data is successfully processed.) For example, consider a company whose product scans temperature sensors across the world to determine weather patterns and trends. Because there is always a temperature, there is a perpetual need to process data. The application that processes the data must be able to run for an indefinite amount of time.

The application must also be scalable. If the number of temperature sensors doubles, the application must double the speed at which it processes data to ensure that analysis is available in a timely manner. 


## 2.1 Setting up your Python environment

The following steps show how you can set up your Python development environment:

1. Ensure that you have Java 8 installed, and the JAVA_HOME environment variable is set:

   ```
   export JAVA_HOME="/usr/lib/jvm/java-1.x.x-openjdk"
   ```
2. Ensure that you have Python 3.5 installed. For example, you can get Python 3.5 from [Anaconda](https://www.continuum.io/downloads) and follow these steps to activate your Python 3.5 environment:

   1: Set the bin directory in the `PATH` environment variable:

   ```
   export PATH="~/anaconda3/bin:$PATH"
   ```
   2: In Windows operating systems, you might also have to set the Scripts directory in the `PATH` environment variable:

   ```
   set PATH="%ANACONDA%;%ANACONDA_SCRIPTS%;%PATH%"
   ```

   3: To use Python 3.5 for the current session, enter the following command in the terminal:

   ```
   conda create –n py35 python=3.5
   ```
   4: Enter *y* to proceed, and then activate the 3.5 sub-environment with the following command:

   ```
   source activate py35
   ```
3. Install the latest streamsx package with *pip*, a package manager for Python.

   ```
   pip install --user --upgrade streamsx
   ```

## 2.2 Starting a Streaming Analytics service

If you have a Streaming Analytics service in [IBM Bluemix](https://console.ng.bluemix.net/), make sure that it's up and running.

To create a new Streaming Analytics service:

  1. Go to the [Bluemix web portal](https://www.ibm.com/cloud-computing/bluemix/) and log in (or sign up for a free Bluemix account).
  2. Click **Catalog**, browse for the Streaming Analytics service and then click on it.
  3. Enter the service name and then click **Create** to set up your service. The service dashboard opens and your service starts automatically. The service name appears as the title of the service dashboard.

## 2.3 Creating your application
The remainder of this tutorial will walk you through creating your application.  The steps are broken up such that they can be run from the Python interpreter.  If you prefer, you can download the [complete application](#29-the-complete-application) and run it in the Python 3.5 environment.

## 2.4 Setting up access to the service

The streaming application must be able to access the service. To set up access to the service:

1. Start your Python environment:

   ```
   python
   ```

2. Go to your service dashboard, click **Service Credentials**, and then **View Credentials** to copy your service credentials.

   Paste your credentials using the following command:

   ```python
   c={
     # ... *paste your credentials here*
   }
   ```

3. Enter the name of your service and define the build configuration used to deploy your application to the service:

   ```python
   from streamsx.topology import context

   service_name="Your Service Name Here"

   def build_streams_config(service_name, credentials):
       vcap_conf = {
           'streaming-analytics': [
               {
                   'name': service_name,
                   'credentials': credentials,
               }
           ]
       }
       config = {
           context.ConfigParams.VCAP_SERVICES: vcap_conf,
           context.ConfigParams.SERVICE_NAME: service_name,
           context.ConfigParams.FORCE_REMOTE_BUILD: True
       }
       return config

   streams_conf = build_streams_config(service_name=service_name, credentials=c)
   ```

## 2.5 Creating a topology object
The first component of your application is a `Topology` object.

~~~~~~
from streamsx.topology.topology import Topology
topo = Topology("temperature_sensor")
~~~~~~

A streaming analytics application is a directed flow graph that specifies how data is generated and processed. The `Topology` object contains information about the structure of the directed flow graph.


## 2.6 Defining a data source
The `Topology` object also includes functions that enable you to define your data sources. In this application, the data source is the temperature sensor.

In this example, simulate temperature sensor readings by defining a Python generator function that returns an iterator of random numbers.


Create a new file called temperature_sensor_functions.py :

~~~~~~
import random
def readings():
    while True:
        yield random.gauss(0.0, 1.0)
~~~~~~

The `Topology.source()` function takes as input a zero-argument callable object, such as a function or an instance of a callable class, that returns an iterable of tuples. In this example, the input to `source` is the `readings()` function.  The `source` function calls the `readings()` function, which returns a generator object.  The `source` function gets the iterator from the generator object and repeatedly calls the `next()` function on the iterator to get the next tuple, which returns a new random temperature reading each time.

In this example, data is obtained by calling the `random.gauss()` function. However, you can use a live data source instead of the `random.gauss()` function.


## 2.7 Creating a Stream
The `Topology.source()` function produces a `Stream` object, which is a potentially infinite flow of tuples in an application. Because a streaming analytics application can run indefinitely, there is no upper limit to the number of tuples that can flow over a `Stream`.

Tuples flow over a `Stream` one at a time and are processed by subsequent data **operations**. Operations are discussed in more detail in the [Common Streams operations](../python-appapi-devguide-4/) section of this guide.

A tuple can be any Python object that is serializable by using the pickle module.

Returning to the interpreter, create a source stream with the following line:

~~~~~~
import temperature_sensor_functions
source = topo.source(temperature_sensor_functions.readings)
~~~~~~


## 2.8 Printing to output
After obtaining the data, you print it to standard output using the `sink` operation, which terminates the stream.

Include the following code in the temperature_sensor.py file:

~~~~~~
source.sink(print)
~~~~~~

The `Stream.sink()` operation takes as input a callable object that takes a single tuple as an argument and returns no value. The callable object is invoked with each tuple. In this example, the `sink` operation calls the built-in `print()` function with the tuple as its argument.

**Tip:** The `print()` function is useful, but if your application needs to output to a file, you need to implement a custom sink operator.



## 2.9 Submitting the job to the Streaming Analytics service

After you define the application, you can submit it by using `streamsx.topology.context` module. When you submit the application, use the `submit()` function from the `streamsx.topology.context` module to submit the application.  Use the `STREAMING_ANALYTICS_SERVICE` context to submit your Python application (the `topo` object) to the Streaming Analytics service. The config object contains the credentials required to access the service:

``` python
context.submit('STREAMING_ANALYTICS_SERVICE', topo, config=streams_conf)
```

After your application is running in the Streaming Analytics service, you can monitor the application through the Streams Console in your service.

## 2.9.1 Viewing the streaming data

In the Streams Console, the Application Dashboard view shows a summary of all of the jobs that are running on the service.

 1. Go to the Application Dashboard view, click the Streams console log viewer on the left toolbar.
 2. Expand the log navigation tree and select the item with `PE` in its name, e.g. `PE:4`.
 3. Select the **Console Log** tab.
 4. Click **Load console messages**.
 The contents of your output should look something like this:
     ```
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
     ```


## 2.10 The complete application

The following code should be in the temperature_sensor.py file, which is your main application:

~~~~~~

from streamsx.topology import context
from streamsx.topology.topology import Topology
from streamsx.topology.context import *
import temperature_sensor_functions

def build_streams_config(service_name, credentials):
     vcap_conf = {
         'streaming-analytics': [
             {
                 'name': service_name,
                 'credentials': credentials,
             }
         ]
     }
     config = {
         context.ConfigParams.VCAP_SERVICES: vcap_conf,
         context.ConfigParams.SERVICE_NAME: service_name,
         context.ConfigParams.FORCE_REMOTE_BUILD: True
     }
     return config

def main():
    c={
       # ... *paste your credentials here*
    }

    service_name="service_name" #Change this to your service name
    streams_conf = build_streams_config(service_name=service_name, credentials=c)

    topo = Topology("temperature_sensor")
    source = topo.source(temperature_sensor_functions.readings)
    source.sink(print)
    context.submit('STREAMING_ANALYTICS_SERVICE', topo, config=streams_conf)

if __name__ == '__main__':
     main()

~~~~~~


The following code should be in the temperature_sensor_functions.py file:

~~~~~~
import random

def readings():
     while True:
         yield random.gauss(0.0, 1.0)

~~~~~~
