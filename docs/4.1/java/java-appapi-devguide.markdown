---
layout: docs
title: IBM Streams Java Application Development Guide
description: IBM Streams Java Application Development Guide
weight: 1
---

# Java Application API Development Guide
~~~~~~
package com.ibm.streamsx.sample.java;
import com.ibm.streams.function.model.Function;

public class Calculator {

	@Function(name = "add", namespace = "com.ibm.streamsx.sample.java.calculator", description = "Add two integers" )
	public static int add(int num1, int num2) {
		return num1 + num2;
	}
}
~~~~~~
## Setting up environment

There are three primary ways to get started with the API. If you are trying the API for the first time, the Streams Quick Start Edition VM is likely the fastest way to start working with the tutorials on this page. Download it at the following link to get started: [Streams Quick Start Edition VM](http://www-01.ibm.com/software/data/infosphere/stream-computing/trials.html)

The Streams Quick Start Edition VM contains a ready-to-go release of IBM  Streams. Additionally, the Quick Start VM comes bundled with IBM Streams Studio, which provides an intuitive, visual representation of your streaming application. After you've downloaded it, start the VM, open a console and type:
``` bash
streamtool startinstance
```
This starts the default IBM Streams instance that comes with the VM. This instance is disabled on startup. 

If you are **not** using the IBM Streams Quick Start Edition and already have an IBM Streams installation, make sure you've followed the instructions for [setting up your domain and instance](https://github.com/wmarshall484/websiteTest/blob/master/drafts/DomainSetup.md).

## Getting the Java Application API from GitHub
Although the QuickStart VM comes with a version of the Java Application API out of the box, you might want to obtain the most recent version from GitHub. To do so, simply navigate to the [releases section](https://github.com/Ibmstreams/streamsx.topology/releases) of the GitHub site, download the latest version, and extract it to your file system.

Alternatively, if you want the cutting edge of the API, clone the main repository directly:
``` bash 
git clone git@github.com:IBMStreams/streamsx.topology.git
```
After cloning the repository, you must build the project to produce the `com.ibm.streamsx.topology.jar`file. Fortunately, the project provides an Ant script to take care of this automatically. The script has three requirements:
* Ant version later than 1.9.1
* [Optional] For tests, the JUnit JAR files must be stored in `~/.ant/lib`
* [Optional] For tests, the Jacoco code coverage JAR files must be stored in `~/.ant/lib`

To build the project, navigate to the project root and simply type ```ant```. The `com.ibm.streamsx.topology.jar`file is produced in the `<project_root>/com.ibm.streamsx.topology/lib directory`.

To run the suite of unit tests, type ```ant test```.

## Setting up with Eclipse/Streams Studio
If you've followed the previous instructions and are ready to start writing code in Eclipse or StreamsStudio, take the following steps.

1. Start Eclipse / Streams Studio.
* Set the class path variable in your workspace:
  1. Open __Window > Preferences > Java > Build Path > Classpath Variables__.
  * Click __New__.
  * In the __New Variable Entry__ dialog, provide a name for the library, for example, STREAMS_JAVA_FUNCTIONAL_API.
  * Click __File__.
  * Browse to locate the following file: `<streamsx.topology install path>/com.ibm.streamsx.topology/lib/com.ibm.streamsx.topology.jar`
  * Save this setting.

If you haven't yet linked Eclipse/Streams Studio with IBM Streams, ensure the following JAR files are part of the class path:
* `<streamsx.topology install path>/com.ibm.streamsx.topology/lib/com.ibm.streamsx.topology.jar`
* `$STREAMS_INSTALL/lib/com.ibm.streams.operator.samples.jar`

This completes the installation of the streamsx.topology project. Note, however, that the provided instructions are specific to installing the Java Application API libraries in Eclipse or Streams Studio (or any Java IDE, really).

You are now ready to go!

# Writing the First Streams Java Appication

If you're viewing this page, it's likely that you haven't worked with the Java Application API before, or possibly streaming applications in general. In this document, we discuss at a high level the general principles behind streaming application development and the benefits of the Java Application API, and  we demonstrate these in a sample application. 

The Java Application API allows you to write programs for streaming data exclusively in Java — no SPL! You can run the programs as Java programs, you can run them as stand-alone Streams applications, or you can run them as distributed Streams applications. If you need help getting your environment set up, visit [the Java Application API setup guide](Environment_Setup).

The primary goals of the Java Application API are to enable the developer to:
* Define the structure of a streaming application using only Java
* Pass Java objects as tuples on a stream 
* Define how data is processed in a modular, scalable, and stateful manner

Each of these points is covered in further detail in the tutorials on this site and in the example here where we create an application that processes temperature readings from a device. 

The Java Application API is fully compatible with IBM Streams version 4.0.0 and later. The API is open source and is available for download from our [streamsx.topology project on GitHub](https://github.com/IBMStreams/streamsx.topology).

# Data streaming principles & the Java Application API
Streaming applications are usually solutions that meet real-time data processing needs. Whereas frameworks like Apache Hadoop deal with batch jobs that eventually terminate after being submitted, data streaming applications are designed to run forever. For example, consider a company whose product scans temperature sensors across the world to determine weather patterns and trends. Because there is *always* a temperature, there is a perpetual need to process data. 

The application must be allowed to run for an indeterminate amount of time, and it also must be allowed to scale flexibly. Say, for example, that the number of temperature sensors doubles, so correspondingly the speed must double at which the application must process data. With the Java Application API, you can easily parallelize your data pipeline, and you can specify which pieces of the application run on which resources across a certain number of specified processes.

The latter features will be covered in a [subsequent tutorial](UDP_Windowing). For now, let's take the simple example of reading data from a temperature sensor and printing the output to the screen. 

## Creating a topology object
When writing an application with the Java Application API, the very first thing to do is to create the Topology object:
``` Java
Topology topology = new Topology("temperatureSensor");
```
The topology object contains information about the structure of our graph (that is, our application), including how the data is generated and processed. The topology object also provides utility methods that allow us to define our data sources, in this case the temperature sensor. By invoking `topology.endlessSource()`, we can pass a Java Function that returns the next data item each time it is called.

## Defining a data source

For simplicity, we will simulate a temperature sensor by reading from a Java Random object as follows.  
``` Java
Random random = new Random();
        
TStream<Double> readings = topology.endlessSource(new Supplier<Double>(){
    @Override
    public Double get() {
        return random.nextGaussian();
    }
});
```
The `endlessSource()`method will repeatedly call the function's overridden `get()`method and return a new random temperature reading each time. Although in this case we are obtaining our data by calling `random.nextGaussian()`, in principle this could be substituted for any live data source such as reading from a Kafka cluster, or MQTT server. This will be shown in subsequent tutorials.

As a side note, the API is compatible with Java 8 so this data source could be written more concisely using a lambda expression:
``` Java
TStream<Double> readings = topology.endlessSource(() -> random.nextGaussian());
```

## Understanding TStream

The `endlessSource()`method produces a TStream, which is arguably the most important Java class in the Java Application API. 

**A TStream represents a potentially infinite flow of tuples in your application**. Because an application might run forever, there is no upper limit to the number of tuples that can flow over a TStream. Tuples flow one at a time over a TStream and are processed by subsequent data **operations**. We do not define any data operations in this example (such as filtering or transforming the data on a TStream). Data operations are covered in the [common streams operations](CommonStreamOperations) tutorial.

One of the strengths of the Java Application API is that a tuple can be any Java Object, so long as it is serializable. As such, a TStream is parameterized to a Java type as shown in this line:
```
TStream<Double> readings = ...;
```
In this case, the TStream is parameterized to a Double.

## Printing to output

Now, in true "Hello World" fashion, after obtaining the data we simply print it to standard output. 
``` Java
readings.print();
```
Because each tuple is a Java object, invoking TStream's `print()`method calls the `toString()`method on each tuple and prints the results to output using `System.out.println()`. Although TStream's `print()`method is useful in its convenience, there are likely cases where the application will need to output to a file or Kafka. These cases are covered in the [Kafka](Kafka) and [common streams operations](CommonStreamOperations) tutorials.

## Submitting and running the application

After the application has been defined, it can be run by acquiring a *context* from the StreamsContextFactory, and invoking its `submit()`method while passing the topology object as a parameter:
``` Java 
StreamsContextFactory.getEmbedded().submit(topology);
```
The `getEmbedded()` method returns an EMBEDDED submission context, which runs the application in a single JVM on a single host. There are three primary submission contexts, each of which runs the application in a different manner:

* EMBEDDED - Runs the application in embedded mode. This is a simulated Java environment for running your Streams application.
* DISTRIBUTED - Runs the application in distributed mode. When an application is submitted with this context, a Streams Application Bundle (.sab file) is produced. The .sab file contains all of the application's logic and third-party dependencies, and is submitted to an IBM Streams instance automatically.
* STANDALONE - Runs the application in stand-alone mode. When running in this mode, the application also produces a Streams Applicaition Bundle (.sab file), but rather than submitting it to a cluster, the bundle is instead executable. The bundle will run within a single process, and can be terminated with Ctrl-C interrupts.

# First Streams Java Application Complete
 
The application, in its entirety, is as follows:
``` Java 
import java.util.Arrays;
import java.util.Random;

import com.ibm.streamsx.topology.TStream;
import com.ibm.streamsx.topology.Topology;
import com.ibm.streamsx.topology.context.StreamsContextFactory;
import com.ibm.streamsx.topology.function.Supplier;

public class TemperatureTest {
    public static void main(String[] args){
        
        Topology topology = new Topology("temperatureSensor");
        Random random = new Random();
        
        TStream<Double> readings = topology.endlessSource(new Supplier<Double>(){
            @Override
            public Double get() {
                return random.nextGaussian();
            }
        });
    
        readings.print();
        StreamsContextFactory.getEmbedded().submit(topology);
    }
}
```

# Common Streams Operations

After creating a TStream, the three primary operations that will be performed are *filter*, *transform*, and *sink*. Each operation accepts a user-supplied function to determine how to process one of the TStream's tuples. A few best practice use cases are outlined here.

## Filtering Data

Invoking *filter* on a TStream allows the user to selectively allow and reject tuples from being passed along to another stream based on a provided predicate. For example, suppose that we have a TStream of String, where each String is a word out of the English dictionary.
``` Java
TStream<String> words = topology.source(/*code for reading from dictionary*/);
```
Furthermore, suppose that we want only a TStream of dictionary words that do not contain the letter "a". To create such a TStream, we simply invoke `.filter()`on the TStream of words:

``` Java
TStream<String> words = topology.source(/*code for reading from dictionary*/);
TStream<String> wordsWithoutA = words.filter(new Predicate<String>(){
    	@Override
			public boolean test(String word) {
				if(tuple.contains("a")){
					return false;
				}
				return true;
			}
		});
```

Or, more concisely by using Java 8 lambda expressions:

``` Java
TStream<String> words = topology.source(/*code for reading from dictionary*/);
TStream<String> wordsWithoutA = words.filter(word -> word.contains("a") ? false : true);
```
		
The returned TStream, *wordsWithoutA*, now contains all words without a lowercase "a". Whereas before, the output might have been:
```
...
qualify
quell
quixotic
quizzically
...
```
The output now is:
```
...
quell
quixotic
...
```

You'll notice that we provide a predicate function, and need to override only its `test()`method to return true or false for respectively permitting and rejecting the tuple. 

**Important:** While the code has access to the tuples of the TStream, and thus can modify their contents, a filter is intended to be an *immutable* operation. As such, tuples should not be altered. For details about transforming the contents or type of a tuple, refer to the transform operation in the next section.

## Transforming Data

*Transform* is the workhorse of the Java Application API. It will likely be the most frequently used method in your application. Primarily, the `.transform()`method is responsible for taking the tuples of a TStream and doing any one of the following:
* Modifying the contents of the tuple
* Changing the type of the tuple
* Keeping track of state across tuples

For each of these, we'll walk through an example.
### Transform: Modifying tuple contents
Let's take the previous example of reading words from a dictionary. It's not necessarily the case that we want *exactly* the tuples of a stream; we might need to modify them before we use them. Instead of having a TStream of dictionary words, what if we wanted a TStream of only the first four letters of each word? The transform operation is best suited to this task because it permits data-modifying operations on the tuple:
``` Java
TStream<String> words = topology.source(/*code for reading from dictionary*/);
TStream<String> firstFourLetters = words.transform(new Function<String, String>(){
            @Override
            public String apply(String word) {
                return v.substring(0,4);
            }
            
        });
```
Or, more concisely by using Java 8 lambda expressions:

``` Java
TStream<String> words = topology.source(/*code for reading from dictionary*/);
TStream<String> firstFourLetters = words.transform(word -> word.substring(0,4));
```
Now, instead of the entire word, printing the *firstFourLetters* TStream produces this output:
```
...
qual
quel
quix
quiz
...
```
As you can see, invoking `.transform()` allows for the modification of tuples. Yet what if your application seeks to change the type? For the previous example, both the inputs and outputs of the transform function were strings. In the next section, we will demonstrate how `transform()`can change tuple types entirely.

### Transform: Changing the tuple type
The `transform()`method does not require that the input tuple type is the same as the output tuple type. In fact, one of the strengths of the Java Application API is that the tuples on a TStream can be used as parameters when creating tuples to pass on the output TStream. As an example, let's suppose that we have a TStream of Java Strings, each corresponding to an Integer:
``` Java
// Creates a TStream with four Java Strings as tuples -- "1", "2", "3", and "4"
TStream<String> stringIntegers = topology.strings("1","2","3","4");
```
If we want to perform an operation that treats the tuples as Java Integers (and not Java Strings), we need to transform the tuples to a new type using `.transform()`. This could be done as follows:

``` Java
// Creates a TStream with four Java Strings as tuples -- "1", "2", "3", and "4"
TStream<String> stringTuples = topology.strings("1","2","3","4");
TStream<Integer> integerTuples = stringTuples.transform(new Function<String, Integer>(){
            @Override
            public Integer apply(String stringInt) {
                return Integer.parseInt(stringInt);
            }    
        });
```

Or, as a Java 8 lambda expression:

``` Java
// Creates a TStream with four Java Strings as tuples -- "1", "2", "3", and "4"
TStream<String> stringTuples = topology.strings("1","2","3","4");
TStream<Integer> integerTuples = stringTuples.transform(stringTuple -> Integer.parseInt(stringTuple));
```
Now that actual Java Integers are being passed as tuples on the Stream, operations such as addition, subtraction, and multiplication can directly be invoked:
``` Java
// Creates a TStream with four Java Strings as tuples -- "1", "2", "3", and "4"
TStream<String> stringTuples = topology.strings("1","2","3","4");
TStream<Integer> integerTuples = stringTuples.transform(stringTuple -> Integer.parseInt(stringTuple));
integerTuples.transform(integerTuple -> integerTuple * 2 + 1).print();
```

Yielding the following output:
```
3
5
7
9
```
Although this example only converts Strings to Integers, in principle it could work for any two arbitrary Java types, so long as they are both serializable. 

Another strength of the API is that users aren't restricted to only passing datatypes defined by the Java runtime (String, Integer, Double, and so on) -- users can define their own classes and datatype, and pass them as tuples on a TStream.

### Transform: Keeping track of state across tuples
The previous examples would be termed *stateless* operators. A stateless operator does not keep track of any information about tuples that have been seen in the past, for example, the number of tuples that have been passed on a TStream, or the sum of all Integers seen on a TStream. Yet keeping track of state is both an easy and powerful part of the Java Application API, enabling a much broader range of applications.

Although the following example pertains primarily to the `transform()` method, in principle *any* of the source, filter, sink, modify, or transform methods can keep track of state. 

An example of a stateful operator would be one which outputs the average of the last ten Doubles in a TStream. For this example, we first define a TStreams of random numbers:
``` Java
TStream<Double> doubles= topology.endlessSource(new Supplier<Double>(){
            Random random = new Random();
            @Override
            public Double get() {
                return random.nextGaussian();
            }  
      });
```

You'll note that in defining the *doubles* TStream, Supplier contains the **random** field, which is used to generate the random numbers.

Next, we want to define an operation which consumes the *doubles* stream and keeps track of its moving average across the last ten tuples. Similar to how **random** was defined as a part of the internal state of *doubles*, we can define a LinkedList to keep track of the tuples on the TStream:

``` Java
TStream<Double> avg = doubles.transform(new Function<Double, Double>(){
            LinkedList<Double> lastTen = new LinkedList<>();
            @Override
            public Double apply(Double d) {
                lastTen.addLast(d);
                if(lastTen.size() > 10)
                    lastTen.removeFirst();
                return calculateAverage(lastTen);
            }
            
        });
```
This is an important point: the state of the operator does *not* reset between tuples. If there are eight tuples in the *lastTen* LinkedList at the start of the invocation of `apply()`, then the next invocation of `apply()` immediately following will see nine tuples in the LinkedList.

Although in this case our state is a LinkedList with the ultimate goal of calculating a moving average, the following are some examples of state used in sources, sinks, and transformations.

| Operation        | State           | Goal  |
| ------------- |-------------| -----|
| Source	| File Handle	| Reading lines from a file to send as tuples	|
| Source	| Socket	| Listening on a TCP socket for data to send as tuples	|
| Transform | HashMap | A HashMap can be used as state to make a histogram of the most commonly seen tuples|
| Transform | Set | A set can be used as state to keep track of all unique tuples on a TStream |
| Sink | File Handle | Similar to source, except the file handle is used to write tuples to a file |
| Sink | Socket | Similar to source, except the socket is used to write tuples to a TCP stream |

## Creating Data Sink

*Sink* takes tuples from a stream, but does not return a stream as output. It is invoked on a TStream when the tuples themselves are output to the system. The output can take the form of a file, a log, a TCP connection, HDFS, Kafka, or anything that you can define -- because operations such as sink can be stateful, you can provide any handle that is required.

TStream comes with the `.print()`method out of the box. The `.print()`method is a sink that simple invokes ``` System.out.println(tuple.toString()); ``` on every tuple that is sent on the stream.

The following is an example of a sink that writes the string representation of a tuple to standard error instead of standard output:
``` Java
TStream<String> strings = ...;
strings.sink(new Consumer<String>(){
            @Override
            public void accept(String string) {
                System.err.println(string);             
            }     
  });
```
Or, more concisely with Java 8 lambda expressions:
``` Java
TStream<String> strings = ...;
strings.sing(string -> System.err.println(string));
```
For a more in-depth tutorial on how to write a sink that writes to a file, visit the [file reading/writing](http://www.google.com) introduction. Or, for Kafka, the [digesting and ingesting with Kafka](www.google.com) tutorial should contain relevant information.

# Integrating SPL operators with the Java Application API

Since the applications written with the Java Application API are capable of running on the IBM Streams platform, it's natural that the API would integrate with SPL primitive operators and toolkits. IBM Streams comes with a number of toolkits that provide functionality such as text analysis, HDFS integration, and GeoSpatial processing. Furthermore, if you're currently working with IBM Streams, it's possible that you've implemented your own toolkits that you'd like to utilize. 

The purpose of this guide is to demonstrate the basics of interfacing the Java Application API with such toolkits. This is important not only for backward compatibility, but also because it shows that that API can interact with C++ operators in addition to Java ones. Although it isn't assumed that the reader has an understanding of SPL and the structure of toolkits, consulting [the IBM Knowledge Center](http://www-01.ibm.com/support/knowledgecenter/SSCRJU_4.0.0/com.ibm.streams.dev.doc/doc/creating_toolkits.html?lang=en) may prove informative.

## Background about Streams Toolkit

Before the Java Application API was released, developing IBM Streams was a two-step process that involved defining C++ or Java *primitive operators* (which manipulated data), and then subsequently connecting them together into an application by using a language called SPL. Since, as a java developer, you may not want to learn an entirely new programming language to build your application, the Java Application API presents a useful alternative.

Yet the primitive operators are still very useful. For one thing, many primitive operators are organized into *toolkits* which come packaged with any IBM Streams release to provide tools for machine learning, statistical analysis, and pattern recognition. In addition, since primitive operators can be written in C++, a developer using Java Application API can have certain portions of the application written in C++ if so desired.

In this tutorial, we will not cover [the development of C++ or Java primitive operators](http://www-01.ibm.com/support/knowledgecenter/SSCRJU_4.0.0/com.ibm.streams.dev.doc/doc/developing_primitive_operators.html?lang=en), however the process for utilizing an already existing toolkit is outlined below.

## Sample toolkit and operator
To begin, suppose that we have a 'myTk' toolkit in the home directory. In the 'myTk' toolkit, there is one package named 'myPackageName', and one operator named 'myOperatorName':
``` bash
$ cd ~/
$ tree
|--  ./myTk
|   |--  ./myTk/appendPackage
|   |   |-- ./myTk/appendPackage/appendOperator
|   |   |   |-- <implementation of appendOperator>
|   |--  ./myTk/toolkit.xml
```

 As such, when the toolkit is included into the application, the full path of the operator will be **appendPackage::appendOperator**. The 'appendOperator' operator itself is very simple, it takes an SPL rstring, appends it with the string " appended!", and submits the resulting rstring as an output tuple. For example, if the input to the 'appendOperator' operator are the following rstring tuples (one per line):
```
 Rhinoceros
 Modest Mouse
 The cake is a lie
```

The output output tuples will be:
```
 Rhinoceros appended!
 Modest Mouse appended!
 The cake is a lie appended!
```

It's important to note that every primitive operator is strongly typed with respect to the tuples that are sent to and emitted from the operator. As such, each primitive operator is associated with a *stream schema*, which simply contains the types of its input and output tuples. For example, the stream schema for both the input and output tuples of 'appendOperator' would be:
```
tuple<rstring attribute_name>
```
Which makes sense, since 'appendOperator' both takes and produces an rstring. A hypothetical operator that takes and emits an rstring and an integer would look like:
```
tuple<rstring first_attribute_name, uint32 second_attribute_name>
```

You'll notice that each attribute of a tuple requires a corresponding name. This is because certain primitive operators require that an attribute have a particular name to operate correctly; however, the vast majority of operators shipped with IBM Streams are flexible and allow the usage of any name.

Defining stream schemas is not necessary when just developing exclusively withing the Java Application API -- it only becomes necessary with interfacing with primitive operators. We see why this is true in the next section.

# Using the toolkit within the Java Application API

In the introductory tutorials to the Java Application API, we created TStream objects which represented the flows of data in our application. To utilize a primitive operator, we must first convert our TStream to a special kind of stream called an SPLStream. SPLStreams are exactly like TStreams, except instead of being templated to a Java type, as in:
```
TStream<Double> myStream = ...;
```

Their types are instead defined by the *stream schemas* that were mentioned in the previous section, e.g.:
```
tuple<rstring attribute_name>
```

To create an SPLStream it's also necessary to provide a transformation Function to convert from the types of the TStream's Java objects to the SPLStream's SPL types. To show this in action, let's suppose that we have a TStream of Java Strings that we want to run through the 'appendOperator' that is found in the 'myTk' toolkit:
``` Java
Topology topology = new Topology("primitiveOperatorTest");
TStream<String> strings = topology.strings("Rhinoceros", "Modest Mouse", "The cake is a lie");
```

The first thing we do is import the toolkit by using the *addToolkit* utility method found in com.ibm.streamsx.topology.spl.SPL:
``` Java
SPL.addToolkit(topology, new File("/home/streamsadmin/myTk"));
```

Then, we convert the TStream of Strings to an SPLStream of SPL tuples -- each tuple conforming to the stream schema of the operator:
``` Java
StreamSchema rstringSchema = Type.Factory.getStreamSchema("tuple<rstring rstring_attr_name>");
SPLStream splInputStream = SPLStreams.convertStream(strings, new BiFunction<String, OutputTuple, OutputTuple>(){
			@Override
			public OutputTuple apply(String input_string, OutputTuple output_rstring) {
				output_rstring.setString("rstring_attr_name", input_string);
				return output_rstring;
			}	
		}, rstringSchema);
```
In the above lines of code, the convertStream method takes three parameters
* **strings** - The TStream to convert to an SPL Stream
* **A BiFunction** - The BiFunction may appear complicated, but its functionality is easy to understand. It takes two arguments
  * It's first argument is a Java String. This is the current Java tuple on the TStream (e.g., "Rhinoceros") to be transformed to an SPL tuple. 
  * Its second argument is an OutputTuple. An OutputTuple can be thought of as a wrapper for an SPL tuple. It contains methods such as *setString* or *setDouble* which take Java types (Strings, Doubles, etc.) and converts them to SPL types according to the provided schema. In the above code, we can see that the "rstring_attr_name" attribute is set by invoking ```output_rstring.setString("rstring_attr_name", input_string);```. After being modified, the OutputTuple is returned by the BiFunction.
* **rstringSchema** - This is the stream schema for the input to the 'appendOperator' primitive operator. This determines the name used when calling *OutputTuple.setString*.

Voila! We've created an SPLStream of SPL types. To use this stream and invoke the 'appendOperator' on its tuples, it's only one line of code: 
``` Java
SPLStream splOutputStream = SPL.invokeOperator("appendPackage::appendOperator", splInputStream, rstringSchema, new HashMap());
```
Similar to the way that transforming a TStream produces another TStream, invoking a primitive operator on an SPLStream produces another SPLStream; in this case *splOutputStream*. You may have noticed that *invokeOperator* takes a Map as an argument, this is in case the primitive operator requires any parameters which, in this case, it doesn't.

Now that we have the output we desired, we'd like to print it to output. Unfortunately, since the tuples on the stream are SPL tuples and not Java tuples, we can't simply invoke ```splOutputstream.print()```. First, we need to convert the SPL tuples back the Java strings in a manner similar to the earlier conversion:
``` Java
TStream<String> javaStrings = splOutputStream.convert(new Function<Tuple, String>(){
			@Override
			public String apply(Tuple inputTuple) {
				return inputTuple.getString("rstring_attr_name");
			}			
		});
```
This time, we take a *Tuple* object, and retrieve the value of the "rstring_attr_name" parameter as a Java String by invoking ```inputTuple.getString("rstring_attr_name");```, resulting in a TStream of Strings.

Now we can simply call print():
``` Java
javaStrings.print();
```
and submit:
``` Java
StreamsContextFactory.getStreamsContext("STANDALONE").submit(topology).get();
```

When the application is run, it correctly produces the following output
```
 Rhinoceros appended!
 Modest Mouse appended!
 The cake is a lie appended!
 ```

### Summary
 
 When using a primitive operator, the general structure of your application is the following:
 
 1) Convert form a TStream to an SPLStream
 
 2) Pass the SPLStream as input when invoking the primitive operator
 
 3) Convert the output SPLStream back to a TStream
 
 The application, in its entirety, is as follows:
 ``` Java
import java.io.File;
import java.util.HashMap;

import com.ibm.streams.operator.OutputTuple;
import com.ibm.streams.operator.StreamSchema;
import com.ibm.streams.operator.Tuple;
import com.ibm.streams.operator.Type;
import com.ibm.streamsx.topology.TStream;
import com.ibm.streamsx.topology.Topology;
import com.ibm.streamsx.topology.context.StreamsContextFactory;
import com.ibm.streamsx.topology.function.BiFunction;
import com.ibm.streamsx.topology.function.Function;
import com.ibm.streamsx.topology.spl.SPLStream;
import com.ibm.streamsx.topology.spl.SPL;
import com.ibm.streamsx.topology.spl.SPLStreams;


public class SPLTest {
	public static void main(String[] args) throws Exception{
		Topology topology = new Topology("SPLTest");
		SPL.addToolkit(topology, new File("/home/streamsadmin/scratch/myTk"));
		
		TStream<String> strings = topology.strings("Rhinoceros", "Modest Mouse", "The cake is a lie");
		
		StreamSchema rstringSchema = Type.Factory.getStreamSchema("tuple<rstring rstring_attr_name>");
		SPLStream splInputStream = SPLStreams.convertStream(strings, new BiFunction<String, OutputTuple, OutputTuple>(){
			@Override
			public OutputTuple apply(String input_string, OutputTuple output_rstring) {
				output_rstring.setString("rstring_attr_name", input_string);
				return output_rstring;
			}	
		}, rstringSchema);
		
		SPLStream splOutputStream = SPL.invokeOperator("appendPackage::appendOperator", splInputStream, rstringSchema, new HashMap());
		TStream<String> javaStrings = splOutputStream.convert(new Function<Tuple, String>(){
			@Override
			public String apply(Tuple inputTuple) {
				return inputTuple.getString("rstring_attr_name");
			}			
		});
		
		javaStrings.print();
		StreamsContextFactory.getStreamsContext("STANDALONE").submit(topology).get();				
	}
}
```


