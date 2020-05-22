---
layout: docs
title:  Run your first IBM Streams application with Streams Studio
description:  Learn how to get started with IBM Streams
weight:  30
published: true
tag: spl-qs
navlevel: 2
prev:
  file: qs-1
  title: Run your first application
next:
  file: qs-2
  title: Overview of Streams concepts
---

After [downloading and installing the Streams Quick Start Edition (QSE)](/streamsx.documentation/docs/4.3/qse-intro), you are ready to compile and run an application using Streams Studio.

This is a good way to get familiar with the environment.

In this tutorial, you'll learn how to:

-  Import a project into Streams Studio
-  Compile the application
-  Launch it as a standalone, or distributed application.
-  View the data on a stream
-  Download logs from a running application, which is called a job.

## Launch Streams Studio

Launching instructions depend on how you installed the Streams QSE. Following are instructions if you installed the Docker image or if you used a native installation of the QSE.

### Docker QSE users

  {: .simple}

  * [Start a VNC session](http://localhost:4000/streamsx.documentation/docs/4.3/qse-install-docker/#vnc).
  
  * Launch Streams Studio:
    * Click the Streams Studio by clicking **Applications** > **Streams Studio**   from the desktop.
      <img alt="launch studio" src="/streamsx.documentation/images/qse/StartStudio.jpg"/>

    * Pick a workspace when prompted, such as `/home/streamsadmin/workspaces/quickstart`.
      <img alt="launch studio" src="/streamsx.documentation/images/qse/Workspace.png"/>
    * Click **OK**.
  
    * Streams Studio should open. Accept the default installation location in the **Edit installation location** dialog. 
  
    * In the **Add Streams Domain Connection** dialog, click **Find Domain** and select the default domain, as shown in this diagram:
    
      <img alt="launch studio" src="/streamsx.documentation/images/qse/SelectDomain.gif"/>



### Users with a Native Streams installation 

  {: .simple}

  - Follow the instructions in the documentation to [install and launch Streams Studio](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.install.doc/doc/tinstall-studio-linux.html)


## Import the sample application


The application we will use is called **TradesAppCloud** in the **TradesApp** project. It processes a stream of stock quotes for various companies, each identified by a ticker.
It computes the rolling average price for each unique stock ticker and prints it to standard out.

1. From the QSE, open a browser and download the sample application project using this URL: `https://streams-github-samples.mybluemix.net/?get=QuickStart%2FTradesApp`

2. From Streams Studio, import the downloaded project:
   1. Click **File** > **Import..**
   2. In the dialog that appears, select **General** > **Existing Projects into Workspace**. Click **Next**.
   3. Make sure **Select archive file** is selected, then click **Browse**, and navigate to the location of the zip file you downloaded. 
   4. Click **Finish**.
3. After the project is imported, it will complile automatically. This might take a few seconds. In the **Console** pane you should see a message like `---- SPL Build for project TradesApp completed in 70.366 seconds ----`.

<img alt="build complete" src="/streamsx.documentation/images/qse/build.jpg"/>

## Compiling the application

The application should compile automatically, but here are steps to compile it if that does not happen.

You need a build configuration to compile SPL applications in Streams Studio. 

This project should already have a build configuration: In the Project Explorer, expand the **TradesApp** project and then expand the **application** node, and the  **TradesAppCloud** node under it.

The **TradesAppCloud** node represents the main application we will be running.

<img alt="build complete" src="/streamsx.documentation/images/qse/build-config.jpg"/>

As shown in the image there should be an item called *BuildConfig* in the project. This is the build configuration.

Select the build configuration and click **Build** from the context menu. The **TradesAppCloud** application should now compile.

Compiling will generate a few artifacts in the `output` folder.  The most important of these is the Streams Application Bundle, (SAB) file. This is an executable file in the `output/application.TradesAppCloud/BuildConfig` folder with a `.sab` extension.  Next we will launch the application.

## Run the application

Now that the application is built, you can run it in the following ways:

- [locally as a standalone application, meaning it is executed as a single process](#standalone)
- As a distributed application:
  -  [in the Streams instance in the Quick Start Edition](#dist),
  -  [On a Streams instance in IBM Cloud Pak for Data](#cpd).


<a id="standalone"></a>

## Option 1: Run the application as a standalone application 

This means that you run the application as a single process. This is useful for debugging and testing. 

In the Project Explorer, expand the **TradesApp** project. Expand the **application** node, right-click **TradesAppCloud**. Select **Launch** \> **Launch Active Build Config as Standalone**.

<img alt="launch app" src="/streamsx.documentation/images/qse/launch.jpg"/>

In the **Edit Configuration** dialog, click **Launch**.

Streams Studio will locate the SAB file and launch it for you.

The application should start running and the Console view will show its output. You should see this:

```
Average asking price for NNN  is 20.8
Average asking price for PG  is 58.72
Average asking price for PNR  is 34.918
```

Each stock is represented by a ticker, e.g. `PNR`. Each line in the output reports the computed average price for the indicated stock.

Click the terminate button in the Console pane to stop the application.


<img alt="app output" src="/streamsx.documentation/images/qse/terminate.jpg"/>


<a id="dist"></a>

## Option 2: Run as a distributed application on the local Streams instance

Now, let's try deploying the application on the Streams instance.

Return to thhe Project Explorer, expand the **TradesApp** project. Expand the **application** node, right-click **TradesAppCloud**, but this time select **Launch** \> **Launch Active Build Config To Running Instance**. 

In the **Edit Configuration** dialog, click **Apply**, and then click **Launch**.

Streams Studio will send the executable SAB file to the Streams instance for execution.

You can observe this in the **Console** view. Click the **Display Selected Console** button on the right to switch consoles to the Streams Studio Console.\
\
![](/streamsx.documentation/images/spl_lab_1/lab1step8-3dwc009.png)

You should see some output like: `Submitted: StreamsInstance@StreamsDomain job id: 1 name: application::TradesAppCloud_1`.


This shows that a new application was submitted to the instance.  A running Streams application is called a *job*.


### View the running job in Streams Studio

After launching the application in distributed mode, follow these steps to view the running application. 

1. Switch to the **Streams Explorer**, which is the second tab in the view on the left, behind the Project Explorer.
2. Expand the **StreamsInstances** folder, and right-click the **default@StreamsInstance** instance and choose **Show instance graph**.

<img alt="app output" src="/streamsx.documentation/images/qse/graph.jpg"/>

A new view called the **Instance Graph** should open.  This view shows a graph that represents the application we launched. Streams applications are really directed graphs that analyze data as it is processed. Each node in the graph is an **operator** that processes data, and each arrow represents a **stream** of live data. Don't worry about the colors on each node for now.

<img alt="app output" src="/streamsx.documentation/images/qse/graph-view.jpg"/>



This view shows all the running applications in the instance, so if you were to launch this application again, it would shortly appear in the graph. 


### Observe the data flowing through the job in real time

You can look at the data on a given Stream to observe the data that is being processed or produced by an operator. For example, the **Quotes** operator
produces a stream of stock quotes. Let's take a look at the data.

- Select the stream that comes out of the **Quotes** operator, right-click, and click - **Show Data**.
- Accept the default attributes in dialog that appears and you should soon see a second view showing the tuples in the stream produced by the **Quotes** operator. 

The following animation shows the sequence of steps.

<img alt="app output" src="/streamsx.documentation/images/qse/showdata.gif"/>

### View job logs


All application output, including messages printed to standard out, errors and trace data are sent to the logs. To view an operator's logs, select the operator and click **Show Log**.

In this application, the output is generated by the **PrintAvPrice** operator.

To view the printed output, select the **PrintAvPrice** operator in the **Instance Graph**, right click it, and click **Show Log** > **Show all PE Logs**.

The logs for the operator will be retrieved and displayed.

<img alt="application logs" src="/streamsx.documentation/images/qse/logs.jpg"/>

[Skip to the conclusion](#summary).

<a id="cpd"></a>

## Option 3: Run on a Streams instance in IBM Cloud Pak for Data

If you have a Streams instance in IBM Cloud Pak for Data or in Kubernetes/OpenShift, the steps to launch the application are different. 

As mentioned earlier, compiling the application creates an executable called a Streams Application Bundle (SAB) file. To run the application on Cloud Pak for Data, you need need to upload the application using the Streams Console.

### Launch the application using the Streams Console

{%  include qs/open-streams-console.md %}


Next, from the Streams Console, click **Submit job**:
  <br/>
![submit job](/streamsx.documentation/images/qse/streams-submit-job.png)

   * Browse to the location of the compiled application.  This will be a `.sab` file in the `output` folder of your project.
   * Set any parameters, and submit the application.

You should see a popup like this once submission is successfull:

<img alt="job success" src="/streamsx.documentation/images/qse/submit-console.png"/>

Notice that a running Streams application is called a *job*.

Keep these steps in mind for submitting applications for IBM Cloud Pak for Data when developing with Streams Studio.

### View the running job in Cloud Pak for Data

After launching the application in the Streams Console you can go to the Job Graph in Cloud Pak for Data to view the running application. 

1. From the main menu, go to **My Instances** > **Jobs**. This will bring you to the list of jobs.
2. Find your job in the list  based on its name, and from the context menu of the job, click **View job graph**.

A new page called the Job Graph should open. 
This shows a graph that represents the application we launched. Streams applications are really directed graphs that analyze data as it is processed. Each node in the graph is an **operator** that processes data, and each arrow represents a **stream** of live data. 

<img alt="job graph in cpd" src="/streamsx.documentation/images/qse/graph-cpd.jpg"/>



### Observe the data flowing through the job in real time

You can look at the data on a given Stream to observe the data that is being processed or produced by an operator. For example, the **Quotes** operator produces a stream of stock quotes. Let's take a look at the data.

Select the stream that comes out of the **Quotes** operator, right-click and click **View Data** > **Create new view**.

A new pane will appear that shows the data in the stream produced by the **Quotes** operator.  Notice that the view is processed as new data arrives.

<img alt="view data in cpd" src="/streamsx.documentation/images/qse/showdata-cpd.gif"/>


### View job logs

The application prints output to standard out. This output, errors and trace data are all sent to the logs. To view an operator's logs, go back tto the list of jobs:  **My instances** > **Jobs**.

Find the job in the list and click **Download Logs** from the job's context menu:

<img alt="view data in cpd" src="/streamsx.documentation/images/qse/logs-cpd.png"/>


### Summary
You've just launched a Streams application using Streams studio. In the next section you will learn Streams concepts and how to create this application.

But first, cancel the running job.

## Cancel the job

In the job list, select **Delete** from the job's context menu.

<a id="summary"></a>

## Summary

In this section, you learned how to:

-  Import a project into Streams Studio
-  Compile the application
-  Launch it as a standalone, or distributed application.
-  View the data on a stream
-  Download logs from a running application, which is called a job.

You also created a new project and a new main composite, which will come in handy as you try to create the application you just ran in the next section.


### References
- [Streams Studio documentation](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.studio.doc/doc/studio-container.html)
 
- [Streams in Cloud Pak for Data documentation](https://www.ibm.com/support/producthub/icpdata/docs/content/SSQNUZ_current/cpd/svc/streams/developing-intro.html)