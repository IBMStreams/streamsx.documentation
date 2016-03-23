---
layout: docs
title: Getting started with Kafka operators
description:  Getting Started Guide for IBM Streams Messaging Toolkit - Kafka operators
weight: 10
published: false
---

# Messaging Toolkit - Getting started with Kafka operators

## Introduction
The IBM Streams Messaging Toolkit is designed to get you connected to your messaging servers as quickly as possible. Kafka is an ideal messaging server for stream computing. This guide will get you sending and receiving messages in no time, and will highlight some of the best practices. 

## Skill Level
Readers of this guide are expected to have a basic understanding of Kafka and IBM Streams terminology. To get up to speed on Kafka basics, run through their great <a target="_blank" href="http://kafka.apache.org/documentation.html#quickstart">Quick Start guide</a>. To get a basic understanding of IBM Streams, you can read our <a target="_blank" href="https://developer.ibm.com/streamsdev/docs/streams-quick-start-guide/">Quick Start</a>.

## Requirements
Prior to using Kafka operators, the following software must be installed and configured:

* **IBM Streams** - A <a target="_blank" href="http://ibmstreams.github.io/streamsx.documentation//docs/4.1/qse-install-vm/">Quick Start Edition VM</a> is available for free. This guide assumes that you have a Streams domain and instance up and running. 
* **Messaging Toolkit** - An official version of the toolkit is shipped with Streams or you can download it from the IBM Streams Github Messaging Toolkit Repository <a target="_blank" href="https://github.com/IBMStreams/streamsx.messaging/releases">Release Page</a>.
* **Kafka servers** - This guide will assume you are using Kafka 0.9 or above. To quickly get a Kafka server up and running, follow <a target="_blank" href="http://kafka.apache.org/documentation.html#quickstart">this guide</a>. If you are using Kafka 0.8 servers, make sure that you download a version of the messaging toolkit that supports Kafka 0.8 (product versions of the Kafka operators up through Streams 4.1 support Kafka 0.8). 

[Sam:  The last part about version is confusing.  Can we make this a bit clear?  Perhaps we should say, for 0.8, use these toolkits, for 0.9, use another set of toolkit?]

## Information to Collect
Once you have your Kafka server (or servers) set up, you will need their hostnames and listener ports. You can find them in your configuration file for each server (default is server.properties): 

~~~~~~
# The port the socket server listens on
port=9092

# Hostname the broker will bind to. If not set, the server will bind to all interfaces
host.name=f0701b01.pok.hpc-ng.ibm.com
~~~~~~

## Steps
2. Configure the SPL compiler to find the messaging toolkit directory. Use one of the following methods.
   * *Set the STREAMS_SPLPATH environment variable to the root directory of a toolkit or multiple toolkits (with : as a separator)*

     `echo "export STREAMS_SPLPATH=$STREAMS_INSTALL/toolkits/com.ibm.streamsx.messaging" >> /home/streamsadmin/.bashrc`

   * *Specify the -t or --spl-path command parameter when you run the sc command.*

     `sc -t $STREAMS_INSTALL/toolkits/com.ibm.streamsx.messaging -M MyMain`

   * *If  Streams Studio is used to compile and run SPL application, add messaging toolkit to toolkit locations in Streams Explorer.*
2. Create an SPL application and add the Kafka operator use directives to it. If Streams Studio is used, this directive is automatically added when dragging and dropping a Kafka operator to SPL application (you can also just start with the <a target="_blank" href="https://github.com/IBMStreams/streamsx.messaging/tree/master/samples/KafkaSample">KafkaSample</a> to skip this and the following step). 

	`use com.ibm.streamsx.messaging.kafka::*;`
	
	or
	
	`use com.ibm.streamsx.messaging.kafka::KafkaProducer;`
	
	`use com.ibm.streamsx.messaging.kafka::KafkaConsumer;`
4. Add a toolkit dependency on the Messaging toolkit in your application. You can do this by editing the application dependency in Streams Studio, or by editing the info.xml for the application (if you start with an sample from the messaging toolkit, this step is already done for you). 
5. The Kafka Producer and Kafka Consumer require that either the propertiesFile parameter or the KafkaProperty parameter are set. The KafkaConsumer operator also requires that the topic parameter be specified, while the KafkaProducer can either get the topic as a parameter or an incoming attribute. 
Here is the sample beacon and KafkaProducer code from the <a target="_blank" href="https://github.com/IBMStreams/streamsx.messaging/tree/master/samples/KafkaSample">KafkaSample</a>:

	<pre><code>//create some messages and send to KafkaProducer
    stream&lt;rstring topic, rstring key, rstring message&gt; OutputStream = Beacon() {
        param
            initDelay : 5.0;
            period : 0.2;
        output OutputStream: topic = $topic, message = &quot;Reality is merely an illusion, albeit a very persistent one.&quot; 
        					, key = &quot;Einstein&quot;;
    }


    () as KafkaSinkOp = KafkaProducer(OutputStream) {
        param
            propertiesFile : &quot;etc/producer.properties&quot;;
    }
	</code></pre>
	The producer.properties file will be placed in the `etc` directory of the application. This ensures that it will be included in the .sab application bundle (important for cloud and HA deployment). You can also specify an absolute or relative file path, where the path is relative to the application directory. The following is a sample producer.properties file. bootstrap.servers refers to Kafka brokers (the host and port information you gathered at the start of this guide).      
	<pre><code>bootstrap.servers=broker.host.1:9092,broker.host.2:9092,broker.host.3:9092
