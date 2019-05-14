Now that you have created a project, let us walk through the creation of
the BusAlerts application.

Recall that this application will display alerts and advertisements
within the city's public transit vehicles as they move around the city.
The buses periodically report their location. When a bus is near an area
with an alert, the application will detect this and send the alert.

What will the application do?
=============================

We're going to develop the application in 3 steps:

1.  Receive data from each bus as it moves about

2.  Detect when the bus is near a point of interest

3.  Send the alert to the bus

Use operators to process data in steps
--------------------------------------

In the introduction to Streams concepts we learned that an **operator**
is a basic building block of a Streams application. It performs a
specific task with an **input stream** of data and then produces an
**output stream** which is the result of the processing.

In this application we'll use different operators at perform each of the
above 3 tasks.

Create the Main Composite

Create a new Main

Step 1: Ingest data
====================

Whenever creating a Streams application, you must first have a data to
analyze.

In our case, the data we are processing is the location of each bus as
it is reported. Each record is a XML string that describes the bus and
it's latitude, longitude, current speed, end so on:

> \<vehicle id=\"5764\" routeTag=\"24\" dirTag=\"24\_\_\_I\_F00\"
> lat=\"37.734356\" lon=\"-122.390739\" secsSinceReport=\"9\"
> predictable=\"true\" heading=\"218\" speedKmHr=\"0\"/\>

We have a sample of this data saved in a file. Later, we will extend
this application to ingest live data from the NextBus service.

stream\<xml locationXMLDoc\> NextBusData\_FromFile = FileSource()

{

param

file : getApplicationDir() + \"/data/saved\_BusLocations.txt\" ;

initDelay : 30.0 ;

}

stream\<rstring id,TimeMillis reportTime, float64 latitude, float64
longitude\> ParsedDataStream = ParseNextBusData(NextBusData\_FromFile )

{

param

agency : \$agency ;

}

stream\<POI\_WKT\_Type\> POI\_FromFile = FileSource()

{

param

file : getApplicationDir() + \"/data/poi.csv\" ;

}

stream\<Alert\> BusesToAlert as O = Custom(ParsedDataStream as
BusLocationStream ; POI\_FromFile

as F)

{

logic

state :

{

mutable list\<POI\_WKT\_Type\> POIList = \[ \];

}

onTuple F:

{

//add the POIs to a list

appendM(POIList, F) ;

}

onTuple BusLocationStream :

{

rstring busWKT = point(BusLocationStream.longitude,

BusLocationStream.latitude) ;

//for each POI

for(POI\_WKT\_Type poi in POIList)

{

//check the distance from the bus\' current location to the point

float64 distanceFromPOI = distance(busWKT, poi.locationWKT) ;

if(distanceFromPOI \< poi.radius)

{

//bus is near POI.

//Submit an alert tuple

mutable Alert out = { } ;

out.distance = distanceFromPOI ;

out.poi = poi.POI\_ID ;

out.message = poi.message ;

//copy input data to output

assignFrom(out, BusLocationStream) ;

submit(out, O) ;

}

}

}

}

() as AlertPrinter = Custom(BusesToAlert as In)

{

logic

onTuple In :

{

printStringLn(\"Bus \" + id + \" is near \" + poi +

\", message = \" + message + \" time \" +
com.ibm.streamsx.datetime.convert::toIso8601(reportTime)) ;

}

}

}

Creating Streams applications

-   Streams application pattern

-   Best practice

-   Acquiring Input Data

    -   Ingest data using a source operator

        -   Find the right source operator

        -   Define the incoming data schema

        -   (Optional) Convert JSON, XML and Binary data to tuples

        -   Validate the incoming data

    -   Generating data using a Beacon or Custom operator

        -   Geospatial data generator

-   Where to find examples

-   Writing your own Custom operators

**Streams application pattern**

You have an idea of what your application should do, e.g. "Detect when a
moving bus passes the known points of interest and send any alerts to
the bus".

How should you design your application?

First, recall the Streams application pattern:

![appPattern2](media/image1.gif){width="4.70245406824147in"
height="2.543646106736658in"}

All Streams applications follow this basic pattern: ingest the data,
filter/discard any uninteresting/erroneous data, analyze it and act on
the results.

Each stage in the diagram above is handled by one or more operators.

For example, in the BusAlerts application:

![](media/image2.tiff){width="6.5in" height="1.7715277777777778in"}

The bus data is *ingested*, buses near POIs are *detected*, and then the
*alert* is sent.

**Best practice**

To follow this pattern, you should build your application incrementally.

