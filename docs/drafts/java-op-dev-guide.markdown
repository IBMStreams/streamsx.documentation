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

* **void initialize(OperatorContext context)** - This is called once before any tuples are processed and before any of the other required methods. Here is where you should put code to establish connections to external systems and data. You will have access to parameters set in the SPL operator invocation. 

* **void allPortsReady()** - This is called once after the **initialize()** method has returned and all input and output ports are connected and ready to receive/submit tuples. Operators that process incoming tuples generally won't use this, since the process method is used to handle tuples. In the case of a source operator, there are no incoming tuples so this is where the tuple producing threads are started. We will cover this more in the source operator section.

* **void process(StreamingInput\<Tuple> port, Tuple tuple)** - This is where the manipulation of incoming tuples will take place, followed by submission to an output port or an external connection (in the case of a sink operator). **The performance of your operator is almost completely dependent on how efficient your process method is.** See the Developing a High Performance process() method section. 

* **void processPunctuation(StreamingInput\<Tuple> port, Punctuation mark)** - This is where incoming punctuation markers that arrived on the specified port are processed. The two types of punctuation to be handled are window and final. 

* **void shutdown()** - This is where connections are closed and resources related to any external system or data store are released. This method is invoked when a job is cancelled or an operator is stopped. 


##**Creating Your First Java Operator**

<div class="modal-body">
	<video controls width="60%" src="/streamsx.documentation/images/JavaOperatorGuide/JavaOpIn1Min5.mp4"></video>
</div>

The only requirement for running your Java code in Streams is to implement the Operator interface. The simplest way to do that is to extend your class from AbstractOperator and override the methods that you want to customize. In many cases, the **process()** method is the only method that needs to be overridden. 


###Annotations

To modify the Streams operator model for your Java operator, you will use annotations. We will introduce some of the basic ones here, and get into others as they become more relevant. Here is a snippet that shows the minimum amount of code needed to implement the StringToCaps operator that was created using the Streams Studio template in the video above. The StringToCaps operator takes in tuples from its input port with an attribute type of rstring, transforms the strings to uppercase, then submits the transformed strings as a tuple to the output port. 

**Notice:**     

* The required set of annotations are located above the operator class definition (highlighted in blue). Annotations define the Streams operator model discussed next. 
* We extend AbstractOperator and use the default behavior on all required methods in the Operator interface except for the process() method. This is common for operators that don't interact with external systems. 
* General formula for process method:
	1. Get attributes that you want to manipulate from the incoming tuple using getter methods. 
	2. Manipulate the attributes in the desired way. 
	3. Write attributes to the output tuple using setter methods. 
	4. Submit output tuple. 

<pre style="font-family: Andale Mono, Lucida Console, Monaco, fixed, monospace; color: #000000; background-color: #eee;font-size: 12px;border: 1px dashed #999999;line-height: 14px;padding: 5px; overflow: auto; width: 100%"><code><b><font color="blue">@PrimitiveOperator()
@InputPorts(@InputPortSet(cardinality=1))
@OutputPorts(@OutputPortSet(cardinality=1))</font></b>
public class StringToCaps extends AbstractOperator {
    @Override
    public final void <b>process</b>(StreamingInput&lt;Tuple&gt; inputStream, Tuple tuple)
            throws Exception {
        // Create a new tuple for output port 0
        StreamingOutput&lt;OutputTuple&gt; outStream = getOutput(0);
        OutputTuple outTuple = outStream.newTuple();
        
        // Get attribute from input tuple and manipulate
        String myString = tuple.getString(&quot;myString&quot;);
        myString = myString.toUpperCase();
        outTuple.setString(&quot;myString&quot;, myString);
        
        // Submit new tuple to output port 0
        outStream.submit(outTuple);
    } 
}
</code></pre>

The definitions below are followed by examples of the bare minimum requirements for the annotations. 

####Annotation Definitions

**@PrimitiveOperator** - Configure high-level operator properties such as name, namespace, and description. 

~~~~~~
@PrimitiveOperator()
~~~~~~
**@InputPorts** - Defines one or more @InputPortSets that describe the ports for incoming tuples.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**@InputPortSet** - Contains the property definitions for one or more ports. The available properties are description, cardinality, optional, windowingMode, and windowPunctuationInputMode. Only the last @InputPortSet within an @InputPorts definition can have a cardinality of -1 (define multiple input ports). 

~~~~~~
@InputPorts(@InputPortSet(cardinality=1))
~~~~~~
**@OutputPorts** - Defines one or more @OutputPortSets that describe the ports for incoming tuples.   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**@OutputPortSet** - Contains the property definitions for one or more ports. The available properties are description, cardinality, optional, windowingMode, and windowPunctuationInputMode. Only the last @OutputPortSet within an @OutputPorts definition can have a cardinality of -1 (define multiple input ports). 

