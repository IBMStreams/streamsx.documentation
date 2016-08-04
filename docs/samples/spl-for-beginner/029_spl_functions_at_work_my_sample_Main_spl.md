---
layout: samples
title: 029_spl_functions_at_work
---

### 029_spl_functions_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/029_spl_functions_at_work_my_sample_Calculator_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/030_spl_config_at_work_my_sample3_Main_spl/"> > </a>
</div>

~~~~~~
/*
This example shows how helper and utility functions can be written using the
SPL language. It also shows how those SPL functions can be put to use inside
the context of an application. Learning this simple concept will go a long 
way in doing a lot of neat stuff in real-world applications.

All the SPL functions to perform different arithmetic calculations are
defined in a separate SPL file (Calculator.spl) in this project directory.
*/
namespace my.sample;

composite Main {		
	graph
		stream <arithmeticOperation> ArithmeticOperation = FileSource() {
			param
				file: "Calculator_Input.txt";
				format: csv;
				hasDelayField: true;
		} // End of ArithmeticOperation = FileSource()
		
		// A custom operator executes the required calculator SPL funtions to 
		// get the required result.
		stream <arithmeticOperation> CalculatorResult = Custom(ArithmeticOperation) {
			logic
				state: {
					mutable uint32 cnt = 0u;
					mutable tuple<ArithmeticOperation> myOutput = {};
				} // End of state:
					
				onTuple ArithmeticOperation: {
					if (cnt++ == 0u) {
						printStringLn("a) Results of the Arithmetic operations:");
						printStringLn("=====================");
					} // End of if (++cnt == 0)
					
					myOutput = ArithmeticOperation;
					
					if (ArithmeticOperation.operation == "Add") {
						myOutput.result = addition(ArithmeticOperation.operand1, ArithmeticOperation.operand2);
					} else if (ArithmeticOperation.operation == "Subtract") {
						myOutput.result = subtraction(ArithmeticOperation.operand1, ArithmeticOperation.operand2);
					} else if (ArithmeticOperation.operation == "Multiply") {
						myOutput.result = multiplication(ArithmeticOperation.operand1, ArithmeticOperation.operand2);
					} else if (ArithmeticOperation.operation == "Divide") {
						myOutput.result = division(ArithmeticOperation.operand1, ArithmeticOperation.operand2);
					} // End of if (ArithmeticOperation.operation == "Add")
					
					printStringLn((rstring) cnt + "a) Operation: " + myOutput.operation);
					printStringLn("Operand1: " + (rstring) myOutput.operand1);
					printStringLn("Operand2: " + (rstring) myOutput.operand2);
					printStringLn("Result: " + (rstring) myOutput.result);
					printStringLn("=====================");
				} // End of onTuple ArithmeticOperation
		} // End of CalculatorResult = Custom(ArithmeticOperation)
} // End of composite Main

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/029_spl_functions_at_work_my_sample_Calculator_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/030_spl_config_at_work_my_sample3_Main_spl/"> > </a>
</div>

