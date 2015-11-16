---
layout: docs
title:  Java Operator Development Guide
description:  IBM Streams Java Operator Development Guide
published: true
---
#  Introduction 

Java is a deeply integrated part of Streams. Making Java easy in Streams has been a priority for years because of its extensive libraries and huge developer base. The goal of this guide is to take a two-tiered approach. Spots that are bolded and jump out at you are going to help you get your Java operators up and running as quickly and easily as possible. Streams Studio abstracts many details away from the developer, so we also go more into depth on how Java and Streams work together, rather than solely focusing on the easiest path. 

#  Java Operator Development Guide (Draft)
Page under construction

##  Operator Lifecycle
Unless you're writing an extremely simple Java operator, it's important to understand how the operator lifecycle works. All operators written in Java must implement the following interface and implement a no-argument constructor:

~~~~~~
     com.ibm.streams.operator.Operator   
     
     public interface Operator {
		public void initialize(OperatorContext context) throws Exception;
		public void allPortsReady() throws Exception;
		public void process(StreamingInput<Tuple> port, Tuple tuple) throws Exception;
		public void processPunctuation(StreamingInput<Tuple> port, Punctuation mark) throws Exception;
		public void shutdown() throws Exception;
	}      
~~~~~~


In general, you will extend AbstractOperator, which implements the Operator interface and takes default actions. You will then override the methods that need to be customized. 
Here is a brief explanation of the required methods:

**void initialize(OperatorContext context)** - This is called once before any tuples are processed and before any of the other required methods. Here is where you should put code to establish connections to external systems and data. You will have access to parameters supplied to the operator invocation in SPL. 

**void allPortsReady()** - This is called once after the initialize() method has returned and all input and output ports are connected and ready to receive/submit tuples. Operators that process incoming tuples generally won't use this, since the process method is used to handle tuples. In the case of a source operator, there are no incoming tuples so this is where the production threads are started. We will cover this more in the source operator section.

**void process(StreamingInput\<Tuple> port, Tuple tuple)** - This is where the manipulation of incoming tuples will take place, followed by submission to an output port or an external connection (in the case of a sink operator). The performance of your operator will be decided by how efficient your process method is. See the Developing a High Performance process() method section. 

**void processPunctuation(StreamingInput\<Tuple> port, Punctuation mark)** - Process  incoming punctuation markers that arrived on the specified port. The two types of punctuation to be handled are window and final. 

**void shutdown()** - Close connections and release resources related to any external system or data store. This method is invoked when a job is cancelled or an operator is stopped. 


##**Creating Your First Java Operator**

<iframe width="480" height="298" src="https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/11/JavaOpIn1Min5.mp4" frameborder="0" allowfullscreen></iframe>

The only requirement for running your Java code in Streams is to implement the Operator interface. The simplest way to do that is to extend your class from AbstractOperator and override the methods that you want to customize. 

To modify the Streams operator model for your Java operator, you will use annotations. We will introduce some of the basic ones here, and get into others as they become more relevant. These go above the class definition for your operator. Each explanation is followed by an example. 

###Annotations:

**@PrimitiveOperator** - Configure high-level operator properties name, namespace, and description. 

~~~~~~
@PrimitiveOperator(name="StringToCaps", namespace="stringToCaps", description="Java Operator StringToCaps")
~~~~~~
**@InputPorts** - Defines one or more @InputPortSets that describe the ports for incoming tuples.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**@InputPortSet** - Contains the property definitions for one or more ports. The properties are description, cardinality, optional, windowingMode, and windowPunctuationInputMode. Only the last @InputPortSet within an @InputPorts definition can have a cardinality of -1 (define multiple input ports). 

~~~~~~
@InputPorts({@InputPortSet(description="Port that ingests tuples", cardinality=1, optional=false
	, windowingMode=WindowMode.NonWindowed, windowPunctuationInputMode=WindowPunctuationInputMode.Oblivious)
	, @InputPortSet(description="Optional input ports", cardinality=-1, optional=true
	, windowingMode=WindowMode.NonWindowed, windowPunctuationInputMode=WindowPunctuationInputMode.Oblivious)})