~~~~~~
@OutputPorts(@OutputPortSet(cardinality=1))
~~~~~~





<!--  
In the video above, a simple Java operator is created that takes in tuples from its input port with an attribute type of rstring, transforms the string to uppercase, then submits the transformed string as a tuple to the output port. This example is built on throughout the beginners portion of this developers guide. 

Creating a simple Java operator:   

1.	File -> New -> Project   
2.	Expand InfoSphere Streams Studio   
3.	Select SPL Project   
4.	Name your project (MyJavaOp in this case)    
5.	In the generated project, right-click and select New -> Java Primitive Operator   
6.	Name your Java operator and the namespace (StringToCaps and stringToCaps respectively)
7.	Click Finish   
8.	In the generated template, StringToCaps.java, modify the process operator to look like this:    

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
-->

###Building the Operator Model
When the SPL compiler parses your Java code, specifically the annotations, it generates an operator model for the Java operator. Within your SPL Project(also called a toolkit), your operator model will be located at:   
`<SPL toolkit>/<operator namespace>/<operator name>/<operator name>.xml`   

**Do not modify the operator model yourself.** Change the operator model by updating the annotations in your Java code. 



<ul class="nav nav-tabs">
  <li class="active"><a data-toggle="tab" href="#command-0">Build with Command-line</a></li>
  <li><a data-toggle="tab" href="#studio-0">Build with Streams Studio (Video Steps)</a></li>
</ul>

<div class="tab-content">
  <div id="command-0" class="tab-pane fade in active">
  <br>
  The steps for building the simple Java primitive operator from above on the command line are as follows:
  <br><br>
<ol>
	<li>Create a directory for your SPL toolkit (MyJavaOp in this case). Create these directories as well: </li>
	<pre><code>MyJavaOp/impl/java/src/
MyJavaOp/impl/java/bin/</code></pre>
	<li>Place your StringToUpper.java operator class in <pre>MyJavaOp/impl/java/src/</pre></li>
	<li>Compile the Java operator class from the SPL toolkit directory using:</li>
	<pre><code>javac -cp $Streams_Install/lib/com.ibm.streams.operator.jar impl/java/src/StringToCaps.java -d impl/java/bin/</code></pre>
	<li>Index the toolkit from the SPL toolkit directory. This will generate the operator model and build the toolkit directory structure.  </li>
	<pre><code>spl-make-toolkit -i ./</code></pre>
</ol>  
  </div>
  <div id="studio-0" class="tab-pane fade">
  <br>
   The steps for building the simple Java primitive operator using Streams Studio are as follows: 
<br><br>
<ol>
	<li>	File -> New -> Project</li>   
	<li>Expand InfoSphere Streams Studio</li> 
	<li>Select SPL Project</li>
	<li>Name your project (MyJavaOp in this case)</li>
	<li>In the generated project, right-click and select New -> Java Primitive Operator</li>
	<li>Name your Java operator and the namespace (StringToCaps and stringToCaps respectively)</li>
	<li>Click Finish</li>
	<li>In the generated template, StringToCaps.java, modify the process operator to look like this:</li> 
<pre style="font-family: Andale Mono, Lucida Console, Monaco, fixed, monospace; color: #000000; background-color: #eee;font-size: 12px;border: 1px dashed #999999;line-height: 14px;padding: 5px; overflow: auto; width: 100%"><code>    @Override
    public final void process(StreamingInput&lt;Tuple&gt; inputStream, Tuple tuple)
            throws Exception {
        // Create a new tuple for output port 0
        StreamingOutput&lt;OutputTuple&gt; outStream = getOutput(0);
        OutputTuple outTuple = outStream.newTuple();
        String myString = tuple.getString(&quot;myString&quot;);
        myString = myString.toUpperCase();
        outTuple.setString(&quot;myString&quot;, myString);
        // Submit new tuple to output port 0
        outStream.submit(outTuple);
    }
</code></pre>
	<li>Save your changes and Studio will automatically build your operator model and create the toolkit directory structure.</li> 
</ol>
  </div>
</div>

<!--
The steps for building the simple Java primitive operator from above on the command line are as follows:
1. Create a directory for your SPL toolkit (MyJavaOp in this case). Create these directories as well:
	`MyJavaOp/impl/java/src/`
	`MyJavaOp/impl/java/bin/`
2. Place your StringToUpper.java operator class in MyJavaOp/impl/java/src/
3. Compile the Java operator class from the SPL toolkit directory using:
	`javac -cp $Streams_Install/lib/com.ibm.streams.operator.jar impl/java/src/StringToCaps.java -d impl/java/bin/`
