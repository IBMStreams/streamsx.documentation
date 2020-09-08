---
layout: docs
title:  Debugging a Streams Java Application using the Eclipse Debugger
description:
weight: 5
published: true
tag: java-app
prev:
    file: java-appapi-setting-parameters
    title: Setting parameter values when invoking operators
---

With the [streamsx.topology](http://ibmstreams.github.io/streamsx.topology/) toolkit, you can create a Streams application using only Java, Python, or Scala. 

If your application is developed using the Java Application API from the streamsx.topology toolkit, how can you use the Eclipse debugger to debug your application?

## Debugging in Embedded Mode

Recall that a very simple Streams application can be written in Java like this:

~~~~ java
    public class TemperatureTest {
    public static void main(String[] args) throws Exception{

    Topology topology = new Topology("temperatureSensor");
    Random random = new Random();

    TStream readings = topology.endlessSource(new Supplier(){ // Generate random readings
    @Override
    public Double get() {
    return random.nextGaussian();
    }
    });

    readings.print(); // Print the numbers
    StreamsContextFactory.getEmbedded().submit(topology); // Submit the topology for execution.
    }
    }

~~~~ 

This application has an endless source that continuously generates a list of random temperature readings. The numbers are then printed out to the console. The topology is then submitted to a Streams context to be executed. In this example, the application is submitted in `EMBEDDED` mode. When the application is submitted in `EMBEDDED` mode, the application is going to run in a simulated Java environment. In this Streams context, the execution of the Topology is done in the same JVM used to launch it. Therefore, you can use the Eclipse Java Debugger like you normally would to debug this application:

1.  Set a breakpoint to the location where you would like the debugger to stop
2.  In the Java Editor, right click -> Debug As Java Application

This will launch a debug session in Eclipse. This is the easiest way to develop and debug your Streams application in Java.

### Limitations of using `EMBEDDED` mode

*   Since the application is running in `EMBEDDED` mode, dynamic connection (publish/subscribe) is not supported. If you application uses dynamic connections, you will have to comment out this code for the application to launch.
*   When the application is launched in STANDALONE or DISTRIBUTED mode, the topology toolkit generates the SPL code for the application. It then builds the application bundle and then execute the bundle. In some cases, problems may only arise when the application is run in STANDALONE or DISTRIBUTED mode. For example, your application may have issues in specifying classpath dependencies or packaging of the application bundle. Launching of the debugger in `EMBEDDED` mode does not help debug these issues.

We still need a way to debug the Streams Java application when running in standalone or distributed mode.

## Debugging in Standalone or Distributed Mode

Debugging a Streams Java application in standalone and distributed mode is similar to debugging a Java primitive operator. The basic idea is that we are going to start the JVM running your Java topology in debug mode. Once the JVM is started, we are going to use the remote support from Eclipse Java Debugger to connect to the JVM and start a debug session. The trick is to figure how how we can specify the VM arguments to start the JVM in debug mode.

To launch a Java topology in debug mode, you can do the following:

1.  Specify submission parameters in your Streams application:

~~~~ java
    // Create map for submission time parameters
    Map<String, Object> subProperties = new HashMap<>();

    // Specify the debug parameters
    subProperties.put(ContextProperties.VMARGS, "-agentlib:jdwp=transport=dt_socket,suspend=y,server=y,address=127.0.0.1:7777");

    // run in distributed mode with parameters
    StreamsContextFactory.getStreamsContext("DISTRIBUTED").submit(topology, subProperties);
~~~~

1.  Run the Java application like you normally would
2.  Follow instructions from this [guide](/streamsx.documentation/docs/java/java-op-dev-pd/#start-the-eclipse-java-debugger) under the subheading **Start the Eclipse Java Debugger**, to attach to the JVM.

And that's it! I hope this helps debugging your Java Streams applications!