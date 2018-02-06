---
layout: docs
title:  Getting Started with IBM Streams v4.2 Quick Start Edition
description:  Learn how to get started witH IBM Streams Quick Start Edition
weight:  50
published: true

tag: 42qse
prev:
  file: qse-intro
  title:  Download the Quick Start Edition (QSE)

---
## Download and Install
If you haven't downloaded and installed the Streams QSE, the [preceding section](../qse-intro) has instructions.

## Streams Overview

For a quick overview about Streams and developing in Streams, see the following video:

<button class="btn btn-primary btn-md" data-toggle="modal" data-target="#learnStreams">
Video:  Learn Streams in 5 min!
</button>

## Getting Started for the Developer

As a developer, you want to:

* Learn about Streams
* Write your first Streams application
* Work with the development tooling in Streams

Below are some resources to get you up and running!

### Developing applications in Java, Scala or Python
In addition to Streams Processing Language (SPL, discussed below), Streams applications can be created in Java, Scala, and Python.

Example Streams Application:

<ul class="nav nav-tabs">


  <li class="active" ><a data-toggle="tab" href="#java-0">Java</a></li>  
  <li ><a data-toggle="tab" href="#scala-0">Scala</a></li>
  <li><a data-toggle="tab" href="#python-0">Python</a></li>
</ul>

<div class="tab-content">

    <div id="java-0" class="tab-pane fade in active">
  <pre><code>package simple;

  import com.ibm.streamsx.topology.TStream;
  import com.ibm.streamsx.topology.Topology;
  import com.ibm.streamsx.topology.context.StreamsContextFactory;

  public static void main(String[] args) throws Exception {

          /*
           * Create the container for the topology that will
           * hold the streams of tuples.
           */
          Topology topology = new Topology(&quot;HelloWorld&quot;);

          /*
           * Declare a source stream (hw) with String tuples containing two tuples,
           * &quot;Hello&quot; and &quot;World!&quot;.
           */
          TStream&lt;String&gt; hw = topology.strings(&quot;Hello&quot;, &quot;World!&quot;);

          /*
           * Sink hw by printing each of its tuples to System.out.
           */
          hw.print();

          /*
           * At this point the topology is declared with a single
           * stream that is printed to System.out.
           */

          /*
           * Now execute the topology by submitting to a StreamsContext.
           * If no argument is provided then the topology is executed
           * within this JVM (StreamsContext.Type.EMBEDDED).
           * Otherwise the first and only argument is taken as the
           * String representation of the desired context
           */
          if (args.length == 0)
              StreamsContextFactory.getEmbedded().submit(topology).get();
          else
              StreamsContextFactory.getStreamsContext(args[0]).submit(topology)
                  .get();
      }
  </code></pre>   
    </div>


    <div id="scala-0" class="tab-pane fade">
    <pre><code>package simple

    import com.ibm.streamsx.topology.Topology
    import com.ibm.streamsx.topology.streams.BeaconStreams
    import com.ibm.streamsx.topology.context.StreamsContextFactory

    import java.util.concurrent.TimeUnit

    import com.ibm.streamsx.topology.functions.FunctionConversions._

    object HelloWorldScala {
      def main(args: Array[String]) {
        val topology = new Topology(&quot;HelloWorldScala&quot;)

        var hw = topology.strings(&quot;Hello&quot;, &quot;World!&quot;)    
        hw.print()

       StreamsContextFactory.getStreamsContext(&quot;EMBEDDED&quot;).submit(topology).get()
      }
    }
    </code></pre>
      </div>
  <div id="python-0" class="tab-pane fade">
  <pre><code>import sys
from streamsx.topology.topology import Topology
import streamsx.topology.context
import hello_world_functions


def main():
    """
    Sample Hello World topology application. This Python application builds a
    simple topology that prints Hello World to standard output.

    The application implements the typical pattern
    of code that declares a topology followed by
    submission of the topology to a Streams context.

    This demonstrates the mechanics of declaring a topology and executing it.

    Example:
        python3 hello_world.py
    Output:
        Hello
        World!
    """

    # Create the container for the topology that will hold the streams of tuples.
    topo = Topology("hello_world")

    # Declare a source stream (hw) with string tuples containing two tuples,
    # "Hello" and "World!".
    hw = topo.source(hello_world_functions.source_tuples)

    # Sink hw by printing each of its tuples to standard output
    hw.print()

    # At this point the topology is declared with a single
    # stream that is printed to standard output

    # Now execute the topology by submitting to a standalone context.
    streamsx.topology.context.submit("STANDALONE", topo.graph)


