---
layout: docs
title:  Installing IBM Streams Runner for Apache Beam
navtitle: Installing
description:  
weight:  10
published: true
tag: beam
prev:
  file: beamrunner-1-intro
  title: Introduction
next:
  file: beamrunner-2a-using
  title: Using
---

Installing IBM® Streams Runner for Apache Beam involves downloading and extracting the Streams Runner toolkit, configuring environment variables, and creating a credentials file for your Streaming Analytics service.

## Before you start

A Red Hat Enterprise Linux 6 or 7 environment is recommended for submitting Apache Beam 2.0 applications to the Streaming Analytics service in Bluemix.

## Creating a Streaming Analytics service on Bluemix

Before you can download Streams Runner, you must have a Streaming Analytics service so that you can open the Streams Console. For a video demonstration of creating the service, see [Creating a Streaming Analytics service on IBM Bluemix](https://ibm.box.com/s/fz0mq6plxuiqx8dfjtwenldyr6vopolz).
`Need updated link???`

To create a Streaming Analytics service:

1. On the [Bluemix catalog](https://console.ng.bluemix.net/catalog/services/streaming-analytics/?cm_mc_uid=05407033353914938482142&amp;cm_mc_sid_50200000=) page, log in. If you don't yet have a Bluemix account, you can create one.
2. On the Bluemix dashboard page, click **Catalog**.
3. Use the **Filter** option to search for Streaming Analytics.
4. Click the **Streaming Analytics** service to configure an instance.
5. On the catalog page for the Streaming Analytics service, change **Service name** to something meaningful to you, for example, `Streaming Analytics-beam`.
6. Click **Create**. The service page opens and your service starts automatically. The service name appears as the title of the service page.

For more information about the Streaming Analytics service, see [Introduction to the Bluemix Streaming Analytics Service](https://developer.ibm.com/streamsdev/docs/streaming-analytics-now-available-bluemix-2/).

## Downloading and configuring Streams Runner

1. Open the Streams Console:
    1. Click the **Manage** tab of your Streaming Analytics Service.
    1. Click **Launch**.
1. Download Streams Runner:
    1. In the Streams Console, click **Help > Download > Download Streams Runner for Apache Beam**.
    1. Select **Save File**, specify a location if necessary, and click **OK**.
1. Extract the toolkit by entering the following command where you downloaded the file:
```
tar -zxvf com.ibm.streams.beam-1.0.0.tar.gz
```
1. (Optional) Configure the environment variables. Although the variables are not required, the documentation refers to them for convenience. If you do not set the environment variables, you must use the full paths when you run the sample applications.
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th>Description</th>
        <th>Notes</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>STREAMS_RUNNER_HOME</td>
        <td>The absolute path to the extraction location of the <code class="highlighter-rouge">com.ibm.streams.beam-1.0.0</code> directory</td>
        <td>Set by using one of the following methods:
        <ul><li>Source the <code class="highlighter-rouge">$STREAMS_RUNNER_HOME/samples/bin/streams-runner-env.sh</code> file.</li>
        <li>Use the  <code class="highlighter-rouge">export</code> command.</li></ul></td>
      </tr>
      <tr>
        <td>STREAMS_BEAM_TOOLKIT</td>
        <td>The path to the Streams Runner toolkit (<code class="highlighter-rouge">$STREAMS_RUNNER_HOME/com.ibm.streams.beam</code>)</td>
        <td>Set by using one of the following methods:
        <ul><li>Source the <code class="highlighter-rouge">$STREAMS_RUNNER_HOME/samples/bin/streams-runner-env.sh</code> file.</li>
        <li>Use the  <code class="highlighter-rouge">export</code> command.</li></ul></td>
      </tr>
      <tr>
        <td>VCAP_SERVICES</td>
        <td>The path to the Bluemix credentials file. If this environment variable is set, the <code class="highlighter-rouge">--vcapServices</code> parameter does not need to be specified on the command line.<br /><br />For more information about the credentials file, see <a href="#creating-a-credentials-file-for-your-streaming-analytics-service">Creating a credentials file for your Streaming Analytics service</a>.</td>
        <td>Set by using the <code class="highlighter-rouge">export</code> command.</td>
      </tr>
      <tr>
        <td>STREAMING_ANALYTICS_SERVICE_NAME</td>
        <td>The name of the Streaming Analytics service in the Bluemix credentials file to use. If this environment variable is set, the <code class="highlighter-rouge">--serviceName</code> parameter does not need to be specified on the command line.</td>
        <td>Set by using the <code class="highlighter-rouge">export</code> command.</td>
      </tr>
      <tr>
        <td>STREAMS_INSTALL</td>
        <td>The path to the IBM Streams installation if Streams is installed </td>
        <td><strong>Important</strong>: If this variable exists, you must use the `unset` command to unset it before you submit an application to the Streaming Analytics service. </td>
      </tr>
    </tbody>
  </table>

## Validating the Streams Runner installation

The Streams Runner relies on preserving the `com.ibm.streams.beam` directory structure. To verify an installation, ensure that the translation and sdk JAR files appear as follows when you enter the following command:
`ls $STREAMS_BEAM_TOOLKIT/lib`

```
> com.ibm.streams.beam.sdk.jar  com.ibm.streams.beam.translation.jar
```

The Streams Runner directory tree structure:
```
com.ibm.streams.beam-1.0.0/
| - template.vcap
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
| - samples/
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

## Creating a credentials file for your Streaming Analytics service

To submit a Beam application to your Streaming Analytics service on Bluemix, you must create a JSON-formatted VCAP file that holds credentials and other information for the service. For a video demonstration of creating the credentials file, see [Creating a credentials file for the Streaming Analytics service on IBM Bluemix](https://ibm.box.com/s/qasw203e6gtdjpwu5ybmygcvstkr0xx8).
`need updated link???`

To create a VCAP file for an existing Streaming Analytics service:

1. Navigate to the folder where you installed the toolkit (`$STREAMS_RUNNER_HOME`) and copy the `template.vcap` file to a new file. Give the file a meaningful name and a file extension of `.vcap`.
2. Copy the credentials of your Streaming Analytics service:
  1. On the Streaming Analytics service page, click **Service credentials**.
  2. If necessary, create a credential by clicking **New credential**. Use the default information and click **Add**.
  3. Click **View credentials** for the credential that you want to use in your VCAP file. Click **Copy** to copy the credentials.
3. Paste the copied credentials into the VCAP file that you created, replacing the following line:  
    `<REMOVE THIS LINE AND INSERT CREDENTIALS HERE>`
