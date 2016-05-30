---
layout: docs
title:  Java Operator Development Guide Future Enhancements
description:  IBM Streams Java Operator Development Guide Future Enhancements
weight: 10
---

##Handling Errors

Streams applications are meant to run for a long time without stopping or crashing.  Your application resiliency depends on how well your operators can handle and recover from various types of errors.  As a rule of thumb, a primitive operator should never crash unless a fatal error has occurred and the operator cannot recover from it.  Examples of fatal errors include losing connection to external system and unable to reconnect with number of retries; or writing to a file system, but the file system is full,etc.  In the cases where the operator may have received some unexpected data, the operator should handle the error gracefully and not disrupt the application.  

When an exception is thrown, the best-practice responses are:

1. Catch the exception.
2. Log the exception as an error in the operator log.
3. Optionally, write the error out to an error port.

In the code below, we enhanced our ServerSource operator to include error handling.

<ul class="nav nav-tabs">
  <li class="active"><a data-toggle="tab" href="#minimum-1">Code</a></li>
  <li><a data-toggle="tab" href="#fullsource-1">Full Source</a></li>
</ul>

<div class="tab-content">
  <div id="minimum-1" class="tab-pane fade in active">
<pre><code>

// Add an optional output port as an output port to send error out
@PrimitiveOperator()
@OutputPorts({@OutputPortSet(cardinality=1),<b>@OutputPortSet(description=&quot;Error Port&quot;, cardinality=1, optional=true)</b>})
public class ServerSource extends AbstractOperator {
    private Thread processThread;
    private Server server;
    private boolean shutdown = false;

		// Create a Logger to write to application trace
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

// Add an optional output port as an output port to send error out
@PrimitiveOperator()
@OutputPorts({@OutputPortSet(cardinality=1),<b>@OutputPortSet(description=&quot;Error Port&quot;, cardinality=1, optional=true)</b>})
public class ServerSource extends AbstractOperator {
    private Thread processThread;
    private Server server;
    private boolean shutdown = false;

