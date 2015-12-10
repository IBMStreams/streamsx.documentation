---
layout: samples
title: com.ibm.streamsx.ps
---

### com.ibm.streamsx.ps

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/com_ibm_streamsx_dps_samples_dps_test_1_DpsTest1_spl/"> < </a></div>

~~~~~~
/*
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2011, 2013
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with
# IBM Corp.
*/
/*
This example shows a particular implementation about how data can be
shared across multiple FUSED operators using an in-memory store.
Here, we are simply showing a way to use the SPL native function
facility to perform data sharing via an SPL-specific in-memory store.
As mentioned above, this example shows data sharing between multiple operators
that are fused inside a single PE (Processing Element). This data sharing
mechanism will NOT work between operators that are on different PEs.

This particular SPL file is a test application packaged inside of the 
process store (ps) toolkit in order to aid the testing of the ps toolkit.
This example is pre-packaged with the process store (ps) .so libraries for RHEL5, CentOS5, RHEL6, and CentOS6.
You can run this example only on Intel x86 machines installed with one of those flavors of Linux.

It is a critical feature that will be of tremendous use to share data among
different fused operators in a Streams application. Technical approach used in this in-memory
process store (ps) you will see below is a brilliant effort by my friend and our 
fantastic Streams designer/developer Bugra Gedik. He wrote the code for the in-memory process store
logic that is being used below via .so libraries. I cherished the opportunity to
collaborate with him on this toolkit project as well as in another complementary toolkit named
"Distributed Process Store [dps].

In order to compile and run this test applicaiton, you will find some tips in the following 
file available in this toolkit: ../../doc/ps-usage-tips.txt

Important Note
--------------
We provide two technical approaches for sharing data between different components of a Streams application.

1) Process Store  (ps) for data sharing among the fused operators within a single PE  [This SPL toolkit you are reading about now]
2) Distributed Process Store (dps) for data sharing among multiple PEs  [dps is a different SPL toolkit]

You can consider using both ps and dps to provide data sharing among many different fused and non-fused Streams operators.
Both the toolkits are available for a free download from the IBM developerWorks Streams Exchange web site.
(URL: http://tinyurl.com/kebzwyo)

A disclaimer: There is no formal plan at this time (Sep/2013) to make either the ps or the dps features
as part of the official InfoSphere Streams product. Both the process store (ps) and the 
distributed process store (dps) projects are made available in that URL shown above as reusable toolkits.
Streams developers can use them as they see fit for their project needs.
*/

// Declare the use of the two namespaces containing the process store native functions.
// You are also encouraged to refer to the native function model XML files available inside
// the com.ibm.streamsx directory of this SPL project.
// Associated C++ include files and the .so libraries for these native functions are
// made available in the impl/include and impl/lib directories of this SPL project.
// As shown in several other examples in this collection, there is also 
// the impl/bin/archLevel file that helps in selecting the appropriate .so library for
// the version of the Linux running on your machine.
use com.ibm.streamsx.process.store::*;
use com.ibm.streamsx.process.lock::*;

composite PsTest1 {
	graph
		//Simply invoke another composite that will showcase all the
		// capabilities of our in-memory store implementation.
		() as Sink1 = OperationsTest() {} 
}