if __name__ == '__main__':
    main()
</code></pre>
<pre><code>def source_tuples():
    """
    Returns an iterable of strings
    """
    return ["Hello", "World!"]
</code></pre>
  </div>
</div>

To get started, follow these development guides:

* [Develop Streams Applications in Java](http://ibmstreams.github.io/streamsx.documentation/docs/java/java-appapi-devguide/)
* [Develop Streams Applications in Scala](https://github.com/IBMStreams/streamsx.topology/wiki/Scala-Support)
* Develop Streams Applications in Python [v1.6](http://ibmstreams.github.io/streamsx.documentation/docs/python/1.6/python-appapi-devguide/) , [v1.4](http://ibmstreams.github.io/streamsx.documentation/docs/python/1.4/python-appapi-devguide/)


### Developing applications using Streams Processing Language (SPL)

The Streams Processing Language is designed from the ground up for writing streaming applications.  To quickly get started:

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

If you have existing Java code, you may easily reuse your code by writing a Java operator or native Java functions.

* [Java Operator Development Guide](../../java/java-op-dev-guide/)

### SparkMLLib in Streams

To get started, follow this development guide:

* [SparkMLLib Getting Started Guide](https://developer.ibm.com/streamsdev/docs/getting-started-with-the-spark-mllib-toolkit/)

### Apache Edgent (aka Open Embedded Streams) Integration

<div class="alert alert-success" role="alert"><b>New in Streams 4.2!</b>  Streams now supports integration with Apache Edgent.</div>

Gather local, real-time analytics from equipment, vehicles, systems, appliances, devices and sensors of all kinds. To get started, check out the Apache Edgent website for more information and guides:

* [Apache Edgent Official Website](https://edgent.incubator.apache.org/)

## Getting Started for the Data Engineer

As a Data Engineer, you are responsible for:

* Designing, building, and managing data and analytic systems to ensure they are secure, reliable, and scalable
* Making all data, including data in motion, available for analysis by other team members such as data scientists and developers
* Capturing data in motion and integrating it with data at rest
* Leveraging the newest technologies for stream computing

Below are some resources to help you get started.

### Integrating with Streams

Streams is shipped with many toolkits out of the box to enable integration with some of the most popular systems like HDFS, HBase, Kafka, Active MQ and more.  To learn about the set of toolkits that are shipped as part of the Streams product, refer to the [Product Toolkits Overview](https://developer.ibm.com/streamsdev/docs/product-toolkits-overview/)

[IBMStreams on Github](https://github.com/ibmstreams) provides a platform enabling Streams to rapidly deliver our support to emgerging technologies to you.  It is also a place for us to share sample applications and helpful utilities.  For a list of open-source projects hosted on Github, see: [IBM Streams Github Projects Overview](https://developer.ibm.com/streamsdev/docs/github-projects-overview/)

### Integration with IBM InfoSphere Data Governance Catalog

With this support, developers can easily discover the data and schema that are available for use.  By building data lineage with your Streams application, you can quickly see and control how data is consumed.
To get started, refer to  [Streams Governance Quickstart Guide](../governance/governance-quickstart/)

### Cybersecurity Toolkit


The Cybersecurity Toolkit provides operators that are capable of analyzing network traffic and detecting suspicious behaviour. For more information on using the Cybersecurity Toolkit, refer to [Cybersecurity Getting Started Guide](../cybersecurity/cybersecurity-getting-started/)

### Streams and SPSS

SPSS is analytic predictive software enabling you to build predictive model from your data.  Your application may perform real-time predictive scoring by running these predictive models using the SPSS operators.

To learn about Streams can integrate with SPSS:  [Streams and SPSS Lab](https://developer.ibm.com/streamsdev/docs/spss-analytics-toolkit-lab/).

### Streams Domain Management and Administration

Streams Console is the web-based administration console for monitoring and managing your Streams domain. Create customized dashboards to monitor your Streams domain, instances and applications.

<img src="/streamsx.documentation/images/qse/Application-Dashboard-4.1.png" alt="Streams Console" style="width: 60%;"/>

To familiarize yourself with the Streams Console, see this video:

<button class="btn btn-primary btn-md" data-toggle="modal" data-target="#streamsConsole">
Video:  Streams Console
</button>

## Getting Started for the Business User

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

<div class="alert alert-success" role="alert"><b>New in Streams 4.2!</b>  Streams now supports integration with ODM rules.</div>

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
