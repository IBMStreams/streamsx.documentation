---
layout: docs
title:  WordCount sample application for IBM Streams Runner for Apache Beam
navtitle: WordCount sample app
description:  
weight:  10
published: true
tag: beam
prev:
  file: beamrunner-2a-using
  title: Using
next:
  file: beamrunner-3-sample
  title: TemperatureSample sample app
---

You can use IBM® Streams Runner for Apache Beam to run the Apache Beam 2.0 Java™ SDK Quickstart WordCount sample application.

## Before you start

Before you run the `WordCount` sample application, you must configure and run the following services on IBM Bluemix®:

- Streaming Analytics. For more information, see [Creating a Streaming Analytics service on Bluemix](../beamrunner-2-install/#creating-a-streaming-analytics-service-on-bluemix).
- Object Storage OpenStack Swift for Bluemix.
   - Create the service if you don't already have one. For more information, see [Creating the Object Storage OpenStack Swift for Bluemix service](../beamrunner-5a-io/#creating-the-object-storage-openstack-swift-for-bluemix-service).
   - Set up credentials for the service. **Remember**: Make sure the environment variables are configured. For more information, see [Set up credentials for the service](../beamrunner-5a-io/#setting-up-credentials-for-the-service).
   - (Optional) Install the Swift CLI client. For more information, see [Configuring the CLI to use Swift and Cloud Foundry commands](https://console.stage1.bluemix.net/docs/services/ObjectStorage/os_configuring.html).

In addition, you must set up your Java Development Kit (JDK) and Maven environment. For more information, see [Set up your Development Environment](https://beam.apache.org/get-started/quickstart-java/#set-up-your-development-environment).

**Important**: If you want to compile your application on Bluemix, you must unset the `STREAMS_INSTALL` variable before you submit the application to the Streaming Analytics service.

## Running the WordCount sample

1. Get and compile the WordCount sample application for Apache Beam 2.0.  
    **Important:** The `-DarchetypeVersion` variable must be set to 2.0.0, as shown in the following command.

   ```
  $ mvn archetype:generate \
            -DarchetypeGroupId=org.apache.beam \
            -DarchetypeArtifactId=beam-sdks-java-maven-archetypes-examples \
            -DarchetypeVersion=2.0.0 \
            -DgroupId=org.example \
            -DartifactId=word-count-beam \
            -Dversion="0.1" \
            -Dpackage=org.apache.beam.examples \
            -DinteractiveMode=false
  $ cd word-count-beam
  $ mvn package
  ```

1. Choose one of the following options to run the WordCount sample application. For more information about the `streams://` and `swift://` storage options, see [Input/output options for IBM Streams Runner for Apache Beam](../beamrunner-5a-io/).

    - The following command uses `streams://` to provide the input, and writes the output to Object Storage.

      ```
      $ java -cp $STREAMS_BEAM_TOOLKIT/lib/com.ibm.streams.beam.translation.jar:target/word-count-beam-0.1.jar \
          org.apache.beam.examples.WordCount \
          --filesToStage="{\"./pom.xml\":\"pom.xml\"}" \
          --inputFile=streams://pom.xml \
          --output=swift://beam-container/quickstart.out- \
          --runner=StreamsRunner \
          --jarsToStage=target/original-word-count-beam-0.1.jar:$STREAMS_BEAM_TOOLKIT/lib/com.ibm.streams.beam.sdk.jar \
          --contextType=STREAMING_ANALYTICS_SERVICE \
          --vcapServices=/path/to/vcap/file \
          --serviceName=yourSasName
      ```

    - The following command uses Object Storage to host both input and output files. Make sure that the `pom.xml` input file is uploaded to `beam-container` before you submit the application. For more information about adding a file to the container, see [Getting started with Object Storage](https://console.stage1.bluemix.net/docs/services/ObjectStorage/index.html).

      ```
      $ java -cp $STREAMS_BEAM_TOOLKIT/lib/com.ibm.streams.beam.translation.jar:target/word-count-beam-0.1.jar \
          org.apache.beam.examples.WordCount \
          --inputFile=swift://beam-container/pom.xml \
          --output=swift://beam-container/quickstart.out- \
          --runner=StreamsRunner \
          --jarsToStage=target/original-word-count-beam-0.1.jar:$STREAMS_BEAM_TOOLKIT/lib/com.ibm.streams.beam.sdk.jar \
          --contextType=STREAMING_ANALYTICS_SERVICE \
          --vcapServices=/path/to/vcap/file \
          --serviceName=yourSasName
      ```

1. Inspect the results.  
    After the pipeline completes, you can download the output through the Object Storage OpenStack Swift for Bluemix web management page or by using the Swift CLI client. Each output file contains up to 50,000 lines. If the output goes beyond that limit, multiple output files are created.

    ```
    swift download beam-container -p quickstart.out -D swift-output
    cat swift-output/*
    ```

 **Remember**: The job continues to run on the Streaming Analytics service to allow for inspection by the Streams Console. When you are done with the tutorial, make sure to use the Streams Console to cancel any jobs you started.
