---
layout: docs
title:  Java Operator Development Guide
description:  IBM Streams Java Operator Development Guide
weight: 10
---
#  Introduction

Java is a deeply integrated part of Streams. Making Java easy in Streams has been a priority for years because of its extensive libraries and huge developer base. The goal of this guide is to take a two-tiered approach. The videos and instructions are going to help you get your Java operators up and running as quickly and easily as possible. Streams Studio abstracts many details away from the developer, so we also go more into depth on how Java and Streams work together, rather than solely focusing on the easiest path. Following the CLI versions of instructions will give you a deeper understanding of Java operators in Streams, while following the videos and Streams Studio instructions will make you fast.

#  Java Operator Development Guide

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
<iframe width="560" height="315" src="https://www.youtube.com/embed/3B_IO3U2xVY" frameborder="0" allowfullscreen></iframe>
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

* **@PrimitiveOperator** - The `@PrimitiveOperator` annotation marks the `StringToCap` class to be the implementation class of a Java primitive operator.  The toolkit indexer looks for any classes that has this annotation and will include it as part of the containing Streams toolkit.  You may configure other high-level operator properties such as operator name, namespace and description using this annotation.

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

<div class="alert alert-info" role="alert"><b>Best Practice: </b>In our example, we used com.ibm.streams.operator.jar to demonstrate key concepts with Java primitive operator.  As a best practice, you should include the com.ibm.streams.operator.samples.jar in the classpath.  This jar provides common patterns, like source and sink operators, that you can extend when implementing your Java primitive operator.   For more details, refer to <a href="https://www-01.ibm.com/support/knowledgecenter/#!/SSCRJU_4.1.0/com.ibm.streams.spl-java-operators.doc/samples/overview-summary.html">Java Primitive Operator Sample Javadoc</a></div>

When `spl-make-toolkit` is run, the toolkit indexer scans the toolkit for operator model.  It includes operators defined in the operator model into the toolkit index.  This step is required to make the Java primitive operator accessible from SPL.

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
	<iframe width="560" height="315" src="https://www.youtube.com/embed/CZNXqQCBASU" frameborder="0" allowfullscreen></iframe>
</div>

### SPL Toolkit Dependency

The best way to start testing your Java operator is to create a simple SPL application. Typically, you want this test application in a separate SPL toolkit, such that the test code is independent from the Java primitive operator.  We will create a new toolkit called `TestJavaOp`.

For your test application to be able to access the Java primitive operator, the `TestJavaOp` toolkit must specify the toolkit that contains the Java primitive operator as part of its toolkit dependency.

At the root of the `TestJavaOp` toolkit, create a file named `info.xml`.  In the info.xml, specify toolkit dependency:

~~~~~~
<?xml version="1.0" encoding="UTF-8"?>
<info:toolkitInfoModel xmlns:common="http://www.ibm.com/xmlns/prod/streams/spl/common" xmlns:info="http://www.ibm.com/xmlns/prod/streams/spl/toolkitInfo">
  <info:identity>
    <info:name>TestJavaOp</info:name>
    <info:description></info:description>
    <info:version>1.0.0</info:version>
    <info:requiredProductVersion>4.1.0.0</info:requiredProductVersion>
  </info:identity>
  <info:dependencies>
    <info:toolkit>
      <common:name>MyJavaOp</common:name>
      <common:version>[1.0.0,2.0.0)</common:version>
    </info:toolkit>
  </info:dependencies>
</info:toolkitInfoModel>
~~~~~~

* We specify `MyJavaOp` toolkit as a dependency for `TestJavaOp`
* We specify that `TestJavaOp` depends on version `1.0.0` to `2.0.0` (exclusive) of the `TestJavaOp` toolkit.

{% include bestpractices.html text= "info.xml is an optional file for a SPL toolkit.  However, it is a best practice to always create this file.  It helps the SPL compiler builds dependency trees among other things.  This file is also used by Streams Studio to help scope content assist suggestions."%}

### Test Application

