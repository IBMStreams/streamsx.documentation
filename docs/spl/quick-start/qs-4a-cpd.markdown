---
layout: docs
title: Monitoring IBM Streams applications with Cloud Pak for Data
description: How to use the Job Graph and other tools in IBM Cloud Pak for Data to monitor Streams applications
weight: 80
published: true
tag: spl-qs
navlevel: 2

next:
  file: qs-4b-console
  title:  Monitoring with Streams Console

prev:
  file: qs-4
  title:  Monitoring Streams applications
---

If you submitted a job to run on an IBM Streams instance in IBM Cloud Pak for Data (CPD), you can monitor and manage the application from the CPD user interface.  This page discusses some of the features available and how to use them.

To monitor an application using the Streams extension for VS Code instead, [see the documentation](https://ibmstreams.github.io/vscode-ide/docs/building-running-applications/#job-graph)

This guide will cover:

*   [Viewing the Streams job](#open)
*   [Working with the job in the Job Graph ](#jobgraph)
*   [Downloading logs](#logs)
*   [Canceling the job](#cancel)


<a id="open"></a>

## Viewing a Streams job in Cloud Pak for Data

To monitor or manage a job, you first need to find the job in the Cloud Pak for Data user interface.

Follow these steps to open the job details in your version of CPD.

You need the job name and job ID, which are displayed whenever you submit the job from VS Code or Streams Console.


{% include spl/cpd/job-details-cpd-main.html %}


<a id="jobgraph"></a>

## Working with the job in the Job Graph 
The Job Graph displays the graph of the application and provides tools for monitoring it. 

You can also use the Job Graph to:

- View the application graph
- Observe operator health, metrics and congestion
- Download trace information for an individual operator.
- View a sample of the data flowing through your application by examining data in the view panel.

### Viewing the application graph

Streams applications are directed graphs that analyze data as it is processed. Each node in the graph is an **operator** that processes data, and each line between operators is a **stream** of live data. 

<img alt="application Graph in cpd" src="/streamsx.documentation/images/qse/graph-cpd.jpg"/>

The streams in the graph are color coded to help you easily understand the current status of your application.

<img alt="legend for streams" src="/streamsx.documentation/images/qse/job-graph-legend.png"/>


### Additional Job Graph features

This screencast shows some features of the Job Graph and how to use them.

<img alt="Job Graph in cpd" src="/streamsx.documentation/images/qse/job-graph-gif.gif"/>



#### Watch Operator/Stream metrics

Hover over a stream or an operator to view information about it and its metrics. To pin the metrics so they are always visible, right-click the operator or stream and click **Watch**.


<a id="logs"></a>

## Downloading logs

Follow the [steps](#open) described earlier in this page to find the job and then download its logs. 

Logs will be downloaded as an archive. Unpack the archive and examine files with name matching `<hostname>/<jobs>`.


<a id="views"></a>

## Observe streaming data with Views

{% include spl/views_overview.md %}


### Displaying an existing View

When the Job Graph opens, any Views already defined in the application are visible in the View Pane. 

![view pane](/streamsx.documentation/images/qse/view-pane.png)

If the View Pane is not visible, right-click anywhere in the canvas and click **Show Views**.

![show views](/streamsx.documentation/images/qse/show-views.png)

Choose the view you want to see from the drop-down menu.


### Adding a view to a running application

To see the data on any Stream in the Job Graph, you can add a view:

1.  Right-click on the Stream and select **View data > Create new view**.
2.  The new view should appear in the View Pane.
  ![new view](/streamsx.documentation/images/qse/new-view-cpd.png)

If the **View data** action is not visible in the menu, the Stream does not support adding a View at runtime. 

<a id="cancel"></a>

## Cancel a running job

To cancel a running job, select **Delete job** from the Job Graph.

<img alt="cancel job cpd" src="/streamsx.documentation/images/qse/delete-job-graph.png"/>


## Summary

This page has a summary of the Job Graph. The Streams Console has more advanced features. See the [next section](/streamsx.documentation/docs/spl/quick-start/qs-4b-console) to learn more.
