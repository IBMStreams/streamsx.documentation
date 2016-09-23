---
layout: samples
title: 005_throttle_at_work
---

### 005_throttle_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/004_delay_at_work_sample_delay_at_work_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/006_barrier_at_work_sample_barrier_at_work_spl/"> > </a>
</div>

~~~~~~
/*
This example shows how a stream can be throttled to flow at a
specified rate. This example also mixes other operators such as
Beacon, Custom, and FileSink.
*/
namespace sample;

composite throttle_at_work {
	type ProductInfo = tuple <timestamp ts, rstring productName, uint32 productId, rstring description, float64 price, boolean freeShipping>;

	graph
		stream <ProductInfo> Product = Beacon() {
			param 
				iterations: 500u;
      	} // End of Beacon.

		stream<ProductInfo> ThrottledProduct = Throttle(Product) {
			param
				rate: 50.0;
		} // End of Throttle.

		stream<ProductInfo> CustomizedProduct = Custom(ThrottledProduct as newProduct) {
			logic 
				state:
					mutable uint32 productCnt = 0; 

				onTuple newProduct: {
					productCnt++;
					ProductInfo productInfo = 
						{ts = newProduct.ts, productName = "Product" + (rstring)productCnt, productId = productCnt,
						description = "Description" + (rstring)productCnt, price = (float64)(random()*10.0),
						freeShipping = ((productCnt%(uint32)2) == (uint32)0 ? true : false)};
						submit(productInfo, CustomizedProduct);
				} // End of onTuple newProduct.
		} // End of Custom(ThrottledProduct)

		// Write the arriving tuples to a File sink.
		() as FileWriter = FileSink(CustomizedProduct) {
			param file: "MyResults.txt";
		} // End of FileSink.      
} // End of composite throttle_at_work.

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/004_delay_at_work_sample_delay_at_work_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/006_barrier_at_work_sample_barrier_at_work_spl/"> > </a>
</div>

