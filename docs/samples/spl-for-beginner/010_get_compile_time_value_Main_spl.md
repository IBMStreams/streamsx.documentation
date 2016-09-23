---
layout: samples
title: 010_get_compile_time_value
---

### 010_get_compile_time_value

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/009_custom_operator_using_get_submission_time_value_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/011_compiler_intrinsic_functions_Main_spl/"> > </a>
</div>

~~~~~~
/*
This example shows how arguments supplied during the 
application compile time can be accessed inside of the SPL applications.
In the Streams Studio, these values can be entered by editing the
active build configuration to provide additional SPL compiler
options in the resulting build configuration dialog.

You have to provide compile time parameters in the compiler dialog for
the given launch configuration.

For this project, those compile time values are already configured.

You can check that by right clicking on the "Standalone" launch in
the project explorer here and then by selecting "Edit". In the
resulting dialog, you can click on "Other" to see the compile-time
parameters entered in there. 
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
					// Note that, param1 has a default value.
					// These values must be provided during application compile time.
					str1 = getCompileTimeValue ("param1", "5"),
					str2 = getCompileTimeValue ("param2"),
					str3 = getCompileTimeListValue("param3") [0],
					str4 = getCompileTimeListValue("param3") [1],
					str5 = getCompileTimeListValue("param3") [2],
					str6 = getCompileTimeListValue("param4") [0],
					str7 = getCompileTimeListValue("param4") [1];				
		} // End of Functor(Input)
		
		() as ScreenWriter = Custom(Output) {
			logic
				onTuple Output:
					printStringLn("The tuple = " + (rstring)Output + "\n");
		} // End of Custom(Output)
} // End of composite Main.


~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/009_custom_operator_using_get_submission_time_value_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/011_compiler_intrinsic_functions_Main_spl/"> > </a>
</div>

