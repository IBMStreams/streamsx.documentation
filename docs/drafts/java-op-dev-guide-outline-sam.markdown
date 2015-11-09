---
layout: docs
title:  Java Operator Development Guide Outline - Sam
published: true
---

# Samantha

## Introduction

* The goal of this guide is to walk through the steps and basic concepts of creating a Java operator and also Java Functions
* This is not intended to be a comprehensive guide, but enough to get users going.
* We also want to go through the basic process of creating an operator, and how one would usually expand and build on top of it.

* Streams supports Java and why this is important 
    * many java libraries and applications in the world
    * allow for code reuse
    * many java developers
    
* Streams allows Java code to be run in one of two ways:
    * Java operator
    * Java function
    * Briefly describe when we would want to use which?
        * java operator - almost like a template, people can drag and drop the template and customize via parameters
        * java function - more flexible, but more work for end-user.  Functions can be used anywhere, but require end-user to use things like the custom operator
        
## Java Operator Development Guide

### Java Operator Life-Cycle

* the redbook does a pretty good job here, reuse 
* talks about the different methods:  initialize, process(), processTuples(), shutdown, etc.
* do not good into details about source operators, threading models, locks, etc.  The goal here is to provide basic understanding of the operator life-cycle.
* We also will not talk about all the different annotations at this point.  We will talk about them when we need them.

### Creating the First Java Operator

* only requirement here is that the java class has to implement the Operator interface
* client may optionally extend from AbstractOperator
* Talk about @PrimitiveOperator, @InputPorts and @OutputPorts - only talk about the basic, like desciprtion, cardinality and optional.  Skip topics about windowing.

```
@PrimitiveOperator(name="MyJavaOp", namespace="com.ibm.streamsx.sample.MyJavaOp",
description="Java Operator MyJavaOp")
```
```
@InputPorts({@InputPortSet(description="Port that ingests tuples", cardinality=1, optional=false, windowingMode=WindowMode.NonWindowed, windowPunctuationInputMode=WindowPunctuationInputMode.Oblivious), @InputPortSet(description="Optional input ports", optional=true, windowingMode=WindowMode.NonWindowed, windowPunctuationInputMode=WindowPunctuationInputMode.Oblivious)})
@OutputPorts({@OutputPortSet(description="Port that produces tuples", cardinality=1, optional=false, windowPunctuationOutputMode=WindowPunctuationOutputMode.Generating), @OutputPortSet(description="Optional output ports", optional=true, windowPunctuationOutputMode=WindowPunctuationOutputMode.Generating)})
```

* steps to create this operator in Studio 
* shoot video

* What happens when the project is built?
   * talk about how SPL compiler parses the annotation and generates the operator model for the Java operator
   * customers should not modify the generated operator model.  Use annotations to control the annotation model
   
### Implementing the First Java Operator

* Design a simple sample that will go through all the different life-cycle methods, except for processTuples
* Make sure we add trace statements to all of the methods for user to understand when the life-cycle methods are called
* Operator should have one input and one output port - this should be the most basic setup.

### Running and Testing the First Java Operator

* Discuss how one would test this Java operator and have it running
* Create a separate SPl application that calls this Java operator - the best practise is to have a small external SPL application that invokes the operator being developed
* Show it running as stand-alone - to demonstrate that this runs
* Show it running as distributed - talk about how to get logs and debug the simple java operator.   

### Reusing functions from existing libraries

* In this session, we discuss how customers can reuse existing code
* Sample should have some library / client written, but stored externally in a jar file
* Use the @Library tag to add the jar file into the class path, and reuse these functions in the operator.
* I would avoid using a third-party library for this exercise.  I think it makes things more complicated, as user has to learn the third-party library.  Have simple code that we want to reuse.
* Discuss the @Library annotation
* Show the generated operator
* Talk about referencing libraries using environment variables
* Talk about using astericks
* Run the example again to demonstrate.

### Adding parameters

* Next step is to add a new parameter to the operator
* Use @Parameter to add new parameter
* Discuss how to get to the parameter and use it in the code
* Discuss limitations on parameters, compared to C++
* Run the example again to demonstrate

### Adding custom metrics

* Next step is to add custom metric to help monitor the operator and also good for debugging
* Use the @Metric annotation and discuss it
* Demonstrate how to implement
* Demonstrate how to see these custom metrics in Studio and Console

### Error Handling and Error Port

* Best practise is to log and submit error to error port
* Operator should not crash
* Library should throw some exception
* Add an error port
* submit error information to error port

At this point, I would say we have gone through all the beginner topics.  Next step is to start talking about the Advanced Topics

### Implementing Source Operator
* Why is source operator special?
* How to implement source operator?
* Threading considerations

### Processing Punctuation

* What are punctuations?
* What call backs are called?
* Threading considerations
* How to ensure that the operator is thread-safe

### Handling Window

* Discuss the different window configurations for input ports and output ports
* Demonstrate how to handle
   
### Compile time checks
* How to implement compile time checks

### Debugging Java operator using the Eclipse Java Debugger
* Reference to my document on StreamsDev

### Performance Tuning
* Discuss some of the things to watch out for to avoid performance problems
* No unnecessary locks
* Reduce function calls in the process method stack
* Do not copy data
* How to monitor performance - using metrics view and alerts
* How to measure performance - may consider putting the FlowCalculator operator as a sample on Github.
* Reference to my document on StreamsDev

## Java Function Development Guide       

TBD
    
