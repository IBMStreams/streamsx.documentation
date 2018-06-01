---
layout: docs
title:  Installing IBM Streams Runner for Apache Beam
navtitle: Installing
description:  Installing IBM® Streams Runner for Apache Beam involves downloading and extracting the Streams Runner toolkit, configuring environment variables, and creating a credentials file for your Streaming Analytics service.
weight:  10
published: true
tag: beam
prev:
  file: beamrunner-1-intro
  title: Introduction
---

IBM® Streams Runner for Apache Beam is installed by extracting the Streams Runner toolkit. You can extract the toolkit from your IBM Streams v4.3 or later installation or you can download a Streams Runner installation archive from an IBM Streaming Analytics service on IBM Cloud. Additional configuration steps are required, depending on which option you choose.

## Before you start: Develop your application
Apache Beam applications can be developed without Streams Runner being installed. For information about developing your Beam application, see the [Beam SDK for Java](https://beam.apache.org/documentation/sdks/java/) and its [Java SDK Quickstart](https://beam.apache.org/get-started/quickstart-java/).

## Choose your Streams environment

### IBM Streams
Installing IBM® Streams Runner for Apache Beam from an installation of IBM Streams involves extracting the Streams Runner toolkit and configuring environment variables. For instructions, see [Installing IBM Streams Runner for Apache Beam from an IBM Streams on-premises installation](../beamrunner-2a-onprem).

### IBM Streaming Analytics service
Installing IBM® Streams Runner for Apache Beam from an IBM Streaming Analytics service on IBM Cloud involves downloading and extracting the Streams Runner toolkit, configuring environment variables, and creating a credentials file for your Streaming Analytics service. You don't need to install IBM Streams to use Streams Runner. For instructions, see [Installing IBM Streams Runner for Apache Beam from an IBM Streaming Analytics service on IBM Cloud](../beamrunner-2b-sas).
