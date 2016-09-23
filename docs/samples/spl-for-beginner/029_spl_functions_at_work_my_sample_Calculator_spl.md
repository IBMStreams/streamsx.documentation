---
layout: samples
title: 029_spl_functions_at_work
---

### 029_spl_functions_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/028_multiple_composites_at_work_my_sample3_StockOrderCommission_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/029_spl_functions_at_work_my_sample_Main_spl/"> > </a>
</div>

~~~~~~
// This file includes the SPL functions used in this application.
namespace my.sample;

type arithmeticOperation = tuple<rstring operation, uint32 operand1, uint32 operand2, uint32 result>;

public uint32 addition(uint32 operand1, uint32 operand2) {
	return(operand1 + operand2);
} // End of function addition.

public uint32 subtraction(uint32 operand1, uint32 operand2) {
	return(operand1 - operand2);
} // End of function subtraction.

public uint32 multiplication(uint32 operand1, uint32 operand2) {
	return(operand1 * operand2);
} // End of function multiplication.

public uint32 division(uint32 operand1, uint32 operand2) {
	return(operand1 / operand2);
} // End of function addition.

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/028_multiple_composites_at_work_my_sample3_StockOrderCommission_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/029_spl_functions_at_work_my_sample_Main_spl/"> > </a>
</div>

