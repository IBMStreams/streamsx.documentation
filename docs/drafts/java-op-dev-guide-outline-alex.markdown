---
layout: docs
title:  Java Operator Development Guide Outline - Alex
published: true
---
#  Java Operator Development Guide Outline - Alex

# Alex
## Quick start guide to talk about how to develop java operators

Outline:
1. Introduction – You can easily write operators in Java
2. Create a new Java Operator (with input and output ports) using Studio. Walk through template and explain methods:

I want to do a video of this section where I go through the template, but also have details so they can use this as a reference. 

a. annotations:

@PrimitiveOperator

@InputPorts

@OutputPorts

@Libraries

b. initialize()
c. allPortsReady()
d. process()
e. shutdown()

3. Discuss the high level differences between Source, Sink, and normal operator (produceTuples() vs. process())
4. Build a simple java operator from the template that will take in a string and id, then capitalize the String, forward the id, and write out a new field that is the size of the string.

Do we want a video for this? 

Idea for sample: “CapitalizeAndMeasure” – Takes in stream outputs id, capitalized myString, and the size of the string.
I’m open to more interesting ideas, but this is a simple getting start and can show:
1. Read in data and output the same thing.
2. Transforming data then outputting it.
3. Outputting an attribute that didn’t exist before.

5. Build a Java Sink operator for RabbitMQ

Start with java code that does simple rabbitMQ producing
Show how easy it is to leverage that and turn it into a Streams operator
@Libraries and leveraging jars
produceTuples() explanation

