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

When developing Streams applications by using Atom, the application is compiled and executed in the cloud. From Atom, you can compile an SPL application using the **Build** or **Build and submit job** actions.

![build-submit action](/streamsx.documentation/images/atom/jpg/build-submit.jpg)

If you choose **Build,** the application will be compiled and the resulting `.sab` (Streams Application Bundle) file will be saved to the `output` folder of your project. If you choose **Build and submit job**, the application will be compiled and you will be prompted to submit the job to be run in the cloud.

Here is an example.

About the sample application
----------------------------

The `BusAlerts` application displays alerts and advertisements within the city's public transit vehicles as they move through points of interest. For example, if there is a security incident, or if a participating local business is nearby, an alert about the incident or an ad for the business is displayed inside the bus as the bus approaches the region. To follow along you can download the application if you haven't already. [LINK TBD]

Build the application
---------------------

In the **Project** pane, select the SPL file containing the composite you want to run. In our example, select **BusAlerts > sample > Main.spl**. Then right click, and select **IBM Streams > Build and submit job**. As your application is building you will see various alerts describing the progress of compilation.

![build-progress action](/streamsx.documentation/images/atom/jpg/build-progress.jpg)

View compile messages and errors
----------------------------------------------------

The Atom Console pane contains all information and error messages rece1ived from the Streaming Analytics service. Check this pane to view details of any errors that may occur during compilation. To open the console pane, in the menu bar of Atom click **View > Toggle Console**.

![Atom console pane](/streamsx.documentation/images/atom/jpg/console-pane.jpg)

If an error occurs, see the [Troubleshooting section](atom-guide-7-problems) for help to resolve errors.

Run the application
-------------------

If you compiled using **Build and submit job**, you will receive an alert once compilation is successful

![Streams console main](/streamsx.documentation/images/atom/jpg/submit-prompt.jpg)

_Submitting the job_ means launching the application on the Streaming analytics service.

Click **Submit** and the application will be launched for you. You can also use the **Submit via Console** option if you need to configure your application before submitting. The **Submit via Console** option is discussed later on.

View the running application in the Streams Console
---------------------------------------------------

Once the application is launched, you will be prompted to view the application in the Streams Console.

![Streams console prompt](/streamsx.documentation/images/atom/jpg/console-prompt.jpg)

Click **Open Streaming Analytics Console** to open the console in your browser.

Streams Console overview
------------------------

You can manage and monitor your running applications from the Streams Console. You can start, restart and stop applications here, view log data, and observe metrics such as throughput or resource utilization.

![Streams console main](/streamsx.documentation/images/atom/jpg/console-main.jpg)

### Viewing the application's Logs

You can start by looking at the output of the application. For the bus application, whenever a bus should receive an alert, it just prints the alerts. We can take a look at the output by going to the **Log Viewer**, which is opened from the menu options on the left.

![open log viewer](/streamsx.documentation/images/atom/jpg/log-viewer.jpg)

Then, expand the application, select the `AlertPrinter` operator, and click **Console Log**. Click **Reload** if no data appears.

![app logs](/streamsx.documentation/images/atom/jpg/operator-log.jpg)

Each line indicates the bus route, the business or area of interest, and the message that would be sent. For example, the first message would be to the N bus, stating that there is a security incident near Mission Dolores Park.

Launching an application with parameters
----------------------------------------

If you have an application and would like to specify a parameter at runtime, you cannot submit the application from Atom after compilation.

Submitting such an application from Atom would result in the following message
  ```
  CDISR1146E The following job submission parameter is required, but it is missing: sample::BusAlerts_Main.bus-agency.
  ```
which tell you that the application requires you to specify a value for a parameter.
To specify application parameters, submit the application via the Streams Console.

Submit an application from Streams Console
------------------------------------------
The general steps to submit your application from Streams console is as follows:

1. Create an executable file using **Build**, and not **Build and submit job**. This will compile the application and place an executable file called `myapp.sab` file to your project's `output` directory.
2.  Open the Streams Console, and upload the `.sab` file.
3.  Set any needed parameters.

Continuing with the bus application, your application has a parameter called `$agency`, which is set in the code.

![param](/streamsx.documentation/images/atom/jpg/param-default.png)

 This parameter changes the application to monitor buses in a different regions. The default value is `sf-muni`, so by default our application monitors buses in the San Francisco Municipality. The default value also explains why we were able to submit the application the first time. When you use the **Build and submit** option and then submit directly from Atom, the default values for any parameters are used, if there are no default values for some parameters the submission will fail. Your goal is setting the `$agency` parameter to _ttc_ when you submit the job.

### Use Build to create an executable
In order to create the executable file, select the SPL file that contains your application, right click, and click **Build**. This will compile the application and save the executable file to the **output** folder of your project. If the build is successful, you will see a new folder within the project containing the following executable file.

![downloaded sab location](/streamsx.documentation/images/atom/jpg/sab-downloaded.jpg)

To launch the application, you can right click the `.sab` file from the output folder and click **Submit job**.

![submit dialog atom](/streamsx.documentation/images/atom/jpg/sab-submit.jpg)

You will again be prompted to submit the application, but this time, choose **Submit via Console**.

  ![Streams console main](/streamsx.documentation/images/atom/jpg/sab-submit-dark.jpg)


This will open the Streams Console in your browser.


### Submit a job from Streams console
From the Console, click the **Submit job** button to submit a job.

![submit new job](/streamsx.documentation/images/atom/jpg/submit-play.jpg)

Click **Browse** in the dialog that pops up.  Select the `.sab` file from the output folder of your project.

![Browse to sab](/streamsx.documentation/images/atom/jpg/submit-console.jpg)

**Tip**: The path to the file is printed in the Atom Console, so you can copy and paste it. Use `CMD+SHIFT+G` on a Mac.

![Console URL](/streamsx.documentation/images/atom/jpg/console-url.jpg)

Click **Submit**. You will be prompted with a list of all the application's parameters.

  ![Parameter prompt](/streamsx.documentation/images/atom/jpg/params-in-console.jpg)

You can change the `bus-agency` parameter to _ttc_ (Toronto Transit Commission) will cause this application to monitor buses in Toronto.

##### Setting parameters summary

Application parameters are also called submission time values, because they are specified at submission time. The `getSubmissionTimeValue` function returns the user-specified value of a named parameter.

Stop a running application
--------------------------

**Avoid leaving an application running on the Streaming Analytics service so that you do not exceed the free computation limit and/or incur additional charges.**

Once you are finished with an application, stop it by clicking the **Cancel** button from anywhere in the Streams console.

![Streams console main](/streamsx.documentation/images/atom/jpg/cancel.jpg)

Select the jobs to be cancelled and click Cancel Jobs.

![Streams console main](/streamsx.documentation/images/atom/jpg/cancel-dialog.jpg)


# Next steps

The next section will discuss adding functionality to your application by downloading and using toolkits.
