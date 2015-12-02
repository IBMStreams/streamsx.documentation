---
layout: samples
title: 062_data_sharing_between_non_fused_spl_custom_and_java_primitive_operators
---

### 062_data_sharing_between_non_fused_spl_custom_and_java_primitive_operators

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/061_data_sharing_between_non_fused_spl_custom_operators_and_a_native_function_com_acme_test_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/063_on_the_fly_tuple_creation_and_encoding_decoding_in_java_primitive_operators_application_Main_spl/"> > </a>
</div>

~~~~~~
/*
================================================================================
With the Distributed Process Store (dps) features, it is now possible to share
data between any of the SPL standard toolkit (built-in) operators and
the user created Java primitive operators that are NOT fused together.
This example shows how to call the Distributed Process Store (dps)
native function APIs from both within the built-in as well as the
Java primitive operators.

In this SPL project, we added a dependency to the Distributed Process Store (dps)
toolkit, which is already a part of this SPL-Examples-For-Beginners
workspace. You can locate the distributed process store (dps) toolkit in this
workspace by looking for a project named "com.ibm.streamsx.dps".

If you are not already familiar with the Distributed Process Store (dps) APIs,
please go to the com.ibm.streamsx.dps toolkit project and read the
following two files to get a good grasp about what the dps does.
It is highly recommended that you study and run the test application included 
in the dps toolkit to get a first hand experience on how to work with the dps APIs.

1) A quick high-level read about using the dps:
   com.ibm.streamsx.dps/doc/dps-usage-tips.txt

2) A test application that exercises all the dps APIs:
   com.ibm.streamsx.dps/samples/dps_test_1/DpsTest1.splmm

If you are already familiar with (1) and (2) above, please proceed
to work with the following code.

IMPORTANT
--------- 
Before doing anything with this example, you have to do one
important thing. You must first configure the name of your back-end 
NoSQL DB store and the name(s) of your one or more back-end server(s).
Please take a look inside the ../etc/no-sql-kv-store-servers.cfg file and
ensure that everything is in order as required. 

ANOTHER IMPORTANT THING
-----------------------
Here, we are going to deal with a Java primitive operator that will invoke C++ dps functions via JNI.
(In fact, we are going to show you how to invoke the dps functions from two different Java operators that
 are fused together in a single PE. Read the comments available above the invocations of those 
 Java operators in this SPL file and the additional comments inside those Java operators to learn more.)
In order to do that, we have to import the DpsHelper java package. This helper package is part of 
the dps toolkit (com.ibm.streamsx.dps/impl/java/bin/dps-helper.jar). When we created this SPL project,
we added that jar file to the java build path of this 062_XXXX SPL project. We specifically did that
inside the properties of this 062_XXXXX SPL project.

1) You have to import the dpsHelper package as done below. This helper package is part of 
   the dps toolkit (com.ibm.streamsx.dps/impl/java/bin/dps-helper.jar). This jar file contains the
   Java dps APIs that the Java primitive operator developers will use. We added that jar file
   to the java build path of the 062_XXXX SPL project. We specifically did that inside the 
   properties of this 062_XXXXX SPL project.
   
   a) In Streams Studio 3.2 and later versions, this jar file gets deleted while importing the dps toolkit (No idea, why it does that).
      Let us rebuild the jar file now.
      i)   Open a Linux terminal window.
      ii   Inside your SPL-Examples-For-Beginners directory, change to the following sub-directory:
           com.ibm.streamsx.dps/impl/java/src/com/ibm/streamsx/dps/impl
      iii) Now, run this build script:   ./build_dps_helper.sh 
      
      iv)  Change focus to the Streams Studio.
      
   b) You can right click at the top-level 062_XXXXXX project name and select "Properties". In the resulting
   dialog, select "Java Build Path" in the left pane. Now, on the right pane, select the "Libraries" tab.
   There, you will see the dps-helper.jar file. If that full path is at a different location on your machine,
   you should remove that existing entry and "Add an External Jar" by navigating to your specific
   com.ibm.streamsx.dps/impl/java/bin directory.

   In addition, you must also do the following:

   This Java primitive operator class is extended from a Streams AbstractOperator and
   in addition it uses a lot of other Streams Java artifacts such as the Tuple class. In order to
   resolve those Streams Java classes and compile it correctly, you have to do the following.
 
      i)   Ensure you are in the Eclipse Java perspective.
      ii)  Right click on the 062_XXXXX project and select Properties.
      iii) In the left pane of the resulting dialog, click on "Java Build Path".
      iv)  In the right pane, click on the tab titled "Libraries".
      v)   Click the "Add External Jars" button, add the following Streams jar files from your
           Streams installation directory.
       
           <Your Streams Install Directory>/lib/com.ibm.streams.operator.jar
           <Your Streams Install Directory>/lib/com.ibm.streams.operator.samples.jar
                
   c) After adding these two dependent jar files, you may delete/remove the three
      erroneous jar entries in your "Libraries" tab that point to invalid directories.
      
   d) Now, right-click on the 062_XXXXX project and select "Build Active Configurations".
 
CAUTION
-------
If you are planning to run the Java primitive operator in this example with a memcached back-end server,
you should be aware of the fact that memcached puts a limit on the length of the key.
Test case 23 in the Java operator will attempt to store a key:value pair with a key length exceeding that
allowed limit (240 characters). You will get an exception for test case 23 while running this
example with memcached. Other than that exception no other harm is done. Rest of the application
will run just fine. 

You can happily run all the test cases in this Java primitive operator with a redis server.
Because, redis doesn't have such a limitation. It allows keys with a size of few megabytes.
================================================================================  
*/
namespace com.acme.test;

