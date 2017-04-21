---
layout: docs
title:  6.0 The Python REST API
description:  Learn how to use the Python REST API to monitor and interact with streams resources
weight: 60
published: true
tag: py16
prev:
  file: python-appapi-devguide-5
  title: "5.0 API features: User-defined parallelism"
---

Depending on the problem at hand, a developer may choose to create an IBM Streams application in a particular programming language. To this end, the streamsx.topology project supports APIs in Java, Scala, Python, and SPL. However, regardless of the language used to develop and submit the application, it becomes necessary to monitor the application while it is running. By monitoring, we mean to observe runtime information regarding the application or its environment, for example:

* Whether a job is running, stopped, or even exists
* Whether the instance containing a job is running or stopped; in other words, are additional jobs even able to be submitted
* Metrics of a stream such as flow rate or congestion
* Individual tuples on a stream, potentially for purposes of data visualization

This information is exposed through the Python REST API in the `streamsx.rest` module. Furthermore, the REST API is not strictly read only as it also supports the cancellation of remote jobs. This guide walks through some of the most common use cases for the API, but also aims to give users a more general understanding for types of applications which can be written.

# Creating a StreamsConnection

The primary abstraction in the Python REST API is the `StreamsConnection` class -- every application which seeks to use the REST API must first create an instance of this class. To create a `StreamsConnection`, pass a valid Streams username and password to the constructor:

```
>>> from streamsx import rest
>>> sc = rest.StreamsConnection(username="streamsadmin", password="passw0rd")
```

By default, the `StreamsConnection` connects to a local streams install. Users who are connecting to the Streaming Analytics service on Bluemix, should instead instantiate a subclass of `StreamsConnection` called `StreamingAnalyticsConnection`. Instead of a username and password, the constructor arguments should include the path to a `vcap` file, and the name of the Streaming Analytics service:

```
>>> from streamsx import rest
>>> sc = rest.StreamingAnalyticsConnection("/home/streamsadmin/vcap.json", "Streaming Analytics-be")
```

The `StreamsConnection` retrieves runtime information about your application via HTTP. By default, SSL authentication is enabled. To disable it, type `sc.session.verify = False` immediately after creading your `StreamsConnection`.

# Retrieving Resources Elements

The `StreamsConnection` object represents the root in a tree of resource elements, where each node in the tree is a resource that can be queried to retrieve its state. If we look at the methods exposed by `StreamsConnection`, we see several related to obtaining a resource element:

```
sc.get_instance()
sc.get_instances()
sc.get_resources()
sc.get_domain()               
sc.get_domains()            
sc.get_installations()
```

Each of these methods, when invoked, retrieves up-to-date information about a resource in the form of a Python object. For example, an IBM Streams instance is the container in which jobs are executed. The `get_instance` method retrieves the resource element containing current information about an instance; including the instance's owner, status, and the time it was started.

```
>>> from streamsx import rest
>>> sc = rest.StreamingAnalyticsConnection("/home/streamsadmin/vcap.json", "Streaming Analytics-be")
>>> instance = sc.get_instance(id="MyStreamsInstance")
>>> print(instance.owner, instance.status, instance.startTime)
streamsdomainowner running 1492194564662 

```

The `instance.status` field reflects whether or not the instance is running. An instance whose status is `stopped` is not currently able to run jobs. The following is an example of all information which can be obtained from the `instance` resource.