acks=0</code></pre>
	Notice that we don't specify the topic as a parameter, it is part of the incoming tuple. This means that each incoming tuple could be directed towards a different topic. The key is an optional attribute that will be null if you don't set it. 

	Here is the KafkaConsumer operator from the <a target="_blank" href="https://github.com/IBMStreams/streamsx.messaging/tree/master/samples/KafkaSample">KafkaSample</a>: 

	<pre class="source-code"><code>stream&lt;rstring key, rstring message&gt; KafkaStream = KafkaConsumer()
    {
        param
            propertiesFile : &quot;etc/consumer.properties&quot;;
            topic : $topic;
    }</code></pre>
	The standard consumer.properties file will be placed in the etc directory of the application and look like this:
	<pre><code>bootstrap.servers=broker.host.1:9092,broker.host.2:9092,broker.host.3:9092
group.id=mygroup</code></pre>

   <div class="alert alert-success" role="alert"><b>Tip: </b>Not seeing any messages coming into your consumer? You may have stray consumers in the same consumer group reading from your topic. Try adding this as a KafkaProperty parameter:<br>
&nbsp;&nbsp;&nbsp;&nbsp;<b>kafkaProperty : "group.id=" +(rstring) getTimestampInSecs() ;</b></div>

##Consistent Region
Kafka operators support consistent regions. The KafkaConsumer can be the start of a consistent region and supports exactly-once tuple processing. The KafkaProducer can participate in a consistent region (it cannot be the start), and can guarantee at-least-once tuple processing. For general questions on consistent region, read this <a target="_blank" href="https://developer.ibm.com/streamsdev/2015/02/20/processing-tuples-least-infosphere-streams-consistent-regions/">overview</a> and these <a target="_blank" href="https://www-01.ibm.com/support/knowledgecenter/SSCRJU_4.1.0/com.ibm.streams.dev.doc/doc/consistentregions.html">docs</a>. 
To use the KafkaProducer operator in a consistent region, you can simply use it as you normally would (no special configuration is necessary). 
Since the KafkaConsumer will start any consistent region that it is a part of, it will have the `@consistent` annotation and you must specify the topic partitions that you want to consume from. 
Here is the KafkaConsumer from the <a target="_blank" href="https://github.com/IBMStreams/streamsx.messaging/tree/master/samples/KafkaConsistentRegionConsumerSimple">KafkaConsistentRegionConsumerSimple</a> sample:
<pre class="source-code"><code>    //Read in from a kafka server and start consistent region
    @consistent(trigger = operatorDriven) stream&lt;rstring message, rstring key&gt;
    KafkaConsumerOut = KafkaConsumer()
    {
        param
            propertiesFile : &quot;etc/consumer.properties&quot; ;
            topic : $topic ;
            partition : 0 ;
            triggerCount : 20 ;
    }
</code></pre>

Key points to notice: 

* **Must specify the partition parameter**  - This example is for a single-partition topic, but for a three-partition topic you can simple specify: `partition: 0,1,2;`
* **Specify triggerCount parameter for operatorDriven trigger**  - The trigger count gives the approximate number of messages between checkpointing. If you are using a periodic trigger for your consistent region, you do not need to specify this. 

##Parallel Consuming
Consuming in parallel lets you take advantage of the scalability of both Kafka and Streams. For a multi-partition topic, you can have as many consumers as you have partitions (if you have more consumers than partitions, they will just sit idly). 

<div class="alert alert-danger" role="alert"><b>Warning: </b>Do not rely on Kafka consumer rebalancing to consume in parallel. We have experienced many issues with failed rebalancing, and there is no way to know ahead of time which partitions each consumer will be reading from.</div>
 
<div class="alert alert-info" role="alert"><b>Best Practice: </b>To consume in parallel, specify the partition parameter. You can specify one or more partitions per operator. Partition numbers start at 0, so a 3-partition topic will have partitions 0, 1, and 2.</div>

Here is a simple example of using three consumers to read from a 3-partition topic using <a href="https://www-01.ibm.com/support/knowledgecenter/SSCRJU_4.1.0/com.ibm.streams.dev.doc/doc/udpoverview.html" target="_blank">User Defined Parallelism</a> (from the <a target="_blank" href="https://github.com/IBMStreams/streamsx.messaging/blob/master/samples/KafkaParallelConsumers/application/KafkaParallelConsumers.spl">KafkaParallelConsumers sample</a>):

<pre class="source-code"><code>    @parallel(width = 3)
    stream&lt;rstring message, rstring key&gt; KafkaConsumerOut = KafkaConsumer()
    {
        param
            propertiesFile : &quot;etc/consumer.properties&quot; ;
            topic : $topic ;
            partition : getChannel() ;
    }
</code></pre>

If you would like to consume in parallel within a consistent region, check out this <a target="_blank" href="https://github.com/IBMStreams/streamsx.messaging/tree/master/samples/KafkaConsistentRegionConsumerParallel">KafkaConsistentRegionConsumerParallel sample</a>.

##Advanced Parallel Processing
**This section is under construction**

## Additional Resources
* [IBM MQ Knowledge Center](http://www-01.ibm.com/support/knowledgecenter/SSFKSJ_8.0.0/com.ibm.mq.helphome.v80.doc/WelcomePagev8r0.htm)
* [ActiveMQ website](http://activemq.apache.org/)
* [ Streams Messaging Toolkit SPLDoc](http://ibmstreams.github.io/streamsx.messaging/com.ibm.streamsx.messaging/doc/spldoc/html/index.html)
