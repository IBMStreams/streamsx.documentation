---
layout: docs
title: Installing Python APIs
description: Prerequisites and installation instructions for the Python Application API
weight:  20
published: true
tag: py16
prev:
  file: python-appapi-devguide
  title: Introduction
next:
  file: python-appapi-devguide-2a
  title: Create an application for the Streaming Analytics service
---


# Setup instructions

For developing with the Python API, at the very minimum you need to install a supported version of Python and the `streamsx` package.

##  Supported versions of Python

Make sure you have the right version of Python for your Streams instance:

* For the **[Streaming Analytics service](https://cloud.ibm.com/catalog/services/streaming-analytics)** in IBM Cloud, use Python **3.6**.
* For **a local installation** of IBM Streams, Python **3.5, 3.6 or 3.7** are supported.
* For **[IBM Cloud Private for Data](https://docs-icpdata.mybluemix.net/docs/content/SSQNUZ_current/com.ibm.icpdata.doc/streams/intro.html)**, use Python **3.6**.


##  Install the `streamsx` package
Use *pip* to install `streamsx`:

        pip install streamsx

If `streamsx` is already installed, upgrade to the latest version:

        pip install --upgrade streamsx

**Note:** For the most up to date instructions regarding installation, including when a local installation of Streams is required, see the
 [developer setup page of the streamsx project documentation](https://streamsxtopology.readthedocs.io/en/stable/pysetup.html).

# Create your first application

To get started with the Python Application API, you'll create an application that reads data from a temperature sensor and prints the output.

Choose one of the following tutorials to create your first application for:

* The [**IBM Streaming Analytics service**](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-2a/)
* [**A local installation of IBM Streams**](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-3/)
* [**IBM Cloud Private for Data**](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-2b/)

## Learn more about the API

After you create your first application, visit the [Process data with common Streams transforms](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-4/) section to learn more about the API.
