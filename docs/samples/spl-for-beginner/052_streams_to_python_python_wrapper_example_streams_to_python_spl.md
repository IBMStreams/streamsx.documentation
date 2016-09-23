---
layout: samples
title: 052_streams_to_python
---

### 052_streams_to_python

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/051_native_functions_with_collection_types_com_ibm_nf_test_native_functions_with_collection_types_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/053_java_primitive_operator_with_complex_output_tuple_types_com_acme_test_java_primitive_operator_with_complex_output_tuple_types_spl/"> > </a>
</div>

~~~~~~
/*
===========================================================================
This SPL file includes a very simple application flow graph that
demonstrates calling python code within Streams. Simple scenario used here
for this purpose is to take a URL string and call python functions to
get back the corresponding IP Address for a given URL.

First created on: Jan/21/2013
Last modified on: Feb/08/2013
===========================================================================
*/
namespace python.wrapper.example;

composite streams_to_python {
	// Define input and output schema for this application.
	type
		InputSchema = tuple<rstring url>;
		OutputSchema = tuple<rstring url, rstring primaryHostName, 
			rstring alternateHostNames, rstring ipAddressList, rstring companyName>;
		
	graph
		// Read from an input file all the URLs for which we need to 
		// get the corresponding IP addresses.
		stream<InputSchema> UrlInput = FileSource() {
			param
				file: "UrlInput.csv";
				initDelay: 4.0;
		} // End of UrlInput = FileSource()

		// In the custom operator below, we will call python code to get the
		// primary host name, alternative host names, and IP addresses.
		stream<OutputSchema> IpAddressOfUrl = Custom(UrlInput) {
			logic
				onTuple UrlInput: {
					mutable rstring _primaryHostName = "";
					mutable rstring _alternateHostNames = "";
					mutable rstring _ipAddressList = "";
					mutable rstring _companyName = "";
					// Call the C++ native function that in turn will
					// call Python functions.
					boolean result = getIpAddressFromUrl(UrlInput.url, _primaryHostName,
						_alternateHostNames, _ipAddressList, _companyName);
						
					if (result == true) {
						mutable OutputSchema _oTuple = {};
						_oTuple.url = UrlInput.url;
						_oTuple.primaryHostName = _primaryHostName;
						_oTuple.alternateHostNames = _alternateHostNames;
						_oTuple.ipAddressList = _ipAddressList;
						_oTuple.companyName = _companyName;
					
						submit(_oTuple, IpAddressOfUrl);
					}
				} // End of onTuple UrlInput
		} // End of IpAddressOfUrl = Custom(UrlInput)
		
		// Write the results to a file using FileSink.
		() as FileWriter1 = FileSink(IpAddressOfUrl) {
			param
				file: "UrlToIpAddress-Result.csv";
		} // End of FileWriter1 = FileSink(IpAddressOfUrl)
} // End of composite streams_to_python

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/051_native_functions_with_collection_types_com_ibm_nf_test_native_functions_with_collection_types_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/053_java_primitive_operator_with_complex_output_tuple_types_com_acme_test_java_primitive_operator_with_complex_output_tuple_types_spl/"> > </a>
</div>

