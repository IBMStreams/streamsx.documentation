---
layout: samples
title: 902_word_count
---

### 902_word_count

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/902_word_count_word_count_Helpers_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/903_unique_Main_spl/"> > </a>
</div>

~~~~~~
/*
This example is the same code that can be found in the SPL introductory tutorial PDF file.
Please see that PDF file for a description about what this application does.
*/
namespace word.count;

composite WordCount {
	graph
		stream <rstring lineContents> Data = FileSource() {
			param
				format: line;
				file: getSubmissionTimeValue("file");
				// file		: "catFood.txt";
		} // End of FileSource.
		
		stream <LineStat> OneLine = Functor(Data) {
			output
				OneLine: 
					lines = 1, words = countWords(lineContents);
		} // End of Functor.
		
		() as Counter = Custom(OneLine) {
			logic
				state: mutable LineStat sum = {lines = 0, words =0};
				
				onTuple OneLine: 
					addStat (sum, OneLine);

				onPunct OneLine: {
					if (currentPunct() == Sys.FinalMarker) {println(sum);}
				} // End of onPunct OneLine
		} // End of Custom.
} // End of WordCount.

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/902_word_count_word_count_Helpers_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/903_unique_Main_spl/"> > </a>
</div>

