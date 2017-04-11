---
layout: docs
title:  Creating Python apps for the Streaming Analytics service
description:  Learn how to deploy a Python app in the Streaming Analytics service
weight: 10
published: true
---

You can create an app in your Python environment, and then deploy the app to an instance of the Streaming Analytics service running on IBM Bluemix.

The Streaming Analytics service is built on IBM Streams technology. You do not need a local version of IBM Streams to build apps for the service.

This tutorial shows how to build a simple app with Python. The app runs as a job in your Streaming Analytics instance. 

*Note:* Familiarity with Python is recommended. This tutorial is designed to run in a Python 3.5 environment.

<!-- This set up section will probably be removed when the DSX integration with the Streaming Analytics service is enhanced -->

## Setting up your environment

The following steps show how to set up your Python environment and your Streaming Analytics instance:

1. Install [Java 8](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html) and set the JAVA_HOME environment variable:
   ```
   export JAVA_HOME="/usr/lib/jvm/java-1.x.x-openjdk"
   export PATH=$JAVA_HOME/bin:$PATH
   ```
2. Install [Anaconda 3](https://www.continuum.io/downloads). Follow the instructions that apply to your operating system.

3. Set the bin and scripts directories in the `PATH` environment variable:
   ```
   export PATH="~/anaconda3/bin:$PATH"
   ```
   In Windows operating systems, you must also set the Scripts directory in the `PATH` environment variable:  
   ```
   set PATH="%ANACONDA%;%ANACONDA_SCRIPTS%;%PATH%"
   ```

4. To use Python 3.5 for the current session, enter the following command in the terminal:
   ```
   conda create –n py35 python=3.5
   ```
5. Enter *y* to proceed and then activated the 3.5 sub-environment with the following command:
   ```
   source activate py35
   ```
6. [Install the Python package pypi.streamsx](#step1)
7. [Start a Streaming Analytics service](#step2)
8. [Set up access to the service](#step3)

<a id="step1"/>
### Installing the Python package pypi.streamsx

Install the latest Python package pypi.streamsx from the Python Package Index (PyPI) into your Python environment:

```
pip install --user --upgrade streamsx
```
Use this package to:

  - Create streaming apps that run in the Streaming Analytics service.
  - Access data streams from views defined in any app that is running in the Streaming Analytics service.

<a id="step2"></a>
### Starting a Streaming Analytics service

If you have a Streaming Analytics service in [IBM Bluemix](https://console.ng.bluemix.net/), make sure that it's up and running. To check the status of your service, go to the **Manage** tab of your service dashboard. The status should read: *The Streaming Analytics service is started*. 

To create a new Streaming Analytics service:

  1. Go to the [Bluemix web portal](https://www.ibm.com/cloud-computing/bluemix/) and log in (or sign up for a free Bluemix account).
  2. Click **Catalog**, browse for the Streaming Analytics service and then click on it.
  3. Enter the service name and then click **Create** to set up your service. The service dashboard opens and your service starts automatically. The service name appears as the title of the service dashboard.

<a id="step3"></a>
### Setting up access to the service 

The streaming app must have access to the service. To set up access to the service:

1. Start your Python environment:
   
   ```
   python
   ```

3. Go to your service dashboard, click **Service Credentials**, and then **View Credentials** to copy your service credentials.

   Paste your credentials using the following command:

   ```python
   c={
     # ... *paste your credentials here*
   }
   ```

4. Create a simple Hello World! streaming app. To create a simple streaming application you must first create a Topology object. A topology object represents a declaration of a streaming application that will be executed by a Streams instance as a job. The topology also specifies an iterable stream source and prints the contents of the stream to the application console:

   ```python
   from streamsx.topology.topology import Topology
   from streamsx.topology.context import *
   from streamsx.topology import context
   topo = Topology('hello_world')
   hw = topo.source(['World!', 'Hello'])
   hw.print()
   ```

4. Enter the name of your service and define the build configuration used to deploy your app to the service:

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

## Submitting the job to the Streaming Analytics service

Submit the `topo` object, which represents the app topology, to the `STREAMING_ANALYTICS_SERVICE` context. The config object contains the credentials required to access the service: 

```python
context.submit('STREAMING_ANALYTICS_SERVICE', topo, config=streams_conf)
```

After your application is built by the Streaming Analytics service, you can monitor the app through the Streams Console in your service.

## Viewing the streaming data

In the Streams Console, the Application Dashboard view shows a summary of all of the jobs that are running on the service. 

 1. Go to the Application Dashboard view, click the Streams console log viewer on the left toolbar.
 2. Expand the log navigation tree and highlight the PE (processing element).
 3. Select the **Console Log** tab.
 4. Click **Load console messages**.
 