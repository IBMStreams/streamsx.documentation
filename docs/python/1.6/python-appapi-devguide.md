---
layout: docs
title:  Developing IBM Streams Applications with Python
description:  Learn how to develop a sample IBM Streams application in Python by using the the Python Application API in the Topology Toolkit
weight:  10
published: true
tag: py16
next:
  file: python-appapi-devguide-2
  title: Installing Python APIs
---

The IBM Streams Python Application API enables you to create streaming analytics applications in [Python](https://python.org). The API is open source from the [streamsx.topology](http://ibmstreams.github.io/streamsx.topology/) project on GitHub.


## About streaming applications

Streaming applications are intended to run indefinitely because they meet the need for real-time data processing. (This is in contrast to applications created for the Apache Hadoop framework, which are intended to terminate when a batch of data is successfully processed.)

For example, consider a company whose product scans temperature sensors across the world to determine weather patterns and trends. Because there is always a temperature, there is a perpetual need to process data. The application that processes the data must be able to run for an indefinite amount of time.

The application must also be scalable. If the number of temperature sensors doubles, the application must double the speed at which it processes data to ensure that analysis is available in a timely manner.

Applications created with the Python API can:

 - Ingest data from Apache Kafka, Apache HBase, IBM Db2 Warehouse, IBM Event Streams, and more.
 - [Analyze data using Windows](/streamsx.documentation/docs/python/1.6//python-appapi-devguide-4/#windows)
 - [Run in parallel](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-5/)
 - Support data recovery in event of system failure.


You can use the Python Application API to define the structure of a streaming application using Python.

This development guide will show you how to create streaming applications using Python.
# Get started

To get started with the Python Application API, follow the steps in the next section [to install the API and create your first application](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-2/).


### Reference information

#### Which data sources are supported?

There are Python packages that provide support for common data sources like Apache Kafka or Hadoop File System. [See the adapters section for a list](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-4/#adapters)


* For full reference, see the [documentation for the Python Application API](https://streamsxtopology.readthedocs.io/en/stable/).
* Documentation for older releases is available on the [releases page of the streamsx.topology project](https://github.com/IBMStreams/streamsx.topology/releases).

### Terminology
If you're new to IBM Streams and want to learn more about the terms in this guide, see the [IBM Streams glossary](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.glossary.doc/doc/glossary_streams.html) in IBM Knowledge Center.
