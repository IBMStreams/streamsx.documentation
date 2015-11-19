---
layout: docs
title:  Java Operator Development Guide
description:  IBM Streams Java Operator Development Guide
published: true
---
#  Introduction 

Java is a deeply integrated part of Streams. Making Java easy in Streams has been a priority for years because of its extensive libraries and huge developer base. The goal of this guide is to take a two-tiered approach. The videos and instructions are going to help you get your Java operators up and running as quickly and easily as possible. Streams Studio abstracts many details away from the developer, so we also go more into depth on how Java and Streams work together, rather than solely focusing on the easiest path. Following the CLI versions of instructions will give you a deeper understanding of Java operators in Streams, while following the videos and Streams Studio instructions will make you fast. 

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

<div class="alert alert-success" role="alert"><b>Thread Safety:</b> Aside from the initialize(...) method, all other methods from the Operator interface can be called concurrently from multiple threads.  For the operator to work correctly, you must ensure that these methods implemented in a thread-safe manner.</div>

##**Creating Your First Java Operator**

<div class="modal-body">
	<video controls width="60%" src="https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/11/JavaOpIn1Min5.mp4"></video>
</div>

In our first Java primitive operator, we will create an operator that converts a string from the incoming tuple to all upper case.  This example is really simple, but it demonstrates some basic concepts about Java primitive operator.  

<pre><code><b>@PrimitiveOperator()
@InputPorts(@InputPortSet(cardinality=1))
@OutputPorts(@OutputPortSet(cardinality=1))</b>
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

Key points to note from this example:

* **Extend AbstractOperator** - Java primitive operator needs to implement the `Operator` interface. The simplest way to do that is to extend from the `AbstractOperator` and override the methods that you want to customize. In this cases, the **process()** method is the only method that needs to be overridden. 

* **@PrimitiveOperator** - The `@PrimitiveOperator` annotation marks the `StringToCap` class to be the implementation class of a Java primitive operator.  The SPL compiler looks for any classes that has this annotation and will include it as part of the containing Streams toolkit.  You may configure other high-level operator properties such as operator name, namespace and description using this annotation.

* **@InputPorts** - Defines one or more `@InputPortSets` that describe the ports for incoming tuples.  
    * **@InputPortSet** - Contains the property definitions for one or more ports. The available properties are description, cardinality, optional, windowingMode, and windowPunctuationInputMode. Only the last `@InputPortSet` within an `@InputPorts` definition can have a cardinality of -1 (define multiple input ports).
    
* **@OutputPorts** - Defines one or more @OutputPortSets that describe the ports for outgoing tuples.   
    * **@OutputPortSet** - Contains the property definitions for one or more ports. The available properties are description, cardinality, optional, windowingMode, and windowPunctuationInputMode. Only the last `@OutputPortSet` within an `@OutputPorts` definition can have a cardinality of -1 (define multiple input ports).   
    
* **process(StreamingInput&lt;Tuple&gt; inputStream, Tuple tuple)** - This is the main method that gets called when a tuple is received by the operator.  In our example, the operator gets the `myString` attribute from the incoming stream.  It converts the string to upper case, and assigns the resulting string to the output tuple.  The operator then submits the output tuple to the output port.  This example demonstrates a common pattern in the process method for Java primitive operator:
    1. Get attributes that you want to manipulate from the incoming tuple using getter methods. 
	1. Manipulate the attributes in the desired way. 
	1. Write attributes to the output tuple using setter methods. 
	1. Submit output tuple. 

<div class="alert alert-success" role="alert"><b>Tip:</b> The performance of your Java primitive operator is highly dependent on how efficient the process method is.  See Performance section later for details.</div>

###Building Java Primitive Operator

<ul class="nav nav-tabs">
  <li class="active"><a data-toggle="tab" href="#command-0">Build with Command-line</a></li>
  <li><a data-toggle="tab" href="#studio-0">Build with Streams Studio</a></li>
</ul>

<div class="tab-content">
  <div id="command-0" class="tab-pane fade in active">
  <br>
  The steps for building the simple Java primitive operator from above on the command line are as follows:
  <br><br>
<ol>
	<li>Create a directory for your SPL toolkit (MyJavaOp in this case). Create these directories as well: </li>
	<pre><code>MyJavaOp/impl/java/src/
