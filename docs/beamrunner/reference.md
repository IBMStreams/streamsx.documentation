---
layout: docs
title:  Reference information for IBM Streams Runner for Apache Beam
navtitle: Reference
description:  Learn about the package contents and pipeline options for IBM® Streams Runner for Apache Beam.
weight:  10
published: true
tag: beam
prev:
  file: monitor
  title: Monitoring
next:
  file: performance
  title: Performance considerations
---

Learn about the package contents and pipeline options for IBM® Streams Runner for Apache Beam.

## Package contents for Streams Runner

The Streams Runner package contains the following directories:

- `com.ibm.streams.beam`: The IBM Streams Runner for Apache Beam toolkit, which you can use to submit Apache Beam  2.4 applications to the IBM Streams runtime environment.

- `examples`: Toolkit sample applications. For information about the samples, see the README file in the `examples` directory.

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
      <td>A list of JAR files (separated by colons) that are required to run the Apache Beam application. Include the JAR files that contain your program and any dependencies. (You don’t need to include Beam Google IO SDK or core Beam JAR files.) The listed JAR files are added to the SAB file. Globs (wildcards) may be used to specify files (e.g., <code class="highlighter-rouge">`foo/bar/*.jar`</code>). However, globs in directory paths are not supported (e.g., <code class="highlighter-rouge">`**/*.jar`</code>).<br /><br /><strong>Note</strong>: The use of fat or uber JAR files can reduce the number of JAR files that must be specified, but take care not to include JAR files that are provided by Streams Runner. Including redundant dependencies can increase the application archive and can negatively impact submission times to IBM Cloud.</td>
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
      <td>Set the tracing and logging level of StreamsRunner translation and runtime. If specified, overrides all other tracing options. Levels: <code class="highlighter-rouge">ERROR</code>, <code class="highlighter-rouge">WARN</code>, <code class="highlighter-rouge">INFO</code>, <code class="highlighter-rouge">DEBUG</code>, <code class="highlighter-rouge">TRACE</code></td>
      <td><code class="highlighter-rouge">[null]</code></td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">traceTranslation</code></td>
      <td>Set the translation trace level for the application. Specify a single level: <code class="highlighter-rouge">ERROR</code>, <code class="highlighter-rouge">WARN</code>, <code class="highlighter-rouge">INFO</code>, <code class="highlighter-rouge">DEBUG</code>, <code class="highlighter-rouge">TRACE</code> to set all loggers to level and/or set individual components. Components include Runner and Streams. For example, to set Streams Runner to <code class="highlighter-rouge">WARN</code> and all other loggers to <code class="highlighter-rouge">INFO</code>, specify the following:<br /><br /><code class="highlighter-rouge">INFO,Runner=WARN</code></td>
      <td><code class="highlighter-rouge">Runner=INFO,Streams=WARN</code></td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">traceRuntime</code></td>
      <td>Set the runtime trace level for the application. See <code class="highlighter-rouge">traceTranslation</code> for more information.</td>
      <td><code class="highlighter-rouge">WARN</code></td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">bundleSize</code></td>
      <td>Controls the maximum number of data tuples in every bundle. Applications should make sure that each bundle does not exceed 2GB.</td>
      <td><code class="highlighter-rouge">1</code></td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">bundleMillis</code></td>
      <td>Controls the maximum time delay of every bundle. Applications should make sure that each bundle does not exceed 2GB.</td>
      <td><code class="highlighter-rouge">100</code></td>
    </tr>
    <tr>
      <td><code class="highlighter-rouge">parallelWidths</code></td>
      <td><strong>Experimental</strong><br /><br />Sets the parallelism for the entire Beam pipeline or individual transforms via transform step names. A default parallel width for the pipeline is specified as plain number with no step name, and a list of step paths with widths gives the widths for matching steps. If not specified, the parallel width for all transforms will be 1. Step matching is done the same way step names are matched in Beam<code class="highlighter-rouge">MetricsFilter</code>.<br /><br />If a step name matches multiple paths, the first match is used. Likewise, if a default is given multiple times, the first one is used.<br /><br />For example, the following configuration sets the default (entire pipeline parallelism) to width 2, but steps (transforms) that contain the subpath <code class="highlighter-rouge">Device_3/Map</code> will have width 3.<br /><br /> <code class="highlighter-rouge">--parallelWidths=2,Device_3/Map=3</code><br /><br />As the first match is taken, the parallel width for <code class="highlighter-rouge">Device_3/Map</code>  is still 3 in the following configuration.<br /><br /> <code class="highlighter-rouge">--parallelWidths=2,Device_3/Map=3,Map=4</code><br /><br /> For <code class="highlighter-rouge">Source</code> transforms, the runner attempts to match the configured parallel width by calling the <code class="highlighter-rouge">split</code> API. For <code class="highlighter-rouge">UnboundedSource</code>, the runner uses the specified parallel width as the desiredNumSplits argument in <code class="highlighter-rouge">split</code>. For <code class="highlighter-rouge">BoundedSource</code>, the runner uses the specified parallel width to calculate the <code class="highlighter-rouge">desiredBundleSizeBytes</code>. However, the <code class="highlighter-rouge">split</code> API does not guarantee to respect the desired widths. Some sources might be unsplittable, and some only split to a certain number of sub-sources. Source parallel width is set to either the specified width or the number of sub-sources, whichever is smaller. If there were more sub-sources than specified width, one channel could contain multiple sub-source instances.<br /><br />For <code class="highlighter-rouge">KV</code> <code class="highlighter-rouge">PCollection</code>s, it is guaranteed that the same key is always processed in the same parallel instance, correctly preserving per-key states.<br /><br />Changing parallel width (since IBM Streams release 4.3.0) dynamically at runtime will <b>break</b> Beam pipelines.</td>
      <td><code class="highlighter-rouge">[null]</code></td>
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
| `restUrl` | The URL for the REST API when you use the `DISTRIBUTED` context type. This parameter is required if you implement metrics in the application. | The return value of command `streamtool geturl` |
| `userName` | The user name for basic authentication with REST API when you use the `DISTRIBUTED` context type. | The `user.name` system property |
| `userPassword` | A path to a file containing the user password (recommended) or a string containing the user password for basic authentication for REST API when you use the `DISTRIBUTED` context type. If the option value is a path to a readable file, the first line of the file will be used as the password. | [null] |

