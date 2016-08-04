---
layout: samples
title: 095_consistent_region_spl_06
---

### 095_consistent_region_spl_06

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/095_consistent_region_spl_06_com_acme_test_ConsistentRegion6_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/096_consistent_region_cpp_07_com_acme_test_ConsistentRegion7_spl/"> > </a>
</div>

~~~~~~
/*
============================================================================
This is an utility application that is used to pump test data for testing
the ConsistentRegion6 application located in this same project directory.
After starting the ConsistentRegion6 application, you can start this
TCPDataSender application to get the data flowing via TCP sockets. 
============================================================================ 
*/
namespace com.acme.test;

composite TCPDataSender {
	graph
		// This entire graph is not in the consistent region.
		// It is simply an application to send data via TCP.
		stream<int32 i, rstring str> TestData = Beacon() {
			param
				iterations: 100000;
				initDelay: 4.0;
				
			output
				TestData: i = (int32)IterationCount() + 1,
					str = "A" + (rstring)((int32)IterationCount() + 1);
		}
		
		() as MySink1 = TCPSink(TestData) {
			param
				format: csv;
				flush: 1u;
				role: client;
				// Following is the name used in the TCPSource of the main application in this project.
				// That name will be registered with the Streams runtime nameservice which will
				// provide the necessary network address and the TCP port.
				name: "ConsistentRegion6-TCP";
				reconnectionPolicy: InfiniteRetry;
				retryFailedSends: true;
		}		
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/095_consistent_region_spl_06_com_acme_test_ConsistentRegion6_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/096_consistent_region_cpp_07_com_acme_test_ConsistentRegion7_spl/"> > </a>
</div>