MyJavaOp/impl/java/src/stringToCaps
MyJavaOp/impl/java/bin/
</code></pre>
	<li>Place your StringToUpper.java operator class in <pre>MyJavaOp/impl/java/src/stringToCaps</pre></li>
	<li>Compile the Java operator class from the SPL toolkit directory using:</li>
	<pre><code>javac -cp $Streams_Install/lib/com.ibm.streams.operator.jar impl/java/src/stringToCaps/StringToCaps.java -d impl/java/bin/</code></pre>
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
	<li>In the generated template, StringToCaps.java, modify the process operator to look like the example above.</li>
	<li>Save your changes and Studio will automatically build your operator model and create the toolkit directory structure.</li> 
</ol>
  </div>
</div>
<br>

When the Java compiler is run, by having the com.ibm.streams.operator.jar file in the class path, the Java compiler invokes the Streams annotation processor to process the annotations on the Java primitive operator class.  The Streams annotation processor generates an `operatorName$StreamsModel.class' which contains all the information required to run the Java operator from SPL.  Using this information, the annotation processor then generates the operator model for the Java primitive operator.  

When `spl-make-toolkit` is run, the toolkit indexer scans the toolkit for operator model.  It includes operators defined in the operator model into the toolkit index.  This step is required to make the Java primitive operator accessible from SPL.

You should find the generated operator model here: 

~~~~~~
<SPL toolkit>/<operator namespace>/<operator name>/<operator name>.xml
~~~~~~   

<div class="alert alert-danger" role="alert"><b>IMPORTANT: </b>Do not modify the generated operator model.  Any changes made to the model will be overwritten when the toolkit is built.  To modify the operator model, use annotations.</div>
 
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
* **toolkit.xml** - a generated resource by the SPL toolkit indexing processing.  This file should not be modified and is used by the compiler and various components in Streams.
* **[name-space]** - similar to packages in Java, allow you to group related SPL toolkit artifacts together.
    * **[operator]** - a directory containing all artifacts relative to a Java / C++ primitive operator.  Each operator has its own separate directory.
* **impl** - the impl directory contains implementation code of primitive operators or native functions
    * **impl/java/src** - contains Java primitive operator or native function code
    * **impl/java/bin** - contains Java class files for the Java implementation code
* **lib** - contains any external libraries that this toolkit may require

Note:  If you use Streams Studio to create a new SPL project, Streams Studio will automatically create the correct directory structure for you.	
	

##Running and Testing Your Operator

<div class="modal-body">
	<video controls width="60%" src="https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/11/TestJavaOp2Min3.mp4"></video>
</div>

The best way to start testing your Java operator is to create a simple SPL application. The flow of a simple test application is typically **Beacon -> Java Operator -> FileSink.** Here are the steps I took to build an application in 2 minutes using Studio (I won't go into the CLI approach, since it is the same as with an Streams application): 

**Project Setup**

1.	File -> New -> Project   
2.	Expand InfoSphere Streams Studio   
3.	Select SPL Application Project   
4.	Name your project (TestJavaOp in this case)  
5.	Click Next  
6.	Add a dependency on your Java operator project 
7.	Click Finish

**Application Development**

<img src="/streamsx.documentation/images/JavaOperatorGuide/testApp.png" alt="Streams Studio" style="width: 60%;"/> 

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
11.	Save and let the application automatically build. Code will look like this:   
	<pre style="font-family: Andale Mono, Lucida Console, Monaco, fixed, monospace; color: #000000; background-color: #eee;font-size: 12px;border: 1px dashed #999999;line-height: 14px;padding: 5px; overflow: auto; width: 100%"><code>    namespace application ;
	
	    use stringToCaps::StringToCaps ;
	
	    composite TestJavaOp
	    {
	        graph
	            (stream&lt;rstring myString&gt; Beacon_1_out0) as Beacon_1 = Beacon()
	            {
	                param
	                    period : 1.0 ;
	                output
	                    Beacon_1_out0 : myString = &quot;lowercase&quot; +(rstring) IterationCount() ;
	            }
	
	            (stream&lt;rstring myString&gt; StringToCaps_2_out0) as StringToCaps_2 =
	                <b>StringToCaps</b>(Beacon_1_out0){}
	
	            () as FileSink_3 = FileSink(StringToCaps_2_out0 as inputStream)
	            {
	                param
	                    file : &quot;results.txt&quot; ;
	                    flush : 1u;
	            }
	    }
	</code></pre>

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
**<font color="blue">@Libraries</font>** - This operator annotation tells your operator where to find the JARs that it needs during execution in a Streams environment. 

Options for how to specify the path:

* Specific JARs: `@Libraries("opt/Reverse.jar")`
* Entire directories using "*": `@Libraries("opt/*")`
* Environment variables: `@Libraries("@REVERSE_HOME@")` where the environment variable would be REVERSE_HOME. 

To specify multiple locations for JARs, simply comma separate your locations:  
	`@Libraries("opt/Reverse.jar" , "opt/downloaded/*", "@REVERSE_HOME@")`

<div class="modal-body">
	<video controls width="60%" src="https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/11/AddingJar2.mp4"></video>
</div>

The example above uses a JAR with a simple function that reverses a String [(download here)](/streamsx.documentation/images/JavaOperatorGuide/reverse.tar). Here are the steps taken to leverage that code: 


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

<ul class="nav nav-tabs">
  <li class="active"><a data-toggle="tab" href="#command-1">Build with Command-line</a></li>
  <li><a data-toggle="tab" href="#studio-1">Build with Streams Studio (Video Steps)</a></li>
</ul>

<div class="tab-content">
  <div id="command-1" class="tab-pane fade in active">
  <br>
   The steps for using an external JAR with the command-line are as follows: 
<br><br>
<ol>  
	<li>In your Java operator project toolkit directory, create an opt/ directory. Place the Reverse.jar file in the MyJavaOp/opt/ directory.</li> 
	<li>In your operator Java code, import the package: </li>
	<pre><code>import reverse.Reverse;</code></pre>
	<li>Use the @Libraries annotation to add the JAR to the operator's class path. The @Libraries parameter can be placed above the operator class definition with the other annotations (If you ever get "class not found" exceptions once you submit your job, check your @Libraries annotation first). </li> 
	<pre><code>@Libraries("opt/Reverse.jar")</code></pre>
	<li>Go down to the process method, and before setting the "myString" attribute, add this line to reverse the String: </li>
<pre style="font-family: Andale Mono, Lucida Console, Monaco, fixed, monospace; color: #000000; background-color: #eee;font-size: 12px;border: 1px dashed #999999;line-height: 14px;padding: 5px; overflow: auto; width: 100%"><code>    @Override
    public final void process(StreamingInput&lt;Tuple&gt; inputStream, Tuple tuple)
            throws Exception {
        // Create a new tuple for output port 0
        StreamingOutput&lt;OutputTuple&gt; outStream = getOutput(0);
        OutputTuple outTuple = outStream.newTuple();
        
        // Get attribute from input tuple and manipulate
        String myString = tuple.getString(&quot;myString&quot;);
        myString = myString.toUpperCase();
        <font color="blue"><b>myString = Reverse.reverse(myString);</b></font>
        outTuple.setString(&quot;myString&quot;, myString);
        
        // Submit new tuple to output port 0
        outStream.submit(outTuple);
    } 
</code></pre>
	<li>Compile the Java operator class as you did before, but add the JAR to the class path:</li>
	<pre><code>javac -cp $Streams_Install/lib/com.ibm.streams.operator.jar<font color="blue">:opt/Reverse.jar</font> impl/java/src/stringToCaps/StringToCaps.java -d impl/java/bin/</code></pre>
	<li>Index the toolkit again.</li>
	<pre><code>spl-make-toolkit -i ./</code></pre>
	<li>Rebuild your test application and submit. The output in results.txt will look like this:</li>
	<pre><code>	"0ESACREWOL"
	"1ESACREWOL"
	"2ESACREWOL"
	"3ESACREWOL"</code></pre>
</ol> 
  </div>
  <div id="studio-1" class="tab-pane fade">
  <br>
   The steps for using an external JAR with Streams Studio are as follows: 
<br><br>
<ol>  
	<li>In your Java operator project folder, create an opt directory. Add the Reverse.jar file to it.</li> 
	<li>In the Project Explorer, refresh your Resources folder and expand opt. Right-click on Reverse.jar and select Build Path -> Add to Build Path. </li> 
	<li>Import the package: </li>
	<pre><code>import reverse.Reverse;</code></pre>
	<li>Use the @Libraries annotation to add the JAR to the operator's class path. (If you ever get "class not found" exceptions once you submit your job, check your @Libraries annotation first). </li> 
	<pre><code>@Libraries("opt/Reverse.jar")</code></pre>
	<li>Go down to the process method, and before setting the "myString" attribute, add this line to reverse the String: </li>
<pre style="font-family: Andale Mono, Lucida Console, Monaco, fixed, monospace; color: #000000; background-color: #eee;font-size: 12px;border: 1px dashed #999999;line-height: 14px;padding: 5px; overflow: auto; width: 100%"><code>    @Override
    public final void process(StreamingInput&lt;Tuple&gt; inputStream, Tuple tuple)
            throws Exception {
        // Create a new tuple for output port 0
        StreamingOutput&lt;OutputTuple&gt; outStream = getOutput(0);
        OutputTuple outTuple = outStream.newTuple();
        
        // Get attribute from input tuple and manipulate
        String myString = tuple.getString(&quot;myString&quot;);
        myString = myString.toUpperCase();
        <font color="blue"><b>myString = Reverse.reverse(myString);</b></font>
        outTuple.setString(&quot;myString&quot;, myString);
        
        // Submit new tuple to output port 0
        outStream.submit(outTuple);
    } 
</code></pre>
	<li>Save and let Studio automatically build your toolkit.</li>
	<li>Rebuild your test application and submit. The output in results.txt will look like this:</li>
	<pre><code>	"0ESACREWOL"
	"1ESACREWOL"
	"2ESACREWOL"
	"3ESACREWOL"</code></pre>
</ol>
  </div>
</div>


##Making Your Operator Generic with Parameters

Most operators will take in some kind of parameters from the SPL application. This allows your operator to be more generic, and usable under diverse circumstances. 

####New Annotation
**<font color="blue">@Parameter</font>** - This operator annotation allows you to pass in configurations from the param section of the operator definition in an SPL application. 

<div class="modal-body">
	<video controls width="60%" src="https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/11/AddParameter2.mp4"></video>
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
**<font color="blue">@CustomMetric</font>** - This operator annotation allows you to define your own custom metrics that will be visible to the SPL runtime. Live feed of this metric can be viewed in Streams Studio and the Streams Console.

The **@CustomMetric** annotation can take four parameters. **name** and **description** as they are used in other annotations, and then **kind** and **mxbean** which are unique to @CustomMetric:

* **kind** - This describes the type of metric that is being provided. It can take one of three values as defined in the Metric.Kind enumeration:
	* **Counter** indicates that this metric represents a count of occurrence of some event. 
	* **Gauge** indicates a value that is continuously variable with time. 
	* **Time** indicates a metric that represents a point in time.
* **mxbean** - This Boolean indicates whether to register this metric into the platform's MBean server. The default value is false. 

<div class="modal-body">
	<video controls width="60%" src="https://developer.ibm.com/streamsdev/wp-content/uploads/sites/15/2015/11/AddingMetrics2.mp4"></video>
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
5.	Once you save and build your toolkit and test application, submit your application. In the instance graph view in Studio, you will be able to hover over the StringToCaps operator and see a live update of numCharacters. 

	<img src="/streamsx.documentation/images/metrics.png" alt="Streams Studio" style="width: 60%;"/>

##Creating a Source Operator
Source operators are unique because they don't rely on an incoming tuple to trigger the sending of an output tuple. Source operators are typically used to bring data into your Streams application from an external source such as a database or messaging server.

Here is the best-practices recipe for a Source operator:  

1. Override the **initialize()** method to:
	1. Initialize the AbstractOperator super class: `super.initialize(context)` 
	1. Setup connections with external data sources.
	2. Initialize base state for the operator.
	3. Create a thread that will produce tuples using the produceTuples() method.
2. Override the **allPortsReady()** method to start your production thread. 
3. Use a **produceTuples()** to generate tuples. Typically this is done within a while loop that terminates on operator shutdown. 
4. Override the **shutdown()** method to:
	1. Interrupt your production thread. 
	2. Close and cleanup connections to external data sources. 
	3. Shutdown the AbstractOperator super class: `super.shutdown()` 
	
`Video showing how to create a Source operator`

The simple source operator in the video above and the code below generates a string of random length based on the `stringBase` variable.  

<ul class="nav nav-tabs">
  <li class="active"><a data-toggle="tab" href="#minimum-0">Code</a></li>
  <li><a data-toggle="tab" href="#fullsource-0">Full Source</a></li>
</ul>

<div class="tab-content">
  <div id="minimum-0" class="tab-pane fade in active">
<pre><code>@PrimitiveOperator()
@OutputPorts(@OutputPortSet(cardinality=1))
public class ServerSource extends AbstractOperator {
    private Thread processThread;
    private Server server;
    private boolean shutdown = false;
    
    @Override
    public synchronized void initialize(OperatorContext context)
            throws Exception {
        // Must call super.initialize(context) to correctly setup an operator.
        super.initialize(context);
  
        server = new Server();
        server.initialize(&quot;myUser&quot;, &quot;myPassw0rd&quot;);

        processThread = getOperatorContext().getThreadFactory().newThread(
                new Runnable() {

                    @Override
                    public void run() {
                        try {
                            produceTuples();
                        } catch (Exception e) {
                            Logger.getLogger(this.getClass()).error(&quot;Operator error&quot;, e);
                        }                    
                    }
                    
                });
        
        processThread.setDaemon(false);
    }
    
    @Override
    public synchronized void allPortsReady() throws Exception {
        processThread.start();
    }
    
    private void produceTuples() throws Exception  {
        final StreamingOutput&lt;OutputTuple&gt; out = getOutput(0);
        
        OutputTuple tuple = out.newTuple();
        while(!shutdown ){
            String myString = server.getData();
            tuple.setString(&quot;myString&quot;, myString);
            out.submit(tuple);
            Thread.sleep(1000);
        }        
    }
    
    public synchronized void shutdown() throws Exception {
        shutdown = true;
        if (processThread != null) {
            processThread.interrupt();
            processThread = null;
        }
        server.disconnect();
        super.shutdown();
    }
    
}
</code></pre>  
  </div>
  <div id="fullsource-0" class="tab-pane fade">
<pre><code>package serverSource;

import org.apache.log4j.Logger;

import com.ibm.streams.operator.AbstractOperator;
import com.ibm.streams.operator.OperatorContext;
import com.ibm.streams.operator.OutputTuple;
import com.ibm.streams.operator.StreamingOutput;
import com.ibm.streams.operator.model.OutputPortSet;
import com.ibm.streams.operator.model.OutputPorts;
import com.ibm.streams.operator.model.PrimitiveOperator;

@PrimitiveOperator()
@OutputPorts(@OutputPortSet(cardinality=1))
public class ServerSource extends AbstractOperator {
    private Thread processThread;
    private Server server;
    private boolean shutdown = false;
    
     /*
     * Initialize this operator. Called once before any tuples are processed.
     * @param context OperatorContext for this operator.
     * @throws Exception Operator failure, will cause the enclosing PE to terminate.
     */
    @Override
    public synchronized void initialize(OperatorContext context)
            throws Exception {
        // Must call super.initialize(context) to correctly setup an operator.
        super.initialize(context);
  
        server = new Server();
        server.initialize(&quot;myUser&quot;, &quot;myPassw0rd&quot;);

        /*
         * Create the thread for producing tuples. 
         * The thread is created at initialize time but started.
         * The thread will be started by allPortsReady().
         */
        processThread = getOperatorContext().getThreadFactory().newThread(
                new Runnable() {

                    @Override
                    public void run() {
                        try {
                            produceTuples();
                        } catch (Exception e) {
                            Logger.getLogger(this.getClass()).error(&quot;Operator error&quot;, e);
                        }                    
                    }
                    
                });
        
        /*
         * Set the thread not to be a daemon to ensure that the SPL runtime
         * will wait for the thread to complete before determining the
         * operator is complete.
         */
        processThread.setDaemon(false);
    }
    
    /**
     * Notification that initialization is complete and all input and output ports 
     * are connected and ready to receive and submit tuples.
     * @throws Exception Operator failure, will cause the enclosing PE to terminate.
     */
    @Override
    public synchronized void allPortsReady() throws Exception {
        processThread.start();
    }
    
    /**
     * Submit new tuples to the output stream
     * @throws Exception if an error occurs while submitting a tuple
     */
    private void produceTuples() throws Exception  {
        final StreamingOutput&lt;OutputTuple&gt; out = getOutput(0);
        
        OutputTuple tuple = out.newTuple();
        while(!shutdown ){
            String myString = server.getData();
            tuple.setString(&quot;myString&quot;, myString);
            out.submit(tuple);
            Thread.sleep(1000);
        }        
    }
    
    /**
     * Shutdown this operator, which will interrupt the thread
     * executing the &lt;code&gt;produceTuples()&lt;/code&gt; method.
     * @throws Exception Operator failure, will cause the enclosing PE to terminate.
     */
    public synchronized void shutdown() throws Exception {
        shutdown = true;
        if (processThread != null) {
            processThread.interrupt();
            processThread = null;
        }
        server.disconnect();
        super.shutdown();
    }
    
}
</code></pre>
  </div>
</div>

##Handling Errors
Your Streams operator should never crash unless you want it to. There are cases where an exception will be thrown because of a loss of connection or other normal error causes, but it is important to handle those errors so that your operator can continue to produce and process tuples. 

When an exception is thrown, the best-practice response is to:

1. Catch the exception. 
2. Log the exception as an error in the operator log. 
3. Write the error out to an error port. 

There are some cases where you will actually want your operator to fail. These cases are typically only during the initial startup of your operator and are usually related to bad configuration, connections, or parameters. 

In the code below, we enhanced our ServerSource operator to include error handling in the produceTuples() method. 

<ul class="nav nav-tabs">
  <li class="active"><a data-toggle="tab" href="#minimum-1">Modified Sections</a></li>
  <li><a data-toggle="tab" href="#fullsource-1">Full Source</a></li>
</ul>

<div class="tab-content">
  <div id="minimum-1" class="tab-pane fade in active">
<pre><code>@PrimitiveOperator()
@OutputPorts({@OutputPortSet(cardinality=1),<b>@OutputPortSet(description=&quot;Error Port&quot;, cardinality=1)</b>})
public class ServerSource extends AbstractOperator {
    private Thread processThread;
    private Server server;
    private boolean shutdown = false;
    <b>private Logger trace = Logger.getLogger(this.getClass());</b>
	.
	.
	.
    private void produceTuples() throws Exception  {
        final StreamingOutput&lt;OutputTuple&gt; out = getOutput(0);
        <b>final StreamingOutput&lt;OutputTuple&gt; error = getOutput(1);</b>
        
        OutputTuple tuple = out.newTuple();
        while(!shutdown ){
            <b>try{
                String myString = server.getData();
                tuple.setString(&quot;myString&quot;, myString);
                out.submit(tuple);
                Thread.sleep(1000);
            } catch (Exception e){
                trace.log(TraceLevel.ERROR, &quot;Error submitting tuple. Message: &quot; + e.toString());
                OutputTuple errorTuple = error.newTuple();
                errorTuple.setString(&quot;error_message&quot;, &quot;Error submitting tuple. Message: &quot; + e.toString());
                error.submit(errorTuple);
            }</b>
        }      
    }  
}
</code></pre>  
  </div>
  <div id="fullsource-1" class="tab-pane fade">
<pre><code>package serverSource;

<b>import org.apache.log4j.Logger;</b>
import com.ibm.streams.operator.AbstractOperator;
import com.ibm.streams.operator.OperatorContext;
import com.ibm.streams.operator.OutputTuple;
import com.ibm.streams.operator.StreamingOutput;
import com.ibm.streams.operator.log4j.TraceLevel;
import com.ibm.streams.operator.model.OutputPortSet;
import com.ibm.streams.operator.model.OutputPorts;
import com.ibm.streams.operator.model.PrimitiveOperator;

@PrimitiveOperator()
@OutputPorts({@OutputPortSet(cardinality=1),<b>@OutputPortSet(description=&quot;Error Port&quot;, cardinality=1)</b>})
public class ServerSource extends AbstractOperator {
    private Thread processThread;
    private Server server;
    private boolean shutdown = false;
    <b>private Logger trace = Logger.getLogger(this.getClass());</b>
    
    @Override
    public synchronized void initialize(OperatorContext context)
            throws Exception {
        super.initialize(context);
  
        server = new Server();
        server.initialize(&quot;myUser&quot;, &quot;myPassw0rd&quot;);

        processThread = getOperatorContext().getThreadFactory().newThread(
                new Runnable() {

                    @Override
                    public void run() {
                        try {
                            produceTuples();
                        } catch (Exception e) {
                            Logger.getLogger(this.getClass()).error(&quot;Operator error&quot;, e);
                        }                    
                    }
                    
                });
        
        processThread.setDaemon(false);
    }
    
    @Override
    public synchronized void allPortsReady() throws Exception {
        processThread.start();
    }

    private void produceTuples() throws Exception  {
        final StreamingOutput&lt;OutputTuple&gt; out = getOutput(0);
        <b>final StreamingOutput&lt;OutputTuple&gt; error = getOutput(1);</b>
        
        OutputTuple tuple = out.newTuple();
        while(!shutdown ){
            <b>try{
                String myString = server.getData();
                tuple.setString(&quot;myString&quot;, myString);
                out.submit(tuple);
                Thread.sleep(1000);
            } catch (Exception e){
                trace.log(TraceLevel.ERROR, &quot;Error submitting tuple. Message: &quot; + e.toString());
                OutputTuple errorTuple = error.newTuple();
                errorTuple.setString(&quot;error_message&quot;, &quot;Error submitting tuple. Message: &quot; + e.toString());
                error.submit(errorTuple);
            }</b>
        }      
    }
    
    public synchronized void shutdown() throws Exception {
        shutdown = true;
        if (processThread != null) {
            processThread.interrupt();
            processThread = null;
        }
        server.disconnect();
        super.shutdown();
    }
    
}
</code></pre>
  </div>
</div>

##Adding Compile-Time and Runtime Checks
Adding compile-time checks to your Java operator can be useful for a variety of reasons and is done using the **@ContextCheck**. Here are some common checks:

* Check to see if an operator that does not support consistent region is within a consistent region. 
* Check incoming and outgoing port schemas. Make sure that the attributes you require are available at an SPL level. 
* More ideas??

**@ContextCheck** - This operator annotation allows you to run checks at operator compile-time or before the initialize() method is called at runtime. The check is done by creating a public static method that takes an argument of type `OperatorContextChecker`. At runtime @ContextCheck methods are invoked before invocation of @Parameter annotated methods. The compile-time and runtime checks use Boolean values (default is compile = true):

* `@ContextCheck(compile = true)`
* `@ContextCheck(runtime = true)`


The following example is part of the StringToCaps operator. We have added compile-time checks to make sure that the incoming and outgoing SPL streams have an attribute named "myString" that is of type `rstring`. This code is placed inside the StringToCaps operator definition. If any of the checks run by `checker` fail, the compile is interrupted with an error message. 

<pre style="font-family: Andale Mono, Lucida Console, Monaco, fixed, monospace; color: #000000; background-color: #eee;font-size: 12px;border: 1px dashed #999999;line-height: 14px;padding: 5px; overflow: auto; width: 100%"><code>    @ContextCheck
    public static void checkAttributes(OperatorContextChecker checker){
        OperatorContext context = checker.getOperatorContext();
        
        //Check that myString attributes exist
        <b>checker.checkRequiredAttributes(context.getStreamingInputs().get(0), &quot;myString&quot;);
        checker.checkRequiredAttributes(context.getStreamingOutputs().get(0), &quot;myString&quot;);</b>
        
        //Check the myString attributes are of correct type
        Attribute incoming = context.getStreamingInputs().get(0).getStreamSchema().getAttribute(&quot;myString&quot;);
        <b>checker.checkAttributeType(incoming, Type.MetaType.RSTRING);</b>
        Attribute outgoing = context.getStreamingOutputs().get(0).getStreamSchema().getAttribute(&quot;myString&quot;);
        <b>checker.checkAttributeType(outgoing, Type.MetaType.RSTRING);</b>
    }
</code></pre>

##Using Windows

<ul class="nav nav-tabs">
  <li class="active"><a data-toggle="tab" href="#minimum-3">Code</a></li>
  <li><a data-toggle="tab" href="#fullsource-3">Full Source</a></li>
</ul>

<div class="tab-content">
  <div id="minimum-3" class="tab-pane fade in active">
<pre><code>@PrimitiveOperator()
@InputPorts(@InputPortSet(cardinality=1, windowingMode=WindowMode.Windowed))
@OutputPorts(@OutputPortSet(cardinality=1))
public class WindowConcatenator extends AbstractWindowOperator {
    @Override
    public synchronized void initialize(OperatorContext context)
            throws Exception {
        super.initialize(context);
        getInput(0).getStreamWindow().registerListener(
                new WindowHandler(getOutput(0)), false);
        
    }
}
</code></pre>  
  </div>
  <div id="fullsource-3" class="tab-pane fade">
<pre><code>package windowConcatenator;

import org.apache.log4j.Logger;

import com.ibm.streams.operator.AbstractOperator;
import com.ibm.streams.operator.OperatorContext;
import com.ibm.streams.operator.StreamingData.Punctuation;
import com.ibm.streams.operator.StreamingInput;
import com.ibm.streams.operator.Tuple;
import com.ibm.streams.operator.model.InputPortSet;
import com.ibm.streams.operator.model.InputPortSet.WindowMode;
import com.ibm.streams.operator.model.InputPortSet.WindowPunctuationInputMode;
import com.ibm.streams.operator.model.InputPorts;
import com.ibm.streams.operator.model.Libraries;
import com.ibm.streams.operator.model.OutputPortSet;
import com.ibm.streams.operator.model.OutputPortSet.WindowPunctuationOutputMode;
import com.ibm.streams.operator.model.OutputPorts;
import com.ibm.streams.operator.model.PrimitiveOperator;
import com.ibm.streams.operator.window.AbstractWindowOperator;


@PrimitiveOperator()
@InputPorts(@InputPortSet(cardinality=1, windowingMode=WindowMode.Windowed))
@OutputPorts(@OutputPortSet(cardinality=1))
public class WindowConcatenator extends AbstractWindowOperator {
    @Override
    public synchronized void initialize(OperatorContext context)
            throws Exception {
        super.initialize(context);
        getInput(0).getStreamWindow().registerListener(
                new WindowHandler(getOutput(0)), false);
        
    }
}

</code></pre>
</code></pre>
  </div>
</div>

<ul class="nav nav-tabs">
  <li class="active"><a data-toggle="tab" href="#minimum-4">Code</a></li>
  <li><a data-toggle="tab" href="#fullsource-4">Full Source</a></li>
</ul>

<div class="tab-content">
  <div id="minimum-4" class="tab-pane fade in active">
<pre><code>public class WindowHandler implements StreamWindowListener&lt;Tuple&gt; {
    private int tupleCount;
    private String myConcatenatedString = &quot;&quot;;
    private final StreamingOutput&lt;OutputTuple&gt; output;
    
    public WindowHandler(StreamingOutput&lt;OutputTuple&gt; output) {
          this.output = output;
        }
    
    @Override
    public synchronized void handleEvent(StreamWindowEvent&lt;Tuple&gt; event) throws Exception {
        
        switch (event.getType()) {
        case INSERTION:
            for (Tuple tuple : event.getTuples()){
                String myString = tuple.getString(&quot;myString&quot;);
                myConcatenatedString += myString;
                tupleCount++;
            }
            break;
        case EVICTION:
            if (tupleCount != 0){
                OutputTuple tuple = output.newTuple();
              tuple.setString(&quot;myString&quot;, myConcatenatedString);
              output.submit(tuple);
              output.punctuate(Punctuation.WINDOW_MARKER);
              myConcatenatedString = &quot;&quot;;
              tupleCount= 0;
            }
            break;
        case FINAL:
            // handle final mark
            break;
        default:
            break;
        } 
    }
}
</code></pre>  
  </div>
  <div id="fullsource-4" class="tab-pane fade">
<pre><code>package windowConcatenator;

import com.ibm.streams.operator.OutputTuple;
import com.ibm.streams.operator.StreamingData.Punctuation;
import com.ibm.streams.operator.StreamingOutput;
import com.ibm.streams.operator.Tuple;
import com.ibm.streams.operator.window.StreamWindowEvent;
import com.ibm.streams.operator.window.StreamWindowListener;

public class WindowHandler implements StreamWindowListener&lt;Tuple&gt; {
    private int tupleCount;
    private String myConcatenatedString = &quot;&quot;;
    private final StreamingOutput&lt;OutputTuple&gt; output;
    
    public WindowHandler(StreamingOutput&lt;OutputTuple&gt; output) {
          this.output = output;
        }
    
    @Override
    public synchronized void handleEvent(StreamWindowEvent&lt;Tuple&gt; event) throws Exception {
        
        switch (event.getType()) {
        case INSERTION:
            for (Tuple tuple : event.getTuples()){
                String myString = tuple.getString(&quot;myString&quot;);
                myConcatenatedString += myString;
                tupleCount++;
            }
            break;
        case EVICTION:
            if (tupleCount != 0){
                OutputTuple tuple = output.newTuple();
              tuple.setString(&quot;myString&quot;, myConcatenatedString);
              output.submit(tuple);
              output.punctuate(Punctuation.WINDOW_MARKER);
              myConcatenatedString = &quot;&quot;;
              tupleCount= 0;
            }
            break;
        case FINAL:
            // handle final mark
            break;
        default:
            break;
        } 
    }
}

</code></pre>
</code></pre>
  </div>
</div>



##References

####Annotation parameters:

*	**name** - Used in @PrimitiveOperator and @Parameters.    
*	**namespace** - Used in @PrimitiveOperator. Defines namespace of the operator. 
*	**description** - Used in all annotations. This element provides a textual description of the operator and its functionality. Streams Studio also shows this description to developers using your operator in SPL applications.   
*	**cardinality** - Used in all @InputPortSet, @OutputPortSet, and @Parameter. This element indicates the number of values allowed for a parameter. A value of minus 1 (-1) indicates that the parameter can take any number of values.   
*	**optional** - Used in @InputPortSet, @OutputPortSet, and @Parameter. Defines whether a port or parameter is required.    
*	**type** - Used in the @Parameter. This element indicates the SPL type of the parameter and determines the values that the parameter can assume.   



