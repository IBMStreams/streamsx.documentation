---
layout: docs
title:  Using the IBM Object Storage OpenStack Swift for Bluemix service with IBM Streams Runner for Apache Beam
navtitle: Using IBM Cloud Object Storage
description:  You can use the IBM® Streams Runner for Apache Beam `FileStreamSample` sample application to learn how to use IBM Cloud object storage for file input and output.
weight:  10
published: true
tag: beam
prev:
  file: beamrunner-5a-io
  title: I/O options
next:
  file: beamrunner-6-issues
  title: Limitations and known issues
---

You can use the IBM® Streams Runner for Apache Beam `FileStreamSample` sample application to learn how to use IBM Cloud (formerly IBM Bluemix) object storage for file input and output.

## Before you start

Before you run the Apache Beam 2.1 `FileStreamSample` sample application, you must configure and run the following services on IBM Cloud®:

- Streaming Analytics. For more information, see [Creating a Streaming Analytics service on IBM Cloud](../beamrunner-2-install/#creating-a-streaming-analytics-service-on-bluemix).
- Object Storage OpenStack Swift for Bluemix.
   - Create the service if you don't already have one. For more information, see [Creating the Object Storage OpenStack Swift for Bluemix service](../beamrunner-5a-io/#creating-the-object-storage-openstack-swift-for-bluemix-service).
   - Set up credentials for the service. **Remember**: Make sure the environment variables are configured. For more information, see [Set up credentials for the service](../beamrunner-5a-io/#setting-up-credentials-for-the-service).
   - (Optional) Install the Swift CLI client. For more information, see [Configuring the CLI to use Swift and Cloud Foundry commands](https://console.bluemix.net/docs/services/ObjectStorage/os_configuring.html).

**Important**: If you want to compile your application on IBM Cloud, you must unset the `STREAMS_INSTALL` variable before you submit the application to the Streaming Analytics service.

## Running the sample application

These instructions assume that you have already set up and run other samples on the Streaming Analytics service on IBM Cloud.

1. Navigate to the `samples` directory in Streams Runner, and set up environment variables for the runner:

    ```
    cd <installdir>/samples
    . bin/streams-runner-env.sh
    ```

2. Set the environment variables `VCAP_SERVICES` to point to the VCAP file that contains your Streaming Analytics service credentials and `STREAMING_ANALYTICS_SERVICE_NAME` to the service name within that file, for example:

    ```
    export VCAP_SERVICES=$HOME/sample.vcap
    export STREAMING_ANALYTICS_SERVICE_NAME="sample-service"
    ```

3. Run the `FileStreamSample` Beam application by entering the following command.

    ```
java -cp \
  $STREAMS_BEAM_TOOLKIT/lib/com.ibm.streams.beam.translation.jar:\
lib/com.ibm.streams.beam.samples.jar \
    com.ibm.streams.beam.sample.FileStreamSample \
    --runner=StreamsRunner \
    --contextType=STREAMING_ANALYTICS_SERVICE \
    --jarsToStage=lib/com.ibm.streams.beam.samples.jar:$STREAMS_BEAM_TOOLKIT/lib/com.ibm.streams.beam.sdk.jar \
    --filesToStage='{"README.md":"sample/README.md"}' \
    --input=streams://sample/README.md \
    --output=swift://out/README.md
```

   The command submits the application to the Streaming Analytics Service, copies the file to object storage, and then exits. If it does not submit the application successfully, check your `VCAP_SERVICES` and `STREAMING_ANALYTICS_SERVICE_NAME` variables. If the application submits but does not complete, download and inspect the job logs from the Streams Console on IBM Cloud.

   The command is similar to the one that is used in the README.md for this sample application, but there are a few important differences:

    - The `--jarsToStage` option includes more JAR files. The `swift://` scheme support is in the `$STREAMS_BEAM_TOOLKIT/lib/com.ibm.streams.beam.sdk.jar`, which is not staged by default and so must be included here.
    - The `--filesToStage` option is used to move the local `README.md` file to the runtime environment on IBM Cloud to be used as input for the sample. Alternatively, this file can be uploaded to Object Storage OpenStack Swift for Bluemix by using the web UI or command-line Swift client and referenced with the `swift://` scheme, but staging it this way allows you to use it without that extra step.
    - The `--input` option uses the `streams://` scheme to refer to the `README.md` file.
    - The `--output` option uses the `swift://` scheme to direct the application to write the output file into an object named `README.md` in a container named `out`.

     When the job completes successfully, the Streams Console shows the job as healthy (green) and the copied file is available in the Object Storage OpenStack Swift for Bluemix web management page.

     <img src="/streamsx.documentation/images/beamrunner/objectstorageresult.jpg" alt="Result file shown in the object storage container" width="700" />

     **Remember**: Whether the job is successful or not, it continues to run on the Streaming Analytics service to allow for inspection by the Streams Console. When you are done with the tutorial, make sure to use the Streams Console to cancel any jobs you started.
