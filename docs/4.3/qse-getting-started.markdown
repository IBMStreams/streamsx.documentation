---
layout: docs
title:  Getting started with IBM Streams v4.3 with Quick Start Edition
description:  Learn how to get started with IBM Streams Quick Start Edition
weight:  50
published: true

tag: 43qse
prev:
  file: qse-intro
  title:  Download Quick Start Edition

---
## Download and install
If you haven't already done so, download and install Streams Quick Start Edition. For instructions, see [Try IBM Streams v4.3 with Quick Start Edition](../qse-intro).

## Streams overview

For a quick overview about Streams and developing in Streams, see the following video:

<button class="btn btn-primary btn-md" data-toggle="modal" data-target="#learnStreams">
Video:  Learn Streams in 5 min!
</button>



**Developing applications in Java or Python**
In addition to Streams Processing Language (SPL) discussed in the following section, Streams applications can be created in Java and Python.
To get started with those languages, see these development guides:

* [Develop Streams Applications in Java](/streamsx.documentation/docs/java/java-appapi-devguide/)
* Develop Streams Applications in Python [latest](/streamsx.documentation/docs/python/1.6/python-appapi-devguide/)



## Getting started with SPL 
Run your first Streams application, "Hello, World!" using Streams Studio.

### Launch Streams Studio
**If you are using the Docker QSE:**
  * [Start a VNC session](http://localhost:4000/streamsx.documentation/docs/4.3/qse-install-docker/#vnc).

**If you are using the Native Streams installation:**
  * [Install Streams Studio](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.install.doc/doc/tinstall-studio-linux.html)
  * [Install and launch Streams Studio](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.install.doc/doc/tinstall-studio-linux.html)
  * [Download the sample application project](https://streams-github-samples.mybluemix.net/?get=Examples-for-beginners%2F001_hello_world_in_spl)

#### Import and run the applications
Watch this 2-minute walkthrough on importing and running your first Streams application.

*Note: this video does not have narration.*
<div class="modal-body"><iframe width="560" height="315" src="https://www.youtube.com/embed/EZm1yUpm-4M" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
</div>



### Developing for IBM Cloud Pak for Data
*Skip this section if you are not using IBM Cloud Pak for Data or Streams deployed in Kubernetes or Red Hat OpenShift.*


The concepts in this tutorial apply to developing for Streams v4.3. The video above showed launching an application to a local instance of Streams v4.3.

If your Streams instance is running in IBM Cloud Pak for Data or as a stand-alone deployment, the steps to launch the application are different. This is because you have Streams v5 or later.

To launch the application in Streams v5+:
- Compile the application as shown above
- Instead of launching it to the local instance, you need to submit the application manually using the Streams Console.

#### Submit the job using the Streams Console
1. You need to get the URL of the Streams Console for your Streams instance. 
   - **Find the URL for Streams add-on in IBM Cloud Pak for Data:**
     - From the navigation menu, click <strong>My instances</strong>.
     - Click the <strong>Provisioned Instances</strong> tab.
     - Find your Streams instance, and click **View details** from the context menu. Open the URL under **External console endpoint**.
       
   - **Find the URL for Streams stand-alone deployment:** [See the documentation](https://www.ibm.com/support/knowledgecenter/en/SSCRJU_5.2.0/com.ibm.streams.dev.doc/doc/find-dns-url.html#find-dns-url). Choose *finding the internal URL*  or *finding the external URL* depending on whether or not you will be accessing the Streams Console from within the Kubernetes cluster.


2. From the Streams Console, submit the job by clicking **Submit job**:
  <br/>
![submit job](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/11/streams-submit-job.png)

   * Browse to the location of the compiled application.  This will be a `.sab` file in the `output` folder of your project.

   * Set any parameters, and submit the application.


<h5>Streams Console Overview</h5>

The following animation shows some of the useful features of the Streams Console.

<img alt="app in streams console" src="/streamsx.documentation/images/python/view-in-console-python.gif" />


<br/><br/>
<h5>Viewing the application’s logs</h5>
See application logs by going to the <strong>Log Viewer</strong>, which is opened from the menu options on the left.
<img alt="Streams console main" src="/streamsx.documentation/images/atom/jpg/console-main.jpg" />
<br/>
Next, expand the application, select the operator whose logs you want to inspect,  and click <strong>Console Log</strong>. Click <strong>Reload</strong> if no data appears.

<img alt="app logs" src="/streamsx.documentation/images/atom/jpg/operator-log.jpg" />
<br/>


<h3> More about the Streams Console</h3>
<br/>
See this <a href="https://developer.ibm.com/streamsdev/docs/streams-console-overview/">article on Streamsdev for an overview of the Streams Console</a>.

You can follow the rest of the guides but keep these steps in mind for submitting applications for IBM Cloud Pak for Data.


### Developing applications by using Streams Processing Language (SPL)

Streams Processing Language is designed from the ground up for writing streaming applications.  To quickly get started, see the following resources:

* Start with the [Streams Quick Start Guide](https://developer.ibm.com/streamsdev/?p=5686)
* [Streams Hands-on Lab](https://developer.ibm.com/streamsdev/docs/streams-lab-introduction/)
* [SPL Examples for Beginners](/streamsx.documentation/samples/)
* [Search our samples catalog](https://ibmstreams.github.io/samples/)

Streams is shipped with comprehensive development tooling.

<img src="/streamsx.documentation/images/qse/streamsStudio.jpg" alt="Streams Studio" style="width: 60%;"/>

To learn about how to develop using Streams Studio (our drag-and-drop IDE):

* [Streams Studio Quick Start Guide](https://developer.ibm.com/streamsdev/docs/studio-quick-start/)

<!-- Launch video in modal dialog -->
<button class="btn btn-primary btn-md" data-toggle="modal" data-target="#streamsStudioInAction">
Video:  Streams Studio in Action!
</button>

### Writing Java Operators

If you have existing Java code, you can easily reuse your code by writing a Java operator or native Java functions.

* [Java Operator Development Guide](../../java/java-op-dev-guide/)

### SparkMLLib in Streams

To get started, follow this development guide:

* [SparkMLLib Getting Started Guide](https://developer.ibm.com/streamsdev/docs/getting-started-with-the-spark-mllib-toolkit/)

### Apache Edgent (aka Open Embedded Streams) Integration

Gather local, real-time analytics from equipment, vehicles, systems, appliances, devices and sensors of all kinds. To get started, check out the Apache Edgent website for more information and guides:

* [Apache Edgent Official Website](https://edgent.incubator.apache.org/)

## Getting started for the data engineer

As a data engineer, you are responsible for:

* Designing, building, and managing data and analytic systems to ensure they are secure, reliable, and scalable
* Making all data, including data in motion, available for analysis by other team members such as data scientists and developers
* Capturing data in motion and integrating it with data at rest
* Leveraging the newest technologies for stream computing

Below are some resources to help you get started.

### Integrating with Streams

Streams is shipped with many toolkits out of the box to enable integration with some of the most popular systems like HDFS, HBase, Kafka, Active MQ and more.  To learn about the set of toolkits that are shipped as part of the Streams product, refer to the [Product Toolkits Overview](https://developer.ibm.com/streamsdev/docs/product-toolkits-overview/).

[IBMStreams on Github](https://github.com/ibmstreams) provides a platform that enables Streams to rapidly deliver our support to emgerging technologies to you.  It is also a place for us to share sample applications and helpful utilities.  For a list of open-source projects hosted on Github, see: [IBM Streams Github Projects Overview](https://developer.ibm.com/streamsdev/docs/github-projects-overview/).

### Integration with IBM InfoSphere Data Governance Catalog

With IBM InfoSphere Data Governance Catalog integration, developers can easily discover the data and schema that are available for use.  By building data lineage with your Streams application, you can quickly see and control how data is consumed.
To get started, see the  [Streams Governance Quickstart Guide](../governance/governance-quickstart/).

### Cybersecurity Toolkit


The Cybersecurity Toolkit provides operators that are capable of analyzing network traffic and detecting suspicious behaviour. For more information about using the Cybersecurity Toolkit, see the [Cybersecurity Getting Started Guide](../cybersecurity/cybersecurity-getting-started/)

### Streams and SPSS

SPSS is analytic predictive software that enables you to build predictive models from your data.  Your application can perform real-time predictive scoring by running these predictive models using the SPSS operators.

To learn about Streams can integrate with SPSS:  [Streams and SPSS Lab](https://developer.ibm.com/streamsdev/docs/spss-analytics-toolkit-lab/).

### Streams domain management and administration

Streams Console is the web-based administration console for monitoring and managing your Streams domain. Create customized dashboards to monitor your Streams domain, instances and applications.

<img src="/streamsx.documentation/images/qse/Application-Dashboard-4.1.png" alt="Streams Console" style="width: 60%;"/>

To familiarize yourself with Streams Console, see this video:

<button class="btn btn-primary btn-md" data-toggle="modal" data-target="#streamsConsole">
Video:  Streams Console
</button>

## Getting started for the business user

As a business user, you need to:

* Identify patterns, trends, risks and opportunities in data
* Build predictive analytic models
* Use visualization tools to explore and uncover high value data.

Below are some resources to help you get started.

### Streams and Microsoft Excel

<img src="/streamsx.documentation/images/qse/BargainIndex1.jpg" alt="Streams and Excel" style="width: 60%;"/>

IBM Streams integrates with Microsoft Excel, allowing you to see, analyze and visulize live streaming data in an Excel worksheet.  This article helps you get started:  [Streams for Microsoft Excel](https://developer.ibm.com/streamsdev/docs/streams-4-0-streams-for-microsoft-excel/)

In the following demo, we demonstrate how you may build a marketing dashboard from real-time data using Excel.

<button class="btn btn-primary btn-md" data-toggle="modal" data-target="#streamsAndExcel">
Video:  Streams and Excel Demo
</button>

### Operational Decision Manager (ODM)

IBM Streams integrates with ODM rules, allowing you to create business rules, construct rule flows, and create and deploy rules applications to analyze data and automate decisions in real-time.  This article helps you get started:  [ODM Toolkit Lab](https://developer.ibm.com/streamsdev/docs/rules-toolkit-lab/)



## Streams Community
The following Streams resources can help you connect with the Streams community and get support when you need it:

* **[Streamsdev](https://developer.ibm.com/streamsdev/)** - This resource is a developer-to-developer website maintained by the Streams Development Team.  It contains many useful articles and getting started material.  Check back often for new articles, tips and best practises to this website.
* **[Streams Tutorials Hub](http://ibmstreams.github.io/tutorials/)** A collection of available tutorials, labs and courses.
* **[Streams Forum](https://www.ibmdw.net/answers/questions/?community=streamsdev&sort=newest&refine=none)** - This forum enables you to ask, and get answers to your questions, related to IBM Streams. If you have questions, start here.
* **[IBMStreams on Github](http://ibmstreams.github.io)** - Streams is shipped with many useful toolkits out of the box.  IBMStreams on Github  contains many open-source toolkits.  For a list of available toolkits available on Github, see this web page:  [IBMStreams Github Toolkits](https://developer.ibm.com/streamsdev/docs/github-projects-overview/).
* **[IBM Streams Support](http://www.ibm.com/support/entry/portal/Overview/Software/Information_Management/InfoSphere_Streams)** - This website provides information about IBM Streams downloads, technical support tools, documentation, and other resources.
* **[IBM Streams Product Site](http://www.ibm.com/analytics/us/en/technology/stream-computing/)** - This website provides a broad range of information and resources about Streams and related topics.


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
