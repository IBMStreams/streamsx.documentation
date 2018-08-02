---
layout: docs
title:  Installing IBM Streams Runner for Apache Beam from an IBM Streaming Analytics service on IBM Cloud
navtitle: Installing
description:  Installing IBM® Streams Runner for Apache Beam from an IBM Streaming Analytics service on IBM Cloud involves downloading and extracting the Streams Runner toolkit, configuring environment variables, and creating a credentials file for your Streaming Analytics service.
weight:  10
published: true
tag: beam
prev:
  file: beamrunner-2-install
  title: Installing
next:
  file: using
  title: Using
---

Installing IBM® Streams Runner for Apache Beam from an IBM Streaming Analytics service on IBM Cloud involves downloading and extracting the Streams Runner toolkit, configuring environment variables, and creating a credentials file for your Streaming Analytics service. You don't need to install IBM Streams to use Streams Runner.

## Before you start
The Streaming Analytics installation of Streams Runner supports Apache Beam 2.1 applications, so your application must use the [Apache Beam SDK for Java API version 2.1](https://beam.apache.org/documentation/sdks/javadoc/2.1.0/)

## Creating a Streaming Analytics service on IBM Cloud

Before you can download Streams Runner, you must have a Streaming Analytics service so that you can open the Streams Console. The following video demonstrates how to create the service.

<iframe width="560" height="315" src="https://www.youtube.com/embed/zz0jqt61Xkg" frameborder="0" allowfullscreen></iframe>

<br>To create a Streaming Analytics service:

1. On the [IBM Cloud catalog](https://console.bluemix.net/catalog/) page, log in. If you don't have an IBM Cloud account, you can create one.
3. On the catalog page, use the **Filter** option to search for Streaming Analytics.
4. Click the **Streaming Analytics** service to configure an instance.
5. On the catalog page for the Streaming Analytics service, change **Service name** to something meaningful to you, for example, `Streaming Analytics-beam`.
6. Select a pricing plan.

    **Important**: To get the latest Streams Runner version, select a container-based plan like 'Lite' or 'Entry Container Hourly'.
6. Click **Create**. The service page opens and your service starts automatically. The service name appears as the title of the service page.

For more information about the Streaming Analytics service, see [Introduction to the Streaming Analytics Service in the IBM Cloud](https://developer.ibm.com/streamsdev/docs/streaming-analytics-now-available-bluemix-2/).

## Downloading and configuring Streams Runner
The following video demonstrates how to download and install the Streams Runner package.

<iframe width="560" height="315" src="https://www.youtube.com/embed/tG1uixwvnwg" frameborder="0" allowfullscreen></iframe>

<br>To download and install the Streams runner package:

1. Open the Streams Console:
    1. Click the **Manage** tab of your Streaming Analytics Service.
    1. Click **Launch**.
1. Download Streams Runner:
    1. In the Streams Console, click **Help > Download > Download Streams Runner for Apache Beam**.
    1. Select **Save File**, specify a location if necessary, and click **OK**.
1. Extract the toolkit by entering the following command where you downloaded the file, where `<runner-version>` indicates the version of the archive file:
```bash
tar -zxvf com.ibm.streams.beam-<runner-version>.tar.gz
```
1. (Optional) Configure the IBM Streams Runner environment variables.

    Tip: Although the variables are not required, the documentation refers to them for convenience. If you do not set the environment variables, you must use the full paths when you run the sample applications.
    1. Go to the `examples/bin` directory in the expanded toolkit and run the `streams-runner-env.sh` command to set up  environment variables for the runner:
    ```bash
    cd com.ibm.streams.beam-<runner-version>/examples/bin
    . streams-runner-env.sh
    ```

## Creating a credentials file for your Streaming Analytics service

To submit a Beam application to your Streaming Analytics service on IBM Cloud, you must create a JSON-formatted VCAP file that holds credentials and other information for the service. The following video demonstrates how to create the credentials file.

<iframe width="560" height="315" src="https://www.youtube.com/embed/YqtuWkxkaXU" frameborder="0" allowfullscreen></iframe>

<br>To create a VCAP file for an existing Streaming Analytics service:

1. Go to the directory where you installed the toolkit (`$STREAMS_RUNNER_HOME`) and copy the `template.vcap` file to a new file. Give the file a meaningful name and a file extension of `.vcap`.
2. Copy the credentials of your Streaming Analytics service:
   1. On the Streaming Analytics service page, click **Service credentials**.
   2. If necessary, create a credential by clicking **New credential**. Use the default information and click **Add**.
   3. Click **View credentials** for the credential that you want to use in your VCAP file. Click **Copy** to copy the credentials.
3. Paste the copied credentials into the VCAP file that you created, replacing the following line:  
    `<REMOVE THIS LINE AND INSERT CREDENTIALS HERE>`
4. (Optional) Configure the service credentials environment variables:

    Tip: Although the variables are not required, the documentation refers to them for convenience. If you do not set the environment variables, you must use the full paths when you run the sample applications.
    - `VCAP_SERVICES`: Point to the VCAP file that contains your Streaming Analytics service credentials.
    - `STREAMING_ANALYTICS_SERVICE_NAME`: Point to the service name within that file.

    For example:
```bash
export VCAP_SERVICES=$HOME/sample.vcap
export STREAMING_ANALYTICS_SERVICE_NAME="sample-service"
```


## Validating the Streams Runner installation

Streams Runner relies on preserving the `com.ibm.streams.beam` directory structure. To verify an installation, ensure that the `translation` and `sdk` JAR files appear as follows when you enter the following command:
```bash
ls $STREAMS_BEAM_TOOLKIT/lib
> com.ibm.streams.beam.sdk.jar  com.ibm.streams.beam.translation.jar
```

### The Streams Runner directory tree structure
```
com.ibm.streams.beam-<runner-version>/
| - template.vcap
| - README.html
| - README.md
| - com.ibm.streams.beam/
| | - info.xml
| | - toolkit.xml
| | - com.ibm.streams.beam.transforms/
| | - doc/
| | - opt/
| | - impl/
| | | - lib/
| | | | - com.ibm.streams.beam.runtime.jar
| | - lib/
| | | - com.ibm.streams.beam.sdk.jar
| | | - com.ibm.streams.beam.translation.jar
| - examples/
| | - README.html
| | - Makefile
| | - README.md
| | - src/
| | - doc/
| | - bin/
| | | - streams-runner-env.sh
| | - lib/
| | | - com.ibm.streams.beam.samples.jar
```
