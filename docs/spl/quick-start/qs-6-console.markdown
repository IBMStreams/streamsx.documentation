---
layout: docs
title: Monitoring IBM Streams applications with Streams Console
description: How to use the Streams Console web application to monitor Streams applications
weight: 80
published: true
tag: spl-qs
navlevel: 2
prev:
  file: qs-4
  title:  Tips for development
---

The Streams Console is a web application that allows you to easily monitor and manage your Streams instance and jobs. You can quickly gain insights on the health, metrics, issues and performance of your applications and the systems they are running on.  

In Streams on Cloud Pak for Data, the Streams Console is a more advanced alternative to the Job Graph.  

This article describes the most common features and how to use them.  

*   [Opening the Streams Console](#open)
*   [Submitting a Job](#submit)
*   [View a sample of streaming data](#view)
*   [Monitoring a job](#monitor)
*   [Downloading logs](#logs)

<img alt="Screenshot of the Streams Console" src="/streamsx.documentation/images/qse/vs-code-streams-console-v5.png" height="600" width="1080"/>

_Streams Console_

<a id="open"></a>

## Opening the Streams Console

{% include spl/console/open_streams_console.html %}

### IBM Streams extension for Visual Studio Code

These instructions assume that you already have the [IBM Streams extension](https://marketplace.visualstudio.com/items?itemName=IBM.ibm-streams) for Visual Studio Code installed. If not, start [here](https://ibmstreams.github.io/streamsx.documentation/docs/spl/quick-start/qs-1b/#installation-and-setup) and follow the instructions.

1.  Click on the IBM Streams icon on the left side to bring up the **Streams Explorer** view.
2.  Hover over an instance node and then click on the **Open IBM Streams Console** icon that appears on the right. This will open the Streams Console in your browser.

<a id="submit"></a>

## Submitting a job

After opening the Streams Console, you can follow these steps to submit a job to run on your Streams instance. Streams applications are always compiled into a file with a `.sab` extension. SAB stands for Streams application bundle. This is a single, relocatable file that contains all the artifacts that are needed to run your application. Learn more about application bundle files [here](https://www.ibm.com/support/knowledgecenter/en/SSCRJU_4.3.0/com.ibm.streams.dev.doc/doc/applicationbundle.html).

So, when we say "submit a `.sab` file", we mean, run a compiled Streams application.

1.  Click on the play icon in the header bar at the top.  
    ![submit job](/streamsx.documentation/images/qse/streams-submit-job.png)
    
2.  Choose one of the options and point to your `.sab` file.
3.  To configure the job submission, click on the **Configure** button. To submit the job with the default configuration, click on the **Submit** button. [Learn more about job configuration here.](https://community.ibm.com/community/user/cloudpakfordata/viewdocument/configuring-job-submissions-using-s?CommunityKey=c0c16ff2-10ef-4b50-ae4c-57d769937235&tab=librarydocuments&LibraryFolderKey=43a572a8-f9f1-4a66-a4b3-ef2cd38af124&DefaultView=folder)

<a id="view"></a>

## View a sample of streaming data

You can look at the data on a given stream to observe the data that is being processed or produced by an operator.  

To observe the data, create a dashboard view:  

1.  In the **Application Dashboard**, find the **Streams Graph** card and expand it.
2.  Hover over the stream that comes out of an operator and right-click.
3.  Select **Create Dashboard View**.
4.  Accept the default options and click on the **OK** button.
5.  Minimize the **Streams Graph** card.
6.  A new card is created in the dashboard that displays the tuples in the stream produced by the operator. Notice that the view is updated as new data arrives.

These steps are demonstrated in the following animation.  

<img alt="animation showing how to create a view" src="/streamsx.documentation/images/vs-code/vs-code-streams-console-view-v5.gif" width="110%" height="110%"/>

<div style="text-align: center;"><em>Creating a view on a stream</em></div>

<a id="monitor"></a>

## Managing and Monitoring Jobs

You can hover over an operator, a job, or a Stream to see available actions. You can perform actions like:  

*   Set application trace
*   Restart PEs,
*   Submit job
*   View PE restart recommendations
*   Download operator and PE logs
*   Modify parallel regions

<img src="/streamsx.documentation/images/qse/operator-actions.png" alt="operator actions" height="100%" width="100%"/> 

### Adding Metric/Health charts and grids:

Monitor metrics and health through various configurable charts like pie charts, bar charts, scatter charts, etc and grids.  

**How to do** **it:**
1. Click **Add card** in the console  
    <img src="/streamsx.documentation/images/qse/add-card-action.png" alt="add card action" height="60%" width="60%"/>

2. In **Visualization Settings** tab, choose a type of metric, e.g PE memory consumption, and in the **Card Properties,** select the type of graph, e.g. bar chart.  

    <img src="/streamsx.documentation/images/qse/add-card.png" alt="add card dialog" height="80%" width="80%"/>

<a id="logs"></a>

## Download and View Logs

Analyze application trace, product and console logs through a reader friendly viewer.  

**How to use it:**

1. Open the log viewer from the far right pane of the Streams Console.

   ![open log viewer](/streamsx.documentation/images/qse/log-viewer.png)

2. Select the job of interest. Expanding the tree and selecting an operator or PE will open the logs pane. Click any of the tabs: Application trace, Console log or Product log to show trace data, messages printed to standard out, and product logs, respectively  
<img src="/streamsx.documentation/images/qse/logs-console.png" alt="data in log viewer" height="90%" width="90%"/>


### Streams Graph

This is a graphical view of your Streams Application which shows flow rates, health of connections & operators and allows you to apply customized metric color schemes.  
<img src="/streamsx.documentation/images/qse/sample-graph.png" alt="example streams graph" height="80%" width="80%"/>

### Learn more

*   [Find errors and performance problems in Streams Console](https://community.ibm.com/community/user/cloudpakfordata/viewdocument/streams-console-detecting-operator?CommunityKey=c0c16ff2-10ef-4b50-ae4c-57d769937235&tab=librarydocuments)
*   [Learn how to create and use Application Dashboards](https://community.ibm.com/community/user/cloudpakfordata/viewdocument/tutoriall-using-application-dashbo?CommunityKey=c0c16ff2-10ef-4b50-ae4c-57d769937235&tab=librarydocuments) to monitor jobs
*   To learn how to customize how your application will be deployed, read [Configuring job submissions with Streams Console](https://community.ibm.com/community/user/clouadpakfordata/viewdocument/configuring-job-submissions-using-s?CommunityKey=c0c16ff2-10ef-4b50-ae4c-57d769937235&tab=librarydocuments&LibraryFolderKey=43a572a8-f9f1-4a66-a4b3-ef2cd38af124&DefaultView=folder)