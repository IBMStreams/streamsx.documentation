---
layout: docs
title: Introduction to Streams development for edge analytics
navtitle: Introduction
description: IBM® Streams can be used to develop and build applications for edge analyics using IBM Edge Analytics Beta on Cloud Pak for Data.
weight: 45
published: true
tag: edge
next:
  file: edgeanalytics/kafka-options
  title: Apache Kafka options for edge applications
---

IBM® Streams can be used to develop and build applications for edge analytics using IBM Edge Analytics Beta on Cloud Pak for Data.


For more information about Edge Analytics, see the [IBM Edge Analytics Beta on Cloud Pak for Data](https:// https://www.ibm.com/support/knowledgecenter/SSQNUZ_3.0.1/svc-welcome/edge.html) documentation.

## Getting Started

To get started creating a Streams application for edge analytics, view one or more Streams edge samples:

* Basic Edge Samples - simple, hello-world like application that you can deploy to the edge
  * [Edge Rolling Average sample](https://github.com/IBMStreams/sample.edge-rolling-average) - A Python notebook that computes the rolling average of a set of sensor values on an edge system.
  * [Edge Application Control sample](https://github.com/IBMStreams/sample.edge-app-control) - A Streams Processing Language (SPL) application that performs some basic analytics on the edge.  This sample also illustrates how to pass parameters and set runtime options for edge applications.
* Multi-tier Samples - an application that runs on edge systems, and another application that runs on the Cloud Pak for Data control plane (CP4D Hub).
  * [Edge Digit-Recognition notebook sample](https://github.com/IBMStreams/sample.edge-mnist-notebook) - An edge application written in a Python notebook uses a machine-learning model to identify hand-drawn integers.  Results from the model scoring at the edge are sent to another notebook running in the the CP4D Hub.
  * [Edge Digit-Recognition Streams Flows sample](https://github.com/IBMStreams/sample.edge-mnist) - Similar to the Edge Digit Recognition sample except that the edge application is constructed using the Streams Flows visual builder.
  * [Edge Network Analysis sample](https://github.com/IBMStreams/sample.netflow) - The Netflow sample collects and aggregates network traffic data.  It is written in Streams Processing Language (SPL) and can deployed in many different configurations (on-premise, cloud, edge, etc.)  Instructions have been added explaining how to build the sample using VS-Code deploy the collection and aggregation portion of the sample to edge systems.

For more information about develop and building edge applications using IBM Streams, see [Moving analytics to the edge with Edge Analytics](https://www.ibm.com/support/knowledgecenter/SSQNUZ_3.0.1/svc-edge/usage.html).

## Transferring data from the edge

One way to communicate data from edge applications to a central cloud platform, service, or application is through a data feed or messaging system like Apache Kafka. See [Apache Kafka options for edge applications](kafka-options) for a list of a few possible Kafka installation options and how to interface with those options in your edge applications using Streams toolkits.
