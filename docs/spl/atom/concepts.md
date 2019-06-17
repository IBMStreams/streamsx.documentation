---
layout: docs
title:  Streams  Introduction
navlevel: 2
---
Overview
--------

IBM® Streams is an advanced analytic platform that allows user-developed
applications to quickly ingest, analyze and correlate information as it
arrives from thousands of real-time sources. Streams can handle very
high data throughput rates, millions of events or messages per second.
Here are some of the key highlights of Streams:

-   **SPEED -** Streams** **can process data and provide actionable
    insight with sub-second latency.  Data is processed in memory as it
    arrives.  There is no need to store data.
-   **EFFICIENT **- Not only is Streams really fast, it is very
    efficient.  It can handle extremely high volume of data flow, with
    much less hardware requirement.
-   **INTEGRATE** - Streams can easily integrate with many external
    systems.  We support common storage systems like HDFS, HBase, DB and
    Files. In addition, we also support some of the most popular
    messaging systems like Kafka, MQTT and ActiveMQ.
-   **FLEXIBLE** - Streams can analyze any kind of data.  Streams can
    analyze structured data like csv, CDRs, XML, JSON.  It can also
    process unstructured data like audio, video, and text from social
    media site.
-   **ADVANCED ANALYTICS - **Streams provides a rich set of advanced
    analytics like geospatial and time series analysis.  It can also be
    integrated with popular data analytic tools like R and SPSS.
-   **EXTENSIBLE** - Streams comes with a programming framework that
    allows you to implement your own adapters to external systems or
    analytic functions in Java or C++.
-   **RESILIENT** - Streams distributed runtime is designed to be
    extremely resilient.  In the case of any system failure, the runtime
    can recover automatically without any human intervention.  Streams
    also has an application framework that allows Streams applications
    to be resilient, ensuring that no data is lost in the case of
    application or system failures. This is all done with minimal impact
    to application performance.
-   **TOOLING** - Streams is shipped with an integrated development
    environment - Streams Studio.  Streams Studio allows you to write,
    run, and debug your Streams application easily, all with a graphical
    interface.  The Streams Console is a web-based dashboard that allows
    Streams administrator to easily manage a Streams cluster.

