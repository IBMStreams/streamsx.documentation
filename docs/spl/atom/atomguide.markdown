SPL Development Guide for Atom
==============================

This development guide will cover using the Atom editor to create and
develop applications written in Streams Processing Language (SPL).

If you want to learn about Streams and SPL without downloading and
install the Streams runtime, this guide is for you.

To get started with Streams using a local installation, see the Getting
Started with the Streams Quick Start Edition page.
(/streamsx.documentation/docs/latest/qse-intro)

Prerequisites
-------------

If you are completely new to Streams, read the Quick Start Guide for a
basic introduction. Then you can return to this guide to:

-   Configure Atom/VSCode for development

-   Run a sample application to see Streams in action

-   Create your own applications from scratch

Note: This guide will only cover creating Streams applications using
SPL. See the Python development guide or the Java development guide to
learn about development in those languages.

If you would rather use VSCode, the development guide for that editor is
coming soon.

Table of Contents
-----------------

-   Overview

-   Configure Atom

-   Get your code into Atom

-   Get Familiar With the Editor

-   Creating a Streams application from scratch

-   Running an application

-   Adding a toolkit

-   Where to find samples

-   Appendix/Troubleshooting

Overview
========

Instead of downloading the Streams compiler and runtime to create your
applications, you will use the Streaming Analytics service, a cloud
based version of Streams. Applications created in Atom are sent to the
Streaming Analytics to be compiled and executed.

So, the first step is to create an instance of the service in the IBM
Cloud. Visit
<https://console.bluemix.net/catalog/services/streaming-analytics> to do
so.

Configure Atom
==============

