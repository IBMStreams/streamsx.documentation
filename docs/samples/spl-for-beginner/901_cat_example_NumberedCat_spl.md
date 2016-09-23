---
layout: samples
title: 901_cat_example
---

### 901_cat_example

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/103_view_annotation_at_work_com_acme_test_ViewAnnotationAtWork_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/902_word_count_word_count_Helpers_spl/"> > </a>
</div>

~~~~~~
/*
This example is the same code that can be found in the SPL introductory tutorial PDF file.
Please see that PDF file for a description about what this application does.
*/
composite NumberedCat {
	graph
		stream <rstring contents> Lines = FileSource() {
			param
				format: line;
				file: getSubmissionTimeValue("file");
					//file			: "catFood.txt";	
		} // End of FileSource.
		
		stream <rstring contents> Numbered = Functor(Lines) {
			logic
				state: {
					mutable int32 i = 0;
				}
				
				onTuple Lines: { 
					i++;
				}
					
			output
				Numbered: contents = (rstring)i + " " + Lines.contents;
		} // End of Functor.
		
		() as Sink = FileSink(Numbered) {
			param
				file: "result.txt";
		} // End of Sink.
} // End of NumberedCat.

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/103_view_annotation_at_work_com_acme_test_ViewAnnotationAtWork_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/902_word_count_word_count_Helpers_spl/"> > </a>
</div>