In the `TestJavaOp` toolkit, we create a test application that calls the Java primitive operator, `StringsToCap`.  A common pattern for testing a primitive operator is **Beacon -> Java Operator -> FileSink** as in the following example.

<img src="/streamsx.documentation/images/JavaOperatorGuide/testApp.png" alt="Streams Studio" style="width: 60%;"/>


SPL Code for test application:

<pre><code>
namespace application ;

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

Key points to note from this example:

* **Beacon** - The Beacon operator is provided as part of the SPL Standard Toolkit.  It is a great tool for testing primitive operators as it helps generate any kind of continuous data for testing the operator.  In the example, the `Beacon` operator generates a String of `lowercase + InterationCount()`.  `InterationCount()` is an output function provided by the Beacon operator for us to query how many tuples have been generated by the operator.
* **StringToCaps** - The output stream from the Beacon operator is fed into the StringToCap operator.  For each tuple received by this Java primitive operator, its process method is called.  In our case, the Java primitive operator converts each of the incoming Strings to uppercase and submits it out as output tuple.
* **FileSink** - The FileSink operator receives the incoming tuples from StringToCap and prints the result to a file named `results.txt`.  The `flush` parameter tells the operator to flush output to file for each tuple it has received.

**Running Test Application**

Compile and launch the `TestJavaOp` main composite.  The quickest way to test an application is to run it in stand-alone mode.  

~~~~~~
cd [root directory  of TestJavaOp toolkit]

sc -M TestJavaOp --output-directory=[build-output-dir] --data-directory=data -T -a -t ../MyJavaOp
~~~~~~

Key points to note from the command above:

* **-T** - compiles the application in stand-alone mode.  To compile in distributed mode, remove this option.
* **-t ../MyJavaOp** - specifies the toolkit path for the compiler to find the `MyJavaOp` toolkit.  Alternatively, set this location with using the STREAMS_SPL_PATH environment variable.
* **--output-directory** - specifies where the output of the compilation should go.

To run this program:

~~~~~~
cd [build-output-dir]
standalone
~~~~~~

You should see the following output:

~~~~~~
"LOWERCASE0"
"LOWERCASE1"
"LOWERCASE2"
"LOWERCASE3"
~~~~~~

You may also compile and run the application in distributed mode as shown in the video.  The output can be found in the Console log.

## Referencing External Libraries

<div class="modal-body">
	<iframe width="560" height="315" src="https://www.youtube.com/embed/H9ZB1bNs7AI" frameborder="0" allowfullscreen></iframe>
</div>

Your Java operators can take advantage of all JARs and existing Java code you already have. This makes connecting to any servers, databases, etc that have Java clients easy, and it makes converting your Java code to Streams simple.

There are two simple steps that are required to start using external libraries in your Java operator:

1.	Make JARs of interest available to the Java operator at Streams runtime.
1.	Use the @Libraries annotation to add the JARs to the operator class path.

### Accessing JARS at Runtime

When the Java primitive operator is executed, the operator code must be able to access the dependent JAR files at runtime.  In designing your operator, you need to determine how the Java primitive operator can access the external JARS.  There are two general approaches, each with its own pros and cons.