4. Index the toolkit from the SPL toolkit directory using: 
	spl-make-toolkit -i ./
-->

In both the CLI and the Streams Studio cases, the toolkit structure will now look approximately like this: 

~~~~~~
/+ <toolkit> 
   /* toolkit.xml 
   /+ <name-space>
      /+ <operator>
      	/* <operator model>
   /+ impl
      /+ bin
      /+ include
      /+ java
          /+ src
          /+ bin
      /+ lib
      /+ src             
~~~~~~
	
* **[toolkit]** - root directory of the toolkit.  Typically the name of the root directory matches the name of the toolkit in info.xml.
* **toolkit.xml** - a generated resource by the SPL toolkit indexing processing.  This file should not be modified and is used by the compiler and various comoponents in Streams.
* **[name-space]** - similar to packages in Java, allow you to group related SPL toolkit artifacts together.
    * **[operator]** - a directory containing all artifacts relative to a Java / C++ primitive operator.  Each operator has its own separate directory.
* **impl** - the impl directory contains implementation code of primitive operators or native functions
    * **impl/java/src** - contains Java primitive operator or native function code
    * **impl/java/bin** - contains Java class files for the Java implementation code
* **lib** - contains any external libraries that this toolkit may require

Note:  If you use Streams Studio to create a new SPL project, Streams Studio will automatically create the correct directory structure for you.	
	

##Running and Testing Your Operator

<div class="modal-body">
	<video controls width="60%" src="/streamsx.documentation/images/JavaOperatorGuide/TestJavaOp2Min3.mp4"></video>
</div>

The best way to start testing your Java operator is to create a simple SPL application. Here are the steps I took to build an application in 2 minutes, which should approximate how to simply test any Java operator: 

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
Your Java operators can take advantage of all JARs and existing Java code you already have. This makes connecting to any servers, databases, etc that have Java clients easy, and it makes converting your Java code to Streams simple. 

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

<div class="modal-body">
	<video controls width="60%" src="/streamsx.documentation/images/JavaOperatorGuide/AddingJar.mp4"></video>
</div>

The example above uses a JAR with a simple function that reverses a String (download here). Here are the steps taken to leverage that code: 

1.	In your Java operator project folder, create an opt directory. Add the Reverse.jar file to it. 
2.	In the Project Explorer, refresh your Resources folder and expand opt. Right-click on Reverse.jar and select Build Path -> Add to Build Path. 
3.	Import the package:  
	`import reverse.Reverse;`
4.	Use the @Libraries annotation to add the JAR to the operator's class path. (If you ever get "class not found" exceptions once you submit your job, check your @Libraries annotation first).  
	`@Libraries("opt/Reverse.jar")`
5.	Go down to the process method, and before setting the "myString" attribute, add this line to reverse the String: 
 
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

####New Annotation
**@Parameter** - This operator annotation allows you to pass in configurations from the param section of the operator definition in an SPL application. 

<div class="modal-body">
	<video controls width="60%" src="/streamsx.documentation/images/JavaOperatorGuide/AddParameter.mp4"></video>
</div>

The example in the video above shows how to generalize the StringToCaps operator so that it reverses (or doesnt reverse) the incoming string based on a reverseString boolean parameter in the SPL operator code. Here are the steps taken, which are similar for all parameters:

1.	In the operator class definition add a Boolean member variable that we will use to hold the parameter value. We want the default to be false if the parameter is not specified. 
`private Boolean reverseString = false;`
2.	Scroll down to the `process()` method and surround the String reversal line with an if statement:
 
	~~~~~~
    public final void process(StreamingInput<Tuple> inputStream, Tuple tuple)
            throws Exception {
		// Create a new tuple for output port 0
        StreamingOutput<OutputTuple> outStream = getOutput(0);
        OutputTuple outTuple = outStream.newTuple();
        String myString = tuple.getString("myString");
        myString = myString.toUpperCase();
        if (reverseString){
        	myString = Reverse.reverse(myString);
        }
        outTuple.setString("myString", myString);
        // Submit new tuple to output port 0
        outStream.submit(outTuple);
    }
	~~~~~~
3.	Near the bottom (still within the class definition), we will use the @Parameter annotation above a set method. The name of the parameter will be "reverseString", it will be optional, and we will add a description. Since the parameter is of type Boolean, the cardinality is automatically set to 1, meaning that only a single value can be provided. 

	~~~~~~
    @Parameter(name = "reverseString", optional = true,
    	description = "Boolean value. Reverse strings if true. Default: false.")
    public void setReverseString(Boolean value){
    	reverseString = value;
    }
	~~~~~~
4.	Once you save, you are done updating your operator. To test our modification, modify the StringToCaps operator in TestJavaOp.spl to look like this: 

	~~~~~~
	(stream<rstring myString> StringToCaps_2_out0) as StringToCaps_2 =
			StringToCaps(Beacon_1_out0)
		{
			param
				reverseString : true; 
		}
	~~~~~~
5.	Your output should look like this:

	~~~~~~
	"0ESACREWOL"
	"1ESACREWOL"
	"2ESACREWOL"
	"3ESACREWOL"
	~~~~~~

Here are some more parameter examples:
`tabs with different parameter examples`

##Adding Custom Metrics
Metrics are simple counters, maintained at run time, that can be read from outside of a running job to monitor statistics of interest. Two types of metrics are provided by the SPL language runtime:

* **System metrics** - predefined and maintained by the SPL runtime (this includes things like number of tuples processed on a port, tuple flow rate, etc.)
* **Custom metrics** - created and maintained by the operator. 

This section will show you how to add your own custom metrics to your Java operator. 

####New Annotation
**@CustomMetric** - This operator annotation allows you to define your own custom metrics that will be visible to the SPL runtime. Live feed of this metric can be viewed in Streams Studio and the Streams Console.

The **@CustomMetric** annotation can take four parameters. **name** and **description** as they are used in other annotations, and then **kind** and **mxbean** which are unique to @CustomMetric:

* **kind** - This describes the type of metric that is being provided. It can take one of three values as defined in the Metric.Kind enumeration:
	* **Counter** indicates that this metric represents a count of occurrence of some event. 
	* **Gauge** indicates a value that is continuously variable with time. 
	* **Time** indicates a metric that represents a point in time.
* **mxbean** - This Boolean indicates whether to register this metric into the platform's MBean server. The default value is false. 

<div class="modal-body">
	<video controls width="60%" src="/streamsx.documentation/images/JavaOperatorGuide/AddingMetrics.mp4"></video>
</div>

The example in the video above shows how to add a custom metric to **count**l the number of characters processed by the StringToCaps operator. These steps are approximately the same as adding any other custom metrics.

**Adding a numCharacter Metric:**

1.	Add a private member variable of type Metric to the StringToCaps operator class:
`private Metric numCharacters;`
2.	Import the Metric library, com.ibm.streams.operator.Metrics:
`import com.ibm.streams.operator.metrics.Metric;`
3.	Add the @CustomMetric annotation. Name the Metric "numCharacters" and make the kind Metric.Kind.COUNTER. Below the annotation you will add a setter method that takes a runtime Metric object and assigns it to our local Metric class variable numCharacters. The set is done before initialization similar to the way @Parameter sets are done. 

	~~~~~~
	@CustomMetric(name = "numCharacters", kind = Metric.Kind.COUNTER)
	public void setNumCharacters(Metric runtimeMetric){
		numCharacters = runtimeMetric;
	}
	~~~~~~
4.	In the process() method, the numCharacters metric is incremented by the length of myString right before the outgoing tuple is submitted:

	~~~~~~
    @Override
    public final void process(StreamingInput<Tuple> inputStream, Tuple tuple)
            throws Exception {

    	// Create a new tuple for output port 0
        StreamingOutput<OutputTuple> outStream = getOutput(0);
        OutputTuple outTuple = outStream.newTuple();

        String myString = tuple.getString("myString");
        myString = myString.toUpperCase();
        if (reverseString){
        	myString = Reverse.reverse(myString);
        }
        outTuple.setString("myString", myString);
        numCharacters.incrementValue(myString.length());
        // Submit new tuple to output port 0
        outStream.submit(outTuple);
    }
    ~~~~~~
5.	Once you save and build your test application, in the instance graph you will be able to hover over the StringToCaps operator and see a live update of numCharacters. 
<img src="/streamsx.documentation/images/metrics.png" alt="Streams Studio" style="width: 60%;"/>

###Annotation parameters:

*	**name** - Used in @PrimitiveOperator and @Parameters.    
*	**namespace** - Used in @PrimitiveOperator. Defines namespace of the operator. 
*	**description** - Used in all annotations. This element provides a textual description of the operator and its functionality. Streams Studio also shows this description to developers using your operator in SPL applications.   
*	**cardinality** - Used in all @InputPortSet, @OutputPortSet, and @Parameter. This element indicates the number of values allowed for a parameter. A value of minus 1 (-1) indicates that the parameter can take any number of values.   
*	**optional** - Used in @InputPortSet, @OutputPortSet, and @Parameter. Defines whether a port or parameter is required.    
*	**type** - Used in the @Parameter. This element indicates the SPL type of the parameter and determines the values that the parameter can assume.   



