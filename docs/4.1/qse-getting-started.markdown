---
layout: docs
title:  Getting Started with Streams Quick Start Edition
weight:  10
---

# Getting Started with Streams Quick Start Edition

## Streams Overview

For a quick overview about Streams and developing in Streams, see the following video:

<button class="btn btn-primary btn-md" data-toggle="modal" data-target="#learnStreams">
Video:  Learn Streams in 5 min!
</button>

## Getting Started for the Developer

As a developer, you are trying to:

* Learn about Streams
* How to write your first Streams application
* How to work with the development tooling in Streams

Here are some resources to get you up and running!

### Streams and SPL

To quickly get started and learn about Streams:

* [Streams Quick Start Guide](https://developer.ibm.com/streamsdev/?p=5686)
* [Streams Hands-on Lab](https://developer.ibm.com/streamsdev/docs/introductory-lab-for-streams-4-0-1/)
* [SPL Examples for Beginners](https://developer.ibm.com/streamsdev/docs/spl-examples-beginners/)
    
Streams is shipped with comprehensive development tooling.  To learn about how to develop using Streams Studio (our IDE):

* [Streams Studio Quick Start Guide](https://developer.ibm.com/streamsdev/docs/studio-quick-start/)

<!-- Launch video in modal dialog -->
<button class="btn btn-primary btn-md" data-toggle="modal" data-target="#streamsStudioInAction">
Video:  Streams Studio in Action!
</button>

### Java and Scala

<div class="alert alert-success" role="alert"><b>New in Streams 4.1!</b>  You can now write your Streams application purely in Java or Scala</div>

To get started, follow this development guide:

* [Develop Streams Applications in Java or Scala](http://ibmstreams.github.io/streamsx.topology/)

### Writing Java Operator

If you have existing Java code, you may easily reuse your code by writing a Java operator or native Java functions.

* [Roadmap for Java Developers](https://developer.ibm.com/streamsdev/docs/roadmap-for-java-developer/)

### SparkMLLib in Streams

<div class="alert alert-success" role="alert"><b>New in Streams 4.1!</b>  You can now now reuse your SparkMLLib models and analytics in Streams.</div>

To get started, follow this development guide:

* [SparkMLLib Getting Started Guide](http://ibmstreams.github.io/streamsx.sparkMLLib/gettingstarted.html)
    
## Getting Started for the Data Engineer

As a Data Engineer, you are responsible to:

* Design, build and manage data management and analytic systems that are secure, reliable, and scalable
* Make all data including in motion available for analysis by other team members such as the data scientists and developers
* Capture data in motion and integrate it with data at rest
* Need to leverage the newest technologies for stream computing

Here are some resources to help you get started.

### Integrating with Streams

Streams is shipped with many toolkits out of the box to help you integrate with some of the most popular systems like HDFS, HBase, Kafka, Active MQ and more.  To learn about the set of toolkits that are shipped as part of the Streams product:  [Product Toolkits Overview](https://developer.ibm.com/streamsdev/docs/product-toolkits-overview/)

[IBMStreams on Github](https://github.com/ibmstreams) provides a platform for us to rapidly deliver support to the emgerging technologies.  It is also a place for us to share sample applications and helpful utilities.  For a list of open-source projects hosted on Github:  [IBM Streams Github Projects Overview](https://developer.ibm.com/streamsdev/docs/github-projects-overview/)

### Integration with IBM InfoSphere Data Governance Catalog
<div class="alert alert-success" role="alert"><b>New in Streams 4.1!</b>  The IBM InfoSphere Data Governance Catalog can help you manage and govern your data.</div>

With this support, developers can easily discover the data and schema that are available to use.  By building data lineage with your Streams application, you can quickly see and control how data is consumed.
To get started:  [Streams Governance Quickstart Guide](governance-quickstart)

### Streams and SPSS

SPSS is an analytic predictive software for you to build predictive model from your data.  Your application may perform real-time predictive scoring by running these predictive models using the SPSS operators.

To learn about how Streams can integrate with SPSS:  [Streams and SPSS Lab](https://developer.ibm.com/streamsdev/docs/spss-analytics-toolkit-lab/).

### Stream Domain Management and Administration

Streams Console is the web-based administration console to help you monitor and manage your Streams domain. To familiarize yourself with the Streams Console, see this video:

<button class="btn btn-primary btn-md" data-toggle="modal" data-target="#streamsConsole">
Video:  Streams Console Navigation
</button>

<div class="alert alert-success" role="alert"><b>New in Streams 4.1! </b>Customizable Dashboard in Streams Console</div>

Prior to Streams 4.1, the Streams Console dashboard contains a fixed set of widgets.  In the latest release, you can now create customized dashboards to monitor your Streams domain, instances and applications


## Getting Started for the Business User

As a business user, you need to:

* Identify patterns, trends, risks and opportunities in data
* Build predictive analytic models
* Use visualization tools to explore and uncover high value data.

Here are some resources to help you get started.

### Streams and Microsoft Excel

IBM Stremas integrates with Microsoft Excel, allowing you to see, analyze and visulize live streaming data in an Excel worksheet.  This article helps you get started:  [Streams for Microsoft Excel](https://developer.ibm.com/streamsdev/docs/streams-4-0-streams-for-microsoft-excel/)

In the following demo, we demonstrate how you may build a marketing dashboard from real-time data using Excel.

<button class="btn btn-primary btn-md" data-toggle="modal" data-target="#streamsAndExcel">
Video:  Streams and Excel Demo
</button>

## Streams Community
The following Streams resources can help you connect with the Streams community and get support when you need it:

* **[StreamsDev](https://developer.ibm.com/streamsdev/)** - This resource is a developer-to-developer website maintained by the Streams Development Team.  It contains many useful articles and getting started material.  Check back often for new articles, tips and tricks to this website.
* **[Streams Forum](https://www.ibmdw.net/answers/questions/?community=streamsdev&sort=newest&refine=none)** - This forum enables you to ask and answer questions that relate to InfoSphere Streams. If you have questions, start here.
* **[IBMStreams on Github](http://ibmstreams.github.io)** - Streams is shipped with many useful toolkits out of the box.  IBMStreams on Github  contains many open-source toolkits.  For a list of available toolkits available on Github, see this web page:  [IBMStreams Github Toolkits](https://developer.ibm.com/streamsdev/docs/github-projects-overview/).
* **[IBM Streams Support](http://www.ibm.com/support/entry/portal/Overview/Software/Information_Management/InfoSphere_Streams)** - This website provides information about InfoSphere Streams downloads, technical support tools, documentation, and other resources.
* **[IBM Streams Product Site](http://www.ibm.com/software/data/infosphere/streams)** - This website provides a broad range of information and resources about Streams and related topics.


<!-- Modal -->
<div class="modal fade" id="learnStreams" tabindex="-1" role="dialog" aria-labelledby="learn-streams-in-5-min" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="learn-streams-in-5-min">Learn Streams in 5 Min</h4>
      </div>
      <div class="modal-body">
        <iframe width="480" height="298" src="https://www.youtube.com/embed/HLHGRy7Hif4" frameborder="0" allowfullscreen></iframe>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>

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
		<iframe width="480" height="298" src="https://www.youtube.com/watch?v=8hzMXFBw7ns" frameborder="0" allowfullscreen></iframe>
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
        <h4 class="modal-title" id="streams-console">Streams Console Navigation</h4>
      </div>
      <div class="modal-body">
		<iframe width="480" height="298" src="https://www.youtube.com/embed/wkt5k9TCaiw" frameborder="0" allowfullscreen></iframe>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>
