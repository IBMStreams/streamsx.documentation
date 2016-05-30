---
layout: docs
title:  Java Functions Development Guide
description:  IBM Streams Java Function Development Guide
published: true
---

# Java Function Development Guide (Draft)

# Before You Begin

You need to have some basic understanding about Streams and the SPL language.

If you are new to Streams:

* [https://developer.ibm.com/streamsdev/docs/streams-quick-start-guide/](Streams Quick Start Guide)
* [https://developer.ibm.com/streamsdev/docs/studio-quick-start/](Streams Studio Quick Start Guide)

# Overview

IBM Streams supports native functions to be written in Java.  A native function can be called anywhere in the SPL code.
It is quite easy to create a Java native function, this guide is to show you how.

The general steps of creating a Java native function are as follows:

1. Create a SPL toolkit
1. In the toolkit create a new Java class
1. In the Java class, create a *static* Java function
1. Add the @Function annotation  
1. Compile the Java class containing the method.
1. Package the class and its nested classes in a jar file in lib or impl/lib within the toolkit.
1. Index the toolkit.

# Create a SPL toolkit

To write a Java native function, you need a SPL toolkit.  A toolkit is a collection of reusable artifacts that your SPL programs
can use. 

A SPL toolkit typically has the following structure:

~~~~~~
/+ <toolkit> 
   /+ info.xml
   /* toolkit.xml 
   /+ <name-space>
      /+ <spl-file>
      /+ native.function
         /+ function.xml
      /+ <operator>
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
* **info.xml** - an XML file that describes the version, name, required dependencies, etc of the toolkit.
* **toolkit.xml** - a generated resource by the SPL toolkit indexing processing.  This file should not be modified and is used by the compiler and various comoponents in Streams.
* **[name-space]** - similar to packages in Java, allow you to group related SPL toolkit artifacts together.
    * **[spl-file]** - files containing SPl composites, functions, and types of the toolkit
    * **native.function** - a directory containing the function model of all native functions defined in this toolkit.
    * **[operator]** - a directory containing all artifacts relative to a Java / C++ primitive operator.  Each operator has its own separate directory.
* **impl** - the impl directory contains implementation code of primitive operators or native functions
    * **impl/java/src** - contains Java primitive operator or native function code
    * **impl/java/bin** - contains Java class files for the Java implementation code
* **lib** - contains any external libraries that this toolkit may require

Note:  If you use Streams Studio to create a new SPL project, Streams Studio will automatically create the correct directory structure for you.

See this video about how to create SPL project in Studio:  [VIDEO PENDING]

# Creating Your First Java Native Function

To create a Java native function:

*  Create a new class.  Place the java file of this class in the *impl/java/src* directory.
*  Create a new **public static** method
*  Annotate the function with the **@Function** annotation.  

Here's an example of a native function that calculates and returns the sum of two integers:

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

In this example:

* **name** - the name of the function in SPL
* **namespace** - the namespace of the function in SPL
* **description** - the description of the function. This information can be used to generate SPLDoc.  

Streams Studio provides a Java native function wizard.  You may create a new Java native function as follows:

1. Create a new SPL Project
1. Select the project, right click -> New -> Java Native Function
1. In the resulting dialog, specify the name, namespace, description and parameter information for the function.
1. Optionally, click Next, to specify the name of the Java class implementation of the function.
1. Click Finish will generate a Java class, the static function, and the @Function annotation.

See this video about how to create Java native function in Studio:  [VIDEO PENDING]

# Building the Java Native Function

To build the Java native function code and have it included as part of the SPL toolkit:

* Compile the Java code and place the class file in the *impl/java/bin* directory.  Make sure that the *com.ibm.streams.operator.jar* file is included as part of the classpath.  

~~~~~~
cd JavaFunctionSample/impl/java/src
javac -cp <Streams_Install>/lib/com.ibm.streams.operator.jar com/ibm/streamsx/sample/java/Calculator.java -d ../bin/
~~~~~~

*  Index the toolkit

~~~~~~
cd JavaFunctionSample
spl-make-toolkit -i ./
~~~~~~

The toolkit indexing process will generate the function model for the Java native function.  You should see the following files generated:

~~~~~~
JavaFunctionSample                                             -> this is the root of the toolkit
    com.ibm.streamsx.sample.java                               -> this is the namespace of the SPL funciton
        native.function                                        -> directory containing the native function
            javaFunction.xml                                   -> function model containing the function prototypes accessible from SPL
            SPL_JNIFunctions_com_ibm_streamsx_sample_java_h    -> wrapper JNI code for the Java functions
~~~~~~

# Testing the Java Function Code

To test the new Java native function, you need an SPL application that calls the function.  Typically, it is a good idea
to separate out the test code from the toolkit code.  Therefore, we will create a new SPL toolkit, JavaFunctionSampleTest for our test application.

See this video about how to test Java native function in Studio:  [VIDEO PENDING]

In JavaFunctionSampleTest, add the *JavaFunctionSample* as a toolkit dependency.  This will make the toolkit's functions accessible from the test toolkit.

This is the info.xml from JavaFunctionSampleTest:

~~~~~~
<?xml version="1.0" encoding="UTF-8"?>
<info:toolkitInfoModel xmlns:common="http://www.ibm.com/xmlns/prod/streams/spl/common" xmlns:info="http://www.ibm.com/xmlns/prod/streams/spl/toolkitInfo">
  <info:identity>
    <info:name>JavaFunctionSampleTest</info:name>
    <info:description></info:description>
    <info:version>1.0.0</info:version>
    <info:requiredProductVersion>4.0.1.0</info:requiredProductVersion>
  </info:identity>
  <info:dependencies>
    <info:toolkit>
      <common:name>JavaFunctionSample</common:name>            -> Added JavaFunctionSample toolkit as dependency
      <common:version>[1.0.0,2.0.0)</common:version>           -> Specify dependency version constraints:  1.0.0 to 2.0.0 (exclusive)
    </info:toolkit>
  </info:dependencies>
</info:toolkitInfoModel>
~~~~~~

Now, we will create a main composite that calls the Java native function.  In this application:

* Use a Beacon operator to generate 100 numbers, one every second.
* The Custom operator is used to invoke the *com.ibm.streamsx.sample.java::add(...)* function.
* We print out the sum of the current counter and the last counter.

~~~~~~
namespace application ;

// Import all functions from namespace
use com.ibm.streamsx.sample.java::* ;

composite JavaFunctionSampleTest
{
    graph
        // generate 100 numbers, 1 every second
        (stream<int32 counter> Beacon_1_out0 as O) as Beacon_1 = Beacon()
        {
            logic
                state : mutable int32 i = 0 ;
            param
                iterations : 100 ;
                period : 1.0 ;
            output
                O : counter = i ++ ;
        }

        // Custom operator to call the new function
        () as Custom_2 = Custom(Beacon_1_out0 as inputStream)
        {
            logic
                state :
                {
                    mutable int32 last = 0 ;
                }

                onTuple inputStream :
                {
                    // call the new add function, currentCounter + lastCounter
                    int32 sum = add(counter, last) ;

                    // print the result
                    printStringLn((rstring)counter + "+" + (rstring) last  + "=" + (rstring) sum) ;
                    
                    last = counter ;
                }
        }
}
~~~~~~

The best way to test this is to build this as a stand-alone application.  To compile this as a stand-alone application:

~~~~~~
cd [root directory  of test toolkit]

sc -M application::JavaFunctionSampleTest --output-directory=[build-output-dir] --data-directory=data -T -a -t ../JavaFunctionSample
~~~~~~

To run this program:

~~~~~~
cd [build-output-dir]
standAlone
~~~~~~

You should see program output like this:

~~~~~~
0+0=0
1+0=1
2+1=3
3+2=5
4+3=7
5+4=9
6+5=11
7+6=13
:
:
~~~~~~

# Packaging for Deployment

To package your toolkit for deployment you may want to create a jar file for your Java native function implementation classes.  Follow these steps to create the jar file and have it included in the SPL toolkit.

* To create a jar file for your Java primitive function implementation classes and place jar file in *impl/lib* directory.  When you build the jar file, make sure to include all the inner classes that are generated by the annotation processor from com.ibm.streams.operator.jar.

~~~~~~
cd JavaFunctionSample/impl/java/bin                  -> go to the java/bin directory
jar -cf functions.jar ./                             -> create functions.jar
mv functions.jar JavaFunctionSample/impl/lib         -> move functions.jar to impl/lib directory
~~~~~~

* Remove the class files

~~~~~~
cd JavaFunctionSample/impl/java/bin
rm -R com
~~~~~~

* Re-index the toolkit

~~~~~~
cd JavaFunctionSample
spl-make-toolkit -i ./
~~~~~~

# Referencing to Third-Party Libraries

If additional jars are required in the class path then it is recommended that the java native function implementation classes are packaged in a jar file and the jar file.  In the manifest file for the jar, add a Class-Path manifest entry that references required jars. These required jars would typically be contained within the toolkit. Typically these required jars are stored in the *opt* or *impl/lib* directory.

To add Class-path entry into the manifest, see the instructions here: [https://docs.oracle.com/javase/tutorial/deployment/jar/downman.html](Adding Classes to the JAR File's Classpath)

# Exception Handling

To execute Java functions, a single JVM is started for each processing element (PE) that calls into Java.  By default, any uncaught exception in the Java code will cause the PE to terminate.

There are a couple of ways to handle exceptions in your Java code:

* Catch all exceptions in Java and Log Errors

    Streams applications are supposed to run continuously and do not end.  When dealing with exceptions in your Java code, you have to think about whether the error is recoverable from your Streams application.  If the error is recoverable, then the exception should be caught and logged, and we should prevent the PE from crashing.  A PE should only be terminated if the error is truly non-recoverable.

    Here's one example of handling exception in a Java function:
    
* Handling Exceptions in SPL

    Alternatively, you can handle any uncaught exception in SPL.  Staring in Streams 4.1, you can add a ```@catch``` annotation in the SPL code to control how uncaught exceptions from primitve operators or native functions are to be handled.  To enable exception handling,     



# Log and Trace

# Type Mapping

# Fusion Considerations

# Performance Considerations

# Limitations

* Unable to develop this in Studio
* Unable to specify vm arguments

# References

[Java Function Development Reference on InfoCenter](https://www-01.ibm.com/support/knowledgecenter/#!/SSCRJU_4.0.0/com.ibm.streams.spl-java-operators.doc/api/com/ibm/streams/function/model/package-summary.html)