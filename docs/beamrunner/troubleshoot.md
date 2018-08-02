---
layout: docs
title:  Troubleshooting IBM Streams Runner for Apache Beam
navtitle: Troubleshooting
description: You can troubleshoot any issues that occur when you launch, run, or monitor IBM® Streams Runner for Apache Beam applications.
weight:  10
published: true
tag: beam
prev:
  file: performance
  title: Performance considerations
next:
  file: issues
  title: Limitations and known issues
---

You can troubleshoot any issues that occur when you launch, run, or monitor IBM® Streams Runner for Apache Beam applications. Streams Runner includes several pipeline parameters and componentized options to print more information and help narrow the scope to a specific component. 

## Ensure you have the latest fixes
The latest Streams Runner version is 1.2.1. You can [download](../../../beamrunner-2b-sas/#creating-a-streaming-analytics-service-on-ibm-cloud) the latest Streams Runner installation archive from an IBM Streaming Analytics container-based service. 

## Check known problems and solutions
See if your problem matches any issues in the [issues and limitations page](../issues).

## Enable tracing
Tracing can give information about the translation and execution of your Beam application and can help debug problems.

### Trace levels
Streams Runner tracing levels follow SLF4J's levels of `ERROR`, `WARN`, `INFO`, `DEBUG`, and `TRACE` with increasing verbosity and information.

### Translation-time tracing
Streams Runner uses Beam utilities and the [streamsx.topology](http://ibmstreams.github.io/streamsx.topology/) toolkit to translate your Beam application into a Streams application, submit the application to your IBM Streams instance or IBM Streaming Analytics service, and provide connections to the instance or service for monitoring or cancellation. Log messages about these activites are printed to the console where the Beam program is executed. When you specify the program command, you can use the `--traceTranslation` pipeline option to specify a trace level for the runner, topology toolkit, and global scopes. For example, you can debug a SAB compilation (a SAB file is compiled by using the topology toolkit) without verbose Beam or Streams Runner translation logging by specifying `--traceTranslation=INFO,Streams=DEBUG`.

By default, Streams Runner uses `INFO` level tracing during translation and the topology toolkit and Beam loggers are set to `WARN`. The `INFO` level displays messages that can be helpful during your application preparation and submission. For information about seeting the tracel level for the runner, topology, or global (for Beam and its dependencies) loggers, see the description of `traceTranslation` in [Streams Runner pipeline options](../reference/#streams-runner-pipeline-options).

### Runtime tracing
When your application is successfully submitted and started on a Streams environment, the application uses the tracing levels set by `--traceRuntime`. All messages, including standard output and error, are logged to log files on the distributed environment. After the job is running, you can change the application trace level for individual operators (transforms), processing elements (PEs), or the entire job from Streams Console. For more information about viewing, downloading application logs, or changing trace levels from Streams Console, see the [Troubleshooting section of the Streaming Analytics Development Guide](https://developer.ibm.com/streamsdev/docs/bluemix-streaming-analytics-development-guide/#troubleshooting).

You can set the Streams Runner runtime component separately from the global trace levels, in the same way you set translation-time logging. By default, the runtime trace level is set to `WARN`. For more information, see `traceRuntime` in [Streams Runner pipeline options](../reference/#streams-runner-pipeline-options). **Note**: increasing runtime trace levels can negatively impact performance of an application.

For a complete IBM Streams troubleshooting guide, see [Troubleshooting and support](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.pd.doc/doc/ts_parent.html).

## Have questions?
If you have any questions regarding Streams Runner, you can post a question to the [StreamsDev forum](https://developer.ibm.com/answers/smartspace/streamsdev/index.html).
