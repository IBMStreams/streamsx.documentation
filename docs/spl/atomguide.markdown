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

Atom Overview
-------------

This section covers some of the SPL features in Atom.

**The Project Pane**

This pane shows the projects you are currently working on. You can have
multiple projects open at any time. Use **File \> Add Project Folder**
to import a project.

![](media/image17.png){width="5.63907261592301in"
height="2.4532370953630798in"}

**The Command Palette**

Open the command palette (CMD + SHIFT + P) on a mac to see all the
available commands. If you are ever unsure of how to do something,
search the command palette to see if it is available.

**Version Control with Git**

The Git tab manages changes in your local repository and the GitHub tab
helps you with projects hosted on GitHub.

![](media/image18.png){width="3.6624234470691164in"
height="1.8479166666666667in"}

From the command palette, you can search for *Git or Github tab* and you
will be able to open or close these tabs. You can also open the Github
and Git tabs from the bottom right of the editor:

![](media/image17.png){width="5.63907261592301in"
height="2.4532370953630798in"}

![](media/image18.png){width="1.2549015748031496in"
height="1.8479166666666667in"}

Folders and files that have been changed are also highlighted in the
**Project** pane. For example, in the screenshot above, the QuickStart
folder and README.md file have both been changed.

See the Atom Flight Manual's section on Git to learn more about the Git
support in Atom.

<https://flight-manual.atom.io/using-atom/sections/github-package/>

SPL Editing Features
--------------------

The editor has rich code completion and content assist features.

For example, open sample/Main.spl from the BusAlerts project.

Line 7 contains the line *composite BusAlerts\_Main.*

This is the *main composite* of this application. It is the
application's entry point.

Let's use this application to explore some Atom features.

**Bracket matching** allows you to see the scope of a declaration:

![](media/image19.png){width="4.152083333333334in"
height="2.3222222222222224in"}

**Code Folding**

If the closing bracket isn't easily visible, Atom allows you to fold
portions of code, as shown below:

> ![](media/image20.gif){width="2.4797462817147857in"
> height="2.6047922134733157in"}
>
> Collapsing the composite shows the other functions defined in the SPL
> file.

Anywhere a downwards caret
![](media/image21.png){width="0.17692257217847768in"
height="0.1432108486439195in"} occurs, use it to collapse the code to
make it easier to read.

After defining any needed parameters, a composite must always start with
a graph clause (line 11).

Everything after the graph clause represents the application itself,
which is composed of one or more operators.

The first operator in the application is a FileSource operator:

![](media/image22.png){width="4.145262467191601in"
height="1.0918635170603674in"}

> FileSource operator invocation

The kind of the operator is a FileSource, but to differentiate between
invocations of operators of the same kind, each instance of the operator
is called by the name of the output stream. Thus, we refer to this
invocation of FileSource as the BusDataFromFile operator.

**View an operator's documentation **

You can hover over any artifacts, such as parameters, streams,
operators, and its documentation will be displayed, if it is available.

For example, hover over the FileSource to see its documentation:

> ![](media/image23.png){width="3.887619203849519in"
> height="1.534828302712161in"}

This operator reads data from a file and produces a stream of tuples
representing the data that was in the file.

This helps us understand the next few lines:

The **param** clause is a list of named parameters of the operator, such
as the file parameter which specifies the name of the file.

Hover over the initDelay parameter to see what it does.

**Find References within a File**

Above we saw a FileSource operator that produces a stream called
BusDataFromFile representing the data that was in the file.

To find out how the BusDataFromFile output stream is used in this
application, click on it to highlight occurrences:

> ![](media/image24.png){width="3.36709208223972in"
> height="1.405236220472441in"}
>
> References to that stream are highlighted in grey.

**Find All References Within a Project**

Continuing the example above, the BusDataFromFile stream is used by the
ParseNextBusData operator.

To see where this operator is defined, right click and select **Find
References** from the context menu.

![](media/image25.png){width="3.231788057742782in"
height="2.415209973753281in"}

This will show all mentions of this operator, including its definition
in the **Symbol References** pane:

![](media/image26.png){width="3.7406277340332457in"
height="1.8133497375328085in"}