// This composite contains operators (some are not fused and some are fused) containing
// code to test a bulk of our in-memory store operational features.
composite OperationsTest() {
	graph
		// Let us have a Beacon kick start the action.
		stream<int8 dummy> Beat = Beacon() {
			param iterations: 1u;
		}

		// In this single Custom operator, we will go through many of the
		// versatile native functions APIs for the in-memory store.
		stream<int32 dummy> DummyStream = Custom(Beat) {
			logic
				onTuple Beat: {
					mutable boolean res = false;
                
					{
						// All the native function APIs starting with psXXXXXX indicate that
						// these APIs will allow us to create, read, update and delete
						// data entries from any of the operators fused inside a single PE.
						// Here, ps stands for "Process Store".
						//
						// There are two kinds of process stores:
						// 1) Global process store (It is a single uber store that any operator within a PE can store, fetch, update, and delete data items).
						// 2) Named process store (It is a named store that can be accessed using a store handle to store, fetch, update and delete data items.)
						//
						// There is a very well thought out group of in-memory store APIs available. This example will show you how those
						// APIs will work. If needed, you can use this example as a reference and use this in-memory store in your own applications.
						//
						// Basic usage pattern for this particular in-memory store is that you can store any key/value pair as a data item in the process store.
						//
						//
						// ----------------------------- Beginning of Global Process Store functions -----------------------------
						printStringLn("===== Results from exercising various in-memory store APIs on GLOBAL process store are displayed below =====");
						// Let's put an int32 as a value and get it back
						// We can name our process store data item as 'abc' and store an integer value there.
						psPut("abc", 10); 
						mutable int32 v = 0;
						// The value we stored in the process store above is available for an
						// immediate read either within this operator or any other operators fused in a single PE.
						res = psGet("abc", v);
						assert(res==true); // get has succeeded 
						assert(v==10); 
		                
						// Yay!, we can use any type as value.
						// Let us replace the integer value we stored above with a tuple.
						res = psPut("abc", {fun=true, joy=[1,2,3]}); // replace '10'
						assert(res==false); // value was replaced, rather than inserted
						// Read back the value we stored in the process store and verify it.
						mutable tuple<boolean fun, list<int32> joy> funJoy = {};
						res = psGet("abc", funJoy);
						assert(res==true); // get has succeeded
						assert(funJoy=={fun=true,joy=[1,2,3]});
		
						// We can also obtain the type of the data stored in a store item.
						mutable rstring typeName = "";
						res = psTypeOf("abc", typeName);
						assert(res==true); // succeeded
						assert(typeName=="tuple<boolean fun,list<int32> joy>");
		
						// Query for a non-existing entry in the store and see it returning gracefully.
						res = psTypeOf("abcd", typeName);
						assert(res==false); // not there
		
						// We can check existence, also remove
						mutable boolean exists = psHas("abc");
						assert(exists); 
		
						// This is how we can remove an entry from the store.
						res = psRemove("abc");
						assert(res==true); // remove has succeeded 
						exists = psHas("abc");
						assert(!exists); 
		                
						// Let us show the versatility of our API Set.
						// Woo hoo!, we can use any type as key
						// In this case, we are using set<int32> type as a key and int32 as value.
						res = psPut({3, 5, 6}, 10);
						assert(res==true); // value was inserted
		
						// Replace the value of the data item we stored above.  
						res = psPut({3, 5, 6}, 11);
						assert(res==false); // value was replaced
						res = psGet({3, 5, 6}, v);
						assert(res==true); // get has succeeded 
						assert(v==11); 
		                
						// This is how we can clear the entire process store.
						// clear all contents
						psClear();
		
						// We can also get the size of our process store.
						uint64 size = psSize();
						assert(size==0ul);
		
						// Let us now store a few data items in the process store and
						// then do an iteration of the entire store.
						psPut("a", 1);
						psPut("b", 2);
						psPut("c", 3);
						psPut("d", 4);
		                
						// During the iteration, operations that require
						// modification to the store are not allowed.
						{
							uint64 it = psBeginIteration();
							mutable rstring key = "";
							mutable int32 value = 0;
		
							// Display the key and value of each item in the process store.
							while(psGetNext(it, key, value)) 
								printStringLn("'"+key+"' => "+(rstring)value);
								
							psEndIteration(it);  
						}
		
						printStringLn("");
		
						// Get rid of all the data items stored in the process store.
						psClear();
						// Let us now stretch it a little bit by using all kinds of
						// types as store data item keys and values.
						// int32 type for key and a map<int32, rstring> as value.
						psPut(1, {3: "x", 4:"y"});
						// rstring as key and int32 as value.
						psPut("b", 3);
						// list<int32> as key and set<int32> as value.
						psPut([4, 5, 6], {1, 2, 3});
						// tuple<rstring d, set<rstring> e> as key and rstring as value.
						psPut({d="d", e={"a", "b"}}, "abc");
		                
						// Let us iterate over the entire process store and print what it contains.
						// During the iteration, operations that require
						// modification to the store are not allowed.
						{
							uint64 it = psBeginIteration();
							mutable rstring key = "";
							mutable rstring value = "";
							mutable rstring keyType = "";
							mutable rstring valueType = "";
		
							while(psGetNext(it, key, value, keyType, valueType))  
								printStringLn("'"+key+"' ("+keyType+") => '"+(rstring)value+"' ("+valueType+")");
								                            
							psEndIteration(it);
						}         
		
						printStringLn("");
		
						// We can serialize a complex tuple structure into binary bits and store it in a blob typed variable.
						// We can also deserialize it from a blob typed variable back into a process store.
						//
						// We can serialize the store contents selectively by specifying a nested tuple structure
						// containing the combination of tuple<key, value> attributes inside the main tuple.
						// We will see how we can query a specific combination of data items from our process store.
						// 
						// At this point in our code, we have 4 different data items stored in our process store.
						// As you can see from the previous block of code that all 4 data items use completely
						// different key and value types.
						// Out of those 4 combinations, we are going fetch 3 key, value types and serialize them
						// into a blob data structure.
						{ // serialize
							tuple<tuple<int32 key,  map<int32, rstring> value> type1,
								tuple<rstring key,  int32 value> type2,
								tuple<tuple<rstring d, set<rstring> e> key, rstring value> type4> types = {};
							mutable blob data = [];
							// Fetch the matching data items in the store for the types specification we provided and
							// serialize all of the fetched data items.
							psSerialize(data, types);
							// Clear the entire process store.
							psClear();
							// Now, populate the store by deserializing the blob content.
							// We should get back the 3 data items that we serialized into a blob before clearing the entire store.
							psDeserialize(data, types);  
		
							mutable uint64 it = psBeginIteration();
							mutable rstring key = "";
							mutable rstring value = "";
							mutable rstring keyType = "";
							mutable rstring valueType = "";
		
							while(psGetNext(it, key, value, keyType, valueType))  
								printStringLn("'"+key+"' ("+keyType+") => '"+(rstring)value+"' ("+valueType+")");
								                            
							psEndIteration(it);
						}
		
						printStringLn("");
		
						// Let us experiment a little bit more with process store serialize and deserialize funtions.
						psClear();
						psPut({a=1,b=4}, "a");
						psPut({a=2,b=3}, "b");
						psPut({a=3,b=2}, "c");
						psPut({a=4,b=1}, "d");
						{
							// We are going to show here that we can serialize/clearStore/deserialize any number of times and
							// the data consistency in the in-memory store will remain the same.
							tuple<int32 a, int32 b> keyDummy = {};
							rstring valueDummy = "";
							mutable blob data = [];
							psSerialize(data, keyDummy, valueDummy);
							psClear();
							psDeserialize(data, keyDummy, valueDummy);
							psSerialize(data);
							psClear();
							psDeserialize(data, keyDummy, valueDummy);
						}
		
						{
							uint64 it = psBeginIteration();
							mutable rstring key = "";
							mutable rstring value = "";
							mutable rstring keyType = "";
							mutable rstring valueType = "";
		
							while(psGetNext(it, key, value, keyType, valueType))  
								printStringLn("'"+key+"' ("+keyType+") => '"+(rstring)value+"' ("+valueType+")");
								                            
							psEndIteration(it);
						}         
					} 
		
					printStringLn("");
					printStringLn("");                      
		
					// ----------------------------- End of Global Process Store functions -----------------------------
		
					// ----------------------------- Beginning of Named Process Store functions -----------------------------
					// Now, on to a new process store feature.
					// So far, we have been putting, getting, and deleting from a global process store.
					// We can also have named stores. 
					printStringLn("===== Results from exercising various in-memory store APIs on NAMED process store are displayed below =====");					
					
					{ 
						// We can do the same operations as above, but with an individual store
						// You can create any number of stores by optionally passing a name for the store.
						uint64 store1 = psCreateStore();
						assert(store1!=0ul); // successfully created
						uint64 store2 = psCreateStore("a");
						assert(store2!=0ul); // successfully created
						uint64 store3 = psCreateStore("b");
						assert(store3!=0ul); // successfully created
						uint64 store4 = psCreateStore("a");
						assert(store4==0ul); // duplicate
						uint64 store5 = psFindStore("b");
						assert(store5==store3); // found successfully
		
						// You can remove a named store using its store handle.
						psRemoveStore(store3);
		
						// We can find a store by its name.
						uint64 store6 = psFindStore("b");
						assert(store6==0ul); // not there anymore
		
						// Let's put an int32 as a value into a named store and get it back
						// We can name our process store data item as 'abc' and store an integer value there.                        
						psPut(store1, "abc", 10); 
						mutable int32 v = 0;
						res = psGet(store1, "abc", v);
						assert(res==true); // get has succeeded 
						assert(v==10); 
		
						// Yay!, we can use any type as value.
						// Let us replace the integer value we stored above with a tuple.                        
						res = psPut(store1, "abc", {fun=true, joy=[1,2,3]}); // replace '10'
						assert(res==false); // value was replaced, rather than inserted
						// Read back the value we stored in the process store and verify it.
						mutable tuple<boolean fun, list<int32> joy> funJoy = {};
						res = psGet(store1, "abc", funJoy);
						assert(res==true); // get has succeeded
						assert(funJoy=={fun=true,joy=[1,2,3]});
		
						// We can also obtain the type of the data stored in a store item.
						mutable rstring typeName = "";
						res = psTypeOf(store1, "abc", typeName);
						assert(res==true); // succeeded
						assert(typeName=="tuple<boolean fun,list<int32> joy>");
		                
						// We can check for existence, also remove
						mutable boolean exists = psHas(store1, "abc");
						assert(exists); 
		
						// This is how we can remove an entry from the store.
						res = psRemove(store1, "abc");
						assert(res==true); // remove has succeeded 
						exists = psHas(store1, "abc");
						assert(!exists); 
		
						// Let us show the versatility of our API Set.
						// Woo hoo! we can use any type as key
						// In this case, we are using set<int32> type as a key and int32 as value.
						res = psPut(store1, {3, 5, 6}, 10);
						assert(res==true); // value was inserted
		
						// Replace the value of the data item we stored above.  
						res = psPut(store1, {3, 5, 6}, 11);
						assert(res==false); // value was replaced
						res = psGet(store1, {3, 5, 6}, v);
						assert(res==true); // get has succeeded 
						assert(v==11); 
		
						// This is how we can clear the entire named process store.
						// clear all contents
						psClear(store1);
		
						// We can also get the size of our named process store.
						uint64 size = psSize(store1);
						assert(size==0ul); 
		
						// Let us now store a few data items in the process store and
						// then do an iteration of the entire store.                       
						psPut(store1, "a", 1);
						psPut(store1, "b", 2);
						psPut(store1, "c", 3);
						psPut(store1, "d", 4);
		                
						// During the iteration, operations that require
						// modification to the store are not allowed.
						{
							uint64 it = psBeginIteration(store1);
							mutable rstring key = "";
							mutable int32 value = 0;
		
							// Display the key and value of each item in the named process store.
							while(psGetNext(store1, it, key, value))  
								printStringLn("'"+key+"' => "+(rstring)value);
								                            
							psEndIteration(store1, it);
						}
		
						printStringLn("");
		
						// Get rid of all the data items stored in the named process store.
						psClear(store1);
						// Let us now stretch it a little bit by using all kinds of
						// types as store data item keys and values.
						// int32 type for key and a map<int32, rstring> as value.
						psPut(store1, 1, {3: "x", 4:"y"});
						// rstring as key and int32 as value.
						psPut(store1, "b", 3);
						// list<int32> as key and set<int32> as value.
						psPut(store1, [4, 5, 6], {1, 2, 3});
						// tuple<rstring d, set<rstring> e> as key and rstring as value.
						psPut(store1, {d="d", e={"a", "b"}}, "abc");
		
						// Let us iterate over the entire process store and print what it contains.
						// During the iteration, operations that require
						// modification to the store are not allowed.                        
						{
							uint64 it = psBeginIteration(store1);
							mutable rstring key = "";
							mutable rstring value = "";
							mutable rstring keyType = "";
							mutable rstring valueType = "";
		
							while(psGetNext(store1, it, key, value, keyType, valueType))  
								printStringLn("'"+key+"' ("+keyType+") => '"+(rstring)value+"' ("+valueType+")");     
		               
							psEndIteration(store1, it);
						}                       
		
						printStringLn("");
		
						// We can serialize a complex tuple structure into binary bits and store it in a blob typed variable.
						// We can also deserialize it from a blob typed variable back into a process store.
						//
						// We can serialize the store contents selectively by specifying a nested tuple structure
						// containing the combination of tuple<key, value> attributes inside the main tuple.
						// We will see how we can query a specific combination of data items from our process store.
						// 
						// At this point in our code, we have 4 different data items stored in our process store.
						// As you can see from the previous block of code that all 4 data items use completely
						// different key and value types.
						// Out of those 4 combinations, we are going fetch 3 key, value types and serialize them
						// into a blob data structure.
						{ // serialize
							tuple<tuple<int32 key,  map<int32, rstring> value> type1,
								tuple<rstring key,  int32  value> type2,
								tuple<tuple<rstring d, set<rstring> e> key,  rstring  value> type4> types = {};
							mutable blob data = [];
							// Fetch the matching data items in the store for the types specification we provided and
							// serialize all of the fetched data items.
							psSerialize(store1, data, types);
							psClear(store1);
		
							// Now, populate the store by deserializing the blob content.
							// We should get back the 3 data items that we serialized into a blob before clearing the entire store.
							psDeserialize(store1, data, types);  
		
							uint64 it = psBeginIteration(store1);
							mutable rstring key = "";
							mutable rstring value = "";
							mutable rstring keyType = "";
							mutable rstring valueType = "";
							while(psGetNext(store1, it, key, value, keyType, valueType))  
								printStringLn("'"+key+"' ("+keyType+") => '"+(rstring)value+"' ("+valueType+")");
								                            
							psEndIteration(store1, it);                           
						}
		
						printStringLn("");
		
						// Let us experiment a little bit more with process store serialize and deserialize funtions.
						psClear(store1);
						psPut(store1, {a=1,b=4}, "a");
						psPut(store1, {a=2,b=3}, "b");
						psPut(store1, {a=3,b=2}, "c");
						psPut(store1, {a=4,b=1}, "d");
						{
							// We are going to show here that we can serialize/clearStore/deserialize any number of times and
							// the data consistency in the in-memory store will remain the same.
							tuple<int32 a, int32 b> keyDummy = {};
							rstring valueDummy = "";
							mutable blob data = [];
							psSerialize(store1, data, keyDummy, valueDummy);
							psClear(store1);
							psDeserialize(store1, data, keyDummy, valueDummy);  
							psSerialize(store1, data);
							psClear(store1);
							psDeserialize(store1, data, keyDummy, valueDummy);
						}
		
						{
							uint64 it = psBeginIteration(store1);
							mutable rstring key = "";
							mutable rstring value = "";
							mutable rstring keyType = "";
							mutable rstring valueType = "";
							while(psGetNext(store1, it, key, value, keyType, valueType))  
								printStringLn("'"+key+"' ("+keyType+") => '"+(rstring)value+"' ("+valueType+")");
								                            
							psEndIteration(store1, it);
						}                                 
					}
					
					mutable list<rstring> storeNames = [];
					mutable list<uint64> storeHandles = [];
					// We can also get information about all the named stores in this PE (processing element).
					psGetAllStoreInfo(storeNames, storeHandles);
					println(storeNames);
					println(storeHandles);
					// ----------------------------- End of Named Process Store functions -----------------------------
		
					//Emit a dummy tuple to do a few more in-memory store activities in the subsequent operators.
					mutable DummyStream _dummy = {dummy = 10};
					submit(_dummy, DummyStream);
			}
		}

		// In the previous Custom operator, we exercised many of the in-memory store APIs all within a single operator.
		// Now, we are going to have the following two operators to show how fused operators can share data between them via the process store.
		stream<DummyStream> SharedDataProvider = Custom(DummyStream) {
			logic
				onTuple DummyStream: {
					// We will create a named store called "Life_Is_Good".
					uint64 myStoreHandle = psCreateStore("Life_Is_Good");
					assert(myStoreHandle!=0ul); // successfully created
					// Let us put some values.
					// int32 type for key and a map<int32, rstring> as value.
					psPut(myStoreHandle, 1964, {1: "1965", 2:"1995"});
					// rstring as key and int32 as value.
					psPut(myStoreHandle, "Star Wars 4", 1977);
					// list<int32> as key and set<int32> as value.
					psPut(myStoreHandle, [205, 405, 605], {45, 65, 85});
					// tuple<rstring d, set<rstring> e> as key and rstring as value.
					psPut(myStoreHandle, {a="IBM", b={"MSFT", "GOOG"}}, "Great Tech Stocks");     
					submit(DummyStream, SharedDataProvider);
				}

			config
				// Let us fuse this operator with the following operator so that they will be
				// together inside the same PE.
				placement: partitionColocation("In_Memory_Data_Sharing");
		}

		// In this Custom operator, we are going to access the data stored by the
		// previous Custom operator into the in-memory named process store.
		() as SharedDataConsumer = Custom(SharedDataProvider as SDP) {
			logic
				onTuple SDP: {
					// Let us find the store created by the previous Custom operator.
					uint64 myStoreHandle = psFindStore("Life_Is_Good");
					assert(myStoreHandle != 0ul); // Ensure that the store is still there.

					// When the application is compiled with -a (optimized code generation), 
					// our assert statement above will be disabled.
					// In that case, if the named store is not found or if this operator is 
					// not fused with the previous operator, then it will result in a 
					// PE failure while trying to access the named store in the code below.
					// We will do a check for the valid store handle.
					if (myStoreHandle == 0ul) {
						printStringLn("Unable to find the name store 'Life_Is_Good'.");
						return;
					}

					printStringLn("");
					printStringLn("");
					printStringLn("===== Following are the results obtained from reading the named store 'Life_Is_Good' inside the second FUSED operator =====");
					printStringLn("Handle for the 'Life_Is_Good' named store = " + (rstring) myStoreHandle); 
					uint64 it = psBeginIteration(myStoreHandle);
					mutable rstring key = "";
					mutable rstring value = "";
					mutable rstring keyType = "";
					mutable rstring valueType = "";

					while(psGetNext(myStoreHandle, it, key, value, keyType, valueType))  
						printStringLn("'"+key+"' ("+keyType+") => '"+(rstring)value+"' ("+valueType+")");                            

					psEndIteration(myStoreHandle, it);

					// You can see above that we can access our named process store to 
					// read/modify/delete the data items originally stored by the previous 
					// operator with which our current operator is fused.
					// In addition to using the named process store, you can also share data 
					// via the global process store in the same way.
                  
					// In this operator, let us also remove the named store created by the 
					// previous Custom operator.
					psRemoveStore(myStoreHandle);
				}

			config
				// Let us fuse this operator with the previous operator so that they will be
				// together inside the same PE.
				placement: partitionColocation("In_Memory_Data_Sharing_Within_One_PE");
		}
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/com_ibm_streamsx_dps_samples_dps_test_1_DpsTest1_spl/"> < </a></div>

