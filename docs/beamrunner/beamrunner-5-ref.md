---
layout: docs
title:  Reference information for IBM® Streams Runner for Apache Beam
navtitle: Reference
description:  description
weight:  10
published: true
tag: beam
prev:
  file: beamrunner-4-monitor
  title: Monitoring
next:
  file: beamrunner-6-issues
  title: Limitations and known issues
---

Learn about the package contents and pipeline options for IBM Streams Runner for Apache Beam.

## Package contents for Streams Runner

The Streams Runner package contains the following folders:

- `com.ibm.streams.beam`: The IBM Streams Runner for Apache Beam toolkit, which you can use to submit Beam applications to the IBM Streams runtime environment.

- `samples`: Toolkit sample applications. For information about the samples, see the README file in the samples folder.

## Pipeline options for Streams Runner

### General pipeline options

| Parameter | Description | Default value |
| --- | --- | --- |
| `runner` | The pipeline runner to use. Use this option to determine the pipeline runner at run time. | Set this option to `StreamsRunner` to run with IBM Streams. |
| `streaming` | A flag to indicate whether streaming mode is enabled (`true`). <br /><br />Note: IBM Streams is a pure streaming engine and does not have a discrete batch-processing mode. For this reason, this parameter is ignored and is automatically set to `true`.  | `True`  |
| `jobName` | The name of the job. | Defaults to a Beam-generated string. |
| `appName` | The name of the app for display purposes. | Defaults to the class name of the PipelineOptions creator. |

### Streams Runner pipeline options

| Parameter | Description | Default value |
| --- | --- | --- |
| `contextType` | The mode to run the application in:<ul><li>STREAMING\_ANALYTICS\_SERVICE: Compile a Streams application bundle (SAB) file remotely and submit the translated pipeline to a Streaming Analytics service on IBM Bluemix. </li><li>DISTRIBUTED: Submit the pipeline to a Streams instance. The domain and instance are configured by the STREAMS\_DOMAIN\_ID and STREAMS\_INSTANCE\_ID environment variables.</li><li>BUNDLE: Create a Streams application bundle (SAB) file for submission at a later time.</li></ul> | `STREAMING\_ANALYTICS\_SERVICE` |
| `jarsToStage` | A list of JAR files (separated by colons) that are required to run the Apache Beam application. Include the JAR files that contain your program and any dependencies. (You don't need to include Beam Google IO SDK or core Beam JAR files.) The listed JAR files are added to the SAB file.<br /><br />Note: The use of fat or uber JAR files increases the size of the SAB file and can negatively impact submission times to IBM Bluemix.  | [null] |
| `filesToStage` | The JSON files with local file paths as keys and destination paths as values. For example, <br /> ``--filesToStage="{\"/path/to/local/file\": \"input/file1.in\", \"path/to/another/local/file\": \"env.conf\"}"``<br /><br />  In this example, the two local files are added into the bundle at the specified destination paths, which can then be accessed by using ``"streams://input/file1.in"`` and ``"streams://env.conf"`` paths. | [null] |
| `beamToolkitDir` | The location of the Streams Runner toolkit. Use this option to explicitly specify the Streams Runner toolkit location. | Defaults to the path of the `com.ibm.streams.beam.translation.jar` file in the Java `classpath`. |
| `tracingLevel` | Set the tracing and logging level of StreamsRunner translation and runtime. Levels: ERROR, WARN, INFO, DEBUG, TRACE  | Defaults to the path of the `com.ibm.streams.beam.translation.jar` file in the Java `classpath`. |
| `textIOBundleSize` | The user password for basic authentication for REST API when you use the `DISTRIBUTED` context type. | `WARN` |

### STREAMING\_ANALYTICS\_SERVICE context-specific pipeline options
| Parameter | Description | Default value |
| --- | --- | --- |
| `vcapServices` | The location of the Streaming Analytics VCAP file. This parameter is required when you use the `STREAMING\_ANALYTICS\_SERVICE` context type.This parameter can be omitted if the `$VCAP\_SERVICES` environment variable is set to the path of the file. | [null] |
| `serviceName` | The name of the Streaming Analytics service on Bluemix. This parameter is required when you use the STREAMING\_ANALYTICS\_SERVICE context type. | [null] |

### DISTRIBUTED context-specific pipeline options

| Parameter | Description | Default value |
| --- | --- | --- |
| `restUrl` | The URL for the REST API when you use the `DISTRIBUTED` context type. This parameter is required if you implement metrics in the application. | [null] |
| `userName` | The user name for basic authentication with REST API when you use the `DISTRIBUTED` context type. | [null] |
| `userPassword` | The user password for basic authentication for REST API when you use the `DISTRIBUTED` context type. | [null] |

For the full list of pipeline options, enter  `--help=StreamsPipelineOptions` on the Beam application command line.
