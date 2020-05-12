---
layout: docs
title:  Run your first IBM Streams application with Streams Studio
description:  Learn how to get started with IBM Streams
weight:  50
published: true

next:
  file: qse-development-2
  title: Overview of Streams concepts
---

After downloading and installing the Quick Start Edition (QSE), you are ready to compile and run an application using Streams Studio.

This is a good way to get familiar with the environment.

Run your first Streams application using Streams Studio, by following these steps.

## Launch Streams Studio

**If you are using the Docker QSE:**

  * [Start a VNC session](http://localhost:4000/streamsx.documentation/docs/4.3/qse-install-docker/#vnc).
  
  * Launch Streams Studio:
    * Click the Streams Studio by clicking **Applications** > **Streams Studio**   from the desktop.
      <img alt="launch studio" src="/streamsx.documentation/images/qse/StartStudio.jpg"/>

    * Pick a workspace when prompted, such as `/home/streamsadmin/workspaces/quickstart`.
      <img alt="launch studio" src="/streamsx.documentation/images/qse/Workspace.png"/>
    * Click **OK**.
  
    * Streams Studio should open. Accept the default installation location in the **Edit installation location** dialog. 
  
    * In the **Add Streams Domain Connection** dialog, click **Find Domain** and select the default domain, as shown below:
    
      <img alt="launch studio" src="/streamsx.documentation/images/qse/SelectDomain.gif"/>



**If you are using the Native Streams installation:**
  
  * [Install and launch Streams Studio](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.install.doc/doc/tinstall-studio-linux.html)


When Streams Studio is finished loading, it looks like this:

<img src="/streamsx.documentation/images/spl_lab_1/explore-streams-2nd-image-dwc009.png" width="100%" height="100%"/>

The various panes are highlighted.


## Import the sample application

The application we will use is called **TradesAppCloud** in the **TradesApp** project. It processes a stream of stock quotes for various companies, each identified by a ticker.
It computes the rolling average price for each unique stock ticker and prints it to standard out.

1. From the QSE, open a browser and download [the sample application project](https://streams-github-samples.mybluemix.net/?get=QuickStart%2FTradesApp).

2. From Streams Studio, import the project:
   1. Click **File** > **Import..**
   2. In the dialog that appears, select **General** > **Existing Projects into Workspace**. Click **Next**.
   3. Make sure **Select archive file** is selected, then click **Browse**, and navigate to the location of the zip file you downloaded. 
   4. Click **Finish**.
3. After the project is imported, it will complile automatically. This might take a few seconds. In the **Console** pane you should see a message like `---- SPL Build for project TradesApp completed in 70.366 seconds ----`.

<img alt="build complete" src="/streamsx.documentation/images/qse/build.jpg"/>

### Compiling the application

If the application does not compile automatically, or if you wish to recompile it, you need to create a build configuration. Build configurations are used to compile SPL applications.

This project should already have a build configuration: In the Project Explorer, expand the **TradesApp** project. Expand the **application** node, expand the  **TradesAppCloud** node, which is the main application we will be running.

<img alt="build complete" src="/streamsx.documentation/images/qse/build-config.jpg"/>

As shown in the image there should be an item called *BuildConfig* in the project. This is the build configuration.

Select the build configuration and click **Build** from the context menu. The **TradesAppCloud** application should now compile.

If a build configuration does not already exist, select the **TradesAppCloud** node, click **New** > **Build Configuration** from the context menu, accept the defaeults and click **OK**. 

## Run the application

Now that the application is built, you can run it in the following ways:
- [locally as a standalone application, meaning it is executed as a single process](#standalone)
- As a distributed application:
  -  [in the Streams instance in the Quick Start Edition](#dist),
  -  [On a Streams instance in IBM Cloud Pak for Data](#cpd).


<a id="standalone"></a>

### Option 1: Run the application as a standalone application 

Now you're ready to launch the application. 

You can run the application as a standalone application, meaning it will not be distributed across processes but will be a single process. This is useful for debugging and testing. 

In the Project Explorer, expand the **TradesApp** project. Expand the **application** node, right-click **TradesAppCloud**. Select **Launch** \> **Launch Active Build Config as Standalone**.

<img alt="launch app" src="/streamsx.documentation/images/qse/launch.jpg"/>

In the **Edit Configuration** dialog, click **Launch**.

The application should start running and the Console should show its output. You should see this:

```
Average asking price for NNN  is 20.8
Average asking price for PG  is 58.72
Average asking price for PNR  is 34.918
```

Each stock is represented by a ticker, e.g. `PNR`. Each line in the output reports the computed average price for the indicated stock.

<img alt="app output" src="/streamsx.documentation/images/qse/console.jpg"/>

Click the terminate button in the Console pane to stop the application.

<img alt="app output" src="/streamsx.documentation/images/qse/terminate.jpg"/>


<a id="dist"></a>

### Option 2: Run the application as distributed application on the local Streams instance

Now, let's try deploying the application on the Streams instance.

Return to thhe Project Explorer, expand the **TradesApp** project. Expand the **application** node, right-click **TradesAppCloud**, but this time select **Launch** \> **Launch Active Build Config To Running Instance**. 

In the **Edit Configuration** dialog, click **Apply**, and then click **Launch**.\

In the **Console** view, click the **Display Selected Console** button on the right to switch consoles to the Streams Studio Console.\
\
![](/streamsx.documentation/images/spl_lab_1/lab1step8-3dwc009.png)

You should see some output like: `Submitted: StreamsInstance@StreamsDomain job id: 1 name: application::TradesAppCloud_1`.


This shows that a new application was submitted to the instance.  A running Streams application is called a *job*.


## View the running application in Streams Studio

After launching the application in distributed mode, follow these steps to view the running application. 

1. Switch to the **Streams Explorer**, which is the second tab in the view on the left, behind the Project Explorer.
2. Expand the **StreamsInstances** folder, and right-click the **default@StreamsInstance** instance and choose **Show instance graph**.

<img alt="app output" src="/streamsx.documentation/images/qse/graph.jpg"/>

A new view called the **Instance Graph** should open.  This view shows a graph that represents the application we launched. Streams applications are really directed graphs that analyze data as it is processed. Each node in the graph is an **operator** that processes data, and each arrow represents a **stream** of live data. Don't worry about the colors on each node for now.

<img alt="app output" src="/streamsx.documentation/images/qse/graph-view.jpg"/>



This view shows all the running applications in the instance, so if you were to launch this application again, it would shortly appear in the graph. 


### Observe the data flowing through the application in real time

You can look at the data on a given Stream to observe the data that is being processed or produced by an operator. For example, the **Quotes** operator
produces a stream of stock quotes. Let's take a look at the data.

Select the stream that comes out of the **Quotes** operator, right-click and click **Show Data**.
Accept the default attributes in dialog that appears and you should soon see a second view showing the tuples in the stream produced by the **Quotes** operator. 

<img alt="app output" src="/streamsx.documentation/images/qse/showdata.gif"/>

### View Job Logs

The application prints output to standard out. This output, errors and trace data are all sent to the logs. To view an operator's logs, select the operator and click **Show Log**.

The output is genertaed by the **PrintAvPrice** operator, the last operator in the graph.
To view the printed output, select the **PrintAvPrice** operator in the **Instance Graph**, right click it, and click **Show Log** > **Show all PE Logs**.

The logs for the operator will be retrieved and displayed.

## Cancel the Job

Select the job in the **Instance Graph**, right click, and select **Cancel Job**.

<img alt="cancel job" src="/streamsx.documentation/images/qse/cancel.jpg"/>

[Skip to the conclusion](#summary).

<a id="cpd"></a>

### Option 3: Run the application on a Streams instance in IBM Cloud Pak for Data
If you have a Streams instance in IBM Cloud Pak for Data or in Kubernetes/OpenShift, the steps to launch the application are different. 

To launch the application:
- Compile the application as shown above.
- Instead of launching it to the local instance, you need to submit the application manually using the Streams Console.

#### Launch the application using the Streams Console

1. You need to get the URL of the Streams Console for your Streams instance. 
   - **Find the URL for Streams add-on in IBM Cloud Pak for Data:**
     - From the navigation menu, click <strong>My instances</strong>.
     - Click the <strong>Provisioned Instances</strong> tab.
     - Find your Streams instance, and click **View details** from the context menu. Open the URL under **External console endpoint**.
       
   - **Find the URL for Streams stand-alone deployment:** [See the documentation](https://www.ibm.com/support/knowledgecenter/en/SSCRJU_5.2.0/com.ibm.streams.dev.doc/doc/find-dns-url.html#find-dns-url). Choose *finding the internal URL*  or *finding the external URL* depending on whether or not you will be accessing the Streams Console from within the Kubernetes cluster.


2. From the Streams Console, click **Submit job**:
  <br/>
![submit job](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/11/streams-submit-job.png)

   * Browse to the location of the compiled application.  This will be a `.sab` file in the `output` folder of your project.
   * Set any parameters, and submit the application.

You should see a popup like this once submission is successfull:

<img alt="job success" src="/streamsx.documentation/images/qse/submit-console.png"/>

Notice that a running Streams application is called a *job*.

Keep these steps in mind for submitting applications for IBM Cloud Pak for Data when developing with Streams Studio.

## View the running application in Cloud Pak for Data

After launching the application in the Streams Console you can go to the Job Graph in Cloud Pak for Data to view the running application. 

1. From the main menu, go to **My Instances** > **Jobs**. This will bring you to the list of jobs.
2. Find your job in the list  based on its name, and from the context menu of the job, click **View job graph**.

A new page called the Job Graph should open. 
This shows a graph that represents the application we launched. Streams applications are really directed graphs that analyze data as it is processed. Each node in the graph is an **operator** that processes data, and each arrow represents a **stream** of live data. 

<img alt="job graph in cpd" src="/streamsx.documentation/images/qse/graph-cpd.jpg"/>



### Observe the data flowing through the application in real time

You can look at the data on a given Stream to observe the data that is being processed or produced by an operator. For example, the **Quotes** operator produces a stream of stock quotes. Let's take a look at the data.

Select the stream that comes out of the **Quotes** operator, right-click and click **View Data** > **Create new view**.

A new pane will appear that shows the data in the stream produced by the **Quotes** operator.  Notice that the view is processed as new data arrives.

<img alt="view data in cpd" src="/streamsx.documentation/images/qse/showdata-cpd.gif"/>


### View logs

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
-  Download logs from a running job.

The next section will cover basic Streams concepts. You will also learn how to create this same application.


### References
- Streams studio documentation
- Streams in Cloud Pak for Data documentation