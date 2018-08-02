---
layout: docs
title:  Limitations and known issues for IBM Streams Runner
navtitle: Limitations and known issues
description:  Learn about limitations and known issues for IBM® Streams Runner for Apache Beam.
weight:  10
published: true
tag: beam
prev:
  file: troubleshoot
  title: Troubleshooting
next:
  file: release-notes
  title: Release notes
---

Learn about limitations and known issues for IBM® Streams Runner for Apache Beam.

## Limitations

- Streams Runner does not support the Beam Python SDK.
- Experimental Splittable ParDos are not supported.

## Known issues
### Issue
The Streams job for a submitted Beam application does not show the Pipeline layout in the Streams Graph in the IBM Streams Console.

#### Workaround
Click on the 'Configure' icon (the wrench) in the Streams Graph for your application, check the 'Show raw graph' option, and click 'Apply' to see the Pipeline using all primitive transforms.

Additionally, use the latest version of IBM Streams (which contains the latest Streams Console) to run your Beam application. The latest version can be obtained in the [Quick Start Edition]().

### Issue

The local Java™ installation is the outdated Java 8.0u31 (a release from 2015) and the Streams JRE version is 8.0u93 (from 2016).

This difference in versions causes the following error to be displayed when you run a Streams job in `DISTRIBUTED` mode:

```
java.io.InvalidClassException: org.apache.beam.runners.core.SystemReduceFn$1;
local class incompatible: stream classdesc serialVersionUID = -7628843818184175876,
local class serialVersionUID = 2067056052611054708
```

#### Workaround
Choose one of the following options:
- Export `JAVA_HOME` to the internal IBM Streams Java Runtime Environment (JRE) found at `$STREAM_INSTALL/java/`.
- Update your Java installation.
