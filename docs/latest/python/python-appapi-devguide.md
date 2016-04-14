---
layout: docs
title:  Developing IBM Streams applications with Python
description:  Learn how to develop a sample IBM Streams application in Python by using the the Python Application API in the Topology Toolkit
---

**Important:** The Python Application API is currently an alpha release.


# Python Application API overview
Python is a popular language with a large standard library. The IBM Streams Python Application API enables you to create streaming analytics applications in Python.

The API is open source. An alpha release of the API is available for download from the [streamsx.topology](http://ibmstreams.github.io/streamsx.topology/) project on GitHub.

This guide covers the high-level concepts of streaming application development with Python. The guide also walks you through the process of creating a sample application to help you get more familiar with how to create an IBM Streams application with Python.

When you create an IBM Streams application written in Python, you can run the application in the following modes:

* As a **Streams distributed application** (DISTRIBUTED). When running in this mode, the application produced will be deployed automatically on your IBM Streams instance.
* As a **Streams Application Bundle file** (BUNDLE). When running in this mode, the application produces a SAB file that you can then deploy on your IBM Streams instance by using the `streamtool submitjob` command or by using the application console
* As a **stand-alone application** (STANDALONE).  When running in this mode, the application produces a Streams Application Bundle file (SAB file), but rather than submitting the SAB file to an instance, the bundle is executed. The bundle runs within a single process and can be terminated with Ctrl-C interrupts.


The Python Application API enables you to:

* Define the structure of a streaming application using Python
* Pass Python objects as tuples on a stream
* Define how streaming data is processed in a modular, scalable, and stateful manner

The sample applications in this guide illustrates each of these points in more detail.

If you'd prefer to dig in to the Pydoc yourself, you can find the documentation in the following installation directories:

* `com.ibm.streamsx.topology/doc/pydoc/streamsx.topology.context.html`
* `com.ibm.streamsx.topology/doc/pydoc/streamsx.topology.topology.html`


# Terminology
If you're new to IBM Streams and want to learn more about the terms in this guide, see the [IBM Streams glossary](www.ibm.com/support/knowledgecenter/SSCRJU_4.1.1/com.ibm.streams.glossary.doc/doc/glossary_streams.html) in IBM Knowledge Center.


# Prerequites
Before you can use the Python Application API, you must complete the following tasks:

1. Install IBM Streams Version 4.0.0 (or later) or IBM Streams Quick Start Edition Version 4.0.0 (or later):

  * [IBM Streams Version 4.1.1 installation documentation](http://www.ibm.com/support/knowledgecenter/SSCRJU_4.1.1/com.ibm.streams.install.doc/doc/installstreams-container.html)

  * [IBM Streams Quick Start Edition Version 4.1.1 installation documentation](http://www.ibm.com/support/knowledgecenter/SSCRJU_4.1.1/com.ibm.streams.qse.doc/doc/installtrial-container.html)

1. Ensure that you configure the IBM Streams product environment variable by entering the following command:
    ```
    source product-installation-root-directory/4.n.n.n/bin/streamsprofile.sh
    ```

    **Tip:** Add the source command to your `home-directory/.bashrc` shell initialization file. Otherwise, you must enter the command every time you start IBM Streams. For example, if the product is installed in the `/home/streamsadmin/InfoSphere_Streams/4.1.1.0` directory, add the following line to your `.bashrc` file:
    ```
    source /home/streamsadmin/InfoSphere_Streams/4.1.1.0/bin/streamsprofile.sh
    ```

1. Download the IBM Streams Topology Toolkit, which includes the Python Application API. You can download the most recent version of the toolkit from the IBMStreams organization on GitHub from the streamsx.topology [Releases page](https://github.com/Ibmstreams/streamsx.topology/releases).

  After the toolkit downloads, extract it to your file system.

1. Install CPython 3.5.0 or later [https://www.python.org](https://www.python.org).
The Python Application API has been tested with Python 3.5.1

1. Include the fully qualified path of the `com.ibm.streamsx.topology/opt/python/packages` directory in the PYTHONPATH environment variable. For example:
  ```
  export PYTHONPATH=/home/myuser/download/com.ibm.streamsx.topology/opt/python/packages:$PYTHONPATH
  ```




# Developing your first application
Streaming analytics applications are intended to run indefinitely because they meet the need for real-time data processing. (Unlike applications created for the Apache Hadoop framework, which are intended to terminate when a batch of data is successfully processed.) For example, consider a company whose product scans temperature sensors across the world to determine weather patterns and trends. Because there is always a temperature, there is a perpetual need to process data. The application that processes the data must be able to run for an indefinite amount of time.

The application must also be scalable. If the number of temperature sensors doubles, the application must double the speed at which it processes data to ensure that analysis is available in a timely manner. With the Python Application API, you can develop a streaming analytics application natively in Python.

To get started with the Python Application API, you'll use the example of reading data from a temperature sensor and printing the output to the screen.


## Creating a topology object
The first component of your application is a `Topology` object.

Include the following code in the temperature_sensor.py file (the main module):

```
from streamsx.topology.topology import Topology
topo = Topology("temperature_sensor")
```

A streaming analytics application is a directed flow graph that specifies how data is generated and processed. The `Topology` object contains information about the structure of the directed flow graph.


## Defining a data source
The `Topology` object also includes functions that enable you to define your data sources. In this application, the data source is the temperature sensor.

In this example, simulate temperature sensor readings by defining a Python generator function that returns an iterator of random numbers.

**Important:** Callable inputs to functions, such as the definition of the `readings()` function, cannot be defined in the `'_main_'` module. The inputs must be defined in a separate module.

Include the following code in the temperature_sensor.py file (the main module):

```
import temperature_sensor_functions
source = topo.source(temperature_sensor_functions.readings)
```

Include the following code in the temperature_sensor_functions.py file:
```
import random
def readings():
    while True:
        yield random.gauss(0.0, 1.0)
```

The `Topology.source()` function takes as input a zero-argument callable object, such as a function or an instance of a callable class, that returns an iterable of tuples. In this example, the input to `source` is the `readings()` function.  The `source` function calls the `readings()` function, which returns a generator object.  The `source` function gets the iterator from the generator object and repeatedly calls the `next()` function on the iterator to get the next tuple, which returns a new random temperature reading each time.

In this example, data is obtained by calling the `random.gauss()` function. However, you can use a live data source instead of the `random.gauss()` function.


## Creating a Stream
The `Topology.source()` function produces a `Stream` object, which is a potentially infinite flow of tuples in an application. Because a streaming analytics application can run indefinitely, there is no upper limit to the number of tuples that can flow over a `Stream`.  

Tuples flow over a `Stream` one at a time and are processed by subsequent data **operations**. Operations are discussed in more detail in the [Common Streams operations](#common-streams-operations) section of this guide.

A tuple can be any Python object that is serializable by using the pickle module.

Include the following code in the temperature_sensor.py file:

```
source = topo.source(temperature_sensor_functions.readings)
```


## Printing to output
After obtaining the data, you print it to standard output using the `sink` operation, which terminates the stream.

Include the following code in the temperature_sensor.py file:

```
source.sink(print)
```

The `Stream.sink()` operation takes as input a callable object that takes a single tuple as an argument and returns no value. The callable object is invoked with each tuple. In this example, the `sink` operation calls the built-in `print()` function with the tuple as its argument.  

**Tip:** The `print()` function is useful, but if your application needs to output to a file, you need to implement a custom sink operator.


## Submitting the application
After you define the application, you can submit it by using `streamsx.topology.context` module. When you submit the application, use the `submit()` function from the `streamsx.topology.context` module and pass the context type and the topology graph object as parameters to the function.

Include the following code in the temperature_sensor.py file:

```
streamsx.topology.context.submit("STANDALONE", topo.graph)
```

**Remember:** You can run your application in the following ways:

* As a **Streams distributed application** (DISTRIBUTED). When running in this mode, the application produced will be deployed automatically on your IBM Streams instance.
* As a **Streams Application Bundle file** (BUNDLE). When running in this mode, the application produces a SAB file that you can then deploy on your IBM Streams instance by using the `streamtool submitjob` command or by using the application console
* As a **stand-alone application** (STANDALONE).  When running in this mode, the application produces a Streams Application Bundle file (SAB file), but rather than submitting the SAB file to an instance, the bundle is executed. The bundle runs within a single process and can be terminated with Ctrl-C interrupts.


## The complete application
Your complete application should look like this:

The following code should be in the temperature_sensor.py file:

```
from streamsx.topology.topology import Topology
import streamsx.topology.context
import temperature_sensor_functions

def main():
    topo = Topology("temperature_sensor")
    source = topo.source(temperature_sensor_functions.readings)
    source.sink(print)
    streamsx.topology.context.submit("STANDALONE", topo.graph)

if __name__ == '__main__':
    main()
```


The following code should be in the temperature_sensor_functions.py file:

```
import random

def readings():
    while True:
        yield random.gauss(0.0, 1.0)

```

## Running the application
To run the sample application, enter the following command:

```
python3 temperature_sensor.py
```

Enter `Ctrl-C` to stop the application.

## Sample output
The contents of your output should look something like this:
```
...
1.6191338426594375
-0.3088492294198733
0.43973191574979087
-1.0249371132740133
-0.3151212021333815
-0.6787283449628287
-0.11907886745291935
-0.24096558784475972
...
```



# Common Streams Operations
The primary operations in the Python Application API are listed below.  After you create a `Stream` from `Topology.source()`, you can perform operations on the `Stream`.

Topology

* source

Stream

* filter
* transform
* parallel
* union
* sink

The following sections outline best practices for each type of operation.

You can also find more information about IBM Streams operations in the [Python Application API SPLDOC](http://ibmstreams.github.io/streamsx.topology/experimental/python/doc/spldoc/html/tk$com.ibm.streamsx.topology/ns$com.ibm.streamsx.topology.python$8.html)


## Creating data sources
A `source` operation fetches information from an external system and presents that information as a `Stream`.  The function for creating a source stream is `Topology.source()`.  It accepts as input a user-supplied callable object, such as a function or an instance of a callable class, that takes no arguments and returns an iterable. The `source` function returns a `Stream` whose tuples will be the result of iterating against the iterable returned by the provided callable.

From the temperature sensor example above (temperator_sensor.py), the input to the `source` function is the user-supplied function `temperature_sensor_functions.readings`.  The `readings` function produces data for the stream.

```
topo = Topology("temperature_sensor")
source =
    topo.source(temperature_sensor_functions.readings)
```

The following sections show operations that process each tuple that passes through the `Stream`.


## Filtering data
You can invoke `filter` on a `Stream` when you want to selectively allow and reject tuples from being passed to another stream. The filtering is done based on a provided callable object. The `Stream.filter()` function takes as input a callable object that takes a single tuple as an argument and returns True or False.

Filtering is an immutable operation. When you filter a stream, the tuples are not altered. (If you want to alter the type or content of a tuple, see the section [Transforming data](#transforming-data).)

For example, you have a `source` function that returns a set of four words from the English dictionary. However, you want to create a `Stream` of words that do not contain the letter "a".

To achieve this:

1. Define a `Stream` called `words` that is created by calling a function that generates a list of four words. (For simplicity, specify a `source` function that returns only four words.)

  Include the following code in the filter_words.py file:

  ```
  words = topo.source(filter_words_functions.words_in_dictionary)
  ```

  Include the following code in the filter_words_function.py file:

  ```
  def words_in_dictionary():
     return {"qualify", "quell", "quixotic", "quizzically"}
  ```

1. Define a `Stream` called `words_without_a` by calling a function that returns True if the tuple does not contain the letter "a" or False if it does. Then invoke the `filter()` function on the `Stream` named `words`.

  Include the following code in the filter_words.py file:

  ```
  words = topo.source(filter_words_functions.words_in_dictionary)
  words_without_a = words.filter(filter_words_functions.words_without_a)
  ```

  Include the following code in the filter_words_functions.py file:

  ```
  def words_without_a(tuple):
     return "a" not in tuple
  ```

The `Stream` that is returned, `words_without_a`, contains only words that do not include a lowercase "a".


### The complete application
Your complete application should look like this:

The following code should be in the filter_words.py file:

```
from streamsx.topology.topology import Topology
import streamsx.topology.context
import filter_words_functions

def main():
    topo = Topology("filter_words")
    words = topo.source(filter_words_functions.words_in_dictionary)
    words_without_a = words.filter(filter_words_functions.words_without_a)
    words_without_a.sink(print)
    streamsx.topology.context.submit("STANDALONE", topo.graph)

if __name__ == '__main__':
    main()
```

The following code should be in the filter_words_functions.py file:

```
def words_in_dictionary():
   return {"qualify", "quell", "quixotic", "quizzically"}

def words_without_a(tuple):
   return "a" not in tuple
```


### Sample output
Run `python3 filter_words.py`.

The contents of your output will look like this:

```
quixotic
quell
```


## Transforming data
You can invoke `transform` or `multi_transform` on a `Stream` when you want to:

* Modify the contents of the tuple
* Change the type of the tuple
* Break one tuple into multiple tuples

The following sections walk you through an example of each type of transform.

### Transform: Modifying the contents of a tuple
The `Stream.transform()` function takes as input a callable object that takes a single tuple as an argument and returns either 0 or 1 tuples.

For example, you have a `source` function that returns a set of four words from the English dictionary. However, you want to create a `Stream` that contains only the first four letters of each word. You need to use a `transform` operation because it enables you to modify the tuple.

To achieve this:

* Define a `Stream` called `words` that is created by calling a function that generates a list of four words. (For simplicity, specify a `source` function that returns only four words.)
* Define a `transform` function called `transform_substring_functions.first_four_letters` that transforms the tuples from the `words` `Stream` into tuples that contain the first four letters from the original tuple.
* Define a `sink` function that uses the `print` function to write the tuples to output.

Include the following code in the transform_substring.py file:

```
from streamsx.topology.topology import Topology
import streamsx.topology.context
import transform_substring_functions

def main():
    topo = Topology("transform_substring")
    words = topo.source(transform_substring_functions.words_in_dictionary)
    first_four_letters = words.transform(transform_substring_functions.first_four_letters)
    first_four_letters.sink(print)
    streamsx.topology.context.submit("STANDALONE", topo.graph)

if __name__ == '__main__':
    main()
```

Include the following code in the transform_substring_functions.py file:

```
def words_in_dictionary():
   return {"qualify", "quell", "quixotic", "quizzically"}

def first_four_letters(tuple):
   return tuple[:4]
```


#### Sample output
Run `python3 transform_substring.py`.

The contents of your output looks like this:

```
quix
quel
qual
quiz
```

As you can see, the `transform` operation modifies the tuples. In this instance, it the operation modifies the tuples so that only the first four letters of each word are returned.


### Transform: Changing the type of a tuple
In this example, you have a `Stream` of strings, and each string corresponds to an integer. You want to create a `Stream` that uses the integers, rather than the strings, so that you can perform mathematical operations on the tuples.

To achieve this:

* Define a `Stream` called `string_tuples` that is created by calling a function named `int_strings` that returns a list of string values that are integer values. (For simplicity, specify a `source` function that returns the following strings: "1", "2", "3", "4'.)
* Define a `transform` function called `transform_type_functions.string_to_int` that transforms the tuples from the `string_tuples` `Stream` into Python `int` objects.
* Define a `transform` function called `transform_type_functions.multiply2_add1` that multiples each `int` by 2 and adds one to the result.
* Define a `sink` function that uses the `print` function to write the tuples to output.

Include the following code in the transform_type.py file:

```
from streamsx.topology.topology import Topology
import streamsx.topology.context
import transform_type_functions

def main():
    topo = Topology("transform_type")
    string_tuples = topo.source(transform_type_functions.int_strings)
    int_tuples = string_tuples.transform(transform_type_functions.string_to_int)
    int_tuples.transform(transform_type_functions.multiply2_add1).sink(print)
    streamsx.topology.context.submit("STANDALONE", topo.graph)

if __name__ == '__main__':
    main()
```

Include the following code in the transform_type_functions.py file:

```
def int_strings():
   return ["1", "2", "3", "4"]

def string_to_int(tuple):
   return int(tuple)

def multiply2_add1(tuple):
   return (tuple * 2) + 1
```


#### Sample output
Run `python3 transform_type.py`.

The contents of your output looks like this:

```
3
5
7
9
```

**Tip:** You can transform a `Stream` tuple to any Python object if the returned object's class can be serialized using the pickle module.

Additionally, you aren't restricted to using built-in Python classes, such as string, integer, float, and so on. You can define your own classes and pass objects of those classes as tuples on a `Stream`.


### Transform: Breaking one tuple into multiple tuples
The `multi_transform` operation transforms each tuple from a `Stream` into 0 or more tuples.  The `Stream.multi_transform()` function takes a single tuple as an argument, and returns an iterable of tuples.

For example, you have a `Stream` in which each tuple is a line of text. You want to break each tuple down so that each resulting tuple contains only one word. The order of the words from the original tuple is maintained in the resulting `Stream`.  

* Define a `Stream` called `lines` that is created by calling a function that generates lines of text. (For simplicity, specify a `source` function that returns two lines from the nursery rhyme "Mary Had A Little Lamb".)
* Define a `transform` function called `multi_transform_lines_functions.split_line` that transforms each tuple from the `lines` `Stream` into multiple tuples, each consisting of one word.
* Define a `sink` function that uses the `print` function to write the tuples to output.


#### Sample application
To achieve this:

Include the following code in the multi_transform_lines.py file:

```
from streamsx.topology.topology import Topology
import streamsx.topology.context
import multi_transform_lines_functions

def main():
    topo = Topology("multi_transform_lines")
    lines = topo.source(multi_transform_lines_functions.lines_of_text)
    words = lines.multi_transform(multi_transform_lines_functions.split_line)
    words.sink(print)
    streamsx.topology.context.submit("STANDALONE", topo.graph)

if __name__ == '__main__':
    main()
```

Include the following code in the multi_transform_lines_functions.py file:

```
def lines_of_text():
   return ["mary had a little lamb", "its fleece was white as snow"]

def split_line(tuple):
   return tuple.split()
```   


#### Sample output
Run `python3 multi_transform_lines.py`.

The contents of your output looks like this:

```
mary
had
a
little
lamb
its
fleece
was
white
as
snow
```

As you can see, the `multi_transform` operation broke each of the original tuples into the component pieces, in this case, the component words, and maintained the order of the pieces in the resulting tuples.

**Tip:** You can use the `multi_transform` operation with any list of Python objects that is serializable with the pickle module. The members of the list can be different classes, such as strings and integers, user-defined classes, or classes provided by a third-party module.


## Keeping track of state across tuples
In the previous examples, you used **stateless** functions to manipulate the tuples on a `Stream`. A stateless function does not keep track of any information about the tuples that have been processed, such as the number of tuples that have been received or the sum of all integers that have been processed.

Keeping track of state information, such as a count or a running total, enables you to create more useful applications.

A **stateful** function references data that is preserved across calls to the function.

You can define stateful data within the scope of a callable object. The data is local to the function. When the function exits, the data is no longer accessible.

For example, you have a `Stream` of random numbers and you want to define an function that consumes the `Stream` and keeps track of the moving average across the last ten tuples. You can define a list in the callable object to keep track of the tuples on the `Stream`. The state of the list persists across calls to the function.

To achieve this:

Add the following code in the transform_stateful.py file:

```
from streamsx.topology.topology import Topology
import streamsx.topology.context
import transform_stateful_functions

def main():
    topo = Topology("transform_stateful")
    floats = topo.source(transform_stateful_functions.readings)
    avg = floats.transform(transform_stateful_functions.AvgLastN(10))
    avg.sink(print)
    streamsx.topology.context.submit("STANDALONE", topo.graph)

if __name__ == '__main__':
    main()
```

Add the following code in the transform_stateful_functions.py file:

```
import random

def readings():
    while True:
        yield random.gauss(0.0, 1.0)

class AvgLastN:
   def __init__(self, n):
      self.n = n
      self.last_n = []
   def __call__(self, tuple):
      self.last_n.append(tuple)
      if (len(self.last_n) > self.n):
          self.last_n.pop(0)
      return sum(self.last_n) / len(self.last_n)
```


### Sample output
Run `python3 transform_stateful.py`.

The contents of your output file should look something like this:

```
...
-0.129801183721193
-0.24261908760937825
-0.31236638019773516
-0.40426366430734334
-0.24643244932349337
-0.28186826075709115
...
```

In this example, `AvgLastN.n`, which is initialized from the user-defined parameter n, and `AvgLastN.last_n` are examples of data whose state is kept in between tuples.

**Tip:** Any type of of operation (source, filter, transform, and sink) can accept callable objects that maintain stateful data.

You can also create a user-defined function that refers to global variables. Unlike variables that are defined within a function, global variables persist in the runtime process. However, this approach is **not recommended** because the way in which the processing elements are fused can change how global variables are shared across functions or callable objects.

For example, in stand-alone mode, there is a single copy of a global variable. This copy is shared by all of the functions that reference it. In distributed mode, multiple copies of a global variable might exist because the topology is distributed across multiple processing elements (processes). If any Python code on a processing element executes a function that references the global variable, the processing element will have its own copy of the global variable.



## Creating data sinks
If you have the data that you need from a particular `Stream`, you need to preserve the tuples on the `Stream` as output. For example, you can use a Python module to write the tuple to a file, write the tuple to a log, or send the tuple to a TCP connection.

For example, you can create a `sink` function that writes the string representations of a tuple to a standard error message.

### Sample application
To achieve this:

* Define a `Stream` called `source` that is created by calling a function named `source_tuples` that returns a list of string values. (For simplicity, specify a `source` function that returns "tuple1", "tuple2", "tuple3").
* Define a `sink` function that uses the `print_stderr` function to write the tuples to stderr.

Include the following code in the sink_stderr.py file:

```
from streamsx.topology.topology import Topology
import streamsx.topology.context
import sink_stderr_functions

def main():
    topo = Topology("sink_stderr")
    source = topo.source(sink_stderr_functions.source_tuples)
    source.sink(sink_stderr_functions.print_stderr)
    streamsx.topology.context.submit("STANDALONE", topo.graph)

if __name__ == '__main__':
    main()
```

Include the following code in the sink_stderr_functions.py file:

```
import sys

def source_tuples():
    return ["tuple1", "tuple2", "tuple3"]

def print_stderr(tuple):
    print(tuple, file=sys.stderr)
    sys.stderr.flush()
```

Tip: If the `sink` function prints to the console, ensure the output to stdout or stderr is flushed by calling `sys.stdout.flush()` or `sys.stderr.flush()`, respectively.

### Sample output
Run `python3 sink_stderr.py`.

The contents of your stderr console looks like this:

```
tuple1
tuple2
tuple3
```


## Splitting streams
You can split a stream into more than one output stream. Splitting a stream enables you to perform different processing on the data depending on an attribute of a tuple. For example, you might want to perform different processing on log file messages depending on whether the message is a warning or an error.

You can split a stream by using any operator. Each time you call a function, such as `filter`, `transform`, or `sink`, the function produces one output stream. If you call a function on the same `Stream` three times, it creates three output streams.  The tuples from the input stream are distributed to all of the destination streams.

For example, the following code snippet splits the `stream1` `Stream` into two steams:

```
stream2 = stream1.filter(...)
stream3 = stream1.filter(...)
```

A visual representation of this code would look something like this:

![Visual representation of splitting a stream](../../../images/pythonGuide/stream_split.jpg)

The following example shows how you can distribute tuples from a `source` function to two `sink` functions.  Each `sink` function receives a copy of the tuples from the `source` `Stream`.

### Sample application
Include the following code in the split_source.py file:

```
from streamsx.topology.topology import Topology
import streamsx.topology.context
import split_source_functions

def main():
    topo = Topology("split_source")
    source = topo.source(split_source_functions.source_tuples)
    source.sink(split_source_functions.print1)
    source.sink(split_source_functions.print2)
    streamsx.topology.context.submit("STANDALONE", topo.graph)

if __name__ == '__main__':
    main()
```

Include the following code in the split_source_functions.py file:  

```
def source_tuples():
    return ["tuple1", "tuple2", "tuple3"]i

def print1(tuple):
    print("print1", tuple)

def print2(tuple):
    print("print2", tuple)
```

### Sample output
Run `python3 split_source.py`.

The contents of your output file should look something like this:
```
...
print2 tuple1
print1 tuple1
print2 tuple2
print1 tuple2
print2 tuple3
print1 tuple3
```


## Joining streams (union)
You can combine multiple streams into a single `Stream` by using the `union` operation. The `Stream.union()` function takes a set of streams as an input variable and combines them into a single `Stream`. However, the order of the tuples in the output `Stream` is not necessarily the same as in the input streams.

For example, you want to combine the streams from the `source` functions h, b, c, and w. You can combine the streams by using the `union` function and then use the `sink` function to write the resulting `Stream` to output.

### Sample application
To achieve this:

Include the following code in the union_source.py file:

```
from streamsx.topology.topology import Topology
import streamsx.topology.context
import union_source_functions

def main():
    topo = Topology("union_source")
   h = topo.source(union_source_functions.hello)
   b = topo.source(union_source_functions.beautiful)
   c = topo.source(union_source_functions.crazy)
   w = topo.source(union_source_functions.world)
    streamSet = {b, c, w}
    hwu = h.union(streamSet)
    hwu.sink(union_source_functions.print1)
    streamsx.topology.context.submit("STANDALONE", topo.graph)

if __name__ == '__main__':
    main()
```

Include the following code in the union_source_functions.py file:

```
def hello() :
    return ["Hello",]

def beautiful() :
    return ["beautiful",]

def crazy() :
    return ["crazy",]

def world() :
    return ["World!",]

def print1(tuple):
    print(" - ", tuple)
```


### Sample output
Run `python3 union_source.py`.

The contents of your output file should look something like this:

```
...
- Hello
- beautiful
- crazy
- World!
```

**Remember:** The order of the tuples might be different in your output.


# API features

## User-defined parallelism
If a particular portion of your graph is causing congestion because the application needs additional throughput at that point, you can define a **parallel region** in your graph. A parallel region enables the application to use multiple channels to run operations (such as filtering or transforming data) concurrently.

In the [Developing your first application](#developing-your-first-application) section, you created a topology and defined a pseudo temperature source. In this example, you want to convert all of the source tuples from Celsius to Kelvin.

To achieve this, add a function called `convertToKelvin()` to the application you created in the [Developing your first application](#developing-your-first-application) section.

Your application should look like this:

The following code should be in the temperature_sensor.py file:

```
from streamsx.topology.topology import Topology
import streamsx.topology.context
import temperature_sensor_functions

def main():
    topo = Topology("temperature_sensor")
    source = topo.source(temperature_sensor_functions.readings)
    kelvin = source.transform(temperature_sensor_functions.convertToKelvin)
    kelvin.sink(print)
    streamsx.topology.context.submit("STANDALONE", topo.graph)

if __name__ == '__main__':
    main()
```

The following code should be in the temperature_sensor_functions.py file:

```
import random

def readings():
    while True:
        yield random.gauss(0.0, 1.0)i

def convertToKelvin(tuple) :
        return tuple +  273.15
```

Converting a temperature reading from Celsius to Kelvin is not a resource-intensive task. However, you can use this example to see how using a parallel region can help distribute processing across resources when an operation is resource-intensive or inefficient and is causing a bottleneck in your application.

To parallelize an operation, invoke `.parallel()` on a `Stream` where you want to process data in parallel.

**Restriction:** Nested parallelism is not supported. You cannot invoke `parallel()` on a `Stream` that is already parallelized. If you do, your application will throw an exception.

To end parallel processing, invoke `.end_parallel()` on the parallelized `Stream`. When you invoke `end_parallel()` subsequent operations on the `Stream` that is returned by `end_parallel()` are not processed in parallel. For example, call `.end_parallel()` on the `kelvin` `Stream` before you call `sink(print)`.

The above example becomes:

```
def main():
    topo = Topology("temperature_sensor")
    source = topo.source(temperature_sensor_functions.readings)
    kelvin = source.parallel(4).transform(temperature_sensor_functions.convertToKelvin)
    end = kelvin.end_parallel()
    end.sink(print)
          streamsx.topology.context.submit("STANDALONE", topo.graph)
```

Any operations that are performed on the parallelized `Stream` occur in parallel to the degree that is specified in the `.parallel()` function. In the example above, you specified 4, which means that four channels process the data in the parallel region on the graph.
