---
layout: docs
title:  Using IBM® Streams Runner for Apache Beam
navtitle: Using the runner
description:  description
weight:  10
published: true
tag: beam
prev:
  file: beamrunner-2-install
  title: Installing
next:
  file: beamrunner-2b-wordcount
  title: Wordcount sample app
---

Using the Streams Runner requires being accessable to the Beam application when it is executed. Additionally, you need to select a mode informing the runner what it should do with the Beam application. Lastly, like with any Beam pipeline, you will need to specify any custom or additionaly runner parameters.

## Enable the Streams Runner
To allow Apache Beam 2.0 applications to utilize the Streams Runner, you must:
1. Include the `com.ibm.streams.beam.translation.jar` located at `$STREAMS_BEAM_TOOLKIT/lib` in your Java classpath.
2. Specify the Beam pipeline parameter `--runner=StreamsRunner`.

## Select the Streams Context

Once the Streams Runner is accessible to your application, you must decide what mode you want the runner to perform. The Streams Runner has three modes (called contexts) and each has its own set of prerequisities and setup. The three contexts are `STREAMING_ANALYTICS_SERVICE`, `DISTRIBUTED`, and `BUNDLE` and should be specified by using the `--contextType` parameter.

### The `STREAMING_ANALYTICS_SERVICE` Context (Recommended)
Build and submit applications to a Streaming Analytics service on IBM Bluemix

#### Prerequisites
1. Started Streaming Analytics service
2. Streaming Analytics service credentials file
3. STREAMS_INSTALL environment variable is unset

#### Overview
By default, the Streams Runner will use `STREAMING_ANALYTICS_SERVICE` 
as the context type and is recommended since you already created a service
in order to download the runner. 

This mode does *NOT* require that an IBM Streams installation be accessible on your system.

