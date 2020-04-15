---
layout: docs
title:  Streams Quick Start Guide
description:  Get started with Streams using SPL
weight : 1
published: true
tag: 43qse
prev:
  file: qse-getting-started
  title: Getting started
---


The Streams Quick Start Guide is intended to help you get up and running with IBM Streams quickly. We will first introduce the basic concepts and building blocks. And then we will write a very simple Streams application, and demonstrate how you can run and monitor this application in the Streams distributed runtime environment.

*   [Overview](#overview)
*   [Basic Building Blocks](#basic_building_blocks)
*   [Simple Streams Application](#simple_streams_application)
*   [SPL Basics](#spl_basics)
*   [Streams Application Pattern](#streams_application_pattern)
*   [Building Streams Applications](#building_streams_applications)
*   [Streams Domain and Instance](#streams_domain_and_instance)
*   [Setting up a Development Domain and Instance](#setting_up_a_development_domain_and_instance)
*   [Running Streams Applications in Distributed Mode](#running_streams_applications_in_distributed_mode)
*   [Querying for Job Status](#querying_for_job_status)
*   [Sample Application Output](#sample_application_output)
*   [Streams Console](#streams_console)
*   [Streams Studio](#streams_studio)
*   [What's Next](#whats_next)

<a name="overview"></a>

## Overview

Streams is an advanced analytic platform that allows you to develop applications that analyze data in real-time. You can ingest, analyze and correlate information as it arrives from thousands of real-time sources. Here are some important Streams features:

This tutorial will cover the basics of creating a Streams application with SPL, Streams Processing Language.  You can also create Streams application with [Java](http://ibmstreams.github.io/streamsx.documentation/docs/4.1/java/java-appapi-devguide/) and [Python](http://ibmstreams.github.io/streamsx.documentation/docs/python/1.6/python-appapi-devguide/index.html).

<a name="basic_building_blocks"></a>

## Basic Building Blocks
To write a Streams application, you need to first understand the basic building blocks: operators, streams, and tuples, and how they work together.


•	Stream – A stream is an infinite sequence of records to be processed. 
o	
•	Tuple – A tuple represents individual records of the streaming data.  It is a structured list of attributes and their data types. 
o	Continuing the example above, in the stream of images, each tuple could contain information about the image and even the raw data containing the image itself.


### Tuples, Streams, and Operators

1.	**Streams**: A stream is a continuous sequence of records. 
    For example, think of images being uploaded to Twitter. Images are constantly being uploaded and the sequence of new images never ends. This sequence is an example of a Stream.
1.	**Tuples**:  A tuple represents a single record in the streaming data. 
     It is a structured list of attributes and their data types. Continuing the example above, in the stream of images, each tuple could contain information about the image's dimensions, tags, and so on.

1.	**Operators**: An operator processes tuples in a stream, one by one, and then sends the result of the processing to another operator downstream. 
    An example operator could be one that checks each uploaded image to filter out inappropriate content.

![Streams building Blocks](/streamsx.documentation/images/qse/buildingBlock1.gif) 

As shown in the diagram above, there are other important components called input ports and output ports, but we will cover them later.
An **input port** is a port where an operator can consume data. After the operator processes the records in memory, it produces a new stream of records as output. This new output stream of data is emitted from the **output port**.  An operator can have multiple input and output ports.


###  Build applications by connecting operators
To create a Streams application, you connect multiple operators in order of processing. This chain of operators makes up the application and is called the **Streams graph**.

![streams graph](/streamsx.documentation/images/qse/streams-graph-animation.gif)  



### How do I create a Stream?

Use an operator to create a Stream. 
The first Stream you create is the Stream containing the data you want to analyze from your external data source (Kafka, JMS, MQTT, database, HTTP endpoint).

To ingest this data, you use a special operator called a **Source Adapter** to connect to the external data source. The source adapter produces a stream of tuples that represent each event or message in the external data source. 

### How do I create an operator?

There are hundreds of built-in operators that you can reuse to build your application, or you can write your own. Streams includes source adapters for popular systems, like Kafka and Db2.

Below is an sample of a Streams graph that reads streaming data from Kafka filters it, scores an R model and saves the data to Db2 Event Store, using  built-in operators:

-  a `KafkaSource` operator to read the data, 
-  a `Filter` operator to include only elements of interest
-  the `RScript` operator to score the filtered data,
-  and the `EventStoreSink` operator to save the scored results. 

 ![streams graph](/streamsx.documentation/images/qse/sample-app-animation.gif)

<div class="alert alert-info" role="alert">
The available operators are grouped into tooklits. See the documentation for a <a href="https://www.ibm.com/support/knowledgecenter/en/SSCRJU_4.3.0/com.ibm.streams.toolkits.doc/spldoc/dita/toolkits/toolkits.html">list of available and toolkits</a>
</div>


## Create your first Streams Application in SPL

Now that we have gone through the basics, we are going to write a simple application that covers these concepts. We will use data in a file to make it easy to run. Later examples use a

The application will:

1. Process stock trades from a CSV file.
1. Filter out some of the stocks based on ticker names.
1. For each stock, calculate the latest average, maximum and minimum ask price. 
1. Verify the calculation
1. Print the results to `stdout`.

Here is the application's graph in Streams Studio:
Each operator in the graph corresponds to one of the steps above.

![application graph](/streamsx.documentation/images/qse/sampleApp4.gif)

You ran the completed version of this application in the previous section.
[TODO LINK]

You may find this example in the samples repository from Github. [TradeApp Sample on Github](https://github.com/IBMStreams/samples/tree/master/QuickStart/TradesApp).

#### Input data overview

To start writing a Streams application, you must have an understanding of the data that you are trying to process. 

The list of data Each row in the CSV file has the following format:

*   Ticker - a string that represents the name of the stock ticker
*   Date - a string that represents the date of the stock quote
*   Time - a string that represents the time of the stock quote
*   Ask Price - the ask price of the stock at the specified time

Here is a sample of the CSV data that we are going to process:
```
#ticker, date, time, askprice
"GLD","27-DEC-2019","14:06:09.854",50.7
"IYF","27-DEC-2019","14:12:38.019",103.69
"IOO","27-DEC-2019","14:13:20.873",64.02
"AU","27-DEC-2019","14:13:32.877",49
"CAJ","27-DEC-2019","14:14:17.938",60
"EWZ","27-DEC-2019","14:14:46.039",33.25</pre>
```

### 1. Create the main composite


The entry point of a Streams application is a **main composite**. A **main composite** is like the _main_ method from a Java / C++ program.

Create a main composite called `TradesAppMain`. This is represented in SPL as follows:

```
// Main composite: TradesAppMain
// A main composite has no input port and no output port.
composite TradesAppMain
{
    //application graph goes here
}
```

##### 1b Add the `graph` clause


To write a directed flow graph in the main composite, we add a **graph clause** into the main composite. A **graph** **clause** is a section in the composite that describes a list of operators in the graph, how the operators are connected, and what data is sent between the operators.

````
/ Main composite TradesAppMain
// A main composite has no input port and no output port.
composite TradesAppMain
{
    graph
}

````

###  2. Use operators to process data in steps

Remember, Streams applications are made up of **operators**. 
Each operator performs a specific task with an **input stream** of data and then produces an **output stream** that is the result of the processing.

#### What does an operator look like?

*Defining* an operator is not the same as *using* an operator. There are many built in operators that are included with Streams, so you just have use, or **invoke*** them. 

Comparing to Java/C++, think of a class that is defined in a 3rd-party library. To use the class, you typically have to create an instance of it. 

Similarly, an operator definition is like a class definition, whereas an instance of a class is called an **operator invocation**.

Let's see an example operator invocation.



#####  Sample operator invocation

The following image is a generic overview of an operator invocation, with the name of the operator that will be invoked, and its input and output. Every operator in your application will follow this format.


 - **Operator kind**: The type of the operator, e.g. `FileSource` or `Geofence`.
 - **Input stream** (optional) - The stream of data to be processed by the operator
 - **Output stream** (optional)- The results of the operator's action on the incoming data.
   - **Output stream schema** - Describes the content of each outgoing tuple.

There is a new term here, **schema**.   A schema is a specification of data types and attributes in a tuple. We'll see an example shortly.

   ![operator definition](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/04/splOverivew2.gif)


Let's start adding operators to your application graph.

### 2.1 Ingest data from the file

The first step is to ingest the data that you want to analyze. 
Thus, the first operator we'll use is a **`FileSource`** operator to read the input file.  The **`FileSource`** is an operator from the spl.adapter namespace in the SPL Standard Toolkit.


<pre>
/** Main composite for stock processing application
 * 
 */
composite TradesAppMain
{
    graph
         stream<<span style="color: #ff6600;">**rstring ticker, rstring date, rstring time, float64 askprice**</span>> <span style="color: #333399;">**TradeQuotesSrc**</span> = FileSource()
         {
  <span style="color: mauve;">param</span>
             <span style="color: #008000;"><strong>file:</strong> getApplicationDir() + "/data/trades.csv"</span>;
                 <span style="color: #008000;"><strong>format</strong>: csv;</span>
         }
}</pre>


In this operator invocation, we have defined the following:
* **Operator kind:**: **`FileSource`**.
* **Output stream name:**   <span style="color: #333399;">**TradeQuotesSrc**</span>.
* The **Output stream schema**, containing  4 attributes: <span style="color: #ff6600;">**ticker, date, time and askprice**</span>. Please note that this schema must match the format as specified in the CSV file for the operator to be able to parse the content of the file.
  
Within the operator invocation (curly brackets), we use the **param** clause to specify the location of the file using the **<span style="color: #008000;">file</span>** parameter.

To parse the input file as comma-separated-values, assign **<span style="color: #008000;">csv</span>** as the value for the **<span style="color: #008000;">format</span>** parameter.

This is all it takes to read a CSV file for processing. 

So far, the application graph has one operator and lookst like this:

 ![sampleApp0](/streamsx.documentation/images/qse/sampleApp0.gif)

### 2.2 Filter the input data by stock ID

Next, we are going to filter out some of the stocks based on its ticker by adding a **Filter** operator into the graph. ![sampleApp1](/streamsx.documentation/images/qse/sampleApp1.gif)

<pre> /** Main composite for stock processing application
  * 
 */
composite TradesAppMain
{
    graph
         <span style="color: #000000;">(stream<rstring ticker, rstring date, rstring time, float64 askprice> <span style="color: #333399;">**TradeQuotes**</span>) as TradeQuoteSrc = FileSource()
         {
             param
                 file: "/home/myuserid/data/trades.csv";
                 format: csv;
         }</span>

         (stream<**<span style="color: #ff6600;">rstring ticker, rstring date, rstring time, float64 askprice</span>**> <span style="color: #3366ff;">**FilteredTradeQuotes**</span>) 
         as FilteredTrade = Filter(**<span style="color: #333399;">TradeQuotes</span>**)
         {
             param
                 <span style="color: #008000;">**filter: ticker != "GLD";**</span>
         }
}</pre>

*   The **Filter** operator consumes the **<span style="color: #333399;">TradeQuotes</span>** stream from the **FileSource** operator.
*   The Filter operator also produces a stream named <span style="color: #3366ff;">**FilteredTradeQuotes.**</span>
*   <span style="color: #3366ff;"><span style="color: #000000;">The output stream schema is the same as the input stream. Therefore, we do not need an output clause to perform manual output attribute assignment. If a tuple is allowed to pass through in the Filter operator, attributes from the input stream will automatically be assigned to the same attributes on the output stream.</span></span>
*   The **Filter** operator defines a parameter named **<span style="color: #008000;">filter</span>.** This <span style="color: #008000;"><span style="color: #000000;">parameter specifies the condition to allow a tuple to pass through the filter. In this case, if the ticker name is not **GLD,** then the tuple will be allowed to get through the Filter.</span></span>

Next, we will add an **Aggregate** operator to calculate the min, max and average askprice of the stocks. ![sampleApp2](/streamsx.documentation/images/qse/sampleApp2.gif)

<pre> (stream<rstring ticker, float64 min, float64 max, float64 average>
 <span style="color: #666699;">**TradesSummary**</span>) as AggregateTrades = Aggregate(<span style="color: #3366ff;">**FilteredTradeQuotes**</span> as inPort0Alias)
 {
      **<span style="color: #800080;">window</span>**
          <span style="color: #800080;">**inPort0Alias : tumbling, count(5), partitioned ;**
     ** param
          partitionBy : ticker ;**</span>
      output
          TradesSummary : min = Min(askprice), max = Max(askprice), average =Average(askprice) ;
 }</pre>

The **Aggregate** operator consumes data from the **<span style="color: #3366ff;">FilteredTradeQuotes</span> **stream and produces a stream named **<span style="color: #666699;">TradesSummary.</span>** <span style="color: #000000;"></span> <span style="color: #000000;">The Aggregate operator operates on a window of data. We have set up a tumbling window with a count of 5\. The window is partitioned by ticker. With a partitioned window, the operator maintains a separate window for each of the stocks it encounters. For example, the operator maintains a window of 5 tuples for IBM stock. At the same time, a separate window is maintained for the last 5 stock prices from Apple.</span> <span style="color: #000000;">When the window is filled with 5 tuples (i.e. the trigger policy is met), the operator looks at the output functions specified in the **Output** clause. In this case, the user wants the operator to calculate the min, max and average askprice of the tuples in the window. The operator runs the output functions ( Min, Max and Average) and assign the results to the output attributes as specified. Since this is a **tumbling** window, the window will be emptied once the trigger policy is met.</span> The SPL language has two kinds of windows, tumbling and sliding. They both store tuples while they preserve the order of arrival, but differ in how they handle tuple evictions. Rather than keeping all the tuples ever inserted, windows are configured to evict expired tuples. In this respect, tumbling windows operate in batches. When a <dfn class="term">tumbling</dfn> window fills up, all the tuples in the window are evicted. This process is called a window <dfn class="term">flush</dfn>. Conversely, sliding windows operate in an incremental fashion. When a <dfn class="term">sliding</dfn> window fills up, the future tuple insertions result in evicting the oldest tuples in the window. The details of tuple eviction are defined by the eviction policy. Next, we will add a **Custom** operator to do some special processing with the TradesSummary data. The **Custom** operator is a special logic-related operator that can receive and send to any number of streams and does not do anything by itself. Thus, it offers a blank slate for customization in SPL. ![sampleApp3](/streamsx.documentation/images/qse/sampleApp3.gif)

<pre>(stream<rstring ticker, float64 min, float64 max, float64 average>
 CheckedTradesSummary) as CustomProcess = Custom(<span style="color: #0000ff;">**TradesSummary**</span>)
{
     <span style="color: #800080;">**logic**</span>
         onTuple <span style="color: #0000ff;">**TradesSummary**</span>: {
             if (average == 0.0l)
             {
                  printStringLn("ERROR: " + ticker);
             }
             else 
            {
                  submit(TradesSummary, CheckedTradesSummary);
            }
        }
 }</pre>

To write custom SPL logic, we add a **logic** clause in the **Custom** operator. On each tuple received by the operator, the logic clause is executed. In our logic clause, we check the average ask price for the stock. We flag an error with the data if the average ask price is zero and will not submit the tuple to the output port. If the average ask prices is greater than zero, then we submit the tuple to the CheckedTradesSummary output stream. Finally, we add a **FileSink** operator to write our analysis results to a file. ![sampleApp4](/streamsx.documentation/images/qse/sampleApp4.gif)

<pre> () as CheckedTradesSummaryFile = FileSink(<span style="color: #333399;">**CheckedTradesSummary**</span>)
 {
     param
          file : "/homes/myuserid/data/tradesSummary.csv" ;
          flush : 1u ;
          format : csv ;
 }</pre>

The **FileSink** consumes the output stream, <span style="color: #333399;">**CheckedTradesSummary**</span>, from the **Custom** operator. The operator writes output to a file named, "/homes/myuserid/data/tradesSummary.csv". The **flush** parameter controls how often the operator will flush content to the file system. In this case, the operator will flush after each tuple is received. The format parameter tells the operator the format to write the data in. In our example, the output file will be written in csv format. Here's the source code for this application:

<pre> /** Main composite for stock processing application
  *  
  */
composite TradesAppMain
{
    graph
         <span style="color: #000000;">(stream<rstring ticker, rstring date, rstring time, float64 askprice> <span style="color: #333399;">**TradeQuotes**</span>) 
         as TradeQuoteSrc = FileSource()
         {
             param
                 file: "/home/myuserid/data/trades.csv";
                 format: csv;
         }</span>

         <span style="color: #000000;">(stream<rstring ticker, rstring date, rstring time, float64 askprice> FilteredTradeQuotes) 
         as FilteredTrade = Filter(TradeQuotes)
         {
             param
                 filter: ticker != "GLD";
         }</span> 
        (stream<rstring ticker, float64 min, float64 max, float64 average>
         TradesSummary) as AggregateTrades = Aggregate(FilteredTradeQuotes as inPort0Alias)
        {
            window
                inPort0Alias : tumbling, count(5), partitioned ;
            param
                partitionBy : ticker ;
            output
                TradesSummary : average =Average(askprice), min = Min(askprice), max = Max(askprice) ;
        }

        (stream<rstring ticker, float64 min, float64 max, float64 average>
         CheckedTradesSummary) as CustomProcess = Custom(TradesSummary)
        {
            logic
                onTuple TradesSummary: {
                    if (average == 0.0l)
                    {
                       printStringLn("ERROR: " + ticker);
                    }
                    else 
                    {
                       submit(TradesSummary, CheckedTradesSummary);
                    }
                }
         }

         () as CheckedTradesSummaryFile = FileSink(<span style="color: #000000;">CheckedTradesSummary</span>)
         {
            param
               file : "/homes/myuserid/data/tradesSummary.csv" ;
               flush : 1u ;
               format : csv ;
         }
}</pre>

<a name="spl_basics"></a>

## SPL Basics

Although Streams applications can be developed using [Java](http://ibmstreams.github.io/streamsx.documentation/docs/4.1/java/java-appapi-devguide/) and [Python](http://ibmstreams.github.io/streamsx.documentation/docs/python/1.6/python-appapi-devguide/index.html), Streams Processing Language (SPL) is still a great option for writing Streams applications because it has been designed specifically for that purpose. You use it to describe the directed flow graph, define the schema on each of the streams; and customize the behaviour of each of the operators in the graph. This section is intended to help you get a high-level understanding of SPL.

### Main Composite

The entry point of a Streams application is a **main composite**. A **composite** operator is a graph of operators. A **main composite** is a special composite operator that has no input port and output port. Think of this as the _main_ method from a Java / C++ program. A main composite is represented in SPL as follows:

<pre>// Main composite: SampleMain
// This special composite has no input port and no output port.
composite SampleMain
{
}</pre>

To write a directed flow graph in the main composite, we add a **graph clause** into the main composite. A **graph** **clause** is a section in the composite that describes a list of operators in the graph, how the operators are connected, and what data is sent between the operators. ![splOverivew1](/streamsx.documentation/images/qse/splOverivew2.gif) 


An operator invocation starts by defining the schema and the name of the output stream that the operator is going to produce. In the example above, the name of the stream for **Operator1**, is **Operator1_output**. The stream is defined with a schema of **<rstring name>**. Next, the operator invocation block defines the operator to call. In the example above, we are invoking an operator named **Functor** from the _SPL Standard Toolkit_. Finally, an operator invocation block defines an input stream feeding into the operator. This is done by specifying the name of the output stream of another operator. In the example above, **Operator1** consumes data from a stream named FileSrcOutput. You may customize the behavior of an operator by writing additional clauses in an operator invocation:

<pre> (stream<rstring name> Operator2_output) as Operator2 = Operator(Operator1_output)
 {
    logic
       onTuple FileSrcOutput :
      {
        printStringLn(FileSrcOutput.name) ;
      }

    <span style="color: #800080;">**window**</span>
       inputStream : tumbling, count(5) ;
    <span style="color: #800080;">**param**</span>
       param1 : "param1Val";
       param2 : "param2Val";
    <span style="color: #800080;">**output**</span>
       Operator1_output : name = name + " newName" ;
    <span style="color: #800080;">**config**</span>
       placement : partitionColocation("pe1") ;
 }
</pre>

The clauses must be specified in the order as shown.

*   **logic -** The **logic** clause is called each time the operator receives a tuple. You may write custom SPL code here to process the input tuple.
*   **window** -The **window** clause allows you specify the kind of window the operator should use, and its trigger and eviction policy.
*   **params** - Each of the operators define a set of parameters to help you customize its behaviour.The **params** clause allows you to specify the values of the parameters.
*   **output** -The **output** clause allows you to customize attribute assignments of the output tuple. By default, if the input stream and the output stream contains an attribute of the same name and same type, the attribute value of the input stream will be automatically assigned to the same attribute on the output stream. In addition, you may customize output attribute assignment by specifying custom assignment expressions in the **output** clause. If the output stream contains an attribute that is not present in the input stream, you must specify an assignment for that attribute in the output clause.
*   **config** - The **config** clause allows you to specify various operator / process configurations supported by Streams. For example, you may use the config clause to control if two operators should run in the same process. You may also use the config clause to control which resource / host to run the process on.

This is a very high-level overview of the SPL language. For more details, refer to the [SPL Programming Reference](http://www-01.ibm.com/support/knowledgecenter/SSCRJU_4.0.0/com.ibm.streams.ref.doc/doc/spl-container.html?lang=en) from the Knowledge Center.

## **Choosing a development environment for SPL**

You can use [Atom](http://atom.io), [Microsoft VS Code](https://code.visualstudio.com/), or Streams Studio to create SPL applications. Streams Studio has been designed specifically for creating applications with SPL. In addition to its SPL editor, it also includes a drag and drop Graphical Editor for constructing Streams applications. You can simply drag and drop operators and connect them up in the SPL Graphical Editor. **The remainder of this guide focuses on Streams Studio.** **To start [developing applications using Atom or VS Code instead, follow this guide](http://ibmstreams.github.io/streamsx.documentation/docs/spl/atom/atom-apps/).**

*   To see a demo of Streams Studio, see this video: [InfoSphere Streams Studio in Action](https://www.youtube.com/watch?v=7kQqQSa2iSw&list=PLCF04A48C22F34B19&index=12)
*   To see a demo of the SPL Graphical Editor, on how to design and implement a Streams application, see this video: [Introduction to SPL Graphical Editor](https://developer.ibm.com/streamsdev/videos/infosphere-streams-v3-streams-studio-graphical-program-development-skill-builder/)

<a name="simple_streams_application"></a>



<a name="streams_application_pattern"></a>

## Streams Application Pattern

The sample Streams application demonstrates a common Streams application pattern. Most applications follow this pattern described as follows. Data is ingested from various data sources. As data is flowing through the application, it is prepared, analyzed and processed in memory. You can optionally store the data into a data store for record keeping or deeper analysis at any stage of the application. With the exception of the Ingest stage, all stages in this application pattern are optional. ![appPattern2](/streamsx.documentation/images/qse/appPattern2.gif)

*   **Ingest:** At the beginning of all Streams applications is the Ingest stage. In this stage, the application consumes continuous live data from disparate data sources. A data source can be a machine sensor, live feeds from social media sites, databases, file system, HDFS, etc. Streams provides a set of adapters to help ingest data from different kinds of data sources. Streams can handle any kind of data, both structured and unstructured. Examples of structured data include XML, JSON, CDRs, etc. Examples of unstructured data include unstructured text, voice, videos, signals, etc. As soon as data is ingested into the application, the data can be manipulated and analyzed in memory as it is flowing through the application.
*   **Prepare:** In this stage, the application can parse, transform, filter, clean, aggregate, or enrich the data in memory, preparing the data for real-time analytics. For example, if your application is ingesting videos from security cameras, you may need to process and parse the videos, and then convert them into a form that can be analyzed in the following stages. Another example is that if you are reading data from a message server in JSON format, you may need to parse the JSON text. At this stage, you may also correlate data from the different data sources, and enrich the data for analysis.
*   **Detect and Predict**: This is the stage where the application performs real-time analysis of the data, and for the application to gain insight into the data that is coming through. Streams provides a set of toolkits for data analysis. For example, Streams provides a timeseries toolkit for modeling, anomaly detection, and short-term and long-term forecasting. The SPSS toolkit allows a Streams application to perform real-time scoring against a pre-built SPSS model. The R toolkit allows you to analyze your data using R with your existing R scripts. There are many more toolkits available for analysis. If you need to run any specialized analysis that is not already available in one of the toolkits, you may write your own toolkits and operators to analyze the data.
*   **Decide**: In this stage, you use the insight gathered in the previous stage, and create logic to decide how to act on that insight. In addition, Streams can integrate with Business Rules software, like Operational Decision Manager (ODM). You may run the business rules against the flowing data, allowing you to make critical business decisions in real-time.
*   **Act:** In this stage, we act on the decision made from the previous stage. You may send the analysis result to a data visualization server. You may decide to send an alert to someone about the anomaly detected in the data. You may publish the results to a list of subscribers.

<a name="building_streams_applications"></a>

## Building Streams Applications

In the following sections, we are going to discuss how you can build your Streams application, and submit it to the Streams distributed runtime. **Before you begin:** Set up the necessary environment variables by running the following command:

<pre>source <Streams_Install>/bin/streamsprofile.sh</pre>

There are two ways to build a Streams application: _standalone_ or _distributed_. _Standalone_ Standalone mode is good for testing and debugging. In this mode, the application is built into a single program. You may run this program without submitting the application to a _Streams Instance_ (the Streams distributed runtime). To build the sample application in standalone mode, use the command below:

<pre>/opt/ibm/InfoSphere_Streams/4.0.0.0/bin/sc -M application::TradesAppMain --output-directory=output/application.TradesAppMain/Standalone --data-directory=data -T -a</pre>

*   The -M option specifies the name of the main composite to build
*   The --output-directory option specifies where to write the build output.
*   The --data-directory option specifies the data directory of the application. A data directory is an optional directory where data may be read or written for your application.
*   The -T option indicates that the application should be compiled into standalone mode.
*   The -a option specifies that the application should be compiled in optimized mode.

To run this application in standalone mode, run this command:

<pre><ApplicationOutputDir>/bin/standalone</pre>

_Distributed_ To build the sample application in distributed mode, simply remove the -T option as follows:

<pre>/opt/ibm/InfoSphere_Streams/4.0.0.0/bin/sc -M application::TradesAppMain --output-directory=output/application.TradesAppMain/Distributed --data-directory=/homes/myuserid/data -a</pre>

In distributed mode, the application is built into an application bundle (*.sab) in the output directory. The application bundle contains all file resources, libraries and dependencies required for running the application in distributed mode. To run the application in distributed mode, you need to submit this application bundle to a _Streams Instance_.<a name="streams_domain_and_instance"></a>

## Streams Domain and Instance

To run your application in distributed mode, you need a _Streams Domain_ and a _Streams Instance_. A domain is a logical grouping of resources (or containers) in a network for common management and administration. It can contain one or more instances that share a security model, and a set of domain services. An instance is the Streams distributed runtime environment. It is composed of a set of interacting services running across one or multiple resources. The Streams Instance is responsible for running Streams applications. When an application is submitted onto a Streams instance, it distributes the application code onto each of the resources. It coordinates with the instance services to execute the processing elements.<a name="setting_up_a_development_domain_and_instance"></a>

## Setting up a Development Domain and Instance

To set up a development domain and instance, follow these steps. A development domain and instance runs on a single host. You can dynamically add additional host to the domain later. First, if you have not already done so, set up the necessary environment variables by running the streamsprofile.sh.

<pre>source <Streams_Install>/bin/streamsprofile.sh</pre>

Next, start streamstool by typing the following command:

<pre>streamtool</pre>

When prompted to provide a ZooKeeper ensemble, enter the ZooKeeper ensemble string if you have a ZooKeeper server set up. Otherwise, press enter to use the embedded ZooKeeper. _streamtool_ is an interactive tool. To get content assist and auto-complete, press <Tab>.

### Domain

To make a new domain, enter this command in the _streamtool_ interactive command session:

<pre>mkdomain -d <domainName></pre>

Generate public and private key for Streams, so you do not have to keep logging in:

<pre>genkey</pre>

Start the domain:

<pre>startdomain</pre>

**Tip**: If the domain fails to start because a port is in use, you may change the port number by using setdomainproperty. For example, if JMX and SWS ports are in use:

<pre>setdomainproperty jmx.port=<jmxPort> sws.port=<sws.Port></pre>

### Instance

To make a new instance, enter this command:

<pre>mkinstance -i <instance-id></pre>

Start the instance:

<pre>startinstance</pre>

For information about domain and instance set up, refer to the following documentation:

*   [Enterprise Install and Setup Videos](https://developer.ibm.com/streamsdev/docs/streams-4-0-enterprise-install-and-setup-videos/)
*   [Multi-host environment: Installing to a shared file system](https://developer.ibm.com/streamsdev/docs/multi-host-environment-installing-shared-file-system/)
*   [Multi-host environment: Installing to each host and setting up a domain](https://developer.ibm.com/streamsdev/docs/multi-host-environment-installing-host-setting-domain/)

<a name="running_streams_applications_in_distributed_mode"></a>

## Running Streams Applications in Distributed Mode

Now that you have a domain and instance started, you can run your application in distributed mode. To submit a job, find the application bundle file (*.sab), and run the following command:

<pre>streamtool submitjob appBundleName.sab</pre>

To submit our sample application, we will change into the output directory of the application and submit the application bundle:

<pre>cd output/application.TradesAppMain/
streamtool submitjob application.TradesAppMain.sab</pre>

<a name="querying_for_job_status"></a>

## Querying for Job Status

You may query job status from your Streams Instance using streamtool commands. If using embedded ZooKeeper:

<pre>streamtool lsjob -d <streamsDomainName> -i <instanceName> --embeddedzk</pre>

If using external ZooKeeper ensemble:

<pre>streamtool lsjob -d <streamsDomainName> -i <instanceName> --zkconnect <zooKeeperHost>:<zooKeeperPort></pre>

You will see job status similar to this:

<pre>[streamsadmin@streamsqse Distributed]$ streamtool lsjobs -d StreamsDomain -i StreamsInstance --embeddedzk
Instance: StreamsInstance
 Id State Healthy User Date Name Group
 6 Running yes streamsadmin 2015-04-30T18:32:48-0400 application::TradesAppMain_6 default

</pre>

<a name="sample_application_output"></a>

## Sample Application Output

To see the result of the sample application, open the file as specified in the _file_ parameter of the FileSink operator:

<pre>() as CheckedTradesSummaryFile = FileSink(<span style="color: #000000;">CheckedTradesSummary</span>)
{
    param
        file : **<span style="color: #800080;">"/homes/myuserid/data/tradesSummary.csv"</span>** ;
        flush : 1u ;
        format : csv ;
}
</pre>

You will find entries like this in the file. The first string is the _ticker_ name of the stock that you have done this analysis for. The first number is the minimum ask price of the stock. The second number is the maximum ask price of the stock. The last number is the average ask price of the stock. The summary result is based on the last 5 records that the application has received about the stock.

<pre>"TWX",0,17.7,10.62
"FSL",0,26.19,15.62
"FSLb",0,26.29,20.928
"BK",0,32.53,26.024
"NFJ",0,21.59,17.26
"RIO",0,41.15,32.872
"NLY",0,11.23,8.97
"BGG",0,39.81,31.848</pre>

<a name="streams_console"></a>

## Streams Console

In addition to querying for job status using streamstool, you may also look at your job status and monitor the health of your Streams cluster using the Streams Console. Streams Console is a web-based admin console that allows you to monitor and administer your Streams Domain. To find the URL of the Streams Console, run the following command:

<pre>[streamsadmin@streamsqse Distributed]$ streamtool geturl
https://streamsqse.localdomain:8443/streams/domain/console</pre>

Open this URL in a browser, and you will see a log-in screen. If you are using the Streams Quick Start Edition VM, enter the following user ID and password: **streamsadmin:passw0rd** You will then see a dashboard like this: ![quikStartConsole](/streamsx.documentation/images/qse/quikStartConsole.gif) For more information about the Streams Console, see the following:

*   [Streams Console Overview](https://developer.ibm.com/streamsdev/docs/streams-console-overview/)
*   Videos from [Streams V4.0 Info](https://developer.ibm.com/streamsdev/docs/streams-v4-0-info/)

<a name="streams_studio"></a>

## Streams Studio

Streams provides an Eclipse-based integrated development environment (IDE) for you to develop your Streams applications. You may view and monitor your running applications in the Streams Studio Instance Graph: ![quickStartInstanceGraph](/streamsx.documentation/images/qse/quickStartInstanceGraph.gif) In addition, Streams Studio provides the following features:

*   Streams Explorer View - to help you manage your Streams Development Environment
*   Project Explorer build and launch support - to help you build and launch your Streams application
*   SPL Graphical Editor - to allow you to create your Streams application using a graphical interface, without having to know the details of the SPL language
*   SPL Editor - to help you write SPL code, providing you with support like syntax highlight, content assist, refactoring.
*   Instance Graph - to help you visualize, debug and monitor your running applications.
*   Metrics View - to help you debug and monitor your running applications, by looking at the metrics of your operators and processing elements

To get started with Streams Studio, try out the [Streams Studio Quick Start Guide](https://developer.ibm.com/streamsdev/docs/studio-quick-start/). For more information about Streams Studio, refer to the following: [Streams Studio Overview](https://developer.ibm.com/streamsdev/?p=6539)<a name="whats_next"></a>

## What's Next?

Learn by doing:

*   [Online Course: Get started with IBM Streams](https://developer.ibm.com/courses/all-courses/get-started-with-ibm-streams/)

Learn more about Streams:

*   [Explore Streams](https://developer.ibm.com/streamsdev/explore-streams/)