1.  Package the JAR as part of the toolkit

	In this approach, the JAR file is packaged as part of the toolkit, and eventually as part the Streams application bundle when the application is built.  This approach simplifies the set up of the distributed environment, as you do not to need to manually set up these JARS on the resources in the domain.  When the application is run and deployed, the Streams runtime automatically copy these dependencies onto the remote systems.  The disadvantage of this approach is that it makes the size of the application bundle larger.  This affects the time required to submit the application to the Streams instance.

	{% include bestpractices.html text= "External JARS should be stored in the <code>toolkit_root/opt</code> directory.  The opt directory is packaged into the application bundle by default."%}

	For more information about applicaiton bundles, refer to this documentation:  [Application bundle files](http://www-01.ibm.com/support/knowledgecenter/?lang=en#!/SSCRJU_4.1.0/com.ibm.streams.dev.doc/doc/applicationbundle.html).

2.  Using Environment Variables

	In this approach, the JAR files are stored at the same file location on all resources that can run the operator.  The operator then defines an environment variable for the end user to indicate where to find the JAR files.  When running the application, the environment variable must be set on the instance.  The advantage of this approach is that it makes the application bundle smaller, thereby, reducing the time required to submit a job to an instance.  The disadvantage is that the end user must now manually set up the environment before the operator can be used.

### Setting up Classpath

To set up the classpath for the Java primitive operator, use the **@Libraries** annotation.  This annotation sets up the classpath for the Java primitive operator at run time.  

Options for specifying classpaths using the @Libraries annotation:

* Specific JARs: `@Libraries("opt/Reverse.jar")`
* Entire directories using wildcard (this adds all files with extension .jar or .JAR): `@Libraries("opt/*")`
* Environment variables: `@Libraries("@REVERSE_HOME@")` where the environment variable would be REVERSE_HOME. **WARNING:** The environment variable is resolved at compile-time, resulting in an application bundle that is not relocatable. 

To specify multiple locations for JARs, simply comma separate your locations:  
	`@Libraries({"opt/Reverse.jar" , "opt/downloaded/*", "@REVERSE_HOME@"})`

### Sample Application


The example in the video above uses a JAR with a simple function that reverses a String [(download here)](/streamsx.documentation/images/JavaOperatorGuide/reverse.tar).

<ul class="nav nav-tabs">
  <li class="active"><a data-toggle="tab" href="#command-1">Build with Command-line</a></li>
  <li><a data-toggle="tab" href="#studio-1">Build with Streams Studio</a></li>
</ul>

<div class="tab-content">
  <div id="command-1" class="tab-pane fade in active">
  <br>
   The steps for using an external JAR with the command-line are as follows:
<br><br>
<ol>  
	<li>In your Java primitive operator toolkit directory, create an opt/ directory.  For example, place the Reverse.jar file in the MyJavaOp/opt/ directory.</li>
	<li>In your operator Java code, import the package: </li>
	<pre><code>import reverse.Reverse;</code></pre>
	<li>Use the @Libraries annotation to add the JAR to the operator's class path. The @Libraries parameter can be placed above the operator class definition with the other annotations.</li>
	<pre><code>@Libraries("opt/Reverse.jar")</code></pre>
	<li>Go down to the process method, and before setting the "myString" attribute, add this line to reverse the String: </li>

<pre><code>    @Override
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
<pre>
"0ESACREWOL"
"1ESACREWOL"
"2ESACREWOL"
"3ESACREWOL"
</pre>

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
	<pre>"0ESACREWOL"
	"1ESACREWOL"
	"2ESACREWOL"
	"3ESACREWOL"</pre>
</ol>
  </div>
</div>

##Making Your Operator Generic with Parameters

Parameters allow your Java primitive operator to be more generic and enables the end-user to configure and control the behavior of the operator.

<div class="modal-body">
	<iframe width="560" height="315" src="https://www.youtube.com/embed/RkOkiDJYe8o?rel=0" frameborder="0" allowfullscreen></iframe>
</div>

The example in the video above shows how to generalize the StringToCaps operator so that it reverses (or doesn't reverse) the incoming string based on a reverseString boolean parameter in the SPL operator code.

Below are the general steps to create a parameter for Java primitive operator:

1.  Determine how the parameter will control the behavior of the Java primitive operator.  A parameter may toggle some behavior on and off.  It can be a String that allows the end user to specify the location of some configuration file.  It can refer to an attribute that the operator should act on when a tuple is received.  To learn more about the different kinds of parameters and the supported SPL types, refer to this documentation:  [Parameter Annotation Javadoc](http://www-01.ibm.com/support/knowledgecenter/#!/SSCRJU_4.1.0/com.ibm.streams.spl-java-operators.doc/api/com/ibm/streams/operator/model/Parameter.html)
1. Based on the SPL type that the user needs to specify in the SPL code, define a matching private member in the Java class to store the parameter value.
1. Create a setter method for setting the newly define private field.  
1. Annotate the setter method with the @Parameter annotation.  You may configure the parameter name, description, and cardinality, etc using this annotation.  The annotated setter method will be recognized by the Streams runtime as the method for initializing the parameter value.  The setter method will be called **before** the `initialize` method is called.
1. Modify your operator logic to honor the parameter value.

### Example Parameter

In our example, we will introduce a boolean parameter named `reverseString` to control if the incoming String from a tuple should be reversed or not.

1. In the operator class, add a Boolean member field that will be used to hold the parameter value. Default the parameter value to be false if it is not specified.

	<pre><code>  
	private Boolean reverseString = false;
	</code></pre>

1. Add a setter method for `reverseString`.
1. Add the @Parameter annotation.  Since the parameter is of type Boolean, the cardinality is automatically set to 1, meaning that only a single value can be provided.

	<pre><code>
	  @Parameter(name = "reverseString", optional = true,
	  	description = "Boolean value. Reverse strings if true. Default: false.")
	  public void setReverseString(Boolean value){
	  	reverseString = value;
	  }
	</code></pre>
1.	In the `process()` method, modify the operator logic to only reverse the string if the `reverseString` field is true.

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

1. Save and build the operator.

1. To test the parameter, add a `param` clause at the invocation of the StringToCaps operator:

	<pre><code>
	(stream&lt;rstring myString&gt; StringToCaps_2_out0) as StringToCaps_2 =
			StringToCaps(Beacon_1_out0)
		{
			param
				reverseString : true;
		}
	</code></pre>

1.	Run the application.  You should see output similar to the following:

	~~~~~~
	"0ESACREWOL"
	"1ESACREWOL"
	"2ESACREWOL"
	"3ESACREWOL"
	~~~~~~
<!--
Here are some more parameter examples:
`tabs with different parameter examples` -->

##Defining Custom Metrics

A metric represents a measurement of an element in either an operator or a processing element. A metric's value is an signed 64-bit integer value, represented as a primitive long in the Java Operator API.  A metric enables the operator keep track of current state, and allows the end-user or external systems to monitor the operator based on metric values.

Two types of metrics are provided by the SPL language runtime:

* **System metrics** - predefined and maintained by the SPL runtime (this includes things like number of tuples processed on a port, tuple flow rate, etc.)
* **Custom metrics** - created and maintained by the operator.

There are three kinds of metrics:

* **Counter** indicates that this metric represents a count of occurrence of some event.
* **Gauge** indicates a value that is continuously variable with time.
* **Time** indicates a metric that represents a point in time.

Live feed of the system metrics and operator custom metrics can be viewed in Streams Studio and the Streams Console.  You may retrieve the latest metrics using the Streams REST APIs.  This allows you to monitor your Streams domain, and your applications using your favorite monitoring tools.  Refer to this documentation about the [Metrics REST APIs](http://www-01.ibm.com/support/knowledgecenter/#!/SSCRJU_4.1.0/com.ibm.streams.restapi.doc/doc/restapis-metrics.html).

For more information about metrics, refer to the [Metrics Javadoc](http://www-01.ibm.com/support/knowledgecenter/#!/SSCRJU_4.1.0/com.ibm.streams.spl-java-operators.doc/api/com/ibm/streams/operator/metrics/Metric.html).

This section will show you how to add your a custom metric to your Java operator.

<div class="modal-body">
	<iframe width="560" height="315" src="https://www.youtube.com/embed/hLjuJqNJ86Q" frameborder="0" allowfullscreen></iframe>
</div>

###Custom Metric Example

Below are steps to add a custom operator metric.  In this example, we will try to create a metric that counts the number of characters the Java primitive oeprator `StringToCaps` has processed.

1.	Import the Metric library, com.ibm.streams.operator.Metrics:

	~~~~~~
	import com.ibm.streams.operator.metrics.Metric;
	~~~~~~

1.	Add a private field of type Metric.  In our example, we added the `numCharacters` field in the `StringToCaps` class:

	~~~~~~
	private Metric numCharacters;
	~~~~~~

1.	Create a setter method for the Metric field.  Add the @CustomMetric annotation to the setter method.

	~~~~~~
	@CustomMetric(name = "numCharacters", kind = Metric.Kind.COUNTER)
	public void setNumCharacters(Metric runtimeMetric){
		numCharacters = runtimeMetric;
	}
	~~~~~~

	The `@CustomMetric` annotation let you define the name and desription of the metric.  In addition, you can specify the metric kind:  COUNTER, GUAGE OR TIME.  Optionally, specify if the metric should be registerred with the platform's MBean server, using the `mxbean` property.  The default value is false.  

	The setter method is called before initialization similar to the way @Parameter sets are done.

1.	In the process() method, increment the numCharacters metric by the length of myString right before the outgoing tuple is submitted:

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

Below are the basic steps for creating a source operator:  

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

### Example Source Operator

In this example, we will implement a source operator that gets data from an external server system.  This is a simulated server.  The server provides the following interface to get data from the server.  While this example is simple, and the interface does not reflect a real external system, this example demonstrates the key concepts required for implementing a source operator.

~~~~~~~

/*
 * Simulated Server interface
 */
public interface Server {
	/*
	 * Connect to the server to receive data
	 */
	public void initialize(String userId, String password) throws Exception;

	/*
	 * Read the next record from the server
	 */
	String getData() throws Exception;

	/*
	 * Disconnect from the server
	 */
	public void disconnect() throws Exception;
}

~~~~~~~

Below is the `ServerSource` operator that usese this interface:

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

        while(!shutdown ){
					  OutputTuple tuple = out.newTuple();
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

Key things to note from this example:

1.  In the **initialize** method:

	* Call super class's `initialize(context)` method to properly initialize the operator.
	* Create a `Server` object and make a connection via its `Server.initalize(...)` method.
	* Use the operator context thread factory to create a thread.  This thread will be used to read data from the server.  The thread is set up in the `initialize(...)` method, but it is not started.  When the operator is initializing, connections to downstream operators may not have been made yet.  Therefore, it is not recommended to start reading from the external system at this point.


1.  In the **allPortsReady** method:

	* At this point, connections to downstream operators have been established.  Therefore, we can start the tuple processing thread and start reading from external system.


1.  In the **prodcueTuples** method:

	This method is called by the processing thread that we have started from `allPortsReady`.  In this method:

	* Get the output port from the operator:  `out`
	* Create a while loop to start reading from server until the operator is shut down.
	* From the output port, create a new tuple.
	* Read data from the server.
	* Assign data to the output tuple.
	* Submit the tuple to the output port

1.  In the **shutdown** method:

	This method is called when the operator is shutdown by the runtime.  This is where the operator should clean up:
	In this method:

	* Stop the processing thread
	* Disconnect from the server
	* Always call super.shutdown() in the shutdown method

This covers the basics of creating a source operator.  Streams Java Operator APIs come with many useful patterns and samples.  You may extend from these patterns when implementing the source operator.  To have access to these patterns, include the com.ibm.streams.operator.sample.jar in your classpath.  For more information about these samples and patterns, refer to this documentation.  <a target="_blank" href="http://www-01.ibm.com/support/knowledgecenter/#!/SSCRJU_4.1.0/com.ibm.streams.spl-java-operators.doc/samples/overview-summary.html">Java Operator Samples</a>

## Next steps

This covers the basics of writing a Java primitive operator.  To learn more about the details, refer to the [knowledge center](http://www-01.ibm.com/support/knowledgecenter/#!/SSCRJU_4.1.0/com.ibm.streams.spl-java-operators.doc/api/overview-summary.html).

We will continue to improve this development guide.  If you have any feedback, please click on the **Feedback** button at the top and let us know what you think!
