---
layout: docs
title:  Reference information for IBM Streams Runner for Apache Beam
navtitle: Reference
description:  Learn about the package contents and pipeline options for IBM® Streams Runner for Apache Beam.
weight:  10
published: true
tag: beam
prev:
  file: beamrunner-4-monitor
  title: Monitoring
next:
  file: beamrunner-5a-io
  title: I/O options
---

Learn about the package contents and pipeline options for IBM® Streams Runner for Apache Beam.

## Package contents for Streams Runner

The Streams Runner package contains the following folders:

- `com.ibm.streams.beam`: The IBM Streams Runner for Apache Beam toolkit, which you can use to submit Apache Beam  2.1 applications to the IBM Streams runtime environment.

- `samples`: Toolkit sample applications. For information about the samples, see the README file in the samples folder.

## Pipeline Options
### General pipeline options

| Parameter | Description | Default value |
| --- | --- | --- |
| `runner` | The pipeline runner to use. Use this option to determine the pipeline runner at run time. | Set this option to `StreamsRunner` to run with IBM Streams. |
| `streaming` | A flag to indicate whether streaming mode is enabled (`true`). <br /><br /><strong>Note</strong>: IBM Streams is a pure streaming engine and does not have a discrete batch-processing mode. For this reason, this parameter is ignored and is automatically set to `true`.  | `true`  |
| `jobName` | The name of the job. | Defaults to a Beam-generated string. |
| `appName` | The name of the app for display purposes. | Defaults to the class name of the `PipelineOptions` creator. |

### Streams Runner pipeline options

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code class="highlighter-rouge">contextType</code></td>
      <td>The mode to run the application in:
      <ul><li><code class="highlighter-rouge">STREAMING_ANALYTICS_SERVICE</code>: Compile an application remotely and submit the translated application to a Streaming Analytics service on IBM Cloud (formerly IBM Bluemix).</li>
      <li><code class="highlighter-rouge">DISTRIBUTED</code>: Submit the application to a Streams instance. The domain and instance are configured by the <code class="highlighter-rouge">STREAMS_DOMAIN_ID</code> and <code class="highlighter-rouge">STREAMS_INSTANCE_ID</code> environment variables.</li>
      <li><code class="highlighter-rouge">DISTRIBUTED</code>: Submit the application to a Streams instance. The domain and instance are configured by the <code class="highlighter-rouge">STREAMS_DOMAIN_ID</code> and <code class="highlighter-rouge">STREAMS_INSTANCE_ID</code> environment variables.</li>
      <li><code class="highlighter-rouge">BUNDLE</code>: Create a Streams application bundle (SAB) file for submission at a later time.</li></ul></td>
      <td><code class="highlighter-rouge">STREAMING_ANALYTICS_SERVICE</code></td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">jarsToStage</code></td>
      <td>A list of JAR files (separated by colons) that are required to run the Apache Beam application. Include the JAR files that contain your program and any dependencies. (You don’t need to include Beam Google IO SDK or core Beam JAR files.) The listed JAR files are added to the SAB file.<br /><br /><strong>Note</strong>: The use of fat or uber JAR files can reduce the number of JAR files that must be specified, but take care not to include JAR files that are provided by the Streams Runner. Including redundant dependencies can increase the application archive and can negatively impact submission times to IBM Cloud.</td>
      <td>[null]</td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">filesToStage</code></td>
      <td>A JSON string that maps local file paths as keys to destination paths as values. The local files are included in the SAB and can be accessible to the application through the destination path. For example, <br /> <code class="highlighter-rouge">--filesToStage="{\"/path/to/local/file\": \"input/file1.in\", \"path/to/another/local/file\": \"env.conf\"}"</code><br /><br />  In this example, the two local files are added into the bundle at the specified destination paths, which can then be accessed by using <code class="highlighter-rouge">"streams://input/file1.in"</code> and <code class="highlighter-rouge">"streams://env.conf"</code> paths.</td>
      <td>[null]</td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">beamToolkitDir</code></td>
      <td>The location of the Streams Runner toolkit. Use this option to explicitly specify the Streams Runner toolkit location.</td>
      <td>Defaults to the path of the <code class="highlighter-rouge">com.ibm.streams.beam.translation.jar</code> file in the Java™ class path.</td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">tracingLevel</code></td>
      <td>Set the tracing and logging level of StreamsRunner translation and runtime. Levels: <code class="highlighter-rouge">ERROR</code>, <code class="highlighter-rouge">WARN</code>, <code class="highlighter-rouge">INFO</code>, <code class="highlighter-rouge">DEBUG</code>, <code class="highlighter-rouge">TRACE</code></td>
      <td><code class="highlighter-rouge">WARN</code></td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">textIOBundleSize</code></td>
      <td>The batch size for <code class="highlighter-rouge">TextIO.Write</code> transforms that create an output file per batch and per shard. Increase the batch size to decrease the number of output files that are created.</td>
      <td><code class="highlighter-rouge">50000</code></td>
    </tr>
  </tbody>