Instead of adding all the operators at once, **the best way to create
your application is to do so in stages, starting small and progressively
adding complexity.**

-   Ingest the data and validate that the data you are working with is
    correct.

-   Then, you can add operator(s) to further refine the data, with
    validation again as the last step.

-   Add more complex analytics and logic

-   Reporting, alerts and visualization.

So let's start with the first step in your streaming application, which
is acquiring data for processing.

**Acquiring input data**

Since all Streams applications start with a data ingestion step, this is
the first stage of your application.

If you do not yet have data to ingest, you can skip to the "generating
sample data" section for a few tips on generating data for your
application.

Ingesting data using a source operator

The first step is to find the right source operator for your data.

The table below lists common data sources and the corresponding Streams
operators.

View the full list of supported toolkits in the cloud and in a local
install.

Supported toolkits on the IBM Cloud Streaming Analytics service \[LINK\]

<https://cloud.ibm.com/docs/apps/tutorials/tutorial_scratch.html#tutorial>

<https://cloud.ibm.com/docs/services/StreamingAnalytics/r_integrating_cloudant_rest.html#tutorials>

Supported toolkits on-prem \[LINK\]
<https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.toolkits.doc/spldoc/dita/toolkits/toolkits.html>

Where is my data coming from? File, HDFS, HBase, IoT devices, e.t.c.

+-----------------------+-----------------------+-----------------------+
| Data source           | Operator              | Toolkit               |
+=======================+=======================+=======================+
| Event Streams         | MessageHubConsumer    | streamsx.messagehub   |
| (formerly Message     |                       |                       |
| Hub)                  |                       |                       |
+-----------------------+-----------------------+-----------------------+
| MQTT                  | MQTTSource            | streamsx.mqtt         |
+-----------------------+-----------------------+-----------------------+
| Kafka                 | KafkaConsumer         | streamsx.kafka        |
+-----------------------+-----------------------+-----------------------+
| HDFS                  | HDFS2FileSource       | streamsx.hdfs         |
|                       |                       |                       |
|                       | HDFS2DirectoryScan    |                       |
+-----------------------+-----------------------+-----------------------+
| HBase                 | HBaseScan/HBaseGet    | streamsx.hbase        |
+-----------------------+-----------------------+-----------------------+
| Any JDBC compliant    | JDBCRun               | streamsx.jdbc         |
| RDBMS                 |                       |                       |
+-----------------------+-----------------------+-----------------------+
| JMS/XMS/              | JMSSource             |                       |
|                       |                       |                       |
|                       | XMSSource             |                       |
+-----------------------+-----------------------+-----------------------+

1B) Define the incoming data schema and use it with the source operator

> Define the output schema that describes each incoming tuple:
>
> e.g.
>
> type XMLFromNextBus = xml xmlString;
>
> type JsonFromKafka = rstring jsonString;
>
> type DBRow = rstring id, rstring name, int32 id, timestamp last\_seen;

1c) If your data is in a different format, such as JSON or XML string,
or a binary blob, it will need to be converted to Streams tuples.

For example, if you have JSON data, use the JSONToTuple operator to
convert it to SPL tuples. The XMLParse operator is used to convert XML
data to tuples.

Step 1d) Verify the data is correct. Create a small application that
ingests the data and then prints it to console or to a file:

Example 1: no parsing needed

//change this to match the tuples you expect

type RawDataType = int32 id, rstring name, rstring timestamp;

composite MyApp {

graph

> stream\<RawDataType\> DataFromXYZ = XYZSource() {
>
> }

**() as DataPrinter = Custom(DataFromXYZ as port0) {**

**logic**

**onTuple port0: {**

**printStringLn("New Tuple : + (rstring)port0.id + port0.name");**

**}**

**}**

The DataPrinter operator will almost always be more or less the same as
shown above.

If you are not using the Streaming Analytics service and you have access
to the local filesystem, you could also write the incoming data to a
file using a FileSink and verify the ouput file's contents.

Example 2

Adding a parsing step and using a FileSink

Generating data

-   Use a Beacon to generate data:
    <https://github.com/IBMStreams/samples/blob/master/Examples-for-beginners/003_sink_at_work/sample/sink_at_work.spl#L16>

-   More complex samples can be generated using a Custom operator:

    <https://github.com/IBMStreams/samples/blob/master/Geospatial/MapViewerSample/com.ibm.streamsx.mapviewer/Main.spl#L27>

    Helper functions defined here:
    https://github.com/IBMStreams/samples/blob/master/Geospatial/MapViewerSample/com.ibm.streamsx.mapviewer.gen/GeospatialGen.spl
