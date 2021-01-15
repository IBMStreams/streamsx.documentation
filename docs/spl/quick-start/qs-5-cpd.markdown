---
layout: docs
title: Monitoring IBM Streams applications with Cloud Pak for Data
description: How to use the Job Graph and other tools in IBM Cloud Pak for Data to monitor Streams applications
weight: 80
published: true
tag: spl-qs
navlevel: 2

next:
  file: qs-6-console
  title:  Monitoring with Streams Console

prev:
  file: qs-4
  title:  Tips for development
---

If you submitted a job to run on an IBM Streams instance in IBM Cloud Pak for Data (CPD), you can monitor and manage the application from the (CPD) user interface.  This page discusses some of the features available and how to use them.

To monitor an application using the Streams extension for VS Code instead, [see the documentation](https://ibmstreams.github.io/vscode-ide/docs/building-running-applications/#job-graph)


*   [Viewing the Streams job](#jobs)
*   [Working with the job graph ](#jobgraph)
*   [Downloading logs](#logs)


This screencast shows some features of the Job Graph and how to use them.

<img alt="job graph in cpd" src="/streamsx.documentation/images/qse/job-graph-gif.gif"/>
<a id="jobs"></a>

## Viewing a Streams job in Cloud Pak for Data

To download logs and open the job graph, you need to find the job in CPD.

Follow these steps to open the job details in your version of CPD.

You need the job name and job ID, which are displayed whenever you submit the job from VS Code or Streams Console.


{% include spl/cpd/job-details-cpd-main.html %}

<a id="open"></a>

## Working with the job graph

Follow the [steps](#jobs) described earlier in this page  open the Job Graph.

You can also use the job graph to:

- View the application graph
- Observe operator health, metrics and congestion
- Download trace information for an individual operator.
- View a sample of the data flowing through your application by examining data in the view panel.


#### The application graph

The Job Graph displays the graph of the application. 

Streams applications are directed graphs that analyze data as it is processed. Each node in the graph is an **operator** that processes data, and each line between operators is a **stream** of live data. 

<img alt="job graph in cpd" src="/streamsx.documentation/images/qse/graph-cpd.jpg"/>

The streams in the graph are color coded to help you easily understand the current status of your application.

<img alt="job graph in cpd" src="/streamsx.documentation/images/qse/job-graph-legend.png"/>



#### Watch Operator/Stream metrics

Hover over a stream or an operator to view information about it and its metrics. To pin the metrics so they are always visible, right-click the operator or stream and click **Watch**.


<a id="logs"></a>

## Downloading logs

Follow the [steps](#jobs) described earlier in this page to find the job and then download its logs. 

Logs will be downloaded as an archive. Unpack the archive and examine files with name matching `<hostname>/<jobs>`.


## Summary

This page has a summary of the job graph. The Streams Console has many more advanced features. See the [next section](/streamsx.documentation/docs/spl/quick-start/qs-6-console) to learn more.