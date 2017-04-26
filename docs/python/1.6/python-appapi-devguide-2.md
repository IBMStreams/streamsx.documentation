---
layout: docs
title: 1.0 Installing Python APIs
description: Prerequisites and installation instructions for the Python Application API
weight:  20
published: true
tag: py16
prev:
  file: python-appapi-devguide
  title: Developing IBM Streams Applications with Python
next:
  file: python-appapi-devguide-2a
  title: 2.0 Developing for the IBM Streaming Analytics service
---

The Python language support package is shipped with IBM Streams. You can also download the latest package as part of the com.ibm.streamsx.topology toolkit or as a stand-alone streamsx Python package. You can use either the toolkit or the Python package, the only difference between them is how you download them.

* Topology toolkit (com.ibm.streamsx.topology)

  The topology toolkit comes with IBM Streams 4.2 or later. It's located in: `$STREAMS_INSTALL/toolkits/com.ibm.streamsx.topology`.
  <br>You can download the latest version of the toolkit from <https://github.com/IBMStreams/streamsx.topology/releases/latest>.

* Stand-alone streamsx Python package

  The streamsx Python package is available for download from <https://pypi.python.org/pypi/streamsx>. You can install it with the **pip** command:

        pip install streamsx
