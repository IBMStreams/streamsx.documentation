---
layout: docs
title:  Create your first application
description: To get started with the Python Application API, use the example of reading data from a temperature sensor and printing the output to the screen.
weight:  30
published: true
tag: py16
prev:
  file: python-appapi-devguide-2
  title: Install and setup
next:
  file: python-appapi-devguide-4
  title: Common Streams transforms
---


This tutorial demonstrates creating a Streams Python application to perform some analytics, and viewing the results.

Familiarity with [Python](https://www.python.org/about/gettingstarted/) is recommended.



# Prerequisites

Follow the steps in the previous section to [install the Python API and set up your development environment](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-2/).

### Download this tutorial
  - **As a notebook:**

    If you have IBM Watson Studio, IBM Cloud Pak for Data, or Jupyter notebooks installed, this tutorial is available as a notebook. 
    Click the link below, and then click **Save Page** in your browser to save the notebook.
      <form action="https://raw.githubusercontent.com/IBMStreams/sample.starter_notebooks/CP4D-2.5.0.0/Streams-RollingAverageSample.ipynb" target="_blank">
          <input type="submit" value="Download this tutorial as a notebook">
      </form>

 - **As a Python file:**

   To get the latest version of this tutorial as a Python (`.py`) file, open the  the notebook in Jupyter Notebook Viewer, click **View as code**, then click **Save Page** in your browser.
   ![save notebook](/streamsx.documentation/images/python/save_nb.png)
   
   <form action="https://nbviewer.jupyter.org/github/IBMStreams/sample.starter_notebooks/blob/master/Streams-RollingAverageSample.ipynb" target="_blank">
          <input type="submit" value="Download this tutorial as a Python file">
      </form>


# Overview

This tutorial demonstrates creating a Streams Python application to perform some analytics, and viewing the results.

The application simulates a data hub that receives readings from sensors. It computes the 30 second rolling average of the reported readings using [Pandas](https://pandas.pydata.org/).  

## Streams Python application basics
A Streams Python application processes a continuous and potentially infinite stream of data. The data is processed in memory and is not stored in a database first.
A Streams application is a directed flow graph of data called a `Topology`.  Data is ingested and then processed using *transforms*, which are either built-in or user-defined functions.


![streams graph animation](/streamsx.documentation/images/python/streams-graph.gif)

There are 2 basic steps to creating and running a `Topology`.

First, you define the `Topology` by describing how the application will ingest and process data.

Once you define the `Topology`, you submit it for execution.  This means that the `Topology` will be converted into a runnable Streams application and (typically, but not always) sent to the Streams instance for execution.

As the subsequent animation shows, when you submit a `Topology`, the `Topology` will not run directly on your local host, but on the Streams runtime you specify.

![topology to execution](/streamsx.documentation/images/python/animation.gif)

Once the application is running on the Streams instance, you can connect to it to continuously retrieve the results.


To summarize:
- A Streams Python application is called a `Topology`.
- You define a `Topology` by specifying how it will process a stream of data
- The `Topology` is submitted to the Streams instance for execution.




## 1. Set up a connection to the Streams instance
<a id="setup"></a>
To submit the application for execution, you first have to connect to the Streams instance. Although the application is always the same, the information required to connect to the instance depends on the target installation of Streams.

Therefore, choose your target Streams installation from the list below and use the code snippet provided to connect to the instance.

Each snippet will define a function called `submit_topology` that will be used later on to submit the `Topology` once it is defined.


#### Choose a target installation

<details>
  <summary>Streams v5 in IBM Cloud Pak for Data</summary>
{% include cpd_config.html%}
</details>

<details>
  <summary>Streams v5 installed in a Kubernetes or OpenShift cluster</summary>
    {% include edge_config.html%}
</details>
<details>
  <summary>Streaming Analytics service/IBM Watson Studio</summary>
  {% include sas_config.html%}
</details>
<details>
  <summary>Local installation of Streams v4.2/4.3</summary>
    {% include local_config.html%}
</details>



## 2. Create the application

All Streams applications start with  a `Topology` object, so start by creating one:

~~~~ python
from streamsx.topology.topology import Topology

topo = Topology(name="SensorAverages")
~~~~

## 2.1 Define  sources

Your application needs some data to analyze, so the first step is to define a data source that produces the data to be analyzed. 

Next, use the data source to create a `Stream` object. A `Stream` is a potentially infinite sequence of tuples containing the data to be analyzed.

Tuples are Python objects by default. Other supported formats include JSON. [See the doc for all supported formats](https://streamsxtopology.readthedocs.io/en/stable/streamsx.topology.topology.html#stream).

### 2.1.1 Define a source class

Define a callable class that will produce the data to be analyzed.

This example class simulates readings from sensors.


~~~~python
import random 
import time
from datetime import datetime, timedelta

# Define a callable source 
class SensorReadingsSource(object):
    def __call__(self):
        # This is just an example of using generated data, 
        # Here you could connect to db
        # generate data
        # connect to data set
        # open file
        while True:
            time.sleep(0.001)
            sensor_id = random.randint(1,100)
            reading = {}
            reading ["sensor_id"] = "sensor_" + str(sensor_id)
            reading ["value"] =  random.random() * 3000
            reading["ts"] = int((datetime.now().timestamp())) 
            yield reading 
~~~~

### 2.1.2  Create a source `Stream`

A `Topology` always begins creating a source `Stream` that contains the data you want to process.

Create a `Stream` called  `readings` that will contain the simulated data from the `SensorReadingsSource` class:

~~~~python
# Create a stream from the data using Topology.source
readings = topo.source(SensorReadingsSource(), name="Readings")
~~~~


# 2.2 Analyze data

Use a variety of methods in the `Stream` class to analyze your in-flight data, including applying machine learning models.

This application will:

- Filter out tuples based on a condition
- Compute the rolling average
- Enrich the rolling average with data from another source

<div class="alert alert-success" role="alert"><b>Tip:</b> <br/>
Built-in methods exist for common operations, such as <code>Stream.filter</code> and <code>Stream.split</code>, which filter or split a stream of data respectively.

See the <a href="/streamsx.documentation/docs/python/1.6/python-appapi-devguide-4/"> common operations section</a> for other common examples. Check out the <a href="https://streamsxtopology.readthedocs.io/en/stable/streamsx.topology.topology.html#streamsx.topology.topology.Stream">documentation </a> of the <code>Stream</code> class for full list of functions.

</div>


### 2.2.1 Filter data from the  `Stream`  

Use `Stream.filter()` to remove data that doesn't match a certain condition.


~~~~python
# Accept only values greater than 100

valid_readings = readings.filter(lambda x : x["value"] > 100,
                                 name="ValidReadings")

# You could create another stream of the invalid data:
# invalid_readings = readings.filter(lambda x : x["value"] <= 100,)
~~~~

### 2.2.2  Compute averages on the  `Stream`  

Define a function to compute the 30 second rolling average for the readings. 

See the numbered steps in the code below.



~~~~python
import pandas as pd

# 1. Define aggregation function
    
def average_reading(items_in_window):
    df = pd.DataFrame(items_in_window)
    readings_by_id = df.groupby("sensor_id")
    
    averages = readings_by_id["value"].mean()
    period_end = df["ts"].max()

    result = []
    for id, avg in averages.iteritems():
        result.append({"average": avg,
                "sensor_id": id,
                "period_end": time.ctime(period_end)})
               
    return result

# 2. Define window: e.g. a 30 second rolling average, updated every second

interval = timedelta(seconds=30)
window = valid_readings.last(size=interval).trigger(when=timedelta(seconds=1))


# 3. Pass aggregation function to Window.aggregate
# average_reading returns a list of the averages for each sensor,
# use flat map to convert it to individual tuples, one per sensor
rolling_average = window.aggregate(average_reading).flat_map()

~~~~

<div class="alert alert-success" role="alert"><br/>
A <code>Window</code> is a subset of the potentially infinite data on a <code>Stream</code>. When you use a <code>Window</code> to process a subset of  your data, the data is not stored on disk or in a database, but is processed in memory.


<ul><li><a href="/streamsx.documentation/docs/python/1.6/python-appapi-devguide-4/#windows">Learn more about Windows</a></li><li><a href="(https://streamsxtopology.readthedocs.io/en/stable/streamsx.topology.topology.html#streamsx.topology.topology.Window">Window class documentation</a></li></ul>
Learn more about windowing
See the [Window class documentation]()  for details.
</div>


### 2.2.3 Enrich the data on the `Stream`

Each tuple on the `rolling_average Stream` has the following format: 

`{'average': 1655.1009278955999, 'sensor_id': 'sensor_17', 'period_end': 'Tue Nov 19 22:07:02 2019'}
`. (See the average_reading function above).

Imagine that you want to add the geographical coordinates of the sensor to each tuple. This information might come from a different data source, such as a database.

Use `Stream.map()`. The `map` transfrom uses a function you provide to convert each tuple on the `Stream` into a new tuple.

In our case, for each tuple on the `rolling_average Stream`,  we will update it to include the geographical coordinates of the sensor.

~~~~ python 

# Modify this tuple with the coordinates of the sensor
# Returns the original tuple with a new `coords` attribute
# representing the latitude and longitude of the sensor
def enrich(tpl):
    # use simulated data, but you could make a database call, 
    lat = round(random.random() + 39.8338515, 4)
    lon = round(-74.871826 + random.random(), 4)
    # update the tuple with new data

    tpl["coords"] = (lat, lon)
    return tpl

# Update the data on the rolling_average stream with the map transform
enriched_average = rolling_average.map(enrich)

~~~~

# 2.3 Create a `View` to preview the tuples on the `Stream` 


A `View` is a connection to a `Stream` that becomes activated when the application is running.  The connection allows you to access the data on the `Stream` as it is being processed.


After submitting the `Topology`, we use a `View`  to examine the data in section 4.


To view the data on the `enriched_average Stream`, define a `View` using `Stream.view()`:

~~~~python
averages_view = enriched_average.view(name="RollingAverage", description="Sample of rolling averages for each sensor")
~~~~

<div class="alert alert-success" role="alert"><br/>
You can <a href="/streamsx.documentation/docs/python/1.6/python-appapi-devguide-6/#accessing-the-tuples-of-a-view">connect to a view in <em>any</em> running Streams job using the REST API</a> , regardless of what language was used to create the application.
</div>

# 2.4 Define output

You could also enable a microservices based architecture by publishing the results so that other Streams applications can connect to it.

Use `Stream.publish()` to make the `enriched_average Stream` available to other applications. 

To send the stream to another database or system, use a sink function (similar to the source function) and invoke it using `Stream.for_each`.




~~~~python
import json
# publish results as JSON
enriched_average.publish(topic="AverageReadings",
                        schema=json, 
                        name="PublishAverage")

# Other options include:
# invoke another sink function:
# enriched_average.for_each(func=send_to_db)
~~~~


# 3. Submit the application
A running Streams application is called a *job*.  Use this code to submit the `Topology` for execution, using the `submit_topology` function [defined in step 1](#setup).


~~~~python
# The submission_result object contains information about the running application, or job
print("Submitting Topology to Streams for execution..")
submission_result = submit_topology(topo)

if submission_result.job:
  streams_job = submission_result.job
  print ("JobId: ", streams_job.id , "\nJob name: ", streams_job.name)
else:
  print("Submission failed: "   + str(submssion_result))
~~~~



# 4. Use a `View` to access data from the job
Now that the job is started, use the `averages_view` object you created in step 2.3 to start retrieving data from the `enriched_average Stream`.


~~~~python
# Connect to the view and display the data
print("Fetching view data ...")
queue = averages_view.start_data_fetch()
try:
    for val in range(10):
        print(queue.get())    
finally:
    averages_view.stop_data_fetch()
~~~~


### 4.0.1 Run the application
If you are using a notebook, the application should have been submitted when you ran step 3. Otherwise, if you are using the Python interpreter, running the above code should produce output like this:
~~~~
JobId:  7 
Job name:  notebook::SensorAverages_7
{'average': 1503.8703753120099, 'sensor_id': 'sensor_1', 'period_end': 'Thu Nov 21 22:22:41 2019', 'coords': [40.7013, -74.2747]}
{'average': 1430.7707245569663, 'sensor_id': 'sensor_10', 'period_end': 'Thu Nov 21 22:22:41 2019', 'coords': [40.7474, -74.0083]}
{'average': 1574.5588234099662, 'sensor_id': 'sensor_100', 'period_end': 'Thu Nov 21 22:22:41 2019', 'coords': [40.6807, -74.3725]}
{'average': 1457.2224636625913, 'sensor_id': 'sensor_11', 'period_end': 'Thu Nov 21 22:22:41 2019', 'coords': [40.2518, -74.6188]}
{'average': 1651.968830163488, 'sensor_id': 'sensor_12', 'period_end': 'Thu Nov 21 22:22:41 2019', 'coords': [40.2845, -74.6882]}
~~~~


## 4.1 (Optional) Display the results in real time
**Note: This code only works in a notebook that has [ipywidgets](https://ipywidgets.readthedocs.io/en/latest/) enabled.**

Calling `View.display()` from the notebook displays the results of the view in a table that is updated in real-time.


~~~~python
# Display the results for 30 seconds
averages_view.display(duration=30)
~~~~

## 4.2 See job status 

<a id="monitor"></a>
You can further interact with the job through the Streams Console. If you have IBM Cloud Pak for Data, you can also use the Job Graph.

<ul class="nav nav-tabs">
   <li class="active"><a data-toggle="tab" href="#cpd"><b>Job Graph </b></a></li>
  <li ><a data-toggle="tab" href="#console"><b>Streams Console</b></a></li>
</ul>

<div class="tab-content">

  <div id="cpd" class="tab-pane fade   in active">
  <h3>Monitoring a job in IBM Cloud Pak for Data</h3>
To view job status and logs:
<ol>
<li>From the main menu, go to <b>My Instances &gt; Jobs</b>. </li>
<li>Find your job based on the <code>JobId</code> printed when you submitted the topology.</li>
<li>Select <b>View graph</b> from the context menu action for the running job.</li>
</ol>
<br/>
<img alt="app in CPD Job graph" src="/streamsx.documentation/images/python/view-in-cpd-python.gif"/>

  </div>

  <div id="console" class="tab-pane fade ">
  <h3>Monitoring a job with the Streams Console</h3>
  To can access the Streams console through your browser, you need its URL.  Choose one of the following options for instructions to open the Console for your Streams instance.<br/>

  <details>
  <summary>IBM Cloud Pak for Data:</summary>
    <ol>
    <li>From the navigation menu, click <strong>My instances</strong>.</li>
    <li>Click the <strong>Provisioned Instances</strong> tab.</li>
    <li>Find your Streams instance in the list.</li>
    <li>From the context menu, click <b>View Details.</b></li>
    <li>Under <b>Endpoints</b> find the Streams Console URL under <b>External Console endpoint.</b></li>
    </ol>
  <br/>  <br/>
</details>
  <details>
   <summary>Open the Streams Console for Streams v5</summary>
  Consult the documentation to get the Streams Console URL.
  <br/>  <br/>
</details>

  <details>
  <summary>Streaming Analytics service in IBM Cloud</summary>

  <ol>
    <li>Log in to the IBM Cloud dashboard.</li>
    <li> Find your service instance, and click on it to go to its dashboard</li>
    <li>Click <b>Launch</b> from the service dashboard page.  </li>
    </ol>
    <br/>  <br/>
</details>

  <details>
  <summary>Local installation of Streams v4.2 or 4.3</summary>

  From the command line, run: <code>streamtool geturl -d DOMAIN_NAME --console</code>
  <p>For example, if the domain name is <code>StreamsDomain</code>:</p>
<pre><code>$ streamtool geturl -d StreamsDomain --console </code></pre>
 <p>Output:</p>
 <pre><code> https://streamsqse.localdomain:8443/streams/domain/console
  </code></pre>
Open that URL in your browser, and log in to the console using the same username and password you used to submit the Topology.
</details>

<img alt="app in streams console" src="/streamsx.documentation/images/python/view-in-console-python.gif"></img>


  </div>

</div>

### More about the Streams Console

See this article on Streamsdev for an [overview of the Streams Console](https://developer.ibm.com/streamsdev/docs/streams-console-overview/)

# 5. Cancel the job

Streams jobs run indefinitely, so make sure you cancel the job once you are finished running the sample.

If you are using a notebook, run this line:
~~~~ python
if submission_result.job.cancel():
  print("Sucessfull cancelled the job")

~~~~
Otherwise, cancel the job from Streams Console or the Job graph.

#### Cancel the job from the Streams Console:

- Click the Cancel Job button in the toolbar.
- Select the job 
- Click **Cancel**

#### Cancel the job from the Job Graph:

<ol>
<li>From the main menu, go to <b>My Instances &gt; Jobs</b>. </li>
<li>Find your job based on the <code>JobId</code> printed when you submitted the topology.</li>
<li>Select <b>Delete</b> from the context menu action for the running job.</li>
</ol>


# Summary

We started with a `Stream` called `readings`, which contained the data we wanted to analyze. Next, we used functions in the `Stream` object to perform simple analysis and produced the `enriched_average` stream.  This stream is `published` for other applications running within our Streams instance to access.

After submitting the application to the Streams service, we used the `enriched_average` view to see the results.




# Next Steps

- **Find more samples**: There are several sample notebooks available in the [starter notebooks repository on GitHub](https://github.com/IBMStreams/sample.starter_notebooks). Visit the repository for examples of how to connect to common data sources, including Apache Kafka, IBM, and Db2 Warehouse. 
- Learn more about how to use the API from the [common Streams transforms](/streamsx.documentation/docs/python/1.6/python-appapi-devguide-4/) section.