[]{#basic_building_blocks}

Basic Building Blocks
---------------------

To write a Streams application, you need to first understand the basic
building blocks.
[![buildingBlock](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/04/buildingBlock1-300x165.gif){.wp-image-6219
.aligncenter width="265"
height="146"}](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/04/buildingBlock1.gif)
The fundamental building block of a Streams application is an
**operator**.  A **stream** of continuous records (messages, events,
tuples) flows into the **input port** of an operator.  An **input port**
is a port where an operator can consume data.  An operator can have 1 or
more input ports.  The operator processes the records in memory and
produces a new stream of records as output.  The new stream of data is
emitted from the **output port** of the operator.  An output port is a
port where the operator produces a stream of data.  An operator can have
1 or more output ports. A Streams application is a directed flow graph
of operators.  The diagram below is an example of a Streams application.
[![buildingBlockApp](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/04/buildingBlockApp-1024x445.gif){.wp-image-6217
.aligncenter width="537"
height="233"}](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/04/buildingBlockApp.gif)
 

-   **Source Adapter - **At the beginning of the application is a source
    adapter.   A source adapter is an operator that reads data from
    external systems and produces a **stream** as its output.
-   **Stream ** - A stream is an infinite sequence of records to be
    processed.
-   **Tuple** - A tuple represents individual records of the streaming
    data.  It is a structured list of **attributes** and their
    **data types**.
-   **Schema** - A schema is a specification of data types and
    attributes in a tuple.
-   **Operator** - An operator processes the stream from its upstream
    operator and produces a new output stream. The operator can process
    data on a tuple-by-tuple basis.  It can also operate on a **window**
    of data.  When processing is complete, the
    operator *submits* the result as a new tuple to its downstream
    operator. This process continues until it reaches the **sink
    adapter**.  An operator can perform any kind of processing on the
    data.  For example, it can perform simple processing like filtering
    unwanted data, transforming data from one format to another.  It can
    also be advanced analytic like predictive forecasting, data mining,
    text analytic, and geofencing.
-   **Window** - A finite sequence of tuples that the operator keeps in
    memory. A window is useful for processing real-time data in
    batches.  For example, for a telecommunication company, it may be
    interested in monitoring number of drop calls every 10 min for early
    detection of severe network failures.  A single drop call may not
    indicate a problem with the network.  But a large number of drop
    calls in a 10 min window may signal that something is seriously
    wrong.  In their Streams application, they can set up a window of
    drop call records to be processed every 10 mins.  Once the time
    expired, the drop call records can be analyzed.  And if the result
    indicates a significant problem, the company can act in a timely
    manner.
-   **Sink Adapter - **At the end of the application is a sink adapter.
     A sink adapter is an operator that writes data to external systems
    and does not produce a new stream.

**TIP:   **At this point, you may wonder where you can find the
operators to write your Streams application and if you need to write
them from scratch.  Streams ships with many operators out-of the box.
 The SPL Standard Toolkit provides basic data processing functions like
filtering, aggregation, sorting, etc.  In addition, Streams is shipped
many specialized toolkits for working with external systems and advanced
real-time analytics.

-   For a list of operators provided by the SPL Standard Toolkit:  [SPL
    Standard Toolkit
    Reference](http://www-01.ibm.com/support/knowledgecenter/SSCRJU_4.0.0/com.ibm.streams.ref.doc/doc/splstdtlkt-container.html?lang=en)
-   For a list of available specialized toolkit:  [Product Toolkits
    Overview](https://developer.ibm.com/streamsdev/docs/product-toolkits-overview/)
-   For a list of available open-source specialized toolkit on Github:
     [Github Projects
    Overview](https://developer.ibm.com/streamsdev/docs/github-projects-overview/)

[]{#spl_basics}

SPL Basics
----------

The Streams Processing Language (SPL) is a distributed data flow
composition language for writing a Streams application.  It is designed
to help you describe the directed flow graph; define the schema on each
of the streams; and allow you to easily customize the behavior of each
of the operators in the graph.  This section is intended to help you get
a high-level understanding of the SPL language. **TIP:**  Streams Studio
ships with SPL Graphical Editor for constructing Streams applications.
 You can simply drag and drop operators and connect them up in the SPL
Graphical Editor.  The editor supports the full SPL language
specification and you do not have to manually write SPL code.  In
addition, Streams Studio also provides an SPL editor.  The SPL Editor
provides syntax highlighting, content assist and code completion.  It is
a good tool to learn about the various SPL language features and
functions.

-   To see a demo of Streams Studio, see this video:  [InfoSphere
    Streams Studio in
    Action](https://www.youtube.com/watch?v=7kQqQSa2iSw&list=PLCF04A48C22F34B19&index=12)
-   To see a demo of the SPL Graphical Editor, on how to design and
    implement a Streams application, see this video: [Introduction to
    SPL Graphical
    Editor](https://developer.ibm.com/streamsdev/videos/infosphere-streams-v3-streams-studio-graphical-program-development-skill-builder/)

### Main Composite

The entry point of a Streams application is a **main composite**.
 A **composite** operator is a graph of operators.  A **main composite**
is a special composite operator that has no input port and output port.
 Think of this as the *main* method from a Java / C++ program.  A main
composite is represented in SPL as follows:

    // Main composite: SampleMain
    // This special composite has no input port and no output port.
    composite SampleMain
    {
    }

To write a directed flow graph in the main composite, we add a **graph
clause** into the main composite.  A **graph** **clause** is a section
in the composite that describes a list of operators in the graph, how
the operators are connected, and what data is sent between the
operators.
[![splOverivew1](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/04/splOverivew1.gif){.wp-image-6223
.aligncenter width="514"
height="180"}](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/04/splOverivew1.gif)
  The diagram above is an example of a graph clause in the main
composite.  Each of the operators is represented by an **operator
invocation** block in SPL.
[![splOverivew2](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/04/splOverivew2.gif){.alignnone
.wp-image-6228 .size-full width="872"
height="453"}](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/04/splOverivew2.gif)
An operator invocation starts by defining the schema and the name of the
output stream that the operator is going to produce.  In the example
above, the name of the stream for **Operator1**,
is **Operator1\_output**.  The stream is defined with a schema of
**\<rstring name\>**. Next, the operator invocation block defines the
operator to call.  In the example above, we are invoking an operator
named **Functor** from the *SPL Standard Toolkit*. Finally, an operator
invocation block defines an input stream feeding into the operator.
 This is done by specifying the name of the output stream of another
operator.  In the example above, **Operator1 **consumes data from a
stream named FileSrcOutput. You may customize the behavior of
an operator by writing additional clauses in an operator invocation:

     (stream<rstring name> Operator2_output) as Operator2 = Operator(Operator1_output)
     {
        logic
           onTuple FileSrcOutput :
          {
            printStringLn(FileSrcOutput.name) ;
          }

        window
           inputStream : tumbling, count(5) ;
        param
           param1 : "param1Val";
           param2 : "param2Val";
        output
           Operator1_output : name = name + " newName" ;
        config
           placement : partitionColocation("pe1") ;
     }

The clauses must be specified in the order as shown.

-   **logic - ** The **logic** clause is called each time the operator
    receives a tuple.  You may write custom SPL code here to process the
    input tuple.
-   **window** -** **The **window** clause allows you specify the kind
    of window the operator should use, and its trigger and eviction
    policy.
-   **params** - Each of the operators define a set of parameters to
    help you customize its behavior. ** **The **params** clause allows
    you to specify the values of the parameters.
-   **output** -** **The **output** clause allows you to customize
    attribute assignments of the output tuple.  By default, if the input
    stream and the output stream contains an attribute of the same name
    and same type, the attribute value of the input stream will be
    automatically assigned to the same attribute on the output stream.
     In addition, you may customize output attribute assignment by
    specifying custom assignment expressions in the **output **clause.
     If the output stream contains an attribute that is not present in
    the input stream, you  must specify an assignment for that attribute
    in the output clause.
-   **config** - The **config **clause allows you to specify various
    operator / process configurations supported by Streams.  For
    example, you may use the config clause to control if two operators
    should run in the same process.  You may also use the config clause
    to control which resource / host to run the process on.

This is a very high-level overview of the SPL language.  For more
details, refer to the [SPL Programming
Reference](http://www-01.ibm.com/support/knowledgecenter/SSCRJU_4.0.0/com.ibm.streams.ref.doc/doc/spl-container.html?lang=en)
from the Knowledge Center.   []{#simple_streams_application}

Simple Streams Application
--------------------------

Now that we have gone through the basics, we are going to write a simple
application that covers these concepts. Our first application will
process stock trades from a CSV file.  The application will filter out
some of the stocks based on ticker names.  It will then calculate the
average, maximum and minimum ask price for each of the stocks.  The
results will be written to a file. You may find this example in the
Samples repository from Github. [TradeApp Sample on
Github](https://github.com/IBMStreams/samples/tree/master/QuickStart/TradesApp)
To start writing a Streams application, you must have an understanding
of the data that you are trying to process.  The csv file that we are
going to process looks like this.

    #ticker, date, time, askprice
    "GLD","27-DEC-2005","14:06:09.854",50.7
    "IYF","27-DEC-2005","14:12:38.019",103.69
    "IOO","27-DEC-2005","14:13:20.873",64.02
    "AU","27-DEC-2005","14:13:32.877",49
    "CAJ","27-DEC-2005","14:14:17.938",60
    "EWZ","27-DEC-2005","14:14:46.039",33.25

The CSV file has the following format:

-   Ticker - a string that represents the name of the stock ticker
-   Date - a string that represents the date of the stock quote
-   Time - a string that represents the time of the stock quote
-   Ask Price - the ask price of the stock at the specified time

To create this application, we will first create a main composite named
**TradesAppMain:**

    * Main composite for stock processing application
     *
     */
    composite TradesAppMain {
    }

To read data from a file, you need to add the **FileSource** operator
into the graph.  **FileSource** is an operator from the **spl.adapter**
namespace in the SPL Standard Toolkit.
[![sampleApp0](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/04/sampleApp0-300x210.gif){.alignnone
.size-medium .wp-image-6341 width="300"
height="210"}](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/04/sampleApp0.gif)

    /** Main composite for stock processing application
     *
     */
    composite TradesAppMain
    {
        graph
             (stream<rstring ticker, rstring date, rstring time, float64 askprice> TradeQuotes) as TradeQuoteSrc = FileSource()
             {
                 param
                     file: "/home/myuserid/data/trades.csv";
                     format: csv;
             }
    }

-   In this FileSource invocation, we have defined the name of the
    output stream as [**TradeQuotes**]{style="color: #333399;"}.
-   The schema on the output stream contains 4 attributes:  [**ticker,
    date, time and askprice**]{style="color: #ff6600;"}.  Please note
    that this schema must match the format as specified in the CSV file
    for the operator to be able to parse the content of the file.
-   In the param clause, specify the location of the file using the
    **[file]{style="color: #008000;"}** parameter.
-   To parse the input file as comma-separated-values, assign
    **[csv]{style="color: #008000;"}** as the value for the
    **[format]{style="color: #008000;"}** parameter.

This is all it takes to read a CSV file for processing. Next, we are
going to filter out some of the stocks based on its ticker by
adding a **Filter** operator into the graph.
[![sampleApp1](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/04/sampleApp1.gif){.alignnone
.wp-image-6331 .size-full width="465"
height="157"}](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/04/sampleApp1.gif)

     /** Main composite for stock processing application
      *
     */
    composite TradesAppMain
    {
        graph
             (stream<rstring ticker, rstring date, rstring time, float64 askprice> TradeQuotes) as TradeQuoteSrc = FileSource()
             {
                 param
                     file: "/home/myuserid/data/trades.csv";
                     format: csv;
             }

             (stream<rstring ticker, rstring date, rstring time, float64 askprice> FilteredTradeQuotes)
             as FilteredTrade = Filter(TradeQuotes)
             {
                 param
                     filter: ticker != "GLD";
             }
    }

-   The **Filter **operator consumes the
    **[TradeQuotes]{style="color: #333399;"}** stream from
    the **FileSource** operator.
-   The Filter operator also produces a stream named
    [**FilteredTradeQuotes.  **]{style="color: #3366ff;"}
-   [[The output stream schema is the same as the input stream. 
    Therefore, we do not need an output clause to perform manual output
    attribute assignment.  If a tuple is allowed to pass through in the
    Filter operator, attributes from the input stream will automatically
    be assigned to the same attributes on the output
    stream.]{style="color: #000000;"}]{style="color: #3366ff;"}
-   The **Filter** operator defines a parameter
    named **[filter]{style="color: #008000;"}.  **This [[parameter
    specifies the condition to allow a tuple to pass through the filter.
     In this case, if the ticker name is not **GLD, **then the tuple
    will be allowed to get through the
    Filter.]{style="color: #000000;"}]{style="color: #008000;"}

Next, we will add an **Aggregate** operator to calculate the min, max
and average askprice of the stocks.
[![sampleApp2](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/04/sampleApp2.gif){.alignnone
.wp-image-6343 .size-full width="693"
height="172"}](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/04/sampleApp2.gif)

     (stream<rstring ticker, float64 min, float64 max, float64 average>
     TradesSummary) as AggregateTrades = Aggregate(FilteredTradeQuotes as inPort0Alias)
     {
          window
              inPort0Alias : tumbling, count(5), partitioned ;
          param
              partitionBy : ticker ;
          output
              TradesSummary : min = Min(askprice), max = Max(askprice), average =Average(askprice) ;
     }

The **Aggregate** operator consumes data from
the **[FilteredTradeQuotes ]{style="color: #3366ff;"}**stream and
produces a stream named
**[TradesSummary.]{style="color: #666699;"}**[ ]{style="color: #000000;"}
[The Aggregate operator operates on a window of data.  We have set up a
tumbling window with a count of 5.  The window is partitioned by ticker.
 With a partitioned window, the operator maintains a separate window for
each of the stocks it encounters.  For example, the operator maintains a
window of 5 tuples for IBM stock.  At the same time, a separate window
is maintained for the last 5 stock prices from Apple.
]{style="color: #000000;"} [When the window is filled with 5 tuples
(i.e. the trigger policy is met), the operator looks at the output
functions specified in the **Output** clause.  In this case, the user
wants the operator to calculate the min, max and average askprice of the
tuples in the window.  The operator runs the output functions ( Min, Max
and Average) and assign the results to the output attributes as
specified.  Since this is a **tumbling** window, the window will be
emptied once the trigger policy is met.  ]{style="color: #000000;"} The
SPL language has two kinds of windows, tumbling and sliding. They both
store tuples while they preserve the order of arrival, but differ in how
they handle tuple evictions. Rather than keeping all the tuples ever
inserted, windows are configured to evict expired tuples. In this
respect, tumbling windows operate in batches. When a tumbling window
fills up, all the tuples in the window are evicted. This process is
called a window flush. Conversely, sliding windows operate in an
incremental fashion. When a sliding window fills up, the future tuple
insertions result in evicting the oldest tuples in the window. The
details of tuple eviction are defined by the eviction policy. Next, we
will add a **Custom** operator to do some special processing with the
TradesSummary data.  The **Custom** operator is a special logic-related
operator that can receive and send to any number of streams and does not
do anything by itself. Thus, it offers a blank slate for customization
in SPL.
[![sampleApp3](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/04/sampleApp3.gif){.alignnone
.size-full .wp-image-6347 width="878"
height="163"}](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/04/sampleApp3.gif)

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

To write custom SPL logic, we add a **logic** clause in the **Custom**
operator.  On each tuple received by the operator, the logic clause is
executed.  In our logic clause, we check the average ask price for the
stock.  We flag an error with the data if the average ask price is zero
and will not submit the tuple to the output port.  If the average ask
prices is greater than zero, then we submit the tuple to the
CheckedTradesSummary output stream. Finally, we add a **FileSink**
operator to write our analysis results to a file.
[![sampleApp4](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/04/sampleApp4.gif){.alignnone
.size-full .wp-image-6351 width="879"
height="137"}](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/04/sampleApp4.gif)

     () as CheckedTradesSummaryFile = FileSink(CheckedTradesSummary)
     {
         param
              file : "/homes/myuserid/data/tradesSummary.csv" ;
              flush : 1u ;
              format : csv ;
     }

The **FileSink** consumes the output stream,
[**CheckedTradesSummary**]{style="color: #333399;"},  from the
**Custom** operator.  The operator writes output to a file
named, \"/homes/myuserid/data/tradesSummary.csv\".  The **flush**
parameter controls how often the operator will flush content to the file
system.  In this case, the operator will flush after each tuple is
received.  The format parameter tells the operator the format to write
the data in. In our example, the output file will be written in csv
format. Here\'s the source code for this application:

     /** Main composite for stock processing application
      *
      */
    composite TradesAppMain
    {
        graph
             (stream<rstring ticker, rstring date, rstring time, float64 askprice> TradeQuotes)
             as TradeQuoteSrc = FileSource()
             {
                 param
                     file: "/home/myuserid/data/trades.csv";
                     format: csv;
             }

             (stream<rstring ticker, rstring date, rstring time, float64 askprice> FilteredTradeQuotes)
             as FilteredTrade = Filter(TradeQuotes)
             {
                 param
                     filter: ticker != "GLD";
             }


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

             () as CheckedTradesSummaryFile = FileSink(CheckedTradesSummary)
             {
                param
                   file : "/homes/myuserid/data/tradesSummary.csv" ;
                   flush : 1u ;
                   format : csv ;
             }
    }

[]{#streams_application_pattern}

Streams Application Pattern
---------------------------

The sample Streams application demonstrates a common Streams application
pattern.  Most applications follow this pattern described as follows.
Data is ingested from various data sources.  As data is flowing through
the application, it is prepared, analyzed and processed in memory. You
can optionally store the data into a data store for record keeping or
deeper analysis at any stage of the application. With the exception of
the Ingest stage, all stages in this application pattern are optional.
[![appPattern2](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/05/appPattern2.gif){.alignnone
.size-full .wp-image-6966 width="860"
height="465"}](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/05/appPattern2.gif)

-   **Ingest:** At the beginning of all Streams applications is the
    Ingest stage.  In this stage, the application consumes continuous
    live data from disparate data sources.  A data source can be a
    machine sensor, live feeds from social media sites, databases, file
    system, HDFS, etc.  Streams provides a set of adapters to help
    ingest data from different kinds of data sources.  Streams can
    handle any kind of data, both structured and unstructured.  Examples
    of structured data include XML, JSON, CDRs, etc.  Examples of
    unstructured data include unstructured text, voice, videos, signals,
    etc.  As soon as data is ingested into the application, the data can
    be manipulated and analyzed in memory as it is flowing through the
    application.
-   **Prepare:**  In this stage, the application can parse, transform,
    filter, clean, aggregate, or enrich the data in memory, preparing
    the data for real-time analytics.  For example, if your application
    is ingesting videos from security cameras, you may need to process
    and parse the videos, and then convert them into a form that can be
    analyzed in the following stages.  Another example is that if you
    are reading data from a message server in JSON format, you may need
    to parse the JSON text.  At this stage, you may also correlate data
    from the different data sources, and enrich the data for analysis.
-   **Detect and Predict**:  This is the stage where the application
    performs real-time analysis of the data, and for the application to
    gain insight into the data that is coming through.  Streams provides
    a set of toolkits for data analysis.  For example, Streams provides
    a timeseries toolkit for modeling, anomaly detection, and short-term
    and long-term forecasting.  The SPSS toolkit allows a Streams
    application to perform real-time scoring against a pre-built SPSS
    model.  The R toolkit allows  you to analyze your data using R with
    your existing R scripts.  There are many more toolkits available for
    analysis.  If you need to run any specialized analysis that is not
    already available in one of the toolkits, you may write your own
    toolkits and operators to analyze the data.
-   **Decide**:  In this stage, you use the insight gathered in the
    previous stage, and create logic to decide how to act on
    that insight.  In addition, Streams can integrate with Business
    Rules software, like Operational Decision Manager (ODM).  You may
    run the business rules against the flowing data, allowing you to
    make critical business decisions in real-time.
-   **Act:  **In this stage, we act on the decision made from the
    previous stage.  You may send the analysis result to a data
    visualization server.  You may decide to send an alert to someone
    about the anomaly detected in the data.  You may publish the results
    to a list of subscribers.