~~~~~~
**@OutputPorts** - Defines one or more @OutputPortSets that describe the ports for incoming tuples.   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**@OutputPortSet** - Contains the property definitions for one or more ports. The properties are description, cardinality, optional, windowingMode, and windowPunctuationInputMode. Only the last @OutputPortSet within an @OutputPorts definition can have a cardinality of -1 (define multiple input ports). 

~~~~~~
@OutputPorts({@OutputPortSet(description="Port that produces tuples", cardinality=1, optional=false
	,windowPunctuationOutputMode=WindowPunctuationOutputMode.Generating), @OutputPortSet(description="Optional 
	output ports", optional=true, windowPunctuationOutputMode=WindowPunctuationOutputMode.Generating)})
~~~~~~
    
The steps followed to create the Java operator in the video above are:   

1.	File -> New -> Project   
2.	Expand InfoSphere Streams Studio   
3.	Select SPL Project   
4.	Name your project (MyJavaOp in this case)    
5.	In the generated project, right-click and select New -> Java Primitive Operator   
6.	Name your Java operator and the namespace   
7.	Click Finish   
8.	In the generated template, modify the process operator to look like this:    

~~~~~~
    @Override
    public final void process(StreamingInput<Tuple> inputStream, Tuple tuple)
            throws Exception {
    	// Create a new tuple for output port 0
        StreamingOutput<OutputTuple> outStream = getOutput(0);
        OutputTuple outTuple = outStream.newTuple();
        String myString = tuple.getString("myString");
        myString = myString.toUpperCase();
        outTuple.setString("myString", myString);
        // Submit new tuple to output port 0
        outStream.submit(outTuple);
    }
~~~~~~

When the SPL compiler parses you Java code, specifically the annotations, it generates an operator model for the Java operator. Within your SPL Project, your operator model will be located at:   
`<SPL Project>/<operator namespace>/<operator name>/<operator name>.xml`   

**Do not modify the operator model yourself.** Change the operator model by updating the annotations in your Java code. 



##Running and Testing Your Operator

<iframe width="480" height="298" src="https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/11/TestJavaOp2Min3.mp4" frameborder="0" allowfullscreen></iframe>

The best way to start testing your Java operator is to create a simple SPL application. Here are the steps I took to build an application in 2 minutes: 

**Project Setup**

1.	File -> New -> Project   
2.	Expand InfoSphere Streams Studio   
3.	Select SPL Application Project   
4.	Name your project (TestJavaOp in this case)  
5.	Click Next  
6.	Add a dependency on your Java operator project 
7.	Click Finish

**Application Development**

1.	In the TestJavaOp.spl graphical editor, drag a beacon operator onto the palette.
2.	Search for your Java operator and add that to the palette. 
3.	Connect the output port of the Beacon operator with the input port of the Java operator. 
4.	Add a Filesink operator to the palette and connect the Java operator to it. 
5.	Right-click on the palette. Select Open in SPL Editor. 
6.	Modify the output stream of the Beacon to be <rstring myString>
7.	Assign an arbitrary string to myString in the output clause. I also added the iteration count to the end of the string. 
Beacon_1_out0 : myString = "lowercase" +(rstring) IterationCount() ;
8.	Delete the entire logic clause (up to param). 
9.	Change the filename in the FileSink operator to results.txt. 
10.	Go back to the graphical editor. Copy the stream between the Beacon and the Java operator and paste it to the stream between the Java operator and the FileSink. 
11.	Save and let the application automatically build. 

**Application Deployment**

1.	Launch the application to the instance you have setup: Right-click on your TestJavaOp composite in the Project Explorer. Select Launch Active Build Config
2.	Accept defaults and click Continue
3.	Go to the Streams Explorer view. Right-click on the job and select Show Instance Graph.
4.	Watch your job become healthy. Give your application some time to flush output to results.txt (you can speed this up by adding flush: 1u; to your FileSink parameters) 
5.	Go back to the Project Explorer. In the Resources folder for TestJavaOp, refresh the data directory. The open data -> results.txt. 
6.	Output should look like this: 

~~~~~~
	"LOWERCASE0"
	"LOWERCASE1"
	"LOWERCASE2"
	"LOWERCASE3"
~~~~~~

##Taking Advantage of Existing Libraries
Your Java operators can take advantage of all JARs and existing Java code you already have. This easily opens up your operator to any servers, databases, etc that have Java clients, and it makes converting your Java code to Streams easy. 

There are two simple steps that are required to start using external libraries in your Java operator:

1.	Add the JARs of interest to your build path. 
2.	Use the @Libraries parameter to add the JARs to the class path.

####New annotation  
**@Libraries** - This operator annotation tells your operator where to find the JARs that it needs during execution in a Streams environment. 

Options for how to specify the path:

* Specific JARs: `@Libraries("opt/Reverse.jar")`
* Entire directories using "*": `@Libraries("opt/*")`
* Environment variables: `@Libraries("@REVERSE_HOME@")` where the environment variable would be REVERSE_HOME. 

To specify multiple locations for JARs, simply comma separate your locations:  
	`@Libraries("opt/Reverse.jar" , "opt/downloaded/*", "@REVERSE_HOME@")`

`<Video of adding the JAR>`

The example above uses a JAR with a simple function that reverses a String (download here). Here are the steps taken to leverage that code: 

1.	In your Java operator project folder, create an opt directory. Add the Reverse.jar file to it. 
2.	In the Project Explorer, refresh your Resources folder and expand opt. Right-click on Reverse.jar and select Build Path -> Add to Build Path. 
3.	Import the package:  
	`import reverse.Reverse;`
4.	Use the @Libraries annotation to add the JAR to the operator's class path. (If you ever get "class not found" exceptions once you submit your job, check your @Libraries annotation first).  
	`@Libraries("opt/Reverse.jar")`
5.	Go down to the process method, and before setting the myString attribute, add this line to reverse the String: 
 
	~~~~~~
	    @Override
	    public final void process(StreamingInput<Tuple> inputStream, Tuple tuple)
	            throws Exception {
	    	// Create a new tuple for output port 0
	        StreamingOutput<OutputTuple> outStream = getOutput(0);
	        OutputTuple outTuple = outStream.newTuple();
	        String myString = tuple.getString("myString");
	        myString = myString.toUpperCase();
	        myString = Reverse.reverse(myString);
	        outTuple.setString("myString", myString);
	        // Submit new tuple to output port 0
	        outStream.submit(outTuple);
	    }
	~~~~~~
6.	The output in results.txt will look like this:   
	
	~~~~~~
	"0ESACREWOL"
	"1ESACREWOL"
	"2ESACREWOL"
	"3ESACREWOL"
	~~~~~~

##Making Your Operator Generic with Parameters

Most operators will take in some kind of parameters from the SPL application. This allows your operator to be more generic, and usable under diverse circumstances. 

`Video of adding a parameter`

####New Annotation
**@Parameter** - This operator annotation allows you to pass in configurations from the param section of the operator definition in an SPL application.



###Annotation properties:

*	**name** - Used in @PrimitiveOperator and @Parameters.    
*	**namespace** - Used in @PrimitiveOperator. Defines namespace of the operator. 
*	**description** - Used in all annotations. This element provides a textual description of the operator and its functionality. Streams Studio also shows this description to developers using your operator in SPL applications.   
*	**cardinality** - Used in all @InputPortSet, @OutputPortSet, and @Parameter. This element indicates the number of values allowed for a parameter. A value of minus 1 (-1) indicates that the parameter can take any number of values.   
*	**optional** - Used in @InputPortSet, @OutputPortSet, and @Parameter. Defines whether a port or parameter is required.    
*	**type** - Used in the @Parameter. This element indicates the SPL type of the parameter and determines the values that the parameter can assume.   



