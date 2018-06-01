---
layout: docs
title:  Release Notes for IBM Streams Runner for Apache Beam
navtitle: Reference
description:  Learn about the IBM® Streams Runner features and changes by release.
weight:  10
published: true
tag: beam

prev:
  file: issues
  title: Limitations and known issues
---
View the features and changes of Streams Runner from release to release. Any items marked *Experimental* are subject to change between releases

## v1.2.1
Includes all features and bug fixes from v1.1.1
### New Functionality:
* Support for Apache Beam 2.4 Java SDK
* Support bundling of elements by size and timeout
* Support for componentized logging
    * Allow users to specify trace levels for translation-time and/or runtime separately
* Support for parallel pipelines and transforms (*Experimental*)
    * Allow users to specify parallelism at translation-time

### Improvements:
* Migrated provided samples to Maven project
* `--jarsToStage` option now support wildcards for filenames
* Fast failure if required submission parameters are missing
* Automatic Streams SDK jar inclusion to Streams Application Bundle
* Metrics can now be quiered after job cancellation from Beam application
* GroupByKey and Stateful ParDo garbage collection
* Add default factories for `--userName` and `--restUrl`
* Allow `--userPassword` to specify path to file containing password
* Add helpful detail to Streams Runner compile/submission messages
* Optimizations for ParDos using multiple side inputs or marked as sinks
* Optimizations for timer handling

### Deprecation:
The Swift FileSystem has been removed form the Streams SDK due to IBM Cloud service deprecation
* Beam now provides S3 I/O which can be used to read/store files to an IBM Cloud Object Storage S3 service

### Bug Fixes:
* Race condition in GroupByKey
* GroupByKey processes max watermark without all timers cleared


## v1.1.1
For details of v1.1, see [v1.1.0 release notes](#v110)
### Bug Fixes:
* Fix submission-time parameters being ignored


## v1.1.0
### New Functionality:
* Support for Apache Beam 2.1 Java SDK
* Support for new IAM authentication for Streaming Analytic services

### Improvements:
* Smarter selection of Stateful ParDo usage
* Stateful ParDos perform state/timer clean up
* Reduced watermark overhead for several transforms
* Various documentation enhancements

### Bug Fixes:
* User-defined teardown methods not invoked
* Global windowing with `Repeatedly.forever` trigger gets stuck
* Deadlock in GroupByKey while firing processing timers


## v1.0.0
### New Functionality:
* Support for Apache Beam 2.0 Java SDK
* Support primitive and custom composite Beam transforms
* Support for custom Beam metrics
    * Counter, Distribution, and Gauge types
    * Watermark metrics are automatically created for you
* Support for processing-time and event-time timers and window triggers
* Support for stateful processing
* Support for custom parameters specified at runtime of applications
* Integration into the Streams Platform
    * Remotely build and submit a translated Beam application to a Streaming Analytics service (no Streams installation required)
    * Locally build and submit a translated Beam application to a local Stream instance (supports Streams v4.2 and higher)
    * Locally build a Stream Application Bundle (SAB) to submit to a Streams instance of Streaming Analytics service later
    * Support for local files in distributed execution
    * Support to cancel Streams job from Beam application
    * View Beam Pipeline layouts in the Streams Graph
* Specialized Beam SDK for Streams
    * Publish or subscribe data streams for other Streams applications to utilize or for your application to consume
    * Read/write files to an IBM Object Storage Swift instance