## Environment Variables
These environment variables are not required for Streams Runner to work; however, they can be used for convenience when you launch your Beam application.
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
        <td>The absolute path to the extraction location of the `com.ibm.streams.beam-<runner-version>` directory, where `<runner-version>` is the version of Streams Runner</td>
        <td>Set by using one of the following methods:
        <ul><li>Source the <code class="highlighter-rouge">$STREAMS_RUNNER_HOME/examples/bin/streams-runner-env.sh</code> file.</li>
        <li>Use the  <code class="highlighter-rouge">export</code> command.</li></ul></td>
      </tr>
      <tr>
        <td>STREAMS_BEAM_TOOLKIT</td>
        <td>The path to the Streams Runner toolkit (<code class="highlighter-rouge">$STREAMS_RUNNER_HOME/com.ibm.streams.beam</code>)</td>
        <td>Set by using one of the following methods:
        <ul><li>Source the <code class="highlighter-rouge">$STREAMS_RUNNER_HOME/examples/bin/streams-runner-env.sh</code> file.</li>
        <li>Use the  <code class="highlighter-rouge">export</code> command.</li></ul></td>
      </tr>
      <tr>
        <td>VCAP_SERVICES</td>
        <td>The path to the IBM Cloud credentials file. If this environment variable is set, the <code class="highlighter-rouge">--vcapServices</code> parameter does not need to be specified on the command line.<br /><br />For more information about the credentials file, see <a href="../../../beamrunner-2b-sas/#creating-a-credentials-file-for-your-streaming-analytics-service">Creating a credentials file for your Streaming Analytics service</a>.</td>
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
See Beam's [Java API Reference](https://beam.apache.org/documentation/sdks/javadoc/2.4.0/) for information on application APIs.

## Streams Runner SDK API Reference
See the [javadoc](../release/1.2/javadoc/index.html) for more information.
