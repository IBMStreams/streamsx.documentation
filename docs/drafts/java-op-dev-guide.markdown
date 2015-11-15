---
layout: docs
title:  Java Operator Development Guide
description:  IBM Streams Java Operator Development Guide
published: true
---
#  Introduction 

Java is a deeply integrated part of Streams. Making Java easy in Streams has been a priority for years because of its extensive libraries and huge developer base. The goal of this guide is to take a two-tiered approach. Spots that are bolded and jump out at you are going to help you get your Java operators up and running as quickly and easily as possible. Streams Studio abstracts many details away from the developer, so we also go more into depth on how Java and Streams work together, rather than solely focusing on the easiest path. 

#  Java Operator Development Guide (Draft)
Page under construction

##  Operator Lifecycle
Unless you're writing an extremely simple Java operator, it's important to understand how the operator lifecycle works. All operators written in Java must implement the following interface and implement a no-argument constructor:

~~~~~~
     com.ibm.streams.operator.Operator   
     
     public interface Operator {
		public void initialize(OperatorContext context) throws Exception;
		public void allPortsReady() throws Exception;
		public void process(StreamingInput<Tuple> port, Tuple tuple) throws Exception;
		public void processPunctuation(StreamingInput<Tuple> port, Punctuation mark) throws Exception;
		public void shutdown() throws Exception;
	}      
~~~~~~


In general, you will extend AbstractOperator, which implements the Operator interface and takes default actions. You will then override the methods that need to be customized. 
Here is a brief explanation of the required methods:

**void initialize(OperatorContext context)** - This is called once before any tuples are processed and before any of the other required methods. Here is where you should put code to establish connections to external systems and data. You will have access to parameters supplied to the operator invocation in SPL. 

**void allPortsReady()** - This is called once after the initialize() method has returned and all input and output ports are connected and ready to receive/submit tuples. Operators that process incoming tuples generally won't use this, since the process method is used to handle tuples. In the case of a source operator, there are no incoming tuples so this is where the production threads are started. We will cover this more in the source operator section.

**void process(StreamingInput\<Tuple> port, Tuple tuple)** - This is where the manipulation of incoming tuples will take place, followed by submission to an output port or an external connection (in the case of a sink operator). The performance of your operator will be decided by how efficient your process method is. See the Developing a High Performance process() method section. 

**void processPunctuation(StreamingInput\<Tuple> port, Punctuation mark)** - Process  incoming punctuation markers that arrived on the specified port. The two types of punctuation to be handled are window and final. 

**void shutdown()** - Close connections and release resources related to any external system or data store. This method is invoked when a job is cancelled or an operator is stopped. 