If you haven't already done so, download and install
Atom.(https://atom.io)

### Set up and download the Streams plugins for Atom:

*atom-ide-ui, ide-ibmstreams, language-ibmstreams-spl,
build-ibmstreams*:

-   Go to **Atom** \> **Preferences** \> **Install** (might be different
    for Windows)

-   Search for each of the above packages and install it:

    ![](media/image1.png){width="6.307692475940508in"
    height="2.928090551181102in"}

<!-- -->

-   Install the themes of your choice:

    -   **Atom** \> **Preferences** \> **Install** \> **Themes**

    -   Search for and install either of *streams-dark-syntax* or
        *streams-light-syntax*.

#### Add the credentials for your Streaming analytics service:

-   ![](media/image2.png){width="4.047916666666667in"
    height="1.863888888888889in"}From the IBM Cloud dashboard, click the
    instance of the Streaming Analytics service you created earlier.
    This will bring you to the service's main page.

-   Make sure the service is started, if not, click **Start**.

-   Click **Service Credentials** to get the credentials for the
    service.

    -   If there are no credentials listed, click **New Credential** to
        create one, accepting the defaults.

-   Copy the credentials:

> ![](media/image3.png){width="4.738410979877515in"
> height="2.2213834208223973in"}

-   Go to **Atom \> Preferences \> Packages. Find the
    build-ibmstreams** package and click **Settings**.

-   Paste the credentials you copied in to the **Settings** text box.

<!-- -->

-   Add a toolkits folder:

    -   Designate an empty folder on your local filesystem as your
        toolkits directory. This folder will contain any additional
        toolkits that provide extra functionality.

    -   Go to **Atom \> Preferences \> Packages. Find the
        ide-ibmstreams** package and click **Settings.** Paste the path
        to the toolkit directory you just created in the **Toolkits
        Path** box.

        ![](media/image4.png){width="3.3216622922134733in"
        height="1.9873195538057742in"}

### Migrating from Streams Studio

If you have been using Streams Studio, below you can find links to
sections that show you how to import your projects, compile a summary of
major differences between Streams Studio and Atom.

-   **SPL Projects from Streams Studio** can be used in Atom without
    having to make any changes. See the Get your Code into Atom section
    \[LINK\] for instructions on how to do this.

-   **Adding a Streams Toolkit to your workspace** is discussed in the
    Extending your application with toolkits section below \[LINK\].

-   **The SPL Graphical Editor** is not available, you can view an
    application's graph in the Streams Console.

-   **Build Configurations** are not used to compile or launch
    applications from Atom.\
    To compile an SPL composite, you select the SPL file containing the
    composite, right click, and choose **Build** or **Build and submit
    Job**.

> ![](media/image5.png){width="3.915384951881015in"
> height="1.3051279527559054in"}

-   **Streams Installation, Instance and Domain Management:** SPL
    Plugins for Atom do not include any Domain or Instance management
    features because your Streams instance is created and managed in the
    IBM Cloud. You can manage your Streams instance from the Streaming
    Analytics Console. Learn more about the Streams Console here.
    \[LINK\]

-   **Application Monitoring:** Applications launched from Atom are
    executed on the Streaming Analytics service. Thus, you need to use
    Streams Console to view metrics, errors, and the Streams graph.

Get your code into Atom
=======================

To get the most out of this guide, it is a good idea to import the
sample application.

If you have your own code, you can also jump to the section that best
describes your use case:

-   Import an existing project (including Streams Studio projects)

-   Import a project from GitHub

-   Creating a new project in Atom

Import the sample project for this guide
-----------------------------------------

To follow along with this guide, download the BusAlerts application
archive. \[LINK\]

-   Unpack it into a folder

-   Import it into Atom: click **File** \> **Add Project Folder**.
    Browse to the project folder and click **Open.**

The following sections describe other ways to start development --
importing your own code from a file or GitHub, or creating a new
project.

Import an existing project
--------------------------

The same steps above apply to import any SPL project for use in Atom.

From Atom, click **File** -\> **Add Project Folder**. Browse to the
project folder, and click **Open.**

Import A Project From GitHub
----------------------------

If you have existing SPL code on Github**,** you can clone the
repository from within Atom:\
From the Command Palette (*CMD + Shift + P* on Mac), type *Github
Clone*:

> ![](media/image6.png){width="4.084616141732283in"
> height="2.577128171478565in"}

-   Then paste the repository URL and click **Clone**.

> ![](media/image7.png){width="4.211873359580053in"
> height="1.3076924759405075in"}

The project should be added to the project pane.

Creating a new project
----------------------

To create a new project, you have to create an empty folder and import
it into Atom, create the

###

### Create the project folder

-   Create an empty folder on your filesystem, e.g. MyStreamsProject

-   From Atom, go to **File** \> **Add Project Folder** and select the
    project folder.

### Create a toolkit information file

SPL projects are also known as toolkits. Each toolkit must have a
toolkit information file, info.xml, that describes the project and any
other applications/toolkits it depends on. This file must be in the top
level of the project.

-   Create a file within the folder called info.xml. Right-click the
    MyStreamsProject folder, select **New File**, and enter info.xml as
    the file name:

    ![](media/image8.png){width="3.707043963254593in"
    height="0.6178412073490813in"}

    Copy the contents of sampleinfo.xml \[LINK\] to get you started.

    ![](media/image9.png){width="4.484615048118985in"
    height="3.406919291338583in"}

    *Sample info.xml file*

Learn more about the information file in the Knowledge Center
<https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.dev.doc/doc/toolkitinformationmodelfile.html>

Create a namespace
------------------

Namespaces allow you to organize your SPL code, similar to Python
modules or Java packages.

-   Create a folder within your project with the target namespace:\
    Select the project, right click, and click **New Folder***. *

    -   Enter a name for the namespace, e.g. my.name.space:\
        ![](media/image10.png){width="4.019099956255468in"
        height="1.0069444444444444in"}

    -   Create a new file within the my.name.space folder, call it
        .namespace

        ![](media/image11.png){width="5.053846237970253in"
        height="1.046405293088364in"}

    -   The final folder structure should look like this:

        ![](media/image12.png){width="2.2918799212598424in"
        height="1.5437040682414698in"}

Now that your namespace is created, you can create your first SPL source
file.

### Create a SPL source file

A project can have multiple namespaces, and each namespace can have
multiple SPL source files. The SPL source file is where you define the
application you are creating. They can also contain helper functions.

-   Select the "my.name.space" folder, right click \> "New File"

-   Enter the name for the new SPL file, Main.spl.

-   Add the namespace declaration to the file adding the following line
    to Main.spl:\
    namespace my.name.space;

### Create a main composite

Executable SPL applications are called main composites. Below is a stub
for a new executable composite:

composite MyApp {

}

-   The final code should appear like this:

    ![](media/image13.png){width="4.330768810148731in"
    height="1.529650043744532in"}

Now you are ready to start development. If you would like some guidance
on how to create one please see the designing your streams application
section \[LINK\]

Whether you imported an existing application or are creating one from
scratch, it is a good idea to explore the Atom editor to learn about
useful editing features.

![](media/image14.png){width="4.741064085739283in"
height="2.523179133858268in"}

Get familiar with the Editor
============================

Run An Application
==================

Extending your application with toolkits
========================================

What is a toolkit?
------------------

The Streams runtime includes many operators which provide a wide variety
of functionality. Operators, in turn, are grouped by function into
toolkits. For instance, the operators used to connect to Kafka are in
the Kafka Toolkit.

Sometimes you need to add a toolkit that isn't already included in
Streams, such as one of the many open source toolkits available on
GitHub\[link\]. Or, you might wish to use an updated version of an
existing toolkit instead of the one included in the Streams runtime.

How to add a toolkit for development
------------------------------------

The general steps are:

-   Download the toolkit,

-   Place it in the Toolkits Directory you created when you configured
    Atom,

-   Add a dependency to the toolkit in your project's info.xml file.

Then the toolkit's operators and functions are ready for use within
Atom.

Let's walk through an example.

Adding a toolkit example: extending the BusAlerts application to use live data
------------------------------------------------------------------------------

To retrieve live bus locations from the NextBus service, we need to use
the HTTPGetXMLContent operator from the inet toolkit.

The inet toolkit is included in Streams but we will download the latest
version from Github:

1.  Download and unpack the toolkit:

    a.  Go to <https://github.com/IBMStreams/streamsx.inet/releases>

    b.  Download version 3.0 or greater:
        streamsx.inet.toolkit-3.0.0-**el7-amd64**

> ![](media/image57.png){width="4.175573053368329in"
> height="1.5689621609798776in"}
>
> **Note**: Some toolkits have platform dependent features that require
> multiple platform dependent releases. If the toolkit you wish to use
> has multiple releases for different platforms, make sure to choose the
> el7-amd64 release. This is the release that is compatible with the
> Streaming Analytics service.

2.  Place the toolkit in the toolkits directory:

    ![](media/image58.png){width="2.338888888888889in"
    height="2.1662193788276465in"}

> When you copy a toolkit to the toolkit directory, make sure that there
> is a toolkit.xml file is present at the top level of the folder, as
> shown above. I have two toolkits, com.ibm.streamsx.inet and
> com.ibm.streamsx.nlp, and both have a toolkit.xml file.

3.  Add a dependency to the com.ibm.streamsx.inet toolkit to your
    project:

    c.  Open the info.xml file of your project, in this case
        BusAlerts/info.xml. If your project does not have an info.xml
        file, create one using the sample \[HERE\]

    d.  Add a dependency to the com.ibm.streamsx.inet toolkit by editing
        the dependencies node:

        ![](media/image59.png){width="2.9773228346456695in"
        height="2.610255905511811in"}

        Here is a snippet for you to paste:

        \<info:toolkit\>

        \<common:name\>com.ibm.streamsx.inet\</common:name\>

        \<common:version\>\[3.0.0,4.0.0)\</common:version\>

        \</info:toolkit\>

After saving the info.xml file, the com.ibm.streamsx.inet toolkit is
ready for use in our application.

Go back to Main.spl.

We're going to replace the BusDataFromFile operator which is a
FileSource, with a HTTPGetXMLContext operator from the inet toolkit.

1.  Import the operator with a **use** directive:

    At the top of Main.spl, type:

    use com.ibm.streamsx.inet.http::HTTPGetXMLContent;

2.  Highlight the operator's definition and then click Edit \> Toggle
    Comment:\
    ![](media/image60.png){width="4.37081583552056in"
    height="1.8001596675415572in"}

3.  Paste the following snippet in the editor:

    stream\<xml locationXMLDoc\> RawData\_Live = HTTPGetXMLContent()

    {

    param

    url : getUrl(\"vehicleLocations\", \$agency);

    period : 30.0; //poll every 30 seconds

    updateParameter: \"t\";

    updateParameterFromContent: \"/body/lastTime/\@time\";

    }

4.  Change the BusLocationStream operator to use the RawData\_Live
    stream instead of the RawData stream:

    Change the line:

    stream\<NextBusLocation\> BusLocationStream =
    ParseNextBusData(RawData)

    to:

> stream\<NextBusLocation\> BusLocationStream =
> ParseNextBusData(RawData\_Live)

5.  Save the application.

> We've now replaced the operator that was reading from a file with one
> that will connect directly to NextBus. Try it out by selecting
> Main.spl \> Build and submit job.
>
> After the build succeeds, verify it is working by opening the
> Streaming Analytics console, wait a minute or 2 for the application to
> connect, and then checking the Log Viewer again:

Adding a toolkit: full steps
----------------------------

1.  Toolkits must be built, meaning that the top level of the toolkit
    must have a toolkit.xml file.

    a.  If you are downloading a toolkit from GitHub, a built version of
        the toolkit is available from the releases page of the GitHub
        project. If there are releases for different operating systems,
        choose the EL7-AMD64 build.

    b.  If no release exists, or if the downloaded release does not
        include a toolkit.xml file, see the toolkit's page for
        instructions on building it.

2.  Put the toolkit folder into the toolkit directory you created during
    the initial setup\[LINK\]. Recall that you specified this path in
    **the ide-ibmstreams** package settings.

3.  Create a toolkit information file, called info.xml for your project,
    if it does not already have one. This file describes your project
    and its dependencies. Download a sample here: \[LINK\]

    Learn more about the information file here:
    <https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.dev.doc/doc/toolkitinformationmodelfile.html>

4.  Edit the info.xml file to add a dependency to the toolkit you need

    The following is an example of adding com.ibm.streamsx.sometoolkit
    to the project's dependencies:

5.  From your SPL code, import the toolkit with a *use* directive:

    use com.ibm.streamsx.social::\*;

Find out which toolkits are already installed
---------------------------------------------

If you want to use a toolkit and are not sure if it is included in
Streams, the list of Streams toolkits that are supported on the
Streaming Analytics service is here:

https://cloud.ibm.com/docs/services/StreamingAnalytics/compatible\_toolkits.html\#compatible\_toolkits

**Download updated versions of Streams toolkits**

Periodical updates to the toolkits included in Streams are available
from Fix Central

Changing and recompiling a toolkit
----------------------------------

...

Creating Streams applications
=============================

Streams application pattern
---------------------------

You have an idea of what your application should do, e.g. "Detect when a
moving bus passes the known points of interest and send any alerts to
the bus".

How should you design your application?

First, recall the Streams application pattern:

![appPattern2](media/image61.gif){width="4.70245406824147in"
height="2.543646106736658in"}

All Streams applications follow this basic pattern: ingest the data,
filter/discard any uninteresting/erroneous data, analyze it and act on
the results.

Each stage in the diagram above is handled by one or more operators.

For example, in the BusAlerts application:

![](media/image62.tiff){width="6.5in" height="1.7715277777777778in"}

The bus data is *ingested*, buses near POIs are *detected*, and then the
*alert* is sent.

How to do it
------------

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

Acquiring input data
--------------------

Since all Streams applications start with a data ingestion step, this is
the first stage of your application.

If you do not yet have data to ingest, you can skip to the "generating
sample data" section for a few tips on generating data for your
application.

### Ingesting data using a source operator

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

Where to find examples
----------------------

-   Samples for most toolkits are included in the toolkit repository in
    the samples folder.

-   You can also search the Streams Samples catalog for examples. Click
    download zip to download the sample that you can import into Streams
    Studio, Atom or VSCode.

-   Streamsdev also has articles and tutorials, search there.

Troubleshooting
===============

1.  If submitting the job fails, you can view the full error in the Atom
    Console pane.

2.  You receive the following error when opening the Streaming Analytics
    console in the browser:

    CWOAU0062E: The OAuth service provider could not redirect the
    request because the redirect URI was not valid. Contact your system
    administrator to resolve the problem.

    If this occurs, log in to the IBM Cloud Dashboard by visiting
    cloud.ibm.com. Then you can access the console through one of the
    following ways:

    -   From the dashboard, click on your Streaming Analytics service
        instance under Services. Then from the instance page, click
        "Launch" to go to the console

    -   In Atom, there is a direct link available from the Console pane.
        Look for *Streaming Analytics Console URL*.

3.  Compiling an application fails with this message:

    CDISP0127E ERROR: The following toolkit file is out of date:
    ../toolkits/com.ibm.streamsx.inet/toolkit.xml. This file is newer:
    ../toolkits/com.ibm.streamsx.inet/com.ibm.streamsx.inet/InetSource/InetSource.xml.

> This error means a file in a toolkit you downloaded has changed.

1)  If you did not make any changes, this might be a bug that you can
    work around by doing the following:

    a.  Open a terminal window and change to the toolkits directory
        where you copied additional toolkits:

> cd /Users/path/to/tkdir

b.  For each toolkit listed in the error message, change to that toolkit
    directory.

> cd com.ibm.streamsx.inet
>
> touch toolkit.xml

Try recompiling your application again.

2)  If you did try to change a downloaded toolkit, you need to recompile
    the toolkit itself before you can use it within your application.
    This requires you to download the Streams Quick Start edition for
    Docker. \[LINK\]. Once you have done so, you can find compilation
    instructions from the toolkit's main page.

> Note: You will need to download and compile the toolkit on the Quick
> Start Edition, then copy the compiled toolkit back to your local
> filesystem.
