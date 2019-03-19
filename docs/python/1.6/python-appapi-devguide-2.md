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


If you are developing applications that will run within **IBM Cloud Private for Data**, the Streams Python API is already installed.

For all other scenarios, the [streamsx package](https://pypi.python.org/pypi/streamsx) from PyPi contains the Python language support. Install `streamsx` using **pip**:

        pip install streamsx

If it is already installed, upgrading to the latest version is recommended:

        pip install --upgrade streamsx


**Note:** The Streaming Analytics service only supports Python 3.5.


## Create your first application

To get started with the Python Application API, you'll create an application that reads data from a temperature sensor and prints the output.

Choose a tutorial to create your first application on:

* The [**IBM Streaming Analytics service**](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-2a/) (Python 3.5 only).
* [**A local installation of IBM Streams**](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-3/)
* [**IBM Cloud Private for Data**](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-2b/)

## Learn more about the API
After creating your first application, visit the [common Streams transforms](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-4/) section to learn more about the API.