Click on a result in that pane to go to the corresponding file.

**Note:** The **Go to Declaration** menu item is unsupported due to a
limitation in Atom.

**Finding problems**

The bottom left corner of the editor will show how many syntax errors
are in your code:

![](media/image27.png){width="1.5894039807524059in"
height="2.7696030183727034in"}**\
\
**Yay, no errors! But if there were, you could click the error icon and
it would open the Diagnostics pane to help you find and fix the errors.

You can also open all files with errors at once by typing "diagnostics
errors" from the Command Palette:

![](media/image28.png){width="3.388548775153106in"
height="1.039734251968504in"}

**Code Completion**

The editor also supports code completion. As you type, you can hit
CTRL+SPACE to bring up a list of suggestions:

![](media/image29.png){width="2.8862423447069117in"
height="1.9336876640419947in"}

The screenshot above shows the list of parameters available for the
FileSource operator.

**Operator Templates **

You can also add operators using templates.

Imagine that instead of the FileSource operator, we wanted to use the
HDFS2FileSource operator to read data from Hadoop.

To add a new HDFS2FileSource operator to our graph, hit CTRL + SPACE on
an empty line and search the available operator templates for *hdfs*:

![](media/image30.png){width="5.38628937007874in"
height="1.2170942694663167in"}

A template exists, so use the down arrows to select *HDFS2FileSource for
IBM Analytics Engine* and hit enter:

![](media/image31.png){width="3.064390857392826in"
height="1.0190879265091863in"}

The template for the operator is added to the file. Change the
operator's parameters, stream type, and output type to suit your needs.

Remember:

CTRL + SPACE shows code completion suggestions at any time.

ESC dismisses the suggestions that appear.

### Atom Documentation

Additional Information about Atom is available in the documentation:

Atom Basics:
<https://flight-manual.atom.io/getting-started/sections/atom-basics/>

Using Atom: https://flight-manual.atom.io/using-atom/

Run An Application
==================

You must compile, or build an application first before running it. From
Atom, building and execution are all done in the cloud.

Applications are built using the **Build** or **Build and submit job**
actions:

![](media/image32.png){width="4.592307524059493in"
height="1.5307688101487313in"}

Use **Build** to compile the application and download the executable
file to the output folder of your project.

**Build and submit job** builds the application and sends the executable
file to the cloud for execution.

Let's look at an example.

About The Sample Application
----------------------------

The BusAlerts application is for a city's transit system. The goal is to
display alerts and advertisements within the city's public transit
vehicles as they move through points of interest.

For example, if there is a security incident along a route, an alert can
be displayed inside the bus as the bus approaches the area. Also,
advertisements for local businesses along a bus' route will be displayed
as the bus approaches the business.

Build the application
---------------------

In the **Project** pane, select the SPL file containing the composite
you want to build.

![](media/image33.png){width="4.4in" height="1.4666666666666666in"}In
our example, select BusAlerts \> sample \>Main.spl. Right click, and
select **IBM Streams \> Build and submit job*.***

Various alerts describing the progress of compilation will pop up:

![](media/image34.png){width="4.2994663167104115in"
height="1.7713057742782152in"}

View compile messages and errors in the Console pane
----------------------------------------------------

The Console pane contains messages received from the Streaming Analytics
service. Check this pane to view details of any errors that may occur
during compilation.

Click **View \> Toggle Console** and the console pane will appear:

![](media/image35.png){width="2.5153816710411196in"
height="1.7988320209973754in"}

If an error occurs, see the Troubleshooting section for help to resolve
errors.

Run the application
-------------------

If you compiled using **Build**, you will be prompted when the
executable has been downloaded to the output folder of your project.

If you used **Build and submit Job**, you will receive an alert once
compilation is successful:

![](media/image36.png){width="4.222142388451443in"
height="0.9838134295713036in"}

*Submitting the job* means running the application on the Streaming
analytics service.

Click *Submit* and the application will be launched for you. We will
come back to the *Submit via Console* option later.

Once the application is launched, you will be prompted to view the
application in the Streams Console.

![](media/image37.png){width="4.6346117672790905in"
height="2.4430555555555555in"}

