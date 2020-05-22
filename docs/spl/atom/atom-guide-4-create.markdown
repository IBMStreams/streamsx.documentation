---
layout: docs
title:  Create an SPL application
description:  How to create a new project from scratch
navlevel: 2
tag: atom
prev:
  file: atom-guide-3-editor
  title: Reviewing SPL code in Atom
next:
  file: atom-guide-5-build
  title: Build and run an application in Atom
---


{% include atom_create.html %}

Develop the sample application
---------------------------
Now that you created a project, the next step is to define the appliaction graph. The application graph describes the way data is processed within the application.

**Create the main composite**

Create a new main composite for your application as explained in the previous section. Call it `BusAlerts`.

What does the application do?
-----------------------------

Recall that this application displays alerts and advertisements within the city’s public transit vehicles as the vehicles move around the city. The buses periodically report their location. When a bus is near an area with a point of interest (POI), the application detects this and sends the alert

For example, if a bus comes within 1km of the Golden Gate Bridge in San Francisco, you want to display this message inside the bus: "Approaching Golden Gate Bridge, pedestrian bridge is closed."

You will develop the application in three steps:
![application phases](/streamsx.documentation/images/atom/jpg/phases2.jpg)

As shown in the preceeding image, the data is processed in 3 main steps:
1. Ingest data about moving buses.
2. Use the data from step 1 to determine when a bus is near a POI.
3. Send an alert to the bus.


**Tip:**  When you develop Streams applications, first break down the application into individual tasks, and then find one or more operators to perform each task.

Use operators to process data in steps
--------------------------------------

Remember, Streams applications are made up of **operators**. Each operator performs a specific task with an **input stream** of data and then produces an **output stream** that is the result of the processing.

**Sample operator invocation**
The following image is a generic overview of an operator declaration, with the name of the operator that will be invoked, and its input and output. Every operator in your application will follow this format.

 - **Operator kind**: The type of the operator, e.g. `FileSource` or `Geofence`.
 - **Input stream** (optional) - The stream of data to be processed by the operator
 - **Output stream** (optional)- The results of the operator's action on the incoming data.
   - **Output stream schema** - Describes the content of each outgoing tuple

   ![operator definition](https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/04/splOverivew2.gif)

Step 1: Ingest data
====================

All Streams applications start with ingesting the data that will be analyzed.

In this case, the data you are processing is the location of each bus as it is reported.

Your first task is to convert the data in the file to a stream that can be consumed by our data processing operators. You'll use a `FileSource` operator to create a stream that contains the data from the file:

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
Streams applications are directed graphs of connected operators, so the first line in the composite is a `graph` clause, which denotes the beginning of the application.

Next, you have the operator invocation, with the following properties:
- **Operator kind**:  `FileSource` that reads data from a file
- **Input stream**: There is no input stream because it is the _start_ of our Streams application.
- **Output stream**: The output schema is `NextBusData_FromFile`, which is a stream of the lines in the input file.
- **Output stream schema** - Each tuple is an XML string from the file, with the following format:

  ```
  <vehicle id="5764" routeTag="24" dirTag="24___I_F00"
   lat="37.734356" lon="-122.390739" secsSinceReport="9"
   predictable="true" heading="218" speedKmHr="0"\>
  ```

#### Step 1b: Parse the XML data

Now you have a stream of XML strings coming from the `NextBusData_FromFile` operator. But you need to extract the bus ID, latitude, and other information from this XML string.

For this step you will send the `NextBusData_FromFile` stream to an operator called `ParseNextBusData`:

```
stream <rstring id, TimeMillis reportTime, float64 latitude, float64 longitude> /*Output schema*/
    ParsedDataStream /*Output stream name*/ = ParseNextBusData (NextBusData_FromFile /*input stream*/) /*Operator name*/  
	{
		param
			agency : $agency ;
	}
```

The output stream `ParsedDataStream` contains the individual attributes that describe the location of each bus.

The `ParseNextBusData` operator is a special kind of operator called a _composite_  operator. It is called a composite operator because it is made up multiple operators. It uses the `XMLParse` operator to parse the XML data. You can look at its source in `BusAlerts/my.name.space/ParseNextBusData.spl`.


Next, use the stream of bus locations, to detect when a bus is near a point of interest (POI).
The points of interest for our application have been defined in another file, called `poi.csv`. The format of this data is as follows:

```
#POI Name, Message to Bus, Location
"Golden Gate Bridge","Approaching Golden Gate Bridge, pedestrian bridge is closed.","POINT (-122.46746489758902 37.79717439889875)"
AT&T Park,"If the Giants win, show your game ticket to get a discount on a GetThere taxi after the game. Goo giants!","POINT (-122.3914585 37.7785951)"
Mission Dolores Park,"Security incident near Mission Dolores Park, road and sidewalk closures in effect.","POINT (-122.4457047 37.7648361)"
"Fairview Mall","Parade on Yonge Street from 10am to 6pm, expect major delays.","POINT (-79.3463243 43.7770863)"
```

