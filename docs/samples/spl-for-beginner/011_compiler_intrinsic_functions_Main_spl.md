---
layout: samples
title: 011_compiler_intrinsic_functions
---

### 011_compiler_intrinsic_functions

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/010_get_compile_time_value_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/012_filter_functor_at_work_my_sample_Main_spl/"> > </a>
</div>

~~~~~~
/*
Streams compiler provides several intrinsic functions to query the SPL filename,
file path, absolute path of the directory, source code line number, composite instance name etc.
This example shows the use of the compiler intrinsic functions inside of a Functor operator.
*/
composite Main {
	type
		myTuple = tuple <rstring fileName, rstring filePath, rstring fileDir, int32 fileLine, rstring compositeInstanceName, int32 inputPortIndex, int32 outputPortIndex>;
	
	graph
		stream <myTuple> Input = Beacon() {
			param 
				iterations: 2u;
			
			output 
				Input: fileName="File.spl", filePath="/Dir1/SubDir1/File.spl", fileDir="/Dir1/SubDir1",
					   fileLine=-1, compositeInstanceName="InstName", inputPortIndex=-1, outputPortIndex=-1;			
		} // End of Beacon.
		
		stream <myTuple> TupleWithCompilerIntrinsicValues as MyOutput = Functor(Input as MyInput) {
			output 
				TupleWithCompilerIntrinsicValues: 
					fileName = getThisFileName(),
					filePath = getThisFilePath(),
					fileDir = getThisFileDir(),
					fileLine = getThisLine(),
					compositeInstanceName = getThisCompositeInstanceName(),
					inputPortIndex = inputPort(MyInput),
					outputPortIndex = outputPort(MyOutput);
		} // End of Functor(Input).

		() as ScreenWriter = Custom(TupleWithCompilerIntrinsicValues) {
			logic 
				onTuple TupleWithCompilerIntrinsicValues: 
					printStringLn("Tuple with complier intrinsic values=" + (rstring)TupleWithCompilerIntrinsicValues + "\n");
		} // End of Custom(TupleWithCompilerIntrinsicValues).
} // End of composite Main

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/010_get_compile_time_value_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/012_filter_functor_at_work_my_sample_Main_spl/"> > </a>
</div>

