---
layout: samples
title: 033_java_primitive_operator_at_work
---

### 033_java_primitive_operator_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/032_native_function_at_work_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/034_odbc_adapters_for_db2_at_work_my_sample_Main_spl/"> > </a>
</div>

~~~~~~
/*
This example shows how a Java primitive operator is created from scratch.
Java primitive operator is different from JavaOp that you have seen earlier
in a different example. Java primitive operator is a first class operator in
SPL, whereas JavaOp only permits a callout to another Java operator.
On the other hand, Java primitive operator's name becomes the operator instance name.
[THIS EXAMPLE HAS A COMPANION JAVA PROJECT NAMED RSS_Reader_Primitive.]
*/
namespace my.sample;
/*
Some Tips:

1) You can open the Java Operator model file in the com.ibm.streams.rss.header
subdirectory located in the main directory of this application and browse that
file using the operator model editor. It will show you how this Java primitve
operator is configured.

2) You have to build the companion Java project RSS_Reader_Primitive by
switching to the Eclipse Java perspective. The Java source for the business logic 
code can be found in that Java project. Once that Java Project is built,
copy the RSSReader.class in this SPL project's impl/java/bin directory with its
full Java package name (i.e. impl/java/bin/com/ibm/streams/rss/reader/RSSReader.class)
For consistency, it is recommended that you also copy the Java source file here:
(impl/java/src/com/ibm/streams/rss/reader/RSSReader.java). The Java source file
is copied here just for the sake of completion and as noted earlier, 
that Java source file can't be compiled inside the SPL project directory.

This example shows a way of having the Java project outside of the Streams application
directory and then just copy only the Java class files from that external Java project.

Streams also allows you to have the entire Java operator code inside of the impl/java.src
directory. There are numerous other examples in this collection that will show you how to
do that.
*/
// Include the Java primitive operator model namespace here.
use com.ibm.streams.rss.reader::*;

composite Main {
	type
		rssReaderInput = tuple<ustring rssProviderName, ustring rssProviderURL, int32 maxRssItemsToBeReturned>;
		rssReaderOutput = tuple<ustring rssProviderName, ustring rssProviderURL, int32 maxRssItemsToBeReturned, boolean rssEntriesReturned, set <ustring> rssResults>;
		
	graph
		stream <rssReaderInput> RSSReaderInput = FileSource() {
			param
				file: "rss_feed_sources.txt";
				format: csv;
				hasDelayField: true;
				initDelay: 4.0f;
		} // End of RSSReaderInput = FileSource()
		
		// Invoke the Java primitive operator by using its own name.
		stream <rssReaderOutput> RSSReaderOutput = RSSReader(RSSReaderInput) {
		} // End of RSSReaderOutput = RSSReader(RSSReaderInput)
		
		() as RssResults = FileSink(RSSReaderOutput) {
			param
				file: "rss-output.txt";
				format: csv;
				hasDelayField: false;
		} // End of RssResults = FileSink(RSSReaderOutput)
		
} // End of composite Main

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/032_native_function_at_work_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/034_odbc_adapters_for_db2_at_work_my_sample_Main_spl/"> > </a>
</div>

