---
layout: samples
title: 070_convert_block_data_into_tuples_using_parse
---

### 070_convert_block_data_into_tuples_using_parse

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/069_changing_map_value_during_iteration_com_acme_test_ChangeCollectionValue_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/071_java_native_functions_com_acme_test_JavaNativeFunctions_spl/"> > </a>
</div>

~~~~~~
/*
This example shows how a block of data can be ingested and then individual tuples
can be parsed out of that data block. It is a very tiny example. But, it demonstrates
one of the ways in which the Parse operator can be put to use.

Following code block was obtained from the Streams InfoCenter. Full credit goes to
the authors of the Streams InfoCenter. 
*/
namespace com.acme.test;

composite ConvertBlockDataWithParse {
	graph
		// Read a block of data from a file.
		stream<blob b> TestData1 = FileSource() {
			param
				file: "test1.txt";
				format: block;
				blockSize: 1u;
		}
		
		// Parse every line in the blob and send it as an individual tuple.
		stream<rstring s, float64 d, rstring q> ParsedData = Parse(TestData1) {
			param
				format: txt;
		}
		
		// Display each tuple on the stdout.
		() as MySink1 = FileSink(ParsedData) {
			param
				file: "/dev/stdout";
				format: txt;
		}
}

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/069_changing_map_value_during_iteration_com_acme_test_ChangeCollectionValue_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/071_java_native_functions_com_acme_test_JavaNativeFunctions_spl/"> > </a>
</div>