// Declare the use of the two namespaces containing the distributed process store native functions.
// You are also encouraged to refer to the native function model XML files available inside
// the com.ibm.streamsx directory of the dps toolkit project.
use com.ibm.streamsx.store.distributed::*;
use com.ibm.streamsx.lock.distributed::*;

composite Main {
	type
		dummy_signal = tuple<int32 dummy>;
		ticker_symbols = tuple<list<rstring> tickers>;
	
	// All the operators in this composite graph are non-fused.
	// Hence, each operator will be running as individual PEs (Processing Elements) so that
	// we can verify whether the dps functions will work correctly across different PEs.	
	graph
		// Let us kick-start our ride into the world of the distributed process store (dps).
		stream<dummy_signal> StartSignal = Beacon() {
			param
				iterations: 1u;
				initDelay: 5.0;
		} 
		
		// In this example application, there is no earth-shattering business logic.
		// Main goal here is to see how one can access the distributed process store functions
		// inside of both the normal SPL built-in operators as well as the user defined
		// Java primitive operators.
		//
		// We are going to have this simple flow.
		// Thing1 (Custom) --> Thing2 (Java Primitive) --> DisplaySink (Custom).
		//
		// In this Custom operator, we will create a new distributed process store and 
		// populate that store with a few data items.
		stream<ticker_symbols> Thing1 = Custom(StartSignal) {
			logic
				onTuple StartSignal: {
					// Create a new named store that can be accessed by any other operator
					// that is not fused with this Thing1 operator.
					mutable uint64 err = 0ul;
					// It is required to indicate what SPL type will make up the key and value of this store.
					// Simply pass a dummy key and dummy value so that their SPL types will be automatically inferred during the creation of that store.
					// Important note: After creating a store this way, there will not be any check done during the future put operations to validate whether you are
					// using the correct data types indicated at the time of store creation via dummy key and dummy value. It is better to have all the
					// entries to have uniform key:value data types in order for that store to be practically useful. So, a simple advice is don't use
					// the put call with different data types for keys and values of any given store. If you do that, then you are on your own and
					// as a result you are making that store not very useful. It is left to the dps user to follow a disciplined approach for
					// maintaining content uniformity within a store. So, create a store with the required key and value types and simply stick to that
					// key:value pair data type for the full life of that store.
					rstring dummyRstring = "";
					uint64 t1s = dpsCreateOrGetStore("Thing1_Store", dummyRstring, dummyRstring, err);
					
					if (t1s == 0ul) {
						printStringLn("Error while creating the Thing1 store.");
						abort();
					}
					
					// Let us add a few entries into the Thing1 distributed process store.
					// "ticker symbol => company name"
					dpsPut(t1s, "IBM", "IBM Corporation", err);
					dpsPut(t1s, "F", "Ford Motor Company", err);
					dpsPut(t1s, "BA", "The Boeing Company", err);
					dpsPut(t1s, "T", "AT&T Inc.", err);
					dpsPut(t1s, "CSCO", "Cisco Systems, Inc.", err);
					dpsPut(t1s, "GOOG", "Google Inc.", err);
					dpsPut(t1s, "INTC", "Intel Corporation", err);
					
					// Now we are going to pick a subset of the tickers we added, and send that
					// subset to a Java primitive operator
					list<rstring> myStockPicks = ["IBM", "T", "GOOG", "BA"];
					// Create an output tuple containing your personal stock picks.
					ticker_symbols oTuple = {tickers = myStockPicks}; 
					submit(oTuple, Thing1);
				}				
		}
		
		// Within this current SPL project and inside the same namespace of this SPL file, we have created a 
		// Java primitive operator called TickerIdGenerator. Let us invoke that primitive operator.
		// 
		// [Please refer to the impl/java/src/com/acme/test/TickerIdGenerator.java file in this project.
		//  That file contains tips about calling the dps native function APIs within the 
		//  Java primitive operator. At the top of that file, all the required steps are explained clearly.]
		//  
		// This primitive operator will pull out the "ticker symbol and the company name" from Thing1_Store only for
		// the ticker symbols sent in the stock picks list as an input tuple attribute.
		// Then, it will create a unique ticker id for every ticker specified in that stock picks list and insert 
		// "ticker symbol => unique ticker id" in a new store called "Thing2_Store".
		stream<dummy_signal> Thing2 = TickerIdGenerator(Thing1) {
			config
				placement: partitionColocation("JavaOpFusion");
		}
		
		
		// We are going to fuse this operator with the JavaOperator specified above.
		// This will demonstrate how two Java operators fused into a single PE can
		// keep using the DPS APIs. This is done using the @SharedLoader annotation inside
		// those Java operators. Please read the useful comments specified inside of those
		// two Java operators.
		stream<rstring dpsTesterName> Thing2A = com.ibm.acme.test::DataStoreTester(Thing1) {
			config
				placement: partitionColocation("JavaOpFusion");		
		}

		() as Thing2ASink = FileSink(Thing2A) {
			param
				file: "/dev/stdout";
				flush: 1u;
		}
		
		// In the following sink operator, we should be able to access both the distributed process stores.
		// i.e. Thing1_Store created inside of the SPL built-in Custom operator above and 
		// Thing2_Store created within the Java primitive operator.
		// If we can see the correct results from those two stores, then we proved that
		// dps APIs can be accessed both within the SPL built-in as well as the
		// Java primitive operators.
		() as ScreenWriter1 = Custom(Thing2) {
			logic
				onTuple Thing2: {
					// This dps API will return the NoSQL KV store product name that is configured by   
					// the user within the SPL project directory's etc/no-sql-kv-store-servers.cfg file.
                    rstring dbProductName = dpsGetNoSqlDbProductName();
                    // Get the details about the machine where this operator is running.
                    mutable rstring machineName = "", osVersion = "", cpuArchitecture = "";
                    dpsGetDetailsAboutThisMachine(machineName, osVersion, cpuArchitecture);
                    // Display the NoSQL DB product name being used for this test run.
                    printStringLn("=====================================================");
                    printStringLn("Details about this DPS client machine:");
                    printStringLn("NoSQL K/V store product name: " + dbProductName);
                    printStringLn("Machine name: " + machineName);
                    printStringLn("OS version: " + osVersion);
                    printStringLn("CPU architecture: " + cpuArchitecture);
                    printStringLn("=====================================================");
                    
					mutable uint64 err = 0ul;
					mutable uint64 t1s = dpsFindStore("Thing1_Store", err);
	
					if (t1s == 0ul) {
						printStringLn("Unable to find the Thing1_Store inside the screen writer sink.");
						abort();
					}
					
					mutable uint64 t2s = dpsFindStore("Thing2_Store", err);
					
					if (t2s == 0ul) {
						printStringLn("Unable to find the Thing2_Store inside the screen writer sink.");
						abort();
					}					

					// Since we found the store successfully, let us get the original name of that store,
					// spl type name of that store's key, and spl type name of that store's value.
					// These three values are tagged as part of every store's metadata information.
					printStringLn("Metadata 1: Original name of a store with an id " + (rstring)t2s + " is '" +  dpsGetStoreName(t2s) + "'");
					printStringLn("Metadata 2: SPL type name for the key of a store with an id " + (rstring)t2s + " is '" +  dpsGetSplTypeNameForKey(t2s) + "'");
					printStringLn("Metadata 3: SPL type name for the value of a store with an id " + (rstring)t2s + " is '" +  dpsGetSplTypeNameForValue(t2s) + "'");
					
					printStringLn("================ Final Results Begin ================");
					printStringLn("Thing2.dummy = " + (rstring)Thing2.dummy);
					printStringLn("\n\nContents of the Thing1_Store [TickerSymbol => CompanyName]");

					// Iterate the Thing1 store.
					mutable uint64 it = dpsBeginIteration(t1s, err);
					mutable rstring key = "";
					mutable rstring value = "";
			
					if (it == 0ul) {
						printStringLn("Unable to get an iterator for the Thing1_Store");
						abort();
					}

					while(dpsGetNext(t1s, it, key, value, err)) {
						printStringLn("'"+key+"' => '"+(rstring)value+"'");
					}                            

					dpsEndIteration(t1s, it, err);
					
					printStringLn("\n\nContents of the Thing2_Store [TickerSymbol => UniqueTickerId]");

					// Iterate the Thing2 store.
					it = dpsBeginIteration(t2s, err);
			
					if (it == 0ul) {
						printStringLn("Unable to get an iterator for the Thing2_Store");
						abort();
					}
	
					mutable uint64 value2 = 0ul;
					while(dpsGetNext(t2s, it, key, value2, err)) {  
						printStringLn("'"+key+"' => '"+(rstring)value2+"'");                            
					}
					
					dpsEndIteration(t2s, it, err);			
					
					// So far so good. Let us now remove both the distributed process stores.
					dpsRemoveStore(t1s, err);
					dpsRemoveStore(t2s, err);
					
					// Inside the Java operator, a store has been left active with a nested array typed
					// key and value. Let us fetch that value, verify, and then remove that store in this operator.
					uint64 mnts = dpsFindStore("My New Test Store", err);

					if (mnts == 0ul) {
						printStringLn("Unable to find the 'My New Test Store' inside the screen writer sink.");
						abort();
					}

					printStringLn("");
					printStringLn("Metadata 1: Original name of a store with an id " + (rstring)mnts + " is '" +  dpsGetStoreName(mnts) + "'");
					printStringLn("Metadata 2: SPL type name for the key of a store with an id " + (rstring)mnts + " is '" +  dpsGetSplTypeNameForKey(mnts) + "'");
					printStringLn("Metadata 3: SPL type name for the value of a store with an id " + (rstring)mnts + " is '" +  dpsGetSplTypeNameForValue(mnts) + "'");
										
					// Let us get the nested array value.
					mutable list<list<int32>> k = [];
					mutable list<list<int32>> v = [];
					// Iterate the "My New Test Store".
					it = dpsBeginIteration(mnts, err);
			
					if (it == 0ul) {
						printStringLn("Unable to get an iterator for the 'My New Test Store'");
						abort();
					}

					printStringLn("Result from reading a nested array from the 'My New Test Store':");

					while(dpsGetNext(mnts, it, k, v, err)) {
						printStringLn("'"+(rstring)k+"' => '"+(rstring)v+"'");
					}                            

					dpsEndIteration(mnts, it, err);					
					// Remove the store.
					dpsRemoveStore(mnts, err);
					printStringLn("================ Final Results End   ================"); 
				}
		}
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/061_data_sharing_between_non_fused_spl_custom_operators_and_a_native_function_com_acme_test_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/063_on_the_fly_tuple_creation_and_encoding_decoding_in_java_primitive_operators_application_Main_spl/"> > </a>
</div>

