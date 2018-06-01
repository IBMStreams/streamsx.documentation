---
layout: docs
title:  Using IBM Streams Runner for Apache Beam
navtitle: Using the runner
description:  To use IBM® Streams Runner for Apache Beam, its libraries must be available to the Beam application  when the application is executed. Additionally, you must select a context that tells the runner how to build and submit the Beam application. Lastly, as with any Beam pipeline, you must specify any custom application parameters or additional runner parameters.
weight:  10
published: true
tag: beam
prev:
  file: beamrunner-2-install
  title: Installing
next:
  file: io
  title: I/O options
---

To use IBM® Streams Runner for Apache Beam, its libraries must be available to the Beam application  when the application is executed. Additionally, you must select a context that tells the runner how to build and submit the Beam application. Lastly, as with any Beam pipeline, you must specify any custom application parameters or additional runner parameters.

## Before you start

After you develop your Apache Beam 2.4 application, you must package your app as a JAR file to use it with Streams Runner. For example, if you use the `jar` command, enter the following command:

```bash
jar cf target.jar -C <path to class files>
```

## Enabling Streams Runner

To make the Streams Runner libraries available to the Beam application, you must do the following items when you submit the application:
- Include the `com.ibm.streams.beam.translation.jar` file that is located at `$STREAMS_BEAM_TOOLKIT/lib` in your Java™ class path.
- Specify the Beam pipeline parameter `--runner=StreamsRunner`.

## Selecting the Streams context

After Streams Runner is accessible to your application, you must decide in which context you want to build and submit your application. Streams Runner has three contexts, and each has its own set of prerequisites and setup requirements. The three contexts are `STREAMING_ANALYTICS_SERVICE`, `DISTRIBUTED`, and `BUNDLE` and are  specified by using the `--contextType` parameter.

### The `STREAMING_ANALYTICS_SERVICE` context
Use this context to build and submit an application to a Streaming Analytics service on IBM Cloud (formerly IBM Bluemix). `STREAMING_ANALYTICS_SERVICE` is the default context type.

**Tip:** This context is the simplest to use because it doesn't require you to install and configure Streams software; you can use the Streaming Analytics service, which includes the latest features and patches, that you created before you downloaded the Streams Runner toolkit.

#### Prerequisites
- A running Streaming Analytics service.
- A Streaming Analytics service credentials file.
- The `STREAMS_INSTALL` environment variable is unset.

#### Overview

To authenticate and select the Streaming Analytics service to submit to, you must specify the following information:

