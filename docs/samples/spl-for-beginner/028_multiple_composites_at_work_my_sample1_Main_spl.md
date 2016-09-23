---
layout: samples
title: 028_multiple_composites_at_work
---

### 028_multiple_composites_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/027_java_op_at_work_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/028_multiple_composites_at_work_my_sample2_StockMatch_spl/"> > </a>
</div>

~~~~~~
/*
This example shows the use of multiple composites in a single application. 
There is a main composite that in turn uses two other composites. This application
shows how the additional composites in different namespaces get included into
the main composite via the "use" directive. It also demonstrates how the additional
composites can accept their own operator parameters. It teaches the basics of an 
important feature that will come handy when big applications need to be componentized. 
*/
namespace my.sample1;
use my.sample2::StockMatch;
use my.sample3::StockOrderCommission;

composite Main {
	type
		stockOrder = tuple<rstring symbol, float32 price, uint32 quantity, rstring tradeType, boolean matchFound, float32 commission>;
	
	graph
		stream <stockOrder> StockOrderRecord = FileSource() {
			param
				file: "StockOrders.txt";
				format: csv;
				initDelay: 3.0f;
				hasDelayField: true;
		} // End of StockOrderRecord = FileSource()
		
		// Call a composite to decide if this stock order has a match.
		stream <stockOrder> MatchStockOrderResult = StockMatch(StockOrderRecord) {
			param
				matchTradeType: "buy";
				minimumMatchQuantity: 100u;
				minimumMatchPrice: (float32)50.45f;
		} // End of MatchStockOrderResult = StockMatch(StockOrderRecord)
		
		// Call a composite to compute the commission fee.
		stream <stockOrder> MatchedStockOrder = StockOrderCommission(MatchStockOrderResult) {			
		} // End of MatchedStockOrder = StockOrderCommission(MatchStockOrderResult)
		
		// Display the resulting order matched tuples on the console.
		() as ScreenWriter1 = Custom(MatchedStockOrder) {
			logic
				state:
					mutable uint32 cnt = 0u;
			
				onTuple MatchedStockOrder: {
					if (cnt++ == 0u) {
						printStringLn("\na) Matched stock orders:");
					} // End of if (cnt++ == 0)
					
					printStringLn ((rstring) cnt + "a) " + (rstring) MatchedStockOrder);
				} // End of onTuple MatchedStockOrder
		} // End of ScreenWriter1 = Custom(MatchedStockOrder)
} // End of composite Main

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/027_java_op_at_work_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/028_multiple_composites_at_work_my_sample2_StockMatch_spl/"> > </a>
</div>

