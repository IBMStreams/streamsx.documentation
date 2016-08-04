---
layout: samples
title: 008_get_submission_time_value
---

### 008_get_submission_time_value

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/007_split_at_work_sample_split_at_work_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/009_custom_operator_using_get_submission_time_value_Main_spl/"> > </a>
</div>

~~~~~~
/*
This example shows how the tuple attributes can be assigned values
that were supplied by the user at the application/job submission time.
It employs the getSubmissionTimeValue function to obtain different
values made of different SPL data types. 

When you launch this application from the IDE, you will be asked to
enter the submission time values in the application launch dialog.

You have to provide four different parameters. Some parameters are
expected as a list as shown below.

param1=10
param2=56
param3=45,46,47
param4=67,68
*/
composite Main {
	type 
		myTuple1 = tuple <int32 i, int32 j>; 
		myTuple2 = tuple<rstring str1, rstring str2, rstring str3, rstring str4, rstring str5, rstring str6, rstring str7>;
		myTuple3 = tuple<myTuple1, myTuple2>;
	
	graph
		stream <myTuple1> Input = Beacon() {							
			logic	state:	{
				mutable int32 m=0; 
				mutable int32 n=0;
			}
			
			param 
				iterations:	2u;			
			
			output 
				Input: i = ++m, j = ++n;
		} // End of Beacon.

		stream <myTuple3> Output = Functor(Input) {
			output 
				Output:
					i = Input.i, 
					j = Input.j,
					// Note that param1 has a default value.
					// param2 is a primitive type.
					// param3 and param4 are list types with 3 and 2 elements respecively.
					str1 = getSubmissionTimeValue ("param1", "5"),
					str2 = getSubmissionTimeValue ("param2"),
					str3 = getSubmissionTimeListValue("param3") [0],
					str4 = getSubmissionTimeListValue("param3") [1],
					str5 = getSubmissionTimeListValue("param3") [2],
					str6 = getSubmissionTimeListValue("param4") [0],
					str7 = getSubmissionTimeListValue("param4") [1];				
		} // End of Functor(Input)
		
		() as ScreenWriter = Custom(Output) {
			logic 
				onTuple Output: 
					printStringLn("The tuple = " + (rstring)Output + "\n");
		} // End of Custom(Output)
} // End of composite Main.


~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/007_split_at_work_sample_split_at_work_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/009_custom_operator_using_get_submission_time_value_Main_spl/"> > </a>
</div>

