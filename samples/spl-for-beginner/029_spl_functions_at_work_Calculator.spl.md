---
layout: samples
title: 029_spl_functions_at_work
---

### 029_spl_functions_at_work

<div class="sampleNav"><a class="button" href="../028_multiple_composites_at_work_StockOrderCommission.spl/"> < </a><a class="button" href="../029_spl_functions_at_work_Main.spl/"> > </a>
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

<div class="sampleNav"><a class="button" href="../028_multiple_composites_at_work_StockOrderCommission.spl/"> < </a><a class="button" href="../029_spl_functions_at_work_Main.spl/"> > </a>
</div>

