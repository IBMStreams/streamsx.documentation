---
layout: samples
title: 028_multiple_composites_at_work
---

### 028_multiple_composites_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/028_multiple_composites_at_work_my_sample2_StockMatch_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/029_spl_functions_at_work_my_sample_Calculator_spl/"> > </a>
</div>

~~~~~~
namespace my.sample3;

public composite StockOrderCommission (output Output; input Input) {
	type
		stockOrder = tuple<rstring symbol, float32 price, uint32 quantity, rstring tradeType, boolean matchFound, float32 commission>;

	graph
		// All we need to here is to create a random commission fee
		// for the matched orders sent to us.
		stream <stockOrder> Output = Custom(Input) {
			logic
				state:
					mutable tuple <stockOrder> myOutput = {};

				onTuple Input: {										
					myOutput.symbol = Input.symbol;
					myOutput.price = Input.price;
					myOutput.quantity = Input.quantity;
					myOutput.tradeType = Input.tradeType;
					myOutput.matchFound = Input.matchFound;
					myOutput.commission = (float32) random()* (float32)10.0f;
					
					// Send it away.
					submit(myOutput, Output);
				} // End of OnTuple Input:
		} // End of Output = Custom(Input)
} // End of composite StockOrderCommission


~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/028_multiple_composites_at_work_my_sample2_StockMatch_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/029_spl_functions_at_work_my_sample_Calculator_spl/"> > </a>
</div>