```
>>> from streamsx import rest
>>> sc = rest.StreamingAnalyticsConnection("/home/streamsadmin/vcap.json", "Streaming Analytics-be")
>>> instance = sc.get_instances()[0]
>>> print(instance.json_rep)
'activeServices': 'https://streams-console-c6d1.ng.bluemix.net/streams/rest/instances/dd5f603a-7fb1-4e9b-861c-e15542e2d423/activeservices',
'activeVersion': {'architecture': 'x86_64',
				'buildVersion': '20170323145113',
				'editionName': 'IBM Streams',
				'fullProductVersion': '4.2.1.0',
				'minimumOSBaseVersion': '6',
				'minimumOSPatchVersion': '6',
				'minimumOSVersion': 'Red Hat Enterprise Linux '
									'Server release 6.6 '
									'(Santiago)',
				'productName': 'IBM Streams',
				'productVersion': '4.2.0.0'},
'activeViews': 'https://streams-console-c6d1.ng.bluemix.net/streams/rest/instances/dd5f603a-7fb1-4e9b-861c-e15542e2d423/activeviews',
'configuredViews': 'https://streams-console-c6d1.ng.bluemix.net/streams/rest/instances/dd5f603a-7fb1-4e9b-861c-e15542e2d423/configuredviews',
'creationTime': 1485540669058,
'creationUser': 'streamsdomainowner',
'domain': 'https://streams-console-c6d1.ng.bluemix.net/streams/rest/domains/standard1',
'exportedStreams': 'https://streams-console-c6d1.ng.bluemix.net/streams/rest/instances/dd5f603a-7fb1-4e9b-861c-e15542e2d423/exportedstreams',
'health': 'healthy',
'hosts': 'https://streams-console-c6d1.ng.bluemix.net/streams/rest/instances/dd5f603a-7fb1-4e9b-861c-e15542e2d423/hosts',
'id': 'dd5f603a-7fb1-4e9b-861c-e15542e2d423',
'importedStreams': 'https://streams-console-c6d1.ng.bluemix.net/streams/rest/instances/dd5f603a-7fb1-4e9b-861c-e15542e2d423/importedstreams',
'jobs': 'https://streams-console-c6d1.ng.bluemix.net/streams/rest/instances/dd5f603a-7fb1-4e9b-861c-e15542e2d423/jobs',
'operatorConnections': 'https://streams-console-c6d1.ng.bluemix.net/streams/rest/instances/dd5f603a-7fb1-4e9b-861c-e15542e2d423/operatorconnections',
'operators': 'https://streams-console-c6d1.ng.bluemix.net/streams/rest/instances/dd5f603a-7fb1-4e9b-861c-e15542e2d423/operators',
'owner': 'streamsdomainowner',
'peConnections': 'https://streams-console-c6d1.ng.bluemix.net/streams/rest/instances/dd5f603a-7fb1-4e9b-861c-e15542e2d423/peconnections',
'pes': 'https://streams-console-c6d1.ng.bluemix.net/streams/rest/instances/dd5f603a-7fb1-4e9b-861c-e15542e2d423/pes',
'resourceAllocations': 'https://streams-console-c6d1.ng.bluemix.net/streams/rest/instances/dd5f603a-7fb1-4e9b-861c-e15542e2d423/resourceallocations',
'resourceType': 'instance',
'restid': 'dd5f603a-7fb1-4e9b-861c-e15542e2d423',
'self': 'https://streams-console-c6d1.ng.bluemix.net/streams/rest/instances/dd5f603a-7fb1-4e9b-861c-e15542e2d423',
'startTime': 1492194564662,
'startedBy': 'streamsdomainowner',
'status': 'running',
'views': 'https://streams-console-c6d1.ng.bluemix.net/streams/rest/instances/dd5f603a-7fb1-4e9b-861c-e15542e2d423/views'
```

A complete reference for the types of resources and their fields can be found in the [IBM Streams Knowledge Center](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.2.0/com.ibm.streams.restapi.doc/doc/restapis.html). As previously mentioned, resource elements are arranged in a hierarchy. We can understand the child elements of the`instance` resource by inspecting its methods:

```
>>> instance.
inst.get_exported_streams(      inst.get_resource_allocations(
inst.get_hosts(                 inst.get_views(
inst.get_imported_streams(
inst.get_job(                   inst.refresh(
inst.get_jobs(                  
inst.get_operator_connections(  
inst.get_operators(             
inst.get_pe_connections(        
inst.get_active_services(       inst.get_pes(                   
inst.get_domain(                inst.get_published_topics(  
```

The presence of the `get_jobs` method indicates that the `job` resource is a child of the `instance` resource. Furthermore, the `operator` resource is a child of the `job` resource. To find the names of all operators associated with an instance, one could write the following script:

