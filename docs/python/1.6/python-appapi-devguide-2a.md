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
  title: 3.0 Developing with an IBM Streams installation
---

Follow the steps in this tutorial to get started with the Python Application API by creating an application that reads data from a temperature sensor and prints the output to the screen. The application runs as a job in your instance of the Streaming Analytics service on IBM Bluemix.

The Streaming Analytics service is built on IBM Streams technology. You don't need to install a local version of IBM Streams to build Python applications for the service.

This tutorial requires a Python 3.5 environment. Familiarity with Python is recommended.

## About streaming analytics applications

Streaming analytics applications are intended to run indefinitely because they meet the need for real-time data processing. (This is in contrast to applications created for the Apache Hadoop framework, which are intended to terminate when a batch of data is successfully processed.) For example, consider a company whose product scans temperature sensors across the world to determine weather patterns and trends. Because there is always a temperature, there is a perpetual need to process data. The application that processes the data must be able to run for an indefinite amount of time.

The application must also be scalable. If the number of temperature sensors doubles, the application must double the speed at which it processes data to ensure that analysis is available in a timely manner.


## 2.1 Setting up your Python environment

Follow these steps to set up your Python development environment. These steps assume that you are installing Python 3.5 from Anaconda on a Linux workstation.

1. Ensure that you have Java 8 installed and the JAVA_HOME environment variable is set. To set the JAVA_HOME variable, enter the following command on the command line, replacing "1.x.x" with
your Java version:
   ```
   export JAVA_HOME="/usr/lib/jvm/java-1.x.x-openjdk"
   ```