Clicking *Open Streaming Analytics Console* will open the console in
your browser.

View the running application in the Streams Console
---------------------------------------------------

Use the Streams Console application dashboard to manage your running
applications.

You can view data, error logs, and observe metrics such as throughput
and resource utilization.

![](media/image38.png){width="6.083356299212598in"
height="2.96923009623797in"}

The **Streams Graph** in the Console provides a visual representation of
each application that is running. Taking a closer look at this
visualization will help you understand your application's layout and
design.

![](media/image39.png){width="5.319784558180228in" height="2.0in"}

Each rectangle in the graph is an **operator**, and each arrow between
operators is called a **stream.** Each stream is data flowing into or
out of an operator.

You might recognize the first node in the graph, the *BusDataFromFile*
operator, which was an instance of a FileSource:

![](media/image40.png){width="3.6158945756780403in"
height="1.018708442694663in"}

### Viewing the Application's Logs

Recall that our application monitors buses and will send an alert if a
bus is near a business with an ad or an area with an alert.

The application is simple so whenever it detects that a bus should be
receiving an alert it just prints the details of the alert for now.

To see error logs and any other messages printed to stdout/stderr, go to
the Log Viewer from the far left:

![](media/image41.png){width="4.377483595800525in"
height="2.708465660542432in"}

Then, expand the application, select the *AlertPrinter* operator, and
click **Console Log**.

![](media/image42.png){width="6.292307524059493in"
height="2.33877624671916in"}

Each line indicates the bus route, the business or area of interest, and
the message that would be sent. For example, the first message would be
to the N bus, stating that there is a security incident near Mission
Dolores Park.

From the Log Viewer, you can return to the main dashboard by clicking
Application Dashboard \> Open Dashboard \> Application Dashboard.

![](media/image43.png){width="5.387416885389326in"
height="1.9794149168853894in"}

Launching an application with parameters
----------------------------------------

We submitted an application for execution without setting any
parameters.

This section will show how to provide parameters to an application right
before submission.

If you have an application and would like to specify a parameter at
runtime, you cannot submit the application from Atom after compilation.
The application must be submitted through the Streams Console.

If you try to submit a job and get this message:

> CDISR1146E The following job submission parameter is required, but it
> is missing: sample::BusAlerts\_Main.bus-agency.

Or this prompt:

![](media/image44.png){width="4.007692475940507in"
height="1.3637281277340332in"}

It means you need to recompile the application and submit it via the
Streams Console.

Select the SPL file, right click and click **Build**

![](media/image32.png){width="4.592307524059493in"
height="1.5307688101487313in"}

This will compile the application and save the executable file within
the output folder of your project.

If the build is successful, you will see a new folder within the project
containing the executable file:

![](media/image45.png){width="5.274120734908136in"
height="1.4892629046369203in"}

To launch the application, you can select the SAB file from the output
folder and click Submit Job.

![](media/image46.png){width="3.9307688101487313in"
height="1.7839643482064742in"}

You will again be prompted to submit the application, but this time
choose "Submit via Console"

![](media/image36.png){width="4.222142388451443in"
height="0.9838134295713036in"}

This will open the Streams Console in your browser.

From the Console, click the Play button to submit a job.

![](media/image47.png){width="2.44951334208224in"
height="0.7256944444444444in"}

Click **Browse** in the dialog that pops up, to select the SAB file from
the output folder of your project.

![](media/image48.png){width="3.720834426946632in"
height="2.770352143482065in"}

(Tip: the path to the file is printed in the Atom Console, so you can
copy and paste it)

![](media/image49.png){width="5.438461286089239in"
height="0.7855555555555556in"}

Click Submit. You will be prompted to set parameters:

![](media/image50.png){width="3.19034886264217in"
height="2.9384612860892387in"}

Here we are prompted with a list of all the application's parameters.
Change the values as you like and click OK.

This application has one named parameter called bus-agency, and the
default is *sf-muni*. Changing the bus-agency parameter to *ttc*
(Toronto Transit Commission) will cause this application to monitor
buses in Toronto.

Application parameters are called submission time values because they
are specified at submission time. Learn more about parameters and how to
add them to your application here.

Tip:

