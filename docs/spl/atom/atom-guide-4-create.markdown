---
layout: docs
title:  Creating a new SPL application
description:  How to create a new project from scratch
navlevel: 2
tag: atom
prev:
  file: atom-guide-3-editor
  title: Reviewing SPL code in Atom
next:
  file: atom-guide-5-build
  title: Build an run an application in Atom
---

The general steps to create a new project are:
- Create an empty folder on your filesystem and import it into Atom
- Create a toolkit information file

Once you create your project, you can start creating applications. The main entry point of any SPL application is called a _Main Composite_. So after creating your project, you can create your first Main composite by:

- Defining a namespace to organize your code (optional, but recommended)
- Create a Main composite within a SPL file


Create the project folder
---------------------------
Create an empty folder on your filesystem, e.g. `MyStreamsProject`

From Atom, go to **File** \> **Add Project Folder** and select the project folder.

Create a toolkit information file
---------------------------------

SPL projects are also called toolkits. Each toolkit folder must include a file called `info.xml`.  This file describes the toolkit and any other toolkits it depends on.

**This file must be in the top level of the project.**

Create a file within the folder called `info.xml`.
    - Right-click the `MyStreamsProject` folder, select **New File**, and enter `info.xml` as the file name:

![new tk info file](/streamsx.documentation/images/atom/jpg/info1.jpeg)

You can copy the contents of sampleinfo.xml \[LINK\] to get you started.

