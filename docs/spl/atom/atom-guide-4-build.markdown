---
layout: docs
title:  Build and run an application
description:  Steps to build an applicaiton
navlevel: 2
tag: atom
prev:
  file: atom-guide-3-editor
  title: Importing your code into Atom
next:
  file: atom-guide-5-toolkits
  title: Adding toolkits to your application
---

With the cloud based development using Atom, compilation and execution
are all done in the cloud. From Atom, you can compile an SPL application using the
**Build** and **Build and submit Job** actions:

![](media/image32.png){width="4.592307524059493in"
height="1.5307688101487313in"}

If you choose **Build,** the application will be compiled and the
resulting executable (SAB) file will be saved to the `output` folder of
your project. If you choose **Build and submit job**, the SAB file will
be sent to the cloud for execution.

Let's look at an example.

About the sample Application
----------------------------

The `BusAlerts` application displays alerts and advertisements within the city's public transit vehicles as they move through points of interest.

For example, if there is a security incident along a route, an alert is
displayed inside the bus as the bus approaches the region. Also,
advertisements for local businesses along a bus' route will be displayed
as the bus approaches the business.

Build the application
---------------------

![](media/image33.png)
In the **Project** pane, select the SPL file containing the composite you
want to run. In our example, select **BusAlerts** \>**sample** \> **Main.spl**. Right
click, and select **IBM Streams** -\> **Build and submit job**.

Various alerts describing the progress of compilation will pop up:

![](media/image34.png){width="4.2994663167104115in"
height="1.7713057742782152in"}

View Compile Messages and Errors in the Console Pane
----------------------------------------------------

The Console pane contains all information and error messages received
from the Streaming Analytics service. Check this pane to view details of
any errors that may occur during compilation.

Click **View \> Toggle Console** and the console pane will appear:

![](media/image35.png){width="2.5153816710411196in"
height="1.7988320209973754in"}

If an error occurs, see the Troubleshooting section for help to resolve
errors.

Run the application
-------------------

If you compiled using **Build and submit Job**, you will receive an alert
once compilation is successful:

![](media/image36.png){width="4.222142388451443in"
height="0.9838134295713036in"}

*Submitting the job* means running the application on the Streaming
analytics service.

Click **Submit** and the application will be launched for you. We will
come back to the **Submit via Console **option later.

View the running application in the Streams Console
---------------------------------------------------

Once the application is launched, you will be prompted to view the
application in the Streams Console.

![](media/image37.png){width="4.6346117672790905in"
height="2.4430555555555555in"}

Clicking **Open Streaming Analytics Console** will open the console in
your browser.

Streams Console Overview
------------------------

You can manage and observe your running applications from the Streams
Console. You can start, restart and stop applications here, view log
data, and observe metrics such as throughput.

![](media/image38.png){width="6.083356299212598in"
height="2.96923009623797in"}

### Viewing the Application's Logs

Let's start by looking at the output of the application. Recall that our
application monitors buses and will send an alert if a bus is near a
business with an ad or an area with an alert. The application is simple
so whenever it detects that a bus should be receiving an alert, it just
prints the alerts for now. We can take a look at the output by going to
the Log Viewer, which is opened from the far left:

![](media/image39.png){width="4.377483595800525in"
height="2.708465660542432in"}

Then, expand the application, select the *AlertPrinter* operator, and
click **Console Log**.

![](media/image40.png){width="6.292307524059493in"
height="2.33877624671916in"}

Each line indicates the bus route, the business or area of interest, and
the message that would be sent. For example, the first message would be
to the N bus, stating that there is a security incident near Mission
Dolores Park.

Launching an application with parameters
----------------------------------------

So far we submitted an application for execution without setting any
parameters at runtime.

This section will show how to provide parameters to an application right
before submission.

Our application has been monitoring buses in the San Francisco
Municipality. We can change it to monitor buses in a different region,
e.g. Toronto, simply by changing the bus-agency parameter.

If you have an application and would like to specify a parameter at
runtime, you cannot submit the application from Atom after compilation.
The application must be submitted through the Streams Console.

If you try to submit a job and get this message:

> CDISR1146E The following job submission parameter is required, but it
> is missing: sample::BusAlerts\_Main.bus-agency.

Or this prompt:

![](media/image41.png){width="4.007692475940507in"
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

![](media/image42.png){width="5.274120734908136in"
height="1.4892629046369203in"}

To launch the application, you can select the SAB file from the output
folder and click Submit Job.

![](media/image43.png){width="3.9307688101487313in"
height="1.7839643482064742in"}

You will again be prompted to submit the application, but this time
choose "Submit via Console"

![](media/image36.png){width="4.222142388451443in"
height="0.9838134295713036in"}

This will open the Streams Console in your browser.

From the Console, click the Play button to submit a job.

![](media/image44.png){width="2.44951334208224in"
height="0.7256944444444444in"}

Click **Browse** in the dialog that pops up, to select the SAB file from
the output folder of your project.

![](media/image45.png){width="3.720834426946632in"
height="2.770352143482065in"}

(Tip: the path to the file is printed in the Atom Console, so you can
copy and paste it)

![](media/image46.png){width="5.438461286089239in"
height="0.7855555555555556in"}

Click Submit. You will be prompted to set parameters:

![](media/image47.png){width="3.19034886264217in"
height="2.9384612860892387in"}

Here we are prompted with a list of all the application's parameters.
Change the values as you would like. For example, changing the
bus-agency to *ttc* (Toronto Transit Commission) will cause this
application to monitor buses in Toronto.

In the code, this list corresponds to the list of attributes in the
**param** clause:

![](media/image48.png){width="3.9in" height="0.757237532808399in"}

This application has one named parameter, `bus-agency`, whose default
value is `sf-muni`.

Application parameters are also called submission time values, because
they are specified at submission time. The `getSubmissionTimeValue`
function returns the user-specified value of a named parameter.

Tip: If there is no default value for a parameter, invoke
`getSubmissionTimeValue` with only one parameter:

![](media/image49.png){width="4.7461537620297465in"
height="0.6500612423447069in"}



Build vs. Build and Submit Job
------------------------------

To build an application, you must first compile it: Right click the SPL
file and choose **IBM Streams \> Build** or **IBM Streams \> Build and
Submit Job.**

**Build** and **Build and Submit Job** will both send the code to the
service for compilation.

-   Use **Build** to compile the application and save the executable
    file, called a SAB file, to your project.

This allows you to submit the application manually.

You need to submit the application manually when you want to specify a parameter at submission time.
Having the executable file saved locally also means you can relaunch the application whenever you need to, assuming you have not made any changes to the code. Of course, if you have changed the code, you will need to recompile.

-   Use **Build and Submit Job** to compile and submit the application
    for you. It does not download the executable SAB file to the local
    project.

Now that we have our application running, let's take a closer look at
it. From the Log Viewer, you can return to the main dashboard by
clicking Application Dashboard \> Open Dashboard \> Application
Dashboard.

![](media/image51.png){width="5.387416885389326in"
height="1.9794149168853894in"}

Stop a running application
--------------------------

Once you are finished with an application, stop it by clicking the
**Cancel** button from anywhere in the Streams console:

![](media/image55.png){width="3.015384951881015in"
height="0.7707053805774278in"}

Select the jobs to be cancelled and click Cancel Jobs:

![](media/image56.png){width="3.383885608048994in"
height="3.1953838582677165in"}

**Avoid leaving an application running on the Streaming Analytics
service so that you do not exceed the free computation limit and/or
incur additional charges. **
