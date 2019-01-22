---
layout: docs
title: SPL development guide for Atom
description:
tag: atom
weight: 45
published: true
next:
  file: atom/atom-guide-1-configure
  title: Configure Atom
---


This development guide will cover using the [Atom editor](https://atom.io) to create and
develop applications written in Streams Processing Language (SPL).

Follow this guide if you want to learn about Streams and SPL without downloading and
installing the Streams runtime.

To get started with Streams using a local installation, see the [Getting
Started with the Streams Quick Start Edition](/streamsx.documentation/docs/latest/qse-intro) page.

Prerequisites
-------------

If you are completely new to Streams, read the Quick Start Guide for a
basic introduction. Then you can return to this guide to:

-   Configure Atom/VSCode for development

-   Run a sample application to see Streams in action

-   Create your own applications from scratch

**Note**: This guide will only cover creating Streams applications using
SPL. See the Python development guide or the Java development guide to
learn about development in those languages.

If you would rather use VSCode, the development guide for that editor is
coming soon.

Table of Contents
-----------------

-   Overview

-   Configure Atom

-   Get your code into Atom

-   Get Familiar With the Editor

-   Creating a Streams application from scratch

-   Running an application

-   Adding a toolkit

-   Where to find samples

-   Appendix/Troubleshooting

Create an instance of the Streaming Analytics service
---------------------

Instead of downloading the Streams compiler and runtime to create your
applications, you will use the Streaming Analytics service, a cloud
based version of Streams. Applications created in Atom are sent to the
Streaming Analytics to be compiled and executed.

So, the first step is to [create an instance of the service in the IBM Cloud Catalog](https://console.bluemix.net/catalog/services/streaming-analytics).