Try to use parameters as often as possible so that you do not have to
recompile your application to test out variations of a specific
parameter.

Adding parameters to your application 
--------------------------------------

In the code, the list of parameters in the submission dialog above is
based on the list of attributes in the **param** clause of the main
composite:

![](media/image51.png){width="2.6367465004374453in"
height="0.7598031496062992in"}

![](media/image52.png){width="3.230392607174103in"
height="0.5281747594050744in"}

Application parameters are called submission time values because they
are specified at submission time. Use the getSubmissionTimeValue
function to prompt the user for a parameter's value at submission time.

Tip: If there is no default value for a parameter, invoke
getSubmissionTimeValue with only the parameter's name and no default:

![](media/image53.png){width="3.7009798775153104in"
height="0.7185947069116361in"}

### Submission Time Values

Application parameters are also called submission time values, because
they are specified at submission time. The getSubmissionTimeValue
function returns the user-specified value of a named parameter.

This application has one named parameter, bus-agency:

![](media/image54.png){width="5.191773840769904in"
height="1.008053368328959in"}

getSubmissionTimeValue will return the value that you specified for the
bus-agency parameter at submission time, or the default if the value was
specified.

The bus-agency allows you to set id of the municipality that we are
monitoring.

The default is set to sf-muni, which stands for San Francisco
Municipality. So, the application we just launched is monitoring buses
in the San Francisco region. If we change the parameter, it would start
to monitor buses in a different region.

Select BusAlerts\_Main.spl in the Project pane, right click and choose
IBM Streams \> Build :

![](media/image55.png){width="4.476922572178478in"
height="1.4923075240594925in"}

Build vs. Build and Submit Job
------------------------------

To build an application, you must first compile it: Right click the SPL
file and choose **IBM Streams \> Build** or **IBM Streams \> Build and
Submit Job.**

**Running an application: summary**

**Build** and **Build and submit job** will both send the code to the
service for compilation.

-   Use **Build** to compile the application when you need to submit the
    application manually.

<!-- -->

-   You need to submit the application manually when you want to specify
    a parameter at submission time.

-   This action will save the executable file, called a SAB file, to a
    folder within your project called output.

-   Having the executable file saved locally also means you can relaunch
    the application whenever you need to, assuming you have not made any
    changes to the code. Of course, if you have changed the code, you
    will need to recompile.

    -   Use **Build and Submit Job** to compile and submit the
        application. It does not download the executable SAB file to the
        local project.

Understanding operators
-----------------------

You will notice that the BusDataFromFile operator only has an outgoing
arrow and does not have an incoming arrow. This means it does not
receive any incoming data but only produces output. Operators of this
kind are called *source* operators. Although there are dozens, if not
hundreds of operators available in streams, there are only 3 types:

An operator can be:

\- a source operator, meaning it produces data for processing and does
not take any input,

> \- a processing operator that accepts incoming data, performs some
> kind of processing on the incoming data, and forwards it to the next
> operator for more processing/analytics,

\- or a sink operator, which saves incoming data and does not produce
any output.

Looking again at the graph, this application has 2 source operators,
*BusDataFromFile* and *FenceInfo*, and 1 sink operator, *AlertPrinter*.
The remaining operators in between perform some processing.

![](media/image56.png){width="6.5in" height="2.4923611111111112in"}

Source/sink operators usually access external systems to read or write
data. The external systems could be a file, a database, messaging system
such as Kafka, raw TCP packets, HDFS (Hadoop File System), and many
more.

So far, the data about the buses' locations has been coming from a file.

The next step will be to change the application so that the data is no
longer from a file but from the live data feed provided by NextBus.

Stop a running application
--------------------------

Once you are finished with an application, stop it by clicking the
**Cancel** button from anywhere in the Streams console:

![](media/image57.png){width="3.015384951881015in"
height="0.7707053805774278in"}

Select the jobs to be cancelled and click Cancel Jobs:

![](media/image58.png){width="2.474884076990376in"
height="2.3370188101487313in"}

**Avoid leaving an application running on the Streaming Analytics
service so that you do not exceed the free computation limit and/or
incur additional charges. **

Extending your application with toolkits
========================================

