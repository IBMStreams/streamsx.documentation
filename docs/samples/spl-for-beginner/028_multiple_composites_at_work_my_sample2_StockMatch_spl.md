---
layout: samples
title: 028_multiple_composites_at_work
---

### 028_multiple_composites_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/028_multiple_composites_at_work_my_sample1_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/028_multiple_composites_at_work_my_sample3_StockOrderCommission_spl/"> > </a>
</div>

~~~~~~
namespace my.sample2;

public composite StockMatch(output Output; input Input) {		
	param
		expression <rstring> $matchTradeType;
		expression <uint32> $minimumMatchQuantity;
		expression <float32> $minimumMatchPrice;

	type
		stockOrder = tuple<rstring symbol, float32 price, uint32 quantity, rstring tradeType, boolean matchFound, float32 commission>;
	
	graph
		stream <stockOrder> ResultFromStockMatch = Functor(Input) {
			param
				filter: (symbol == "IBM" || symbol == "AAPL") &&
					   (tradeType == $matchTradeType) &&
					   (quantity >= $minimumMatchQuantity) &&
					   (price >= $minimumMatchPrice);
			
			output
				ResultFromStockMatch: matchFound = true;
		} // End of ResultFromStockMatch = Functor(Input)
	
		// Send this tuple out now.
		stream <stockOrder> Output = Custom(ResultFromStockMatch) {
			logic
				onTuple ResultFromStockMatch:
					submit(ResultFromStockMatch, Output);
		} // End of Output = Custom(ResultFromStockMatch)
} // End of StockMatch(output Output; input Input)

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/028_multiple_composites_at_work_my_sample1_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/028_multiple_composites_at_work_my_sample3_StockOrderCommission_spl/"> > </a>
</div>

