---
layout: docs
title:  Introduction to IBM Streams Runner for Apache Beam
navtitle: Introduction
description:  You can use IBM® Streams Runner for Apache Beam to execute Apache Beam 2.0 pipelines in an IBM Streams environment.
weight:  10
published: true
tag: beam
next:
  file: beamrunner-2-install
  title: Installing
---

You can use IBM® Streams Runner for Apache Beam to execute Apache Beam 2.0 pipelines in an IBM Streams environment. A Beam application that is launched with Streams Runner is translated into a Streams Application Bundle (SAB) file. It is then optionally submitted to an IBM Streaming Analytics service in IBM Bluemix or to an existing IBM Streams domain and instance.

The following tables show how Streams Runner fits into the [Beam capability matrix](https://beam.apache.org/documentation/runners/capability-matrix/).

&#10003; Fully supported<br>
~ Partially supported

##### What results are being calculated?

<table>
  <tbody>
    <tr id="cap-summary-what"></tr>
    <tr>
      <th>Transforms</th>
      <th>ParDo</th>
      <th>GroupByKey</th>
      <th>Flatten</th>
      <th>Combine</th>
      <th>Composite</th>
      <th>Side Inputs</th>
      <th>Source API</th>
      <th>Metrics</th>
      <th>Stateful</th>
    </tr>
    <tr>
      <th>Streams Runner</th>
      <td><center>&#10003;</center></td>
      <td><center>&#10003;</center></td>
      <td><center>&#10003;</center></td>
      <td><center>&#10003;</center></td>
      <td><center><b>~</b></center></td>
      <td><center>&#10003;</center></td>
      <td><center>&#10003;</center></td>
      <td><center><b>~</b></center></td>
      <td><center><b>~</b></center></td>
    </tr>
  </tbody>
</table>

##### Where in event time?

<table>
  <tbody>
    <tr>
      <th>Windows</th>
      <th>Global</th>
      <th>Fixed</th>
      <th>Sliding</th>
      <th>Session</th>
      <th>Custom</th>
      <th>Custom Merging</th>
      <th>Timestamp</th>
    </tr>
    <tr>
      <th>Streams Runner</th>
      <td><center>&#10003;</center></td>
      <td><center>&#10003;</center></td>
      <td><center>&#10003;</center></td>
      <td><center>&#10003;</center></td>
      <td><center>&#10003;</center></td>
      <td><center>&#10003;</center></td>
      <td><center>&#10003;</center></td>
    </tr>
  </tbody>
</table>

##### When in processing time?

<table>
  <tbody>
    <tr>
      <th>Triggers</th>
      <th>Configurable</th>
      <th>Event-Time</th>
      <th>Processing-Time</th>
      <th>Count</th>
      <th>Composite</th>
      <th>Allowed Lateness</th>
      <th>Timer</th>  
    </tr>
    <tr>
      <th>Streams Runner</th>
      <td><center>&#10003;</center></td>
      <td><center>&#10003;</center></td>
      <td><center>&#10003;</center></td>
      <td><center>&#10003;</center></td>
      <td><center>&#10003;</center></td>
      <td><center>&#10003;</center></td>
      <td><center><b>~</b></center></td>
    </tr>
  </tbody>
</table>

##### How do refinements of results relate?

<table>
  <tbody>
    <tr>
      <th>Refinements</th>
      <th>Discard</th>
      <th>Accumulate</th>
    </tr>
    <tr>
      <th>Streams Runner</th>
      <td><center>&#10003;</center></td>
      <td><center>&#10003;</center></td>
    </tr>
  </tbody>
</table>
<br>

For more information about Apache Beam, see the [Apache Beam documentation](https://beam.apache.org/documentation/).
