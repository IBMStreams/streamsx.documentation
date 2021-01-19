---
layout: docs
title: Installation and Setup
description: Prerequisites and installation instructions for the Python Application API
weight:  20
published: true
tag: py16
prev:
  file: python-appapi-devguide
  title: Introduction
next:
  file: python-appapi-devguide-3
  title: Create your first application
---


# Setup instructions
These are the basic requirements to create Streams applications with Python:

1. [Set up a Streams instance](#streams)
2. Set up your development environment(#setup)
3. [Set up a connection to the Streams instance](#connect)

### Set up a Streams instance
<a id="streams"></a>

The Python API is used to create a **Topology**, or application that is executed by the Streams runtime.
The Streams runtime can be in the public or private cloud or installed locally.

Choose the option that matches your desired Streams runtime, and follow the steps to install and/or configure the Streams instance.





{% include python/install/install_overview.html%}

<br/><br/>
**Note**: If your applications are a mix of Python and SPL (Streams Processing Language) code, a local installation of Streams is required.

<a id="setup"></a>

## Set up your development environment

To get your development environment ready:

1. Install Python on your local development environment. <b>The version of Python you install must be supported by the Streams instance.</b> 
2. Install the `streamsx` Python package.
3. Install a Java 1.8 JRE, if you do not already have one. 

See the following sections for more information on these steps.

### Install a supported version of Python 
<a id="python"></a>
Make sure you have the right version of Python for your Streams instance:

* For the **[Streaming Analytics service](https://cloud.ibm.com/catalog/services/streaming-analytics)** in IBM Cloud, use Python **3.6**.
* For **a local installation** of IBM Streams, Python **3.5, 3.6 or 3.7** are supported.
* **IBM Cloud Pak for Data**:
  - The Streams add-on is pre-configured with Python 3.6, so **install Python 3.6.**
  - For a standalone installation of Streams, make sure you install, at a minimum, the same version of Python installed with Streams.


### Install the `streamsx` package
<a id="streamsx"></a>
1. Use *pip* to install `streamsx`:

        pip install streamsx

    if `streamsx` is already installed, upgrade to the latest version:

          pip install --upgrade streamsx
2. Set the `JAVA_HOME` environment variable to a Java 1.8 JRE or JDK/SDK.

**For the most complete instructions regarding installation**, including when a local installation of Streams is required, see the
 [developer setup page of the streamsx project documentation](https://streamsxtopology.readthedocs.io/en/stable/pysetup.html).

<a id="connect"></a>

## Set up a connection to the Streams instance

A Streams Python application, or `Topology`, must always be compiled and run on a Streams instance. 

After defining the application, **you programmatically submit the `Topology` to the Streams instance** to be compiled and run using the [`streamsx.topology.context.submit` function](https://streamsxtopology.readthedocs.io/en/stable/streamsx.topology.context.html#streamsx.topology.context.run).

Below is sample code that you can use to connect to the Streams instance and submit your `Topology`.  So copy it now and add it to your Python script or as a cell in your notebook.

You will see an example of how this sample code is used later in this tutorial.


{% include python/config/submit_overview.html%}


# Create your first application

Now you are ready to [create your first application with the Streams Python API](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-3/).


The application will ingest temperature readings from a simulated sensor and compute the rolling average reading for each sensor.

## Learn more about the API

After you create your first application, visit the [Process data with common Streams transforms](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-4/) section to learn more about the API.
