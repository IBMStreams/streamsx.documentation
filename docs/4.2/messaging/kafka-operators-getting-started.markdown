---
layout: docs
title: Getting Started with Kafka Operators (Deprecated) 
description:  Getting Started Guide for IBM Streams Messaging Toolkit - Kafka operators
weight: 10
published: true
---


<div class="alert alert-danger" role="alert">
 <b>Update:</b> The new <a href="https://github.com/IBMStreams/streamsx.kafka">streamsx.kafka</a> toolkit is the recommended way to connect to Kafka from IBM Streams. As of version 5.3.2 of the messaging toolkit, the Kafka support has been deprecated. Read the <a href="https://developer.ibm.com/streamsdev/docs/introducing-kafka-toolkit/">announcement on Streamsdev</a> to learn more about the Kafka toolkit.
</div>



## Introduction
The IBM Streams Messaging Toolkit is designed to get you connected to your messaging servers as quickly as possible. Kafka is an ideal messaging server for stream computing. This guide will get you sending and receiving messages in no time, and will highlight some of the best practices. We will also cover how to get the Kafka operators running in a consistent region.



## Skill Level
Readers of this guide are expected to have a basic understanding of Kafka and IBM Streams terminology. To get up to speed on Kafka basics, run through their great <a target="_blank" href="http://kafka.apache.org/documentation.html#quickstart">Quick Start guide</a>. To get a basic understanding of IBM Streams, you can read our <a target="_blank" href="https://developer.ibm.com/streamsdev/docs/streams-quick-start-guide/">Quick Start</a>.

## Requirements
Prior to using Kafka operators, the following software must be installed and configured:

* **IBM Streams** - A <a target="_blank" href="http://ibmstreams.github.io/streamsx.documentation//docs/4.2/qse-install-vm/">Quick Start Edition VM</a> is available for free. This guide assumes that you have a Streams domain and instance up and running.
* **Messaging Toolkit 4.0+** - You can download it from the IBM Streams Github Messaging Toolkit Repository <a target="_blank" href="https://github.com/IBMStreams/streamsx.messaging/releases">Release Page</a>.
* **Kafka Brokers** - This guide assumes you are using Kafka 0.9 or above. To quickly get a Kafka server up and running, follow <a target="_blank" href="http://kafka.apache.org/documentation.html#quickstart">these directions</a>.

## Information to Collect
Once you have your Kafka server (or servers) set up, you will need their hostnames and listener ports. You can find them in your configuration file for each server (default is `<Kafka-Install>/config/server.properties`):

~~~~~~
# The port the socket server listens on
port=9092

# Hostname the broker will bind to. If not set, the server will bind to all interfaces
host.name=myhost.mycompany.com
~~~~~~

