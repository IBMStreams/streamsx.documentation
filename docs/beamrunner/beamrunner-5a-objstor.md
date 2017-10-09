---
layout: docs
title:  Using Bluemix Object Storage Swift with IBM Streams Runner for Apache Beam
navtitle: Object Storage
description:  
weight:  10
published: true
tag: beam
prev:
  file: beamrunner-5-ref
  title: Reference
next:
  file: beamrunner-6-issues
  title: Limitations and known issues
---

IBM® Streams Runner for Apache Beam can use the IBM® Object Storage for Bluemix service for I/O. The service can be accessed directly by using OpenStack Object Storage (Swift) API v1 calls. Using the Object Storage service is useful when you run Apache Beam 2.0 applications on the Streaming Analytics service on IBM Bluemix, where direct access to output files from Beam applications is difficult.

This topic describes the `swift://` scheme and then shows how to set up Bluemix Object Storage Swift and use the scheme with one of the sample applications from Streams Runner. It assumes you have already set up and run other samples on the Streaming Analytics service on Bluemix.

## The `swift://` scheme

The Bluemix Object Storage Swift service stores objects in containers. For more information, see [Getting started with Object Storage](https://console.stage1.bluemix.net/docs/services/ObjectStorage/index.html). Beam I/O uses URIs to name files, and Streams Runner interprets the URI in the format <code>swift://_container_/_object_</code> to read and write to these objects.

`The name Bluemix Object Storage Swift doesn't appear in the Cloud Object Storage options in the Catalog. Need to determine the proper name.???`
`PaulG: The name keeps changing, it should be: Object Storage OpenStack Swift for Bluemix`

The object storage `should this be upper case???` system doesn't allow the forward slash (/) character in the container name, but does allow it in the object name. Although the forward slash is not special to object storage, Streams Runner treats it as a directory separator in a logical path.

For example if a container named `MyContainer` contains objects named `top.txt` and `dir/nested.txt`, the object storage system shows these together in the list of objects in `MyContainer`. In Beam, the URIs `swift://MyContainer/foo.txt` and `swift://MyContainer/dir/nested.txt` refer to these two objects, but Beam also considers `swift://MyContainer/dir/` to be a logical directory that contains a resource named `nested.txt`. "Glob" patterns for resources (for example, `swift://MyContainer/dir/\*`) are not supported.

For more information about managing file systems and resources with Beam, see the [Beam I/O documentation](https://beam.apache.org/documentation/sdks/javadoc/2.0.0/org/apache/beam/sdk/io/package-summary.html).

## Creating the Bluemix Object Storage Swift service

If you have not already done so, you must create the Bluemix Object Storage Swift service.

1. On the Bluemix [dashboard](https://console.bluemix.net/dashboard) main menu, click **Storage**.
2. Click **Create Storage service**.
3. Click **Cloud Object Storage**.
4. Select **Bluemix Object Storage Swift**. `Doesn't exist. Should it be Object Storage OpenStack Swift for Bluemix??? PaulG: yes`  
  **Important**: The Cloud Object Storage – S3 service is not supported by the Streams Runner and does not work with this tutorial.
5. Click **Create**.
6. For this sample, change the Service name to `Object Storage Demo`. You can optionally change the region, organization, and space.
7. For **Pricing Plan**, click **Lite**.
8. Click **Create**. Bluemix returns to the Dashboard while the service is provisioned.

## Setting up credentials for the service

To use the storage from Beam applications, service credential information is required.

1. After the service is provisioned, select the service from the dashboard to open the **Manage** page for the service. From here, you can manage the files that you create. Streams Runner creates containers and files as required.
2. On the ??? service page, click **Service credentials**.
3. If necessary, create a credential by clicking **New credential**. Use the default information and click **Add**.
4. Click **View credentials**.
5. On the computer where Streams Runner is installed, create the following environment variables from the fields that are shown in the credentials:

| Environment variable | Credentials field | Example |
| --- | --- | --- |
| OS\_USER\_ID | userId | export OS\_USER\_ID="2b670d77432e4cf2bd128ef9ff61fa56" |
| OS\_PASSWORD | password | export OS\_PASSWORD=" f1H/~BIO.=s0wuT9" |
| OS\_PROJECT\_ID | projectId | export OS\_PROJECT\_ID="80301e24254f4ffb81d53f0cddccad78" |
| OS\_REGION\_NAME | region | export OS\_REGION="dallas" |


These environment variables are also used by the command-line Swift client.
For more information, see [Configuring the CLI to use Swift and Cloud Foundry commands](https://console.stage1.bluemix.net/docs/services/ObjectStorage/os_configuring.html).
For MacOS, the Swift command of OpenStack might collide with the existing Xcode Swift command. To avoid the conflicts, create a Python virtual environment, and install the Swift client in the virtual environment.

```
$ virtualenv my_project
$ cd my_project
$ source bin/activate
$ pip install python-swiftclient
$ pip install python-keystoneclient
```

## Running the sample application

1. Navigate to the samples directory in Streams Runner, and set up environment variables for the runner:

    ```
    $ cd <installdir>/samples
    $ . bin/streams-runner-env.sh
    ```

2. Set the environment variables `VCAP_SERVICES` to point to the VCAP file that contains your Streaming Analytics service credentials and `STREAMING_ANALYTICS_SERVICE_NAME` to the service name within that file, for example:

    ```
    $ export VCAP_SERVICES=$HOME/sample.vcap
    $ export STREAMING_ANALYTICS_SERVICE_NAME="sample-service"
    ```

3. Run the `FileStreamSample` Beam application by entering the following command:

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

The command submits the application to the Streaming Analytics Service, copies the file to object storage, and then exits. If it does not submit the application successfully, check your `VCAP_SERVICES` and `STREAMING_ANALYTICS_SERVICE_NAME` variables. If the application submits but does not complete, download and inspect the job logs from the Streams Console on Bluemix.

The command is similar to the one that is used in the README.md for this sample application, but there are a few important differences:

- The `--jarsToStage` option includes more JAR files. The `swift://` scheme support is in the `$STREAMS_BEAM_TOOLKIT/lib/com.ibm.streams.beam.sdk.jar`, which is not staged by default and so must be included here.
- The `--filesToStage` option is used to move the local `README.md` file to the runtime environment on Bluemix to be used as input for the sample. Alternatively, this file can be uploaded to Bluemix Object Storage Swift by using the web UI or command-line Swift client and referenced with the `swift://` scheme, but staging it this way allows using it without that extra step.
- The `--input` option uses the `streams://` scheme to refer to the `README.md` file.
- The `--output` option uses the `swift://` scheme to direct the application to write the output file into an object named `README.md` in a container named `out`.

When the job completes successfully, the Streams Console will show the job as healthy (green) and the copied file will be available in the Bluemix Object Storage Swift web management page:

<img src="/streamsx.documentation/images/beamrunner/objectstorageresult.jpg" alt="Result file shown in Object Storage container" width="700" />

Note that whether the job is successful or not, it continues to run on the Streaming Analytics service to allow for inspection by the Streams Console. When you are done with the tutorial, make sure to use the Streams Console to cancel any jobs you started.