For your reference, below is an overview of the contents of what needs to be present in the file.
    ![sample info]((/streamsx.documentation/images/atom/jpg/sample-info.jpeg)
```
<toolkitInfoModel
          xmlns="http://www.ibm.com/xmlns/prod/streams/spl/toolkitInfo"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema−instance"
          xmlns:cmn="http://www.ibm.com/xmlns/prod/streams/spl/common"
          xsi:schemaLocation="http://www.ibm.com/xmlns/prod/streams/spl/toolkitInfo toolkitInfoModel.xsd">
         <identity>
           <name>MyStreamsProject</name>
           <description>My first toolkit</description>
           <version>1.0.0</version>
           <requiredProductVersion>4.0.0</requiredProductVersion>
         </identity>
         <dependencies/>
           <sabFiles>
             <include path="data/**"/>
              <include path="etc/**"/>
           </sabFiles>
    </toolkitInfoModel>

```
Learn more about the [toolkit information file in the Knowledge Center](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.dev.doc/doc/toolkitinformationmodelfile.html).

Create a namespace
------------------------

Namespaces allow you to organize your SPL code, similar to Python
modules or Java packages. Any folder with an empty file called `.namespace` will be treated as a SPL namespace.

Create a folder within your project with the target namespace:
-   Select the project, right click, and click **New Folder**.

-   Enter a name for the namespace, e.g. `my.name.space`:
    ![sample info](/streamsx.documentation/images/atom/jpg/namespace1.jpeg)

-   Create a new file within the my.name.space folder, call it
    `.namespace`

    ![new namespace](/streamsx.documentation/images/atom/jpg/namespace2.jpeg)

-   The final folder structure should look like this:

    ![folder structure](/streamsx.documentation/images/atom/jpg/namespace3.jpeg)

Now that your namespace is created, you can create your first SPL source
file.

Create a Main composite
--------------------------

Main composites are defined in SPL source files. These files have a `.spl` extension.

**Create a source file within a namespace**:

-   Select the `my.name.space` folder, right-click and choose **New File**.

-   Enter the name for the new SPL file, `Main.spl`.

-   Add the namespace declaration to the file with the following line:

    `namespace my.name.space;`

**Create a main composite**

Executable SPL applications are called main composites. Below is a stub
for a new executable composite:

```
composite BusAlerts {
}
```

The final code should appear like this:

![stub app](/streamsx.documentation/images/atom/jpg/blank-app.jpeg)

Develop a simple application
---------------------------
Now that you have created a project, let us walk through the creation of the BusAlerts application.


**Create the Main Composite**

The main composite is the entry point for your application, so if you haven't already, create a new main composite for your application. See above for instructions.



What will the application do?
-----------------------------

Recall that this application will display alerts and advertisements within the city's public transit vehicles as they move around the city. The buses periodically report their location. When a bus is near an area with an alert, the application will detect this and send the alert.

For example, if a bus comes within 1km of the Golden Gate Bridge in San Fransisco, we want to display this message inside the bus: "Approaching Golden Gate Bridge, pedestrian bridge is closed."

We're going to develop the application in 3 steps:
![application phases](/streamsx.documentation/images/atom/jpg/phases2.jpg)

When developing Streams applications, first **break down the application into individual tasks, and then find one or more operators to perform each task.**


Use operators to process data in steps
--------------------------------------

Remember that Streams applications are made up of **operators**. Each operator performs a specific task with an **input stream** of data and then produces an **output stream** which is the result of the processing.

**Sample operator invocation**
Below we have a generic overview of an operator declaration, with the name of the operator that will be invoked, and its input and output.
Every operator in our application will follow this format.  

 - **Operator kind**
 - **Input Stream** (optional) - stream of data to be processed by the operator
 - **Output Stream** (optional)- the results of the operator's action on the incoming data.  
   - **Output Stream Schema** - describing the content of each outgoing tuple

   ![operator definition](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/04/splOverivew2.gif)


Step 1: Ingest data
====================

All Streams applications start with ingesting the data that will be analyzed.

In our case, the data we are processing is the location of each bus as it is reported.

Our first task is to convert the data in the file to a stream that can be consumed by our data processing operators.


We’ll use a `FileSource` operator to create a stream that contains the data from the file:

```
composite BusAlerts {
graph

	stream<xml locationXMLDoc> NextBusData_FromFile = FileSource()
	{
		param
			file : getApplicationDir() + "/data/saved_BusLocations.txt" ;
	}

}
```
Streams applications are directed graphs of connected operators, so the first line in the composite is a `graph` clause, which denotes the beginning of the application. declaration.


Next we have the operator invocation, with the following properties:
- **Operator kind**:  `FileSource` that reads data from a file
- **Input Stream**: there is no input stream since it is the _start_ of our Streams application.
- **Output Stream**: the output schema is `NextBusData_FromFile`, which is a stream of the lines in the input file.
  - **Output Stream Schema** - each tuple is XML string from the file, with the following format:

```
<vehicle id="5764" routeTag="24" dirTag="24___I_F00"
 lat="37.734356" lon="-122.390739" secsSinceReport="9"
 predictable="true" heading="218" speedKmHr="0"\>

```

#### Parse the XML data


Now we have a stream of XML strings coming from the `NextBusData_FromFile` operator. But we need to extract the bus id, latitude, and so on from this XML string.

For this step we will send the `NextBusData_FromFile` stream to an operator called `ParseNextBusData`:

```
stream
     <rstring id, TimeMillis reportTime, float64 latitude, float64 longitude> /*Output schema*/
    /*Output stream name*/ ParsedDataStream  =
    /*Operator name*/  ParseNextBusData (NextBusData_FromFile /*input stream*/ )
		{
			param
				agency : $agency ;
		}
```

The output stream `ParsedDataStream` contains the individual attributes describing the bus' location.

Note: The `ParseNextBusData` is a special kind of operator called a _composite_  operator, because it is made up multiple operators. It handles the parsing using the `XMLParse` operator. You can look at its source in `BusAlerts/sample/ParseNextBusData.spl`.


Now we have a stream of bus locations, we can use it to detect when a bus is near a point of interest (POI).
But what are the points of interest for our application?
These have also been defined in another file, called `poi.csv`.
The format of this data is as follows:

```
#POI Name, Message to Bus, Location
"Golden Gate Bridge","Approaching Golden Gate Bridge, pedestrian bridge is closed.","POINT (-122.46746489758902 37.79717439889875)"
AT&T Park,"If the Giants win, show your game ticket to get a discount on a GetThere taxi after the game. Goo giants!","POINT (-122.3914585 37.7785951)"
Mission Dolores Park,"Security incident near Mission Dolores Park, road and sidewalk closures in effect.","POINT (-122.4457047 37.7648361)"
"Fairview Mall","Parade on Yonge Street from 10am to 6pm, expect major delays.","POINT (-79.3463243 43.7770863)"
```

Each line describes a point of interest, the alert to send to the buses, and the location of the POI.

Since the data is in a file, we need another `FileSource` to read this data:

```
stream<rstring POI_ID, rstring locationWKT, rstring message> POI_FromFile = FileSource()
{
  param
    file : getApplicationDir() + "/data/poi.csv" ;
}
```
Note that the output schema of the _POI_FromFile_ stream matches the format in the CSV file.

Now we have 2 streams of data, `POI_FromFile` and `NextBusData_FromFile` that we are ready to process in our next step.


So far, our application graph looks like this:

![step-1-graph](/streamsx.documentation/images/atom/jpg/step1-graph.png)

Step 2: Detect when a bus is near a POI
-----------------------------------

The next step is to detect when a bus is within 1km of any of the known points of interest.
_Note: This is a simple form of the problems that the `Geofence` operator is designed to solve. But for demonstration purposes we will write the logic ourselves._

Even though Streams provides dozens of built in operators, your unique needs might require you to write your own code.  This can be done using the `Custom` operator.

The `Custom` operator is, as the name implies, for custom code.


Here is the operator's stub:
```
stream<rstring id, rstring poi, rstring message, float64 distance> BusesToAlert  =
      Custom(ParsedDataStream; POI_FromFile)
{
    logic
        onTuple POI_FromFile : {
            //process POI
        }
        onTuple ParsedDataStream : {
          //A bus has just sent its location
          //check its distance from the POIs,
          //submit an alert if necessary.
        }
}
```

Notice that the **input stream**  will be both the parsed stream of bus locations, `ParsedDataStream`, and the stream of POIs, `POI_FromFile`.
When it detects that a bus is near the POI, it will submit a tuple of type `Alert` to the **output stream**, `BusesToAlert`.


The `Alert` type contains:
  - `id` of the bus
  - name of the `poi`
  - `message` to send to the bus
  - current computed `distance` from the POI.


The `Alert` type has the following definition:

`type Alert = rstring id, rstring poi, rstring message, float64 distance;`

Paste the above line at the top of the file, right before the line `composite BusAlerts`.

Next is a `logic` clause.  

On each tuple received by the operator, the `logic` clause is executed.
Since we have 2 input streams, we have two `onTuple` clauses.


If the tuple is from the `POI_FromFile` stream, the code within the `onTuple POI_FromFile` clause is executed, otherwise the code within the `onTuple ParsedDataStream` clause is executed.  


```
stream<Alert> BusesToAlert  = Custom(ParsedDataStream; POI_FromFile)
{
  logic
    state :
    { //1
       //list of POIs
      mutable list<POI_Type> POIList = [ ];
      float64 radius = 1500.0;
    }

    onTuple POI_FromFile:
    {
    //3 add the POIs to a list
      appendM(POIList, POI_FromFile) ;
    }

    onTuple ParsedDataStream :
    {
      //A bus has just sent its location
      //convert the lat/lon to WKT
      rstring busWKT = point(longitude, latitude) ;
      for(POI_Type poi in POIList)
      {
    //3 calculate its distance from the POI
        float64 distanceFromPOI = distance(busWKT, poi.locationWKT) ;
        //4 is the bus near the POI?
        if(distanceFromPOI <= radius)
        {
          //bus is near POI.
          //5 Submit an alert tuple
            mutable Alert out = { } ;
            out.distance = distanceFromPOI ;
            out.poi = poi.POI_ID ;
            out.message = poi.message ;
            //copy input data to output
            assignFrom(out, ParsedDataStream) ;
            submit(out, BusesToAlert) ; //5
        }
      }
    }
}
```

I have marked the code with lines of interest:
1. The `state` clause is used to define 2 variables:  a list to keep track of the known points of interest and the max distance  from the POI.
2. When we receive a tuple from the `POI_FromFile` stream, we add it to the list.
3. When we receive a bus' location, then for each point of interest, we will use the `distance` function to compute the distance between the bus' current location and the POI.
4. Check if the computed distance is within the predefined `radius` (1000.0 m)
5. If the bus is within the 1km radius, create and send an alert tuple

We have now completed step 2 of our application

![step-2-graph](/streamsx.documentation/images/atom/jpg/step2-graph.png)


Step 3: Send the alert
---------------------------

Last step is to send the alert. We will use  the `printStringLn` function in another `Custom` operator to print the message to the screen.

```
() as AlertPrinter = Custom(BusesToAlert as In)
{
  logic
    onTuple BusesToAlert :
    {
      printStringLn("Bus " + id + "  is near " + poi + ", message = " + message  );
    }

}

```

So now our application is complete:

![step-3-graph](/streamsx.documentation/images/atom/jpg/step3-graph.jpg)

View the complete source in my.name.space/BusAlerts_Main.spl

### Run the application

To see this application in action, go to the next section to learn how to build and run it.


Key Takeaways
----------------------------

From this basic application here are a couple of things I hope you would have noticed:

#### Custom operators

These are an important part of Streams development to do quick tasks such as printing data to console for verification, or other quick tasks for which no operator exists.
The `BusAlerts` operator demonstrates the following:
- Using and iterating over a list
- Handling multiple input streams
- Submitting a tuple from a Custom operator

#### Source and Sink operators

Looking at the above graph again, notice the following:
- The `POI` and `NextBusData_FromFile` operators do not take any input, because they are **source operators**. They produce streams by reading data from external systems.
- Conversely, the `AlertPrinter` operator does not produce any output, because it is a **sink operator**. Sink operators usually send the results of a Streams application to an external system, such as another file, or a database or a messaging system.


#### Best practice: operator granularity

You might have noticed that the last 2 operators in the graph are both `Custom` operators.  So you might wonder, why not just print the alert in the first operator instead of sending the data to a new operator whose only job is to print the message?

This is because it is good practice in Streams for **keep operators simple by performing one task per operator**.
Separating the tasks improves performance because while one operator is performing the detection, the sink operator can spend time writing to the target system.


Learn about operator granularity and other [Streams best practices in the Knowledge Center](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.dev.doc/doc/str_opgran.html).
