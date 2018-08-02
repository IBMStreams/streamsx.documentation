---
layout: docs
title:  Input/output options for IBM Streams Runner for Apache Beam
navtitle: I/O options
description:  Apache Beam 2.4 applications that use IBM® Streams Runner for Apache Beam have input/output options of standard output and errors, local file input, Publish and Subscribe transforms, and object storage and messages on IBM Cloud.
weight:  10
published: true
tag: beam
prev:
  file: using
  title: Using the runner
next:
  file: sample
  title: TemperatureSample app
---

Apache Beam 2.4 applications that use IBM® Streams Runner for Apache Beam have several options for input/output:

- [Standard output and errors](#standard-output-and-errors)
- [Local file input](#local-file-input-streams)
- [Object storage on IBM Cloud](#object-storage-inputoutput-on-ibm-cloud-s3)
- [Messages on IBM Message Hub®](#messages-on-ibm-cloud-message-hub)
- [`Publish` and `Subscribe` transforms](#publish-and-subscribe-transforms)

## Standard output and errors

Standard output and errors from the main thread of the application are shown in the terminal window where the runner is launched. The `TemperatureSample` application uses this method to display collected metrics.

Standard output and errors in the Beam pipeline are not visible in the terminal because the pipeline is running on a distributed resource (on premises or in IBM Cloud). Instead, output and errors are written to log files on the distributed system. You can download the log files from the Streams Console, or you can view them in the console log viewer.

## Local file input (`streams://`)

Because the application runs on remote systems like in the IBM Cloud or distributed environment, it can't have direct access to local files. Local files can be uploaded to the distributed environment when the runner is launched by using the `--filesToStage` option. This option uploads one or more local files to known locations in the environment, and the pipeline can access them directly from those locations by using the `streams://` scheme.

For example, `--filesToStage='{"/local/file.txt":"data/input"}'` copies the file `/local/file.txt` to IBM Cloud or distributed environment where the Beam application can reference it as `streams://data/input`.

For more information about the `--filesToStage` option, see [Streams Runner pipeline options](../reference/#streams-runner-pipeline-options).

## Object storage input/output on IBM Cloud (`s3://`)

A Beam application can use storage on IBM Cloud for both input and output by using the `s3://` scheme from the `beam-sdk-java-io-amazon-web-services` library and a Cloud Object Storage service on IBM Cloud. Objects in the service can be manipulated through the web interface in IBM Cloud, a command-line tool, or from the pipeline in the Beam application. This service is useful when you run Apache Beam 2.4 applications on the Streaming Analytics service on IBM Cloud, where direct access to output files from Beam applications is difficult.

The Cloud Object Storage service stores objects in buckets. For more information, see [About IBM Cloud Object Storage](https://console.bluemix.net/docs/services/cloud-object-storage/about-cos.html#about-ibm-cloud-object-storage). Beam I/O uses URIs to name files, and Streams Runner interprets the URI in the format <code>s3://_bucket_/_object_</code> to read and write to these objects.

The object storage system requires that bucket names must be globally unique and DNS-compliant. Names must be 3 - 63 characters long and must consist of lowercase letters, numbers, and dashes. The forward slash (/) character can't be used in the bucket name, but it is allowed in the object name.

For example, if a bucket named `MyBucket` contains objects named `top.txt` and `dir/nested.txt`, the object storage system shows these objects together in the list of objects in `MyBucket`. In Beam, the URIs `s3://MyBucket/foo.txt` and `s3://MyBucket/dir/nested.txt` refer to these two objects, but Beam also considers `s3://MyBucket/dir/` to be a logical directory that contains a resource named `nested.txt`.

You can use the [FileStreamSample sample application](../objstor) to learn how to use IBM Cloud object storage for file input and output. For more information about managing file systems and resources with Beam, see the [Beam I/O documentation](https://beam.apache.org/documentation/sdks/javadoc/2.4.0/org/apache/beam/sdk/io/package-summary.html).

### Creating an IBM Cloud Object Storage service

If you have not already done so, you must create a Cloud Object Storage service and bucket.

1. On the IBM Cloud [catalog](https://console.bluemix.net/catalog) main menu, click the **Storage** category.
1. From the Storage page, click **Object Storage**.
1. Change the Service name to something meaningful to you or leave the default name.
1. For **Pricing Plans**, click **Lite**.
1. Click **Create**. The **Buckets** page for the object storage service is displayed.
1. On the **Buckets** page, click **Create Bucket**.
1. Provide a unique bucket name (for example, `username-beam-bucket`), resiliency, location, and storage class.
1. Click **Create**.

### Setting up credentials for the Object Storage service

To use the storage service from Beam applications, you must specify the Object Storage service credentials. Because the `s3` FileSystem is based on AWS object storage, you must create credentials with Hash Message Authentication Code (HMAC) keys in your service.

1. On the service page, click **Service credentials**.
1. Create a credential by clicking **New credential**.
1. Put `{"HMAC":true}` in the **Add Inline Configuration Parameters (Optional) field** and click **Add** to create the new credentials.
1. Click **View credentials** on the newly added credentials.
1. On the computer where Streams Runner is installed, create the following environment variables from the fields that are shown in the credentials.

| Environment variable | Credentials field | Environment variable example|
|----------------------|-------------------|-----------------------------|
| `AWS_ACCESS_KEY_ID` | `cos_hmac_keys.access_key_id` | `export AWS_ACCESS_KEY_ID=de4e2e3d7bd943a99b672f13dec40f7c`|
| `AWS_SECRET_ACCESS_KEY` | `cos_hmac_keys.secret_access_key` | `export AWS_SECRET_ACCESS_KEY=54f077c504ebef49bf707cc0d57e3f2a4f4d4a6898b53fec`|

<br/>For more information about object storage in IBM Cloud, see [Getting started with Object Storage](https://console.bluemix.net/docs/services/ObjectStorage/index.html).

### Specifying required parameters

When you launch your Beam application, you must specify the following parameters:
- `--awsServiceEndpoint`

    The service endpoint depends on your service's resiliency, location, and visibility and can be found in the **Endpoint** tab of your object storage service page. For example, if your service is cross-region across all US locations and public, the service endpoint is `s3-api.us-geo.objectstorage.softlayer.net`.
- `--awsCredentialsProvider`

    The credentials for the service must be provided. The `--awsCredentialsProvider` option must be specified as a JSON format with a required `@type` field and `AWSCredentialsProvider` class as the value. It is recommended to use the [AWSStaticCredentialsProvider](https://docs.aws.amazon.com/AWSJavaSDK/latest/javadoc/com/amazonaws/auth/AWSStaticCredentialsProvider.html) class along with the environment variables specified.

- `--jarsToStage`

    Because Streams Runner does not include S3 and AWS libraries in its installation, these JAR files must be specified in the `--jarsToStage` option.

### Launching the sample app

The following example shows how to launch the `FileStreamSample` app.
```
# Recompile samples with S3 usage
mvn clean package -Ps3

# Run sample
mvn exec:java -Ps3 -Dexec.classpathScope=compile -Dexec.cleanupDaemonThreads=false \
    -Dexec.mainClass=com.ibm.streams.beam.sample.FileStreamSample \
    -Dexec.args="--runner=StreamsRunner --filesToStage='{\"./README.md\" : \"readme.md\"}' --jarsToStage=$STREAMS_RUNNER_HOME/examples/target/dependency/*amazon*jar:$STREAMS_RUNNER_HOME/examples/target/dependency/*aws*jar --input=streams://readme.md --output=s3://username-beam-bucket/readme.copy --awsServiceEndpoint='s3-api.us-geo.objectstorage.softlayer.net' --awsCredentialsProvider='{\"@type\" : \"AWSStaticCredentialsProvider\", \"awsAccessKeyId\" : \"$AWS_ACCESS_KEY_ID\",
    \"awsSecretKey\" : \"$AWS_SECRET_ACCESS_KEY\"}'"
```
## Messages on IBM Message Hub

Beam applications can produce messages to and consume messages from IBM Message Hub by using the native Beam [KafkaIO](https://beam.apache.org/documentation/sdks/javadoc/2.4.0/org/apache/beam/sdk/io/kafka/KafkaIO.html).
Message Hub is a scalable, distributed, high-throughput messaging
service that enables applications and services to communicate easily and
reliably.

You can use the [I/O sample applications](../messagehub) to learn how to use Message Hub for input and output. For more information about IBM Message Hub, see [Getting started with Message Hub](https://console.bluemix.net/docs/services/MessageHub/index.html).

### Creating a Message Hub service on IBM Cloud

If you have not already done so, you must create a Message Hub service on IBM Cloud.

1. Go to the [IBM Cloud Catalog](https://console.bluemix.net/catalog/) page and search for **Message Hub**.
2. Click the **Message Hub** service.
3. For **Pricing Plan**, select **Standard**.
4. Click **Create**. After the service is created, the **Manage** page of the Message Hub service is displayed.
5. On the **Manage** page **Topics** tab, create a topic by clicking the plus button (**Create topic**). Enter a topic name and click **Create Topic**. You will provide this topic name to the producer and consumer in subsequent steps.

### Setting up credentials for the Message Hub service

To communicate with Message Hub from Beam applications, you must create a JSON-formatted file that holds credentials and other information for the Message Hub service.

2. Copy the credentials of your Message Hub service:
  1. On the Message Hub service page, click **Service credentials**.
  2. If necessary, create a credential by clicking **New credential**. Use the default information and click **Add**.
  3. Click **View credentials** for the credential that you want to use in your VCAP file. Click **Copy** to copy the credentials.
3. Paste the copied credentials into a file. Give the file a meaningful name and extension, such as `mh.cred`.

## `Publish` and `Subscribe` transforms

IBM Streams applications that are written in Java™, Python, SPL, and with the Beam API can publish and subscribe to tuple streams in other Streams applications. You can do the same in your Beam applications by using the Streams Runner `Publish` and `Subscribe` APIs to publish or subscribe to tuple streams in other Beam or Streams applications.

The `StreamsPubSubSample` in the `$STREAMS_RUNNER_HOME/examples` directory demonstrates basic `Publish` and `Subscribe` usage.

### `Publish` API reference

| Method | Description |
|:------ |:----------- |
| `ofType(class<T> clazz)` <br> `ofType(TypeDescriptor<T> type)` | **Required**. Specifies the published data type. To be compatible with other non-Beam subscribers, the application cannot use a Beam Coder to perform serialization. Instead, published tuples must be `Serializable`. `TypeDescriptor<T>` is more flexible than `Class<T>` because it allows applications to specify nested generic types (for example, `TypeDescriptor<KV<Long, String>>`). |
| `to(String topic)` | **Required**. Use this method to specify the topic to publish to. <br><br> The topic name has the following requirements: <br> - Must not be zero length <br> - Must not contain the null character () <br> - Must not contain the number sign (‘#’) or the plus sign (‘+’) <br><br> The forward slash (‘/’) is used to separate each level within a topic tree and provide a hierarchical structure to the topic names. Topic-level separators can appear anywhere in a topic name. Adjacent topic-level separators indicate a zero length topic level. |

### `Subscribe` API reference

| Method | Description |
|:------ |:----------- |
| `ofType(class<T> clazz)` <br> `ofType(TypeDescriptor<T> type)` | **Required**. Specifies the data type to be subscribed. To be compatible with other non-Beam publishers, the application cannot use a Beam Coder to perform deserialization. Instead, subscribed tuples must be `Serializable`. `TypeDescriptor<T>` is more flexible than `Class<T>` because it allows applications to specify nested generic types (for example, `TypeDescriptor<KV<Long, String>>)`. |
| `from(String topic)` | **Required**. Use this method to specify the topic to subscribe from. Subscribers are matched to published streams when the following requirements are met: <br><br> - The topic is a match (you can use wildcards to match). <br> - The type of the stream `T` is an exact match. <br><br> Publish/subscribe is a many-to-many relationship; multiple streams from multiple applications can be published on the same topic and type. Multiple subscribers can subscribe to a topic and type. A subscription matches all publishers that use the same topic and tuple type. Tuples on the published streams appear on the returned stream as a single stream. <br><br> The subscription is dynamic. The returned stream subscribes to a matching stream that is published by a newly submitted application (a job), and stops a subscription when a running job is canceled. <br><br> Publish/subscribe works only when the pipeline is submitted to a distributed context (`DISTRIBUTED` and `STREAMING_ANALYTICS_SERVICE`). The context allows different applications (or even different parts of the same application) to communicate by using published streams. |
| `setCoder(Coder<T> coder)` | *Optional*. Use this method to provide the output coder. If absent, the `Subscribe` transform tries to infer the coder through the Beam coder registry. |
| `withTimestampFn(SerializedFunction<T, Instant> fn)` | *Optional*.  Use this method to provide a `SerializedFunction` that extracts a time stamp from user type T. If `SerializedFunction`is not specified, the value of `BoundedWindow.TIMESTAMP_MIN_VALUE` is attached to all tuples as the timestamp. |
| `withWatermarkFn(SerializedFunction<T, Instant> fn)` | *Optional*. Use this method to specify a `SerializedFunction` that creates watermarks from user type T. If `SerializedFunction`is not specified, the transform uses `timestampFn` to create watermarks. |