- The location of the [IBM Cloud credentials file](../../../beamrunner-2b-sas/#creating-a-credentials-file-for-your-streaming-analytics-service).  
Use the `--vcapServices` parameter or `VCAP_SERVICES` environment variable.
- The specific service name.  
Use the `--serviceName` parameter or `STREAMING_ANALYTICS_SERVICE_NAME` environment variable.

Because the application is launched on a remote system, the Streams job must be
aware of your Beam application. To include your application and any dependencies,
use the `--jarsToStage` option. For more information about this option, see [Streams Runner pipeline options](../reference/#streams-runner-pipeline-options).

**Note**: Fat or uber JAR files can reduce the number of JAR files to stage. Be mindful to not include dependencies that are already provided by Streams Runner. Including redundant dependencies can increase the application archive size and affect upload and build times.

#### Example

This example submits `MyBeamApplication` to the `my-service-name` Streaming Analytics service on IBM Cloud.

**Note**: This example uses the `--vcapServices` and `--serviceName` parameters, but these parameters aren't necessary if their respective environment variables are set.
Additionally, the `--contextType` parameter can be omitted because `STREAMING_ANALYTICS_SERVICE` is the default.

```bash
java -cp $STREAMS_BEAM_TOOLKIT/lib/com.ibm.streams.beam.translation.jar:/home/beamuser/beamapp/lib/myapp.jar \
    namespace.MyBeamApplication \
    --runner=StreamsRunner \
    --contextType=STREAMING_ANALYTICS_SERVICE \
    --vcapServices=/home/beamuser/streaming-analytics.vcap \
    --serviceName=my-service-name \
    --jarsToStage=/home/beamuser/beamapp/lib/myapp.jar
```

#### Limitations
- If your Beam application writes output to a file, you can’t retrieve output files that are written to a local file system in a Streaming Analytics service. You must configure the application to write output files to object storage instead.

   For information about retrieving files from an IBM Cloud Object Storage service, see [Object storage on IBM Cloud](../io/#object-storage-on-bluemix-swift).
- You can't download Streams application bundle (SAB) files of your Beam applications that are built remotely.

### The `DISTRIBUTED` context
Use this context to build an application locally and submit it to a local Streams instance.

**Tip:**  To ensure that you're getting the latest features and patches, use the `STREAMING_ANALYTICS_SERVICE` context instead.

#### Prerequisites
* A local Streams installation (IBM Streams 4.2 or higher).
* A running Streams domain and instance. For more information, see [Creating an IBM Streams basic domain and instance](https://www.ibm.com/support/knowledgecenter/en/SSCRJU_4.2.1/com.ibm.streams.cfg.doc/doc/creating-basic-domain-and-instance.html).

**Tip:** You can obtain a local Streams installation by installing the [IBM Streams Quick Start Edition](../../../..//4.2/qse-intro/), which is a Red Hat Enterprise Linux virtual machine image that is preconfigured to create and start a Streams runtime environment.

#### Overview
To launch a Beam application to a local, distributed Streams environment, set `DISTRIBUTED` as the
context type. Additionally, because the Beam application is being built locally, you must include the `com.ibm.streams.operator.samples.jar` located at `$STREAMS_INSTALL/lib` in the Java class path.

When the application is launched in a distributed environment, the Streams job must be
aware of your Beam application. To include your application and any dependencies, use the `--jarsToStage` option. For more information about this option, see [Streams Runner pipeline options](../reference/#streams-runner-pipeline-options).

For a Beam application that interacts with the job after it is launched, the application must authenticate with the Streams domain to use the Streams REST API. The domain can be authenticated by using the `--restUrl`, `--userName`, and `--userPassword` parameters.

**Important:** The Streams Console uses a self-signed certificate, which also affects
REST API authentication for some applications. To avoid any problems, generate and
add a trusted certificate for the client host. For more information, see [Configuring security for the IBM Streams REST API](https://www.ibm.com/support/knowledgecenter/en/SSCRJU_4.2.1/com.ibm.streams.dev.doc/doc/restapi-cfgauth.html).

The Streams application is submitted to the Streams domain and instance that are specified by
the `STREAMS_DOMAIN_ID` and `STREAMS_INSTANCE_ID` environment variables. If the domain and instance are not started or do not exist, the application submission fails.

#### Example

This example builds and submits `MyBeamApplication` locally.

```bash
java -cp $STREAMS_BEAM_TOOLKIT/lib/com.ibm.streams.beam.translation.jar:$STREAMS_INSTALL/lib/com.ibm.streams.operator.samples.jar:/home/beamuser/beamapp/lib/myapp.jar \
    namespace.MyBeamApplication \
    --runner=StreamsRunner \
    --contextType=DISTRIBUTED \
    --jarsToStage=/home/beamuser/beamapp/lib/myapp.jar \
    --restUrl=https://myStreamsHost:8443/streams/rest \
    --userName=beamuser \
    --userPassword=streams1
```

### The `BUNDLE` context
Use this context to locally build an application that can be submitted to a Streams runtime environment later.

#### Prerequisites
* A local Streams installation (IBM Streams 4.2 or higher).

**Remember:** Applications that will be submitted to a Streaming Analytics service must be built using the correct Red Hat Enterprise Linux environment. To check the correct operating system version, see the **Plan** tab on your Streaming Analytics service dashboard and the features of your selected plan.

#### Overview
Set the context type to `BUNDLE` to create an application bundle file and a Streams job configuration overlay file (_namespace.application_\_JobConfig.json) for your Beam application. Because the Beam application is packaged locally, you must include the `com.ibm.streams.operator.samples.jar` located at `$STREAMS_INSTALL/lib` in the Java class path.

Because the application is eventually launched in a distributed environment, the Streams job must be
aware of your Beam application. To include your application and any dependencies,
use the `--jarsToStage` option.

If your Beam application uses the Beam [ValueProvider](https://beam.apache.org/documentation/sdks/javadoc/2.4.0/org/apache/beam/sdk/options/ValueProvider.html) types for custom pipeline options,
Streams submission-time parameters are created for the application.

After the application bundle file is created, it can be submitted along with any submission-time parameters to a Streaming Analytics service or local Streams environment through the Streams Console, Streaming Analytics REST API, or `streamtool` command. For more information about bundle submission, see the `$STREAMS_RUNNER_HOME/examples/README` file.

#### Example

This example builds `MyBeamApplication` locally and creates an application bundle file for later submission to a Streaming Analytics service or a local Streams instance.

```bash
java -cp $STREAMS_BEAM_TOOLKIT/lib/com.ibm.streams.beam.translation.jar:$STREAMS_INSTALL/lib/com.ibm.streams.operator.samples.jar:/home/beamuser/beamapp/lib/myapp.jar \
    namespace.MyBeamApplication \
    --runner=StreamsRunner \
    --contextType=BUNDLE \
    --jarsToStage=/home/beamuser/beamapp/lib/myapp.jar
```

## Specify additional parameters
After you select your context, perform any necessary setup, and specify required parameters, you can add your application or additional Streams Runner parameters as needed. For example, if your Beam application reads input from a file, you can include the file in the application bundle to be available in the Streaming Analytics service or Streams instance environment by using the `--filesToStage` parameter.

For more information about input/output options, see [Input/output options for IBM Streams Runner for Apache Beam](../io).

For the full list of Streams Runner options, see [General pipeline options](../reference/#general-pipeline-options).
