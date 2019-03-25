---
layout: docs
title:  Developing IBM Streams Applications with Python (v1.12)
description:  Learn how to develop a sample IBM Streams application in Python by using the the Python Application API in the Topology Toolkit
weight:  10
published: true
tag: py16
next:
  file: python-appapi-devguide-2
  title: Installing Python APIs
---

Python is a popular language with a large and comprehensive standard library as well as many [third-party libraries](https://pypi.python.org).

The IBM Streams Python Application API enables you to create streaming analytics applications in Python. The API is open source from the [streamsx.topology](http://ibmstreams.github.io/streamsx.topology/) project on GitHub.

You can use the Python Application API to:

* Define the structure of a streaming application by using Python.
* Pass Python objects as tuples on a stream.
* Define how streaming data is processed in a modular, scalable, and stateful manner.
* Specify the mode in which you want the streaming application to run.

You can run a streaming application in the following modes:

* In a **Streaming Analytics service running on IBM Cloud** (STREAMING_ANALYTICS_SERVICE). In this mode, the application is run in the cloud in a Streaming Analytics service. The Streaming Analytics service is a cloud version of IBM Streams, so you don't need to install Streams to build Python applications for the service.
* In the **IBM Streams add-on in IBM Cloud Private for Data** (DISTRIBUTED). The application is developed in a Jupyter notebook and deployed to the IBM Streams add-on instance.
* As a **Streams distributed application** (DISTRIBUTED). When running in this mode, the application is deployed automatically on your local IBM Streams instance.
* As a **Streams Application Bundle file** (BUNDLE). When running in this mode, the application produces a Streams Application Bundle (SAB) file that you can then deploy on your IBM Streams instance or Streaming Analytics service instance by using the `streamtool submitjob` command or by using the application console.
* As a **stand-alone application** (STANDALONE).  When running in this mode, the application produces a SAB file, but rather than submitting the SAB file to an instance, the bundle is executed. The bundle runs within a single process and can be terminated with Ctrl-C interrupts.


**Note**: The Python API is the same across all scenarios, the only differences involve how the application is deployed.

This development guide will show you how to create streaming applications using Python.

## About streaming applications

Streaming applications are intended to run indefinitely because they meet the need for real-time data processing. (This is in contrast to applications created for the Apache Hadoop framework, which are intended to terminate when a batch of data is successfully processed.)

For example, consider a company whose product scans temperature sensors across the world to determine weather patterns and trends. Because there is always a temperature, there is a perpetual need to process data. The application that processes the data must be able to run for an indefinite amount of time.

The application must also be scalable. If the number of temperature sensors doubles, the application must double the speed at which it processes data to ensure that analysis is available in a timely manner.

# Get started

To get started with the Python Application API, follow the steps in the next section [to install the API and create your first application](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-2/).

### Reference information
* For full reference, see the [documentation for the Python Application API](https://streamsxtopology.readthedocs.io/en/stable/).
* Documentation for older releases is available on the [releases page of the streamsx.topology project](https://github.com/IBMStreams/streamsx.topology/releases).

### Terminology
If you're new to IBM Streams and want to learn more about the terms in this guide, see the [IBM Streams glossary](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.glossary.doc/doc/glossary_streams.html) in IBM Knowledge Center.
