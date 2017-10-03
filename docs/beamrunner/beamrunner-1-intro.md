---
layout: docs
title:  Introduction to IBM® Streams Runner for Apache Beam
navtitle: Introduction
description:  Introduction to IBM® Streams Runner for Apache Beam
weight:  10
published: true
tag: beam
next:
  file: beamrunner-2-install
  title: Installing
---

You can use IBM Streams Runner for Apache Beam to execute Apache Beam 2.0 pipelines in an IBM Streams environment. A Beam  application that is launched with Streams Runner is translated into a Streams Application Bundle (SAB) file. It is then optionally submitted to an existing IBM Streams domain and instance or to an IBM Streaming Analytics service in IBM Bluemix.

You can use a simple application called `TemperatureSample` to learn how to submit and monitor a Beam application in the Streaming Analytics service on Bluemix.  The sample application is included with Streams Runner. Some familiarity with Beam programming is helpful, though not required; the [Apache Beam website](https://beam.apache.org/) has a useful [Apache Beam Java SDK Quickstart](https://beam.apache.org/get-started/quickstart-java/) page and other documentation.
