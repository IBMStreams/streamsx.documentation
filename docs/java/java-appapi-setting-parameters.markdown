---
layout: docs
title:  Setting parameter values when invoking non-Java operators
description:  IBM Streams Java Operator Development Guide
weight: 4
published: true
tag: java-app
next:
    file: java-appapi-use-debugger
    title: Debugging with Eclipse
prev:
    file: java-appapi-files-in-app-bundle
    title: Working with files and other resources
---

The Java Application API provides the ability to invoke operators from any of the dozens of toolkits included in Streams and [available on GitHub](https://github.com/IBMStreams), regardless of whether the operator is written in Java, C++ Python, or SPL. 

One of the challenges with invoking non-Java operators is setting the value for a parameter whose type does not have a direct mapping to a Java primitive type. For example, setting a parameter that expects an unsigned 32-bit integer (uint32) cannot be done using a Java primitive type since Java does not natively support unsigned numbers.

Fortunately, the Java Application API provides a very simple mechanism for setting Java types to SPL types using the _SPL.createValue(T, MetaType)_ method. The following example demonstrates how to invoke the **spl.adapter::FileSink** operator. The source for this example [can be found here](https://github.com/cancilla/streamsdev/tree/master/FileSinkSample).


~~~~~ java
    public class Main {

        public static void main(String[] args) throws Exception {
            Topology t = new Topology("FileSink_Invoke_Sample");

            // Creating source stream
            TStream<String> src = t.strings("a", "b", "c", "d", "e");

            // Converting topology stream (TStream) to SPL stream (SPLStream)
            StreamSchema schema = Type.Factory.getStreamSchema("tuple<rstring data>");
            SPLStream splStream = convertToSPLStream(src, schema);

            // >>> Invoking FileSink Operator <<<
            Map<String, Object> params = new HashMap<>();
            params.put("file", "/tmp/test.txt");

            SPL.invokeSink("spl.adapter::FileSink", splStream, params);

            StreamsContextFactory.getStreamsContext("STANDALONE").submit(t).get();
        }

        private static SPLStream convertToSPLStream(TStream<String> tStream, StreamSchema schema) {
            return SPLStreams.convertStream(tStream, new BiFunction<String, OutputTuple, OutputTuple>() {
                private static final long serialVersionUID = 1L;

                @Override
                public OutputTuple apply(String data, OutputTuple outTuple) {
                    outTuple.setString(0, data);
                    return outTuple;
                }

            }, schema);
        }
    }

~~~~~ 


In the preceeding example, the FileSink operator is being invoked with only the **file** parameter set. The **file** parameter type is `rstring`, which directly maps to the Java `String` data type. Therefore, there is no need to use `SPL.createValue(...)`. Next, we'll look at how to set the **flush** parameter, which has a type of `uint32`. Here is the new code section for invoking the FileSink operator.



~~~~ java
    // Invoking FileSink Operator
    Map<String, Object> params = new HashMap<>();
    params.put("file", "/tmp/test.txt");
    params.put("flush", SPL.createValue(1, com.ibm.streams.operator.Type.MetaType.UINT32)); // <<<< flush param

    SPL.invokeSink("spl.adapter::FileSink", splStream, params);

~~~~ 


Setting the value of the parameter is done by simply calling _SPL.createValue()_ with the value you want to set and the SPL type that the parameter expects.

## Setting enum parameter values

There are many parameters whose values are constrained using enums. A Java `enum` type can be mapped directly to an SPL enum when setting parameter values. However, you must first create a Java enum that contains the value you plan to set. The following example shows how to set the **format** parameter when invoking the FileSink operator.


~~~~ java
    public class Main {
      static enum FileSinkFormat { csv }; // <<<< define enum

        public static void main(String[] args) throws Exception {
        ...

            // Invoking FileSink Operator
            Map<String, Object> params = new HashMap<>();
            params.put("file", "/tmp/test.txt");
            params.put("flush", SPL.createValue(1, com.ibm.streams.operator.Type.MetaType.UINT32));
            params.put("format", FileSinkFormat.csv); <<<< Set value using FileSinkFormat enum

            SPL.invokeSink("spl.adapter::FileSink", splStream, params);

        ...
        }
      ...

~~~~


At the class-level, we have defined an **enum** called `FileSinkFormat` that contains the value **csv**. We then use this enum value to set the parameter value before invoking the operator. **_NOTE:_** You do not need to create an enum that contains all of the possible values. The enum only needs to contain the values you plan to set for the parameter. Thanks to @dlaboss for helping to figure this out in [Issue #261](https://github.com/IBMStreams/streamsx.topology/issues/261).