</table>

For the full list of pipeline options, enter  `--help=StreamsPipelineOptions` on the Beam application command line.

#### `STREAMING_ANALYTICS_SERVICE` context-specific pipeline options

| Parameter | Description | Default value |
| --- | --- | --- |
| `vcapServices` | The location of the Streaming Analytics VCAP file. This parameter is required when you use the `STREAMING_ANALYTICS_SERVICE` context type. This parameter can be omitted if the `$VCAP_SERVICES` environment variable is set to the path of the file. | [null] |
| `serviceName` | The name of the Streaming Analytics service on IBM Cloud. This parameter is required when you use the   `STREAMING_ANALYTICS_SERVICE`  context type. | [null] |

#### `DISTRIBUTED` context-specific pipeline options

| Parameter | Description | Default value |
| --- | --- | --- |
| `restUrl` | The URL for the REST API when you use the `DISTRIBUTED` context type. This parameter is required if you implement metrics in the application. | [null] |
| `userName` | The user name for basic authentication with REST API when you use the `DISTRIBUTED` context type. | [null] |
| `userPassword` | The user password for basic authentication for REST API when you use the `DISTRIBUTED` context type. | [null] |

## Environment Variables
These environment variables are not required for the Streams Runner to work; however, they can be used for convenience when you launch your Beam application.
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
        <td>The absolute path to the extraction location of the <code class="highlighter-rouge">com.ibm.streams.beam-1.1.0</code> directory</td>
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
        <td>The path to the IBM Cloud credentials file. If this environment variable is set, the <code class="highlighter-rouge">--vcapServices</code> parameter does not need to be specified on the command line.<br /><br />For more information about the credentials file, see <a href="#creating-a-credentials-file-for-your-streaming-analytics-service">Creating a credentials file for your Streaming Analytics service</a>.</td>
        <td>Set by using the <code class="highlighter-rouge">export</code> command.</td>
      </tr>
      <tr>
        <td>STREAMING_ANALYTICS_SERVICE_NAME</td>
        <td>The name of the Streaming Analytics service in the IBM Cloud credentials file to use. If this environment variable is set, the <code class="highlighter-rouge">--serviceName</code> parameter does not need to be specified on the command line.</td>
        <td>Set by using the <code class="highlighter-rouge">export</code> command.</td>
      </tr>
      <tr>
        <td>STREAMS_INSTALL</td>
        <td>The path to the local IBM Streams installation on your system. Only set if submitting an application to a local Streams environment.</td>
        <td><strong>Important</strong>: If this variable exists, you must use the <code class="highlighter-rouge">unset</code> command to unset it before you can submit an application to the Streaming Analytics service. </td>
      </tr>
    </tbody>
  </table>

## Apache Beam SDK for Java
See Beam's [Java API Reference](https://beam.apache.org/documentation/sdks/javadoc/2.1.0/) for information on application APIs.

## Streams Runner SDK API Reference
See the [javadoc](../beamrunner/release/1.1.0/javadoc/index.html) for more information.
