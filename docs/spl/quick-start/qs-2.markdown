---
layout: docs
title:  Overview of Streams Concepts
description:  Get started with Streams using SPL
weight : 50
published: true
tag: spl-qs
navlevel: 2
next:
  file: qs-3
  title: FAQ
prev:
  file: qs-1
  title: Run your first application
---


The SPL Quick Start Guide is intended to help you get up and running with IBM Streams quickly. We will first introduce the basic concepts and building blocks. And then we will write a very simple Streams application.

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

### How do I create an Operator?

There are hundreds of built-in operators that you can reuse in your application, or you can write your own. Streams includes source adapters for popular systems, like Kafka and Db2.

For example, you could create a Streams application that reads from Kafka with the  `KafkaSource` operator, scores an R model with `RScript` operator and saves the data to Db2 Event Store with the `EvenStoreSink` operator.  These are all built-in operators.

#### Finding available operators

The available operators are grouped into tooklits. See the documentation for a <a href="https://www.ibm.com/support/knowledgecenter/en/SSCRJU_4.3.0/com.ibm.streams.toolkits.doc/spldoc/dita/toolkits/toolkits.html">list of available and toolkits</a>.  

There are also open-source toolkits in the [Streams GitHub project](https://github.com/IBMStreams/).
</div>

#### Writing your own operator

If you find that you need to write your own operator, you can also do so using Java, SPL, C++, or Python. You can wrap existing Java, C++ or Python code as a Streams operator.

- [Java operator guide](/streamsx.documentation/docs/java/java-op-dev-guide/) 
- [Python classes and functions as SPL operators](https://streamsxtopology.readthedocs.io/en/stable/streamsx.spl.spl.html#overview)
- C++ operators
    - [Example](https://github.com/IBMStreams/samples/tree/master/Examples-for-beginners/048_source_operator_with_control_port)
    - [Reference](https://www.ibm.com/support/knowledgecenter/en/SSCRJU_4.3.0/com.ibm.streams.dev.doc/doc/str_optypenativec.html)

## Create your first Streams application in SPL

Now that we have gone through the basics, we are going to write a simple application that covers these concepts. We will use data in a file to make it easy to run. Later examples use a

The application will:

1. Process stock trades from a CSV file.
1. Filter out some of the stocks based on ticker names.
1. For each stock, calculate the latest average, maximum and minimum ask price. 
1. Verify the calculation
1. Print the results to `stdout`.
1. Save the results to a file.

Here is the application's graph:
Each operator in the graph corresponds to one of the steps above.

![application graph](/streamsx.documentation/images/qse/sampleApp4.gif)

You ran the completed version of this application in the previous section.
[TODO LINK]

You may find this example in the samples repository from Github.  [TradeApp Sample on Github](https://github.com/IBMStreams/samples/tree/master/QuickStart/TradesApp).

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
"EWZ","27-DEC-2019","14:14:46.039",33.25
```

## 1. Create the main composite


The entry point of a Streams application is a **main composite**. A **main composite** is like the _main_ method from a Java / C++ program.

Create a main composite called `TradesAppCloud`. This is represented in SPL as follows:

```
// Main composite: TradesAppCloud
// A main composite has no input port and no output port.
composite TradesAppCloud
{
    //application graph goes here
}
```

##### 1b Add the `graph` clause


To write a directed flow graph in the main composite, we add a *graph clause* into the main composite. A **graph** **clause** is a section in the composite that describes a list of operators in the graph, how the operators are connected, and what data is sent between the operators.

````
/ Main composite TradesAppCloud
// A main composite has no input port and no output port.
composite TradesAppCloud
{
    graph
    //define application  here
}

````

##  2. Use operators to process data in steps

Remember, Streams applications are made up of **operators**. 
Each operator performs a specific task with an **input stream** of data and then produces an **output stream** that is the result of the processing.

#### What does an operator look like?

*Defining* an operator is not the same as *using* an operator. There are many built in operators that are included with Streams, so you just have to use, or **invoke*** them. 

Comparing to Java/C++, think of a class that is defined in a 3rd-party library. To use the class, you typically have to create an instance of it. 

Similarly, an operator definition is like a class definition, whereas an instance of a class is called an **operator invocation**.
Operator definition, that is, creating operators, is a slightly more advanced topic which we will not cover here. 

Let's look at an example operator invocation, that is, an example of using an operator.


#### Sample operator invocation

The following snippet is a generic overview of an operator invocation, with the name of the operator that will be invoked, and its input and output, if any.

Every operator in your application defines the following:
- Output stream, if any, 
- the name of the operator being invoked, 
- the input stream, if any. 
- Then any operator configuration clauses are defined within curly brackets.

Here is a sample:

<pre> stream&lt;<strong><span style="color: #800080;">rstring name, int32 id&gt;</span><span style="color: #ff6600;"> Operator2_output</span>
                            =<span style="color: #61bbef;"> SomeOperator </span>(<span style="color: #333399;"> Operator1_output</span>)
 {</strong>
    param   
        myParameter: "some value";   
 }
</pre>


- **Output stream**: The stream **Operator2_output** is  the **output stream** 
 
- **Output stream schema**: A **schema** describes the data types and attributes in a tuple. 
This stream is defined with a **schema** of `<rstring name, int32 id>`. This means that each tuple on the stream will have 2 attributes: `name` and `id`.

- **Operator name**: The **SomeOperator** operator is being invoked.
 
- **Input stream** that the operator will process is always the output stream of another operator. In the example above, **SomeOperator** consumes data from a stream named **Operator1_output**`. 

Finally, this operator is configured with some parameters, which are specified with the **param clause**.

There are additional options for customizing an operator, which we will cover later.

Now that we know the generic format of using operators, let's start adding operators to the application graph.

### 2.1 Ingest the input data from a file

You always start with ingesting the data that you want to analyze. This is usually data ingested from a live source such as Kafka. In our case our sample data is in a file, to keep this tutorial simple.

In this case, the first operator we'll use is a **`FileSource`** operator to read the input file.  The **`FileSource`** is an operator from the spl.adapter namespace in the SPL Standard Toolkit.


<pre>
/** Main composite for stock processing application
 * 
 */
composite TradesAppCloud
{
    graph
         stream&lt;<strong><span style="color: #ff6600;">rstring ticker, rstring date, rstring time, float64 askprice&gt;</span> <span style="color: #333399;">Quotes</span></strong>= FileSource()
         {
  <span style="color: mauve;">param</span>
             <span style="color: #008000;"><strong>file:</strong> getApplicationDir() + "/data/trades.csv"</span>;
                 <span style="color: #008000;"><strong>format</strong>: csv;</span>
         }
}</pre>


In this operator invocation, we have defined the following:
* **Operator kind:** `FileSource`.
* **Output stream name:**   <span style="color: #333399;"><strong>Quotes</strong></span>.
* The **Output stream schema**, containing  4 attributes: <span style="color: #ff6600;"><strong>ticker, date, time and askprice</strong></span>. Please note that this schema must match the format as specified in the CSV file for the operator to be able to parse the content of the file.
  
Within the operator invocation (curly brackets), we use the **param** clause to specify the location of the file using the <strong><span style="color: #008000;">file</span></strong>parameter.

To parse the input file as comma-separated-values, assign <strong><span style="color: #008000;">csv</span></strong>as the value for the <strong><span style="color: #008000;">format</span></strong>parameter.

This is all it takes to read a CSV file for processing. 

So far, the application graph has one operator and looks like this:

 ![sampleApp0](/streamsx.documentation/images/qse/sampleApp0.gif)

### 2.2 Filter the input data by stock ID

Next, we are going to filter stocks by ticker with a **Filter** operator. 

<pre> 
/** Main composite for stock processing application
  * 
 */
composite TradesAppCloud
{
    graph
        stream&lt; <span style="color: #000000;">rstring ticker, rstring date, rstring time, float64 askprice&gt;<span style="color: #333399;">Quotes</span> = FileSource()
         {
             param
                 file: getApplicationDir() + &quot;/data/trades.csv&quot;;
                 
                 format: csv;
         }</span>

         stream&lt;<span style="color: #ff6600;">rstring ticker, rstring date, rstring time, float64 askprice</span>&gt;<span style="color: #3366ff;">FilteredQuotes</span> = Filter(<strong><span style="color: #333399;">Quotes</span></strong>)
         {
             param
                 <span style="color: #008000;"><strong>filter: ticker != "GLD";</strong></span>
         }
}
</pre>

*  Operator Kind: **Filter**.  This operator consumes the <strong><span style="color: #333399;">Quotes</span></strong> stream from the **FileSource** operator.
*  The Filter operator produces an **output stream** named <span style="color: #3366ff;"><strong>FilteredQuotes.</strong></span>
*   The **Filter** operator defines a parameter named <strong><span style="color: #008000;">filter</span></strong>. This parameter specifies the condition to allow a tuple to pass through the filter:
    *   If the ticker name is not *GLD*, then the tuple will be included in the output stream, **FilteredQuotes**.  Otherwise, it will not be included in the output stream.
* For a **Filter** operator, the ** output stream schema** is always the same as the input stream schema Therefore, we do not need an output clause to perform manual output attribute assignment. If a tuple is allowed to pass through in the Filter operator, attributes from the input stream will automatically be assigned to the same attributes on the output stream.


This is what the application graph looks like now:

![sampleApp1](/streamsx.documentation/images/qse/sampleApp1.gif)


### 2.3 Calculate average price with the **Aggregate** operator.

Use another built-in operator called  **Aggregate** to calculate the minimum, maximum and average `askprice` of each stock. 

<pre> stream&lt;rstring ticker, float64 min, float64 max, float64 average&gt;<span style="color: #666699;"><strong>AvgPrice</strong></span> = Aggregate(<span style="color: #3366ff;"><strong>FilteredQuotes</strong></span> as inPort0Alias)
 {
     <<strong><span style="color: #800080;">window</span>
          <span style="color: #800080;">inPort0Alias : tumbling, count(5), partitioned ;
     param
          partitionBy : ticker ;</span></strong>
      <strong>output</strong>
          AvgPrice : min = Min(askprice), 
          max = Max(askprice),
         average =Average(askprice) ;
 }
</pre>


The **Aggregate** operator consumes data from the <strong><span style="color: #3366ff;">FilteredQuotes</span></strong> stream and produces a stream named <strong><span style="color: #666699;">AvgPrice.</span></strong>

There are a couple of new clauses in this operator invocation, **window** and **output**. What do they do?

**Window clause**

Usually you process each individual tuple as it arrives. But sometimes, you need to process tuples as a group, so you have to wait for them to arrive.

For example, to calculate the average price of the last 5 tuples, we need to wait till we have 5 tuples, then compute the average.
While we wait for the other tuples to arrive, we store them in a *window*.

**What is a window?** 


A window is a way to divide the stream of tuples into subsets. Tuples are stored in order of arrival. In our example, we create a window of size 5. 

![window example](/streamsx.documentation/images/python/window.jpg)

As shown above, a window stores tuples as they arrive.

When the window is "full", that is when there are 5 tuples in the window, the operator will:

-  Process the tuples in the window
-  Produce output
-  Remove one or more of the tuples from the window.

**Window clause**

The window clause specifies what kind of window we will create, how many tuples to collect in the window before processing, and any further subdivisions on the window.. 

Let's look at the different components:

<pre> <span style="color: #800080;">inPort0Alias : tumbling, count(5), partitioned ;</span></pre>

* **inPort0Alias**: This is the alias we gave to the input stream. So this is saying we want to configure a window on the input stream. This is helpful because sometimes an operator might have more than one input stream.

* **tumbling**: This means we want a tumbling window. Using a tumbling window means that when all tuples in the window are processed at once and removed afterwards. This is effectively a form of batch processing. The other kind of window is a *sliding* window, which process all the tuples in the window but only remove the oldest. What constitues oldest and other details are beyond the scope of this article. [LINK]
 
* **count(5**): The window size is specified here as a count-based window, with a count of 5. This simply means that whenever there are 5 tuples in the window, the operator will process all of them and empty the window. The tuples are said to *tumble* out, which is why it is called a tumbling window. 

The last component is the **partitioned** flag.

**Partitioning a window**

Defining a window as **partitioned**  will divide the tuples in the window into smaller windows based on an attribute.  These sub-windows are called partitions. 

Why do we need this? 

Remember that we want to compute the min, max and average price for each stock ticker. Let's say this list represents the first 5 tuples the operator receives:

        ticker, date, time, price
        "AU","27-DEC-2019","14:13:32.877",49
        "CAJ","27-DEC-2019","14:14:17.938",60
        "EWZ","27-DEC-2019","14:14:46.039",33.25
        "AU","27-DEC-2019","14:15:32.877",47
        "AWZ","27-DEC-2019","14:16:46.039",33.1

We have 5 tuples, but we only have 1 or 2 tuples for each stock ticker. So creating a simple window of 5 tuples will not work.

Thus, we partition the window by the `ticker` attribute. This will create sub-windows, or partitions, for each ticker. Thus each tuple with the same ticker will be in the same partition, and the min, max and average will be computed *for each ticker when the partition has  5 tuples with the same ticker.*

For example, when the first tuple in the list above arrives, the operator creates a window of 5 tuples for the "AU" stock. With the next tuple, a separate window is created for the last 5 stock prices for the "CAJ" stock, and so on.  Each window is maintained simultaneously for each unique stock ticker.

**The output clause**

The **output** clause is used when you need to define attributes that will be on each tuple in the output stream.

Since the Aggregate operator is using a window, when a partition has 5 tuples, the operator produces output based on what is defined in the output clause.

Recall the output clause we're using:
<pre>
<strong>output</strong>
         AvgPrice : min = Min(askprice), 
                    max = Max(askprice), 
                    average = Average(askprice) ;
  </pre>
This says that the **AvgPrice** stream is the output stream, and that it will have 3 attributes: `min, max and average.` 

The min, max and average of the `askprice`  will be computed using the the output functions ( `Min`, `Max` and `Average`) and assigned to respective output attributes.. 


### 2.4 Print the Results with a **Custom** operator

Finally, we will add a **Custom** operator to do some special processing with the data in the **AvgPrice** stream. The **Custom** operator is a special logic-related operator that can receive and send to any number of streams and does not do anything by itself. Thus, it offers a blank slate for customization in SPL. 


<pre>stream&lt;rstring ticker, float64 min, float64 max, float64 average&gt;
 PrintAvPrice = Custom(<span style="color: #0000ff;"><strong>AvgPrice</strong></span>)
{
     <span style="color: #800080;"><strong>logic</strong></span>
         onTuple <span style="color: #0000ff;"><strong>AvgPrice</strong></span>: {
             if (average == 0.0l)
             {
                  printStringLn("ERROR: " + ticker);
             }
             else 
            {
                printStringLn("Average asking price for " + ticker + "  is " +(rstring)
							average) ;
               submit(AvgPrice, PrintAvPrice);
            }
        }
 }</pre>

To write custom SPL logic, we add a **logic** clause in the **Custom** operator. On each tuple received by the operator, the logic clause is executed. In our logic clause, we check the average ask price for the stock. We flag an error with the data if the average ask price is zero and will not submit the tuple to the output port. If the average ask prices is greater than zero, then we submit the tuple to the `PrintAvPrice` output stream.
This is a very simple example of some of the checking you could add with a **Custom**. 

Our application graph has now been extended:

![sampleApp3](/streamsx.documentation/images/qse/sampleApp3.gif)

### 2.5: Writing results to a file (optional)
This part is marked optional because if you are running the application in the cloud you might not have access to the file system to be able to see the results file.

If you wanted to write the  output to a file, you could use a **FileSink** operator. 
It consumes the output stream, <span style="color: #333399;"><strong>PrintAvPrice</strong></span>, from the **Custom** operator and saves it to a file.

Notice that the **FileSink** does not define an output stream because it does not produce any output.

<pre> () as PrintToFile = FileSink(<span style="color: #333399;"><strong>PrintAvPrice</strong></span>)
     param
          file : "/tmp/tradesSummary.csv" ;
          flush : 1u ;
          format : csv ;
 }</pre>

**FileSink parameters**

The operator writes output to a **file** named `/tmp/tradesSummary.csv`.

The **flush** parameter controls how often the operator will flush content to the file system. In this case, the operator will flush after each tuple is received. 

The **format** parameter tells the operator to write the data to the file as `csv`, comma-separated values.



That is it!! We have created an application that computes the average, min and max price of the stock tickers and prints the result.

<a id="fullSource"></a>
## Complete application source

Here's the source code for this application:

<pre> 
composite TradesAppCloud
{
    graph
        stream&lt;rstring ticker, rstring date, rstring time, float64 askprice&gt;<span style="color: #333399;"><strong>Quotes</strong></span> = FileSource()
         {
             param
                 file: getApplicationDir() + "/data/trades.csv";
                 format: csv;
         }

         stream&lt;rstring ticker, rstring date, rstring time, float64 askprice&gt;  FilteredQuotes = Filter(Quotes)
         {
             param
                 filter: ticker != "GLD";
         }
        
        stream&lt;rstring ticker, float64 min, float64 max, float64 average&gt; 
        AvgPrice = Aggregate(FilteredQuotes as inPort0Alias)
        {
            window
                inPort0Alias : tumbling, count(5), partitioned ;
            param
                partitionBy : ticker ;
            output
                AvgPrice : average =Average(askprice),
                min = Min(askprice), max = Max(askprice) ;
        }

        stream&lt;rstring ticker, float64 min, float64 max, float64 average&gt;
         PrintAvPrice = Custom(AvgPrice)
        {
            logic
                onTuple AvgPrice: {
                    if (average == 0.0l)
                    {
                       printStringLn("ERROR: " + ticker);
                    }
                    else 
                    {//
                        printStringLn("Average asking price for " + ticker + "  is " +(rstring)
							average) ;
                       //example showing how to copy input stream to output in a Custom
                       submit(AvgPrice, PrintAvPrice);
                    }
                }
         }

         () as PrintToFile = FileSink(PrintAvPrice)
         {
            param
               file : "/tmp/tradesSummary.csv" ;
               flush : 1u ;
               format : csv ;
         }
}</pre>


### Running the application

This is a slightly modified version of the application you launched in the [previous section](/streamsx.documentation/docs/spl/quick-start/qs-1).

Regardless of the IDE you are using, you have to follow these steps to create and compile a Streams application:

- Create a project, 
- Create a namespace (optionally)
- Create a main composite in a `.spl` source file in the project
- Define the application graph like we did in this section
- Compile the main composite.


### 1. Create a project and a main composite

<ul class="nav nav-tabs">
  <li class="active"><a data-toggle="tab" href="#vscode"><b>VS Code</b></a></li>
   <li><a data-toggle="tab" href="#studio"><b>Streams Studio</b></a></li>
</ul>

<div class="tab-content">

<div id="vscode" class="tab-pane fade in active">
{% include atom_create.html %}

</div>

<div id="studio" class="tab-pane fade">

{% include studio_project.html %}

<br/><br/>
This automatically opens the graphical editor, but in this tutorial we're going to be working directly with SPL code, so open the SPL Editor:

<img alt="empty composite" src="/streamsx.documentation/images/qse/new-composite.jpg"/>

 </div>
</div>



<h3> 2. Save the application source </h3>

Copy and paste the [full application source](#fullSource) in the `.spl`  file you created. Save the file.

<h3> 3. Launch the application </h3>

This is a summary of the same steps you followed when you ran the sample application in the previous section. [LINK]



<ul class="nav nav-tabs">
  <li class="active"><a data-toggle="tab" href="#vscode2"><b>VS Code</b></a></li>
   <li><a data-toggle="tab" href="#studio2"><b>Streams Studio</b></a></li>
</ul>

<div class="tab-content">

<div id="vscode2" class="tab-pane fade in active">
Right click from within the `.spl` source file and click <strong>Build and submit job</strong>.

<br/>


<img alt="empty composite" src="/streamsx.documentation/images/qse/build-vscode.jpg"/>

</div>

<div id="studio2" class="tab-pane fade">
<p>
The application should automatically be built if you are using Streams Studio, so you are ready to launch it.
</p>
<p>
If your application does not build automatically, right click the project in the Project Explorer and click <strong>Build Active Configurations</strong>.

Then follow the instructions to [launch the application from Streams Studio](/streamsx.documentation/docs/spl/quick-start/qs-1a/#run-the-application).
</p>
</div>
</div>



## Sample Application Output

To see the result of the sample application, open the file as specified in the _file_ parameter of the FileSink operator:

<pre>() as CheckedTradesSummaryFile = FileSink(<span style="color: #000000;">CheckedTradesSummary</span>)
{
    param
        file : <strong><span style="color: #800080;">"/tmp/tradesSummary.csv"</span></strong>;
        flush : 1u ;
        format : csv ;
}
</pre>

You will find entries like this in the file. The first string is the _ticker_ name of the stock that you have done this analysis for. The first number is the minimum ask price of the stock. The second number is the maximum ask price of the stock. The last number is the average ask price of the stock. The summary result is based on the last 5 records that the application has received about the stock.

<pre>
ticker, min, max, average
"WLV",5.13,5.18,5.158
"ABI",26.59,26.59,26.59
"AF",30.24,30.25,30.246
"CIB",28.88,28.99,28.962
"CIN",42.91,42.95,42.926
"COT",14.68,14.83,14.738
</pre>




## Review

So far, we created and ran an SPL application using some of the built-in operators: **FileSource, Filter, Aggregate, Custom and FileSink.**


Recall that an operator invocation starts by defining the output schema and name of the output stream, as well as the name of the operator being invoked and its input stream.

### Operator invocation clause review


<pre> stream&lt;rstring name>  Operator2_output = SomeOperator (Operator1_output)
 {
     <span style="color: #800080;"><strong>logic</strong></span>
       onTuple Operator1_output :
      {
        printStringLn(Operator1_output.name) ;
      }

    <span style="color: #800080;"><strong>window</strong></span>
       inputStream : tumbling, count(5) ;
    <span style="color: #800080;"><strong>param</strong></span>
       param1 : "param1Val";
       param2 : "param2Val";
    <span style="color: #800080;"><strong>output</strong></span>
       Operator2_output : name = name + " newName" ;
    <span style="color: #800080;"><strong>config</strong></span>
       placement : partitionColocation("pe1") ;
 }
</pre>



In addition to the **param** clause, there are other clauses available: logic, window, output and config.

If used, the clauses must be specified in the order as shown.

* **logic**: To add additional processing for every incoming tuple, use the **logic** clause. The **logic** clause is called each time the operator receives a tuple. You may write custom SPL code here to process the input tuple, for example, printing the tuple as shown above.
  
* **window**: To process groups of tuples at a time instead of each individual tuples, use a **window** clause.  A *window* is a way to divide tuples into groups for processing. For example, to compute the average price of the last 10uples, we need to create a window of size 10. When the window has 10 tuples, the average will be computed and submitted to the output stream, and the 10 tuples will be removed from the window since they have been processed.

*  **params** - Each of the operators define a set of parameters to help you customize its behaviour.The **params** clause allows you to specify the values of the parameters.
  
*   **output** -The **output** clause allows you to customize attribute assignments of the output tuple. By default, if the input stream and the output stream contains an attribute of the same name and same type, the attribute value of the input stream will be automatically assigned to the same attribute on the output stream. In addition, you may customize output attribute assignment by specifying custom assignment expressions in the **output** clause. If the output stream contains an attribute that is not present in the input stream, you must specify an assignment for that attribute in the output clause.

*   **config** - The **config** clause allows you to specify various operator / process configurations supported by Streams. For example, you may use the config clause to control if two operators should run in the same process. You may also use the config clause to control which resource / host to run the process on.


<a name="streams_application_pattern"></a>

## Streams Application Pattern

The sample Streams application demonstrates a common Streams application pattern. Most applications follow this pattern described as follows.

Data is ingested from various data sources. As data flows through the application, it is prepared, analyzed and processed in memory. 

You can optionally store the data into a data store for record keeping or deeper analysis at any stage of the application.

With the exception of the Ingest stage, all stages in this application pattern are optional. ![appPattern2](/streamsx.documentation/images/qse/appPattern2.gif)

*   **Ingest:** At the beginning of all Streams applications is the Ingest stage. In this stage, the application consumes continuous live data from disparate data sources. A data source can be a machine sensor, live feeds from social media sites, databases, file system, HDFS, etc. Streams provides a set of adapters to help ingest data from different kinds of data sources. Streams can handle any kind of data, both structured and unstructured. Examples of structured data include XML, JSON, CDRs, etc. Examples of unstructured data include unstructured text, voice, videos, signals, etc. As soon as data is ingested into the application, the data can be manipulated and analyzed in memory as it is flowing through the application.


*   **Prepare:** In this stage, the application can parse, transform, filter, clean, aggregate, or enrich the data in memory, preparing the data for real-time analytics.
For example, if your application is ingesting videos from security cameras, you may need to process and parse the videos, and then convert them into a form that can be analyzed in the following stages. Another example is that if you are reading data from a message server in JSON format, you may need to parse the JSON text. At this stage, you may also correlate data from the different data sources, and enrich the data for analysis.


*   **Detect and Predict**: This is the stage where the application performs real-time analysis of the data, and for the application to gain insight into the data that is coming through. Streams provides a set of toolkits for data analysis. For example, Streams provides a timeseries toolkit for modeling, anomaly detection, and short-term and long-term forecasting. The SPSS toolkit allows a Streams application to perform real-time scoring against a pre-built SPSS model. The R toolkit allows you to analyze your data using R with your existing R scripts. There are many more toolkits available for analysis. If you need to run any specialized analysis that is not already available in one of the toolkits, you may write your own toolkits and operators to analyze the data.


*   **Decide**: In this stage, you use the insight gathered in the previous stage, and create logic to decide how to act on that insight. In addition, Streams can integrate with Business Rules software, like Operational Decision Manager (ODM). You may run the business rules against the flowing data, allowing you to make critical business decisions in real-time.


*   **Act:** In this stage, we act on the decision made from the previous stage. You may send the analysis result to a data visualization server. You may decide to send an alert to someone about the anomaly detected in the data. You may publish the results to a list of subscribers.


## Monitoring and managing your applications

### Using the Job Graph in VS Code

(Coming soon)

### Using the Streams Console

You can also look at your job status and monitor the health of your Streams cluster using the Streams Console. Streams Console is a web-based admin console that allows you to monitor and administer your Streams instance. 

{% include qs/open-streams-console.md %} 

You will then see a dashboard like this: 

![quikStartConsole](/streamsx.documentation/images/qse/quikStartConsole.gif) 

For more information about the Streams Console, see the following:

*   [Streams Console Overview](https://developer.ibm.com/streamsdev/docs/streams-console-overview/)
*   Videos from [Streams V4.0 Info](https://developer.ibm.com/streamsdev/docs/streams-v4-0-info/)



## What's Next?


*  Learn more about creating applications with Streams Studio:

   *  To get started with Streams Studio, try out the [Streams Studio Quick Start Guide](https://developer.ibm.com/streamsdev/docs/studio-quick-start/)


   *  Next, follow the [Streams Studio Hands-on tutorial](/streamsx.documentation/docs/spl/lab/spl-lab-00-get-started/)
  
*  Review the [tips for creating SPL applications](/streamsx.documentation/docs/spl/quick-start/qs-3)  


## Reference information

- [Windowing explained](https://developer.ibm.com/streamsdev/2014/05/06/spl-tumbling-windows-explained/)
 
- Operator refrences
   - [FileSink operator](https://www.ibm.com/support/knowledgecenter/en/SSCRJU_4.3.0/com.ibm.streams.toolkits.doc/spldoc/dita/tk$spl/op$spl.adapter$FileSink.html)
  - [FileSource operator](https://www.ibm.com/support/knowledgecenter/en/SSCRJU_4.3.0/com.ibm.streams.toolkits.doc/spldoc/dita/tk$spl/op$spl.adapter$FileSource.html)
  - [Aggregate operator](https://www.ibm.com/support/knowledgecenter/en/SSCRJU_4.3.0/com.ibm.streams.toolkits.doc/spldoc/dita/tk$spl/op$spl.relational$Aggregate.html)

- [Developing toolkits and operators](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.dev.doc/doc/creatingcustomartifacts.html)

- [Streams on GitHub](https://github.com/IBMStreams)