In order to authenticate and select the Streaming Analytics service to 
submit to, the file location to the [Bluemix credentials file](../beamrunner-2-install/#creating-a-credentials-file-for-your-streaming-analytics-service) needs to specified using the `--vcapServices` parameter or `VCAP_SERVICES` environment variable and the specific service name specified using the `--serviceName` parameter or `STREAMING_ANALYTICS_SERVICE_NAME` environment variable.

Since the application will be launched on a remote system, the Streams job needs to be
aware of your Beam application. To include your application and any dependencies it may need, 
use the `--jarsToStage` option. See the [Streams Runner pipeline options](../beamrunner-6-ref/#streams-runner-pipeline-options) for more details. NOTE: While fat/uber jars may be convenient to reduce the amount of jars to stage, doing
so will increase the size of the archive and affect upload and build times.

#### Example
The following example shows `--vcapServices` and `--serviceName` but do not need to be provided if 
their respective environment variables are set. Additionally, the `--contextType` parameter does
not need to be set since `STREAMING_ANALYTICS_SERVICE` is the default.
```
java -cp $STREAMS_BEAM_TOOLKIT/lib/com.ibm.streams.beam.translation.jar:/path/to/myapp.jar \
    namespace.MyBeamApplication \
    --runner=StreamsRunner \
    --contextType=STREAMING_ANALYTICS_SERVICE \
    --vcapServices=/path/to/credentials/file \
    --serviceName=my-service-name \
    --jarsToStage=/path/to/myapp.jar
```

#### Limitations
1. Output files written to local filesystem in a Streaming Analytics service cannot be retrieved 
   * See Using Swift IO to be able to retrieve files from a Bluemix Object Storage service
2. Stream Application Bundles (SABs) of your Beam applications built remotely cannot be downloaded

### The `DISTRIBUTED` Context
Build applications locally and submit it to a local Streams instance

**WARNING:** Running of Beam applications in a local environment is not recommended at this time. It is recommended to use a Streaming Analytics service which includes the latest features and patches.

#### Prerequisites
* Local Streams installation (IBM Streams 4.2 or higher)
* [Started Streams Domain and Instance](https://www.ibm.com/support/knowledgecenter/en/SSCRJU_4.2.1/com.ibm.streams.cfg.doc/doc/creating-basic-domain-and-instance.html)

Tip: You can obtain a local Streams install by installing the [IBM Streams Quick Start Edition](../../4.2/qse-intro/) which is a RHEL6 virtual machine image pre-configured to create and start a Streams runtime environment.

#### Overview
To launch a Beam application to a local, distributed Streams environment, set `DISTRIBUTED` as the 
context type. Additionally, since the Beam application is being built locally, you must include the `com.ibm.streams.operator.samples.jar` located at `$STREAMS_INSTALL/lib` in the Java classpath.

When the application is launched on a distributed environment, the Streams job needs to be
aware of your Beam application. To include your application and any dependencies it needs to
use the `--jarsToStage` option. See the [Streams Runner pipeline options](../beamrunner-6-ref/#streams-runner-pipeline-options) for more details.

For Beam applications that interact with the job once it is launched, the application will need to authenticate with the Streams domain to utilize the Streams REST API. The domain can be authenticated by using the `--restUrl`, `--userName`, and `--userPassword` parameters. 

**Warning:** The Streams Console uses a self-signed certificate. This also affects
REST API authentication for some applications. It is recommended to generate and
add a trusted certificate for the client host. See the [IBM Knowledge Center](https://www.ibm.com/support/knowledgecenter/en/SSCRJU_4.2.1/com.ibm.streams.dev.doc/doc/restapi-cfgauth.html)
for more information.

The Streams job will be submitted to the Streams domain and instance specified by 
the `STREAMS_DOMAIN_ID` and `STREAMS_INSTANCE_ID` environment variables. If the domain and instance are not started or do not exist, the application submission will fail.

#### Example
```
java -cp $STREAMS_BEAM_TOOLKIT/lib/com.ibm.streams.beam.translation.jar:$STREAMS_INSTALL/lib/com.ibm.streams.operator.samples.jar:/path/to/myapp.jar \
    namespace.MyBeamApplication \
    --runner=StreamsRunner \
    --contextType=DISTRIBUTED \
    --jarsToStage=/path/to/myapp.jar \
    --restUrl=https://myStreamshost:8443/streams/rest \
    --userName=streamsuser \
    --userPassword=streams1
```

### The `BUNDLE` Context
Locally build applications to be submitted to a Streams runtime environment later

#### Prerequisites
* Local Streams installation (IBM Streams 4.2 or higher)

**WARNING:** SABs to be submitted to a Streaming Analytics service must be built using Red Hat Enterprise Linux 6 with x86_64 architecture 

#### Overview
Set the context type to `BUNDLE` to create a SAB and a Streams job configuration overlay file (_namespace.application_\_JobConfig.json) for your Beam application. Since the Beam application is being packaged locally, you must include the `com.ibm.streams.operator.samples.jar` located at `$STREAMS_INSTALL/lib` in the Java classpath.

Since the application will eventually be launched on a distributed environment, the Streams job needs to be
aware of your Beam application. To include your application and any dependencies it needs to
use the `--jarsToStage` option.

If your Beam application utilizes Beam's [ValueProvider](https://beam.apache.org/documentation/sdks/javadoc/2.0.0/org/apache/beam/sdk/options/ValueProvider.html) types for custom pipeline options **and no default value is provided**, 
then Streams submission-time parameters will be created for the application.

Once the SAB has been created, it can be submitted along with any submission-time parameters to a Streaming Analytics service or local Streams environment through the Streams Console, Streams REST API, or streamtool command. For more information about bundle submission, see `$STREAMS_RUNNER_HOME/samples/README`.

#### Example
```
java -cp $STREAMS_BEAM_TOOLKIT/lib/com.ibm.streams.beam.translation.jar:$STREAMS_INSTALL/lib/com.ibm.streams.operator.samples.jar:/path/to/myapp.jar \
    namespace.MyBeamApplication \
    --runner=StreamsRunner \
    --contextType=BUNDLE \
    --jarsToStage=/path/to/myapp.jar 
```

## Specify additional parameters
After you've selected your context, performed any necessary setup, and specified required parameters, you may add your application or additional Streams Runner parameters as needed. For example, if your Beam application reads input from a file, you can include the file in the SAB to be available in the Streaming Analytics service or Streams instance environment using the `--filesToStage` parameter. 

For the full list of Streams Runner options, see [here](../beamrunner-6-ref/#general-pipeline-options)