		// Create a Logger to write to application trace
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

<pre style="font-family: Andale Mono, Lucida Console, Monaco, fixed, monospace; color: #000000; background-color: #eee;font-size: 12px;border: 1px dashed #999999;line-height: 14px;padding: 5px; overflow: auto; width: 100%"><code>        if (trace.isInfoEnabled())
            trace.log(TraceLevel.INFO, &quot;StateHandler close&quot;);
</code></pre>

##Using Windows
Intelligent use of Windows can allow you to use the same Streams application for real-time processing, as well as batch processing. Batch processing such as map reduce can be done in Streams by using large window sizes.

The SPL language has two kinds of windows, tumbling and sliding. They both store tuples while they preserve the order of arrival, but differ in how they handle tuple evictions. Rather than keeping all the tuples ever inserted, windows are configured to evict expired tuples.

* **Tumbling** - Tumbling windows operate in batches. When a tumbling window fills up, all the tuples in the window are evicted.
* **Sliding** - Sliding windows operate in an incremental fashion. When a sliding window fills up, the future tuple insertions result in evicting the oldest tuples in the window.

For more details, read [Window Handling](http://www-01.ibm.com/support/knowledgecenter/SSCRJU_4.1.0/com.ibm.streams.dev.doc/doc/windowhandling.html?lang=en).

General strategy for implementing a windowed operator:

1. Have your operator class extend AbstractWindowOperator instead of AbstractOperator.
2. Create a window handler class that implements StreamsWindowListener<Tuple>. This window handler class will be in place of a process method in most cases. You window handler class should:
	1. Have a constructor that takes a `StreamingOutput<OutputTuple>` argument.
	2. Override the `void handleEvent(StreamWindowEvent<Tuple> event)` and develop a switch case to handle tumbling and/or sliding events.
	* Tumbling:
		<pre style="font-family: Andale Mono, Lucida Console, Monaco, fixed, monospace; color: #000000; background-color: #eee;font-size: 12px;border: 1px dashed #999999;line-height: 14px;padding: 5px; overflow: auto; width: 100%"><code>  @Override
	  public synchronized void handleEvent(StreamWindowEvent&lt;Tuple&gt; event) throws Exception {

		    switch (event.getType()) {
		      case INSERTION:
		           // handle insertion of tuples into the window
		           break;
		      case EVICTION:
		           // handle the tumble
		           break;
		      case FINAL:
		           // handle final mark
		           break;
		      }
	  }
	</code></pre>
	* Sliding:
		<pre style="font-family: Andale Mono, Lucida Console, Monaco, fixed, monospace; color: #000000; background-color: #eee;font-size: 12px;border: 1px dashed #999999;line-height: 14px;padding: 5px; overflow: auto; width: 100%"><code>  @Override
	  public synchronized void handleEvent(StreamWindowEvent&lt;Tuple&gt; event) throws Exception {

	        switch (event.getType()) {
		        case INSERTION:
		            // handle insertion of tuples into the window
		            break;
		        case INITIAL_FULL:
		            // handle first time window fills
		            break;
		        case TRIGGER:
		            // handle trigger events
		            break;
		        case PARTITION_EVICTION:
		            // handle partial evictions
		            break;
		        case EVICTION:
		            // handle the tumble
		            break;
		        case FINAL:
		            // handle final mark
		            break;
	        }
	  }
	</code></pre>
	3. In the initialize(...) method of the operator code, register a StreamWindowListener with your window handler class:

		`getInput(0).getStreamWindow().registerListener(new WindowHandler(getOutput(0)), false);`

In the example below, we implement a windowed operator that concatenates the strings that are coming in on its input port for a given window, then submits that concatenated string to the output port and resets the concatenated string on window eviction. Read more details about [tumbling](http://www-01.ibm.com/support/knowledgecenter/SSCRJU_4.1.0/com.ibm.streams.dev.doc/doc/tumblingwindowoperator.html) and [sliding](http://www-01.ibm.com/support/knowledgecenter/SSCRJU_4.1.0/com.ibm.streams.dev.doc/doc/slidingwindow.html) windows by clicking on the links.

<ul class="nav nav-tabs">
  <li class="active"><a data-toggle="tab" href="#minimum-3">Operator Code</a></li>
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
  <li class="active"><a data-toggle="tab" href="#minimum-4">Window Handler Code</a></li>
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
  </div>
</div>



##Problem Determination and Debugging
Debugging your Java operator is similar to debugging normal Java.

Here is the path that most Streams developers take to determine if their operator is working:

1. Go to the instance graph in Streams Studio and see if your operator is healthy. If there is a series of three unhealthy operators, it is typically the fault of the middle one (its crashing makes the connections of the other two unhealthy).
2. If your operator is unhealthy, try looking at standard out for that PE:
	**right click on your operator -> Show Log -> Show PE Console**
3. If you still don't have the information you need, increase the level of logging (this can be set during application launch) and look through the Operator Trace:
	**right click on your operator -> Show Log -> Show Operator Trace**

##SPL to Java Type Mapping
It's not always obvious which SPL types map to which Java types. It's important to get this mapping right when you are defining parameters, reading from input tuples, and writing to output tuples. Folow the link below a comprehensive [table of type mapping](http://www-01.ibm.com/support/knowledgecenter/SSCRJU_4.1.0/com.ibm.streams.dev.doc/doc/workingwithspltypes.html).

##Performance
As we mentioned at the beginning of this guide, your performance will depend on the efficiency of your **process(...)** or **produceTuples(...)** methods (in the case of a windowed operator, it will be in your window handler).

Here are some things to keep in mind:

* Do not print anything to standard out
* Avoid logging. If necessary, make sure that your logging is protected by an if statement:
	<pre style="font-family: Andale Mono, Lucida Console, Monaco, fixed, monospace; color: #000000; background-color: #eee;font-size: 12px;border: 1px dashed #999999;line-height: 14px;padding: 5px; overflow: auto; width: 100%"><code>        if (trace.isInfoEnabled())
	            trace.log(TraceLevel.INFO, &quot;StateHandler close&quot;);</code></pre>

* Minimize the copying of variables.



##References

####Annotation parameters:

*	**name** - Used in @PrimitiveOperator and @Parameters.    
*	**namespace** - Used in @PrimitiveOperator. Defines namespace of the operator.
*	**description** - Used in all annotations. This element provides a textual description of the operator and its functionality. Streams Studio also shows this description to developers using your operator in SPL applications.   
*	**cardinality** - Used in all @InputPortSet, @OutputPortSet, and @Parameter. This element indicates the number of values allowed for a parameter. A value of minus 1 (-1) indicates that the parameter can take any number of values.   
*	**optional** - Used in @InputPortSet, @OutputPortSet, and @Parameter. Defines whether a port or parameter is required.    
*	**type** - Used in the @Parameter. This element indicates the SPL type of the parameter and determines the values that the parameter can assume.   
