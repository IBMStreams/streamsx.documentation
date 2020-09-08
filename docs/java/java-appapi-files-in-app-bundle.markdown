---
layout: docs
title:   Working with external files, JARs and other resources in the Java Application API
description: Using external resources such as files and archives with the Java API
weight: 3
published: true
tag: java-app
next:
    file: java-appapi-setting-parameters
    title: Setting parameter values when invoking operators
prev:
    file: java-appapi-devguide
    title: Java Application development
---


At times, it is necessary to use configuration or static files in your application. For example, if your application reads configuration data from a file, you want that file available at runtime on all the hosts where the application runs. One way to do this is to include the file in the application bundle.

## What is the application bundle?

When you compile a  Streams application, that application is compiled into a file called the **application bundle file**. This is true regardless of the language the application was is written in.  The application bundle file contains all IBM Streams artifacts that are required to execute an application. The application bundle has a `.sab` extension and so is sometimes also called a "sab" file.


The Java Application API provides 3 methods for adding external resources to the application bundle:
 * [Topology.addClassDependency(Class class)](https://ibmstreams.github.io/streamsx.topology/doc/javadoc/com/ibm/streamsx/topology/Topology.html#addClassDependency)
 * [Topology.addFileDependency(String location, String dstDirName)](https://ibmstreams.github.io/streamsx.topology/doc/javadoc/com/ibm/streamsx/topology/Topology.html#addFileDependency) 
 * [Topology.addJarDependency(String location)](https://ibmstreams.github.io/streamsx.topology/doc/javadoc/com/ibm/streamsx/topology/Topology.html#addJarDependency) 
  
For this blog post, I am going to focus on the last 2 methods: `addFileDependency()` and `addJarDependency()`.

## Adding File Dependencies

There are many operators in the available toolkits that can require a configuration file to be present in the application bundle. For example, when using the HDFS operators from the com.ibm.streamsx.hdfs toolkit, you may want to include a credentials file as part of the application bundle to allow the operators to perform authentication. In this case, you would use the `addFileDependency()` method to ensure the file gets added to the application bundle. 

Using the `addFileDependency()` method does come with some restrictions. First, any files added using this method can only be added to the **etc/** or **opt/** directories within the application bundle. Therefore, you must ensure that the operator parameters are looking in the correct directory when accessing the files. 

Second, adding files to the application bundle using this method are not accessible when using the functional logic. In other words, you would not be able to implement a **com.ibm.streamsx.topology.function.Supplier** that can access files stored in the application bundle. In order to access these files directly, you would need create a proper Java Primitive Operator. To access files stored in the application bundle using the functional logic, the `addJarDependency()` method must be used.

## Adding JAR Dependencies

As mentioned in the previous section, it is not possible to access files stored in the application bundle from functional logic. Any files that need to be accessed from the functional logic should be packaged into a JAR file. The JAR file can then be added to the classpath using the `addJarDependency()` method. Using this method, any functional logic can quickly access the files by accessing the **ClassLoader** and calling one of the `getResource*()` methods available.


The following example demonstrates how to create a simple topology application that reads words from a file and prints them to the console. The file 'words.txt' is packaged into a JAR file called 'words.jar'. The JAR file is added to the application classpath using the `addJarDependency()` method (if you are running in Embedded mode, see the "Running Embedded" section below). The source for this sample [can be found here](https://github.com/cancilla/streamsdev/tree/master/FileDepSample).

~~~~ java
    public class Main {

        public static void main(String[] args) throws Exception {

            Topology t = new Topology("FileDepSample");
            t.addJarDependency("./words.jar");
            TStream<String> srcStream = t.source(new FileReader("words.txt"));
            srcStream.print();

            StreamsContextFactory.getStreamsContext(Type.STANDALONE).submit(t).get();
        }
    }

    public class FileReader implements Supplier<Iterable<String>>, Iterable<String>, Iterator<String> {
        private static final long serialVersionUID = 1L;

        private String filename;
        private transient BufferedReader reader;
        private transient String nextLine;

        public FileReader(String filename) {
            this.filename = filename;
        }

        private Object readResolve() throws Exception {
            // read the file contents
            ClassLoader cl = this.getClass().getClassLoader();
            InputStream is = cl.getResourceAsStream(this.filename);
            if(is == null)
                throw new FileNotFoundException("Unable to find '" + filename + "' in any loaded libraries.");

            reader = new BufferedReader(new InputStreamReader(is));
            return this;

        }

        @Override
        public boolean hasNext() {
            try {
                return ((nextLine = reader.readLine()) != null);
            } catch (IOException e) {
                e.printStackTrace();
            }
            return false;
        }

        @Override
        public String next() {
            return nextLine;
        }

        @Override
        public Iterator<String> iterator() {
            return this;
        }

        @Override
        public Iterable<String> get() {
            return this;
        }
    }
~~~~


The important stuff happens inside the `readResolve()` method. First, the **ClassLoader** is accessed so that we can get at the JARs that were added to the classpath.

    ClassLoader cl = this.getClass().getClassLoader();

Next, we retrieve the **InputStream** for the file. The **ClassLoader** takes care of figuring out which JAR file contains the 'words.txt'. If the file cannot be found in any of the JARs, then **InputStream** will be `null`.

~~~~ java
    InputStream is = cl.getResourceAsStream(this.filename);
    if(is == null)
      throw new FileNotFoundException("Unable to find '" + filename + "' in any loaded libraries.");
~~~~

Finally, we create a **BufferedReader** to iterate over each line in the file. Depending on the type of file you are reading, you may need to use a different mechanism to access the contents of the file.

    reader = new BufferedReader(new InputStreamReader(is));

The `next()` and `hasNext()` methods are used to retrieve and return the lines in the file.

## Running Embedded

When running in embedded mode, it is not enough to add the JAR file using the `addJarDependency()` method. You must also add the JAR file to the classpath of the project. Otherwise, the 'words.jar' files file will not be found. For Standalone and Distributed modes, you only need to add the JAR file using the `addJarDependency()` method.