---
layout: docs
title: Monitoring IBM Streams applications with Streams Console
description: How to use the Streams Console web application to monitor Streams applications
weight: 75
published: true
tag: spl-qs
navlevel: 2
prev:
  file: qs-4a-cpd
  title:  Monitoring in Cloud Pak for Data

next:
  file: qs-5
  title:  Tips for creating a Streams application
---

The Streams Console is a web application that allows you to easily monitor and manage your Streams instance and jobs. You can quickly gain insights on the health, metrics, issues and performance of your applications and the systems they are running on.  

In Streams on Cloud Pak for Data, the Streams Console is a more advanced alternative to the Job Graph.  

This guide will cover how to perform the following tasks:
 

*   [Opening the Streams Console](#open)
*   [Submitting a Job](#submit)
*   [Using the Streams Graph](#graph)
*   [View a sample of streaming data](#view)
*   [Downloading logs](#logs)

<img alt="Screenshot of the Streams Console" src="/streamsx.documentation/images/qse/vs-code-streams-console-v5.png" height="600" width="1080"/>

_Streams Console_

<a id="open"></a>

## Opening the Streams Console

{% include spl/console/open_streams_console.html %}

<a id="submit"></a>

## Submitting a job

After opening the Streams Console, you can follow these steps to submit a job to run on your Streams instance. Streams applications are always compiled into a file with a `.sab` extension. SAB stands for Streams application bundle. This is a single, relocatable file that contains all the artifacts that are needed to run your application. Learn more about application bundle files [here](https://www.ibm.com/support/knowledgecenter/en/SSCRJU_4.3.0/com.ibm.streams.dev.doc/doc/applicationbundle.html).

So, when we say "submit a `.sab` file", we mean, run a compiled Streams application.

1.  Click on the play icon in the header bar at the top.  
    ![submit job](/streamsx.documentation/images/qse/streams-submit-job.png)
    
2.  Choose one of the options and point to your `.sab` file.
3.  To configure the job submission, click on the **Configure** button. To submit the job with the default configuration, click on the **Submit** button. [Learn more about job configuration here.](https://community.ibm.com/community/user/cloudpakfordata/viewdocument/configuring-job-submissions-using-s?CommunityKey=c0c16ff2-10ef-4b50-ae4c-57d769937235&tab=librarydocuments&LibraryFolderKey=43a572a8-f9f1-4a66-a4b3-ef2cd38af124&DefaultView=folder)



<a id="graph"></a>

## Streams Graph

This is a graphical view of your Streams Application. Here you can apply color schemes to display flow rates, operator and connection health, errors, and more. 

<img src="/streamsx.documentation/images/qse/sample-graph.png" alt="example streams graph" height="80%" width="80%"/>
<br/>
<em>A Streams application displayed in the Streams Graph. Rectangles are operators and the arrows are Streams.</em>


### Managing and Monitoring Jobs in the Streams Graph

Hover over an operator, a job, or a Stream to see available actions. These include:  

*   Set application trace
*   Restart PEs
*   Submit a job
*   View PE restart recommendations
*   Download operator and PE logs
*   Modify parallel regions

<img src="/streamsx.documentation/images/qse/operator-actions.png" alt="operator actions" height="100%" width="100%"/> 


<a id="view"></a>

### Displaying streaming data with Views

{% include spl/views_overview.md %}


 <details class="details-styled">
    <summary>Displaying an existing view</summary>

    <div><br/>
    <ol>
      <li>In the <strong>Application Dashboard</strong>, <strong>hover</strong> over the menu in the top left corner.</li>
      <li>In the popup that appears, expand the instance, and expand the <strong>Views</strong> node. This will display a list of views in all applications in the instance.</li>
      <li><p>Find the view based on the application name and the view name, and click on it.</p>
      <p><img alt="add view card" src="/streamsx.documentation/images/qse/add-view-console.png" width="80%" height="80%"/></p>
      </li>
      <li><p>Click <strong>Add View Grid</strong>. This will add a new card to the console showing the data from the grid.</p>
      <p>  <img src="/streamsx.documentation/images/qse/new-view-console.png" alt="new view card"></p>
      </li>
      </ol>

    </div>
  </details>

 <details class="details-styled">
    <summary>Adding a view to a running application</summary>

    <div><br/>
      <p>If you did not add a view in the application&#39;s source, you can still do so from the Streams Console:</p>
        <ol>
        <li>In the <strong>Application Dashboard</strong>, find the <strong>Streams Graph</strong> card and expand it.</li>
        <li>Hover over the stream that comes out of an operator and right-click.</li>
        <li>Select <strong>Create Dashboard View</strong>.</li>
        <li>Accept the default options and click on the <strong>OK</strong> button.</li>
        <li>Minimize the <strong>Streams Graph</strong> card.</li>
        <li>A new card is created in the dashboard that displays the tuples in the stream produced by the operator. Notice that the view is updated as new data arrives.</li>
        </ol>
        <p>These steps are demonstrated in the following animation.  </p>
        <p>  <img alt="animation showing how to create a view" src="/streamsx.documentation/images/vs-code/vs-code-streams-console-view-v5.gif" width="110%" height="110%"/>
        <div style="text-align: center;"><em>Creating a view on a stream</em></div>
        </p>
    </div>
  </details>



### Customizing the Streams Console with charts:

Monitor metrics and health through various configurable charts like pie charts, bar charts, scatter charts, etc. and grids.  

**How to do it:**
1. Click **Add card** in the console  
    <img src="/streamsx.documentation/images/qse/add-card-action.png" alt="add card action"/>

2. In **Visualization Settings** tab, choose a type of metric, e.g. PE memory consumption, and in the **Card Properties,** select the type of graph, e.g. bar chart.  

    <img src="/streamsx.documentation/images/qse/add-card.png" alt="add card dialog" height="70%" width="70%"/>

<a id="logs"></a>

## Download and View Logs

Analyze application trace, product and console logs through a reader friendly viewer.  

**How to use it:**

1. Open the log viewer from the far-right pane of the Streams Console.

   ![open log viewer](/streamsx.documentation/images/qse/log-viewer.png)

2. Select the job of interest. Expanding the tree and selecting an operator or PE will open the logs pane. Click any of the tabs: Application trace, Console log or Product log to show trace data, messages printed to standard out, and product logs, respectively  
<img src="/streamsx.documentation/images/qse/logs-console.png" alt="data in log viewer" height="90%" width="90%"/>


## Cancel a Job

- Click the **Cancel Jobs** button in the toolbar.

  <img src="/streamsx.documentation/images/qse/cancel-job-console.png" alt="cancel a job"/>

- Select the job(s).

- Click **Cancel jobs**.



### Learn more

*   [Find errors and performance problems in Streams Console](https://community.ibm.com/community/user/cloudpakfordata/viewdocument/streams-console-detecting-operator?CommunityKey=c0c16ff2-10ef-4b50-ae4c-57d769937235&tab=librarydocuments)
*   [Create and use Application Dashboards](https://community.ibm.com/community/user/cloudpakfordata/viewdocument/tutoriall-using-application-dashbo?CommunityKey=c0c16ff2-10ef-4b50-ae4c-57d769937235&tab=librarydocuments) to monitor jobs
*   [Customize how your application will be deployed](https://community.ibm.com/community/user/clouadpakfordata/viewdocument/configuring-job-submissions-using-s?CommunityKey=c0c16ff2-10ef-4b50-ae4c-57d769937235&tab=librarydocuments&LibraryFolderKey=43a572a8-f9f1-4a66-a4b3-ef2cd38af124&DefaultView=folder)