---
layout: docs
title:  Performance Considerations for IBM Streams Runner for Apache Beam
navtitle: Performance
description: The performance of your IBM® Streams Runner for Apache Beam application is affected by options and configuration parameters.
weight:  10
published: true
tag: beam
prev:
  file: reference
  title: Runner reference
next:
  file: troubleshoot
  title: Troubleshooting
---

The performance of your IBM® Streams Runner for Apache Beam application is
affected by options and configuration parameters given to both the runner
and the IBM Streams instance where your application is deployed.
Understanding how these work will help you get the best performance.

## Bundling elements

The [`DoFn`](https://beam.apache.org/documentation/sdks/javadoc/2.4.0/org/apache/beam/sdk/transforms/DoFn.html)
instances that make up an Apache Beam application process elements in
arbitrary bundles created by the runners. Bundling elements together can
increase overall throughput but can increase latency of individual
elements.

The IBM Streams Runner for Apache Beam pipeline options `--bundleSize` and
`--bundleMillis` control how the runner handles bundles by either directing
the runner to create bundles of a maximum number of elements, or after a
maximum time delay, whichever limit is reached first.

For more information on these options, see [Streams Runner pipeline
options](../reference/#streams-runner-pipeline-options).

## Parallelism

Parallelism is a key concept in Apache Beam and many transforms are able to
process elements in parallel. The IBM Streams Runner for Apache Beam has
experimental support for parallelism using the `--parallelWidths` pipeline
option. Using this option allows the runner to take advantage of IBM
Streams user-defined parallelism when translating and running your
application.

The simplest way to enable parallelism for your application is to set a
default width for the entire application, for example `--parallelWidth=4`
will cause the runner to use parallelism of 4 wherever it can.

In some cases finer control can be useful if, for example, some transforms
in the application will benefit more or less from parallelism. In that
case, the option can supply widths for matching steps.

As an example, suppose the application has a step `VeryParallel` that could
benefit from more parallelism than most of the application as well as one
named `Serial` that should not be parallelized at all. Using the pipeline
option `--parallelWidths=4,Serial=1,VeryParallel=8` would disable
parallelism for `Serial` while using higher parallelism for `VeryParallel`
than the rest of the application.

`PCollection`s of [`KV`](https://beam.apache.org/documentation/sdks/javadoc/2.4.0/org/apache/beam/sdk/values/KV.html) elements are partitioned based on keys. The same key will always go into
the same parallel channel, guaranteeing that keyed states are correctly
handled. `PCollections` of other types are partitioned using the round-robin
scheme. It is applications' responsibility to balance workloads across keys.
Skewed workloads can overwhelm hot keys and hamper performance. Since the
value of keys are determined by applications, the runner cannot easily
detect or predict keys. If a `PCollection` contains fewer keys than the
parallel width, some parallel channels will stay idle, wasting system
resources. One special case is a `PCollection` using the `Void` key. In this
situation, the runner can identify that there is only one global key and
run the transform in a non-parallelized form. The following code snippet
demonstrates an example. As the `AddKey` transform adds the same `Void` key
to all elements, the downstream `GBK` cannot run in parallel. If a user
specifies a parallel width (greater than 1) for the entire pipeline, the
runner can silently ignore the parallel width for the section of the pipeline
that uses the `Void` keys. If a user explicitly specifies a parallel width
for the `GBK` in the example, the runner, again, can ignore the specified width.

```java
Pipeline p = Pipeline.create(options);
p.apply("Source", GenerateSequence.from(0))
 .apply("AddKey", WithKeys.of((Void) null))
 .setCoder(KvCoder.of(VoidCoder.of(), VarLongCoder.of()))
 .apply("GBK", GroupByKey.create());
```

For [`Source`](https://beam.apache.org/documentation/sdks/javadoc/2.4.0/org/apache/beam/sdk/io/Source.html)
transforms, the runner attempts to match the configured parallel width
by splitting the source into sub-sources using the [`UnboundedSource#split`](https://beam.apache.org/documentation/sdks/javadoc/2.4.0/org/apache/beam/sdk/io/UnboundedSource.html) or [`BoundedSource#split`](https://beam.apache.org/documentation/sdks/javadoc/2.4.0/org/apache/beam/sdk/io/BoundedSource.html) method. Applications need to make sure
that the source implementation supports `split` properly. If the number
of sub-sources returned by `split` disagrees with the parallel width, the
source parallel width is set to the smaller value of the specified width and
the number of sub-sources. If there are more sub-sources than the specified
width, the runner will allocate sub-sources to parallel channels in a
round-robin fashion and one parallel channel can contain multiple
sub-source instances. To get the best performance, the number of sub-sources
should match the expected parallel width.

For more information on this option, see [Streams Runner pipeline
options](../beamrunner-6-ref/#streams-runner-pipeline-options).

When the runner launches the application it will set the IBM Streams
operator `fusionType` to `channelIsolation`. To change the fusion type use
the pipeline option `--contextType=BUNDLE` to create your application
bundle and set the fusion type when submitting the bundle. See [The
`BUNDLE` Context](../beamrunner-3-using/#the-bundle-context) for more
information about `--contextType=BUNDLE` and [Operator fusion in parallel
regions **FIX
LINK**](http://leto.svl.ibm.com:9343/help/topic/com.ibm.streams.dev.doc/doc/udpsplpartconfig.html)
for more information on fusion configuration.

Note that IBM Streams Runner for Apache Beam does not allow changing the
degree of parallelism at submission time or at run time.

## Tracing

Tracing can give information about the translation and execution of your
IBM Streams Runner for Apache Beam application and can help debug problems,
but tracing can have a serious performance impact.

If you set tracing levels other than the defaults with any of the
`--traceTranslation`, `--traceRuntime`, or `--tracingLevel` pipeline
options while you are developing and debugging your application, remove
them or set them back to the defaults when deploying your application in
production.

More documentation about tracing options and levels can be found in
[Streams Runner pipeline
options](../beamrunner-6-ref/#streams-runner-pipeline-options).

## IBM Streams performance

Once your IBM Streams Runner for Apache Beam application is running on an
IBM Streams instance, it is subject to the same performance considerations
as any other IBM Streams application. See the IBM Streams documentation for
more information on performance. **(TBD: LINK)**