All SPL projects, including the ones you create, are called toolkits.
Streams includes many toolkits contain useful operators and functions.
For example, the operators used to connect to Kafka are all in the Kafka
toolkit.

Almost all Streams applications you create will take advantage of some
of the toolkits included in the Streams runtime. To use these toolkits
you must add them to your application by

1.  Downloading the toolkit and placing it in your toolkit directory, if
    necessary

2.  Adding an entry for that toolkit to your project's info.xml file

3.  Importing the toolkit with a use directive in your SPL source.

If you did not download the toolkit, you can skip step 1.

You will need to complete step 1 if:

\- you are using an updated version of one of the supported toolkits
\[LINK\] or

\- the toolkit in question was downloaded from GitHub or a 3^rd^ party
toolkit.

\[https://cloud.ibm.com/docs/services/StreamingAnalytics/compatible\_toolkits.html\#compatible\_toolkits\]

Adding a toolkit example
------------------------

Our sample application has been using data that was saved in a file. We
want to change it to retrieve live bus locations from the NextBus
service.

Instead of a FileSource operator, we need to use the HTTPGetXMLContent
operator from the inet toolkit.

The inet toolkit is included in Streams but we want to use the latest
version from Github, so our first taski

### Step 1: Download and unpack the toolkit

a.  Go to <https://github.com/IBMStreams/streamsx.inet/releases>

b.  Download version 3.0 or greater:
    streamsx.inet.toolkit-3.0.0-**el7-amd64**

> ![](media/image59.png){width="4.175573053368329in"
> height="1.5689621609798776in"}
>
> **Note**: Some toolkits have platform dependent features, and so there
> will be that multiple platform dependent releases. If the toolkit you
> wish to use has multiple releases for different platforms, make sure
> to choose the **el7-amd64** release. This is the release that is
> compatible with the Streaming Analytics service.

c.  Place the toolkit in the toolkits directory:

    ![](media/image60.png){width="2.338888888888889in"
    height="2.1662193788276465in"}

    When you copy a toolkit to the toolkit directory, make sure that
    there is a toolkit.xml file is present at the top level of the
    folder, as shown above. I have two toolkits, com.ibm.streamsx.inet
    and com.ibm.streamsx.nlp, and both have a toolkit.xml file.

### Step 2 Add a dependency to the toolkit to your project:

d.  Open the info.xml file of your project, in this case
    BusAlerts/info.xml. If your project does not have an info.xml file,
    create one using the sample \[HERE\]

e.  Add a dependency to the toolkit:

    com.ibm.streamsx.inet toolkit by editing the dependencies node:

    ![](media/image61.png){width="2.9773228346456695in"
    height="2.610255905511811in"}

    Here is a snippet for you to paste:

    \<info:toolkit\>

    \<common:name\>com.ibm.streamsx.inet\</common:name\>

    \<common:version\>\[min\_ver,max\_ver)\</common:version\>

    \</info:toolkit\>

After saving the info.xml file, the com.ibm.streamsx.inet toolkit is
ready for use in our application.

### Step 3: Import the toolkit in your SPL source

Go back to Main.spl.

We're going to replace the BusDataFromFile operator which is a
FileSource, with a HTTPGetXMLContext operator from the inet toolkit.

1.  Import the operator with a **use** directive:

    At the top of Main.spl, type:

    use com.ibm.streamsx.inet.http::HTTPGetXMLContent;

2.  Highlight the operator's definition and then click Edit \> Toggle
    Comment:\
    ![](media/image62.png){width="4.37081583552056in"
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
> Main.spl \> **Build and submit job**.
>
> After the build succeeds, verify it is working by opening the
> Streaming Analytics console, wait a minute or 2 for the application to
> connect, and then checking the Log Viewer again.

Adding a toolkit: summary
-------------------------

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

![appPattern2](media/image63.gif){width="4.70245406824147in"
height="2.543646106736658in"}

All Streams applications follow this basic pattern: ingest the data,
filter/discard any uninteresting/erroneous data, analyze it and act on
the results.

Each stage in the diagram above is handled by one or more operators.

For example, in the BusAlerts application:

![](media/image64.tiff){width="6.5in" height="1.7715277777777778in"}

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
