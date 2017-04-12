---
layout: docs
title: 1.0 Installing
description: Prerequisites and installation instructions for the Python Application API
weight:  20
published: true
tag: py16
prev:
  file: python-appapi-devguide
  title: Developing IBM Streams Applications with Python
next:
  file: python-appapi-devguide-3
  title: 2.0 Developing your first application
---

Before you can create your first Python application with the Python Application API and a local version of IBM Streams, you must complete the following setup tasks:

1. Install version 4.0.1 (or later) of IBM Streams or IBM Streams Quick Start Edition:

    * [IBM Streams Version 4.2.0 installation documentation](http://www.ibm.com/support/knowledgecenter/SSCRJU_4.2.0/com.ibm.streams.install.doc/doc/installstreams-container.html)

    * [IBM Streams Quick Start Edition Version 4.2.0 installation documentation](http://www.ibm.com/support/knowledgecenter/SSCRJU_4.2.0/com.ibm.streams.qse.doc/doc/installtrial-container.html)

1. Ensure that you configure the IBM Streams product environment variable by entering the following command:

        source product-installation-root-directory/4.n.n.n/bin/streamsprofile.sh

    **Tip:** Add the source command to your `home-directory/.bashrc` shell initialization file. Otherwise, you must enter the command every time you start IBM Streams. For example, if the product is installed in the `/home/streamsadmin/InfoSphere_Streams/4.2.0.0` directory, add the following line to your `.bashrc` file:

        source /home/streamsadmin/InfoSphere_Streams/4.2.0.0/bin/streamsprofile.sh


1. If you are using IBM Streams 4.2 or later, you can skip this step because the Python Application API is included  at* `$STREAMS_INSTALL/toolkits/com.ibm.streamsx.topology`. <br><br>If you are using an earlier version of IBM Streams, you must: 
    1. Download the latest version of the IBM Streams Topology toolkit from the IBMStreams organization on GitHub from the streamsx.topology [Releases page](https://github.com/Ibmstreams/streamsx.topology/releases).
    1. After the toolkit downloads, extract it to your file system.

1. Install a supported version of Python:

   * *Recommended* - Anaconda 4.0.0 or later, which includes Python 3.5.0 [https://www.continuum.io/downloads](https://www.continuum.io/downloads).
   
   * CPython 3.5.0 or later [https://www.python.org](https://www.python.org).

   The Python Application API was tested with Python 3.5.1.
   
   **Important:** To build IBM Streams application bundles with the Python Application API that can be submitted to your IBM Streaming Analytics service you **must**:
     * Use Anaconda 4.1.1 (Python 3.5 version) or later.
     * Install Anaconda at `/disk1/opt/Anaconda3` on the machine where you execute the Python code that builds the topology and submits it to the `BUNDLE` context.

1. Include the fully qualified path of the `com.ibm.streamsx.topology/opt/python/packages` directory in the PYTHONPATH environment variable. For example:

        export PYTHONPATH=/home/myuser/download/com.ibm.streamsx.topology/opt/python/packages:$PYTHONPATH
