---
layout: samples
title: 056_data_sharing_between_fused_spl_custom_and_cpp_primitive_operators
---

### 056_data_sharing_between_fused_spl_custom_and_cpp_primitive_operators

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/055_json_to_tuple_to_json_using_c++_com_acme_test_json_to_tuple_to_json_using_cpp_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/057_reading_nested_tuple_data_via_file_source_com_acme_test_Test1_spl/"> > </a>
</div>

~~~~~~
/*
======================================================================
With the Process Store (ps) features, it is now possible to share
data between any of the SPL standard toolkit (built-in) operators and
the user created C++ primitive operators that are fused together.
This example shows how to call the Process Store (ps)
native function APIs from both within the built-in as well as the
C++ primitive operators.

In this SPL project, we added a dependency to the Process Store (ps)
toolkit, which is already a part of this SPL-Examples-For-Beginners
workspace. You can locate the process store (ps) toolkit in this
workspace by looking for a project named "com.ibm.streamsx.ps".

If you are not already familiar with the Process Store (ps) APIs,
please go to the com.ibm.streamsx.ps toolkit project and read the
following two files to get a good grasp about what the ps does.
It is highly recommended that you run the test application included 
in the ps toolkit to get a first hand experience on how to work
with the ps APIs.

1) A quick high-level read about using the ps:
   com.ibm.streamsx.ps/doc/ps-usage-tips.txt

2) A test application that exercises all the ps APIs:
   com.ibm.streamsx.ps/samples/ps_test_1/PsTest1.spl

If you are already familiar with (1) and (2) above, please proceed
to work with the following code.
======================================================================  
*/
namespace com.acme.test;

// Declare the use of the two namespaces containing the process store native functions.
// You are also encouraged to refer to the native function model XML files available inside
// the com.ibm.streamsx directory of the ps toolkit project.
use com.ibm.streamsx.process.store::*;
use com.ibm.streamsx.process.lock::*;

composite Main {
	type
		dummy_signal = tuple<int32 dummy>;
		ticker_symbols = tuple<list<rstring> tickers>;

	// All the operators in this composite graph are fused.
	// Hence, all the operators here will be running inside a single PE (Processing Elements) so that
	// we can verify whether the ps functions will work correctly across different fused operators.		
	graph
		// Let us kick-start our ride into the world of the process store (ps).
		stream<dummy_signal> StartSignal = Beacon() {
			param
				iterations: 1u;
		} 
		
		// In this example application, there is no earth-shattering business logic.
		// Main goal here is to see how one can access the process store functions
		// inside of both the normal SPL built-in operators as well as the user defined
		// C++ primitive operators.
		//
		// We are going to have this simple flow.
		// Thing1 (Custom) --> Thing2 (C++ Primitive) --> DisplaySink (Custom). [All FUSED into a single PE]
		//
		// In this Custom operator, we will create a new process store and 
		// populate that store with a few data items.
		stream<ticker_symbols> Thing1 = Custom(StartSignal) {
			logic
				onTuple StartSignal: {
					// Create a new named store that can be accessed by any other operator
					// that is fused with this Thing1 operator.
					uint64 t1s = psCreateOrGetStore("Thing1_Store", false);
					
					if (t1s == 0ul) {
						printStringLn("Error while creating the Thing1 store.");
						abort();
					}
					
					// Let us add a few entries into the Thing1 process store.
					// "ticker symbol => company name"
					psPut(t1s, "IBM", "IBM Corporation");
					psPut(t1s, "F", "Ford Motor Company");
					psPut(t1s, "BA", "The Boeing Company");
					psPut(t1s, "T", "AT&T Inc.");
					psPut(t1s, "CSCO", "Cisco Systems, Inc.");
					psPut(t1s, "GOOG", "Google Inc.");
					psPut(t1s, "INTC", "Intel Corporation");
					
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
		// [Please refer to the TickerIdGenerator_h.cgt file for tips about calling the process store
		//  native function APIs within the C++ primitive operator. At the top of that file, all the required
		//  steps are explained clearly.]
		//
		// This primitive operator will pull out the "ticker symbol and the company name" from Thing1_Store only for
		// the ticker symbols sent in the stock picks list as an input tuple attribute.
		// Then, it will create a unique ticker id for every ticker specified in that stock picks list and insert 
		// "ticker symbol => unique ticker id" in a new store called "Thing2_Store".
		stream<dummy_signal> Thing2 = TickerIdGenerator(Thing1) {
		}
		
		// In the following sink operator, we should be able to access both the process stores.
		// i.e. Thing1_Store created inside of the SPL built-in Custom operator above and 
		// Thing2_Store created within the C++ primitive operator.
		// If we can see the correct results from those two stores, then we proved that
		// process store APIs can be accessed both within the SPL built-in as well as the
		// C++ primitive operators.
		() as ScreenWriter1 = Custom(Thing2) {
			logic
				onTuple Thing2: {
					mutable uint64 t1s = psFindStore("Thing1_Store");
	
					if (t1s == 0ul) {
						printStringLn("Unable to find the Thing1_Store inside the screen writer sink.");
						abort();
					}
					
					mutable uint64 t2s = psFindStore("Thing2_Store");
					
					if (t2s == 0ul) {
						printStringLn("Unable to find the Thing2_Store inside the screen writer sink.");
						abort();
					}					
					
					printStringLn("================ Final Results Begin ================");
					printStringLn("Thing2.dummy = " + (rstring)Thing2.dummy);
					printStringLn("\n\nContents of the Thing1_Store [TickerSymbol => CompanyName]");

					// Iterate the Thing1 store.
					mutable uint64 it = psBeginIteration(t1s);
					mutable rstring key = "";
					mutable rstring value = "";
					mutable rstring keyType = "";
					mutable rstring valueType = "";
			
					if (it == 0ul) {
						printStringLn("Unable to get an iterator for the Thing1_Store");
						abort();
					}

					while(psGetNext(t1s, it, key, value, keyType, valueType))  
						printStringLn("'"+key+"' ("+keyType+") => '"+(rstring)value+"' ("+valueType+")");                            

					psEndIteration(t1s, it);
					
					printStringLn("\n\nContents of the Thing2_Store [TickerSymbol => UniqueTickerId]");

					// Iterate the Thing2 store.
					it = psBeginIteration(t2s);
			
					if (it == 0ul) {
						printStringLn("Unable to get an iterator for the Thing2_Store");
						abort();
					}

					while(psGetNext(t2s, it, key, value, keyType, valueType))  
						printStringLn("'"+key+"' ("+keyType+") => '"+(rstring)value+"' ("+valueType+")");                            

					psEndIteration(t2s, it);			
					
					// So far so good. Let us now remove both the process stores.
					psRemoveStore(t1s);
					psRemoveStore(t2s);
					printStringLn("================ Final Results End   ================"); 
				}
		}
		
		
		// At the composite level, let us fuse all the operators into a single PE.
		config
			placement: partitionColocation("Process_Store_Test");
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/055_json_to_tuple_to_json_using_c++_com_acme_test_json_to_tuple_to_json_using_cpp_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/057_reading_nested_tuple_data_via_file_source_com_acme_test_Test1_spl/"> > </a>
</div>

