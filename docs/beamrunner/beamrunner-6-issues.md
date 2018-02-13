---
layout: docs
title:  Limitations and known issues for IBM Streams Runner
navtitle: Limitations and known issues
description:  Learn about limitations and known issues for IBM® Streams Runner for Apache Beam.
weight:  10
published: true
tag: beam
prev:
  file: beamrunner-5b-objstor
  title: Using IBM Cloud Object Storage
---

Learn about limitations and known issues for IBM® Streams Runner for Apache Beam.

## Limitations

- Streams Runner does not support the Beam Python SDK.
- Experimental Splittable ParDos are not supported.

## Known issues
### Issue
Submission-time parameters that are specified when you manually submit a SAB file (created by using the `BUNDLE` context) are not used during application runtime.

#### Workaround
Use the `STREAMING_ANALYTICS_SERVICE` or `DISTRIBUTED` contexts to launch the application with the application options set.

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
