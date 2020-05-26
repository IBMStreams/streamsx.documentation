---
layout: docs
title:  Getting started with the IBM Streams Quick Start Edition
description:  Learn how to get started with IBM Streams Quick Start Edition
weight:  50
published: true

tag: 43qse
prev:
  file: qse-intro
  title:  Download Quick Start Edition
---

## Table of Contents

- [Download and install](#install)
- [Start developing applications with SPL, Python or Java](#dev)
- [Monitor applications with Streams Console](#console)
- [Integrate with other systems and technologies](#extend)


<a id="install"></a>

## Download and install

If you haven't already done so, download and install Streams Quick Start Edition. For instructions, see [Try IBM Streams Quick Start Edition](../qse-intro).

## Quick Start Edition overview

The Quick Start Guide comes with the following software already installed:

-   CentOS Linux release 7.7 (64-bit)
-   IBM Streams Quick Start Edition 4.3.1.1, including Streams Studio


<table width="60%">
<tbody><tr>
<th>Parameter</th>
<th>Value</th>
</tr>
<tr>
<td>Host name</td>
<td>streamsqse (streamsqse.localdomain)</td>
</tr>
<tr>
<td>User and administrator ID</td>
<td>streamsadmin (logged in automatically)</td>
</tr>
<tr>
<td>User home directory</td>
<td>/home/streamsadmin</td>
</tr>
<tr>
<td>User password</td>
<td>passw0rd (password with a zero for the O)</td>
</tr>
<tr>
<td>root password</td>
<td>passw0rd</td>
</tr>
<tr>
<td>Streams domain</td>
<td>StreamsDomain (started automatically)</td>
</tr>
<tr>
<td>Streams instance</td>
<td>StreamsInstance (started automatically)</td>
</tr><tr>
<td>Streams Console (used to administer the domain and instance)</td>
<td>https://streamsqse.localdomain:8443/streams/domain/console</td>
</tr>
</tbody></table>

<br/>
<a id="dev"></a>

## Getting started for developers

Pick one of the development guides to learn how to develop applications with Python, Java or Streams Processing Language (SPL).

### Learn Streams Processing Language (SPL)

**[Start here](/streamsx.documentation/docs/spl/quick-start/qs-0)** to launch your first application using the QSE.
  
Next, get familiar with Streams Studio in the [Streams Studio tutorial](/streamsx.documentation/docs/spl/lab/spl-lab-00-get-started/).

### Python developers
Follow the [Python development guide](/streamsx.documentation/docs/python/1.6/python-appapi-devguide/).


###  Java developers

Create an application entirely in Java in the  [Java development guide](/streamsx.documentation/docs/java/java-appapi-devguide/).

#### Use Java code in SPL applications

If you have existing Java code, you can easily reuse your code within an SPL application by writing a Java operator or native Java functions.

Some familiarity with SPL is required, so you need to learn about SPL first.  Then follow the [Java Operator Development Guide](../../java/java-op-dev-guide/)



<a id="console"></a>


## Streams management and administration

Streams Console is the web-based administration console for monitoring and managing your Streams instance. Create customized dashboards to monitor your Streams domain, instances and applications.

<img src="/streamsx.documentation/images/qse/Application-Dashboard-4.1.png" alt="Streams Console" style="width: 60%;"/>

To familiarize yourself with Streams Console, see this video:

<button class="btn btn-primary btn-md" data-toggle="modal" data-target="#streamsConsole">
Video:  Streams Console
</button>

<a id="extend"></a>


## Integrate with other technologies   
You can connect to external data sources using toolkits.  A toolkit is a reusable artifact that provides function, for example, the Kafka toolkit provides functionality to connect  to Apache Kafka.

Streams includes toolkits that support the most popular systems like [HDFS](https://github.com/IBMStreams/streamsx.hdfs), [HBase](https://github.com/IBMStreams/streamsx.hbase), [Kafka](https://ibmstreams.github.io/streamsx.kafka/docs/user/overview/), Active MQ and more. 

Refer to the [Product Toolkits Overview](https://developer.ibm.com/streamsdev/docs/product-toolkits-overview/) for a full list of toolkits included in Streams.

**Find more toolkits on GitHub**

In addition to the toolkits included in the install, [IBMStreams on GitHub](https://github.com/ibmstreams) includes open sour a platform that enables Streams to rapidly add support for emerging technologies.  It also includes sample applications and helpful utilities.  

For a list of open-source projects hosted on GitHub, see: [IBM Streams GitHub Projects Overview](https://developer.ibm.com/streamsdev/docs/github-projects-overview/).

### Streams and SPSS

SPSS is analytic predictive software that enables you to build predictive models from your data.  Your application can perform real-time predictive scoring by running these predictive models using the SPSS operators.

To learn about Streams can integrate with SPSS:  [Streams and SPSS Lab](https://developer.ibm.com/streamsdev/docs/spss-analytics-toolkit-lab/).


### Streams and Microsoft Excel

<img src="/streamsx.documentation/images/qse/BargainIndex1.jpg" alt="Streams and Excel" style="width: 60%;"/>

IBM Streams integrates with Microsoft Excel, allowing you to see, analyze and visualize live streaming data in an Excel worksheet.  This article helps you get started:  [Streams for Microsoft Excel](https://developer.ibm.com/streamsdev/docs/streams-4-0-streams-for-microsoft-excel/)

In the following demo, we demonstrate how you may build a marketing dashboard from real-time data using Excel.

<button class="btn btn-primary btn-md" data-toggle="modal" data-target="#streamsAndExcel">
Video:  Streams and Excel Demo
</button>

### Operational Decision Manager (ODM)

IBM Streams integrates with ODM rules, allowing you to create business rules, construct rule flows, and create and deploy rules applications to analyze data and automate decisions in real-time.  This article helps you get started:  [ODM Toolkit Lab](https://developer.ibm.com/streamsdev/docs/rules-toolkit-lab/)


### Integration with IBM InfoSphere Data Governance Catalog

With IBM InfoSphere Data Governance Catalog integration, developers can easily discover the data and schema that are available for use.  By building data lineage with your Streams application, you can quickly see and control how data is consumed.
To get started, see the  [Streams Governance Quick Start Guide](../governance/governance-quickstart/).


### SparkMLLib in Streams

To get started, follow this development guide:

* [SparkMLLib Getting Started Guide](https://developer.ibm.com/streamsdev/docs/getting-started-with-the-spark-mllib-toolkit/)

### Apache Edgent (aka Open Embedded Streams) Integration

Gather local, real-time analytics from equipment, vehicles, systems, appliances, devices and sensors of all kinds. To get started, check out the Apache Edgent website for more information and guides:

* [Apache Edgent Official Website](https://edgent.incubator.apache.org/)



## Streams Community
The following Streams resources can help you connect with the Streams community and get support when you need it:

* **[Streamsdev](https://developer.ibm.com/streamsdev/)** - This resource is a developer-to-developer website maintained by the Streams Development Team.  It contains many useful articles and getting started material.  Check back often for new articles, tips and best practices to this website.
* **[Streams Forum](https://www.ibmdw.net/answers/questions/?community=streamsdev&sort=newest&refine=none)** - This forum enables you to ask, and get answers to your questions, related to IBM Streams. If you have questions, start here.
* **[IBMStreams on GitHub](http://ibmstreams.github.io)** - Streams is shipped with many useful toolkits out of the box.  IBMStreams on GitHub  contains many open-source toolkits.  For a list of available toolkits available on GitHub, see this web page:  [IBMStreams GitHub Toolkits](https://developer.ibm.com/streamsdev/docs/github-projects-overview/).
* **[IBM Streams Support](http://www.ibm.com/support/entry/portal/Overview/Software/Information_Management/InfoSphere_Streams)** - This website provides information about IBM Streams downloads, technical support tools, documentation, and other resources.
* **[IBM Streams Product Site](http://www.ibm.com/analytics/us/en/technology/stream-computing/)** - This website provides a broad range of information and resources about Streams and related topics.


<!-- Modal -->

<div class="modal fade" id="streamsStudioInAction" tabindex="-1" role="dialog" aria-labelledby="streams-studio-in-action" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="streams-studio-in-action">Streams Studio in Action</h4>
      </div>
      <div class="modal-body">
		<iframe width="480" height="298" src="https://www.youtube.com/embed/ir_nUv4maL4" frameborder="0" allowfullscreen></iframe>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>

<div class="modal fade" id="streamsAndExcel" tabindex="-1" role="dialog" aria-labelledby="streams-and-excel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="streams-and-excel">Streams and Excel</h4>
      </div>
      <div class="modal-body">
		<iframe width="480" height="298" src="https://www.youtube.com/embed/8hzMXFBw7ns" frameborder="0" allowfullscreen></iframe>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>

<div class="modal fade" id="streamsConsole" tabindex="-1" role="dialog" aria-labelledby="streams-console" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="streams-console">Streams Console</h4>
      </div>
      <div class="modal-body">
		<video controls width="480" height="298" src="https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/11/streams.mp4" frameborder="0" allowfullscreen></video>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>
