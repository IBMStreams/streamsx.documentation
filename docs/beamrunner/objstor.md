---
layout: docs
title:  FileStreamSample sample application for IBM Streams Runner for Apache Beam
navtitle: Using IBM Cloud Object Storage
description:  You can use the IBM® Streams Runner for Apache Beam `FileStreamSample` sample application to learn how to use IBM Cloud object storage for file input and output.
weight:  10
published: true
tag: beam
prev:
  file: wordcount
  title: WordCount sample app
next:
  file: messagehub
  title: I/O sample apps
---

You can use the IBM® Streams Runner for Apache Beam `FileStreamSample` sample application to learn how to use IBM Cloud object storage for file input and output.

## Before you start

Before you run the Apache Beam 2.4 `FileStreamSample` sample application, you must configure and run the following services on IBM Cloud®:

- Streaming Analytics. For more information, see [Creating a Streaming Analytics service on IBM Cloud](../beamrunner-2b-sas/#creating-a-streaming-analytics-service-on-ibm-cloud).
- Cloud Object Storage.
   - Create the service if you don't already have one. For more information, see [Creating an IBM Cloud Object Storage service](../io/#creating-an-ibm-cloud-object-storage-service).
   - Set up credentials for the service. **Remember**: Make sure the environment variables are configured. For more information, see [Set up credentials for the Object Storage  service](../io/#setting-up-credentials-for-the-object-storage-service).

**Important**: If you want to compile your application on IBM Cloud, you must unset the `STREAMS_INSTALL` variable before you submit the application to the Streaming Analytics service.

## Running the sample application

These instructions assume that you have already set up and run other samples on the Streaming Analytics service on IBM Cloud.

1. Go to the `examples` directory in Streams Runner and set up environment variables for the runner:

    ```bash
    cd <installdir>/examples
    . bin/streams-runner-env.sh
    ```

2. Set the service credentials environment variables as follows:
    - `VCAP_SERVICES`: The path to the VCAP file that contains your Streaming Analytics service credentials.
    - `STREAMING_ANALYTICS_SERVICE_NAME`: The service name within the VCAP file.

    For example:

    ```bash
    export VCAP_SERVICES=$HOME/sample.vcap
    export STREAMING_ANALYTICS_SERVICE_NAME="sample-service"
    ```

3. Run the `FileStreamSample` Beam application by entering the following command:

    ```bash
mvn exec:java -Ps3 \
  -Dexec.classpathScope=compile -Dexec.cleanupDaemonThreads=false \
  -Dexec.mainClass=com.ibm.streams.beam.sample.FileStreamSample \
  -Dexec.args="--runner=StreamsRunner --contextType=STREAMING_ANALYTICS_SERVICE \
    --jarsToStage=target/dependency/*amazon*jar:target/dependency/*aws*jar \
    --filesToStage='{\"README.md\" : \"sample/readme.md\"}' \
    --awsServiceEndpoint='s3-api.us-geo.objectstorage.softlayer.net' \
    --input=streams://sample/readme.md --output=s3://username-beam-bucket/readme.copy \
    --awsCredentialsProvider='{\"@type\" : \"AWSStaticCredentialsProvider\", \
      \"awsAccessKeyId\" : \"$AWS_ACCESS_KEY_ID\", \"awsSecretKey\" : \"$AWS_SECRET_ACCESS_KEY\"}'"
```

   The command submits the application to the Streaming Analytics Service, copies the file to object storage, and then exits. If it does not submit the application successfully, check your `VCAP_SERVICES` and `STREAMING_ANALYTICS_SERVICE_NAME` variables. If the application submits but does not complete, download and inspect the job logs from the Streams Console on IBM Cloud.

   The command is similar to the one that is used in the README.md for this sample application, but there are a few important differences:

    - The `--filesToStage` option is used to move the local `README.md` file to the runtime environment on IBM Cloud to be used as input for the sample. Alternatively, you can upload this file to your Cloud Object Storage service by using the web UI or command line and reference it with the `s3://` scheme. Using the  `-filesToStage` option eliminates this extra step.
    - The `--input` option uses the `streams://` scheme to refer to the `README.md` file.
    - The `--output` option uses the `s3://` scheme to direct the application to write the output file into an object named `README.md` in a container named `username-beam-bucket`.

     When the job completes successfully, the Streams Console shows the job as healthy (green) and the copied file is available in the Cloud Object Storage object management page.

     <img src="/streamsx.documentation/images/beamrunner/objectstorageresult.jpg" alt="Result file shown in the object storage bucket" width="700" />

     **Remember**: Whether the job is successful, it continues to run on the Streaming Analytics service to allow for inspection by the Streams Console. When you are done with this tutorial, make sure to use the Streams Console to cancel any jobs that you started.
