---
layout: docs
title:  Create your first Python application in the Streaming Analytics service
description:  Learn how to deploy a Python application in the IBM Streaming Analytics service on IBM Cloud, without installing IBM Streams.
weight: 25
published: true
tag: py16
prev:
  file: python-appapi-devguide-2
  title: Installing Python APIs
next:
  file: python-appapi-devguide-2b
  title: Create an application for IBM Cloud Pak for Data
---

Get started with the Python Application API by creating an application that reads data from a temperature sensor and prints the output. The application runs as a job in your instance of the Streaming Analytics service on the IBM Cloud.

The Streaming Analytics service is built on IBM Streams technology. You don't need to install a local version of IBM Streams to build Python applications for the service.

This tutorial requires a Python 3.6 environment. Familiarity with Python is recommended.

## Setting up your Python environment


Follow these steps to set up your Python development environment. These steps assume that you are installing Python 3.6 from Anaconda on a Linux workstation.

1. Ensure that you have Java 8 installed and the JAVA_HOME environment variable is set. To set the JAVA_HOME variable, enter the following command on the command line, replacing "1.x.x" with
your Java version:
   ```
   export JAVA_HOME="/usr/lib/jvm/java-1.x.x-openjdk"
   ```
2. Ensure that you have Python 3.6 installed. For example, you can get Python 3.6 from [the Anaconda archive page](https://repo.continuum.io/archive/index.html). An Anaconda version that contains Python 3.6 is Anaconda3-5.2.x.

3. Follow these steps to activate your Anaconda Python 3.6 environment:

   1. Ensure that the bin directory is added to the `PATH` environment variable. If necessary, add the `bin` directory by entering the following command on the command line:

       ```
       export PATH="~/anaconda3/bin:$PATH"
      ```
   2. To use Python 3.6 for the current session, enter the following command on the command line:

       ```
       conda create –n py36 python=3.6
       ```
       Enter *y* to proceed.

   3. Activate the 3.6 sub-environment with the following command on the command line:

       ```
       source activate py36
       ```
3. Install the latest streamsx package with *pip*, a package manager for Python, by entering the following command on the command line:

   ```
   pip install --user --upgrade streamsx
   ```


**Note:** For the most up to date information regarding supported versions of Python, including when a local installation of Streams is required, see the [developer setup page of the streamsx project documentation](https://streamsxtopology.readthedocs.io/en/stable/pysetup.html).


## Starting a Streaming Analytics service

Make sure that your Streaming Analytics service is running.
* If you have a Streaming Analytics service in [IBM Cloud](https://cloud.ibm.com/), make sure that it is started and running.
* To create a new Streaming Analytics service:
  1. Go to the [IBM Cloud web portal](https://cloud.ibm.com) and sign in (or sign up for a free IBM Cloud account).
  2. Click **Catalog**, browse for the Streaming Analytics service, and then click it.
  3. Enter the service name and then click **Create** to set up your service. The service dashboard opens and your service starts automatically. The service name appears as the title of the service dashboard.

## Creating your application
The remainder of this tutorial walks you through creating your application.  The steps are broken up so that they can be run from the Python interpreter.  If you prefer, you can copy the [complete application](#211-the-complete-application), save it to a file, and run it in the Python 3.6 environment.

## Setting up access to the service

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

## Creating a topology object
The first component of your application is a `Topology` object. Create a topology object by entering the following line at the Python prompt:

~~~~~~ python
from streamsx.topology.topology import Topology
topo = Topology("temperature_sensor")
~~~~~~

A streaming analytics application is a directed graph that specifies how data is generated and processed, also called a flow graph. The `Topology` object contains information about the structure of the directed flow graph.


## Defining a data source
The `Topology` object also includes functions to define your data sources. In this application, the data source is a simulated temperature sensor. The readings are obtained by defining a Python generator function (`random.gauss()`) that returns an iterator of random numbers. However, you can use a live data source instead.

Define the following function:

~~~~~~ python
import random
def readings():
  while True:
    yield {"id": "sensor_1", "value": random.gauss(0.0, 1.0)}
~~~~~~

The `Topology.source()` function takes as input a zero-argument callable object, such as a function or an instance of a callable class, that returns an iterable of tuples. In this example, the input to `source` is the `readings()` function.  The `source` function calls the `readings()` function, which returns a generator object.  The `source` function gets the iterator from the generator object and repeatedly calls the `next()` function on the iterator, which retrieves new random temperature readings on each invocation.

## Creating a `Stream` object
The `Topology.source()` function produces a `Stream` object, which represents a potentially infinite sequence of tuples. Because a streaming analytics application can run indefinitely, there is no upper limit to the number of tuples that can flow over a `Stream` object.

**Tip:** Tuples flow over a `Stream` object one at a time and are processed by subsequent data transforms. Transforms are discussed in more detail in the [Common Streams transforms](../python-appapi-devguide-4/) section of this guide. A tuple can be any Python object that is serializable by using the pickle module.

Create a source stream by entering the following code at the Python prompt:

~~~~~~ python
source = topo.source(readings)
~~~~~~


## Generating output
After you obtain the data, you are ready to produce output.  In our case, we will just print the data to standard output using the `for_each` transform.

Print to output by entering the following code at the Python prompt:

~~~~~~ python
source.for_each(print)
~~~~~~

In this example, the `for_each` function calls the built-in `print()` function for each tuple it receives.

To send a Stream to an external system such as a file or database, implement a callable that takes a tuple as an argument, and pass the callable to `for_each`.



## Submitting the job to the Streaming Analytics service

After you define the application, you can submit it by using the `streamsx.topology.context` module. When you submit the application, use the `submit()` function from the `streamsx.topology.context` module to submit the application.  Use the `STREAMING_ANALYTICS_SERVICE` context to submit your Python application (the `topo` object) to the Streaming Analytics service. The config object contains the credentials required to access the service:

``` python
from streamsx.topology import context
context.submit(context.ContextTypes.STREAMING_ANALYTICS_SERVICE, topo, config=streams_conf)
```

##0 Viewing the streaming data

After your application is running in the Streaming Analytics service, you can monitor the application through the Streams Console in your service. In the Streams Console, the Application Dashboard view shows a summary of all of the jobs that are running on the service.

 1. If necessary, open the Streams console by clicking **Launch** on the Streaming Analytics service dashboard.
 2. On the Application Dashboard view, click **Log Viewer** on the toolbar.
 2. Expand the log navigation tree and select the item with `PE` in its name, for example, `PE:4`.
 3. Click the **Console Log** tab.
 4. Click **Load console messages**.
 The contents of your output will look something like this:
     ```
     ...
     {"id": "sensor_1", "value":1.6191338426594375}
     {"id": "sensor_1", "value":-0.3088492294198733}
     {"id": "sensor_1", "value":0.43973191574979087}
     {"id": "sensor_1", "value":-1.0249371132740133}
     ...
     ```


##1 The complete application

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
      yield {"id": "sensor_1", "value": random.gauss(0.0, 1.0)}

def main():
    creds = *paste your credentials here*

    service_name="service_name" #Change this to your service name
    streams_conf = build_streams_config(service_name, creds)

    topo = Topology("temperature_sensor")
    source = topo.source(readings)
    source.for_each(print)
    context.submit(context.ContextTypes.STREAMING_ANALYTICS_SERVICE, topo, config=streams_conf)

if __name__ == '__main__':
     main()

~~~~~~



## Conclusion

You created a very simple Streams Python application that creates a source `Stream` of data using `Topology.source()` and prints that `Stream`.  Typically, you would not just print the source `Stream`, but would process the data on the `Stream` using the various transformations. These are discussed in section 4, [Common Streams Transformations](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-4).
