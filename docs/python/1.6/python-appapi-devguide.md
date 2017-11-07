---
layout: docs
title:  Developing IBM Streams Applications with Python (Versions 1.6+)
description:  Learn how to develop a sample IBM Streams application in Python by using the the Python Application API in the Topology Toolkit
weight:  10
published: true
tag: py16
next:
  file: python-appapi-devguide-2
  title: 1.0 Installing
---

Python is a popular language with a large and comprehensive standard library as well as many [third-party libraries](https://pypi.python.org).

The IBM Streams Python Application API enables you to create streaming analytics applications in Python. The API is open source from the [streamsx.topology](http://ibmstreams.github.io/streamsx.topology/) project on GitHub.

You can use the Python Application API to:

* Define the structure of a streaming application by using Python.
* Pass Python objects as tuples on a stream.
* Define how streaming data is processed in a modular, scalable, and stateful manner.
* Specify the mode in which you want the streaming application to run.

You can run a streaming application in the following modes:

* In a **Streaming Analytics service running on IBM Bluemix** (STREAMING_ANALYTICS_SERVICE). In this mode, the application is run in the cloud in a Streaming Analytics service. The Streaming Analytics service is built on IBM Streams technology. You don't need a local version of IBM Streams to build Python applications for the service.
* As a **Streams distributed application** (DISTRIBUTED). When running in this mode, the application is deployed automatically on your local IBM Streams instance.
* As a **Streams Application Bundle file** (BUNDLE). When running in this mode, the application produces a Streams Application Bundle (SAB) file that you can then deploy on your IBM Streams instance or Streaming Analytics service instance by using the `streamtool submitjob` command or by using the application console.
* As a **stand-alone application** (STANDALONE).  When running in this mode, the application produces a SAB file, but rather than submitting the SAB file to an instance, the bundle is executed. The bundle runs within a single process and can be terminated with Ctrl-C interrupts.

To get started with the Python Application API, follow the tutorials in this guide to create a sample application that reads data from a temperature sensor and prints the output to the screen.
* One tutorial creates the application in your local Python environment so that the application runs in the IBM Streaming Analytics service and doesn’t require a local installation of IBM Streams.
* The other tutorial creates the same application that runs in stand-alone mode and requires a local installation of IBM Streams.

You can find the latest reference documentation for the Python Application API at: <https://ibmstreams.github.io/streamsx.topology/doc/pythondoc/index.html>.

Documentation for older releases is available on the [releases page of the streamsx.topology project](https://github.com/IBMStreams/streamsx.topology/releases).

### Terminology###
If you're new to IBM Streams and want to learn more about the terms in this guide, see the [IBM Streams glossary](http://www.ibm.com/support/knowledgecenter/SSCRJU_4.2.1/com.ibm.streams.glossary.doc/doc/glossary_streams.html) in IBM Knowledge Center.