2. Ensure that you have Python 3.5 installed. For example, you can get Python 3.5 from [the Anaconda archive page](https://repo.continuum.io/archive/index.html). An Anaconda version that contains Python 3.5 is Anaconda3-4.2.x.

3. Follow these steps to activate your Anaconda Python 3.5 environment:

   1. Ensure that the bin directory is added to the `PATH` environment variable. If necessary, add the bin directory by entering the following command on the command line:

       ```
       export PATH="~/anaconda3/bin:$PATH"
      ```
   2. To use Python 3.5 for the current session, enter the following command on the command line:

       ```
       conda create –n py35 python=3.5
       ```
       Enter *y* to proceed.

   3. Activate the 3.5 sub-environment with the following command on the command line:

       ```
       source activate py35
       ```
3. Install the latest streamsx package with *pip*, a package manager for Python, by entering the following command on the command line:

   ```
   pip install --user --upgrade streamsx
   ```

## 2.2 Starting a Streaming Analytics service

Make sure that your Streaming Analytics service is running.
* If you have a Streaming Analytics service in [IBM Bluemix](https://console.ng.bluemix.net/), make sure that it is started and running.
* To create a new Streaming Analytics service:
  1. Go to the [Bluemix web portal](https://www.ibm.com/cloud-computing/bluemix/) and sign in (or sign up for a free Bluemix account).
  2. Click **Catalog**, browse for the Streaming Analytics service, and then click it.
  3. Enter the service name and then click **Create** to set up your service. The service dashboard opens and your service starts automatically. The service name appears as the title of the service dashboard.

## 2.3 Creating your application
The remainder of this tutorial walks you through creating your application.  The steps are broken up so that they can be run from the Python interpreter.  If you prefer, you can copy the [complete application](#211-the-complete-application), save it to a file, and run it in the Python 3.5 environment.

## 2.4 Setting up access to the service

The streaming application must be able to access the service. To set up access to the service:

1. Start your Python environment by entering the following command on the command line:

   ```
   python
   ```

2. Set your service credentials.
    1. On your Streaming Analytics service dashboard, click **Service Credentials**, and then click **View Credentials**. Copy your service credentials.

    2. At the Python prompt, enter the following code to set your credentials, replacing "paste-your-credentials-here" with the text you copied from the service dashboard:

       ```python
       creds = paste-your-credentials-here
       ```

3. Set the name of your service. A valid build configuration object is required to submit your application; here, you can use the `build_streams_config` function to create the build configuration object, given the provided service name and credentials.

    1. Go to your Streaming Analytics service dashboard and copy the name of your service.

    2. At the Python prompt, enter the following code, replacing "paste-your-service-name-here" with the service name that you copied from the service dashboard:

          ```python
          from streamsx.topology import context

          service_name="paste-your-credentials-here"

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

          streams_conf = build_streams_config(service_name, creds)
          ```

## 2.5 Creating a topology object
The first component of your application is a `Topology` object. Create a topology object by entering the following line at the Python prompt:

~~~~~~ python
from streamsx.topology.topology import Topology
topo = Topology("temperature_sensor")
~~~~~~

A streaming analytics application is a directed graph that specifies how data is generated and processed, also called a flow graph. The `Topology` object contains information about the structure of the directed flow graph.


## 2.6 Defining a data source
The `Topology` object also includes functions to define your data sources. In this application, the data source is a simulated temperature sensor. The readings are obtained by defining a Python generator function (`random.gauss()`) that returns an iterator of random numbers. However, you can use a live data source instead.

Define the following function:

~~~~~~ python
import random
def readings():
    while True:
        yield random.gauss(0.0, 1.0)
~~~~~~

The `Topology.source()` function takes as input a zero-argument callable object, such as a function or an instance of a callable class, that returns an iterable of tuples. In this example, the input to `source` is the `readings()` function.  The `source` function calls the `readings()` function, which returns a generator object.  The `source` function gets the iterator from the generator object and repeatedly calls the `next()` function on the iterator, which retrieves new random temperature readings on each invocation.

## 2.7 Creating a `Stream` object
The `Topology.source()` function produces a `Stream` object, which represents a potentially infinite sequence of tuples. Because a streaming analytics application can run indefinitely, there is no upper limit to the number of tuples that can flow over a `Stream` object.

**Tip:** Tuples flow over a `Stream` object one at a time and are processed by subsequent data operations. Operations are discussed in more detail in the [Common Streams operations](../python-appapi-devguide-4/) section of this guide. A tuple can be any Python object that is serializable by using the pickle module.

Create a source stream by entering the following code at the Python prompt:

~~~~~~ python
source = topo.source(readings)
~~~~~~


## 2.8 Printing to output
After you obtain the data, you print it to standard output by using the `sink` operation, which terminates the stream.

Print to output by entering the following code at the Python prompt:

~~~~~~ python
source.sink(print)
~~~~~~

The `Stream.sink()` operation takes as input a callable object that takes a single tuple as an argument and returns no value. The callable object is invoked with each tuple. In this example, the `sink` operation calls the built-in `print()` function with the tuple as its argument.

**Tip:** The `print()` function is useful, but if your application needs to output to a file, you must implement a custom sink operator.



## 2.9 Submitting the job to the Streaming Analytics service

After you define the application, you can submit it by using the `streamsx.topology.context` module. When you submit the application, use the `submit()` function from the `streamsx.topology.context` module to submit the application.  Use the `STREAMING_ANALYTICS_SERVICE` context to submit your Python application (the `topo` object) to the Streaming Analytics service. The config object contains the credentials required to access the service:

``` python
from streamsx.topology import context
context.submit(context.ContextTypes.STREAMING_ANALYTICS_SERVICE, topo, config=streams_conf)
```

## 2.10 Viewing the streaming data

After your application is running in the Streaming Analytics service, you can monitor the application through the Streams Console in your service. In the Streams Console, the Application Dashboard view shows a summary of all of the jobs that are running on the service.

 1. If necessary, open the Streams console by clicking **Launch** on the Streaming Analytics service dashboard.
 2. On the Application Dashboard view, click **Log Viewer** on the toolbar.
 2. Expand the log navigation tree and select the item with `PE` in its name, for example, `PE:4`.
 3. Click the **Console Log** tab.
 4. Click **Load console messages**.
 The contents of your output will look something like this:
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


## 2.11 The complete application

Copy following code into a file named `temperature_sensor.py`, which is your main application.

~~~~~~ python

from streamsx.topology import context
from streamsx.topology.topology import Topology
from streamsx.topology.context import *
import random

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

def readings():
    while True:
        yield random.gauss(0.0, 1.0)

def main():
    creds = *paste your credentials here*

    service_name="service_name" #Change this to your service name
    streams_conf = build_streams_config(service_name, creds)

    topo = Topology("temperature_sensor")
    source = topo.source(readings)
    source.sink(print)
    context.submit(context.ContextTypes.STREAMING_ANALYTICS_SERVICE, topo, config=streams_conf)

if __name__ == '__main__':
     main()

~~~~~~
