---
layout: docs
title:  How to Debug Java Operators with Eclipse/Streams Studio
description: Steps to connect an operator in a running Streams application to the Eclipse Debugger
weight: 15
published: true
tag: java-op
prev:
  file: java-op-dev-pd
  title: Debugging with Eclipse
---

Recently I spent some time trying to tune a custom Java operator.  In this post I am going to share my experience on the process I followed to make my Java operator as efficient as the C++ version of the same operator.

I am developing a sink operator that needs to write efficiently to an external system.  We already have a version of the same operator written in C++.  We wanted to write a new version of the operator in Java to get around some of the limitations introduced by the C++ APIs from the external system.

## Baseline comparison

Once the operator had been written, the first step is to see how well it performs against the baseline. In this case, the baseline was the previous C++ implementation of the operator.

I wrote a small application that uses a beacon to generate data as fast as possible.  The data is sent directly to the sink operator.  The application is kept running for a prolonged period of time, and we take the average throughput rate.  In the first round of analysis, the throughput rate of the Java operator is disappointingly at about 28% of the C++ operator. This is not good, so we need to figure out why.

There are a few possibilities for the performance degradation:

1.  The switch of implementing the operator from C++ to Java.  Java operators have the reputation of performing slightly worse than a C++ operator due extra serialization that needs be done in the Streams runtime to send data to a Java operator through the JNI layer.
2.  The C++ APIs from the external system is way more efficient than the Java APIs
3.  The Java operator is not implemented efficiently, causing performance bottleneck.

Next, I proceeded to determine how much each of the above three points could contribute to the performance degradation in the Java sink operator.

## Java vs C++ Operators

To determine how much performance degradation was a result of switching from C++ to Java, I designed another benchmark to determine what the maximum throughput one can achieve with the Java operator. To do this I renamed the process method to processSlow and created a new process method that is empty (it does nothing). If I rerun the benchmark with this empty process I can understand the upper bound I can expect. This improved things but still was slower than expected. At this point, one of the key observations was made. The process method itself was _synchronized_. I removed the _synchronized_ keyword and ran it again. This was much better and performed better than the C++ operator. Of course, the C++ was doing the actual writes and this was not doing anything. The point is that there was hope and I could start examining the process method code more closely.

**Lesson Learned: do not synchronize the process method.** Use much finer grained synchronized blocks and only where absolutely needed.

## Implementation of the Java Operator

The most important method to optimize in a Java operator is the `process(StreamingInput<Tuple> stream, Tuple tuple)`  method.  I then started to move code from `processSlow` over to the empty process method. As I did this I ran the benchmarks to note any degradations. As a result of this, I optimized the code by doing the following:

## Remove all “synchronized” keywords in any method definition.

I found many unnecessary synchronized methods in the code to protect ourselves from processing tuples from multiple streams or handling of control input ports.  Each time the operator gets into one of these synchronized methods, the operator has to acquire the lock on the operator, do some work and then release the lock again. Removing the _synchronized_ keywords and adding finer grained synchronized sections only where necessary improved performance of the operator around 25%. As with any of these approaches the gains are all dependent on the scope of the initial problem.

**Lesson Learned: Synchronization is very expensive.** You should keep majority of the code in the operator non-synchronized, and pick very specific points in the operator where synchronization is really necessary.

## Remove unnecessary work in the `process` method chain

The next thing I looked at is whether the process method is implemented optimally.  I started out in the `process` method and went through all the methods that it may call to optimize the processing chain.  I found that the process method is doing a lot of unnecessary work.  For example, logging and tracing each of the tuples is very expensive as it involves concatenating strings, unnecessary checks, expensive string manipulations, inefficiently converting from blob to strings and vice-versa. Cleaning up the logic and making sure that all processing is done efficiently gave us another 10% performance boost. 

