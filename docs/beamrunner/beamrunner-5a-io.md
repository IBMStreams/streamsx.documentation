---
layout: docs
title:  Input/output options for IBM Streams Runner for Apache Beam
navtitle: I/O options
description:  Apache Beam 2.0 applications that use IBM® Streams Runner for Apache Beam on a Streaming Analytics service on Bluemix have input/output options of standard output and errors, local file input, and object storage on Bluemix.
weight:  10
published: true
tag: beam
prev:
  file: beamrunner-5-ref
  title: Reference
next:
  file: beamrunner-5b-objstor
  title: Using Bluemix Object Storage
---

Apache Beam 2.0 applications that use IBM® Streams Runner for Apache Beam on a Streaming Analytics service on Bluemix have several options for input/output:

- Standard output and errors
- Local file input
- Object storage on Bluemix

## Standard output and errors

Standard output and errors from the main thread of the application are shown in the terminal window where the runner is launched. The `TemperatureSample` application uses this method to display collected metrics.

Standard output and errors in the Beam pipeline are not visible in the terminal because the pipeline is running on Bluemix. Instead, output and errors are written to log files on Bluemix. You can download the log files from the Streams Console, or you can view them in the console log viewer.

## Local file input (`streams://`)

Because the application runs on Bluemix, it does not have direct access to local files. Local files can be uploaded to Bluemix when the runner is launched by using the `--filesToStage` option. This option uploads one or more local files to known locations on Bluemix, and the pipeline can access them directly from those locations by using the `streams://` scheme.

For example, `--filesToStage='{"/local/file.txt":"data/input"}'` copies the file `/local/file.txt` to Bluemix where the Beam application can reference it as `streams://data/input`.

For more information about the `--filesToStage` option, see [Streams Runner pipeline options](../beamrunner-5-ref/#streams-runner-pipeline-options).

## Object storage input/output on Bluemix (`swift://`)

The Beam application can use storage on Bluemix itself for both input and output by using the `swift://` scheme and the Object Storage OpenStack Swift for Bluemix service. Objects in the service can be manipulated through the web interface in Bluemix, a command-line tool, or from the pipeline in the Beam application. This service is useful when you run Apache Beam 2.0 applications on the Streaming Analytics service on IBM Bluemix, where direct access to output files from Beam applications is difficult.

The Object Storage OpenStack Swift for Bluemix service stores objects in containers. For more information, see [Getting started with Object Storage](https://console.stage1.bluemix.net/docs/services/ObjectStorage/index.html). Beam I/O uses URIs to name files, and Streams Runner interprets the URI in the format <code>swift://_container_/_object_</code> to read and write to these objects.

The object storage system doesn't allow the forward slash (/) character in the container name, but does allow it in the object name. Although the forward slash is not special to object storage, Streams Runner treats it as a directory separator in a logical path.

For example, if a container named `MyContainer` contains objects named `top.txt` and `dir/nested.txt`, the object storage system shows these objects together in the list of objects in `MyContainer`. In Beam, the URIs `swift://MyContainer/foo.txt` and `swift://MyContainer/dir/nested.txt` refer to these two objects, but Beam also considers `swift://MyContainer/dir/` to be a logical directory that contains a resource named `nested.txt`. You can't use "Glob" patterns for resources (for example, `swift://MyContainer/dir/\*`).

For more information about managing file systems and resources with Beam, see the [Beam I/O documentation](https://beam.apache.org/documentation/sdks/javadoc/2.0.0/org/apache/beam/sdk/io/package-summary.html).

### Creating the Object Storage OpenStack Swift for Bluemix service

If you have not already done so, you must create the Object Storage OpenStack Swift for Bluemix service.

1. On the Bluemix [dashboard](https://console.bluemix.net/dashboard) main menu, click **Storage**.
2. Click **Create Storage service**.
3. Click **Object Storage**.
4. Select **Object Storage OpenStack Swift for Bluemix**.   
  **Important**: Bluemix provides multiple object storage services, but only Object Storage OpenStack Swift for Bluemix is supported by IBM Streams Runner for Apache Beam.
5. Click **Create**.
6. Change the Service name to something meaningful to you. You can optionally change the region, organization, and space.
7. For **Pricing Plan**, click **Lite**.
8. Click **Create**. Bluemix returns to the Dashboard while the service is provisioned.

### Setting up credentials for the service

To use the storage from Beam applications, you must specify the Bluemix service credentials. You can specify the credentials by setting environment variables or by using Swift command-line options. For more information about the Swift command-line options, see [Configuring the CLI to use Swift and Cloud Foundry commands](https://console.stage1.bluemix.net/docs/services/ObjectStorage/os_configuring.html).

1. After the service is provisioned, select the object storage service that you created from the dashboard to open the **Manage** page for the service.
2. On the service page, click **Service credentials**.
3. If necessary, create a credential by clicking **New credential**. Use the default information and click **Add**.
4. Click **View credentials**.
5. On the computer where Streams Runner is installed, create the following environment variables from the fields that are shown in the credentials.  

| Environment variable | Command-line option           | Credentials field | Environment variable example                                                 |
|----------------------|------------------|-------------------|---------------------------------------------------------|
| `OS_USER_ID`           | `--swiftUserId`    | `userId`            | `export OS_USER_ID='2b670d77432e4cf2bd128ef9ff61fa56'`    |
| `OS_PASSWORD`          | `--swiftPassword`  | `password`          | `export OS_PASSWORD=' f1H/~BIO.=s0wuT9'`                  |
| `OS_PROJECT_ID`        | `--swiftProjectId` | `projectId`         | `export OS_PROJECT_ID='80301e24254f4ffb81d53f0cddccad78'` |
| `OS_REGION_NAME`       | `--swiftRegion`    | `region`            | `export OS_REGION='dallas'`                               |

**Tip**: For MacOS, the Swift command of OpenStack might collide with the existing Xcode Swift command. To avoid the conflicts, create a Python virtual environment, and install the Swift client in the virtual environment.

```
virtualenv my_project
cd my_project
source bin/activate
pip install python-swiftclient
pip install python-keystoneclient
```

For more information about object storage in Bluemix, see [Getting started with Object Storage](https://console.stage1.bluemix.net/docs/services/ObjectStorage/index.html). For more information about the command-line Swift client, see [Configuring the CLI to use Swift and Cloud Foundry commands](https://console.stage1.bluemix.net/docs/services/ObjectStorage/os_configuring.html).
