---
layout: docs
title:  Working with SPL toolkits
description:  "Learn how to integrate SPL toolkits in your Python application."
weight: 60
published: true
tag: py16
prev:
  file: python-appapi-devguide-6
  title: "The Python REST API"
---


If you are familiar with Streams Processing Language (SPL) and want instructions to use SPL composites and operators, use the [Streams-SPLToolkitsTutorial.ipynb](https://github.com/IBMStreams/sample.starter_notebooks/blob/latest/Streams-SPLToolkitsTutorial.ipynb) notebook.

Run this [tutorial](https://github.com/IBMStreams/sample.starter_notebooks/blob/latest/Streams-SPLToolkitsTutorial.ipynb) notebook in a Cloud Pak for Data project. The tutorial notebook includes the following tasks:

* Discover toolkits that are installed on the Streams build service
* Launch the SPL main composite
* Work with microservices
* Integrate SPL operators in a Python topology

IBM Streams provides adapters to external systems, analytics and streaming primitives in SPL toolkits shipped with the IBM Streams product.

*When do you need to integrate SPL toolkits in your Python topology?*

Integrate existing SPL toolkits in your Python topology to speed up development of your streaming application. When you need to use C++ or Java libraries for a certain adapter or analytics task, create your custom SPL toolkit with operators invoking specialized libraries.

Python packages that wrap SPL toolkits and provide an API to use in your Python Topology:

* Apache Kafka integration - [streamsx.kafka](https://streamsxkafka.readthedocs.io/)
* Database integration - [streamsx.database](https://streamsxdatabase.readthedocs.io/)
* Geospatial analytics- [streamsx.geospatial](https://streamsxgeospatial.readthedocs.io/)
* MQTT integration - [streamsx.mqtt](https://streamsxmqtt.readthedocs.io/)
* Cloud Object Storage integration - [streamsx.objectstorage](https://streamsxobjectstorage.readthedocs.io/)
* Streaming primitives - [streamsx.standard](https://streamsxstandard.readthedocs.io/)

A full list of available packages is at: [https://pypi.org/search?q=streamsx](https://pypi.org/search?q=streamsx)

# Adding toolkits to your application

If your Topology contains invocations of SPL operators, for example from your own custom toolkit, then their defining toolkit must be made known using [streamsx.spl.toolkit.add_toolkit](https://streamsxtopology.readthedocs.io/en/stable/streamsx.spl.toolkit.html#streamsx.spl.toolkit.add_toolkit).

Toolkits shipped with the IBM Streams product are implictly known.

When do you need to use **streamsx.spl.toolkit.add_toolkit**?

1. You invoke SPL operators of a custom toolkit in your Topology.
2. You invoke SPL operators of an open source toolkit from GitHub that is not shipped with the product, for example [com.ibm.streamsx.nlp](https://github.com/IBMStreams/streamsx.nlp)
3. You need to use a newer version of a Streams toolkit, for example using latest release from GitHub with new features.

The sample code below, download the **nlp** toolkit from GitHub and adds this toolkit to the bundle loaded to the Streams build service when you submit your topology:

~~~python
import streamsx.toolkits as tkutils
nlp_tk = tkutils.download_toolkit('com.ibm.streamsx.nlp')
from streamsx.spl.toolkit import add_toolkit
add_toolkit(topo, nlp_tk)
~~~

When you build your application more frequent or other users shall use the new|custom|updated toolkit, then it might make sense to upload the toolkit to the build service.
As soon as the toolkit has been uploaded to the Streams build service, it will be known when building your Streams application.

# Uploading toolkits to the Streams Build Service

You have developed your own SPL toolkit, or you want to use an open source toolkit from [IBMStreams GitHub](https://github.com/search?q=topic:toolkit+org:IBMStreams&type=Repositories) or you want to update a product toolkit on the Streams build service in Cloud Pak for Data, then you can upload a toolkit in order to have it available when building your Streams applications.

## Integrated configuration within project

In your analytics notebook, you can upload a toolkit to the build service using the `streamsx.build` module.

The sample below, downloads the latest release of the 'com.ibm.streamsx.iot' toolkit from [IBMStreams GitHub](https://github.com/IBMStreams/streamsx.iot) into a temporary folder and uploads this toolkit to the Streams build service.

~~~python
import streamsx.toolkits as tkutils
iot_tk = tkutils.download_toolkit('com.ibm.streamsx.iot') # downloads the latest release from GitHub
from streamsx.build import BuildService
from streamsx.topology import context
cfg[context.ConfigParams.SSL_VERIFY] = False
buildService = BuildService.of_service(cfg)
buildService.upload_toolkit(iot_tk) # uploads the toolkit to the build service
~~~

You can verify that the new version is present, with

~~~python
build_service_toolkits = tkutils.get_build_service_toolkits(cfg)
print(build_service_toolkits)
~~~


## External connection to Cloud Pak for Data

Use [streamsx-streamtool]() command line tool, when you connect from external to the Cloud Pak for Data.

The following steps are an example, how to download the 'com.ibm.streamsx.iot' toolkit from public GitHub and upload the toolkit to the Streams build service.

1. Download the [toolkit 1.3.0 tarball](https://github.com/IBMStreams/streamsx.iot/releases/download/v1.3.0/streamsx.iot.toolkits-1.3.0-20201208-1147.tgz) from the [toolkits release page](https://github.com/IBMStreams/streamsx.iot/releases/) on GitHub.

2. Change the directory to your download location and unpack the downloaded tarball: 

```
tar -zxf streamsx.iot.toolkits-1.3.0-20201208-1147.tgz
```

3. Upload the toolkit: 

```
streamsx-streamtool [--disable-ssl-verify] uploadtoolkit --path com.ibm.streamsx.iot
```

4. You can verify that the new version is present, with 

```
streamsx-streamtool [--disable-ssl-verify] lstoolkit --name com.ibm.streamsx.iot 
```

