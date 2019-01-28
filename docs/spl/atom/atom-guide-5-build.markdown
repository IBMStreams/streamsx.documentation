---
layout: docs
title:  Build and run an application from Atom
description:  Steps to build an applicaiton
navlevel: 2
tag: atom
prev:
  file: atom-guide-4-create
  title: Create a new SPL project in Atom
next:
    file: atom-guide-6-toolkits
    title: Add a toolkit to your application  
---

With the cloud based development using Atom, compilation and execution are all done in the cloud. From Atom, you can compile an SPL application using the
**Build** or **Build and submit job** actions:

  ![build-submit action](/streamsx.documentation/images/atom/jpg/build-submit.jpg)

If you choose **Build,** the application will be compiled and the resulting `.sab` (Streams Application Bundle) executable file will be saved to the `output` folder of your project. If you choose **Build and submit job**, the application will be compiled and executed in the cloud.

Let's look at an example.

About the sample application
----------------------------

The `BusAlerts` application displays alerts and advertisements within the city's public transit vehicles as they move through points of interest.

For example, if there is a security incident along a route, an alert is displayed inside the bus as the bus approaches the region. Also, advertisements for local businesses along a bus' route will be displayed as the bus approaches the business.

To follow along you can download the application if you haven't already [LINK]

Build the application
---------------------

In the **Project** pane, select the SPL file containing the composite you want to run.
  In our example, select **BusAlerts** \>**sample** \> **Main.spl**.
- Right click, and select **IBM Streams** \> **Build and submit job**.

Various alerts describing the progress of compilation will pop up:

  ![build-submit action](/streamsx.documentation/images/atom/jpg/build-progress.jpg)

View compile messages and errors
----------------------------------------------------

The Atom Console pane contains all information and error messages received from the Streaming Analytics service. Check this pane to view details of any errors that may occur during compilation.

Click **View > Toggle Console** and the console pane will appear:

  ![Atom console pane](/streamsx.documentation/images/atom/jpg/console-pane.jpg)

If an error occurs, see the [Troubleshooting section](atom-guide-7-problems) for help to resolve errors.

Run the application
-------------------

If you compiled using **Build and submit job**, you will receive an alert once compilation is successful:

  ![Streams console main](/streamsx.documentation/images/atom/jpg/submit-prompt.jpg)

_Submitting the job_ means launching the application on the Streaming analytics service.

Click **Submit** and the application will be launched for you. We will return to the **Submit via Console** option later.

View the running application in the Streams Console
---------------------------------------------------

Once the application is launched, you will be prompted to view the application in the Streams Console.

  ![Streams console prompt](/streamsx.documentation/images/atom/jpg/console-prompt.jpg)

Click **Open Streaming Analytics Console** to open the console in your browser.

Streams Console overview
------------------------

You can manage and observe your running applications from the Streams Console. You can start, restart and stop applications here, view log data, and observe metrics such as throughput or resource utilization.


![Streams console main](/streamsx.documentation/images/atom/jpg/console-main.jpg)

### Viewing the application's Logs

Let's start by looking at the output of the application. The application is simple; whenever it detects that a bus should receive an alert, it just prints the alerts.  We can take a look at the output by going to the **Log Viewer**, which is opened from the far left:

  ![open log viewer](/streamsx.documentation/images/atom/jpg/log-viewer.jpeg)


Then, expand the application, select the `AlertPrinter` operator, and click **Console Log**. Click **Reload** if no data appears.

  ![app logs](/streamsx.documentation/images/atom/jpg/operator-log.jpg)

Each line indicates the bus route, the business or area of interest, and the message that would be sent. For example, the first message would be to the N bus, stating that there is a security incident near Mission Dolores Park.

Launching an application with parameters
----------------------------------------

If you have an application and would like to specify a parameter at runtime, you cannot submit the application from Atom after compilation.

Submitting such an application from Atom would result in this message:
  ```
  CDISR1146E The following job submission parameter is required, but it is missing: sample::BusAlerts_Main.bus-agency.
  ```
Or this prompt:

  ![param missing prompt](/streamsx.documentation/images/atom/jpg/param-missing.jpeg)

It means the application requires you to specify a value for a parameter.
To specify application parameters, submit the application via the Streams Console.

### How to submit an application from Streams Console

1. Create an executable file using **Build**, and not **Build and submit job**. This will compile the application and place an executable file called `myapp.sab` file to your project's `output` directory.
2.  Open the Streams Console, and upload the `.sab` file.
3.  Set any needed parameters.


Let's continue with the example. In our case, our application has a parameter called `$agency`, which is set in the code:

  ![param](/streamsx.documentation/images/atom/jpg/param-default.png)

 We use this parameter to change our application to monitor buses in a different region.

 Its default value is `sf-muni`, so by default our application will monitor buses in the San Francisco Municipality.

 The default value also explains why we were able to submit the application the first time, because the parameter has a default value.

Our goal is setting the `$agency` parameter to _ttc_ when we submit the job.


### Use Build to create an executable
Select the SPL file, right click and click **Build**.

This will compile the application and save the executable file within the output folder of your project.

If the build is successful, you will see a new folder within the project containing the executable file:
  ![downloaded sab location](/streamsx.documentation/images/atom/jpg/sab-downloaded.jpg)

To launch the application, you can select the `.sab` file from the output folder and click **Submit job**.
    ![submit dialog atom](/streamsx.documentation/images/atom/jpg/sab-submit.jpeg)

You will again be prompted to submit the application, but this time, choose **Submit via Console**.

  ![Streams console main](/streamsx.documentation/images/atom/jpg/sab-submit-dark.jpeg)


This will open the Streams Console in your browser.


Submit a job from Streams console
-------
From the Console, click the **Submit job** button to submit a job.

  ![submit new job](/streamsx.documentation/images/atom/jpg/submit-play.jpeg)

Click **Browse** in the dialog that pops up.  Select the `.sab` file from the output folder of your project.

  ![Browse to sab](/streamsx.documentation/images/atom/jpg/submit-console.jpeg)

**Tip**: The path to the file is printed in the Atom Console, so you can copy and paste it. Use `CMD+SHIFT+G` on a Mac.

  ![Console URL](/streamsx.documentation/images/atom/jpg/console-url.jpeg)

Click **Submit**. You will be prompted with a list of all the application's parameters.

  ![Parameter prompt](/streamsx.documentation/images/atom/jpg/params-in-console.jpeg)

Change the values as you would like. For example, changing the `bus-agency` to _ttc_ (Toronto Transit Commission) will cause this application to monitor buses in Toronto.


##### Setting parameters summary

Application parameters are also called submission time values, because they are specified at submission time. The `getSubmissionTimeValue` function returns the user-specified value of a named parameter.


Stop a running application
--------------------------

**Avoid leaving an application running on the Streaming Analytics service so that you do not exceed the free computation limit and/or incur additional charges.**

Once you are finished with an application, stop it by clicking the
**Cancel** button from anywhere in the Streams console:

  ![Streams console main](/streamsx.documentation/images/atom/jpg/cancel.jpeg)

Select the jobs to be cancelled and click Cancel Jobs:

  ![Streams console main](/streamsx.documentation/images/atom/jpg/cancel-dialog.jpeg)


# Next steps

The next section will discuss adding functionality to your application by downloading and using toolkits.
