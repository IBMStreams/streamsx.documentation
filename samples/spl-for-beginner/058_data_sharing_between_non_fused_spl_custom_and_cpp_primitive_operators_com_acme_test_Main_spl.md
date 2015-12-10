---
layout: samples
title: 058_data_sharing_between_non_fused_spl_custom_and_cpp_primitive_operators
---

### 058_data_sharing_between_non_fused_spl_custom_and_cpp_primitive_operators

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/057_reading_nested_tuple_data_via_file_source_com_acme_test_Test1_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/059_dynamic_scaleout_of_streams_application_com_ibm_streams_pricing_Pricer_spl/"> > </a>
</div>

~~~~~~
/*
================================================================================
With the Distributed Process Store (dps) features, it is now possible to share
data between any of the SPL standard toolkit (built-in) operators and
the user created C++ primitive operators that are NOT fused together.
This example shows how to call the Distributed Process Store (dps)
native function APIs from both within the built-in as well as the
C++ primitive operators.

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
		// C++ primitive operators.
		//
		// We are going to have this simple flow.
		// Thing1 (Custom) --> Thing2 (C++ Primitive) --> DisplaySink (Custom).
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
					// subset to a C++ primitive operator
					list<rstring> myStockPicks = ["IBM", "T", "GOOG", "BA"];
					// Create an output tuple containing your personal stock picks.
					ticker_symbols oTuple = {tickers = myStockPicks}; 
					submit(oTuple, Thing1);
				}				
		}
		
		// Within this current SPL project and inside the same namespace of this SPL file, we have created a 
		// C++ primitive operator called TickerIdGenerator. Let us invoke that primitive operator.
		// 
		// [Please refer to the TickerIdGenerator_h.cgt file for tips about calling the dps
		//  native function APIs within the C++ primitive operator. At the top of that file, all the required
		//  steps are explained clearly.]
		//
		// This primitive operator will pull out the "ticker symbol and the company name" from Thing1_Store only for
		// the ticker symbols sent in the stock picks list as an input tuple attribute.
		// Then, it will create a unique ticker id for every ticker specified in that stock picks list and insert 
		// "ticker symbol => unique ticker id" in a new store called "Thing2_Store".
		stream<dummy_signal> Thing2 = TickerIdGenerator(Thing1) {
		}
		
		// In the following sink operator, we should be able to access both the distributed process stores.
		// i.e. Thing1_Store created inside of the SPL built-in Custom operator above and 
		// Thing2_Store created within the C++ primitive operator.
		// If we can see the correct results from those two stores, then we proved that
		// dps APIs can be accessed both within the SPL built-in as well as the
		// C++ primitive operators.
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

					while(dpsGetNext(t1s, it, key, value, err))  
						printStringLn("'"+key+"' => '"+(rstring)value+"'");                            

					dpsEndIteration(t1s, it, err);
					
					printStringLn("\n\nContents of the Thing2_Store [TickerSymbol => UniqueTickerId]");

					// Iterate the Thing2 store.
					it = dpsBeginIteration(t2s, err);
			
					if (it == 0ul) {
						printStringLn("Unable to get an iterator for the Thing2_Store");
						abort();
					}
	
					mutable uint64 value2 = 0ul;
					while(dpsGetNext(t2s, it, key, value2, err))  
						printStringLn("'"+key+"' => '"+(rstring)value2+"'");                            

					dpsEndIteration(t2s, it, err);			
					
					// So far so good. Let us now remove both the distributed process stores.
					dpsRemoveStore(t1s, err);
					dpsRemoveStore(t2s, err);
					printStringLn("================ Final Results End   ================"); 
				}
		}		
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/057_reading_nested_tuple_data_via_file_source_com_acme_test_Test1_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/059_dynamic_scaleout_of_streams_application_com_ibm_streams_pricing_Pricer_spl/"> > </a>
</div>

