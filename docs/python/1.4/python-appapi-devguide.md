---
layout: docs
title:  Developing IBM Streams Applications with Python (Version 1.4)
description:  Learn how to develop a sample IBM Streams application in Python by using the the Python Application API in the Topology Toolkit
weight:  10
published: true
tag: py14
next:
  file: python-appapi-devguide-2
  title: 1.0 Installing
---

Python is a popular language with a large and comprehensive standard library as well as many [third-party libraries](https://pypi.python.org). The IBM Streams Python Application API enables you to create streaming analytics applications in Python.

The API is open source from the [streamsx.topology](http://ibmstreams.github.io/streamsx.topology/) project on GitHub. IBM Streams 4.2 ships with a release of `com.ibm.streamsx.topology` toolkit which contains the Python Application API.

This guide covers the high-level concepts of streaming application development with Python. The guide also walks you through the process of creating a sample application to help you get more familiar with how to create an IBM Streams application with Python.

When you create an IBM Streams application written in Python, you can run the application in the following modes:

* As a **Streams distributed application** (DISTRIBUTED). When running in this mode, the application produced will be deployed automatically on your IBM Streams instance.
* As a **Streams Application Bundle file** (BUNDLE). When running in this mode, the application produces a SAB file that you can then deploy on your IBM Streams or Bluemix Streaming Analytics service instance by using the `streamtool submitjob` command or by using the application console
* As a **stand-alone application** (STANDALONE).  When running in this mode, the application produces a Streams Application Bundle file (SAB file), but rather than submitting the SAB file to an instance, the bundle is executed. The bundle runs within a single process and can be terminated with Ctrl-C interrupts.


The Python Application API enables you to:

* Define the structure of a streaming application using Python
* Pass Python objects as tuples on a stream
* Define how streaming data is processed in a modular, scalable, and stateful manner

The sample applications in this guide illustrates each of these points in more detail.

If you'd prefer to dig in to the Pydoc yourself, you can find the documentation in the following installation directories:

* `com.ibm.streamsx.topology/doc/pydoc/streamsx.topology.context.html`
* `com.ibm.streamsx.topology/doc/pydoc/streamsx.topology.topology.html`


**Terminology**
If you're new to IBM Streams and want to learn more about the terms in this guide, see the [IBM Streams glossary](http://www.ibm.com/support/knowledgecenter/SSCRJU_4.2.0/com.ibm.streams.glossary.doc/doc/glossary_streams.html) in IBM Knowledge Center.

