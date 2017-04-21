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

The primary abstraction in the Python REST API is the `StreamsConnection` class -- every application which seeks to use the REST API must first create an instance of this class. An instance of a `StreamsConnection` contains the following notable methods and fields:

```
sc.get_instance()
sc.get_instances()
sc.get_resources()
sc.get_domain()               
sc.get_domains()            
sc.get_installations()       
sc.session
```

Each of these methods, when invoked, retrieves up-to-date information about a resource in the form of a Python object. For example, he `get_instance` method retrieves an object containing current information about a specific instance.

```
>>> from streamsx import rest
>>> sc = rest.StreamsConnection(username='streamsadmin', password='passw0rd')
>>> instance = sc.get_instance(id="MyStreamsInstance")
>>> print(instance.owner, instance.status, instance.startTime)
streamsdomainowner running 1492194564662 

```

You can see that the `instance.status` field reflects whether or not the instance is running. Similarly, the `get_domain` and `get_installations` methods will, respectively, return information about a domain or a list of instances. Each of these resources is arranged in a hierarchy; for example, the instance resource contains a list of jobs, while the jobs resource contains a list of operators. To find all jobs associated with an instance, one could write the following script:

```
>>> from streamsx import rest
>>> sc = rest.StreamingAnalyticsConnection("/tmp/vcap.json", "Streaming Analytics-be")
>>> instance = sc.get_instances()[0]
>>> for job in instance.get_jobs():
...     for operator in instance.get_operators():
...         print(operator.name)
... 

identity
neural_net_model
Op.PublishTopic.TopicProperties
periodicSource
print_flush
identity
list_2
neural_net_model
Op.PublishTopic.TopicProperties
periodicSource
print_flush
identity
list_2
neural_net_model
Op.PublishTopic.TopicProperties
periodicSource
print_flush
```


