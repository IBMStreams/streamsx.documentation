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

With the cloud-based development using Atom, compilation and execution are all done in the cloud. From Atom, you can compile an SPL application by using the **Build** or **Build and submit job actions**:

![build-submit action](/streamsx.documentation/images/atom/jpg/build-submit.png)

If you choose **Build**, the application is compiled and the resulting `.sab` (Streams Application Bundle) executable file is saved to the output folder of your project. If you choose **Build and submit job**, the application is compiled and executed in the cloud.

Here is an example.

About the sample application
----------------------------

The `BusAlerts` application displays alerts and advertisements inside the city's public transit vehicles as they move through points of interest.

For example, if there is a security incident an alert about the incident is displayed inside the bus as the bus approaches the region.  Local businesses can also purchase advertising to be displayed when the bus is near the business. To follow along, [download the sample application](https://streams-github-samples.mybluemix.net/?get=QuickStart%2FBusAlerts) if you haven't already.

Build the application
---------------------

In the **Project** pane, select the SPL file containing the composite you want to run. In our example, select **BusAlerts > my.name.space > BusAlerts_CachedData.spl**.

Right-click, and select **IBM Streams > Build and submit job**.

Various alerts that describe the compilation progress are displayed:

![build-progress action](/streamsx.documentation/images/atom/jpg/build-progress.jpg)

View compile messages and errors
----------------------------------------------------

The Atom Console pane contains all information and error messages rece1ived from the Streaming Analytics service. Check this pane to view details of any errors that might occur during compilation.

Click **View > Toggle Console** and the console pane appears:

![Atom console pane](/streamsx.documentation/images/atom/jpg/console-pane.jpg)

If an error occurs, see the [Troubleshooting section](atom-guide-7-problems) for help to resolve errors.

Run the application
-------------------


If you compiled the application by using the **Build and submit job** option, you will receive an alert after compilation completes successfully. From the alert, you can submit the job.

![Streams console main](/streamsx.documentation/images/atom/jpg/submit-prompt.jpg)

_Submitting the job_ means launching the application on the Streams instance in the cloud.

Click **Submit** and the application is be launched for you. You can also use the **Submit via Console** option if you need to configure your application before submitting. The **Submit via Console** option is discussed later on.

View the running application in the Streams Console
---------------------------------------------------

After the application is launched, you are prompted to view the application in the Streams Console.

![Streams console prompt](/streamsx.documentation/images/atom/jpg/console-prompt.jpg)

Click **Open Streaming Analytics Console** to open the console in your browser.

Streams Console overview
------------------------

You can manage and observe your running applications from the Streams Console. You can start, restart, and stop applications here. You can also view log data and observe metrics such as throughput or resource utilization.

![Streams console main](/streamsx.documentation/images/atom/jpg/console-main.jpg)

### Viewing the application's Logs

Start by looking at the output of the application. For the bus application, whenever a bus should receive an alert, it just prints the alerts. Take a look at the output by going to the **Log Viewer**, which is opened from the menu options on the left.

![open log viewer](/streamsx.documentation/images/atom/jpg/log-viewer.jpg)

Next, expand the application, select the `AlertPrinter` operator, and click **Console Log**. Click **Reload** if no data appears.

![app logs](/streamsx.documentation/images/atom/jpg/operator-log.jpg)

Each line indicates the bus route, the business or area of interest, and the message that would be sent. For example, the first message would be to the N bus, stating that there is a security incident near Mission Dolores Park.

Launching an application with parameters
----------------------------------------

If you have an application and would like to specify a parameter at runtime, you cannot submit the application from Atom after compilation.


Submitting such an application from Atom without the runtime parameter results in the following message or prompt:

  ```
  CDISR1146E The following job submission parameter is required, but it is missing: sample::BusAlerts_Main.bus-agency.
  ```

The message means that you must specify a value for a parameter. To specify application parameters, use the Streams Console to submit the application.

Submit an application from Streams Console
------------------------------------------
The general steps to submit your application from Streams console are described in this video:

<iframe width="560" height="315" src="https://www.youtube.com/embed/0gDxeByDO5E" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>
</iframe>


As shown in the video, the steps are as follows:

1.	Create an executable file by using the **Build** option rather than the **Build and submit job** option. This option compiles the application and places an executable file called `myapp.sab` file in your project’s output directory.
2.  Open the Streams Console, and upload the `myapp.sab` file.
3.  Set any needed parameters.

In this case, your application has a parameter called `$agency`, which is set in the code.

![param](/streamsx.documentation/images/atom/jpg/param-default.png)

Use this parameter to change the application to monitor buses in a different regions.

The default value is `sf-muni`, so by default our application monitors buses in the San Francisco Municipality. Your goal is to set the `$agency` parameter to _ttc_, for Toronto Transit Commission. Using this value will change the application  to monitor buses in Toronto instead of San Francisco.

### Use Build to create an executable
Right-click the SPL file and click **Build**.

This option compiles the application and saves the executable file to the output folder of your project.

If the build is successful, you will see a new folder within the project that contains the executable file.

![downloaded sab location](/streamsx.documentation/images/atom/jpg/sab-downloaded.jpg)

To launch the application, you can right click the `.sab` file from the output folder and click **Submit job**.

![submit dialog atom](/streamsx.documentation/images/atom/jpg/sab-submit.jpg)

When you are prompted to submit the application, choose **Submit via Console.**
  ![Streams console main](/streamsx.documentation/images/atom/jpg/sab-submit-dark.jpg)


This option opens the Streams Console in your browser.

### Submit a job from Streams console
From the console, click the **Submit job** to submit a job.

![submit new job](/streamsx.documentation/images/atom/jpg/submit-play.jpg)

In the **Submit Job** window, click **Browse**. Select the .sab file from the output folder of your project.

![Browse to sab](/streamsx.documentation/images/atom/jpg/submit-console.jpg)

**Tip**: The path to the file is printed in the Atom Console, so you can copy and paste it.

![Console URL](/streamsx.documentation/images/atom/jpg/console-url.jpg)

Click **Submit**. The application parameters are displayed.

  ![Parameter prompt](/streamsx.documentation/images/atom/jpg/params-in-console.jpg)


**Note**: because the `bus-agency` parameter has a default value, `sf-muni` we were able to submit the application the first time. When you use the **Build and submit** option and then submit directly from Atom, the default values for any parameters are used, if there are no default values for some parameters the submission will fail.


##### Setting parameters summary

* To set a parameter value when submitting an application, you must use the Streams Console to submit the application.

* To add a parameter to your application that will be set when you submit the job, use the `getSubmissionTimeValue` function to add a named parameter.

Stop a running application
--------------------------

**Important**: If you are using the Streaming Analytics service in IBM cloud, avoid leaving an application running unnecessarily to avoid exceeding the free computation limit and incurring additional charges

When you are finished with an application, stop it by clicking the **Cancel** button from anywhere in the Streams console.

![Streams console main](/streamsx.documentation/images/atom/jpg/cancel.jpg)

Select the jobs to be canceled and click **Cancel Jobs**.

![Streams console main](/streamsx.documentation/images/atom/jpg/cancel-dialog.jpg)


# Next steps

The next section discusses adding functionality to your application by downloading and using toolkits.
