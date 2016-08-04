---
layout: samples
title: com.ibm.streamsx.dps
---

### com.ibm.streamsx.dps

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/905_gate_load_balancer_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/com_ibm_streamsx_ps_samples_ps_test_1_PsTest1_spl/"> > </a>
</div>

~~~~~~
/*
================================================================================================
"We are what we repeatedly do. Excellence, therefore, is not an act, but a habit." -- Aristotle

"If you want to achieve excellence, you can get there today.
 As of this second, quit doing less-than-excellent work." -- Thomas J. Watson (Founder of IBM)
================================================================================================
*/

/*
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2011, 2015
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with
# IBM Corp.
*/
/*
This is a test driver application available inside the dps toolkit. It shows a way for
Streams applications to have a distributed process store (dps) for sharing data among 
multiple PEs (Processing Elements) running on one or more machines. In this implementation of dps,
we are using the following NoSQL databases as our distributed data stores

1) memcached 1.4.15 or higher versions
2) Redis 2.8.17 or higher versions    [No Redis provided HA facility in these versions]
3) Apache Cassandra 2.1.0 or higher versions
4) IBM Cloudant DBaaS  [Database as a service on the cloud]
5) Apache HBase 0.98.8 or higher versions for Hadoop2
6) MongoDB 2.6.6 or higher versions
7) Couchbase 3.0.2 or higher versions
8) Aerospike 3.4.1 or higher versions
9) Redis Cluster 3.0.0 or higher version  [With HA facility for automatic fail-over when
   a Redis instance or the entire machine crashes] 

Making this facility available for Streams opens up new possibilities to share data even among PEs
belonging to different Streams applications. Streams application designers/developers will be able to do
neat things with this facility. memcached, redis, Cassandra, Cloudant, HBase, Mongo, 
Couchbase and Aerospike are open source offerings based on BSD and Apache licensing schemes and
they are used by many top flight commercial software companies. Depending on whether you are using 
memcached or redis or Cassandra or Cloudant or HBase or Mongo or Couchbase or Aerospike, you must first
do a simple configuration before attempting to compile and run this test SPL application.
Please refer to this SPL project directory's etc/no-sql-kv-store-servers.cfg file.
In addition, it is recommended that you read the doc/dps-usage-tips.txt file in this toolkit directory to get some
tips about setting up a memcached or a redis or a Cassandra or Cloudant or HBase or Mongo or Couchbase or
Aerospike back-end NoSQL store server environment.

Important Note
--------------
We have the following two completely different approaches for sharing data between
Streams operators. We would like to suggest the following as a guideline about their usage.

1) For sharing data among fused operators that are part of a single PE, it is a lot
easier and faster to use our process store (ps) facility. Please refer to a different toolkit
that gives an elaborate demonstration of that feature. It is available for download as a 
separate toolkit from the IBMStreams github.

2) For sharing data among non-fused operators that are part of different PEs, you could use
our distributed process store (dps) facility. This toolkit contains the dps source code and a test application with
a detailed explanation about using the dps. It is better to use this toolkit in Distributed mode rather than
in Standalone mode. This package is available for download as a toolkit from the IBMStreams github.

This test application below has plenty of assert statements. If you want to see those assertions printed, 
you should build it without the -a flag i.e. with optimized code generation turned off.

In one of the tests below, we will do one million inserts into the store. Please 
ensure that your memcached server is started with the -m option to use at least 128MB memory.
Other K/V stores mentioned above will also easily handle that test for million inserts.

Following are the major parts that make up the dps facility:

a) SPL test application (file you are reading now) to show how the dps native functions can be used for distributed data sharing.
b) Native function model file (com.ibm.streamsx/store/distributed/native.funcion/function.xml) that shows a list of all the
   dps native functions available for use. 
c) Source code for the DistributedProcessStore available here in the impl/src and impl/include directories. 
  (As a first step, run the mk script here in the ./impl directory. It will build a .so file and copy it
   to a platform-specific location inside the impl/lib directory. After that, you can use the build and run
   scripts available in this example directory to compile and run this test application.

Our distributed process store provides a "global + distributed" in-memory cache for 
different processes (multiple PEs from one or more Streams applications). We provide a set of free for all 
native function APIs to create/read/update/delete data items on one or more stores. In the worst case, there could be 
multiple writers and multiple readers for the same store. It is important to note that a Streams application 
designer/developer should carefully address how different parts of his/her application will access the store 
simultaneously i.e. who puts what, who gets what and at what frequency from where etc.

Please refer to the doc/dps-usage-tips.txt file in this toolkit directory for configuring and running this
test application using one or more memcached (OR) redis (OR) Cassandra (OR) Cloudant (OR) HBase (OR) Mongo (OR)
Couchbase (OR) Aerospike servers. The same test driver code in this SPL application will work for memcached (OR)
redis (OR) Cassandra (OR) Cloudant (OR) HBase (OR) Mongo (OR) Couchbase (OR) Aerospike environment without a need for recompiling.

A disclaimer: There is no formal plan at this time (Feb/2015) to make either the ps or the dps features
as part of the official InfoSphere Streams product. Both the process store (ps) and the 
distributed process store (dps) toolkits are available for download in the IBMStreams github.
Streams developers can download and use them as they see fit for their project needs.

In jointly creating this useful toolkit, I had another great opportunity to
collaborate with my great friend and our fantastic Streams designer/developer Bugra Gedik.
*/
// Declare the use of the namespace under which all our dps native functions are available.
use com.ibm.streamsx.store.distributed::*;
use com.ibm.streamsx.lock.distributed::*;

composite DpsTest1
{
    graph
    	// Kickstart our Distributed Process Store (dps) tests.
    	// Because of the web based Interaction needs of Cloudant and due to its eventual consistency storage model,
    	// Cloudant is usually slow in comparison to Redis and it may not also handle the frequent 
    	// create_store/delete_store/create_same_store cycle we do in these tests. 
    	// So, set your expectations accordingly when using the dps toolkit with not so fast NoSQL K/V stores such as
    	// Cloudant, Cassandra, HBase, Mongo, Couchbase etc.
        () as Sink1 = GeneralTest() {}
        
        // Our dps store also supports a distributed lock mechanism when multiple
        // threads want to access the same store to do transaction based updates. 
        // i.e. a bunch of "get, put, remove" activities all done in one block.
        // Such things are better done within a critical section by acquiring a lock so that
        // two threads will not get into the same store at the same time.
        // Let us do a few tests to show how our dps handles user defined distributed locks.
        //
		// Please be aware that this particular test exercises heavy locking and unlocking of
		// the K/V store to have protected read/write operation. If a chosen back-end data store
		// provides eventual consistency (such as Cassandra, Cloudant etc.) or performs 
		// put/get operations to/from the disk media (HBase, Mongo, Couchbase etc.), the technical requirements for this test 
		// will not be met by such data stores and this test may not finish correctly in such
		// environments (e-g: Cassandra, Cloudant, HBase, Mongo, Couchbase etc.). That is because, data stores with eventual consistency
		// as well as storing it in disks may not return the correct value during a get that
		// immediately follows a put operation. For such data stores, it will take a while 
		// (a second or two) before the actual value we put is written to
		// all the replica servers' memory/disk. Hence, LockTest with too many iterations is not a 
		// suitable one for such data stores based on eventual consistency put/get as well disk based put/get (HBase, Mongo, Couchbase).
		// Before running this test for those slow data stores, please refer to the commentary at the top of
		// this composite to reduce the test count in order to obtain reasonable results.
        () as Sink2 = LockTest() {}
		
        // Do 100K writes and 100K reads and time it.
        // Please be aware this high volume test will finish in a decent time for memcached, Redis and Aerospike.
        // However, Cassandra, Cloudant, HBase, Mongo, Couchbase etc. are not very fast due to their disk writes and 
        // hence it may be a long wait before this test completes when you use those data stores.
		// Before running this test for those slow data stores, please refer to the commentary at the top of
		// this composite to reduce the test count in order to obtain reasonable results.
        () as Sink3 = ReadWritePerformanceTest() {}
        
        // Users can directly execute native back-end data store commands that are of 
        // fire and forget nature (one way calls and not request/response calls).
        // If Cloudant or HBase is used as a back-end data store, then two way calls are allowed because
        // of the well supported/documented REST and JSON data exchange format in Cloudant and HBase.
        () as Sink4 = RunNativeDataStoreCommands() {}
}

