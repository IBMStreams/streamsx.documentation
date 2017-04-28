---
layout: docs
title: 1.0 Installing
description: Prerequisites and installation instructions for the Python Application API
weight:  20
published: true
tag: py14
prev:
  file: python-appapi-devguide
  title: Developing IBM Streams Applications with Python
next:
  file: python-appapi-devguide-3
  title: 2.0 Developing your first application
---

Before you can use the Python Application API, you must complete the following tasks:

1. Install IBM Streams Version 4.0.1 (or later) or IBM Streams Quick Start Edition Version 4.0.1 (or later):

    * [IBM Streams Version 4.2.0 installation documentation](http://www.ibm.com/support/knowledgecenter/SSCRJU_4.2.0/com.ibm.streams.install.doc/doc/installstreams-container.html)

    * [IBM Streams Quick Start Edition Version 4.2.0 installation documentation](http://www.ibm.com/support/knowledgecenter/SSCRJU_4.2.0/com.ibm.streams.qse.doc/doc/installtrial-container.html)

1. Ensure that you configure the IBM Streams product environment variable by entering the following command:

        source product-installation-root-directory/4.n.n.n/bin/streamsprofile.sh

    **Tip:** Add the source command to your `home-directory/.bashrc` shell initialization file. Otherwise, you must enter the command every time you start IBM Streams. For example, if the product is installed in the `/home/streamsadmin/InfoSphere_Streams/4.2.0.0` directory, add the following line to your `.bashrc` file:

        source /home/streamsadmin/InfoSphere_Streams/4.2.0.0/bin/streamsprofile.sh


1. Download the IBM Streams Topology toolkit, which includes the Python Application API. You can download the most recent version of the toolkit from the IBMStreams organization on GitHub from the streamsx.topology [Releases page](https://github.com/Ibmstreams/streamsx.topology/releases). *If you are using IBM Streams 4.2 or later then this step is optional as the toolkit is included at* `$STREAMS_INSTALL/toolkits/com.ibm.streamsx.topology`.

    After the toolkit downloads, extract it to your file system.

1. Install a supported version of Python. The Python Application API has been tested with Python 3.5.1. You can choose from one of these options:

   * *Recommended* - Anaconda 4.0.0 or later, which includes Python 3.5.0 [https://www.continuum.io/downloads](https://www.continuum.io/downloads).

   * CPython 3.5.0 or later [https://www.python.org](https://www.python.org).

     If building Python from source, remember to pass `--enable-shared` as a parameter to  `configure`.  After installation, set `LD_LIBRARY_PATH` to `Python_Install>/lib`.

   To build IBM Streams application bundles with the Python Application API that can be submitted to your Bluemix Streaming Analytics service you **must**:
     * use Anaconda 4.1.1 (Python 3.5 version) or later
     * install Anaconda at `/disk1/opt/Anaconda3` on the machine where you execute the Python code that builds the topology and submits it to the `BUNDLE` context

1. Include the fully qualified path of the `com.ibm.streamsx.topology/opt/python/packages` directory in the PYTHONPATH environment variable. For example:

        export PYTHONPATH=/home/myuser/download/com.ibm.streamsx.topology/opt/python/packages:$PYTHONPATH
