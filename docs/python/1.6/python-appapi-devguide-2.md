---
layout: docs
title: Installation and Setup
description: Prerequisites and installation instructions for the Python Application API
weight:  20
published: true
tag: py16
prev:
  file: python-appapi-devguide
  title: Introduction
next:
  file: python-appapi-devguide-3
  title: Create your first application
---


# Setup instructions
These are the basic requirements to create Streams applications with Python:

1. [Set up a Streams instance](#streams)
2. Set up your development environment:
  - [Install a supported version of Python](#python)
  - [Install the `streamsx` package](#streamsx)


### Set up a Streams instance
<a id="streams"></a>

The Python API is used to create a **Topology**, or application that is executed by the Streams runtime.
The Streams runtime can be in the public or private cloud or installed locally.
Choose the tab that matches where your Streams instance is installed and follow the steps to install and/or configure the Streams instance.


<ul class="nav nav-tabs">
  <li class="active"><a data-toggle="tab" href="#cpd"><b>IBM Cloud Pak for Data</b></a></li>
  <li><a data-toggle="tab" href="#sas"><b>Streaming Analytics service in IBM Cloud</b></a></li>
   <li><a data-toggle="tab" href="#local"><b>Local installation</b></a></li>
</ul>

<div class="tab-content">



  <div id="cpd" class="tab-pane fade  in active ">
<!--- Cloud pak for data ---->

{% include cpd_install.html%}

 </div>


<div id="sas" class="tab-pane fade">
<!--- STREAMING ANALYTICS SERVICE ---->
{% include sas_install.html%}


</div>

<div id="local" class="tab-pane fade">
{% include local_install.html%}
 </div>


 </div>

<br/><br/>
**Note**: You must install Streams on your computer (local installation) if your applications are a mix of Python and SPL (Streams Processing Language) code.


## Set up your development environment
### Install a supported version of Python
<a id="python"></a>
Make sure you have the right version of Python for your Streams instance:

* For the **[Streaming Analytics service](https://cloud.ibm.com/catalog/services/streaming-analytics)** in IBM Cloud, use Python **3.6**.
* For **a local installation** of IBM Streams, Python **3.5, 3.6 or 3.7** are supported.
* **IBM Cloud Pak for Data**:
  - The Streams add-on is pre-configured with Python 3.6, so **install Python 3.6.**
  - For a standalone installation of Streams, make sure you install, at a minimum, the same version of Python installed with Streams.


### Install the `streamsx` package
<a id="streamsx"></a>
1. Use *pip* to install `streamsx`:

        pip install streamsx

    if `streamsx` is already installed, upgrade to the latest version:

          pip install --upgrade streamsx
2. Set the `JAVA_HOME` environment variable to a Java 1.8 JRE or JDK/SDK.

**Note:** For the most up to date instructions regarding installation, including when a local installation of Streams is required, see the
 [developer setup page of the streamsx project documentation](https://streamsxtopology.readthedocs.io/en/stable/pysetup.html).

# Create your first application

To get started with the Python Application API, you'll create an application that reads data from a temperature sensor and prints the output.

Choose one of the following tutorials to create your first application for:

* The [**IBM Streaming Analytics service**](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-2a/)
* [**A local installation of IBM Streams**](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-3/)
* [**IBM Cloud Pak for Data**](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-2b/)

## Learn more about the API

After you create your first application, visit the [Process data with common Streams transforms](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-4/) section to learn more about the API.
