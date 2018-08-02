---
layout: docs
title: TemperatureSample sample application for IBM Streams Runner for Apache Beam
navtitle: TemperatureSample sample app
description:  You can use a simple application called `TemperatureSample` to learn how to submit and monitor an Apache Beam 2.4 application in the Streaming Analytics service on IBM Cloud.
weight:  10
published: true
tag: beam
prev:
  file: io
  title: I/O options
next:
  file: wordcount
  title: WordCount sample app
---

You can use a simple application called `TemperatureSample` to learn how to submit and monitor an Apache Beam 2.4 application in the Streaming Analytics service on IBM Cloud (formerly IBM Bluemix).  The sample application is included with IBM® Streams Runner for Apache Beam. Some familiarity with Beam programming is helpful, though not required; the [Apache Beam website](https://beam.apache.org/) has a useful [Apache Beam Java SDK Quickstart](https://beam.apache.org/get-started/quickstart-java/) page and other documentation.

For more information about this sample application, see [The TemperatureSample application](#the-temperaturesample-application).

## Before you start

Before you run the `TemperatureSample` sample application, you must configure and run the following service on IBM IBM Cloud®:

- Streaming Analytics. For more information, see [Creating a Streaming Analytics service on IBM Cloud](../../../beamrunner-2b-sas/#creating-a-streaming-analytics-service-on-bluemix).

**Important**: If you want to compile your application on IBM Cloud, you must unset the `STREAMS_INSTALL` variable before you submit the application to the Streaming Analytics service.

## Running the `TemperatureSample` application
The following video demonstrates how to launch the `TemperatureSample`.

<iframe width="560" height="315" src="https://www.youtube.com/embed/i-inPl4Yf58" frameborder="0" allowfullscreen></iframe>
<br>

2. Navigate to the `$STREAMS_RUNNER_HOME/examples` directory. The Streams Runner toolkit provides all necessary files. Assuming that all environment variables are set as described in [Downloading and configuring Streams Runner](../../../beamrunner-2a-onprem/#downloading-and-configuring-streams-runner) and that the `$VCAP_SERVICES` IBM Cloud credentials file has credentials in it named `beam-service`, you can launch the `TemperatureSample` application with the following command:

   ```bash
   java -cp \
   $STREAMS_BEAM_TOOLKIT/lib/com.ibm.streams.beam.translation.jar:\
   $STREAMS_RUNNER_HOME/examples/transform/target/beam-examples-transform-<runner-version>.jar \
   com.ibm.streams.beam.examples.transform.temperature.TemperatureSample \
   --runner=StreamsRunner \
   --contextType=STREAMING_ANALYTICS_SERVICE \
   --jarsToStage=$STREAMS_RUNNER_HOME/examples/transform/target/beam-examples-transform-x.y.x.jar
   ```

   **Note**: If the environment variables are not set, you must use full paths, and use the `--vcapServices` parameter to provide the path to the IBM Cloud credentials file.

   For more information about the parameters available to you, see [Pipeline options for Streams Runner](../reference/#streams-runner-pipeline-options).

3. Verify that the application started successfully.

   Streams Runner displays information (INFO) messages as it processes the Beam pipeline for your application, turning it into an IBM Streams application bundle (.sab) file, and eventually submitting the .sab file to IBM Cloud:

   ```
   Sep 27, 2017 2:34:19 PM com.ibm.streams.beam.translation.StreamsRunner run
   INFO: Running pipeline using StreamsRunner in context:
        contextType=STREAMING_ANALYTICS_SERVICE
        beamToolkitDir=null
        tracingLevel=null
        jobName=temperaturesample-johnmac-0927183419-7a8ccbfa
   StreamsRunner: Sending application to be built remotely, then submitting to Streaming Analytics Service...
   StreamsRunner: Application successfully submitted to Streaming Analytic service with Job ID: 1
   ```

   If you see an exception or error report, it indicates the reason for the failure. The following issues are common:

   - A typographical error in the `java` command or one of the variables it uses.
   - A problem with the `$VCAP_SERVICES` file or the wrong service name. Check that the `"credentials"` for `"streaming-analytics"` in the `$VCAP_SERVICES`file match those for your Streaming Analytics service, and that the `"name"` matches the name that you used for the `--serviceName` option to the `java` command.

## Viewing the running application

After the job is submitted successfully, the application output is displayed while it reports metrics:

```
----- Temperature Metrics --------------------------------------------------
good.summary: DistributionResult{sum=272674, count=5434, min=0, max=100}
good.device_1: DistributionResult{sum=88417, count=1792, min=0, max=100}
good.device_3: DistributionResult{sum=90876, count=1806, min=0, max=100}
good.device_2: DistributionResult{sum=93381, count=1836, min=0, max=100}
bad.device_1: 365
bad.device_2: 329
bad.device_3: 373
bad.total: 1067
----- System Metrics for step MergeReadings --------------------------------
MetricName{namespace=com.ibm.streams, name=nTuplesProcessed}: 12585
MetricName{namespace=com.ibm.streams, name=nTuplesSubmitted}: 12581
```
At this point, the application is also visible in the Streams console in IBM Cloud.
To launch the Streams Console, navigate to the **Manage** tab of your Streaming Analytics Service and click **Launch**.

<img src="/streamsx.documentation/images/beamrunner/appinconsole.jpg" alt="The application running in Streams Console in IBM Cloud" width="650" />

Of particular interest for this application is the Streams Graph. The graph shows how the Streaming Analytics service organizes and executes the code in the sample application. When you maximize the graph, you can see the graph of the whole application:

<img src="/streamsx.documentation/images/beamrunner/appgraph.jpg" alt="The application graph maximized" width="650" />

By default, the graph shows the Beam transforms of the application and matches the pipeline structure that is described in the overview. The names that are used in the graph are the same as those used in the application unless there are transform names that are not unique.

Although this simplified view matches Beam, it omits details about how  Streams is executing the application. To see those details, click  **Configure** (the wrench icon), select **Show raw graph**, and click **Apply**.

Now the application is shown with the Streams operators instead of the Beam transforms. It is still similar in structure, and the names are similar to the Beam names but not always identical. In some cases, the Streams operator name contains extra information that comes from the names of the Beam Java™ SDK classes that implement the transforms. Also, Streams does not allow all the same characters in operator names that Beam allows in transform names, so characters might be removed or replaced with valid Streams characters.

You can use the Beam [metrics API](https://beam.apache.org/documentation/sdks/javadoc/2.4.0/org/apache/beam/sdk/metrics/package-summary.html) to insert information to monitor your application. For more information, see [Monitoring IBM Streams Runner for Apache Beam](../monitor/).

## Stopping the application

After you explore the Streams console, stop the application by canceling the job. You can cancel the job in several ways, from almost any place that shows the job in the console, but the simplest way is by clicking **Cancel Jobs** in the navigation bar. Clicking **Cancel Jobs** opens a window that shows running jobs. Select the job or jobs that you want to cancel, in this case the job that is running the sample, and click **Cancel Jobs**.
<img src="/streamsx.documentation/images/beamrunner/canceljobbutton.jpg" alt="Cancel Jobs in the navigation bar" width="100"/>

<img src="/streamsx.documentation/images/beamrunner/canceljobwindow.jpg" alt="Cancel Jobs window" width="400" />

**Important**: Interrupting or killing the `java` command in the terminal where you started the application does _not_ cause the job to be stopped, even though the job does stop reporting metrics.

## The `TemperatureSample` application

The `TemperatureSample` application takes temperature readings from multiple devices. The application splits the readings into "good" (valid) and "bad" (invalid) readings based on a specific threshold. It counts the bad readings and generates some basic statistics for the good readings, and finally logs the results. The full source is available in the `$STREAMS_RUNNER_HOME/examples/transform/src/com/ibm/streams/beam/examples/transform/temperature` directory, but excerpts are included here to describe the structure of the pipeline.

The devices are artificial; they use the Beam `CountingInput` transforms named Counter\_*n* to drive another transform named Device\_*n* to generate random readings:

```java
PCollectionList<KV<String,Double>> deviceReadings = PCollectionList.empty(pipeline);

for (int deviceId = 1; deviceId <= options.getNumDevices(); ++deviceId) {
    PCollection<KV<String,Double>> readings = pipeline
            .apply("Counter_" + deviceId, CountingInput.unbounded()
                    .withRate(options.getRate(), Duration.standardSeconds(1)))
            .apply("Device_" + deviceId, MapElements.via(new GenReadingFn(deviceId, maxTemp)));
    deviceReadings = deviceReadings.and(readings);
}
```

These readings act as inputs to a `MergeReadings` transform. The transform merges readings from the different devices into a single stream of data that consists of pairs of _{deviceName,temperatureReading}_, which are then assigned to windows of fixed time duration:

```java
PCollection<KV<String,Double>> mergedReadings = deviceReadings
        .apply("MergeReadings", Flatten.<KV<String,Double>>pCollections())
        .apply("WindowReadings",
                Window.<KV<String,Double>>into(
                        FixedWindows.of(Duration.standardSeconds(options.getWindowSize()))));
```

The windowed data is validated with a `ValidateReadings` transform that produces two output streams, one of good readings and one of bad readings:

```java
final TupleTag<KV<String,Double>> goodTag = new TupleTag<KV<String,Double>>(){ ... }
final TupleTag<KV<String,Double>> badTag = new TupleTag<KV<String,Double>>(){ ... }
final double badTempThreshold = options.getBadTempThreshold();

PCollectionTuple validatedReadings = mergedReadings.apply("ValidateReadings",
        ParDo.of(new DoFn<KV<String,Double>,KV<String,Double>>() {
            private static final long serialVersionUID = 1L;

            @ProcessElement
            public void processElement(ProcessContext c) {
                String device = c.element().getKey();
                Double temp = c.element().getValue();
                if (temp < badTempThreshold) {
                    // Good reading, output and update distribution metrics
                    c.output(c.element());
                    ...
                } else {
                    // Bad reading, output to side output, update counters
                    c.output(badTag, c.element());
                    ...
                }
            }
        }).withOutputTags(goodTag, TupleTagList.of(badTag)));
```

On the good readings, statistics are calculated in a `GoodStats` transform and then logged by a `GoodLog` transform:

```java
validatedReadings
        .get(goodTag)
        .apply("GoodStats", Combine.<String, Double, Stats>perKey(new DeviceStatsFn()))
        .apply("GoodLog", ParDo.of(new LogWindowFn<Stats>("Temperature device statistics")));
```

The bad readings are counted by a `BadCount` transform and logged by the `BadLog` transform:

```java
validatedReadings
        .get(badTag)
        .apply("BadCount", Count.<String,Double>perKey())
        .apply("BadLog", ParDo.of(new LogWindowFn<Long>("Temperature device error count")));
```

The structure of the application becomes clear after it is displayed in the Streams console after the application is run.