composite GeneralTest()
{
	type
		parallelLoadTestResults = tuple<rstring dpsTask, int32 clientId, rstring startTime, 
			rstring endTime, int64 elapsedTime, int32 errorCnt>;
		
    graph
        stream<int8 dummy> Beat = Beacon() {
            param
            	iterations: 1u;
            	initDelay: 4.0;
        }
    
    	// Here, you will see the use of almost every native function API available for dps.
    	// It is a powerful collection of APIs that you can use in your distributed
    	// Streams application(s). Primary purpose of these APIs is to enable Streams PEs
    	// running on one or more machines to share any arbitrary data between themselves.
    	// Every store created via the dps API set will let you perform full CRUD operations.
    	// Since it is a distributed cache that can be accessed by any PE using the 
    	// dps APIs, extra thinking will be needed about who will write, who will read,
    	// from where and at what frequency. As mentioned at the top of this file,
    	// everything comes together with the power of the proven commercial grade
    	// memcached (OR) redis (OR) Cassandra (OR) Cloudant (OR) HBase (OR) Mongo (OR) 
    	// Couchbase (OR) Aerospike acting as our back-end K/V store.
    	//
    	// Proceed below to learn about using the dps APIs.  
    	//
    	// =========================  This operator demonstrates how the many different dps APIs work =========================
        stream<Beat> NextBeat = Custom(Beat) {
            logic
                onTuple Beat: {
                    mutable uint64 err = 0ul;
                    mutable boolean res = false;
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

                    // Before we start, a quick thing about how data will be stored in the back-end data store infrastructure.
                    // There will be two kinds of storage areas available for the developers.
                    //
                    // 1) Global storage area where one can use a small subset of the dps APIs. 
                    //    Data items stored here must have a TTL [Time To Live in seconds) property so that they will be
                    //    automatically removed after the specified TTL time has expired. Certain applications will need such a 
                    //    global storage space to keep the ephemeral Key Value pairs with a preset life time.
                    //    
                    // 2) Several user created stores that will act as containers to hold the data items forever unless
                    //    otherwise the user deletes them or the user removes the entire store. Such user created stores support
                    //    richer APIs than what one can do with the option (1) above. This type of user created stores will be the
                    //    right way to use the dps facility, whereas the global storage area with the TTL feature can be used in
                    //    special cases where there is a need to automatically age out the stored data items.
                    // 
                    // Let us first gain experience with option (1) which only supports 4 store activities [put, get, remove, has].
                    // After learning option (1) i.e. global storage for TTL based K/V pairs, bulk of the remaining code will 
                    // provide a detailed walk-through of all the possibilities for using option (2) i.e. user created stores.
                    //
                    // ================================= (1) put, get, remove, check existence of data items with TTL ====================================
                    // In order to store TTL based key value pairs, one can directly start storing the data in the global storage area as shown below.
                    // For the put operation with TTL option, very first argument is the key, second argument is the value, 
                    // third argument is a non zero TTL in seconds, fourth argument will receive the error code if any from the performed operation.
                    // Your key and value can be of any SPL type. (If the TTL value is set to 0, then that K/V pair will not be removed automatically.
                    // Instead, it will stay there forever until the user calls the dpsRemoveTTL API to remove it.)
                    //
                    // Do the TTL tests only on those back-end data store products that support the dps TTL APIs.
                    if (dbProductName != "cloudant") { 
                    	// DPS TTL APIs will let you assign arbitrary TTL values for individual K/V pairs when you use
                    	// memcached, Redis, Cassandra, Mongo or Couchbase. But, HBase doesn't allow different TTL values for different
                    	// K/V pairs. HBase supports only a single TTL value for all the data items that are stored using
                    	// the DPS TTL APIs. That is a limitation in HBase (as of Nov/2014). Hence, if you are using HBase,
                    	// it is better to use the same TTL value for all your TTL based data items. If you change the TTL
                    	// value across different dpsPutTTL calls, that will affect the expiration policy for the K/V pairs that
                    	// were already stored. Please be aware of this HBase TTL behavior.
	                    mutable rstring myKey = "", myValue = "";
	                    myKey = "Harvard";
	                    myValue = "Cambridge";
	                    // Put a K/V pair with 5 seconds of TTL.
	                    res = dpsPutTTL(myKey, myValue, 5u, err);
	                    
	                    if (res == false) {
	                    	printStringLn("Unexpected error in dpsPutTTL. Error code=" + (rstring)dpsGetLastErrorCodeTTL() + ", Error msg=" + dpsGetLastErrorStringTTL());
	                    }
	                    
	                    myKey = "Yale";
	                    myValue = "New Haven";
	                    res = dpsPutTTL(myKey, myValue, 5u, err);
	                    
	                    if (res == false) {
	                    	printStringLn("Unexpected error in dpsPutTTL. Error code=" + (rstring)dpsGetLastErrorCodeTTL() + ", Error msg=" + dpsGetLastErrorStringTTL());
	                    }
	                    
	                    // Check for the existence of this key to ensure it is there in the global storage area of the back-end data store.
	                    res = dpsHasTTL(myKey, err);
	                    
	                    if (res == true) {
	                    	printStringLn("TTL based K/V pair 'Yale':'New Haven' exists in the global store.");
	                    } else {
	                    	printStringLn("Unexpected error in checking for the existence of the K/V pair 'Yale':'New Haven'. Error code=" + 
	                    		(rstring)dpsGetLastErrorCodeTTL() + ", Error msg=" + dpsGetLastErrorStringTTL());
	                    }
	                    
	                    // Read the value we stored in this TTL based data item.
	                    myKey = "Harvard";
	                    res = dpsGetTTL(myKey, myValue, err);
	                    
	                    if (res == true) {
	                    	printStringLn("TTL based K/V pair is read successfully from the global store. Key=" + myKey + ", Value=" + myValue);
	                    } else {
	                    	printStringLn("Unexpected error in reading the K/V pair 'Harvard':'Cambridge'. Error code=" + 
	                    		(rstring)dpsGetLastErrorCodeTTL() + ", Error msg=" + dpsGetLastErrorStringTTL());
	                    }
	                    
	                    mutable float64 delayInSeconds = 7.0;
	                    
	                    if (dbProductName == "mongo") {
	                    	// In Mongo, its background TTL expiration task is launched only at every minute boundary (as of Dec/2014).
	                    	// Hence, we will wait for slightly more than a minute.
	                    	delayInSeconds = 70.0;
	                    }
	                    
	                    // Let use wait here for a few seconds so that those two data items will be removed automatically after the TTL expiration.
	                    block(delayInSeconds);
	                    
	                    // If we try to read those two keys now, we should not see them in the back-end data store.
	                    myKey = "Yale";
	                    myValue = "";
	                    res = dpsGetTTL(myKey, myValue, err);
	                    
	                    if (res == true) {
	                    	printStringLn("Unexpected error: TTL based K/V pair is still present after the TTL expiration. Key=" + myKey + ", Value=" + myValue);
	                    } else {
	                    	printStringLn("Expected error in reading the K/V pair 'Yale':'New Haven' after its TTL expiration. Error code=" + 
	                    		(rstring)dpsGetLastErrorCodeTTL() + ", Error msg=" + dpsGetLastErrorStringTTL());
	                    }                    
	
						myKey = "Harvard";
	                    res = dpsHasTTL(myKey, err);
	                    
	                    if (res == true) {
	                    	printStringLn("Unexpected error: TTL based K/V pair 'Harvard':'Cambridge' is still present after the TTL expiration.");
	                    } else {
	                    	printStringLn("K/V pair 'Harvard':'Cambridge' was already removed after its TTL expiration.");
	                    }                     
	                    
	                    // Let us exercise the remaining API (dpsRemoveTTL) that can be used with the TTL based data items.
	                    // We can remove a TTL based data item ahead of its TTL expiration time.
	                    // Let us use a complex typed key and value.
	                    mutable map<rstring, uint64> myComplexKey = {"Apple":1ul, "Orange":2ul};                  
	                    mutable tuple<boolean fun, list<int32> joy> myComplexValue = {fun=true, joy=[7, 8, 9]};
	                    dpsPutTTL(myComplexKey, myComplexValue, 5u, err);
	                    // Insert one more TTL based data item.
	                    myComplexKey = {"x":23ul, "y":56ul}; 
	                    myComplexValue = {fun=false, joy=[1, 2, 3]};
	                    dpsPutTTL(myComplexKey, myComplexValue, 5u, err);
	                    
	                    // Read back the data item we put earlier
	                    myComplexKey = {"Apple":1ul, "Orange":2ul};
	                    dpsGetTTL(myComplexKey, myComplexValue, err);
	                    
	                    if (err == 0ul) {
	                    	printStringLn("TTL based K/V pair is read successfully from the global store. Key=" + (rstring)myComplexKey + ", Value=" + (rstring)myComplexValue);
	                    } else {
	                    	printStringLn("Unexpected error in reading the K/V pair for " + (rstring)myComplexKey + ". Error code=" + 
	                    		(rstring)dpsGetLastErrorCodeTTL() + ", Error msg=" + dpsGetLastErrorStringTTL());
	                    }
	                    
	                    // Let us remove the other complex data item we stored.
	                    myComplexKey = {"x":23ul, "y":56ul}; 
	                    res = dpsRemoveTTL(myComplexKey, err);
	                    
	                    if (res == true) {
	                    	printStringLn("Successfully removed the TTL based data item with a key " + (rstring)myComplexKey + ".");
	                    } else {
	                    	printStringLn("Unexpected error in removing the TTL based data item with a key " + 
	                    		(rstring)myComplexKey + ". Error code=" + 
	                    		(rstring)dpsGetLastErrorCodeTTL() + ", Error msg=" + dpsGetLastErrorStringTTL());
	                    }
	                    
	                    // Let use wait here for a few seconds so that those two data items will be removed automatically after the TTL expiration.
	                    block(delayInSeconds);
	                    
	                    // If we try to check for the existence of a data item now, we should not see it in the back-end data store.
						myComplexKey = {"Apple":1ul, "Orange":2ul};
	                    res = dpsHasTTL(myKey, err);
	                    
	                    if (err != 0ul) {
	                    	printStringLn("Unexpected error in checking the existence of the K/V pair for " + (rstring)myComplexKey + ". Error code=" + 
	                    		(rstring)dpsGetLastErrorCodeTTL() + ", Error msg=" + dpsGetLastErrorStringTTL());
	                    } else if (res == true) {
	                    	printStringLn("Unexpected error: TTL based K/V pair for " + (rstring)myComplexKey + " is still present after the TTL expiration.");
	                    } else {
	                    	printStringLn("K/V pair for " + (rstring)myComplexKey + " was already removed after its TTL expiration.");
	                    }                               
	                    
	                    // At this point we demonstrated all four applicable functions for dealing with TTL based K/V pairs.
	                    printStringLn("=== End of testing for TTL based put, get, has, and remove. ===");
                    }
                    // ==================== End of testing the features of global storage with TTL based data items =========================
                                        
                    // ================================= (2) User created stores [Applicable in majority of the dps use cases) ===========================
                    // As explained above, data items stored in the user created stores will live forever unless they are deleted by the user via an API.
                    // Rest of the code below will feature everything that the user created stores support.
                    //                    
                    mutable uint64 s = 0ul, os=0ul;
                    
					mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
					mutable int64 _timeInNanoSecondsAfterExecution = 0l;
					mutable timestamp _timeNow = getTimestamp();
					_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
					// Inside a given PE, very first contact to the store via any available dpsXXXX function will take a slightly longer time to complete.
					// That is due to the cost we have to pay for doing initial connection setup with the configured memcached (OR) redis (OR)
					// Cassandra (OR) Cloudant (OR) HBase (OR) Mongo (OR) Couchbase (OR) Aerospike servers.
					// This connection setup is done only once during the lifetime of a PE. It is advisable to simply do a dummy
					// activity inside a PE via an initialize operator by creating and removing a dummy store.
					rstring dummyRstring = "";
					uint32 dummyUint32 = 0u;
					// It is required to indicate what SPL type will make up the key and value of this store.
					// Simply pass a dummy key and dummy value so that their SPL types will be automatically inferred during the creation of that store.
					// Important note: After creating a store this way, there will not be any check done during the future put operations to validate whether you are
					// using the correct data types indicated at the time of store creation via dummy key and dummy value. It is better to have all the
					// entries to have uniform key:value data types in order for that store to be practically useful. So, a simple advice is don't use
					// the put call with different data types for keys and values of any given store. If you do that, then you are on your own and
					// as a result you are making that store not very useful. It is left to the dps user to follow a disciplined approach for
					// maintaining content uniformity within a store. So, create a store with the required key and value types and simply stick to that
					// key:value pair data type for the full life of that store.
                    os = dpsCreateStore("myDBStore1", dummyRstring, dummyUint32, err);
					_timeNow = getTimestamp();
					_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
					mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
					printStringLn("Time taken for executing dpsCreateStore = " +  (rstring)_totalExecutionTime + " nanosecs");
					
					if (err != 0ul) {
						printStringLn("Unexpected error in creating a store named myDBStore1: rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}
					
                    assert(os!=0ul && err==0ul); 

                    s = dpsCreateStore("myDBStore1", dummyRstring, dummyUint32, err);
                    // Trying to create another store with the same name will result in an error.
                    // We can display the error code and error message.
					if (err != 0ul) {
						printStringLn("Expected error in creating a duplicate store named myDBStore1: rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}	

                    assert(s==0ul && err!=0ul);   // <---- Attempt to create a duplicate store will return a store id of 0 and a non-zero error code/msg.
					// ==================================================================================
					// Let us show a few things about creating/finding/removing stores and distributed locks.
					// Spaces are allowed in store names as well in the data item key names.
					list<rstring> dummyRstringList = ["1", "2"];
					map<rstring, uint64> dummyRstringUint64Map = {"a":34ul, "b":45ul};
					s = dpsCreateStore("My Mega Store1", dummyRstringList, dummyRstringUint64Map, err);
					
					if (err != 0ul) {
						printStringLn("Error in creating My Mega Store1. rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					} else {
						printStringLn("My Mega Store1 was created with an id of " + (rstring)s);
						// Find the store we created above.
						mutable uint64 k = dpsFindStore("My Mega Store1", err);
						printStringLn ("Found store k=" + (rstring)k + ", which is same as s=" + (rstring)s);
						
						// Since we found the store successfully, let us get the original name of that store,
						// spl type name of that store's key, and spl type name of that store's value.
						// These three values are tagged as part of every store's metadata information.
						printStringLn("Metadata 1: Original name of a store with an id " + (rstring)k + " is '" +  dpsGetStoreName(k) + "'");
						printStringLn("Metadata 2: SPL type name for the key of a store with an id " + (rstring)k + " is '" +  dpsGetSplTypeNameForKey(k) + "'");
						printStringLn("Metadata 3: SPL type name for the value of a store with an id " + (rstring)k + " is '" +  dpsGetSplTypeNameForValue(k) + "'");
						
						k = 55555ul;
						// Try to create or get the same store as above.
						k = dpsCreateOrGetStore("My Mega Store1", dummyRstringList, dummyRstringUint64Map, err);
						printStringLn ("Got store k=" + (rstring)k + ", which is same as s=" + (rstring)s);
						
						// Try to create a new store with that same.
						k = dpsCreateStore("My Mega Store1", dummyRstringList, dummyRstringUint64Map, err);
						if (err != 0ul) {
							printStringLn("Expected error in creating a store named My Mega Store1: rc = " + (rstring)dpsGetLastStoreErrorCode() + 
								", msg = " + dpsGetLastStoreErrorString());
						}						

						// Remove and try to find that store again.
						dpsRemoveStore(s, err);
						k = dpsFindStore("My Mega Store1", err);
						printStringLn("After store Removal, an attempt to find that store returned these results: store k=" + 
							(rstring)k + ", err=" + (rstring)err + ", msg=" + dpsGetLastStoreErrorString());
					}
					
					// Distributed locks are important part of the dps in letting multiple
					// PEs/applications running on one more machines safely perform store operations without
					// bumping into each other.
					// Let us create a distributed lock.
					// You can have spaces in the middle of a lock name. We support that.
					mutable uint64 l = 0ul;
					l = dlCreateOrGetLock("My Sentinel Lock1", err);

					if (err != 0ul) {
						printStringLn("Error in creating My Sentinel Lock1. rc = " + (rstring)dlGetLastDistributedLockErrorCode() + 
							", msg = " + dlGetLastDistributedLockErrorString());
					} else {
						printStringLn("My Sentinel Lock1 was created with an id of " + (rstring)l);
						// Try to create or get that same lock again.
						mutable uint64 k = 55555ul;
						k = dlCreateOrGetLock("My Sentinel Lock1", err);
						printStringLn ("Got lock k=" + (rstring)k + ", which is same as l=" + (rstring)l);										
					
						// Acquire that lock with a lease time for 18 seconds and wait no more than 30 seconds to acquire the lock.
						dlAcquireLock(l, 18.0, 30.0, err);
						if (err == 0ul) {
							printStringLn("We acquired the lock My Sentinel Lock1 l=" + (rstring)l);
						} else {
							printStringLn("Failed to acquire the lock My Sentinel Lock1 l=" + (rstring)l + 
								" rc = " + (rstring)dlGetLastDistributedLockErrorCode() + 
								", msg = " + dlGetLastDistributedLockErrorString());
						}

						// Let us do a mini store operation here by holding onto our lock.					
						s = dpsCreateStore("My Well Protected Store1", dummyRstring, dummyRstring, err);
						dpsPut(s, "Streams", "Flowing steady and fast since 2009.", err);
						dpsPut(s, "Spark", "Not strikingly fast as of 2015.", err);
						dpsPut(s, "Storm", "Not a very fast moving one as of 2015.", err);
						dpsRemoveStore(s, err);
						
						// Release the lock.
						dlReleaseLock(l, err);
						if (err == 0ul) {
							printStringLn("We released the lock My Sentinel Lock1 l=" + (rstring)l);
						} else {
							printStringLn("Failed to release the lock My Sentinel Lock1 l=" + (rstring)l + 
								" rc = " + (rstring)dlGetLastDistributedLockErrorCode() + 
								", msg = " + dlGetLastDistributedLockErrorString());
						}						
						
						// Remove that lock.	
						boolean myResult = dlRemoveLock(l, err);
						if (err == 0ul && myResult == true) {
							printStringLn("We removed the lock My Sentinel Lock1 l=" + (rstring)l);
						} else {
							printStringLn("Failed to remove the lock My Sentinel Lock1 l=" + 
								(rstring)l + ", err=" + (rstring)err + ", msg=" + 
								dlGetLastDistributedLockErrorString());
						}			
					}
					// ==================================================================================
					_timeNow = getTimestamp();
					_timeInNanoSecondsBeforeExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
                    s = dpsFindStore("myDBStore1", err);
					_timeNow = getTimestamp();
					_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
					_totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
					printStringLn("Time taken for executing dpsFindStore = " +  (rstring)_totalExecutionTime + " nanosecs"); 
					
					if (err != 0ul) {
						printStringLn("Unexpected error in finding a store named myDBStore1: rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}
					
                    assert(s==os && err==0ul);

					_timeNow = getTimestamp();
					_timeInNanoSecondsBeforeExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
                    dpsRemoveStore(s, err);
					_timeNow = getTimestamp();
					_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
					_totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
					printStringLn("Time taken for executing dpsRemoveStore = " +  (rstring)_totalExecutionTime + " nanosecs"); 
					
					if (err != 0ul) {
						printStringLn("Unexpected error in removing a store named myDBStore1: rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}
										
                    assert(err==0ul);
                    
                    s = dpsFindStore("myDBStore1", err);
                    
					if (err != 0ul) {
						printStringLn("Expected error in finding an already removed store named myDBStore1: rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}

                    assert(s==0ul && err!=0ul);    // <---- Attempt to find a non-existing store will return a store id of 0 and a non-zero error code/msg
                    
                    int32 dummyInt32 = 0;
                    os = dpsCreateOrGetStore("myDBStore2", dummyRstring, dummyInt32, err);

					if (err != 0ul) {
						printStringLn("Unexpected error in creating a new store named myDBStore2: rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}                    
                    
                    assert(os!=0ul && err==0ul); 
                    s = dpsCreateOrGetStore("myDBStore2", dummyRstring, dummyInt32, err);
                    
					if (err != 0ul) {
						printStringLn("Unexpected error in creating or getting a store named myDBStore2: rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}  
					
					if (s == os) {
						printStringLn("s = " + (rstring)s + ", os = " + (rstring)os + 
							". Two consecutive dpsCreateOrGetStore calls for the same store (myDBStore2) correctly returned the same store id.");
					} else {
						printStringLn("Unexpected error: s = " + (rstring)s + ", os = " + (rstring)os + 
							". Two consecutive dpsCreateOrGetStore calls for the same store (myDBStore2) incorrectly returned different store ids.");
					}
					
                    assert(s==os && err==0ul);                     

					_timeNow = getTimestamp();
					_timeInNanoSecondsBeforeExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
                    res = dpsPut(s, "abc", 10, err);
					_timeNow = getTimestamp();
					_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
					_totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
					printStringLn("Time taken for executing dpsPut = " +  (rstring)_totalExecutionTime + " nanosecs");
					
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsPut(s, abc, 10): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}  
					 
                    assert(res==true && err==0ul);                    
                    
                    mutable int32 v = 0;
					_timeNow = getTimestamp();
					_timeInNanoSecondsBeforeExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
                    res = dpsGet(s, "abc", v, err);
					_timeNow = getTimestamp();
					_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
					_totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
					printStringLn("Time taken for executing dpsGet = " +  (rstring)_totalExecutionTime + " nanosecs"); 
					
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsGet(s, abc, v): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}
										
                    assert(res==true && err==0ul); // get has succeeded 
                    printStringLn("v=" + (rstring)v);
                    assert(v==10);
                                        
                    // Update that previously put K/V entry now.
                    dpsPut(s, "abc", 28, err);
                    if (err != 0ul) {
                    	printStringLn("Error in updating the K/V entry dpsPut(s, abc, 28): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
                    }
                    
                    dpsGet(s, "abc", v, err);
                    printStringLn("Updated v=" + (rstring)v);
                    
                    // Let us try putting an entry with a complex value type.
                    // You could simply do this by doing a dpsPut. But, that action will make the store with
                    // mixed typed keys and values which will make it hard for other operators to do useful things with
                    // that store. Hence, we will recreate that store with a new value type.
                    // Remove and create that same store with a different key and value type.
                    dpsRemoveStore(s, err);
                    tuple<boolean fun, list<int32> joy> dummyFunJoyTuple = {};
                    s = dpsCreateOrGetStore("myDBStore3", dummyRstring, dummyFunJoyTuple, err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsCreateOrGetStore('myDBStore3', dummyRstring, dummyFunJoyTuple, err) rc = " + 
							(rstring)dpsGetLastStoreErrorCode() + ", msg = " + dpsGetLastStoreErrorString());
					}

                    // Woo hoo!, we can use any type as value
                    res = dpsPut(s, "abc", {fun=true, joy=[1,2,3]}, err); // replace '10'
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsPut(s, abc, {fun=true, joy=[1,2,3]}): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}                    
                    assert(res==true && err==0ul); // value was replaced, rather than inserted  // <---- Successful value replacement will return true.
                    mutable tuple<boolean fun, list<int32> joy> funJoy = {};
                    res = dpsGet(s, "abc", funJoy, err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsGet(s, abc, funjoy): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					} 
                    assert(res==true && err==0ul); // get has succeeded
                    assert(funJoy=={fun=true,joy=[1,2,3]});

                    // We can check existence, also remove
					_timeNow = getTimestamp();
					_timeInNanoSecondsBeforeExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
                    mutable boolean exists = dpsHas(s, "abc", err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsHas(s): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					} else {
						if (exists == true) {
							printStringLn("K/V pair with a key 'abc' exists as checked by dpsHas(s).");
						} else {
							printStringLn("Unexpected error in dpsHas(s) as it reports that a K/V pair with key 'abc' doesn't exist.");
						}
					}
					_timeNow = getTimestamp();
					_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
					_totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
					printStringLn("Time taken for executing dpsHas = " +  (rstring)_totalExecutionTime + " nanosecs"); 
                    assert(exists && err==0ul);


					_timeNow = getTimestamp();
					_timeInNanoSecondsBeforeExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
                    res = dpsRemove(s, "abc", err);
					_timeNow = getTimestamp();
					_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
					_totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
					printStringLn("Time taken for executing dpsRemove = " +  (rstring)_totalExecutionTime + " nanosecs"); 

					if (err != 0ul) {
						printStringLn("Unexpected error in dpsRemove(s, abc): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					} 

                    assert(res==true && err==0ul); // remove has succeeded 
                    exists = dpsHas(s, "abc", err);
					if (exists == true) {
						printStringLn("Unexpected error: K/V pair with a key 'abc' still exists after it was removed.");
					} else {
						printStringLn("K/V pair with a key 'abc' was successfully removed.");
					}
                    assert(!exists && err==0ul);
                    res = dpsRemove(s, "abc", err);
					if (err != 0ul) {
						printStringLn("Expected error in dpsRemove(s, abc): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}                     
                    assert(res==false && err!=0ul); // remove has failed  // <---- Attempt to remove a non-existing data item will return false and a non-zero return code/msg. 
                        
                    // Woo hoo!, we can use any type as key.
                    // As a good practice, we will create a new store with a new key spl data type.
                    dpsRemoveStore(s, err);
                    set<int32> dummyInt32Set = {0};
                    s = dpsCreateOrGetStore("myDBStore4", dummyInt32Set, dummyInt32, err);
                    res = dpsPut(s, {3, 5, 6}, 10, err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsput(s, {3,5,6}, 10): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					} 
                    assert(res==true && err==0ul); // value was inserted
                    
					// Update the previously put K/V entry now.                    
                    res = dpsPut(s, {3, 5, 6}, 11, err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsput(s, {3,5,6}, 11): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}                   
                    assert(res==true && err==0ul); // value was replaced // <---- Successful value replacement will return true with a zero error code.
                    res = dpsGet(s, {3, 5, 6}, v, err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsGet(s, {3,5,6}, 10): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}                     
                    assert(res==true && err==0ul); // get has succeeded 
                    assert(v==11); // prints '11'
 
                    // clear all contents
					_timeNow = getTimestamp();
					_timeInNanoSecondsBeforeExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
                    dpsClear(s, err);
					_timeNow = getTimestamp();
					_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
					_totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
					printStringLn("Time taken for executing dpsClear = " +  (rstring)_totalExecutionTime + " nanosecs");

					if (err != 0ul) {
						printStringLn("Unexpected error in dpsClear(s): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					} 					
                    assert(err==0ul);
                    mutable uint64 size = dpsSize(s, err);
                    
                    if (err != 0ul) {
                    	printStringLn("Unexpected error in dpsSize(myDBStore4): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}
                    
                    assert(size==0ul && err==0ul);

					dpsRemoveStore(s, err);
					// Create a new store with a new data type for key and value.
					s = dpsCreateOrGetStore("myDBStore5", dummyRstring, dummyInt32, err);

					_timeNow = getTimestamp();
					_timeInNanoSecondsBeforeExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
                    dpsPut(s, "a", 1, err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsput(s, a, 1): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}                     
                    dpsPut(s, "b", 2, err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsput(s, b, 11): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}                     
                    dpsPut(s, "c", 3, err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsput(s, c, 3): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}                     
                    dpsPut(s, "d", 4, err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsput(s, d, 4): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}                     
					_timeNow = getTimestamp();
					_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
					_totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
					printStringLn("Time taken for executing dpsPut 4 times in a sequence = " +  (rstring)_totalExecutionTime + " nanosecs"); 

					_timeNow = getTimestamp();
					_timeInNanoSecondsBeforeExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
                    size = dpsSize(s, err);
					_timeNow = getTimestamp();
					_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
					_totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
					printStringLn("Time taken for executing dpsSize = " +  (rstring)_totalExecutionTime + " nanosecs");

					if (err != 0ul) {
						printStringLn("Unexpected error in dpsSize(s): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					} else {
						printStringLn("Size of the store 'myDBStore5' is " + (rstring)size);
					}
                    assert(size==4ul && err==0ul);
 
                    dpsRemoveStore(s, err);
 
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsRemoveStore(s): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}                     
                    assert(err==0ul);
                    
                    // Try to store a data item in an invalid store.
                    // CAUTION: Regular and a faster version of dpsPut will simply create an incorrect store structure when an actual store doesn't exist.
                    // Because, faster version of dpsPut doesn't do any safety checks to validate the store existence.
                    // Hence, do this particular test ONLY with the dpsPutSafe API which will work correctly.
                    // If users call dpsPut (faster version) on a non-existing store, that will surely cause all kinds of issues in the
                    // back-end data store by creating invalid store structures thereby producing dangling stores. Users should take proper care
                    // and call the faster version of the dpsPut API only on existing stores. If they ignore this rule, then the back-end data store
                    // will be in a big mess.
                    res = dpsPutSafe(s, 345, "789", err);
                    
					if (err != 0ul) {
						printStringLn("Expected error in dpsPutSafe(s, 345, 789): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}                    
                    assert(res==false && err!=0ul);

                    // Let us create nine stores now with different combintations of key and value types.
                    uint64 s1 = dpsCreateOrGetStore("Red", dummyInt32, dummyRstring, err);
                    uint64 s2 = dpsCreateOrGetStore("Green", dummyRstring, dummyInt32, err);
                    float64 dummyFloat64 = 0.0;
                    uint64 s3 = dpsCreateOrGetStore("Blue", dummyRstring, dummyFloat64, err);
                    uint64 s4 = dpsCreateOrGetStore("Purple", dummyFloat64, dummyRstring, err);
                    list<int32> dummyInt32List = [0];
                    map<rstring, rstring> dummyRStringRStringMap = {"x":"0"};
                    uint64 s5 = dpsCreateOrGetStore("Brown", dummyInt32List, dummyRStringRStringMap, err);
                    uint64 s6 = dpsCreateOrGetStore("Yellow", dummyRstring, dummyFloat64, err);
                    uint64 s7 = dpsCreateOrGetStore("Teal", dummyRstring, dummyRstring, err);
                    
                    dpsPut(s1, 10, "New York", err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsPut(s1, 10, New York): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}                    
                    dpsPut(s2, 'att', 533, err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsPut(s2, att, 533): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}                     
                    dpsPut(s3, "TR", 1.5, err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsPut(s3, TR, 1.5): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}                    
                    dpsPut(s4, 45.47, "Yorktown", err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsPut(s4, 45.47): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}                    
                    dpsPut(s5, [12, 34, 16], {"SWG":"Mills", "Research":"Kelly"}, err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsPut(s5, [12, 34, 16], {SWG:Mills, Research:Kelly}): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}                    
                    dpsPut(s6, "Sprint", 7.6, err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsPut(s6, Sprint, 7.6): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}                    
                    dpsPut(s7, "SPL", "Fantastic", err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsPut(s7, SPL, Fantastic): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}                    

					// Out of those seven stores, only 3 stores will be used in a downstream operator.
					// We can get rid of the rest of the stores.
					// [As of Jan/2015, Couchbase doesn't allow more than 10 stores to be active at any given time.
					//  This limitation is not there in other NoSQL data stores. Hopefully, Couchbase will fix this.
					//  Removing the following stores will help us to complete our tests in Couchbase as well.] 
					dpsRemoveStore(s1, err);
					dpsRemoveStore(s2, err);
					dpsRemoveStore(s3, err);
					dpsRemoveStore(s6, err);

                    size = dpsSize(s4, err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsSize(s4): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}                    
					// CAUTION: In my tests using Couchbase, I noticed the size being returned as 0 even though it should be 1.
                    printStringLn("Size of store id " + (rstring)s4 + " is " + (rstring)size);
                    size = dpsSize(s7, err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsSize(s7): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}                     
                    printStringLn("Size of store id " + (rstring)s7 + " is " + (rstring)size);
					
					// Let us see how we can iterate over the entire store.
					uint64 s8 = dpsCreateOrGetStore("Programming_Languages_Credits", dummyRstring, dummyRstring, err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsCreateOrGetStore(s8): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					} else { 
						// In this operator, we will insert bunch of values.
						// We will show how the next operator can iterate it so easily.
						dpsPut(s8, "Fortran", "John W. Backus", err);
						dpsPut(s8, "C", "Dennis MacAlistair Ritchie", err);
						dpsPut(s8, "C++", "Bjarne Stroustrup", err);
						dpsPut(s8, "Java", "James Arthur Gosling", err);
						dpsPut(s8, "Perl", "Larry Wall", err);
						dpsPut(s8, "PHP", "Rasmus Lerdorf", err);
						dpsPut(s8, "Python", "Guido van Rossum ", err);
						dpsPut(s8, "Ruby", "Yukihiro Matsumoto", err);
						dpsPut(s8, "SPL", "Martin Hirzel, Bugra Gedik", err);
                    }
                    
                    // We are going to create another store that will hold complex types such as tuples.
                    // Then, we will show how the iteration works for such a store holding complex data types.
                    mutable tuple<rstring potusName, rstring spouseName, rstring birthState, 
						rstring orderOfPresidency, int32 yearOfTakingOffice, rstring party> notablePresidents = {};
					uint64 s9 = dpsCreateOrGetStore("notable-commander-in-chiefs", dummyRstring, notablePresidents, err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsCreateOrGetStore(s9): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					} else {
						notablePresidents = {potusName="Abraham Lincoln", spouseName="Mary Todd Lincoln", 
							birthState="Kentucky", orderOfPresidency="16th", yearOfTakingOffice=1861, party="Republican"};
						dpsPut(s9, "Lincoln", notablePresidents, err);
						notablePresidents = {potusName="Theodore Roosevelt", spouseName="Edith Roosevelt", 
							birthState="New York", orderOfPresidency="26th", yearOfTakingOffice=1901, party="Republican"};
						dpsPut(s9, "Roosevelt", notablePresidents, err);
						notablePresidents = {potusName="Woodrow Wilson", spouseName="Edith Wilson", 
							birthState="Virginia", orderOfPresidency="28th", yearOfTakingOffice=1913, party="Democratic"};
						dpsPut(s9, "Wilson", notablePresidents, err);
						notablePresidents = {potusName="Franklin D. Roosevelt", spouseName="Eleanor Roosevelt", 
							birthState="New York", orderOfPresidency="32nd", yearOfTakingOffice=1933, party="Democratic"};
						dpsPut(s9, "FDR", notablePresidents, err);
						notablePresidents = {potusName="John F. Kennedy", spouseName="Jacqueline Kennedy Onassis", 
							birthState="Massachusetts", orderOfPresidency="35th", yearOfTakingOffice=1961, party="Democratic"};
						dpsPut(s9, "JFK", notablePresidents, err);
						notablePresidents = {potusName="Richard Nixon", spouseName="Pat Ryan Nixon", 
							birthState="California", orderOfPresidency="37th", yearOfTakingOffice=1969, party="Republican"};
						dpsPut(s9, "Nixon", notablePresidents, err);
						notablePresidents = {potusName="Ronald Reagan", spouseName="Nancy Reagan", 
							birthState="Illinois", orderOfPresidency="40th", yearOfTakingOffice=1981, party="Republican"};
						dpsPut(s9, "Reagan", notablePresidents, err);
						notablePresidents = {potusName="Bill Clinton", spouseName="Hillary Clinton", 
							birthState="Arkansas", orderOfPresidency="42nd", yearOfTakingOffice=1993, party="Democratic"};
						dpsPut(s9, "Clinton", notablePresidents, err);
						notablePresidents = {potusName="George W. Bush", spouseName="Laura Bush", 
							birthState="Connecticut", orderOfPresidency="43rd", yearOfTakingOffice=2001, party="Republican"};
						dpsPut(s9, "Bush", notablePresidents, err);					
						notablePresidents = {potusName="Barrack Obama", spouseName="Michelle Obama", 
							birthState="Hawaii", orderOfPresidency="44th", yearOfTakingOffice=2009, party="Democratic"};
						dpsPut(s9, "Obama", notablePresidents, err);
						
						// Let us read the metdata entries for this newly created store.
						printStringLn("Metadata 1: Original name of a store with an id " + (rstring)s9 + " is '" +  dpsGetStoreName(s9) + "'");
						printStringLn("Metadata 2: SPL type name for the key of a store with an id " + (rstring)s9 + " is '" +  dpsGetSplTypeNameForKey(s9) + "'");
						printStringLn("Metadata 3: SPL type name for the value of a store with an id " + (rstring)s9 + " is '" +  dpsGetSplTypeNameForValue(s9) + "'");
					}				
					
					// We will do one more thing about the dps iteration capabilities.
					// Then, we will move on to something totally different.
					// How about iterating a store that has keys other than the usual string types?
					// Something more exotic, may be a map data type as a store key?
					// Let us form travel quiz questions to identify the city of certain famous world attractions.
					// Then, we will save them in our own store. As we have done above,
					// we will let the downstream operator do the job of iterating over this store.
					s = dpsCreateOrGetStore("Got_Travel_Quiz_Ideas?", dummyRStringRStringMap, dummyRstring, err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsCreateOrGetStore(s): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					} else {
						// Map Key: Attraction name, Country name
						// Map Value: City name
						dpsPut(s, {"Anitkabir": "Turkey"}, "Ankara", err);
						dpsPut(s, {"Taj Mahal": "India"}, "Agra", err);
						dpsPut(s, {"Big Ben": "United Kingdom"}, "London", err);
						dpsPut(s, {"Temple of Kukulkan": "Mexico"}, "Chichen Itza", err);
						dpsPut(s, {"Mount Rushmore": "USA"}, "Keystone, SD", err);
						dpsPut(s, {"Forbidden City": "China"}, "Beijing", err);
						dpsPut(s, {"Great Pyramid of Giza": "Egypt"}, "Cairo", err);
						dpsPut(s, {"Acropolis": "Greece"}, "Athens", err);
						dpsPut(s, {"Frauenkirche": "Germany"}, "Dresden", err);
						dpsPut(s, {"Golden Pavilion": "Japan"}, "Kyoto", err);
					}
		
					// Let us display the meta data entries for this store.
					printStringLn("Metadata 1: Original name of a store with an id " + (rstring)s + " is '" +  dpsGetStoreName(s) + "'");
					printStringLn("Metadata 2: SPL type name for the key of a store with an id " + (rstring)s + " is '" +  dpsGetSplTypeNameForKey(s) + "'");
					printStringLn("Metadata 3: SPL type name for the value of a store with an id " + (rstring)s + " is '" +  dpsGetSplTypeNameForValue(s) + "'");
					
					// We have a final feature of the dps to show here.
					// dps allows us to serialize a store into a binary blob.
					// Then after a while, we can deserialize that binary blob into an existing or a brand new store.
					// Let us create a new store for ZipCode to "Town and State" lookup.
					mutable blob sData = [];
					s = dpsCreateOrGetStore("Zip_Code_Lookup_ABC", dummyRstring, dummyRstringList, err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsCreateOrGetStore(Zip_Code_Lookup_ABC): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					} else {					
						// Let us add a few entries into our store.
						dpsPut(s, "10514", ["Chappaqua", "New York"], err);
						dpsPut(s, "10598", ["Yorktown Heights", "New York"], err);
						dpsPut(s, "10801", ["New Rochelle", "New York"], err);
						dpsPut(s, "10541", ["Mahopac", "New York"], err);
						dpsPut(s, "10562", ["Ossining", "New York"], err);
						dpsPut(s, "10549", ["Mount Kisco", "New York"], err);
						dpsPut(s, "10506", ["White Plains", "New York"], err);
						dpsPut(s, "10526", ["Goldens Bridge", "New York"], err);
						dpsPut(s, "11577", ["Roslyn Heights", "New York"], err);
						dpsPut(s, "10532", ["Hawthorne", "New York"], err);
						// We can serialize this entire store into a blob in just one native function call.
						// You have to pass a dummy key and a dummy value to indicate the 
						// types used for the keys and values in your store. 
						dpsSerialize(s, sData, dummyRstring, dummyRstringList, err);
						if (err != 0ul) {
							printStringLn("Unexpected error in dpsSerialize(s, sData, dummyRstring, dummyRstringList): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
						}
						
						// Since we serialized the entire store into a blob, we can get rid of this store.
						dpsRemoveStore(s, err);
					}
					
					// We are going to create a new store and use the blob data
					// to deserialize it for populating the new store's contents.
					s = dpsCreateOrGetStore("Zip_Code_Lookup_XYZ", dummyRstring, dummyRstringList, err);
					if (err != 0ul) {
						printStringLn("Unexpected error in dpsCreateOrGetStore(Zip_Code_Lookup_XYZ): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					} else {
						// Define a dummy key and a dummy value as type indicators.					
						// From the blob data we made above, populate the new store we created just now.
						dpsDeserialize(s, sData, dummyRstring, dummyRstringList, err);
						if (err != 0ul) {
							printStringLn("Unexpected error in dpsDeserialize(s, sData, key, value): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
						} else {
							// We populated the entire store through deserialization of the blob data.
							// This is so cool.
							// Let us iterate through this new store and see its contents.
							printStringLn("Contents of a store named 'Zip_Code_Lookup_XYZ' that was populated via dpsDeserialize:");
							uint64 it = dpsBeginIteration(s, err); 
							mutable rstring key = "";
							mutable list<rstring> value = [];
							
							while (dpsGetNext(s, it, key, value, err)) {
								printStringLn("'" + (rstring)key + "' => " + (rstring)value);
							}
							
							dpsEndIteration(s, it, err);
							// Get rid of this store.
							dpsRemoveStore(s, err);
						}
					}

                    // Signal the next operator to read and write using the two presidential stores we created above.
                    mutable NextBeat _beat = {};
                    submit(_beat, NextBeat);
				}
			}

			// =========================  This operator shows how we can access the two stores created by the previous operator. =========================
			// This operator runs on its own PE.
			() as Sink2 = Custom(NextBeat) {
				logic
					onTuple NextBeat: {
						mutable uint64 s4 = 0ul, s5 = 0ul, s7 = 0ul, s8 = 0ul, s9 = 0ul, size = 0ul, err = 0ul;
						mutable boolean res = false;
						s5 = dpsFindStore("Brown", err);
						if (err != 0ul) {
							printStringLn("Unexpected error in dpsFindStore(Brown): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
								", msg = " + dpsGetLastStoreErrorString());
						}   
						assert(s5!=0ul && err==0ul);
						float64 dummyFloat64 = 0.0;
						rstring dummyRstring = "0";
						s4 = dpsCreateOrGetStore("Purple", dummyFloat64, dummyRstring, err);
						if (err != 0ul) {
							printStringLn("Unexpected error in dpsCreateOrGetStore(Purple): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
								", msg = " + dpsGetLastStoreErrorString());
						}
						assert(s4!=0ul && err==0ul);
	                    mutable map<rstring, rstring> myMap = {};
	                    dpsGet(s5, [12, 34, 16], myMap, err);
						if (err != 0ul) {
							printStringLn("Unexpected error in dpsGet(s5, [12, 34, 16], myMap): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
								", msg = " + dpsGetLastStoreErrorString());
						}	 
						// Get rid of store 5
						dpsRemoveStore(s5, err);
	                    printStringLn("myMap = " + (rstring)myMap);
	                    mutable rstring myLab = "";
	                    dpsGet(s4, 45.47, myLab, err);
						if (err != 0ul) {
							printStringLn("Unexpected error in dpsGet(s4, 45.47, myLab): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
								", msg = " + dpsGetLastStoreErrorString());
						}	            
	                    printStringLn("myLab = " + myLab);
	                    s7 = dpsCreateOrGetStore("Teal", dummyRstring, dummyRstring, err);
	                    mutable rstring quality = "";
	                    dpsGet(s7, "SPL", quality, err);
						if (err != 0ul) {
							printStringLn("Unexpected error in dpsGet(s7, SPL, quality): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
								", msg = " + dpsGetLastStoreErrorString());
						}	                   
	                    printStringLn("SPL is " + quality);
	                    // We are using here a data item key with spaces in it.
	                    dpsPut(s7, "Prestigious place in IBM", "T.J.Watson Research Center", err);
						if (err != 0ul) {
							printStringLn("Unexpected error in dpsPut(s7, Prestigious place in IBM, T.J.Watson Research Center): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
								", msg = " + dpsGetLastStoreErrorString());
						}
	                    // Read it back.
	                    mutable rstring prestigiousPlace = "";
	                    dpsGet(s7, "Prestigious place in IBM", prestigiousPlace, err);
						if (err != 0ul) {
							printStringLn("Unexpected error in dpsGet(s, Prestigious place in IBM, prestigiousPlace): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
								", msg = " + dpsGetLastStoreErrorString());
						}	                    
	                    printStringLn("Prestigious place in IBM = " + prestigiousPlace);
	                    dpsClear(s7, err);
						if (err != 0ul) {
							printStringLn("Unexpected error in dpsClear(s7): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
								", msg = " + dpsGetLastStoreErrorString());
						}
	                    size = dpsSize(s7, err);
						if (err != 0ul) {
							printStringLn("Unexpected error in dpsSize(s7): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
								", msg = " + dpsGetLastStoreErrorString());
						}	    
	                    printStringLn("Size of a fully emptied store id " + (rstring)s7 + " is " + (rstring)size);
	                    
	                    // Put and get an empty string as a value and see if it works.
	                    dpsPut(s7, "Empty Data Item", "", err);
						if (err != 0ul) {
							printStringLn("Unexpected error in dpsPut(s7, Empty Data Item, ''): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
								", msg = " + dpsGetLastStoreErrorString());
						}	                    
	                    mutable rstring tmpString = "Babe Ruth";
	                    res = dpsGet(s7, "Empty Data Item", tmpString, err);
						if (err != 0ul) {
							printStringLn("Unexpected error in dpsGet(s7, Empty Data Item, tmpString): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
								", msg = " + dpsGetLastStoreErrorString());
						}	                  
	                    assert(res==true && err==0ul && tmpString=="");

						printStringLn("Our SPL variable originally had a value of 'Babe Ruth'." + 
							" After reading an empty data item value from the data store, it now has this value:'" + 
							tmpString + "'");
	                    
	                    dpsRemoveStore(s7, err);
						if (err != 0ul) {
							printStringLn("Unexpected error in dpsRemoveStore(s7): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
								", msg = " + dpsGetLastStoreErrorString());
						}	                    
	                    dpsRemoveStore(s4, err);
						if (err != 0ul) {
							printStringLn("Unexpected error in dpsRemoveStore(s4): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
								", msg = " + dpsGetLastStoreErrorString());
						}	                    
	                    // Try to get a data item from a store that was just removed.
	                    res = dpsGet(s7, "SPL", quality, err);
						if (err != 0ul) {
							printStringLn("Expected error in dpsGet(s7, SPL, quality): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
								", msg = " + dpsGetLastStoreErrorString());
						}	                    
	                    assert(res==false && err!=0ul);
	                    
                    	// We heard a rumor that the previous operator created a store called "Programming_Languages_Credits".
                    	// Let us get a sneak peek into that store using the dps iteration feature.
                    	s8 = dpsFindStore("Programming_Languages_Credits", err);
						if (err != 0ul) {
							printStringLn("Unexpected error in dpsFindStore(Programming_Languages_Credits): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
								", msg = " + dpsGetLastStoreErrorString());
						} else {
							uint64 it = dpsBeginIteration(s8, err);
							mutable rstring key = "";
							mutable rstring value = "";
							
							printStringLn("Contents of a store named 'Programming_Languages_Credits':");
							
							while(dpsGetNext(s8, it, key, value, err)) {
								 printStringLn("'" + key + "' => " + value);
							}
							
							dpsEndIteration(s8, it, err);
							dpsRemoveStore(s8, err);
						}
						
						// It looks like there exists another store named "notable-commander-in-chiefs".
						// That sounds very interesting. Let us browse its contents.
                    	s9 = dpsFindStore("notable-commander-in-chiefs", err);
						if (err != 0ul) {
							printStringLn("Unexpected error in dpsFindStore(notable-commander-in-chiefs): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
								", msg = " + dpsGetLastStoreErrorString());
						} else {
							uint64 it = dpsBeginIteration(s9, err);
							mutable rstring key = "";
							mutable tuple<rstring potusName, rstring spouseName, rstring birthState, 
								rstring orderOfPresidency, int32 yearOfTakingOffice, rstring party> value = {};
							
							printStringLn("Contents of a store named 'notable-commander-in-chiefs':");
							
							while(dpsGetNext(s9, it, key, value, err)) {
								 printStringLn("'" + key + "' => " + (rstring)value);
							}
							
							dpsEndIteration(s9, it, err);
							dpsRemoveStore(s9, err);
						}
						
						// Finally, we will see how we can do an iteration of a store that uses
						// non-string typed data item keys instead of the mundane string-based keys.
						// Like before, our upstream operator created a store called "Got_Travel_Quiz_Ideas?".
						// Let us learn about some new travel places that we probably have never been to in our life.
						uint64 s = dpsFindStore("Got_Travel_Quiz_Ideas?", err);
						if (err != 0ul) {
							printStringLn("Unexpected error in dpsFindStore(Got_Travel_Quiz_Ideas?): rc = " + (rstring)dpsGetLastStoreErrorCode() + 
								", msg = " + dpsGetLastStoreErrorString());
						} else {
							uint64 it = dpsBeginIteration(s, err);
							mutable map<rstring, rstring> key = {"": ""};
							mutable rstring value = "";
							
							printStringLn("Contents of a store named 'Got_Travel_Quiz_Ideas?':");
							
							while(dpsGetNext(s, it, key, value, err)) {
								 printStringLn("'" + (rstring)key + "' => " + value);
							}
							
							dpsEndIteration(s, it, err);
							dpsRemoveStore(s, err);
						}
						
	                    printStringLn("All the DPS operations worked fine with correct assertions.");
                    }                     
            }

// =========================  Following operators will bombard memcached (OR) redis (OR) Cassandra (OR) Cloudant (OR) HBase (OR) Mongo (OR) Couchbase (OR) Aerospike servers to insert a total of one million or more data items. =========================
// Following block of code will require reasonably powerful server(s) with multiple CPU cores.
// Because, this block of code will add many more PEs to this application topology.
// Hence, this block of code is commented out by default.
// If you want to do a parallel access load test of our dps, you can uncomment the entire block below.
// If you don't have enough number of CPU cores, you can simply change the $numClients and $numDataItems
// below to a much smaller number such that it will work in your environment.
// Main idea of this test is to exercise a heavy load of K/V put and get requests and 
// see how far the back-end data store will scale in terms of throughput and latency.
//
// Please be aware that such load tests from many clients may take a long time when using
// data stores such as Cassandra, Cloudant etc. So, use your judgment about running these
// heavy weight tests based on the choice you made about the back-end data store product. 
//
/*

 


        	(stream<parallelLoadTestResults> DataItemInserter1; stream<Beat> SignalReader1) = Custom(NextBeat) {
 				logic
					onTuple NextBeat: {
						mutable uint64 err = 0ul;
						mutable boolean res = false;
						mutable int32 error_cnt = 0;

						rstring startTime = ctime(getTimestamp());
						// Let us insert 100K unique K/V entries in the global area of our back-end data store and time it.
						mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
						mutable int64 _timeInNanoSecondsAfterExecution = 0l;
						mutable timestamp _timeNow = getTimestamp();
						_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int32 _cnt = 0;
						
						while((isShutdown() == false) && (++_cnt <= 100000)) {
							// Add the host name, writer PE number ($cnt), and the local count (_cnt) to make it a unique string.
							// This will give us key and value strings that are roughly 100 bytes long each.
                            rstring myKey = "This is the time for all the good men and women to come to the aid of our nation." + 
                            	" (Your-Machine-Name1_1_" + (rstring)_cnt + ")";
                            rstring myValue = myKey;
                            // We will use the TTL based put with a TTL value of 305 seconds so that these data items will be 
                            // automatically removed after 5 minutes.
							res = dpsPutTTL(myKey, myValue, 305u, err);
							
							if (res == false && err != 0ul) {
								printStringLn("Unexpected error in dpsPutTTL(myKey, myValue, 0u): rc = " + (rstring)dpsGetLastErrorCodeTTL() + 
									", msg = " + dpsGetLastErrorStringTTL());
								error_cnt++;
							}
						}
						
						_timeNow = getTimestamp();
						_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
						
						// Signal the next operator now to do 100K reads.
						mutable Beat beat = {};
						submit(beat, SignalReader1);
	
						// We will report it to a result collector.												
						mutable parallelLoadTestResults pltr = {};
						pltr.dpsTask = "Insert data item";
						pltr.clientId = (int32)1;
						pltr.startTime = startTime;
						pltr.endTime = ctime(_timeNow);
						pltr.elapsedTime = _totalExecutionTime;
						pltr.errorCnt = error_cnt;
						submit(pltr, DataItemInserter1);
					}					       	

                    config
                       placement:host("Your-Machine-Name1");
        	}    
            
            // Inside this operator (placed on its own PE), we will do 100K reads from the global area of our back-end data store.
			stream<parallelLoadTestResults> DataItemReader1 = Custom(SignalReader1 as SR) {
				logic
					onTuple SR: {
						mutable uint64 err = 0ul;
						mutable boolean res = false;
						mutable int32 error_cnt = 0;
						
						rstring startTime = ctime(getTimestamp());
						// Let us read 100K unique K/V entries from the global area of our data store and time it.
						mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
						mutable int64 _timeInNanoSecondsAfterExecution = 0l;
						mutable timestamp _timeNow = getTimestamp();
						_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable rstring myStringKey = "";
						mutable rstring myStringValue = "";
                        mutable int32 _cnt = 0;
						
						while((isShutdown() == false) && (++_cnt <= 100000)) {
							// Add the host name, writer PE number ($cnt), and the local count (_cnt) to make it a unique string.
							// This will give us key and value strings that are roughly 100 bytes long each.
                            myStringKey = "This is the time for all the good men and women to come to the aid of our nation." + 
                            	" (Your-Machine-Name1_1_" + (rstring)_cnt + ")";
                            myStringValue = "";	
                            // We will use the TTL based get. Our K/V entries are set to be purged automatically after 3 minutes.
							res = dpsGetTTL(myStringKey, myStringValue, err);
							
							if (res == false && err != 0ul) {
								printStringLn("Unexpected error in dpsGetTTL(myStringKey, myStringValue): rc = " + (rstring)dpsGetLastErrorCodeTTL() + 
									", msg = " + dpsGetLastErrorStringTTL());
								error_cnt++;
							}
							
							// Verify what was written and read back from the cache is correct.
							if (myStringKey != myStringValue) {
								printStringLn("Unexpected K/V verification error in dpsGetTTL(myStringKey, myStringValue): myStringKey = " + myStringKey +
									", myStringValue = " + myStringValue);
							}
						}
						
						_timeNow = getTimestamp();
						_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
						
						// We will report it to a result collector.												
						mutable parallelLoadTestResults pltr = {};
						pltr.dpsTask = "Read data item";
						pltr.clientId = 1;
						pltr.startTime = startTime;
						pltr.endTime = ctime(_timeNow);
						pltr.elapsedTime = _totalExecutionTime;
						pltr.errorCnt = error_cnt;
						submit(pltr, DataItemReader1);
					}

					config
						placement:host("Your-Machine-Name1");					
			}
			

        	(stream<parallelLoadTestResults> DataItemInserter2; stream<Beat> SignalReader2) = Custom(NextBeat) {
 				logic
					onTuple NextBeat: {
						mutable uint64 err = 0ul;
						mutable boolean res = false;
						mutable int32 error_cnt = 0;

						rstring startTime = ctime(getTimestamp());
						// Let us insert 100K unique K/V entries in the global area of our back-end data store and time it.
						mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
						mutable int64 _timeInNanoSecondsAfterExecution = 0l;
						mutable timestamp _timeNow = getTimestamp();
						_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int32 _cnt = 0;
						
						while((isShutdown() == false) && (++_cnt <= 100000)) {
							// Add the host name, writer PE number ($cnt), and the local count (_cnt) to make it a unique string.
							// This will give us key and value strings that are roughly 100 bytes long each.
                            rstring myKey = "This is the time for all the good men and women to come to the aid of our nation." + 
                            	" (Your-Machine-Name1_2_" + (rstring)_cnt + ")";
                            rstring myValue = myKey;
                            // We will use the TTL based put with a TTL value of 305 seconds so that these data items will be 
                            // automatically removed after 5 minutes.
							res = dpsPutTTL(myKey, myValue, 305u, err);
							
							if (res == false && err != 0ul) {
								printStringLn("Unexpected error in dpsPutTTL(myKey, myValue, 0u): rc = " + (rstring)dpsGetLastErrorCodeTTL() + 
									", msg = " + dpsGetLastErrorStringTTL());
								error_cnt++;
							}
						}
						
						_timeNow = getTimestamp();
						_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
						
						// Signal the next operator now to do 100K reads.
						mutable Beat beat = {};
						submit(beat, SignalReader2);
	
						// We will report it to a result collector.												
						mutable parallelLoadTestResults pltr = {};
						pltr.dpsTask = "Insert data item";
						pltr.clientId = (int32)2;
						pltr.startTime = startTime;
						pltr.endTime = ctime(_timeNow);
						pltr.elapsedTime = _totalExecutionTime;
						pltr.errorCnt = error_cnt;
						submit(pltr, DataItemInserter2);
					}					       	

                    config
                       placement:host("Your-Machine-Name1");
        	}    
            
            // Inside this operator (placed on its own PE), we will do 100K reads from the global area of our back-end data store.
			stream<parallelLoadTestResults> DataItemReader2 = Custom(SignalReader2 as SR) {
				logic
					onTuple SR: {
						mutable uint64 err = 0ul;
						mutable boolean res = false;
						mutable int32 error_cnt = 0;
						
						rstring startTime = ctime(getTimestamp());
						// Let us read 100K unique K/V entries from the global area of our data store and time it.
						mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
						mutable int64 _timeInNanoSecondsAfterExecution = 0l;
						mutable timestamp _timeNow = getTimestamp();
						_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable rstring myStringKey = "";
						mutable rstring myStringValue = "";
                        mutable int32 _cnt = 0;
						
						while((isShutdown() == false) && (++_cnt <= 100000)) {
							// Add the host name, writer PE number ($cnt), and the local count (_cnt) to make it a unique string.
							// This will give us key and value strings that are roughly 100 bytes long each.
                            myStringKey = "This is the time for all the good men and women to come to the aid of our nation." + 
                            	" (Your-Machine-Name1_2_" + (rstring)_cnt + ")";
                            myStringValue = "";	
                            // We will use the TTL based get. Our K/V entries are set to be purged automatically after 3 minutes.
							res = dpsGetTTL(myStringKey, myStringValue, err);
							
							if (res == false && err != 0ul) {
								printStringLn("Unexpected error in dpsGetTTL(myStringKey, myStringValue): rc = " + (rstring)dpsGetLastErrorCodeTTL() + 
									", msg = " + dpsGetLastErrorStringTTL());
								error_cnt++;
							}
							
							// Verify what was written and read back from the cache is correct.
							if (myStringKey != myStringValue) {
								printStringLn("Unexpected K/V verification error in dpsGetTTL(myStringKey, myStringValue): myStringKey = " + myStringKey +
									", myStringValue = " + myStringValue);
							}
						}
						
						_timeNow = getTimestamp();
						_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
						
						// We will report it to a result collector.												
						mutable parallelLoadTestResults pltr = {};
						pltr.dpsTask = "Read data item";
						pltr.clientId = 2;
						pltr.startTime = startTime;
						pltr.endTime = ctime(_timeNow);
						pltr.elapsedTime = _totalExecutionTime;
						pltr.errorCnt = error_cnt;
						submit(pltr, DataItemReader2);
					}

					config
						placement:host("Your-Machine-Name1");					
			}
			

        	(stream<parallelLoadTestResults> DataItemInserter3; stream<Beat> SignalReader3) = Custom(NextBeat) {
 				logic
					onTuple NextBeat: {
						mutable uint64 err = 0ul;
						mutable boolean res = false;
						mutable int32 error_cnt = 0;

						rstring startTime = ctime(getTimestamp());
						// Let us insert 100K unique K/V entries in the global area of our back-end data store and time it.
						mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
						mutable int64 _timeInNanoSecondsAfterExecution = 0l;
						mutable timestamp _timeNow = getTimestamp();
						_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int32 _cnt = 0;
						
						while((isShutdown() == false) && (++_cnt <= 100000)) {
							// Add the host name, writer PE number ($cnt), and the local count (_cnt) to make it a unique string.
							// This will give us key and value strings that are roughly 100 bytes long each.
                            rstring myKey = "This is the time for all the good men and women to come to the aid of our nation." + 
                            	" (Your-Machine-Name1_3_" + (rstring)_cnt + ")";
                            rstring myValue = myKey;
                            // We will use the TTL based put with a TTL value of 305 seconds so that these data items will be 
                            // automatically removed after 5 minutes.
							res = dpsPutTTL(myKey, myValue, 305u, err);
							
							if (res == false && err != 0ul) {
								printStringLn("Unexpected error in dpsPutTTL(myKey, myValue, 0u): rc = " + (rstring)dpsGetLastErrorCodeTTL() + 
									", msg = " + dpsGetLastErrorStringTTL());
								error_cnt++;
							}
						}
						
						_timeNow = getTimestamp();
						_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
						
						// Signal the next operator now to do 100K reads.
						mutable Beat beat = {};
						submit(beat, SignalReader3);
	
						// We will report it to a result collector.												
						mutable parallelLoadTestResults pltr = {};
						pltr.dpsTask = "Insert data item";
						pltr.clientId = (int32)3;
						pltr.startTime = startTime;
						pltr.endTime = ctime(_timeNow);
						pltr.elapsedTime = _totalExecutionTime;
						pltr.errorCnt = error_cnt;
						submit(pltr, DataItemInserter3);
					}					       	

                    config
                       placement:host("Your-Machine-Name1");
        	}    
            
            // Inside this operator (placed on its own PE), we will do 100K reads from the global area of our back-end data store.
			stream<parallelLoadTestResults> DataItemReader3 = Custom(SignalReader3 as SR) {
				logic
					onTuple SR: {
						mutable uint64 err = 0ul;
						mutable boolean res = false;
						mutable int32 error_cnt = 0;
						
						rstring startTime = ctime(getTimestamp());
						// Let us read 100K unique K/V entries from the global area of our data store and time it.
						mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
						mutable int64 _timeInNanoSecondsAfterExecution = 0l;
						mutable timestamp _timeNow = getTimestamp();
						_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable rstring myStringKey = "";
						mutable rstring myStringValue = "";
                        mutable int32 _cnt = 0;
						
						while((isShutdown() == false) && (++_cnt <= 100000)) {
							// Add the host name, writer PE number ($cnt), and the local count (_cnt) to make it a unique string.
							// This will give us key and value strings that are roughly 100 bytes long each.
                            myStringKey = "This is the time for all the good men and women to come to the aid of our nation." + 
                            	" (Your-Machine-Name1_3_" + (rstring)_cnt + ")";
                            myStringValue = "";	
                            // We will use the TTL based get. Our K/V entries are set to be purged automatically after 3 minutes.
							res = dpsGetTTL(myStringKey, myStringValue, err);
							
							if (res == false && err != 0ul) {
								printStringLn("Unexpected error in dpsGetTTL(myStringKey, myStringValue): rc = " + (rstring)dpsGetLastErrorCodeTTL() + 
									", msg = " + dpsGetLastErrorStringTTL());
								error_cnt++;
							}
							
							// Verify what was written and read back from the cache is correct.
							if (myStringKey != myStringValue) {
								printStringLn("Unexpected K/V verification error in dpsGetTTL(myStringKey, myStringValue): myStringKey = " + myStringKey +
									", myStringValue = " + myStringValue);
							}
						}
						
						_timeNow = getTimestamp();
						_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
						
						// We will report it to a result collector.												
						mutable parallelLoadTestResults pltr = {};
						pltr.dpsTask = "Read data item";
						pltr.clientId = 3;
						pltr.startTime = startTime;
						pltr.endTime = ctime(_timeNow);
						pltr.elapsedTime = _totalExecutionTime;
						pltr.errorCnt = error_cnt;
						submit(pltr, DataItemReader3);
					}

					config
						placement:host("Your-Machine-Name1");					
			}
			

        	(stream<parallelLoadTestResults> DataItemInserter4; stream<Beat> SignalReader4) = Custom(NextBeat) {
 				logic
					onTuple NextBeat: {
						mutable uint64 err = 0ul;
						mutable boolean res = false;
						mutable int32 error_cnt = 0;

						rstring startTime = ctime(getTimestamp());
						// Let us insert 100K unique K/V entries in the global area of our back-end data store and time it.
						mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
						mutable int64 _timeInNanoSecondsAfterExecution = 0l;
						mutable timestamp _timeNow = getTimestamp();
						_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int32 _cnt = 0;
						
						while((isShutdown() == false) && (++_cnt <= 100000)) {
							// Add the host name, writer PE number ($cnt), and the local count (_cnt) to make it a unique string.
							// This will give us key and value strings that are roughly 100 bytes long each.
                            rstring myKey = "This is the time for all the good men and women to come to the aid of our nation." + 
                            	" (Your-Machine-Name1_4_" + (rstring)_cnt + ")";
                            rstring myValue = myKey;
                            // We will use the TTL based put with a TTL value of 305 seconds so that these data items will be 
                            // automatically removed after 5 minutes.
							res = dpsPutTTL(myKey, myValue, 305u, err);
							
							if (res == false && err != 0ul) {
								printStringLn("Unexpected error in dpsPutTTL(myKey, myValue, 0u): rc = " + (rstring)dpsGetLastErrorCodeTTL() + 
									", msg = " + dpsGetLastErrorStringTTL());
								error_cnt++;
							}
						}
						
						_timeNow = getTimestamp();
						_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
						
						// Signal the next operator now to do 100K reads.
						mutable Beat beat = {};
						submit(beat, SignalReader4);
	
						// We will report it to a result collector.												
						mutable parallelLoadTestResults pltr = {};
						pltr.dpsTask = "Insert data item";
						pltr.clientId = (int32)4;
						pltr.startTime = startTime;
						pltr.endTime = ctime(_timeNow);
						pltr.elapsedTime = _totalExecutionTime;
						pltr.errorCnt = error_cnt;
						submit(pltr, DataItemInserter4);
					}					       	

                    config
                       placement:host("Your-Machine-Name1");
        	}    
            
            // Inside this operator (placed on its own PE), we will do 100K reads from the global area of our back-end data store.
			stream<parallelLoadTestResults> DataItemReader4 = Custom(SignalReader4 as SR) {
				logic
					onTuple SR: {
						mutable uint64 err = 0ul;
						mutable boolean res = false;
						mutable int32 error_cnt = 0;
						
						rstring startTime = ctime(getTimestamp());
						// Let us read 100K unique K/V entries from the global area of our data store and time it.
						mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
						mutable int64 _timeInNanoSecondsAfterExecution = 0l;
						mutable timestamp _timeNow = getTimestamp();
						_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable rstring myStringKey = "";
						mutable rstring myStringValue = "";
                        mutable int32 _cnt = 0;
						
						while((isShutdown() == false) && (++_cnt <= 100000)) {
							// Add the host name, writer PE number ($cnt), and the local count (_cnt) to make it a unique string.
							// This will give us key and value strings that are roughly 100 bytes long each.
                            myStringKey = "This is the time for all the good men and women to come to the aid of our nation." + 
                            	" (Your-Machine-Name1_4_" + (rstring)_cnt + ")";
                            myStringValue = "";	
                            // We will use the TTL based get. Our K/V entries are set to be purged automatically after 3 minutes.
							res = dpsGetTTL(myStringKey, myStringValue, err);
							
							if (res == false && err != 0ul) {
								printStringLn("Unexpected error in dpsGetTTL(myStringKey, myStringValue): rc = " + (rstring)dpsGetLastErrorCodeTTL() + 
									", msg = " + dpsGetLastErrorStringTTL());
								error_cnt++;
							}
							
							// Verify what was written and read back from the cache is correct.
							if (myStringKey != myStringValue) {
								printStringLn("Unexpected K/V verification error in dpsGetTTL(myStringKey, myStringValue): myStringKey = " + myStringKey +
									", myStringValue = " + myStringValue);
							}
						}
						
						_timeNow = getTimestamp();
						_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
						
						// We will report it to a result collector.												
						mutable parallelLoadTestResults pltr = {};
						pltr.dpsTask = "Read data item";
						pltr.clientId = 4;
						pltr.startTime = startTime;
						pltr.endTime = ctime(_timeNow);
						pltr.elapsedTime = _totalExecutionTime;
						pltr.errorCnt = error_cnt;
						submit(pltr, DataItemReader4);
					}

					config
						placement:host("Your-Machine-Name1");					
			}
			

        	(stream<parallelLoadTestResults> DataItemInserter5; stream<Beat> SignalReader5) = Custom(NextBeat) {
 				logic
					onTuple NextBeat: {
						mutable uint64 err = 0ul;
						mutable boolean res = false;
						mutable int32 error_cnt = 0;

						rstring startTime = ctime(getTimestamp());
						// Let us insert 100K unique K/V entries in the global area of our back-end data store and time it.
						mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
						mutable int64 _timeInNanoSecondsAfterExecution = 0l;
						mutable timestamp _timeNow = getTimestamp();
						_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int32 _cnt = 0;
						
						while((isShutdown() == false) && (++_cnt <= 100000)) {
							// Add the host name, writer PE number ($cnt), and the local count (_cnt) to make it a unique string.
							// This will give us key and value strings that are roughly 100 bytes long each.
                            rstring myKey = "This is the time for all the good men and women to come to the aid of our nation." + 
                            	" (Your-Machine-Name1_5_" + (rstring)_cnt + ")";
                            rstring myValue = myKey;
                            // We will use the TTL based put with a TTL value of 305 seconds so that these data items will be 
                            // automatically removed after 5 minutes.
							res = dpsPutTTL(myKey, myValue, 305u, err);
							
							if (res == false && err != 0ul) {
								printStringLn("Unexpected error in dpsPutTTL(myKey, myValue, 0u): rc = " + (rstring)dpsGetLastErrorCodeTTL() + 
									", msg = " + dpsGetLastErrorStringTTL());
								error_cnt++;
							}
						}
						
						_timeNow = getTimestamp();
						_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
						
						// Signal the next operator now to do 100K reads.
						mutable Beat beat = {};
						submit(beat, SignalReader5);
	
						// We will report it to a result collector.												
						mutable parallelLoadTestResults pltr = {};
						pltr.dpsTask = "Insert data item";
						pltr.clientId = (int32)5;
						pltr.startTime = startTime;
						pltr.endTime = ctime(_timeNow);
						pltr.elapsedTime = _totalExecutionTime;
						pltr.errorCnt = error_cnt;
						submit(pltr, DataItemInserter5);
					}					       	

                    config
                       placement:host("Your-Machine-Name1");
        	}    
            
            // Inside this operator (placed on its own PE), we will do 100K reads from the global area of our back-end data store.
			stream<parallelLoadTestResults> DataItemReader5 = Custom(SignalReader5 as SR) {
				logic
					onTuple SR: {
						mutable uint64 err = 0ul;
						mutable boolean res = false;
						mutable int32 error_cnt = 0;
						
						rstring startTime = ctime(getTimestamp());
						// Let us read 100K unique K/V entries from the global area of our data store and time it.
						mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
						mutable int64 _timeInNanoSecondsAfterExecution = 0l;
						mutable timestamp _timeNow = getTimestamp();
						_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable rstring myStringKey = "";
						mutable rstring myStringValue = "";
                        mutable int32 _cnt = 0;
						
						while((isShutdown() == false) && (++_cnt <= 100000)) {
							// Add the host name, writer PE number ($cnt), and the local count (_cnt) to make it a unique string.
							// This will give us key and value strings that are roughly 100 bytes long each.
                            myStringKey = "This is the time for all the good men and women to come to the aid of our nation." + 
                            	" (Your-Machine-Name1_5_" + (rstring)_cnt + ")";
                            myStringValue = "";	
                            // We will use the TTL based get. Our K/V entries are set to be purged automatically after 3 minutes.
							res = dpsGetTTL(myStringKey, myStringValue, err);
							
							if (res == false && err != 0ul) {
								printStringLn("Unexpected error in dpsGetTTL(myStringKey, myStringValue): rc = " + (rstring)dpsGetLastErrorCodeTTL() + 
									", msg = " + dpsGetLastErrorStringTTL());
								error_cnt++;
							}
							
							// Verify what was written and read back from the cache is correct.
							if (myStringKey != myStringValue) {
								printStringLn("Unexpected K/V verification error in dpsGetTTL(myStringKey, myStringValue): myStringKey = " + myStringKey +
									", myStringValue = " + myStringValue);
							}
						}
						
						_timeNow = getTimestamp();
						_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
						
						// We will report it to a result collector.												
						mutable parallelLoadTestResults pltr = {};
						pltr.dpsTask = "Read data item";
						pltr.clientId = 5;
						pltr.startTime = startTime;
						pltr.endTime = ctime(_timeNow);
						pltr.elapsedTime = _totalExecutionTime;
						pltr.errorCnt = error_cnt;
						submit(pltr, DataItemReader5);
					}

					config
						placement:host("Your-Machine-Name1");					
			}
			

        	(stream<parallelLoadTestResults> DataItemInserter6; stream<Beat> SignalReader6) = Custom(NextBeat) {
 				logic
					onTuple NextBeat: {
						mutable uint64 err = 0ul;
						mutable boolean res = false;
						mutable int32 error_cnt = 0;

						rstring startTime = ctime(getTimestamp());
						// Let us insert 100K unique K/V entries in the global area of our back-end data store and time it.
						mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
						mutable int64 _timeInNanoSecondsAfterExecution = 0l;
						mutable timestamp _timeNow = getTimestamp();
						_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int32 _cnt = 0;
						
						while((isShutdown() == false) && (++_cnt <= 100000)) {
							// Add the host name, writer PE number ($cnt), and the local count (_cnt) to make it a unique string.
							// This will give us key and value strings that are roughly 100 bytes long each.
                            rstring myKey = "This is the time for all the good men and women to come to the aid of our nation." + 
                            	" (Your-Machine-Name1_6_" + (rstring)_cnt + ")";
                            rstring myValue = myKey;
                            // We will use the TTL based put with a TTL value of 305 seconds so that these data items will be 
                            // automatically removed after 5 minutes.
							res = dpsPutTTL(myKey, myValue, 305u, err);
							
							if (res == false && err != 0ul) {
								printStringLn("Unexpected error in dpsPutTTL(myKey, myValue, 0u): rc = " + (rstring)dpsGetLastErrorCodeTTL() + 
									", msg = " + dpsGetLastErrorStringTTL());
								error_cnt++;
							}
						}
						
						_timeNow = getTimestamp();
						_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
						
						// Signal the next operator now to do 100K reads.
						mutable Beat beat = {};
						submit(beat, SignalReader6);
	
						// We will report it to a result collector.												
						mutable parallelLoadTestResults pltr = {};
						pltr.dpsTask = "Insert data item";
						pltr.clientId = (int32)6;
						pltr.startTime = startTime;
						pltr.endTime = ctime(_timeNow);
						pltr.elapsedTime = _totalExecutionTime;
						pltr.errorCnt = error_cnt;
						submit(pltr, DataItemInserter6);
					}					       	

                    config
                       placement:host("Your-Machine-Name1");
        	}    
            
            // Inside this operator (placed on its own PE), we will do 100K reads from the global area of our back-end data store.
			stream<parallelLoadTestResults> DataItemReader6 = Custom(SignalReader6 as SR) {
				logic
					onTuple SR: {
						mutable uint64 err = 0ul;
						mutable boolean res = false;
						mutable int32 error_cnt = 0;
						
						rstring startTime = ctime(getTimestamp());
						// Let us read 100K unique K/V entries from the global area of our data store and time it.
						mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
						mutable int64 _timeInNanoSecondsAfterExecution = 0l;
						mutable timestamp _timeNow = getTimestamp();
						_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable rstring myStringKey = "";
						mutable rstring myStringValue = "";
                        mutable int32 _cnt = 0;
						
						while((isShutdown() == false) && (++_cnt <= 100000)) {
							// Add the host name, writer PE number ($cnt), and the local count (_cnt) to make it a unique string.
							// This will give us key and value strings that are roughly 100 bytes long each.
                            myStringKey = "This is the time for all the good men and women to come to the aid of our nation." + 
                            	" (Your-Machine-Name1_6_" + (rstring)_cnt + ")";
                            myStringValue = "";	
                            // We will use the TTL based get. Our K/V entries are set to be purged automatically after 3 minutes.
							res = dpsGetTTL(myStringKey, myStringValue, err);
							
							if (res == false && err != 0ul) {
								printStringLn("Unexpected error in dpsGetTTL(myStringKey, myStringValue): rc = " + (rstring)dpsGetLastErrorCodeTTL() + 
									", msg = " + dpsGetLastErrorStringTTL());
								error_cnt++;
							}
							
							// Verify what was written and read back from the cache is correct.
							if (myStringKey != myStringValue) {
								printStringLn("Unexpected K/V verification error in dpsGetTTL(myStringKey, myStringValue): myStringKey = " + myStringKey +
									", myStringValue = " + myStringValue);
							}
						}
						
						_timeNow = getTimestamp();
						_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
						
						// We will report it to a result collector.												
						mutable parallelLoadTestResults pltr = {};
						pltr.dpsTask = "Read data item";
						pltr.clientId = 6;
						pltr.startTime = startTime;
						pltr.endTime = ctime(_timeNow);
						pltr.elapsedTime = _totalExecutionTime;
						pltr.errorCnt = error_cnt;
						submit(pltr, DataItemReader6);
					}

					config
						placement:host("Your-Machine-Name1");					
			}
			

        	(stream<parallelLoadTestResults> DataItemInserter7; stream<Beat> SignalReader7) = Custom(NextBeat) {
 				logic
					onTuple NextBeat: {
						mutable uint64 err = 0ul;
						mutable boolean res = false;
						mutable int32 error_cnt = 0;

						rstring startTime = ctime(getTimestamp());
						// Let us insert 100K unique K/V entries in the global area of our back-end data store and time it.
						mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
						mutable int64 _timeInNanoSecondsAfterExecution = 0l;
						mutable timestamp _timeNow = getTimestamp();
						_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int32 _cnt = 0;
						
						while((isShutdown() == false) && (++_cnt <= 100000)) {
							// Add the host name, writer PE number ($cnt), and the local count (_cnt) to make it a unique string.
							// This will give us key and value strings that are roughly 100 bytes long each.
                            rstring myKey = "This is the time for all the good men and women to come to the aid of our nation." + 
                            	" (Your-Machine-Name1_7_" + (rstring)_cnt + ")";
                            rstring myValue = myKey;
                            // We will use the TTL based put with a TTL value of 305 seconds so that these data items will be 
                            // automatically removed after 5 minutes.
							res = dpsPutTTL(myKey, myValue, 305u, err);
							
							if (res == false && err != 0ul) {
								printStringLn("Unexpected error in dpsPutTTL(myKey, myValue, 0u): rc = " + (rstring)dpsGetLastErrorCodeTTL() + 
									", msg = " + dpsGetLastErrorStringTTL());
								error_cnt++;
							}
						}
						
						_timeNow = getTimestamp();
						_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
						
						// Signal the next operator now to do 100K reads.
						mutable Beat beat = {};
						submit(beat, SignalReader7);
	
						// We will report it to a result collector.												
						mutable parallelLoadTestResults pltr = {};
						pltr.dpsTask = "Insert data item";
						pltr.clientId = (int32)7;
						pltr.startTime = startTime;
						pltr.endTime = ctime(_timeNow);
						pltr.elapsedTime = _totalExecutionTime;
						pltr.errorCnt = error_cnt;
						submit(pltr, DataItemInserter7);
					}					       	

                    config
                       placement:host("Your-Machine-Name1");
        	}    
            
            // Inside this operator (placed on its own PE), we will do 100K reads from the global area of our back-end data store.
			stream<parallelLoadTestResults> DataItemReader7 = Custom(SignalReader7 as SR) {
				logic
					onTuple SR: {
						mutable uint64 err = 0ul;
						mutable boolean res = false;
						mutable int32 error_cnt = 0;
						
						rstring startTime = ctime(getTimestamp());
						// Let us read 100K unique K/V entries from the global area of our data store and time it.
						mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
						mutable int64 _timeInNanoSecondsAfterExecution = 0l;
						mutable timestamp _timeNow = getTimestamp();
						_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable rstring myStringKey = "";
						mutable rstring myStringValue = "";
                        mutable int32 _cnt = 0;
						
						while((isShutdown() == false) && (++_cnt <= 100000)) {
							// Add the host name, writer PE number ($cnt), and the local count (_cnt) to make it a unique string.
							// This will give us key and value strings that are roughly 100 bytes long each.
                            myStringKey = "This is the time for all the good men and women to come to the aid of our nation." + 
                            	" (Your-Machine-Name1_7_" + (rstring)_cnt + ")";
                            myStringValue = "";	
                            // We will use the TTL based get. Our K/V entries are set to be purged automatically after 3 minutes.
							res = dpsGetTTL(myStringKey, myStringValue, err);
							
							if (res == false && err != 0ul) {
								printStringLn("Unexpected error in dpsGetTTL(myStringKey, myStringValue): rc = " + (rstring)dpsGetLastErrorCodeTTL() + 
									", msg = " + dpsGetLastErrorStringTTL());
								error_cnt++;
							}
							
							// Verify what was written and read back from the cache is correct.
							if (myStringKey != myStringValue) {
								printStringLn("Unexpected K/V verification error in dpsGetTTL(myStringKey, myStringValue): myStringKey = " + myStringKey +
									", myStringValue = " + myStringValue);
							}
						}
						
						_timeNow = getTimestamp();
						_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
						
						// We will report it to a result collector.												
						mutable parallelLoadTestResults pltr = {};
						pltr.dpsTask = "Read data item";
						pltr.clientId = 7;
						pltr.startTime = startTime;
						pltr.endTime = ctime(_timeNow);
						pltr.elapsedTime = _totalExecutionTime;
						pltr.errorCnt = error_cnt;
						submit(pltr, DataItemReader7);
					}

					config
						placement:host("Your-Machine-Name1");					
			}
			

        	(stream<parallelLoadTestResults> DataItemInserter8; stream<Beat> SignalReader8) = Custom(NextBeat) {
 				logic
					onTuple NextBeat: {
						mutable uint64 err = 0ul;
						mutable boolean res = false;
						mutable int32 error_cnt = 0;

						rstring startTime = ctime(getTimestamp());
						// Let us insert 100K unique K/V entries in the global area of our back-end data store and time it.
						mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
						mutable int64 _timeInNanoSecondsAfterExecution = 0l;
						mutable timestamp _timeNow = getTimestamp();
						_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int32 _cnt = 0;
						
						while((isShutdown() == false) && (++_cnt <= 100000)) {
							// Add the host name, writer PE number ($cnt), and the local count (_cnt) to make it a unique string.
							// This will give us key and value strings that are roughly 100 bytes long each.
                            rstring myKey = "This is the time for all the good men and women to come to the aid of our nation." + 
                            	" (Your-Machine-Name1_8_" + (rstring)_cnt + ")";
                            rstring myValue = myKey;
                            // We will use the TTL based put with a TTL value of 305 seconds so that these data items will be 
                            // automatically removed after 5 minutes.
							res = dpsPutTTL(myKey, myValue, 305u, err);
							
							if (res == false && err != 0ul) {
								printStringLn("Unexpected error in dpsPutTTL(myKey, myValue, 0u): rc = " + (rstring)dpsGetLastErrorCodeTTL() + 
									", msg = " + dpsGetLastErrorStringTTL());
								error_cnt++;
							}
						}
						
						_timeNow = getTimestamp();
						_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
						
						// Signal the next operator now to do 100K reads.
						mutable Beat beat = {};
						submit(beat, SignalReader8);
	
						// We will report it to a result collector.												
						mutable parallelLoadTestResults pltr = {};
						pltr.dpsTask = "Insert data item";
						pltr.clientId = (int32)8;
						pltr.startTime = startTime;
						pltr.endTime = ctime(_timeNow);
						pltr.elapsedTime = _totalExecutionTime;
						pltr.errorCnt = error_cnt;
						submit(pltr, DataItemInserter8);
					}					       	

                    config
                       placement:host("Your-Machine-Name1");
        	}    
            
            // Inside this operator (placed on its own PE), we will do 100K reads from the global area of our back-end data store.
			stream<parallelLoadTestResults> DataItemReader8 = Custom(SignalReader8 as SR) {
				logic
					onTuple SR: {
						mutable uint64 err = 0ul;
						mutable boolean res = false;
						mutable int32 error_cnt = 0;
						
						rstring startTime = ctime(getTimestamp());
						// Let us read 100K unique K/V entries from the global area of our data store and time it.
						mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
						mutable int64 _timeInNanoSecondsAfterExecution = 0l;
						mutable timestamp _timeNow = getTimestamp();
						_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable rstring myStringKey = "";
						mutable rstring myStringValue = "";
                        mutable int32 _cnt = 0;
						
						while((isShutdown() == false) && (++_cnt <= 100000)) {
							// Add the host name, writer PE number ($cnt), and the local count (_cnt) to make it a unique string.
							// This will give us key and value strings that are roughly 100 bytes long each.
                            myStringKey = "This is the time for all the good men and women to come to the aid of our nation." + 
                            	" (Your-Machine-Name1_8_" + (rstring)_cnt + ")";
                            myStringValue = "";	
                            // We will use the TTL based get. Our K/V entries are set to be purged automatically after 3 minutes.
							res = dpsGetTTL(myStringKey, myStringValue, err);
							
							if (res == false && err != 0ul) {
								printStringLn("Unexpected error in dpsGetTTL(myStringKey, myStringValue): rc = " + (rstring)dpsGetLastErrorCodeTTL() + 
									", msg = " + dpsGetLastErrorStringTTL());
								error_cnt++;
							}
							
							// Verify what was written and read back from the cache is correct.
							if (myStringKey != myStringValue) {
								printStringLn("Unexpected K/V verification error in dpsGetTTL(myStringKey, myStringValue): myStringKey = " + myStringKey +
									", myStringValue = " + myStringValue);
							}
						}
						
						_timeNow = getTimestamp();
						_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
						
						// We will report it to a result collector.												
						mutable parallelLoadTestResults pltr = {};
						pltr.dpsTask = "Read data item";
						pltr.clientId = 8;
						pltr.startTime = startTime;
						pltr.endTime = ctime(_timeNow);
						pltr.elapsedTime = _totalExecutionTime;
						pltr.errorCnt = error_cnt;
						submit(pltr, DataItemReader8);
					}

					config
						placement:host("Your-Machine-Name1");					
			}
			

        	(stream<parallelLoadTestResults> DataItemInserter9; stream<Beat> SignalReader9) = Custom(NextBeat) {
 				logic
					onTuple NextBeat: {
						mutable uint64 err = 0ul;
						mutable boolean res = false;
						mutable int32 error_cnt = 0;

						rstring startTime = ctime(getTimestamp());
						// Let us insert 100K unique K/V entries in the global area of our back-end data store and time it.
						mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
						mutable int64 _timeInNanoSecondsAfterExecution = 0l;
						mutable timestamp _timeNow = getTimestamp();
						_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int32 _cnt = 0;
						
						while((isShutdown() == false) && (++_cnt <= 100000)) {
							// Add the host name, writer PE number ($cnt), and the local count (_cnt) to make it a unique string.
							// This will give us key and value strings that are roughly 100 bytes long each.
                            rstring myKey = "This is the time for all the good men and women to come to the aid of our nation." + 
                            	" (Your-Machine-Name1_9_" + (rstring)_cnt + ")";
                            rstring myValue = myKey;
                            // We will use the TTL based put with a TTL value of 305 seconds so that these data items will be 
                            // automatically removed after 5 minutes.
							res = dpsPutTTL(myKey, myValue, 305u, err);
							
							if (res == false && err != 0ul) {
								printStringLn("Unexpected error in dpsPutTTL(myKey, myValue, 0u): rc = " + (rstring)dpsGetLastErrorCodeTTL() + 
									", msg = " + dpsGetLastErrorStringTTL());
								error_cnt++;
							}
						}
						
						_timeNow = getTimestamp();
						_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
						
						// Signal the next operator now to do 100K reads.
						mutable Beat beat = {};
						submit(beat, SignalReader9);
	
						// We will report it to a result collector.												
						mutable parallelLoadTestResults pltr = {};
						pltr.dpsTask = "Insert data item";
						pltr.clientId = (int32)9;
						pltr.startTime = startTime;
						pltr.endTime = ctime(_timeNow);
						pltr.elapsedTime = _totalExecutionTime;
						pltr.errorCnt = error_cnt;
						submit(pltr, DataItemInserter9);
					}					       	

                    config
                       placement:host("Your-Machine-Name1");
        	}    
            
            // Inside this operator (placed on its own PE), we will do 100K reads from the global area of our back-end data store.
			stream<parallelLoadTestResults> DataItemReader9 = Custom(SignalReader9 as SR) {
				logic
					onTuple SR: {
						mutable uint64 err = 0ul;
						mutable boolean res = false;
						mutable int32 error_cnt = 0;
						
						rstring startTime = ctime(getTimestamp());
						// Let us read 100K unique K/V entries from the global area of our data store and time it.
						mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
						mutable int64 _timeInNanoSecondsAfterExecution = 0l;
						mutable timestamp _timeNow = getTimestamp();
						_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable rstring myStringKey = "";
						mutable rstring myStringValue = "";
                        mutable int32 _cnt = 0;
						
						while((isShutdown() == false) && (++_cnt <= 100000)) {
							// Add the host name, writer PE number ($cnt), and the local count (_cnt) to make it a unique string.
							// This will give us key and value strings that are roughly 100 bytes long each.
                            myStringKey = "This is the time for all the good men and women to come to the aid of our nation." + 
                            	" (Your-Machine-Name1_9_" + (rstring)_cnt + ")";
                            myStringValue = "";	
                            // We will use the TTL based get. Our K/V entries are set to be purged automatically after 3 minutes.
							res = dpsGetTTL(myStringKey, myStringValue, err);
							
							if (res == false && err != 0ul) {
								printStringLn("Unexpected error in dpsGetTTL(myStringKey, myStringValue): rc = " + (rstring)dpsGetLastErrorCodeTTL() + 
									", msg = " + dpsGetLastErrorStringTTL());
								error_cnt++;
							}
							
							// Verify what was written and read back from the cache is correct.
							if (myStringKey != myStringValue) {
								printStringLn("Unexpected K/V verification error in dpsGetTTL(myStringKey, myStringValue): myStringKey = " + myStringKey +
									", myStringValue = " + myStringValue);
							}
						}
						
						_timeNow = getTimestamp();
						_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
						
						// We will report it to a result collector.												
						mutable parallelLoadTestResults pltr = {};
						pltr.dpsTask = "Read data item";
						pltr.clientId = 9;
						pltr.startTime = startTime;
						pltr.endTime = ctime(_timeNow);
						pltr.elapsedTime = _totalExecutionTime;
						pltr.errorCnt = error_cnt;
						submit(pltr, DataItemReader9);
					}

					config
						placement:host("Your-Machine-Name1");					
			}
			

        	(stream<parallelLoadTestResults> DataItemInserter10; stream<Beat> SignalReader10) = Custom(NextBeat) {
 				logic
					onTuple NextBeat: {
						mutable uint64 err = 0ul;
						mutable boolean res = false;
						mutable int32 error_cnt = 0;

						rstring startTime = ctime(getTimestamp());
						// Let us insert 100K unique K/V entries in the global area of our back-end data store and time it.
						mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
						mutable int64 _timeInNanoSecondsAfterExecution = 0l;
						mutable timestamp _timeNow = getTimestamp();
						_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int32 _cnt = 0;
						
						while((isShutdown() == false) && (++_cnt <= 100000)) {
							// Add the host name, writer PE number ($cnt), and the local count (_cnt) to make it a unique string.
							// This will give us key and value strings that are roughly 100 bytes long each.
                            rstring myKey = "This is the time for all the good men and women to come to the aid of our nation." + 
                            	" (Your-Machine-Name1_10_" + (rstring)_cnt + ")";
                            rstring myValue = myKey;
                            // We will use the TTL based put with a TTL value of 305 seconds so that these data items will be 
                            // automatically removed after 5 minutes.
							res = dpsPutTTL(myKey, myValue, 305u, err);
							
							if (res == false && err != 0ul) {
								printStringLn("Unexpected error in dpsPutTTL(myKey, myValue, 0u): rc = " + (rstring)dpsGetLastErrorCodeTTL() + 
									", msg = " + dpsGetLastErrorStringTTL());
								error_cnt++;
							}
						}
						
						_timeNow = getTimestamp();
						_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
						
						// Signal the next operator now to do 100K reads.
						mutable Beat beat = {};
						submit(beat, SignalReader10);
	
						// We will report it to a result collector.												
						mutable parallelLoadTestResults pltr = {};
						pltr.dpsTask = "Insert data item";
						pltr.clientId = (int32)10;
						pltr.startTime = startTime;
						pltr.endTime = ctime(_timeNow);
						pltr.elapsedTime = _totalExecutionTime;
						pltr.errorCnt = error_cnt;
						submit(pltr, DataItemInserter10);
					}					       	

                    config
                       placement:host("Your-Machine-Name1");
        	}    
            
            // Inside this operator (placed on its own PE), we will do 100K reads from the global area of our back-end data store.
			stream<parallelLoadTestResults> DataItemReader10 = Custom(SignalReader10 as SR) {
				logic
					onTuple SR: {
						mutable uint64 err = 0ul;
						mutable boolean res = false;
						mutable int32 error_cnt = 0;
						
						rstring startTime = ctime(getTimestamp());
						// Let us read 100K unique K/V entries from the global area of our data store and time it.
						mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
						mutable int64 _timeInNanoSecondsAfterExecution = 0l;
						mutable timestamp _timeNow = getTimestamp();
						_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable rstring myStringKey = "";
						mutable rstring myStringValue = "";
                        mutable int32 _cnt = 0;
						
						while((isShutdown() == false) && (++_cnt <= 100000)) {
							// Add the host name, writer PE number ($cnt), and the local count (_cnt) to make it a unique string.
							// This will give us key and value strings that are roughly 100 bytes long each.
                            myStringKey = "This is the time for all the good men and women to come to the aid of our nation." + 
                            	" (Your-Machine-Name1_10_" + (rstring)_cnt + ")";
                            myStringValue = "";	
                            // We will use the TTL based get. Our K/V entries are set to be purged automatically after 3 minutes.
							res = dpsGetTTL(myStringKey, myStringValue, err);
							
							if (res == false && err != 0ul) {
								printStringLn("Unexpected error in dpsGetTTL(myStringKey, myStringValue): rc = " + (rstring)dpsGetLastErrorCodeTTL() + 
									", msg = " + dpsGetLastErrorStringTTL());
								error_cnt++;
							}
							
							// Verify what was written and read back from the cache is correct.
							if (myStringKey != myStringValue) {
								printStringLn("Unexpected K/V verification error in dpsGetTTL(myStringKey, myStringValue): myStringKey = " + myStringKey +
									", myStringValue = " + myStringValue);
							}
						}
						
						_timeNow = getTimestamp();
						_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						mutable int64 _totalExecutionTime = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
						
						// We will report it to a result collector.												
						mutable parallelLoadTestResults pltr = {};
						pltr.dpsTask = "Read data item";
						pltr.clientId = 10;
						pltr.startTime = startTime;
						pltr.endTime = ctime(_timeNow);
						pltr.elapsedTime = _totalExecutionTime;
						pltr.errorCnt = error_cnt;
						submit(pltr, DataItemReader10);
					}

					config
						placement:host("Your-Machine-Name1");					
			}
			
		

			// Let us now collect the results coming from 10 data inserters.

			() as DataInsertResults0 = Custom( DataItemInserter1 ,  DataItemInserter2 ,  DataItemInserter3 ,  DataItemInserter4 ,  DataItemInserter5 ,  DataItemInserter6 ,  DataItemInserter7 ,  DataItemInserter8 ,  DataItemInserter9 ,  DataItemInserter10  as DI) {
				logic
					state: {
						mutable list<parallelLoadTestResults> results = [];
					}
					
					onTuple DI: {
						appendM(results, DI);
						
						if (size(results) >= 10) {
							// We got all the results.
							// Let us simply print them here.
							for(parallelLoadTestResults pltr in results) {
								printStringLn((rstring)pltr);
							}	
						}
					}		
                           config
                              placement:host("Your-Machine-Name1");
			}

			// Let us now collect the results coming from 10 data readers.
			() as DataReadResults0 = Custom( DataItemReader1 ,  DataItemReader2 ,  DataItemReader3 ,  DataItemReader4 ,  DataItemReader5 ,  DataItemReader6 ,  DataItemReader7 ,  DataItemReader8 ,  DataItemReader9 ,  DataItemReader10  as DR) {
				logic
					state: {
						mutable list<parallelLoadTestResults> results = [];
					}
					
					onTuple DR: {
						appendM(results, DR);
						
						if (size(results) >= 10) {
							// We got all the results.
							// Let us simply print them here.
							for(parallelLoadTestResults pltr in results) {
								printStringLn((rstring)pltr);
							}	
						}
					}
                           config
                              placement:host("Your-Machine-Name1");		
			}     

*/

	config
		logLevel: error;
}

// In this composite, we will exercise our distributed lock feature available in the dps.
// When multiple Streams applications or PEs want to perform any lengthy store operations,
// one must use the distributed locks to co-ordinate the store access. Use of the
// distributed locks will allow different PEs not to override and collide with 
// each other while working on the same store. Following test will show you
// how two different PEs will comptete with each other in getting entry into the
// store to perform read/write operations without collisions. In general, if there
// is a sequence of store commands that need to be done atomically, then it is time
// to use distributed locks. Every PE can acquire a common user defined distributed
// lock for a lease period and finish all their store commands before that lease
// time expires. During that lease period, only one lock owner will have 
// authorization to do work on the store. If every PE in a big distributed application
// adheres to this policy, then life will become better in a distributed store that is
// accessed by multiple parties. As a best practice, always use the distributed locks for
// a safe and better concurrent access to a store from multiple PEs.
//
// Please be aware that this particular test exercises heavy locking and unlocking of
// the K/V store to have protected read/write operation. If a chosen back-end data store
// provides eventual consistency (such as Cassandra, Cloudant etc.) or performs 
// put/get operations to/from the disk media (HBase, Mongo, Couchbase etc.), the technical requirements for this test 
// will not be met by such data stores and this test may not finish correctly in such
// environments (e-g: Cassandra, Cloudant, HBase, Mongo, Couchbase etc.). That is because, data stores with eventual consistency
// as well as storing it in disks may not return the correct value during a get that
// immediately follows a put operation. For such data stores, it will take a while 
// (a second or two) before the actual value we put is written to
// all the replica servers' memory/disk. Hence, LockTest with too many iterations is not a 
// suitable one for such data stores based on eventual consistency put/get as well disk based put/get (HBase, Mongo, Couchbase).
composite LockTest() {
	graph
		// We are going to spawn two threads that will do the same stuff with proper locking. 
		() as Sink1 = StateUpdater() {}
		() as Sink2 = StateUpdater() {}
}

composite StateUpdater()  {
	param
		// Reduce this iteration count to 10 when testing with eventual consistency data stores (Cassandra, Cloudant etc.) and
		// the ones that put/get to/from the disk media.
		// Frequent and instant get after put is not guaranteed to return consistenct results in such data stores. 
		// Just to demonstrate that the basic locking operation works, let us use a very low number of lock tests for 
		// those eventual consistency data stores and the ones that use the disk media for storage.
		// Memcached, Redis and Aerospike should work just fine with 1000 iterations, because they provide full data consistency during put and get operations.
		expression<int32> $LOCK_TEST_ITERATIONS_NEEDED_FOR_NON_DISK_BASED_STORES : 1000;
		expression<int32> $LOCK_TEST_ITERATIONS_NEEDED_FOR_DISK_BASED_STORES : 10;
		// For those data stores that only provides eventual consistency (Cassandra, Cloudant etc.), you can increase the delay value here
		// from 0.0 to 3.0. That will allow the eventual consistency to work correctly so that we can read the correct data that was put earlier.
		// This whole eventual consistency stuff is really unreasonable.
		// For memcached, Redis and Aerospike, you don't require this delay and you can simply have 0.0 for this delay parameter.
		expression<float64> $DELAY_NEEDED_FOR_NON_DISK_BASED_STORES : 0.0;
		expression<float64> $DELAY_NEEDED_FOR_DISK_BASED_STORES : 3.0;
		
	graph
		// We are going to use the SPL Custom source to generate lock test signals.
		stream<int8 a> Src = Custom() {
			logic
				onProcess: {
					// If the previous run of the application was stopped in the middle of this test, then that may have left
					// the store and the lock intact as it was created in the previous test run. Let us ensure we start from a clean slate.
					mutable uint64 s = 0ul;
					mutable uint64 err = 0ul;
					s = dpsFindStore("Super_Duper_Store", err);
						
					if (err == 0ul) {
						// That store was not cleaned up properly during the previous test run.
						// Let us delete that store now.
						dpsRemoveStore(s,  err);
					}				
					
					// Let us do an initial wait (initDelay)
					block(7.0);
					rstring dbName = dpsGetNoSqlDbProductName();
					int32 loopCnt = (dbName == "cassandra" || dbName == "cloudant" ||
						dbName == "hbase" || dbName == "couchbase") ?
						$LOCK_TEST_ITERATIONS_NEEDED_FOR_DISK_BASED_STORES : $LOCK_TEST_ITERATIONS_NEEDED_FOR_NON_DISK_BASED_STORES;
					mutable int32 cnt = 0;
					Src oTuple = {a=1b};
					
					// Stay in a loop and send the lock test signals.
					while(cnt++ < loopCnt) {
						submit(oTuple, Src);
					}
					
					// Send a final marker punctuation.
					submit(Sys.FinalMarker, Src);
					// We are done sending all the test signals.
				} 
        }
        
		() as Sink = Custom(Src) {
			logic
				state: {
					mutable boolean first = true;
					mutable uint64 s = 0; // store 
					mutable uint64 l = 0; // lock
					mutable int32 lockTestCnt = 0; 
					mutable int32 iterationsNeeded = 0;
					mutable float64 delayBetweenPutAndGet = 0.0;
				}
				
				onTuple Src: {           
					mutable boolean done = false;
					mutable uint64 err = 0;
					lockTestCnt++;
					
					if(first) {
						first = false;
						rstring dummyRstring = "";
						int32 dummyInt32 = 0;

						rstring dbName = dpsGetNoSqlDbProductName();
						iterationsNeeded = (dbName == "cassandra" || dbName == "cloudant" ||
							dbName == "hbase" || dbName == "couchbase") ?
							$LOCK_TEST_ITERATIONS_NEEDED_FOR_DISK_BASED_STORES : $LOCK_TEST_ITERATIONS_NEEDED_FOR_NON_DISK_BASED_STORES;
						// Even though HBase is a disk based data store, in my tests I observed that this delay is not needed for HBase.
						// If someone needs this delay for HBase, it can always be added here easily.
						delayBetweenPutAndGet = (dbName == "cassandra" || dbName == "cloudant") ?
							$DELAY_NEEDED_FOR_DISK_BASED_STORES : $DELAY_NEEDED_FOR_NON_DISK_BASED_STORES;
						
						// If multiple attempts are made to create the same store in parallel from different operators,
						// we may get concurrent execution exception in Cassandra. Hence, let us retry this for 5 times.
						// In general, such multiple tries are not required. We are doing it here for pedantic reasons.
						mutable int32 cnt = 0;
						
						while(cnt++ <= 4) { 
							s = dpsCreateOrGetStore("Super_Duper_Store", dummyRstring, dummyInt32, err);
							if (err != 0ul) {
								printStringLn("Error in dpsCreateOrGetStore(Super_Duper_Store) rc = " + 
									(rstring)dpsGetLastStoreErrorCode() + ", msg=" + dpsGetLastStoreErrorString());
							} else {
								printStringLn("My Super_Duper_Store id = " + (rstring)s + ". Obtained in " +
									(rstring)cnt + " attempt(s).");
								break;
							} 
						}
						
						if (err != 0ul) {
							return;
						}
						
						assert(err==0ul);
						// Get a user defined distributed lock thar will be used to have a thread safe access into the store we created above.	
						l = dlCreateOrGetLock("Super_Duper_Lock", err);
						if (err != 0ul) {
							printStringLn("Error in dlCreateOrGetLock(Super_Duper_Lock) rc = " + 
								(rstring)dlGetLastDistributedLockErrorCode() + ", msg=" + dlGetLastDistributedLockErrorString());
							return;
						} else {
							printStringLn("My distributed Super_Duper_Lock id = " + (rstring)l);
						}
						assert(err==0ul);
					}
					
					// We have an utility function that will return us the process id currently owning this lock.
					// Let us exercise that API.
					mutable uint32 pid = dlGetPidForLock("Super_Duper_Lock", err);
					
					if (err != 0ul) {
						printStringLn("Error in dlGetPidForLock(Super_Duper_Lock)  rc = " + 
							(rstring)dlGetLastDistributedLockErrorCode() + ", msg=" + dlGetLastDistributedLockErrorString());
					} else {
						printStringLn("Before lock acquisition: pid owning the Super_Duper_Lock = " + (rstring)pid);
					}
					
                	// mutual exclusion
                	// Our distributed locking works based on the assumption that every thread interested in
                	// accessing the same store will play a fair game. That means every thread will get into the 
                	// store only if they can successfully acquire a lock. There should not be any rogue threads that
                	// will bypass this gentlemanly agreement and get into the store without owning a lock.
                	// It is purely a trust based cooperative locking scheme.
                	//
                	// printStringLn("Begin lock acquisition");
                	// Acquire that lock with a lease time for 30 seconds and wait no more than 40 seconds to acquire the lock.
                	// These high time values are needed for the eventual consistency based data stores to work correctly (Cassandra, Cloudant etc.)
					dlAcquireLock(l, 30.0, 40.0, err);
					// If we can't aquire the lock, let us return from here.
					if (err != 0ul) {
						printStringLn("Failed to acquire a lock. rc = " + 
							(rstring)dlGetLastDistributedLockErrorCode() + ", msg=" + dlGetLastDistributedLockErrorString());
						
						return;
					}
					assert(err==0ul);
					// This debug print is here to test the lock acquisition logic for data stores such as Cassandra, Cloudant etc.
					// printStringLn("End lock acquisition");
					pid = dlGetPidForLock("Super_Duper_Lock", err);
					
					if (err != 0ul) {
						printStringLn("Error in dlGetPidForLock(Super_Duper_Lock)  rc = " + 
							(rstring)dlGetLastDistributedLockErrorCode() + ", msg=" + dlGetLastDistributedLockErrorString());
					} else {
						printStringLn("After lock acquisition: pid owning the Super_Duper_Lock = " + (rstring)pid);
					}
					
					mutable int32 val = 0;    
					// For the eventual consistency based data stores (Cassandra, Cloudant etc.), let us wait for a while before
					// the actual value is propagated (Eventual consistency is really odd.). We will do a get after that wait.
					if (delayBetweenPutAndGet > 0.0) {
						block(delayBetweenPutAndGet);
					}
					dpsGet(s, "myKey", val, err);					                             
					dpsPut(s, "myKey", val+1, err);
					printStringLn("val=" + (rstring)val + " as read from the store during lock test #" + (rstring)lockTestCnt);
					
					// Only one of the two PEs currently in the race to get from and
					// put into that same store will win in obtaining a chance to
					// store the value of $LOCK_TEST_ITERATIONS_NEEDED * 2u. 
					if(val+1 == (iterationsNeeded * 2)) {
						done=true;
						printStringLn("'myKey' => " + (rstring)(val+1));
						dpsRemoveStore(s,  err); 
						
						if (err != 0ul) {
							printStringLn("Store removal error. rc = " + 
								(rstring)dpsGetLastStoreErrorCode() + ", msg=" + dpsGetLastStoreErrorString());						
						} else {
							printStringLn("Super_Duper_Store with a store id of " + (rstring)s + " has now been removed from the data store.");
						}
						
						assert(err==0ul);
					}
					 
					dlReleaseLock(l, err);
					
					if (err != 0ul) {
						printStringLn("Lock release error. rc = " + 
							(rstring)dlGetLastDistributedLockErrorCode() + ", msg=" + dlGetLastDistributedLockErrorString());
					}
					
					assert(err==0ul);
					
					if(done) {
						dlRemoveLock(l, err);
						
						if (err != 0ul) {
							printStringLn("Lock removal error. rc = " + 
								(rstring)dlGetLastDistributedLockErrorCode() + ", msg=" + dlGetLastDistributedLockErrorString());						
						} else {
							printStringLn("Super_Duper_Lock with a lock id of " + (rstring)l + " has now been removed from the data store.");
						}
						
						assert(err==0ul);
					}     
				}
		}
}
        
// This composite does read/write performance test into the configured back-end data store.     
// Please be aware this high volume test will finish in a decent time for memcached, Redis and Aerospike.
// However, Cassandra, Cloudant, HBase, Mongo, Couchbase etc. are not very fast due to their disk writes and 
// hence it may be a long wait before this test completes when you use those data stores.   
// You may decide whether you want to comment out this test in the DpsTest1 composite at the
// top of this file while using those data stores.
// (OR)
// You can drastically reduce the total number of put/get operations in the param section
// of this composite below for those relatively slow performing data stores.
composite ReadWritePerformanceTest() {
	param
		// Reduce this operations count to 100*1 when testing with relatively slow performing data stores (Cassandra, Cloudant, HBase etc.)
		// Memcached, Redis and Aerospike should work just fine for 100*1000 operations, because they are somewhat faster than the others.
		expression<int32> $PUT_GET_OPERATIONS_NEEDED_FOR_IN_MEMORY_DATA_STORES : 100*1000;
		expression<int32> $PUT_GET_OPERATIONS_NEEDED_FOR_DISK_BASED_DATA_STORES : 100*1;
		
	graph
		stream<int8 a> Src = Beacon() {
			param
				iterations: 1u;
				initDelay: 4.0;
		}
		
		() as MyPerfSink = Custom(Src) {
			logic
				onTuple Src: {
					mutable uint64 err = 0ul;
					mutable uint64 s = 0ul;

					rstring dbName = dpsGetNoSqlDbProductName();
					int32 maxPutGetOperationsCount = (dbName == "cassandra" || dbName == "cloudant" || 
						dbName == "hbase" || dbName == "couchbase") ?
						$PUT_GET_OPERATIONS_NEEDED_FOR_DISK_BASED_DATA_STORES : $PUT_GET_OPERATIONS_NEEDED_FOR_IN_MEMORY_DATA_STORES;
	                    
					mutable int64 _timeInNanoSecondsBeforeExecution = 0l;
					mutable int64 _timeInNanoSecondsAfterExecution = 0l;
					mutable timestamp _timeNow = getTimestamp();
					_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
					rstring myDummyRString = "IBM T.J.Watson Research Center";
					s = dpsCreateOrGetStore("PerfStore1", myDummyRString, myDummyRString, err);
						
					if (err > 0ul) {
						printStringLn("dpsCreateOrGetStore(PerfStore1)--> Error code=" + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}
						
					mutable int32 myCnt = 0;
					
					// Do a bulk write.
					while(++myCnt <= maxPutGetOperationsCount) {
						dpsPut(s, myDummyRString + (rstring)myCnt, myDummyRString + (rstring)myCnt, err);
					} 
	
					if (err > 0ul) {
						printStringLn("Error in dpsPut: rc=" + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
						abort();
					}
	
					_timeNow = getTimestamp();
					_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));					
					mutable int64 _totalExecutionTime_ = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
					printStringLn("Time taken for " + (rstring)maxPutGetOperationsCount + 
						" insertions = " +  (rstring)_totalExecutionTime_ + " nanosecs");
						
					myCnt = 0;
					mutable rstring myValue = 0;
					_timeNow = getTimestamp();
					_timeInNanoSecondsBeforeExecution =  ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));
						
					// Do a bulk read.
					while(++myCnt <= maxPutGetOperationsCount) {
						dpsGet(s, myDummyRString + (rstring)myCnt, myValue, err);
					}					
	
					if (err > 0ul) {
						printStringLn("Error in dpsGet: rc=" + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
						abort();
					}
						
					_timeNow = getTimestamp();
					_timeInNanoSecondsAfterExecution = ((getSeconds(_timeNow) * (int64)1000000000) + (int64)getNanoseconds(_timeNow));					
					_totalExecutionTime_ = _timeInNanoSecondsAfterExecution - _timeInNanoSecondsBeforeExecution;
					printStringLn("Time taken for " + (rstring)maxPutGetOperationsCount + 
						" fetches = " +  (rstring)_totalExecutionTime_ + " nanosecs");					
						
					mutable uint64 perfSize = dpsSize(s, err);
					if (err > 0ul) {
						printStringLn("dpsSize(PerfStore1)--> Error code=" + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}
						
					printStringLn("Size of the PerfStore1 = " +  (rstring)perfSize);
					dpsRemoveStore(s, err);
					if (err > 0ul) {
						printStringLn("dpsRemoveStore(PerfStore1)--> Error code=" + (rstring)dpsGetLastStoreErrorCode() + 
							", msg = " + dpsGetLastStoreErrorString());
					}	
		
			}
		}
}

// This composite shows how we can directly execute commands on certain types of data stores.
composite RunNativeDataStoreCommands() {
	param
 		// For the public cloud based Cloudant service, it must be in this format:
		// http://user:password@user.cloudant.com
		// For the "Cloudant Local" on-premises infrastructure, it must be in this format: 
		// http://user:password@XXXXX where XXXXX is a name or IP address of your on-premises "Cloudant Local" load balancer machine.	
		// This base URL must not end with a forward slash.
		//
		// NOTE: If you give an empty string for the URL, then the Cloudant server configured
		// in the SPL project directory's etc/no-sql-kv-store-servers.cfg file will be used.
		expression<rstring> $CLOUDANT_BASE_URL : "";
		// For HBase, following is the base url. (Must not end with a forward slash.)
		// Format of this URL must be like this:
		// http://user:password@HBase-REST-ServerNameOrIPAddress:port
		//
		// NOTE: If you give an empty string for the URL, then the HBase server(s) configured
		// in the SPL project directory's etc/no-sql-kv-store-servers.cfg file will be used.		
		expression<rstring> $HBASE_BASE_URL : "";
		
	graph	
		stream<int8 a> Src = Beacon() {
			param
				iterations: 1u;
				initDelay: 4.0;
		}
		
		() as RunCommandSink = Custom(Src) {
			logic
				onTuple Src: {
					mutable rstring cmd = "";
					mutable uint64 err = 0ul;
					mutable boolean res = true;
					rstring dbProductName = dpsGetNoSqlDbProductName();
									
					if (dbProductName == "memcached" || dbProductName == "mongo" ||
						dbProductName == "couchbase" || dbProductName == "aerospike") {
						printStringLn("Native data store command execution is not supported when " +
						dbProductName + 
						" is configured as the back-end data store.");
						printStringLn("Exiting now...");
						return;
					}
				
					// If users want to execute simple arbitrary back-end data store (fire and forget)
					// native commands, this API can be used. This covers any Redis or Cassandra(CQL)
					// native commands that don't have to fetch and return K/V pairs or return size of the db etc.
					// (Insert and Delete are the more suitable ones here. However, key and value can only have string types.)
					// User must ensure that his/her command string is syntactically correct according to the
					// rules of the back-end data store you configured. DPS logic will not do the syntax checking.
					//
					// We will simply take your command string and run it. So, be sure of what
					// command you are sending here.				
					//					
					if (dbProductName == "redis" || dbProductName == "redis-cluster") {
						printStringLn("=== Start of the native data store command execution using Redis ===");
						// Let us try some simple Redis native commands (one way calls that don't fetch anything from the DB)
						// (You can't do get command using this technique. Similarly, no complex type keys or values.
						//  In that case, please use the regular dps APIs.)
						// 
						// Insert a K/V pair by using the popular Redis set command.
						cmd = "set foo bar";
						err = 0ul;
						res = dpsRunDataStoreCommand(cmd, err);
					  
						if (res == true) {
							printStringLn("Running a Redis native command 'set foo bar' worked correctly.");
						} else {
							printStringLn("Error in running a Redis native command 'set foo bar'. Error code=" + (rstring)dpsGetLastStoreErrorCode() + 
								", msg = " + dpsGetLastStoreErrorString());
						}
					  
						if (res == true) {
							// Delete a K/V pair by using another Redis native command.
							cmd = "del foo";
							res = dpsRunDataStoreCommand(cmd, err);
							
							if (res == true) {
								printStringLn("Running a Redis native command 'del foo' worked correctly.");
							} else {
								printStringLn("Error in running a Redis native command 'del foo'. Error code=" + (rstring)dpsGetLastStoreErrorCode() + 
									", msg = " + dpsGetLastStoreErrorString());
							}
						}	
						
						printStringLn("=== End of the native data store command execution using Redis ===");
					}			  

					if (dbProductName == "cassandra") {
						printStringLn("=== Start of the native data store command execution using Cassandra ===");
						// Let us try some simple Cassandra native commands (one way calls that don't fetch anything from the DB) 
						// (You can't do select statements using this technique. Similarly, no complex type keys or values.
						//  In that case, please use the regular dps APIs.)
						// 
						// Create a keyspace by using a Cassandra CQL command.
						cmd = "create keyspace test_native_command_exec with replication = {'class' : 'SimpleStrategy', 'replication_factor' : 1};";
						err = 0ul;
						res = dpsRunDataStoreCommand(cmd, err);
					  
						if (res == true) {
							printStringLn("Running a Cassandra native command 'create keyspace test_native_command_exec;' worked correctly.");
						} else {
							printStringLn("Error in running a Cassandra native command 'create keyspace test_native_command_exec;'. Error code=" + (rstring)dpsGetLastStoreErrorCode() + 
								", msg = " + dpsGetLastStoreErrorString());
						}
	
					  	if (res == true) {
							// Drop a keyspace using another Cassandra CQL command.
							cmd = "drop keyspace test_native_command_exec;";
							res = dpsRunDataStoreCommand(cmd, err);
							
							if (res == true) {
								printStringLn("Running a Cassandra native command 'drop keyspace test_native_command_exec;' worked correctly.");
							} else {
								printStringLn("Error in running a Cassandra native command 'drop keyspace test_native_command_exec;'. Error code=" + (rstring)dpsGetLastStoreErrorCode() + 
									", msg = " + dpsGetLastStoreErrorString());
							}
							
							// As shown above, you can go ahead and run other CQL commands such as create table, insert into, delete from etc.
						}
						
						printStringLn("=== End of the native data store command execution using Cassandra ===");
					}

					// We have a full fledged native command execution feature demonstration below for Cloudant.
					if (dbProductName == "cloudant") {
						// For Cloudant, we will support two way commands since the request/response is done via JSON formatted strings.
						// That makes it easier to support almost all the Cloudant Database and Document based commands.
						// We will use the same dps API as used in Redis and Cassandra but with overloaded function arguments.
						// This overloaded API call will support all the HTTP verbs except COPY. So, you can use GET, PUT, POST, DELETE, and HEAD.
						// With those supported HTTP verbs, you can execute all the Cloudant HTTP REST APIs except for the APIs that involve attachments.
						// A very good reference for Cloudant HTTP REST/JSON APIs: https://docs.cloudant.com/api/index.html 
						//
						// DPS API format:
						// boolean dpsRunDataStoreCommand(uint32 cmdType, rstring httpVerb, rstring baseUrl,
						//                                rstring apiEndpoint, rstring queryParams, rstring jsonRequest,
						//                                mutable rstring jsonResponse, mutable uint64 err);
						//
						// This DPS API returns false when it encounters any error inside the DPS or in cURL calls before your command reaches the Cloudant server.
						// In the case of a false return value, you can get the error code from the err argument (See the explanation for err below.)
						// A return value of true simply means that your HTTP REST API request was sent to the Cloudant server and a response was received from the server.
						// In that case, you will get the HTTP response code in the err argument and you should interpret the meaning of that HTTP code to 
						// know whether your request really succeeded or not. 
						//
						// cmdType: Should be 1u if you are executing any of the Cloudant database related APIs.
						//          Should be 2u if you are executing any of the Cloudant document related APIs.
						//
						// httpVerb: Should be one of the supported HTTP verbs (GET, PUT, POST, DELETE, HEAD). [COPY is not a supported verb in this DPS API.]
						// 
						// baseUrl: For the public cloud based Cloudant service, it must be in this format:
						//             http://user:password@user.cloudant.com
						//          For the "Cloudant Local" on-premises infrastructure, it must be in this format: 
						//             http://user:password@XXXXX where XXXXX is a name or IP address of your on-premises "Cloudant Local" load balancer machine.
						//          NOTE: If you give an empty string for the URL, then the Cloudant server configured
						//                in the SPL project directory's etc/no-sql-kv-store-servers.cfg file will be used.
						// 
						// apiEndPoint: It should be a Cloudant DB or document related portion of the URL path as documented in the Cloudant APIs.
						//
						// queryParams: It should be in this format: name1=value1&name2=value2&name3=value3
						//
						// jsonRequest: This is your JSON request needed by the Cloudant API you are executing. Please ensure that any special
						//              characters such as double quotes are properly escaped using the backslash character.     
						//
						// jsonResponse: This is one of the two mutable variables you must pass to this DPS API.
						//               This argument brings back any JSON response string received from the Cloudant server while executing your HTTP REST request.
						//
						// err: 
						//      If this DPS API returns false, then this mutable argument will be set to any DPS or cURL errors that occurred inside the DPS code.
						//      To receive more details about the DPS or cURL errors, you can call the dpsGetLastStoreErrorString() DPS API. 
						//      If this DPS API returns true, then this argument will be set to the HTTP response code returned by the Cloudant server.
						//      In case of this API returning true, there will not be any additional error or status messages provided. You have to
						//      interpret the meaning of the returned HTTP response code and make your further logic from there. 
						//
						// Your input arguments given above will form the full URL inside this API: <baseUrl>/<API endpoint path>?<queryParams> 
						//						
						// ========================= CLOUDANT DB LEVEL REQUESTS ARE SHOWN BELOW =========================
						printStringLn("=== Start of the native data store command execution for the Cloudant DB level requests ===");
						// 1a) Let us create a new database: PUT /db
						// We are going to make a database related HTTP request.
						mutable uint32 cmdType = 1u;
						mutable rstring httpVerb = "PUT";
						mutable rstring baseUrl = $CLOUDANT_BASE_URL;   
						// Specify your new database name.
						// An API endpoint URL path must always begin with a forward slash character.
						mutable rstring apiEndpoint = "/my_db_1";      
						mutable rstring queryParams = "";
						mutable rstring jsonRequest = "";
						mutable uint64 err = 0ul;
						mutable rstring jsonResponse = "";
						mutable boolean result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 201ul || err == 202ul || err == 412ul)) {
							printStringLn("1a) Cloudant database creation: " + apiEndpoint + 
								" is now available for use. JSON response = " + jsonResponse);
						} else {
							printStringLn("1a) Cloudant database " + apiEndpoint + 
								" was not created. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}
						
						// 1b) Let us create a second database: PUT /db
						apiEndpoint = "/my_db_2";
						jsonRequest = "";
						jsonResponse = "";
						
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 201ul || err == 202ul || err == 412ul)) {
							printStringLn("1b) Cloudant database creation: " + apiEndpoint + 
								" is now available for use. JSON response = " + jsonResponse);
						} else {
							printStringLn("1b) Cloudant database " + apiEndpoint + 
								" was not created. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}						

						// 1c) Let us create a third database: PUT /db
						apiEndpoint = "/my_db_3";
						jsonRequest = "";
						jsonResponse = "";
						
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 201ul || err == 202ul || err == 412ul)) {
							printStringLn("1c) Cloudant database creation: " + apiEndpoint + 
								" is now available for use. JSON response = " + jsonResponse);
						} else {
							printStringLn("1c) Cloudant database " + apiEndpoint + 
								" was not created. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}	
						
						// 2) Let us get a list of all databases: GET /_all_dbs
						httpVerb = "GET"; 
						apiEndpoint = "/_all_dbs";
						jsonRequest = "";
						jsonResponse = "";
						
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 200ul)) {
							printStringLn("2) List of the cloudant databases " + apiEndpoint + 
								" was obtained. JSON response = " + jsonResponse);
						} else {
							printStringLn("2) List of the cloudant databases " + apiEndpoint + 
								" could not be obtained. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}	
						
						// 3) Let us get the db information: GET /db
						apiEndpoint = "/my_db_1";
						jsonRequest = "";
						jsonResponse = "";
						
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 200ul)) {
							printStringLn("3) DB information " + apiEndpoint + 
								" was obtained. JSON response = " + jsonResponse);
						} else {
							printStringLn("3) DB information " + apiEndpoint + 
								" could not be obtained. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}							
						
						
						// 4a) Let us delete a database now: DELETE /db
						httpVerb = "DELETE";
						apiEndpoint = "/my_db_2";
						jsonRequest = "";
						jsonResponse = "";						

						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 200ul)) {
							printStringLn("4a) DB deletion " + apiEndpoint + 
								" was completed. JSON response = " + jsonResponse);
						} else {
							printStringLn("4a) DB deletion " + apiEndpoint + 
								" could not be completed. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}												

						// 4b) Let us delete a database now: DELETE /db
						apiEndpoint = "/my_db_3";
						jsonRequest = "";
						jsonResponse = "";						

						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 200ul)) {
							printStringLn("4b) DB deletion " + apiEndpoint + 
								" was completed. JSON response = " + jsonResponse);
						} else {
							printStringLn("4b) DB deletion " + apiEndpoint + 
								" could not be completed. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}

						// 5) Let us insert documents in bulk: POST /db/_bulk_docs
						httpVerb = "POST";
						apiEndpoint = "/my_db_1/_bulk_docs";
						// All the double quotes in your JSON request must be escaped via a backslash character.
						jsonRequest = "{\"docs\": [" +
							"{\"_id\": \"IBM\", \"HQ\": \"Armonk, NY\", \"Date Founded\": \"June 16, 1911\", \"First CEO\": \"Thomas J. Watson\"}," +
							"{\"_id\": \"Microsoft\", \"HQ\": \"Redmond, WA\", \"Date Founded\": \"April 4, 1975\", \"First CEO\": \"Bill Gates\"}," +
							"{\"_id\": \"Amazon\", \"HQ\": \"Seattle, WA\", \"Date Founded\": \"July 5, 1994\", \"First CEO\": \"Jeff Bezos\"}," +
							"{\"_id\": \"Google\", \"HQ\": \"Mountain View, CA\", \"Date Founded\": \"September 4, 1998\", \"First CEO\": \"Larry Page\"}]}";		  
						jsonResponse = "";								

						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 201ul)) {
							printStringLn("5) Insert documents in bulk " + apiEndpoint + 
								" was completed. JSON response = " + jsonResponse);
						} else {
							printStringLn("5) Insert documents in bulk " + apiEndpoint + 
								" could not be completed. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}

						// 6) Let us retrieve all documents in bulk: GET /db/_all_docs
						httpVerb = "GET";
						apiEndpoint = "/my_db_1/_all_docs";
						jsonRequest = "";
						jsonResponse = "";						
						queryParams = "descending=true&include_docs=true&limit=10";
						
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if (result == true) {
							printStringLn("6) Retrieve all documents in bulk " + apiEndpoint + 
								" was completed. JSON response = " + jsonResponse);
						} else {
							printStringLn("6) Retrieve all documents in bulk " + apiEndpoint + 
								" could not be completed. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}						

						// 7) Let us retrieve selective documents in bulk: POST /db/_all_docs
						httpVerb = "POST";
						apiEndpoint = "/my_db_1/_all_docs";
						jsonRequest = "{\"keys\": [\"IBM\", \"Amazon\", \"Google\"]}";
						jsonResponse = "";						
						queryParams = "include_docs=true&limit=10";
						
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if (result == true) {
							printStringLn("7) Retrieve selective documents in bulk " + apiEndpoint + 
								" was completed. JSON response = " + jsonResponse);
						} else {
							printStringLn("7) Retrieve selective documents in bulk " + apiEndpoint + 
								" could not be completed. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}										

						// 8) Let us retrieve information about shards in a DB: GET /db/_shards
						httpVerb = "GET";
						apiEndpoint = "/my_db_1/_shards";
						jsonRequest = "";
						jsonResponse = "";						
						queryParams = "";
						
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if (result == true) {
							printStringLn("8) Retrieve information about shards in a DB " + apiEndpoint + 
								" was completed. JSON response = " + jsonResponse);
						} else {
							printStringLn("8) Retrieve information about shards in a DB " + apiEndpoint + 
								" could not be completed. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}

						// 4c) Let us delete a database now: DELETE /db
						httpVerb = "DELETE";
						apiEndpoint = "/my_db_1";
						jsonRequest = "";
						jsonResponse = "";

						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 200ul)) {
							printStringLn("4c) DB deletion " + apiEndpoint + 
								" was completed. JSON response = " + jsonResponse);
						} else {
							printStringLn("4c) DB deletion " + apiEndpoint + 
								" could not be completed. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}
						
						// ...
						// ...
						// If you are interested, you can add code for the remaining Cloudant DB level API requests here.
						// ...
						// ...
						printStringLn("=== End of the native data store command execution for the Cloudant DB level requests ===");
						// ========================= CLOUDANT DOC LEVEL REQUESTS ARE SHOWN BELOW =========================				
						printStringLn("");								
						printStringLn("=== Start of the native data store command execution for the Cloudant DOC level requests ===");
						// 1d) Let us create a fourth database: PUT /db
						cmdType = 1u;
						httpVerb = "PUT";
						apiEndpoint = "/my_db_4";
						jsonRequest = "";
						jsonResponse = "";
						
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 201ul || err == 202ul || err == 412ul)) {
							printStringLn("1d) Cloudant database creation: " + apiEndpoint + 
								" is now available for use. JSON response = " + jsonResponse);
						} else {
							printStringLn("1d) Cloudant database " + apiEndpoint + 
								" was not created. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}	
						
						// 9) Let us insert a new document now: POST /db
						cmdType = 2u;
						httpVerb = "POST";
						apiEndpoint = "/my_db_4";
						jsonRequest = 
							"{\"_id\": \"Yankees\", \"Home\": \"Bronx, NY\", \"Championships\": 27, " + 
							  "\"A Few Legends\": [\"Babe Ruth\", \"Lou Gehrig\", \"Joe DiMaggio\", \"Mickey Mantle\", \"Derek Jeter\"]}";
						jsonResponse = "";								
						 
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 201ul)) {
							printStringLn("9) Cloudant document creation " + apiEndpoint + 
								" was completed. JSON response = " + jsonResponse);
						} else {
							printStringLn("9) Cloudant document " + apiEndpoint + 
								" was not created. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}	
						
						// 10) Let us insert a new document now using a different technique: PUT /db/doc
						httpVerb = "PUT";
						// Only the API endpoint needs to be taken care for entity characters such as space, ampersand etc. Not the JSON request string.
						apiEndpoint = "/my_db_4/Red%20Sox";
						jsonRequest = 
							"{\"_id\": \"Red Sox\", \"Home\": \"Boston, MA\", \"Championships\": 8, " + 
							  "\"A Few Legends\": [\"Ted Williams\", \"Carl Yastrzemski\", \"Cy Young\", \"Johnny Pesky\"]}";
						jsonResponse = "";								
						 
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 201ul  || err == 202ul)) {
							printStringLn("10) Cloudant document creation " + apiEndpoint + 
								" was completed. JSON response = " + jsonResponse);
						} else {
							printStringLn("10) Cloudant document " + apiEndpoint + 
								" was not created. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}
						
						// 11a) Let us retrieve a document from a given database: GET db/doc
						httpVerb = "GET";
						apiEndpoint = "/my_db_4/Yankees";
						jsonRequest = "";
						jsonResponse = "";								
						 
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 200ul)) {
							printStringLn("11a) Retrieve a document from DB " + apiEndpoint + 
								" was completed. JSON response = " + jsonResponse);
						} else {
							printStringLn("11a) Retrieve a document from DB " + apiEndpoint + 
								" was not completed. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}							

						// Save it for use later in the code below for showing how to perform the document update.
						rstring yankeesDoc = jsonResponse;

						// 11b) Let us retrieve a document from a given database: GET db/doc
						apiEndpoint = "/my_db_4/Red%20Sox";
						jsonRequest = "";
						jsonResponse = "";								
						 
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 200ul)) {
							printStringLn("11b) Retrieve a document from DB " + apiEndpoint + 
								" was completed. JSON response = " + jsonResponse);
						} else {
							printStringLn("11b) Retrieve a document from DB " + apiEndpoint + 
								" was not completed. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}							
						
						// Save it for use later in the code below for showing how to perform the document deletion.
						rstring redSoxDoc = jsonResponse;

						// 12) Let us update an existing document: PUT db/doc
						// Get the revision number from the previously retrieved json response.
						// Ideally, we should be parsing it using a good JSON API.
						// Instead of that, we are going to do string parsing for our layman exercise here.
						// In the json document that was retrieved earlier, we should have a _rev element as shown below.
						// "_rev": "1-2b458b0705e3007bce80b0499a1199e7"
						// Let us skip two double quote characters from the beginning of the _rev tag to 
						// get to the actual revision number of the document we want to update.
						mutable boolean revisionNumberFound = false;
						mutable int32 idx1 = findFirst(yankeesDoc, "_rev\":", 0);
						if (idx1 != -1) {
							// Let us get the first of two double quote characters.
							idx1 = findFirst(yankeesDoc, "\"", idx1);
							
							if (idx1 != -1) {
								// Let us get the second double quote character.
								idx1 = findFirst(yankeesDoc, "\"", idx1+1);
								
								if (idx1 != -1) {
									// Now, let us get the double quote that appears at the end of the revision number.
									int32 idx2 = findFirst(yankeesDoc, "\"", idx1+1);
								
									if (idx2 != -1) {
										// We now have everything to parse the revision number
										// (Please forgive for not using a JSON API which would have made it a lot simpler.)
										int32 slen = idx2 - idx1 - 1;
										rstring revisionNumber = substring(yankeesDoc, idx1+1, slen);
										revisionNumberFound = true;
										// In order to update an existing document, we must add a _rev tag in our JSON reqeust and
										// assign it to the revision number we parsed above.
										httpVerb = "PUT";
										apiEndpoint = "/my_db_4/Yankees";
										jsonRequest = 
											"{\"_id\": \"Yankees\", \"Home\": \"Bronx, NY\", \"Championships\": 27, " + 
										  	"\"A Few Legends\": [\"Babe Ruth\", \"Lou Gehrig\", \"Joe DiMaggio\", \"Yogi Berra\", \"Mickey Mantle\", \"Derek Jeter\"], " + 
										  	"\"_rev\": \"" + revisionNumber + "\"}";
										jsonResponse = "";								
									 
										result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
									
										if ((result == true) && (err == 201ul)) {
											printStringLn("12) Cloudant document update " + apiEndpoint + 
												" was completed. JSON response = " + jsonResponse);
										} else {
											printStringLn("12) Cloudant document update " + apiEndpoint + 
												" was not completed. Error code = " + (rstring) err +
												". Error msg = " + dpsGetLastStoreErrorString());
										}												
									}
								}
							}
						}
						
						if (revisionNumberFound == false) {
							printStringLn("12) Unable to parse the revision number of the Cloudant document. Hence, update document operation was aborted.");
						} else {
							// 11c) Let us retrieve a document from a given database: GET db/doc
							httpVerb = "GET";
							apiEndpoint = "/my_db_4/Yankees";
							jsonRequest = "";
							jsonResponse = "";								
							 
							result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
							
							if ((result == true) && (err == 200ul)) {
								printStringLn("11c) Retrieve a document from DB " + apiEndpoint + 
									" was completed. JSON response = " + jsonResponse);
							} else {
								printStringLn("11c) Retrieve a document from DB " + apiEndpoint + 
									" was not completed. Error code = " + (rstring) err +
									". Error msg = " + dpsGetLastStoreErrorString());
							}
						}

						// 13) Let us delete an existing document: DELETE db/doc 
						// Get the revision number from the previously retrieved json response.
						// Ideally, we should be parsing it using a good JSON API.
						// Instead of that, we are going to do string parsing for our layman exercise here.
						// In the json document that was retrieved earlier, we should have a _rev element as shown below.
						// "_rev": "1-2b458b0705e3007bce80b0499a1199e7"
						// Let us skip two double quote characters from the beginning of the _rev tag to 
						// get to the actual revision number of the document we want to update.
						revisionNumberFound = false;
						idx1 = findFirst(redSoxDoc, "_rev\":", 0);
						if (idx1 != -1) {
							// Let us get the first of two double quote characters.
							idx1 = findFirst(redSoxDoc, "\"", idx1);
							
							if (idx1 != -1) {
								// Let us get the second double quote character.
								idx1 = findFirst(redSoxDoc, "\"", idx1+1);
								
								if (idx1 != -1) {
									// Now, let us get the double quote that appears at the end of the revision number.
									int32 idx2 = findFirst(redSoxDoc, "\"", idx1+1);
								
									if (idx2 != -1) {
										// We now have everything to parse the revision number
										// (Please forgive for not using a JSON API which would have made it a lot simpler.)
										int32 slen = idx2 - idx1 - 1;
										rstring revisionNumber = substring(redSoxDoc, idx1+1, slen);
										revisionNumberFound = true;
										// In order to delete an existing document, we must add a rev query param and 
										// assign it to the revision number we parsed above.
										httpVerb = "DELETE";
										apiEndpoint = "/my_db_4/Red%20Sox";
										jsonRequest = "";
										jsonResponse = "";
										queryParams = "rev=" + revisionNumber; 								
									 
										result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
									
										if ((result == true) && (err != 409ul)) {
											printStringLn("13) Cloudant document deletion " + apiEndpoint + 
												" was completed. JSON response = " + jsonResponse);
										} else {
											printStringLn("13) Cloudant document deletion " + apiEndpoint + 
												" was not completed. Error code = " + (rstring) err +
												". Error msg = " + dpsGetLastStoreErrorString());
										}												
									}
								}
							}
						}
						
						if (revisionNumberFound == false) {
							printStringLn("13) Unable to parse the revision number of the Cloudant document. Hence, delete document operation was aborted.");
						}
						
						// 14) Let us try a different technique to get the revision number and size of a document: HEAD /db/doc
						httpVerb = "HEAD";
						apiEndpoint = "/my_db_4/Yankees";
						jsonRequest = "";
						jsonResponse = "";
						queryParams = "";								
						 
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 200ul)) {
							printStringLn("14) Obtain revision and size of a document " + apiEndpoint + 
								" was completed. JSON response = " + jsonResponse);
						} else {
							printStringLn("14) Obtain revision and size of a document " + apiEndpoint + 
								" was not completed. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}									
						
						// 4c) Let us delete a database now: DELETE /db
						cmdType = 1u;
						httpVerb = "DELETE";
						apiEndpoint = "/my_db_4";
						jsonRequest = "";
						jsonResponse = "";
						queryParams = "";

						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 200ul)) {
							printStringLn("4c) DB deletion " + apiEndpoint + 
								" was completed. JSON response = " + jsonResponse);
						} else {
							printStringLn("4c) DB deletion " + apiEndpoint + 
								" could not be completed. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}
					
						printStringLn("=== End of the native data store command execution for the Cloudant DOC level requests ===");
						// Please note that the dpsRunDataStoreCommand API can be used only in Redis, Cassandra, and Cloudant. (As of Nov/2014).
					} // End of if (dbProductName == "cloudant")					

					// We have a full fledged native command execution feature demonstration below for HBase.
					if (dbProductName == "hbase") {
						// For HBase, we will support two way commands since the request/response is done via JSON formatted strings.
						// That makes it easier to support many of the HBase data store native commands.
						// We will use the same dps API as used in Redis and Cassandra but with overloaded function arguments.
						// This overloaded API call will support these HTTP verbs: GET, PUT, POST, DELETE, and HEAD.
						// With those supported HTTP verbs, you can execute the HTTP REST APIs necessary to do the HBase CRUD operations.
						// Some good references for the HBase HTTP REST/JSON APIs:
						// http://wiki.apache.org/hadoop/Hbase/Stargate
						// https://cwiki.apache.org/confluence/display/KNOX/Examples+HBase
						//
						// DPS API format:
						// boolean dpsRunDataStoreCommand(uint32 cmdType, rstring httpVerb, rstring baseUrl,
						//                                rstring apiEndpoint, rstring queryParams, rstring jsonRequest,
						//                                mutable rstring jsonResponse, mutable uint64 err);
						//
						// This DPS API returns false when it encounters any error inside the DPS or in cURL calls before your command reaches the HBase server.
						// In the case of a false return value, you can get the error code from the err argument (See the explanation for err below.)
						// A return value of true simply means that your HTTP REST API request was sent to the HBase server and a response was received from the server.
						// In that case, you will get the HTTP response code in the err argument and you should interpret the meaning of that HTTP code to 
						// know whether your request really succeeded or not. 
						//
						// cmdType: This is not necessary when you use HBase. You can simply set it to 0u.
						//
						// httpVerb: Should be one of the supported HTTP verbs (GET, PUT, POST, DELETE, HEAD).
						// 
						// baseUrl: It must be in this format:
						//             http://user:password@HBase-REST-ServerNameOrIPAddress:port
						//          Note: If you give an empty string for the URL, then the HBase server(s) configured
						//                in the SPL project directory's etc/no-sql-kv-store-servers.cfg file will be used.
						// 
						// apiEndPoint: It should be the resource portion of the URL path as documented in the HBase REST APIs.
						//
						// queryParams: You may need to set queryParams for scanner APIs. In other cases, you can set it to an empty string.
						//
						// jsonRequest: This is your JSON request needed by the HBase API you are executing. Please ensure that any special
						//              characters such as double quotes are properly escaped using the backslash character.     
						//
						// jsonResponse: This is one of the two mutable variables you must pass to this DPS API.
						//               This argument brings back any JSON response string received from the HBase server while executing your HTTP REST request.
						//
						// err: 
						//      If this DPS API returns false, then this mutable argument will be set to any DPS or cURL errors that occurred inside the DPS code.
						//      To receive more details about the DPS or cURL errors, you can call the dpsGetLastStoreErrorString() DPS API. 
						//      If this DPS API returns true, then this argument will be set to the HTTP response code returned by the HBase server.
						//      In case of this API returning true, there will not be any additional error or status messages provided. You have to
						//      interpret the meaning of the returned HTTP response code and make your further logic from there. 
						//
						// Your input arguments given above will form the full URL inside this API: <baseUrl>/<API endpoint path> 
						//						
						// ========================= HBASE REST REQUESTS ARE SHOWN BELOW =========================
						printStringLn("=== Start of the native data store command execution for HBase ===");
						// 1a) Let us create a new table: PUT /TableName/schema
						// We are going to make a HTTP request related to table creation.
						mutable uint32 cmdType = 0u;
						mutable rstring httpVerb = "PUT";
						mutable rstring baseUrl = $HBASE_BASE_URL;   
						// Specify your new table name.
						// An API endpoint URL path must always begin with a forward slash character.
						// Similarly, in the apiEndpoint you should substitute these special characters with their encoded values:
						// Space --> "%20"
						// "+" --> "%2B"
						// "/" --> "%2F"
						mutable rstring apiEndpoint = "/my_table_1/schema";      
						mutable rstring queryParams = "";
						// All the double quotes inside the jsonRequest must be escaped.
						mutable rstring jsonRequest = "{\"name\": \"my_table_1\", " + 
							"\"ColumnSchema\": [{\"name\": \"cf1\", \"VERSIONS\": \"1\", \"IN_MEMORY\": \"TRUE\"}, " +
							                   "{\"name\": \"cf2\", \"VERSIONS\": \"1\", \"IN_MEMORY\": \"TRUE\"}, " +
							                   "{\"name\": \"cf3\", \"VERSIONS\": \"1\", \"IN_MEMORY\": \"TRUE\"}]}";
						mutable uint64 err = 0ul;
						mutable rstring jsonResponse = "";
						mutable boolean result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 201ul || err == 200ul)) {
							printStringLn("1a) HBase table creation: my_table_1" + 
								" is now available for use. JSON response = " + jsonResponse);
						} else {
							printStringLn("1a) HBase table my_table_1" + 
								" was not created. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}
						
						// 1b) Let us create a second table: PUT /TableName/schema
						apiEndpoint = "/my_table_2/schema";
						jsonRequest = "{\"name\": \"my_table_2\", " + 
							"\"ColumnSchema\": [{\"name\": \"cf1\", \"VERSIONS\": \"1\", \"IN_MEMORY\": \"TRUE\"}]}";
						jsonResponse = "";
						
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 201ul || err == 200ul)) {
							printStringLn("1b) HBase table creation: my_table_2" + 
								" is now available for use. JSON response = " + jsonResponse);
						} else {
							printStringLn("1b) HBase table my_table_2" + 
								" was not created. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}						

						// 1c) Let us create a third table: PUT /TableName/schema
						apiEndpoint = "/my_table_3/schema";
						jsonRequest = "{\"name\": \"my_table_3\", " + 
							"\"ColumnSchema\": [{\"name\": \"cf1\", \"VERSIONS\": \"1\", \"IN_MEMORY\": \"TRUE\"}]}";
						jsonResponse = "";
						
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 201ul || err == 200ul)) {
							printStringLn("1c) HBase table creation: my_table_3" + 
								" is now available for use. JSON response = " + jsonResponse);
						} else {
							printStringLn("1c) HBase table my_table_3" + 
								" was not created. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}	
						
						// 2) Let us get a list of all the tables: GET /
						httpVerb = "GET"; 
						apiEndpoint = "/";
						jsonRequest = "";
						jsonResponse = "";
						
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 200ul)) {
							printStringLn("2) List of the HBase tables " + 
								" was obtained. JSON response = " + jsonResponse);
						} else {
							printStringLn("2) List of the HBase tables" + 
								" could not be obtained. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}	
						
						// 3) Let us get the table information: GET /TableName/schema
						apiEndpoint = "/my_table_2/schema";
						jsonRequest = "";
						jsonResponse = "";
						
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 200ul)) {
							printStringLn("3) Table information for my_table_2" + 
								" was obtained. JSON response = " + jsonResponse);
						} else {
							printStringLn("3) Table information for my_table_2" + 
								" could not be obtained. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}							
						
						
						// 4a) Let us delete a table now: DELETE /TableName/schema
						httpVerb = "DELETE";
						apiEndpoint = "/my_table_2/schema";
						jsonRequest = "";
						jsonResponse = "";						

						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 200ul)) {
							printStringLn("4a) Table deletion of my_table_2" + 
								" was completed. JSON response = " + jsonResponse);
						} else {
							printStringLn("4a) Table deletion of my_table_2" + 
								" could not be completed. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}												

						// 4b) Let us delete a table now: DELETE /TableName/schema
						apiEndpoint = "/my_table_3/schema";
						jsonRequest = "";
						jsonResponse = "";						

						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 200ul)) {
							printStringLn("4b) Table deletion of my_table_3" + 
								" was completed. JSON response = " + jsonResponse);
						} else {
							printStringLn("4b) Table deletion of my_table_3" + 
								" could not be completed. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}

						// 5) Let us insert multiple rows into a table: PUT /TableName/DummyRowKeyName
						//
						// In the HBase row insertion REST API, we must give the HBase table name and a
						// dummy Row key name. Actual row key name will be sent via the JSON request string.
						// Hence, having a dummy row name (e-g: RowData) in the URL resource path is not an issue at all.
						httpVerb = "PUT";
						apiEndpoint = "/my_table_1/RowData";
						// All the double quotes in your JSON request must be escaped via a backslash character.
						// In a sing JSON request, we can pack as many rows as we want to insert.
						// In this test, we are going to insert 4 different rows in our HBase table.
						// In the HBase REST APIs, all the "ColumnFamily:ColumnQualifier" and the corresponding
						// "Cell value" must be base64 encoded. There are base64 encode/decode APIs available in our DPS.
						mutable list<rstring>[5] rk = [], cn = [], hq = [], df = [], fc = [];
						// Base64 encoded value will be filled inside the mutable string variable passed via the 2nd argument.						
						// HBase row key
						dpsBase64Encode("1", rk[0]);
						dpsBase64Encode("2", rk[1]);
						dpsBase64Encode("3", rk[2]);
						dpsBase64Encode("4", rk[3]);
						
						// HBase column key (Format: ColumnFamily:ColumnQualifier)
						dpsBase64Encode("cf1:Company", cn[0]);
						// HBase column value
						dpsBase64Encode("IBM", cn[1]);
						dpsBase64Encode("Microsoft", cn[2]);
						dpsBase64Encode("Amazon", cn[3]);
						dpsBase64Encode("Google", cn[4]);
						
						dpsBase64Encode("cf1:HQ", hq[0]);
						dpsBase64Encode("Armonk, NY", hq[1]);
						dpsBase64Encode("Redmond, WA", hq[2]);
						dpsBase64Encode("Seattle, WA", hq[3]);
						dpsBase64Encode("Mountain View, CA", hq[4]);
						
						dpsBase64Encode("cf1:Date Founded", df[0]);
						dpsBase64Encode("June 16, 1911", df[1]);
						dpsBase64Encode("April 4, 1975", df[2]);
						dpsBase64Encode("July 5, 1994", df[3]);
						dpsBase64Encode("September 4, 1998", df[4]);
						
						dpsBase64Encode("cf1:First CEO", fc[0]);
						dpsBase64Encode("Thomas J. Watson", fc[1]);
						dpsBase64Encode("Bill Gates", fc[2]);
						dpsBase64Encode("Jeff Bezos", fc[3]);
						dpsBase64Encode("Larry Page", fc[4]);
						
						// HBase put K/V pair REST API JSON request format:
						// {"Row":[{"key":"X","Cell":[{"column":"A","$":"a"}]},{"key":"Y","Cell":[{"column":"B","$":"dGVzdA=="}]}]}
						jsonRequest = 
							"{\"Row\":[" +
								"{\"key\":\"" + rk[0] + "\"," +
									"\"Cell\":[" +
										"{\"column\":\"" + cn[0] + "\",\"$\":\"" + cn[1] + "\"}," +
										"{\"column\":\"" + hq[0] + "\",\"$\":\"" + hq[1] + "\"}," +
										"{\"column\":\"" + df[0] + "\",\"$\":\"" + df[1] + "\"}," +
										"{\"column\":\"" + fc[0] + "\",\"$\":\"" + fc[1] + "\"}]}," +
								"{\"key\":\"" + rk[1] + "\"," +
									"\"Cell\":[" +
										"{\"column\":\"" + cn[0] + "\",\"$\":\"" + cn[2] + "\"}," +
										"{\"column\":\"" + hq[0] + "\",\"$\":\"" + hq[2] + "\"}," +
										"{\"column\":\"" + df[0] + "\",\"$\":\"" + df[2] + "\"}," +
										"{\"column\":\"" + fc[0] + "\",\"$\":\"" + fc[2] + "\"}]}," +
								"{\"key\":\"" + rk[2] + "\"," +
									"\"Cell\":[" +
										"{\"column\":\"" + cn[0] + "\",\"$\":\"" + cn[3] + "\"}," +
										"{\"column\":\"" + hq[0] + "\",\"$\":\"" + hq[3] + "\"}," +
										"{\"column\":\"" + df[0] + "\",\"$\":\"" + df[3] + "\"}," +
										"{\"column\":\"" + fc[0] + "\",\"$\":\"" + fc[3] + "\"}]}," +
								"{\"key\":\"" + rk[3] + "\"," +
									"\"Cell\":[" +
										"{\"column\":\"" + cn[0] + "\",\"$\":\"" + cn[4] + "\"}," +
										"{\"column\":\"" + hq[0] + "\",\"$\":\"" + hq[4] + "\"}," +
										"{\"column\":\"" + df[0] + "\",\"$\":\"" + df[4] + "\"}," +
										"{\"column\":\"" + fc[0] + "\",\"$\":\"" + fc[4] + "\"}]}]}";
										
						jsonResponse = "";								
						
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 200ul)) {
							printStringLn("5) Insertion of multiple rows in my_table_1" + 
								" was completed. JSON response = " + jsonResponse);
						} else {
							printStringLn("5) Insertion of multiple rows in my_table_1" + 
								" could not be completed. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}

						// 6) Let us retrieve all the rows from a table: GET /TableName/*
						httpVerb = "GET";
						apiEndpoint = "/my_table_1/*";
						jsonRequest = "";
						jsonResponse = "";						
						
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 200ul)) {
							printStringLn("6) Retrieve all rows from my_table_1" + 
								" was completed. JSON response = ");
							displayHBaseTableRows(jsonResponse);
						} else {
							printStringLn("6) Retrieve all rows from my_table_1" + 
								" could not be completed. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}						

						// 7) Let us retrieve all columns in a specific row: GET /TableName/RowKey
						httpVerb = "GET";
						apiEndpoint = "/my_table_1/1";
						jsonRequest = "";
						jsonResponse = "";						
						
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 200ul)) {
							printStringLn("7) Retrieve all columns from row '1' of my_table_1" + 
								" was completed. JSON response = ");
							displayHBaseTableRows(jsonResponse);
						} else {
							printStringLn("7) Retrieve all columns from row '1' of my_table_1" + 
								" could not be completed. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}										

						// 8) Let us retrieve a specific column family in a specific row: GET /TableName/RowKey/ColumnFamily
						httpVerb = "GET";
						apiEndpoint = "/my_table_1/4/cf1";
						jsonRequest = "";
						jsonResponse = "";						
						
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 200ul)) {
							printStringLn("8) Retrieve a specific column family 'cf1' from row '4' of my_table_1" + 
								" was completed. JSON response = ");
							displayHBaseTableRows(jsonResponse);
						} else {
							printStringLn("8) Retrieve a specific column family 'cf1' from row '4' of my_table_1" + 
								" could not be completed. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}

						// 9) Let us retrieve a specific column qualifier in a specific row: GET /TableName/RowKey/ColumnFamily:ColumnQualifier
						httpVerb = "GET";
						apiEndpoint = "/my_table_1/3/cf1:Company";
						jsonRequest = "";
						jsonResponse = "";						
						
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 200ul)) {
							printStringLn("9) Retrieve a specific column qualifier 'cf1:Company' from row '3' of my_table_1" + 
								" was completed. JSON response = ");
							displayHBaseTableRows(jsonResponse);
						} else {
							printStringLn("9) Retrieve a specific column qualifier 'cf1:Company' from row '3' of my_table_1" + 
								" could not be completed. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}

						// 10) Let us get meta data information about an HBase table: GET /TableName/regions
						httpVerb = "GET";
						apiEndpoint = "/my_table_1/regions";
						jsonRequest = "";
						jsonResponse = "";						
						
						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 200ul)) {
							printStringLn("10) Get meta data information about my_table_1" + 
								" was completed. JSON response = " + jsonResponse);
						} else {
							printStringLn("10) Get meta data information about my_table_1" + 
								" could not be completed. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}

						// 4c) Let us delete a table now: DELETE /TableName/schema
						httpVerb = "DELETE";
						apiEndpoint = "/my_table_1/schema";
						jsonRequest = "";
						jsonResponse = "";						

						result = dpsRunDataStoreCommand(cmdType, httpVerb, baseUrl, apiEndpoint, queryParams, jsonRequest, jsonResponse, err);
						
						if ((result == true) && (err == 200ul)) {
							printStringLn("4b) Table deletion of my_table_1" + 
								" was completed. JSON response = " + jsonResponse);
						} else {
							printStringLn("4b) Table deletion of my_table_1" + 
								" could not be completed. Error code = " + (rstring) err +
								". Error msg = " + dpsGetLastStoreErrorString());
						}
						
						// ...
						// ...
						// Important REST APIs for CRUD functions were already covered above.
						// If you are interested, you can add code for more HBase table actions via REST calls.
						// You can try these:
						// Try to update a cell value in a specific column [You can do a similar logic shown in step(5) above.]
						// Try to delete a specific row [You can do a similar logic shown in step(4c). But, with an apiEndpoint of "/TableName/RowKey"
						// Try to delete a specific column family. [You can do a similar logic shown in step(4c). But, with an apiEndpoint of "/TableName/RowKey/ColumnFamily"
						// Try to delete a specific column. [You can do a similar logic shown in step(4c). But, with an apiEndpoint of "/TableName/RowKey/ColumnFamily:ColumnQualifier"
						// ...
						// ...
						printStringLn("=== End of the native data store command execution for HBase ===");
						// Please note that the dpsRunDataStoreCommand API can be used only in Redis, Cassandra, Cloudant, and HBase. (As of Nov/2014).
					} // End of if (dbProductName == "hbase")
				}
		}	
}

stateful public void displayHBaseTableRows(rstring jsonResponse) {
	// You should properly parse it using a JSON library.
	// i.e. via your own C++ or Java native functions that can parse JSON in the right way. 
	// But, as a quick and dirty solution, we are going to use string token 
	// parsing to pull out the K/V pairs from this JSON result message.
	// Response will be in this format:
	// {"Row":[{"key":"X","Cell":[{"column":"A","timestamp":1,"$":"a"}]},{"key":"Y","Cell":[{"column":"B","timestamp":1,"$":"b"}]}]}
	//
	mutable int32 rowIdx1 = 0, rowIdx2 = 0, keyIdx1 = 0, keyIdx2 = 0, valueIdx1 = 0, valueIdx2 = 0;
	while(true) {
		// Find the next row.
		rowIdx1 = findFirst(jsonResponse, "{\"key\":", rowIdx2);
		if (rowIdx1 == -1) {
			// Row not found.
			break;
		} 
		
		// Parse the row key name.
		mutable rstring rowKey = "";
		mutable rstring base64DecodedString = "";
		mutable rstring columnKey = "";
		mutable rstring columnValue = "";
		// Find the beginning of the row key name.
		rowIdx1 = findFirst(jsonResponse, ":\"", rowIdx1);
		if (rowIdx1 == -1) {
			break;
		}
		
		// Find the end of the row key name.
		rowIdx2 = findFirst(jsonResponse, "\",", rowIdx1);
		if (rowIdx2 == -1) {
			break;
		}
		
		// Parse the row key name
		rowKey = substring(jsonResponse, rowIdx1+2, rowIdx2-(rowIdx1+2));
		dpsBase64Decode(rowKey, base64DecodedString);
		printString(base64DecodedString + "-->");
		mutable boolean firstColumnKeyFound = false;
		
		// We got our row key. Let us now collect all the K/V pairs stored in this row.
		while(true) {
			// Locate the key field.
			keyIdx1 = findFirst(jsonResponse, "column\":\"", keyIdx2);
			if (keyIdx1 == -1) {
				break;
			}
			
			// Find the end of the key field.
			keyIdx2 = findFirst(jsonResponse, "\",", keyIdx1);
			if (rowIdx2 == -1) {
				break;
			}
			
			// Parse the column key name.
			columnKey = substring(jsonResponse, keyIdx1+9, keyIdx2-(keyIdx1+9));
			dpsBase64Decode(columnKey, base64DecodedString);
			// If there are more than one K/V pair, then dispaly them with comma to separate them.
			if (firstColumnKeyFound == true) {
				printString(", ");
			}
			// Decoded column key will have the "cf1:" prefix. Let us not display that prefix.
			printString(substring(base64DecodedString, 4, length(base64DecodedString)-4) + ":");
			firstColumnKeyFound = true;
			
			// Locate the value field.
			valueIdx1 = findFirst(jsonResponse, "$\":\"", valueIdx2);
			if (valueIdx1 == -1) {
				break;
			}
			
			// Find the end of the value field.
			valueIdx2 = findFirst(jsonResponse, "\"}", valueIdx1);
			if (valueIdx2 == -1) {
				break;
			}
			
			// Parse the column value name.
			columnValue = substring(jsonResponse, valueIdx1+4, valueIdx2-(valueIdx1+4));
			dpsBase64Decode(columnValue, base64DecodedString);
			printString(base64DecodedString);
			
			// If there are no more K/V pairs beyond this, let us skip this loop.
			if (jsonResponse[valueIdx2+2] == ']') {
				printStringLn("");
				break;
			}
		}
	} 
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/905_gate_load_balancer_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/com_ibm_streamsx_ps_samples_ps_test_1_PsTest1_spl/"> > </a>
</div>