## Steps - Send and Receive Messages
2. **Configure the SPL compiler to find the messaging toolkit directory. Use one of the following methods.**
   * *Set the STREAMS_SPLPATH environment variable to the root directory of the toolkit (with : as a separator)*

        `export STREAMS_SPLPATH=\<messaging-toolkit-location\>/com.ibm.streamsx.messaging:$STREAMS_SPLPATH`

   * *Specify the -t or --spl-path command parameter when you run the sc command.*

     `sc -t $STREAMS_INSTALL/toolkits/com.ibm.streamsx.messaging -M MyMain`

   * *If  Streams Studio is used to compile and run SPL application, add messaging toolkit to toolkit locations in Streams Explorer by following [these directions](http://www.ibm.com/support/knowledgecenter/SSCRJU_4.2.0/com.ibm.streams.studio.doc/doc/tusing-working-with-toolkits-adding-toolkit-locations.html?lang=en).*

2. **Create an SPL application and add a toolkit dependency on the Messaging toolkit in your application.** You can do this by [editing the application dependency](http://www.ibm.com/support/knowledgecenter/SSCRJU_4.2.0/com.ibm.streams.studio.doc/doc/tcreating-spl-toolkit-app-elements-edit-toolkit-information-dependencies.html) in Streams Studio, or by creating/editing the info.xml for the application and adding the dependency directly (you can also just start with the <a target="_blank" href="https://github.com/IBMStreams/streamsx.messaging/tree/master/samples/KafkaSample">KafkaSample</a> to skip this and the following step).

    Sample info.xml from the <a target="_blank" href="https://github.com/IBMStreams/streamsx.messaging/tree/master/samples/KafkaSample">KafkaSample</a>:

   <pre><code>&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;
&lt;info:toolkitInfoModel xmlns:common=&quot;http://www.ibm.com/xmlns/prod/streams/spl/common&quot; xmlns:info=&quot;http://www.ibm.com/xmlns/prod/streams/spl/toolkitInfo&quot;&gt;
  &lt;info:identity&gt;
    &lt;info:name&gt;KafkaSample&lt;/info:name&gt;
    &lt;info:description&gt;Sample application showing a Streams Kafka Producer and Consumer&lt;/info:description&gt;
    &lt;info:version&gt;1.0.0&lt;/info:version&gt;
    &lt;info:requiredProductVersion&gt;4.0.0.0&lt;/info:requiredProductVersion&gt;
  &lt;/info:identity&gt;
  <b style="color:blue">&lt;info:dependencies&gt;
        &lt;info:toolkit&gt;
          &lt;common:name&gt;com.ibm.streamsx.messaging&lt;/common:name&gt;
          &lt;common:version&gt;[3.0.0,6.0.0)&lt;/common:version&gt;
        &lt;/info:toolkit&gt;
  &lt;/info:dependencies&gt;</b>
&lt;/info:toolkitInfoModel&gt;
</code></pre>

3. **Add the Kafka operator use directives to your application.** If Streams Studio is used, this directive is automatically added when dragging and dropping a Kafka operator onto SPL application in the graphical editor (if you start with a sample from the messaging toolkit, this step is already done for you).  

	`use com.ibm.streamsx.messaging.kafka::*;`

	or

	`use com.ibm.streamsx.messaging.kafka::KafkaProducer;`

	`use com.ibm.streamsx.messaging.kafka::KafkaConsumer;`

5. **Configure the Kafka Producer to send messages to a Kafka Broker.** You must:
    * **Create a producer.properties file and place it in the `etc` directory of your application.** This ensures that it will be included in the .sab application bundle (important for cloud and HA deployment). The following is a sample producer.properties file. See <a target="_blank" href="http://kafka.apache.org/documentation.html#producerconfigs">here</a> for more producer configuration details.
        <pre><code>bootstrap.servers=broker.host.1:9092,broker.host.2:9092,broker.host.3:9092
   acks=0</code></pre>
    * **Specify the location of the producer.properties file in the KafkaProducer operator using the propertiesFile parameter.** You can specify either an absolute or a relative file path, where the path is relative to the application directory:

        `propertiesFile : etc/producer.properties`
    * **Specify the Kafka topic to send messages to.** This can be done via the rstring topic attribute in the incoming tuple or you can specify this using the topic parameter in the KafkaProducer (see the highlighted code in the beacon operator below).


    Here is the sample beacon and KafkaProducer code from the <a target="_blank" href="https://github.com/IBMStreams/streamsx.messaging/tree/master/samples/KafkaSample">KafkaSample</a>:

    <pre><code>//create some messages and send to KafkaProducer
    stream&lt;<b style="color:blue">rstring topic, rstring key, rstring message</b>&gt; OutputStream = Beacon() {
        param
            initDelay : 5.0;
            period : 0.2;
        output
            OutputStream: <b style="color:blue">topic = $topic
                        , message = &quot;Reality is merely an illusion, albeit a very persistent one.&quot;
                        , key = &quot;Einstein&quot;</b>;
    }


    () as KafkaSinkOp = KafkaProducer(OutputStream) {
        param
            <b style="color:blue">propertiesFile : &quot;etc/producer.properties&quot;</b>;
    }
    </code></pre>




    <div class="alert alert-success" role="alert"><b>Notice: </b>We don't specify the topic as a parameter, but instead as a part of the incoming tuple. This means that each incoming tuple can be directed towards a different topic.</div>

6. **Configure the Kafka Consumer to receive messages from the Kafka Broker.** You must:
    * **Create a consumer.properties file and place it in the `etc` directory of your application.** Here is a sample consumer.properties file (for more details on Kafka Consumer configs, see <a target="_blank" href="http://kafka.apache.org/documentation.html#newconsumerconfigs">here</a>:
        <pre><code>bootstrap.servers=broker.host.1:9092,broker.host.2:9092,broker.host.3:9092
group.id=mygroup</code></pre>
    * **Specify the location of the consumer.properties file in the KafkaConsumer operator using the propertiesFile parameter:**

        `propertiesFile : etc/consumer.properties`
    * **Specify the Kafka topic (or topics) to subscribe to receive messages from.** Do this using the rstring topic parameter in the KafkaConsumer. You can subscribe to multiple topics by using a comma separated list:

        `topic: "topic1" , "topic2" , "topic3";`

	Here is the KafkaConsumer operator from the <a target="_blank" href="https://github.com/IBMStreams/streamsx.messaging/tree/master/samples/KafkaSample">KafkaSample</a>:

	<pre class="source-code"><code>stream&lt;rstring key, rstring message&gt; KafkaStream = KafkaConsumer()
    {
        param
            <b style="color:blue">propertiesFile : &quot;etc/consumer.properties&quot;;
            topic : $topic;</b>
    }</code></pre>

   <div class="alert alert-success" role="alert"><b>Tip: </b>Not seeing any messages coming into your consumer? You may have stray consumers in the same consumer group reading from your topic. Try adding this as a KafkaProperty parameter:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<b>kafkaProperty : "group.id=" + (rstring) getTimestampInSecs() ;</b></div>

## Consistent Regions

Kafka operators support consistent regions, which are sections of your operator graph where tuple processing is guaranteed. The KafkaProducer can participate in a consistent region (it cannot be the start), and can guarantee at-least-once tuple processing. No special configuration is required to use the KafkaProducer in a consistent region, so this section will only focus on the KafkaConsumer.

The KafkaConsumer supports exactly-once tuple processing and starts a consistent region (since it is a source).
  For general questions on consistent region, read this <a target="_blank" href="https://developer.ibm.com/streamsdev/2015/02/20/processing-tuples-least-infosphere-streams-consistent-regions/">overview</a> and these <a target="_blank" href="https://www-01.ibm.com/support/knowledgecenter/SSCRJU_4.2.0/com.ibm.streams.dev.doc/doc/consistentregions.html">docs</a>.

To start a consistent region with a KafkaConsumer, you must:

* **Place an `@consistent` annotation above the operator**

* **Specify the partition parameter**  - The partition refers to the Kafka topic partition that we will maintain exactly-once processing for. This example is for a single-partition topic, but for a three-partition topic you can simple specify: `partition: 0,1,2;`
* **Specify triggerCount parameter for operatorDriven trigger** - The trigger count gives you control over the approximate number of messages between checkpointing. If you are using a periodic trigger for your consistent region, you do not need to specify this.
Here is the KafkaConsumer from the <a target="_blank" href="https://github.com/IBMStreams/streamsx.messaging/tree/master/samples/KafkaConsistentRegionConsumerSimple">KafkaConsistentRegionConsumerSimple</a> sample:
<pre class="source-code"><code>    //Read in from a kafka server and start consistent region
    <b style="color:blue">@consistent(trigger = operatorDriven)</b>
    stream&lt;rstring message, rstring key&gt; KafkaConsumerOut = KafkaConsumer()
    {
        param
            propertiesFile : &quot;etc/consumer.properties&quot; ;
            topic : $topic ;
            <b style="color:blue">partition : 0 ;
            triggerCount : 20 ;</b>
    }
</code></pre>


## Parallel Consuming
Consuming in parallel lets you take advantage of the scalability of both Kafka and Streams. For a multi-partition topic, you can have as many consumers as you have partitions (if you have more consumers than partitions, they will just sit idly).

<div class="alert alert-info" role="alert"><b>Best Practice: </b>To consume in parallel, specify the partition parameter. You can specify one or more partitions per operator. Partition numbers start at 0, so a 3-partition topic will have partitions 0, 1, and 2.</div>

The easiest way to consume from a single topic in parallel is to:

* **Use @parallel with a width equal to the number of partitions in your topic:**

    `@parallel(width = $numTopicPartitions)`

* **Use `getChannel()` as the partition parameter value.**

    `partition : getChannel();`

Here is a simple example of using three consumers to read from a 3-partition topic using <a href="https://www-01.ibm.com/support/knowledgecenter/SSCRJU_4.2.0/com.ibm.streams.dev.doc/doc/udpoverview.html" target="_blank">User Defined Parallelism</a> (from the <a target="_blank" href="https://github.com/IBMStreams/streamsx.messaging/blob/master/samples/KafkaParallelConsumers/application/KafkaParallelConsumers.spl">KafkaParallelConsumers sample</a>):

<pre class="source-code"><code>    <b style="color:blue">@parallel(width = 3)</b>
    stream&lt;rstring message, rstring key&gt; KafkaConsumerOut = KafkaConsumer()
    {
        param
            propertiesFile : &quot;etc/consumer.properties&quot; ;
            topic : $topic ;
            <b style="color:blue">partition : getChannel()</b> ;
    }
</code></pre>

If you would like to consume in parallel within a consistent region, check out this <a target="_blank" href="https://github.com/IBMStreams/streamsx.messaging/tree/master/samples/KafkaConsistentRegionConsumerParallel">KafkaConsistentRegionConsumerParallel sample</a>.

<div class="alert alert-danger" role="alert"><b>Warning: </b>Do not rely on Kafka consumer rebalancing to consume in parallel. We have experienced many issues with failed rebalancing, and there is no way to know ahead of time which partitions each consumer will be reading from.</div>

## Advanced Parallel Processing
**This section is under construction**

## Connecting to Message Hub in the Cloud
You can use the Streams Kafka operators to produce to and consume from the Kafka-based <a target="_blank" href="https://developer.ibm.com/messaging/message-hub/">Message Hub</a> Bluemix service. 


<div class="alert alert-success" role="alert">
<b>Update:</b> The simplest way to connect to Message Hub in the cloud is by using the streamsx.messagehub toolkit. For a complete guide on how to do this, check out <a href="https://www.ibm.com/blogs/bluemix/2018/04/get-started-streaming-analytics-message-hub/" target="_blank">this great article</a>.
</div>


## Additional Resources
* <a target="_blank" href="http://ibmstreams.github.io/streamsx.messaging/com.ibm.streamsx.messaging/doc/spldoc/html/index.html">Streams Messaging Toolkit SPLDoc</a>
* <a target="_blank" href="http://kafka.apache.org/documentation.html">Kafka Documentation website</a>
* <a target="_blank" href="https://github.com/IBMStreams/streamsx.messaging/blob/master/performance/KafkaPerformanceSummary.pdf">Kafka Streams Performance Summary</a>
