---
layout: samples
title: 072_using_streams_rest_apis
---

### 072_using_streams_rest_apis

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/071_java_native_functions_com_acme_test_JavaNativeFunctions_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/073_java_operator_fusion_com_acme_test_JavaFusion_spl/"> > </a>
</div>

~~~~~~
/*
This example shows how the Streams REST APIs can be used within the context of an SPL application.
For illustrative purposes, we are showing a few basic REST API calls.
Using this as a base, users can simply try more REST API calls (get job health, get PE details etc.)

In order for this program to work, one has to provide values specific to his/her Streams environment.
Please edit the Java native functions in the impl/java/src directory and change the static values
defined at the top of that Java source file.

Basic template of the REST API Java code was taken from the Streams Knowledge Center. Thanks to
our Streams colleagues Janet Weber and Jason Nikolai for getting the REST API code in the Java file
correctly configured to produce the right results.
*/
namespace com.acme.test;

use com.acme.myrestfunctions::*;

composite UsingStreamsRestApis {
	graph
		stream<int8 dummy> TestData1 = Beacon() {
			param
				iterations: 1u;
		}
		
		() as MySink1 = Custom(TestData1) {
			logic
				onTuple TestData1: {
					// We will use Java functions to query a few of the Streams metrics via the REST APIs.
					// In order to exercise the REST APIs, you must have your Streams instance running.
					//
					// Before running this example, you must edit the Java native functions in the impl/java/src directory and
					// enter several values for userid, password, domain name, instance name etc. at the top of that Java file to suit you environment.
					//
					printStringLn("REST API call results below are correct only if you started your instance.");
					printStringLn("Streams root resource information = " + getStreamsRootResourceInfo());
					printStringLn("Streams instance information = " + getStreamsInstanceInfo());
					printStringLn("Streams host information = " + getStreamsHostInfo());
					//
					// You can refer to the Streams Knowledge Center documentation and add more REST API calls to test here.
					
				}
		}
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/071_java_native_functions_com_acme_test_JavaNativeFunctions_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/073_java_operator_fusion_com_acme_test_JavaFusion_spl/"> > </a>
</div>