```
>>> from streamsx import rest
>>> sc = rest.StreamsConnection(username='streamsadmin', password='passw0rd')
>>> instance = sc.get_instances()[0]
>>> for job in instance.get_jobs():
...     for operator in instance.get_operators():
...         print(operator.name)
... 
identity
list_2
neural_net_model
Op.PublishTopic.TopicProperties
periodicSource
print_flush
```

# Cancelling jobs

The Python REST API is not strictly read only, the REST API also has the ability to cancel jobs. This functionality is exposed through the `job.cancel()` method. A user who wants to cancel a job could do so as follows:

```
>>> from streamsx import rest
>>> sc = rest.StreamsConnection(username='streamsadmin', password='passw0rd')
>>> instance = sc.get_instances()[0]
>>> job = instance.get_jobs()[0]
>>> if job.cancel():
...     print("The job was successfully canceled.")
... else:
...     print("Error canceling job.")
...
The job was successfully canceled.
```

Cancelling remote jobs has the benefit of freeing up resources; or, if the application is running as part of a test suite, to cancel the completed test.

# Accessing the Tuples of a View

Streaming applications process unbounded amounts of data in real time. Naturally, users might wish to have access to the data stream for purposes of visualization or additional monitoring. To this end, the Python REST API allows developers to retrieve the tuples of any Stream that has been created with a view. In the Python Application API, a view is created on a stream by calling the `view` method:

```
>>> from streamsx.topology import Topology
>>> top = Topology("myApplication")
>>> strm = top.source(["Hello", "world!"])
>>> strm.view(name="myView")
```

The last line of code, `strm.view()`, marks the `strm` stream as viewable, meaning we can access its tuples with the Python REST API. When the application is submitted, a `view` resource element is created as a child of `job` and `instance`. To find all views associated with an instance, we can call the `instance.get_views()` method:
```
>>> from streamsx import rest
>>> sc = rest.StreamsConnection(username='streamsadmin', password='passw0rd')
>>> instance = sc.get_instances()[0]
>>> views = instance.get_views()
>>> print(len(views))
2
```

Or, if we want to retrieve all views associated with a job, we can call the `jobs.get_views()` method:
```
>>> from streamsx import rest
>>> sc = rest.StreamsConnection(username='streamsadmin', password='passw0rd')
>>> instance = sc.get_instances()[0]
>>> job = instance.get_jobs()[0]
>>> views = job.get_views()
>>> print(len(views))
1
```

Each view can be created with a name. In the former code, we created a view called `myView`. We can locate the `myView` view by iterating through the list of views and checking whether the name matches:
```
>>> myView = None
>>> for view in views:
...     if view.name == "myView":
...         myView = view
...
>>> if myView:
...     print("Successfully located myView")
... else:
...     print("Could not locate myView")
Successfully located myView
```

Once the correct view is located, its data can be obtained by calling the `view.start_data_fetch()` method. `view.start_data_fetch()` returns a queue whose contents is updated to reflect the contents of the remote Stream. The queue is continuously populated by a background thread until `view.stop_data_fetch()` is invoked. The following is an example of how this would work in practice:

```
>>> queue = view.start_data_fetch()
>>> try:
...     for item in iter(queue.get, None):
...         print(item)
... except KeyboardInterrupt:
...     view.stop_data_fetch()
Hello
world!
^C
>>>
```

Going line by line, `queue = view.start_data_fetch()` begins fetching stream data from the remote view to populate the created `queue.` Next, `for item in iter(queue.get, None)` creates an iterator using the queue, and iterates over its values and simply printing them to the screen with `print(item)`. For the sake of this example, data is consumed until the user sends an interrupt with Control-C, although the user is free to decide when and how data stops being consumed. Lastly, when the user sends an interrupt, `view.stop_data_fetch()` is invoked which terminates the background thread, and data ceases to be retrieved from the remote view.

The ability to obtain live stream data from a running job has proved valuable for real time data visualization. For example, the stream could be sending temperature readings from an engine to be analyzed by a mechanic. High temperature readings could be a signal the limit the engine's maximum RPMs. Jupyter notebooks provide an ideal platform for performing this kind of visualization.


