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

Streaming applications meet the need for continuous, real-time data processing. (This is in contrast to applications created for the Apache Hadoop framework, which are intended to terminate when a batch of data is processed.)

For example, consider an application that scans temperature sensors across the world to determine weather patterns and trends. Because there is always a temperature, the application needs to perpetually process the data and will potentially run indefinitely.

You can create such an application with the Streams Python API. 
<form action="/streamsx.documentation/docs/python/1.6/python-appapi-devguide-2/" target="_blank"><input  type="submit" value="Create your first application"></form>


### Streams Python API Features

The API supports:

 - Data ingest from Apache Kafka, Apache HBase, IBM Db2 Warehouse, IBM Event Streams, and more.
 - [Streaming data analysis with Windows](/streamsx.documentation/docs/python/1.6//python-appapi-devguide-4/#windows)
 - [Parallel execution](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-5/)
 - Data recovery in event of system failure.

You can use the Python Application API to define the structure of a streaming application using Python.

This development guide will show you how to create streaming applications using Python.

#### Where will the Streams Python application run?

Applications created with the IBM Streams Python API are executed on an instance of IBM Streams. 

#### How can I get an instance of Streams?

 There are several ways to get an instance of Streams:

 - Use the **Streaming Analytics service running on IBM Cloud**: The Streaming Analytics service is a cloud version of IBM Streams, so you don't need to install Streams to build Python applications for the service. [Create a free instance of the Streaming Analytics service here](https://cloud.ibm.com/catalog/services/streaming-analytics).  The applications you create will run in the IBM Cloud.


 -  Enable the **IBM Streams add-on in IBM Cloud Pak for Data**: IBM Streams is included as an add-on in for IBM Cloud Pak for Data. Contact your administrator to enable the add-on.  Streams can also be installed as a stand-alone deployment on Red Hat OpenShift or Kubernetes environments.  
  
 - A **local installation of the Streams runtime**:  [Install version 4.2 or later of IBM Streams](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.install.doc/doc/installstreams-container.html) or the free [Streams Quick Start Edition](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.qse.doc/doc/installtrial-container.html). 

#### Which data sources are supported?

There are Python packages that provide support for common data sources like Apache Kafka or Hadoop File System. 

[See the adapters section for a list](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-4/#adapters).


# Get started

To get started with the Python Application API, follow the steps in the next section [to install the API and create your first application](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-2/).

#  More information 

* For full reference, see the [documentation for the Python Application API](https://streamsxtopology.readthedocs.io/en/stable/).
* Documentation for older releases is available on the [releases page of the streamsx.topology project](https://github.com/IBMStreams/streamsx.topology/releases).

### Terminology
If you're new to IBM Streams and want to learn more about the terms in this guide, see the [IBM Streams glossary](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.glossary.doc/doc/glossary_streams.html) in IBM Knowledge Center.
