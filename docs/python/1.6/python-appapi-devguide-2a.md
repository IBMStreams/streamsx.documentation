---
layout: docs
title:  2.0 Developing for the Streaming Analytics service
description:  Learn how to deploy a Python app in the Streaming Analytics service
weight: 25
published: true
tag: py16
prev:
  file: python-appapi-devguide-2
  title: 1.0 Installing Python APIs
next:
  file: python-appapi-devguide-3
  title: 3.0 Developing for IBM Streams on-premises
---
**Attention:** Don't try this just yet. It won't work :-)

This tutorial shows how to build a simple "Hello World!" application with the Python Application API. The application runs as a job in your Streaming Analytics instance.

The Streaming Analytics service is built on IBM Streams technology. You don't need a local version of IBM Streams to build Python applications for the service.

This tutorial requires a Python 3.5 environment. Familiarity with Python is recommended. 

## 2.1 Setting up your Python environment

The following steps show how you can set up your Python development environment:

1. Ensure that you have Java 8 installed, and the JAVA_HOME environment variable is set:

   ```
   export JAVA_HOME="/usr/lib/jvm/java-1.x.x-openjdk"
   export PATH=$JAVA_HOME/bin:$PATH
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
3. Install the latest streamsx package with pip, a package manager for Python.

   ```
   pip install --user --upgrade streamsx
   ```

## 2.2 Starting a Streaming Analytics service

If you have a Streaming Analytics service in [IBM Bluemix](https://console.ng.bluemix.net/), make sure that it's up and running.

To create a new Streaming Analytics service:

  1. Go to the [Bluemix web portal](https://www.ibm.com/cloud-computing/bluemix/) and log in (or sign up for a free Bluemix account).
  2. Click **Catalog**, browse for the Streaming Analytics service and then click on it.
  3. Enter the service name and then click **Create** to set up your service. The service dashboard opens and your service starts automatically. The service name appears as the title of the service dashboard.

### 2.2.1 Setting up access to the service

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

## 2.3 Creating a simple Hello World! streaming application 

To create a simple streaming application you must first create a Topology object. A topology object represents a declaration of a streaming application that will be executed by a Streams instance as a job:

      ```python
      from streamsx.topology.topology import Topology
      from streamsx.topology.context import *
      from streamsx.topology import context
      topo = Topology('hello_world')
      hw = topo.source(['World!', 'Hello'])
      hw.print()
      ```

## 2.4 Submitting the job to the Streaming Analytics service

Use the `STREAMING_ANALYTICS_SERVICE` context to submit your Python application (the `topo` object) to the Streaming Analytics service. The config object contains the credentials required to access the service:

```python
context.submit('STREAMING_ANALYTICS_SERVICE', topo, config=streams_conf)
```

After your application is running in the Streaming Analytics service, you can monitor the application through the Streams Console in your service.

## 2.5 Viewing the streaming data

In the Streams Console, the Application Dashboard view shows a summary of all of the jobs that are running on the service.

 1. Go to the Application Dashboard view, click the Streams console log viewer on the left toolbar.
 2. Expand the log navigation tree and highlight the PE (processing element).
 3. Select the **Console Log** tab.
 4. Click **Load console messages**.
 
## 2.6 The complete application

Your complete application should look like this:
 
       ```
       c={
         # ... *paste your credentials here*
       }
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
       from streamsx.topology.topology import Topology
       from streamsx.topology.context import *
       from streamsx.topology import context
       topo = Topology('hello_world')
       hw = topo.source(['World!', 'Hello'])
       hw.print()
       context.submit('STREAMING_ANALYTICS_SERVICE', topo, config=streams_conf)
       ```
       