Each line describes a point of interest, the alert to send to the buses, and the location of the point of interest. Since the data is in a file, use another `FileSource` to read this data:

```
stream<rstring POI_ID, rstring locationWKT, rstring message> POI_FromFile = FileSource()
{
    param
        file : getApplicationDir() + "/data/poi.csv" ;
}
```
Note that the output schema of the _POI_FromFile_ stream matches the format in the CSV file.

Now you have two streams of data, `POI_FromFile` and `NextBusData_FromFile` that you are ready to process in your next step. So far, the application graph looks like the following image:

![step-1-graph](/streamsx.documentation/images/atom/jpg/step1-graph.png)

Step 2: Detect when a bus is near a POI
-----------------------------------

The next step is to detect when a bus is within 1km of any of the known points of interest.
_Note that the `Geofence` operator is designed to solve this exactly this type of problem. But for demonstration purposes you can write the logic yourself._

Even though Streams provides dozens of built in operators, your unique needs might require you to write your own code.

You can write your own code by using the `Custom` operator. The `Custom` operator is, as the name implies, for custom code. Here is the operator's stub:
```
stream<rstring id, rstring poi, rstring message, float64 distance> BusesToAlert =
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

Notice that there are 2 **input streams**,the parsed stream of bus locations (`ParsedDataStream`), and the stream of POIs (`POI_FromFile`). When the operator detects that a bus is near the POI, it submits a tuple of type `Alert` to the **output stream**, `BusesToAlert`.

The `Alert` type contains the following information:
  - The `id` of the bus.
  - The name of the `poi`.
  - The `message` to send to the bus.
  - The current computed `distance` from the POI.


The `Alert` type has the following definition:

`type Alert = rstring id, rstring poi, rstring message, float64 distance;`

Enter the preceeding line at the top of the file, right before the line `composite BusAlerts`. Next, add a **logic** clause to the `Custom` operator.


The **logic** clause is executed on each tuple that is received by the operator. Because you have two input streams, you have two **`onTuple`** clauses.

If the tuple is from the `POI_FromFile` stream, the code within the `onTuple POI_FromFile` clause is executed. Otherwise the code within the `onTuple ParsedDataStream` clause is executed.

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

The code is marked with numbers that indicate lines of interest:
1. The `state` clause is used to define two variables:  a list to keep track of the known points of interest and the maximum distance  from the POI.
2. When the operator receives a tuple from the `POI_FromFile` stream, the tuple is added to the list.
3. When the operator receives a bus' location, then for each point of interest, the `distance` function is used to compute the distance between the current location of the bus and the POI.
4. Check if the computed distance is within the predefined `radius` (1 km or 1000.0 m)
5. If the bus is within the 1km radius, create and send an alert tuple.

You have now completed step 2 of the application.

![step-2-graph](/streamsx.documentation/images/atom/jpg/step2-graph.png)

Step 3: Send the alert
---------------------------

The last step is to send the alert. Use  the `printStringLn` function in another `Custom` operator to print the message to the screen.

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

So now your application is complete:

![step-3-graph](/streamsx.documentation/images/atom/jpg/step3-graph.jpg)

View the complete source in `my.name.space/BusAlerts_CachedData.spl`.

### Run the application

To see this application in action, go to the next section to learn how to build and run it.


Key takeaways
----------------------------

From this basic application here are a couple of things to notice:

#### Custom operators

Custom operators are an important part of Streams development to do quick tasks such as printing data to console for verification, or other tasks for which no operator exists.

The `BusesToAlert` operator demonstrated the following functionality:
- Using and iterating over a list
- Handling multiple input streams
- Submitting a tuple from a Custom operator

#### Source and Sink operators

Looking at the preceding graph again, notice the following points:
- The `POI` and `NextBusData_FromFile` operators do not take any input, because they are **source operators**. They produce streams by reading data from external systems.
- Conversely, the `AlertPrinter` operator does not produce any output, because it is a **sink operator**. Sink operators usually send the results of a Streams application to an external system, such as another file, or a database or a messaging system.

#### Best practice: operator granularity

You might notice that the last two operators in the graph are both `Custom` operators.  So you might wonder, why not print the alert in the first operator instead of sending the data to a new operator whose only job is to print the message?

The application uses two operators because it is good practice in Streams to **keep operators simple by performing one task per operator**. Separating the tasks improves performance because while one operator is performing the detection, the sink operator can spend time writing to the target system.


Learn about operator granularity and other [Streams best practices in the documentation](https://www.ibm.com/support/knowledgecenter/SSCRJU_4.3.0/com.ibm.streams.dev.doc/doc/str_opgran.html).