**Lesson Learned: String manipulations and logging are very expensive**. The process method is one of the most critical method in the whole operator. Be mindful on what work is being done in the entire call stack of the process method. Avoid any unnecessary checks (while the check may not be expensive, millions of them a second can add up). Logging/tracing must be minimal and any string manipulations need to be optimized or removed.

### Inlining Functions

After doing all that cleaning up, the operator was still not performing to par.  So, I did another experiment.  On the process method, we have delegated some checks and work out to another method.  Because you cannot tell Java that a method should be inline, I moved the work from the methods back into the process method, effectively inlining the work inside the process method.  This surprisingly gave us a 20% performance boost.

**Lesson Learned: Method calls are also expensive** to make, especially if the method is being called many, many times in a second. Minimize calling out to methods unless it is really necessary. If you are processing millions of tuples a second, and each results in 5 or 6 method calls, this can add up to a significant performance hit. A more subtle lesson here is that calling out to methods from the process method can make it harder to spot things like unnecessary logging or string manipulations because they are “hidden” in the called method. 

On the other hand, there needs to be some balance between performance and code readability, code reuse & standard Java practices. For example, it is better to call a getter method than use a field directly. The dynamic optimization performed by the JVM should effectively inline such method calls.

## Expensive Work to Background Thread

After all that clean up, there was not much I could do to make the operator perform any better.  So, I turned my attention to looking at how the operator is interfacing with the external system.  In the sink operator, we are using the default implementation of BufferedWriter to write data to the external system.  If you look closely at how the BufferedWriter is implemented, you would find that the write method of the BufferedWriter is synchronized.  In researching performance of BufferedWriter, I found that this synchronization is the reason for performance bottleneck in Java applications.

Another issue here was that when the operator writes to the external system, this writing is done on the thread where the process method is called. Oh, oh!! We know from above that synchronizes on the process thread are potentially problematic. This means that we have to wait for the write to finish before we can accept tuples again.

To further improve performance of the Java operator, I implemented my own writer to write data to the external system.  My writer is not synchronized at the method level and is only synchronized at the very specific points where I needed it.  I also implemented buffers inside the writer to batch up the amount of writes we have to actually do, and moved the writing to the background thread from the “processing thread”. This optimization improved performance by 20%, bringing us close to and in some cases better than how the C++ operator performs!

**Lesson Learned: move expensive (or slower) operations off the process thread.**  When dealing with an external system, the external system may not be able to process data as fast as Streams does. Writing to these external systems should be batched to reduce the number of actual writes necessary.  In addition, this work should be done in a background thread, away from the processing thread to help improve throughput.


## Notes/Tips

1. For sink type operators, the [pattern class TupleConsumer](https://www.ibm.com/support/knowledgecenter/SSCRJU_5.3/com.ibm.streams.spl-java-operators.doc/samples/com/ibm/streams/operator/samples/patterns/TupleConsumer.html) contains a worker thread that is used to send the tuples onto an external system. By using this pattern class a Java primitive operator developer can focus on the mechanism to send tuples to the external system, rather than threading etc. Then the operator can inherit the full behaviour of TupleConsumer including batching, timeouts etc. The source for this sample is located in  `$STREAMS_INSTALL/lib/com.ibm.streams.operator.samples.jar`.

Reply (Edit)	

1. It’s good to remember that multiple threads can call the operator’s process method concurrently, thus if it is synchronized that will cause the threads to execute the method serially. Multiple threads can occur when the input port is fused with an upstream operator that is multi threaded, or fused with multiple upstream operators connected to the same input port.
1. The “C++ version” of the operator actually used Java as well, since the client library it used called Java functions via JNI.


## Conclusion

Java operator can perform as well as C++ if we are careful with how we are writing the process method.  The extra serialization needed for Java operator to work is in fact negligible.  The important points are that we have to make sure that the process method is only doing work that is absolutely necessary.  Synchronization is expensive and should be minimized.  Finally, any expensive work in the process method should be batched up and moved to a background thread.

