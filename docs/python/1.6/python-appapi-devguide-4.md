---
layout: docs
title:  Common Streams transforms
description:  The primary transforms in the Python Application API are listed
weight:  40
published: true
tag: py16
prev:
  file: python-appapi-devguide-3
  title: "Create an application with an IBM Streams installation"
next:
  file: python-appapi-devguide-5
  title: "API features: User-defined parallelism"
---

This section will discuss how to use the most common functions and transforms in the Streams Python API to analyze your data.

* [Introduction](#intro)
* [Creating a data source](#source)
  - [Ingesting data from popular systems](#adapters)
  - [Examples](#examples)
  - [Working with files](#files)
* [Viewing the contents of a `Stream`](#views)
* [Creating data sinks](#sink)
* [Filtering data from the stream](#filter)
* [Transforming data with custom logic](#map)
* [Keeping state information](#state)
* [Splitting streams](#split)
* [Joining streams](#union)
* [Sharing data between Streams applications](#publish)

Find detailed information about all available transforms in the documentation for the [Stream class](https://streamsxtopology.readthedocs.io/en/stable/streamsx.topology.topology.html#streamsx.topology.topology.Stream).

<a id="intro"></a>

# Introduction

Streams applications are directed graphs of data. The start of the graph is a data source that produces a source [`Stream`](https://streamsxtopology.readthedocs.io/en/stable/streamsx.topology.topology.html#streamsx.topology.topology.Stream), which is processed and analyzed using various transforms, ultimately getting sent to a data sink such as a database or file.

![streams graph animation](/streamsx.documentation/images/python/streams-graph.gif)

As shown above,
1. The data source is a Python class or function that will produce the data to be analyzed. It could be data from Kafka, a file, database, etc.  That data is converted to a `Stream` object called the source `Stream`.
2. The source `Stream` is processed by one or more transforms. A transform could be computing the average of the data on a `Stream`, or filtering out bad data, and so on.
3. Each transform produces another `Stream` as output, which is then forwarded to the next transform.  
4. The last `Stream`, containing the results, is sent to a data sink, another function that will save the data to an external system.

In the previous section, you created a very simple application that created a `Stream` of random numbers and printed it:

~~~~ python
def get_readings():
    while True:
        yield {"id": "sensor_1", "value": random.gauss(0.0, 1.0)}

topo = Topology("temperature_sensor")
src = topo.source(get_readings) # create a source Stream
src.for_each(print) # print the data on the stream
streamsx.topology.context.submit("DISTRIBUTED", topo)
~~~~    

Sample output:
~~~~    
{"id": "sensor_1", "value":-0.11907886745291935}
{"id": "sensor_1", "value":-0.24096558784475972}
...
~~~~~~

The code above defines a `Topology`, or application with the following graph:

![sample app](/streamsx.documentation/images/python/basic.jpg)

Here, the `get_readings` function produces the data that will be analyzed. The `src` `Stream` contains the data produced by `get_readings`.

The source `Stream` is created by calling `Topology.source()` .

In this example, there are no real transforms on the `src` `Stream`. The rest of this section will cover common transforms and best practices.

### A note about execution
The Python API is used to _create_ an application that can be executed on the Streams runtime.  The last line, which calls `submit`, is what triggers the compilation and execution of the application.

This means that callables such as the `get_readings` function are not invoked when the code above is run, but rather, when the created application is executed on the Streams runtime.

This is important to remember because the host where the application is created is often not the same host where it will be executed, i.e. where Streams is installed. For example, if the `get_readings` function opens a file, that file must actually exist on the host where Streams is running. See [working with files](#files) for an example.


<a id="source"></a>

<br/>
## Creating data sources

As mentioned, applications always begin by creating a source `Stream` that contains the data you want to process.
To create the source `Stream`:

1. Write a callable, such as a function or a class, that will connect to the external system and return an [iterable](https://docs.python.org/3/glossary.html#term-iterable).
2. Create your source `Stream` by passing the callable to `Topology.source()`

Example of the basic pattern:
~~~~~~ python
class DbAdapter
  def __call__(self):
    #connect to db/site/e.t.c
    # return data

topo = Topology()
incoming_data = topo.source(DbAdapter())
~~~~~~

Before we discuss source functions further, note that adapters exist for common systems, which you can use instead of writing your own function.

<a id="adapters"></a>
### Ingesting data from popular systems
If you want to process data from one of the following systems, you can use the corresponding Streams Python package instead of writing your own function.

| Application/System        | Package          |
| ------------- | ------------- |
| CSV File on local file system      | Python standard libraries, see the [working with files section below](#files) |
| Hadoop File System (HDFS)    | [streamsx.hdfs](https://streamsxhdfs.readthedocs.io/en/latest/)      |
| Kafka | [streamsx.kafka](https://streamsxkafka.readthedocs.io/en/latest/)      |
| IBM Event Streams | [streamsx.eventstreams](https://streamsxeventstreams.readthedocs.io/en/1.0.0/)      |
| IBM Cloud Object Storage | [streamsx.objectstorage](https://streamsxobjectstorage.readthedocs.io/en/latest)      |
| HTTP servers | [streamsx.inet](https://streamsxinet.readthedocs.io/en/latest/)      |
| JDBC  Database  | [streamsx.database](https://streamsxdatabase.readthedocs.io/en/latest/)      |


**Note:**

These packages are not part of the streamsx package and must be installed using `pip`.
Also, the list above does not include adapters that only support writing *to* the external system or other general utilities. See [the IBM Streams page on PyPi](https://pypi.org/user/ibmstreams/) for the most up to date list of available packages.

## Creating your own source function/callable

The callable passed to `Topology.source()` must:
- Take no arguments, and,
- Return an [iterable](https://docs.python.org/3/glossary.html#term-iterable), such as a list.

### How it works

* When the Streams runtime begins running your application, the callable, (e.g. the `get_readings` function) is invoked and it returns an iterable. The runtime then iterates through the available data by repeatedly calling [__next__](https://docs.python.org/3/library/stdtypes.html#iterator.__next__) on the iterable. Each returned item that is not `None` is submitted as a tuple for downstream processing.
* When or if the iterator throws a `StopException`, no more tuples appear on the source stream.

<a id="examples"></a>
#### Example: Fetch data repeatedly using a blocking source
If you have to repeatedly connect to an external system for data, use `yield` within a loop to repeatedly fetch and return data:

~~~~~~ python
class Readings(object):
  def __call__(self):
    while True:
      next_tuple = poll_for_data()
      yield next_tuple

topo = Topology("readings")
incoming_data = topo.source(Readings())
~~~~~~

### Functions vs. callable classes

You can implement your source callable as a function or a callable class.  Using a callable class is the recommended option because it allows you to keep state and also restore state in the event of an outage.
Let's see an example of the difference.

Our use case is tracking recent changes to Wikipedia. The data source, [Wikipedia event streams](https://stream.wikimedia.org/?doc#!/Streams), is a live stream of recent updates and changes. We will use the [Python Server Side Event (SSE) client](https://github.com/btubbs/sseclient) to retrieve the Wikipedia data.

We could use a simple function:

<a id="full-fn"></a>
~~~~ python
from sseclient import SSEClient
import logging
import json
import streamsx.ec
from streamsx.topology.topology import Topology
import streamsx.topology.context

def wikipedia_stream():
    eventSource = SSEClient("https://stream.wikimedia.org/v2/stream/recentchange", last_id='')
    while True:
        raw_event= next(eventSource)
        if raw_event.id == None: continue
        try:
            parsed_json = json.loads(raw_event.data)
            event = {"ts": parsed_json["timestamp"],
                     "user": parsed_json["user"], "type"
                     "page": parsed_json["meta"]["uri"],
                     "title": parsed_json["title"]}
                yield event
            # Check if the application has shut down between emitted events
            if streamsx.ec.shutdown().wait(0.05): break
        except ValueError: continue


topo = Topology(name="TrackWikipediaEdits")
source = topo.source(wikipedia_stream, name="WikipediaDataSource")
source.print()
~~~~

Or, a callable class:

<a id="full-class"></a>

~~~~~ python
from sseclient import SSEClient
import logging
import json
import streamsx.ec

class WikipediaReader(object):
    def __init__(self, url='https://stream.wikimedia.org/v2/stream/recentchange', filterWiki=None):
        # called when the topology is declared
        self.sseURL = url
        self.counter = 0
        self.filterWikis = filterWiki

    def __enter__(self):
        # Application is starting on the Streams runtime,
        self.eventSource = SSEClient(self.sseURL, last_id='')
        logging.getLogger("WikipediaSource").info("INFO: Wikipedia Source starting up")

    def __exit__(self, exc_type, exc_value, traceback):
        # called to handle an exception or shutdown
        if exc_type or exc_value or traceback:
            #decide if the exception can be ignored
            #return True to suppress and False otherwise
            logging.getLogger("WikipediaSource").warning("WARN: Some exception")
        else:
            #Process is shutting down
            return False
    def __call__(self):
        self.eventSource = SSEClient(self.sseURL, last_id='')
        while True:
            # Submit a tuple in each iteration:
            event = next(self.eventSource)
            if event.id == None: continue
            try:
                data = json.loads(event.data)
                event = {"ts": parsed_json["timestamp"],
                         "user": parsed_json["user"], "type"
                         "page": parsed_json["meta"]["uri"],
                         "title": parsed_json["title"]}
                yield event   
                # Check if the application has shut down between emitted events
                if streamsx.ec.shutdown().wait(0.05): break
            except ValueError: continue
~~~~~

### Advantages of using a callable class
When you compare the two examples above, you'll notice that although `WikipediaReader.__call__` is similar to the `wikipedia_stream` function, the `WikipediaReader` class also has `__enter__` and `__exit__` functions.

- The `__enter__` function is called by the Streams runtime whenever the process executing your application is started or restarted.  This allows you to perform any necessary initialization, such as creating a connection to a database. In our example we initialized the `SSEClient` object. You could also define metrics, or, in the case of a restart due to system outage, restore any previously saved state.

- Similarly, the `__exit__` function allows you to handle exceptions that occurred in the `__call__` function, and also perform any cleanup when the process is shutting down.

Note that  `__enter__`  is invoked at a different time from the constructor, `__init__`.  The class constructor is called when the `Topology` is declared. This is when the Streams application is being created and _before_ it is compiled.  The  `__enter__` function is called after the application has been successfully compiled and is being executed within the Streams runtime.


### Simple Iterable sources: Lists

Used when you have a finite set of data to analyze, e.g. a list. The iterable is returned directly by the function passed to `Topology.source()`.

~~~~ python
# Open a tar file and return list of file names
def get_log_files():
    file_names = []
    with tarfile.open('/path/to/logs.tar.gz') as tar_file:
        tar_file.extractall()
        file_names =  tar_file.getnames()
    return file_names
~~~~

**Note**: In the above example, the `logs.tar.gz` file must be present on the host where Streams is installed. See below for instructions on how to use local files in your Streams application.

<a id="files"></a>
## Working with files

Reading from a file or using a file within your Streams application can be done using any of the built-in file handling functions in Python.

However, you must use `Topology.add_file_dependency` to ensure that the file or its containing directory will be available at runtime.

~~~ python
topo = Topology("ReadFromFile")
topo.add_file_dependency("/home/streamsadmin/hostdir/mydata.txt" , "etc")
~~~

This will place the file within the `etc` folder of the application bundle.

At runtime, the full path to `mydata.txt` will be:

~~~ python
streamsx.ec.get_application_directory() + "/etc/mydata.txt`
~~~

Below are some complete examples.


### Using data from a file as your data source

This is a basic example of reading a file line by line:
~~~ python
import streamsx.ec

class FileReader:
    def __init__(self, file_name):
        self.file_name = file_name            
    def __call__(self):
        # iterate over file contents
        with open(streamsx.ec.get_application_directory()
                       + "/etc/" +  self.file_name) as handle:
            for line in handle:
                yield line.strip()


file_name = "mydata.txt"
topo = Topology("ReadFromFile")
topo.add_file_dependency("/home/streamsadmin/hostdir/" + file_name , "etc")
lines_from_file = topo.source(FileReader(file_name))
lines_from_file.print()

~~~

The `FileReader` class uses `streamsx.ec.get_application_directory() ` to retrieve the path to the file on the Streams host, and then returns the file's contents one line at a time.

**CSV Files**

The `FileReader` class can easily be extended to read CSV data.  For example, if your CSV file had the following format:
```
timestamp,max,id,min
1551729580087,18,"8756",8
1551729396809,0,"6729",0
1551729422809,25,"6508",5
```

You could define a new class to read each line into a `Stream` of `dicts` as follows:
~~~ python

class CSVFileReader:
    def __init__(self, file_name):
        self.file_name = file_name
    def __call__(self):
        # Convert each row in the file to a dict
        header = ["timestamp","max", "id", "min"]
        with open(streamsx.ec.get_application_directory()
               + "/etc/" +  self.file_name) as handle:
            reader = csv.DictReader(handle, delimiter=',',
                                    fieldnames=header)
            #Use this to skip the header line if your file has one
            next(reader)
            for row in reader:
                yield row

topo = Topology(name="CSVFileReader")
topo.add_file_dependency("path/on/local/fs/mydata.txt" , "etc")
lines = topo.source(CSVFileReader("mydata.txt"))
lines.filter(lambda tpl: int(tpl["min"]) >= 5).print()  

~~~~

Sample output:

~~~~ python
{'min': '18', 'id': '8756', 'max': '26', 'timestamp': '1551729580087'}
{'min': '5', 'id': '6508', 'max': '25', 'timestamp': '1551729422809'}
~~~~


### Itertools

The Python module [itertools](https://docs.python.org/3/library/itertools.html) implements a number of iterator building blocks that can therefore be used with the `source` transform.  

#### Infinite counting sequence

The function [count()](https://docs.python.org/3/library/itertools.html#itertools.count) can be used to provide an infinite stream
that is a numeric sequence. The following example uses the default start of 0 and step of 1 to produce a stream of `1,2,3,4,5,...`.

````
import itertools
def infinite_sequence():
    return itertools.count()
````

#### Infinite repeating sequence

The function [repeat()](https://docs.python.org/3/library/itertools.html#itertools.repeat) produces an iterator that repeats the same value,
either for a limited number of times or infiintely.

````
import itertools
# Infinite sequence of tuples with value A
def repeat_sequence():
    return itertools.repeat("A")
````

### Reference
* [Topology.source](https://streamsxtopology.readthedocs.io/en/stable/streamsx.topology.topology.html#streamsx.topology.topology.Topology.source)
* [Topology.add_file_dependency](https://streamsxtopology.readthedocs.io/en/stable/streamsx.topology.topology.html#streamsx.topology.topology.Topology.add_file_dependency)


<a id="filter"></a>
## Filtering data
You can invoke the `filter` transform on a `Stream` object when you want to selectively allow tuples to be passed and reject tuples from being passed to another stream. The filtering is done based on a provided callable object. The `Stream.filter()` function takes as input a callable object that takes a single tuple as an argument and returns True or False.

Filtering is an immutable transform. When you filter a stream, the tuples are not altered. (If you want to alter the type or content of a tuple, see [Transforming data](#map).)

For example, you have a `source` function that returns a set of four words from the English dictionary. However, you want to create a `Stream` object of words that do not contain the letter "a".

To achieve this:

1. Define a `Stream` object called `words` that is created by calling a function that generates a list of four words. (For simplicity, specify a `source` function that returns only four words.)

    Define the following functions in the `filter_words.py` file:


        def words_in_dictionary():
           return {"qualify", "quell", "quixotic", "quizzically"}

        def does_not_contain_a(tuple):
           return "a" not in tuple


1. Next, define a topology and a stream of Python strings in `filter_words.py`:

        topo = Topology("filter_words")
        words = topo.source(words_in_dictionary)


1. Define a `Stream` object called `words_without_a` by passing the `does_not_contain_a` function to the `filter` method on the `words` Stream. This function is True if the tuple does not contain the letter "a" or False if it does.

    Include the following code in the `filter_words.py` file:


        words = topo.source(words_in_dictionary)
        words_without_a = words.filter(does_not_contain_a)


The `Stream` object that is returned, `words_without_a`, contains only words that do not include a lowercase "a".


### The complete application
Your complete application is contained in a single file, 'filter_words.py`.

~~~~~~
from streamsx.topology.topology import Topology
import streamsx.topology.context

def words_in_dictionary():
   return {"qualify", "quell", "quixotic", "quizzically"}

def does_not_contain_a(tuple):
   return "a" not in tuple

def main():
    topo = Topology("filter_words")
    words = topo.source(words_in_dictionary)
    words_without_a = words.filter(does_not_contain_a)
    words_without_a.for_each(print)
    streamsx.topology.context.submit("STANDALONE", topo)

if __name__ == '__main__':
    main()
~~~~~~

### Sample output
Run the `python3 filter_words.py` script.

The contents of your output looks like this:

~~~~~~
quixotic
quell
~~~~~~

<a id="views"></a>
## Viewing the contents of a stream
TBD


<a id="sinks"></a>
## Creating data sinks
If you have the data that you need from a particular `Stream` object, you must preserve the tuples on the `Stream` object as output. For example, you can use a Python module to write the tuple to a file, write the tuple to a log, or send the tuple to a TCP connection.

For example, you can create a `sink` function that writes the string representations of a tuple to a standard error message.

### Sample application
To achieve this:

* Define a `Stream` object called `source` that is created by calling a function called `source_tuples` that returns a list of string values. (For simplicity, specify a `source` function that returns "tuple1", "tuple2", "tuple3").
* Define a `sink` function that uses the `print_stderr` function to write the tuples to stderr.

Include the following code in the `sink_stderr.py` file:

~~~~~~
from streamsx.topology.topology import Topology
import streamsx.topology.context
import sys

def source_tuples():
    return ["tuple1", "tuple2", "tuple3"]

def print_stderr(tuple):
    print(tuple, file=sys.stderr)
    sys.stderr.flush()

def main():
    topo = Topology("sink_stderr")
    source = topo.source(source_tuples)
    source.for_each(print_stderr)
    streamsx.topology.context.submit("STANDALONE", topo)

if __name__ == '__main__':
    main()
~~~~~~

Tip: If the `for_each` transform prints to the console, ensure the output to stdout or stderr is flushed afterward by calling `sys.stdout.flush()` or `sys.stderr.flush()`.

### Sample output
Run the `python3 sink_stderr.py` script.

The contents of your stderr console look like this:

~~~~~~
tuple1
tuple2
tuple3
~~~~~~


<a id="map"></a>
## Modifying data
You can invoke `map` or `flat_map` on a `Stream` object when you want to:

* Modify the contents of the tuple.
* Change the type of the tuple.
* Break one tuple into multiple tuples.

The following sections walk you through an example of each type of transform.

### Map: Modifying the contents of a tuple
The `Stream.map()` function takes as input a callable object that takes a single tuple as an argument and returns either 0 or 1 tuple.

For example, you have a `source` function that returns a set of four words from the English dictionary. However, you want to create a `Stream` object that contains only the first four letters of each word. You need to use a `map` transform because it can modify the tuple.

To achieve this:

* Define a `Stream` object called `words` that is created by calling a function that generates a list of four words. (For simplicity, specify a `source` function that returns only four words.)
* Define a `map` function called `transform_substring_functions.first_four_letters` that transforms the tuples from the `words` `Stream` into tuples that contain the first four letters from the original tuple.
* Define a `sink` function that uses the `print` function to write the tuples to output.

Include the following code in the `transform_substring.py` file:

~~~~~~
from streamsx.topology.topology import Topology
import streamsx.topology.context

def words_in_dictionary():
   return {"qualify", "quell", "quixotic", "quizzically"}

def first_four_letters(tuple):
   return tuple[:4]

def main():
    topo = Topology("map_substring")
    words = topo.source(words_in_dictionary)
    first_four_letters = words.map(first_four_letters)
    first_four_letters.for_each(print)
    streamsx.topology.context.submit("STANDALONE", topo)

if __name__ == '__main__':
    main()
~~~~~~

#### Sample output
Run the `python3 transform_substring.py` script.

The contents of your output look like this:

~~~~~~
quix
quel
qual
quiz
~~~~~~

As you can see, the `map` transform modifies the tuples. In this instance, the tuples are modified so that each tuple now only includes the first four letters of each word.


### Map: Changing the type of a tuple
In this example, you have a `Stream` object of strings, and each string corresponds to an integer. You want to create a `Stream` object that uses the integers, rather than the strings, so that you can perform mathematical operations on the tuples.

To achieve this:

* Define a `Stream` object called `string_tuples` that is created by calling a function called `int_strings`. The `int_strings` function returns a list of string values that are integer values. (For simplicity, specify a `source` function that returns the following strings: "1", "2", "3", "4'.)
* Define a `map` function called `string_to_int` that map the tuples from the `string_tuples` `Stream` object into Python `int` objects.
* Define a `map` function called `multiply2_add1` that multiples each `int` object by 2 and adds one to the result.
* Define a `sink` function that uses the `print` function to write the tuples to output.

Include the following code in the `transform_type.py` file:

~~~~~~
from streamsx.topology.topology import Topology
import streamsx.topology.context

def int_strings():
   return ["1", "2", "3", "4"]

def string_to_int(tuple):
   return int(tuple)

def multiply2_add1(tuple):
   return (tuple * 2) + 1

def main():
    topo = Topology("map_type")
    string_tuples = topo.source(int_strings)
    int_tuples = string_tuples.map(string_to_int)
    int_tuples.map(multiply2_add1).for_each(print)
    streamsx.topology.context.submit("STANDALONE", topo)

if __name__ == '__main__':
    main()
~~~~~~

#### Sample output
Run the `python3 transform_type.py` script.

The contents of your output look like this:

~~~~~~
3
5
7
9
~~~~~~

**Tip:** You can transform a `Stream` tuple to any Python object if the returned object's class can be serialized by using the pickle module.

Additionally, you aren't restricted to using built-in Python classes, such as string, integer, and float. You can define your own classes and pass objects of those classes as tuples on a `Stream` object.


### Flat_map: Breaking one tuple into multiple tuples
The `flat_map` transform converts each incoming tuple from a `Stream` object into 0 or more tuples.  The `Stream.flat_map()` function takes a single tuple as an argument, and returns an iterable of tuples.

For example, you have a `Stream` object in which each tuple is a line of text. You want to break down each tuple so that each resulting tuple contains only one word. The order of the words from the original tuple is maintained in the resulting `Stream` object.  

* Define a `Stream` object called `lines` that generates lines of text.
* Split the `lines` `Stream` object into individual words by passing the `split` function into the `flat_map` transform.

#### Sample application
To achieve this:

Include the following code in the `multi_transform_lines.py` file:

~~~~~~
from streamsx.topology.topology import Topology
import streamsx.topology.context

def main():
    topo = Topology("flat_map_lines")
    lines = topo.source(["mary had a little lamb", "its fleece was white as snow"])
    words = lines.flat_map(lambda t : t.split())
    words.print()
    streamsx.topology.context.submit("STANDALONE", topo)

if __name__ == '__main__':
    main()
~~~~~~

#### Sample output
Run the `python3 multi_transform_lines.py` script.

The contents of your output look like this:

~~~~~~
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
~~~~~~

As you can see, the `flat_map` transform broke each of the original tuples into the component pieces, in this case, the component words, and maintained the order of the pieces in the resulting tuples.

**Tip:** You can use the `flat_map` transform with any list of Python objects that is serializable with the pickle module. The members of the list can be different classes, such as strings and integers, user-defined classes, or classes provided by a third-party module.

<a id="state"></a>
## Keeping track of state information across tuples
In the previous examples, you used **stateless** functions to manipulate the tuples on a `Stream` object. A stateless function does not keep track of any information about the tuples that have been processed, such as the number of tuples that have been received or the sum of all integers that have been processed.

By keeping track of state information, such as a count or a running total, you can create more useful applications.

A **stateful** function references data that is preserved across calls to the function.

You can define stateful data within the scope of a callable object. The data is local to the function. When the function exits, the data is no longer accessible.

For example, you have a `Stream` object of random numbers and you want to define a function that consumes the `Stream` object and keeps track of the moving average across the last ten tuples. You can define a list in the callable object to keep track of the tuples on the `Stream` object. The state of the list persists across calls to the function.

To achieve this:

Add the following code in the `transform_stateful.py` file:

~~~~~~
from streamsx.topology.topology import Topology
import streamsx.topology.context
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

def main():
    topo = Topology("transform_stateful")
    floats = topo.source(readings)
    avg = floats.map(AvgLastN(10))
    avg.for_each(print)
    streamsx.topology.context.submit("STANDALONE", topo)

if __name__ == '__main__':
    main()
~~~~~~

### Sample output
Run the `python3 transform_stateful.py` script.

The contents of your output file looks something like this:

~~~~~~
...
-0.129801183721193
-0.24261908760937825
-0.31236638019773516
-0.40426366430734334
-0.24643244932349337
-0.28186826075709115
...
~~~~~~

In this example, `AvgLastN.n`, which is initialized from the user-defined parameter n, and `AvgLastN.last_n` are examples of data whose state is kept in between tuples.

**Tip:** Any type of transform (source, filter, map, and sink) can accept callable objects that maintain stateful data.

You can also create a user-defined function that refers to global variables. Unlike variables that are defined within a function, global variables persist in the runtime process. However, this approach is **not recommended** because the way in which the processing elements are fused can change how global variables are shared across functions or callable objects.

For example, in stand-alone mode, there is a single copy of a global variable. This copy is shared by all of the functions that reference it. In distributed mode, multiple copies of a global variable might exist because the topology is distributed across multiple processing elements (processes). If any Python code on a processing element executes a function that references the global variable, the processing element will have its own copy of the global variable.



<a id="split"></a>
<br/>
## Splitting streams
You can split a stream into more than one output stream. By splitting a stream, you can perform different processing on the data depending on an attribute of a tuple. For example, you might want to perform different processing on log file messages depending on whether the message is a warning or an error.

You can split a stream by using any operator. Each time you call a function, such as `filter`, `transform`, or `sink`, the function produces one output stream. If you call a function on the same `Stream` object three times, it creates three output streams.  The tuples from the input stream are distributed to all of the destination streams.

For example, the following code snippet splits the `stream1` `Stream` object into two streams:

~~~~~~
stream2 = stream1.filter(...)
stream3 = stream1.filter(...)
~~~~~~

A visual representation of this code would look something like this:

![Visual representation of splitting a stream](../../../../images/python/stream_split.jpg)

The following example shows how you can distribute tuples from a `source` function to two `sink` functions.  Each `sink` function receives a copy of the tuples from the `source` `Stream` object.

### Sample application
Include the following code in the `split_source.py` file:

~~~~~~
from streamsx.topology.topology import Topology
import streamsx.topology.context

def source_tuples():
    return ["tuple1", "tuple2", "tuple3"]

def print1(tuple):
    print("print1", tuple)

def print2(tuple):
    print("print2", tuple)

def main():
    topo = Topology("split_source")
    source = topo.source(source_tuples)
    source.for_each(print1)
    source.for_each(print2)
    streamsx.topology.context.submit("STANDALONE", topo)

if __name__ == '__main__':
    main()
~~~~~~


### Sample output
Run the `python3 split_source.py` script.

The contents of your output file looks something like this:

~~~~~~
...
print2 tuple1
print1 tuple1
print2 tuple2
print1 tuple2
print2 tuple3
print1 tuple3
~~~~~~

<a id="union"></a>
## Joining streams (union)
You can combine multiple streams into a single `Stream` object by using the `union` transform. The `Stream.union()` function takes a set of streams as an input variable and combines them into a single `Stream` object. However, the order of the tuples in the output `Stream` object is not necessarily the same as in the input streams.

For example, you want to combine the streams from the `source` functions h, b, c, and w. You can combine the streams by using the `union` function and then use the `sink` function to write the resulting `Stream` object to output.

### Sample application
To achieve this:

Include the following code in the `union_source.py` file:

~~~~~~
from streamsx.topology.topology import Topology
import streamsx.topology.context

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

def main():
    topo = Topology("union_source")
    h = topo.source(hello)
    b = topo.source(beautiful)
    c = topo.source(crazy)
    w = topo.source(world)
    hwu = h.union({b, c, w})
    hwu.for_each(print1)
    streamsx.topology.context.submit("STANDALONE", topo)

if __name__ == '__main__':
    main()
~~~~~~

### Sample output
Run the `python3 union_source.py` script.

The contents of your output file looks something like this:

~~~~~~
...
- Hello
- beautiful
- crazy
- World!
~~~~~~

**Remember:** The order of the tuples might be different in your output.

<a id="publish"></a>
## Publishing streams
You can make an output stream available to applications by using the `publish` transform. The `Stream.publish()` function takes the tuples on a stream, converts the tuples to Python objects, JSON objects, or strings, and then publishes the output to a topic. (A topic is based on the MQTT topic specification. For more information, see the [MQTT protocol specification](http://public.dhe.ibm.com/software/dw/webservices/ws-mqtt/mqtt-v3r1.html))

To receive the tuples, an application must subscribe to the topic that you publish by specifying the same topic and schema. For more information, see [Subscribing to streams](#39-subscribing-to-streams).

**Restrictions:** The `publish` transform does not work in STANDALONE mode. Additionally, the application that publishes and the one that subscribes must be running in the same instance of IBM Streams.

For example, you can use the `publish` transform to make tuples from a Python streams-processing application available to an IBM Streams Processing Language (SPL) streams-processing application.

The schema that you specify determines the type of objects that are published:

* `CommonSchema.Python` publishes the tuples on the stream as Python objects.

   This is the default schema.

* `CommonSchema.Json` publishes the tuples on the stream as JSON objects. Each tuple is converted to JSON by using the `json.dumps` function.

   JSON is a common interchange format between all languages that are supported by IBM Streams (SPL, Java, Scala, and Python).

   **Restriction:** Each tuple object on the stream must be able to be converted to JSON. If the objects cannot be converted, an exception is thrown and the application fails.

* `CommonSchema.String` publishes the tuples on the stream as strings. Each tuple is converted to a string by using the `str()` function.

   String is a common interchange format between all languages that are supported by IBM Streams (SPL, Java, Scala, and Python).

For more information about topics, see [namespace:com.ibm.streamsx.topology.topic].
<!--- pl  TBD? --->


### Sample code
The `Stream.publish()` function takes as input the name of the topic that you want to publish the tuples to and the schema to publish. The function returns `None`.

For example, you want to publish a stream of integers as JSON objects with the topic called `simple` so that another application in your instance can use the data.

To achieve this:

Include the following lines in the `publish.py` file:

~~~~~
from streamsx.topology.topology import *
from streamsx.topology.schema import *
import streamsx.topology.context
import itertools
import time

def sequence():
   return itertools.count()

def delay(v):
   time.sleep(0.1)
   return True

def main():
   topo = Topology("PublishSimple")
   ts = topo.source(sequence)
   ts = ts.filter(delay)
   ts.publish('simple', CommonSchema.Json)
   ts.print()
   streamsx.topology.context.submit('DISTRIBUTED', topo)

if __name__ == '__main__':
   main()
~~~~~


This example is based on the `pubsub` sample in GitHub. For more information about how this application works, see [https://github.com/IBMStreams/streamsx.topology/tree/master/samples/python/topology/pubsub](https://github.com/IBMStreams/streamsx.topology/tree/master/samples/python/topology/pubsub)


## Subscribing to streams
If an application publishes a stream to a topic, you can use the `subscribe` transform to pull that data into your application.

**Remember:** The `subscribe` transform must be running in the same instance of IBM Streams as the application that is publishing data.

To subscribe to a topic, use the `Topology.subscribe` function, specifying the same topic and schema as the corresponding `Topology.publish` function. The application that published the topic can be written in any language that IBM Streams supports.

The schema determines the type of objects that the application receives:

* `CommonSchema.Python` receives tuples that have been published as Python objects.

   This is the default schema.

* `CommonSchema.Json` receives tuples that have been published as JSON objects. Each tuple on the stream is converted to a Python dictionary object by using the `json.loads(tuple)` function.

* `CommonSchema.String` receives tuples that have been published as strings. Each tuple on the stream is converted to a Python string object.

You can also subscribe to topics that use an SPL schema. (Most applications that publish a topic with an SPL schema are SPL applications. However, Java and Scala applications can also publish streams with an SPL schema.)

When you use the `Topology.subscribe()` function for a topic with an SPL schema in a Python application, the tuple attributes from the topic are converted to the appropriate Python type and added to a Python dictionary object. (The name of the attribute is used as the dictionary key value.)

The syntax that you use to subscribe to an SPL schema is `schema.StreamSchema(“tuple<attribute_type attribute_name, ...>”)`. The schema must exactly match the schema that is specified by the corresponding `publish` transform. For example:

* A simple schema might be `schema.StreamSchema(“tuple<ustring ustr1>”)`
* A more complex schema might be `schema.StreamSchema(tuple“<rstring rs1, uint32 u321, list<uint32> liu321, set<uint32> setu321>")`

Python supports the following SPL attribute types:

| SPL attribute type | Resulting Python type | Notes |
| --- | --- | --- |
| int8, int16, int36, or int64 | int |   |
| uint8, uint16, uint36, or uint64 | int | The uint64 type can't be published to JSON if the value is bigger than Long.MAX_VALUE. |
| float32 or float64 | float |   |
| complex32 or complex64 | complex | The complex32 and complex64 types can't be published to JSON. |
| rstring | str |   |
| ustring |str |   |
| boolean | boolean |   |
| list | list |   |
| map | dictionary |   |
| set | set | The set type can't be published to JSON. |


For more information about topics, see [namespace:com.ibm.streamsx.topology.topic].
<!--- pl TBD? --->

### Sample code
The `Topology.subscribe()` function takes as input the name of the topic that you want to subscribe to and the schema describing the stream. The function returns a `Stream` object whose tuples have been published to the topic by an IBM Streams application.

For example, you want to subscribe to the stream that you published in [Publishing streams](#38-publishing-streams).

To achieve this, include the following lines in the `subscribe.py` file:

~~~~~
from streamsx.topology.topology import *
import streamsx.topology.context

def main():
   topo = Topology("SubscribeSimple")
   ts = topo.subscribe('simple', schema.CommonSchema.Json)
   ts.print()
   streamsx.topology.context.submit("DISTRIBUTED", topo)

if __name__ == '__main__':
   main()
~~~~~


### Sample output
Run the `python3 subscribe.py` script.

The contents of your output file look something like this:
~~~~~
...
12390
12391
12392
12393
12394
12395
...
~~~~~
