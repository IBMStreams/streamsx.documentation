---
layout: samples
title: 022_deduplicate_at_work
---

### 022_deduplicate_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/021_pair_at_work_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/023_union_at_work_my_sample_Main_spl/"> > </a>
</div>

~~~~~~
/*
This example describes the use of an important operator that is highly applicable
in many telco scenarios. That operator is called DeDuplicate, which eliminates
duplicate tuples for a specified duration of time. It has two output ports.
In the first output port, all the non-duplicate tuples are sent. In the 
optional second output port, all the duplicate tuples are sent.
*/
namespace my.sample;

composite Main {
	type
		bookInfo = tuple<rstring title, rstring isbn, rstring author, rstring publisher, float32 price>;
		
	graph
		stream <bookInfo> DefaultBoolInfo1 = Beacon() {
			param
				iterations: 100u;
		} // End of BookInfo1 = Beacon()

		// In a custom operator, let us set the attributes of the BookInfo1 tuples.
		stream<bookInfo> BookInfo1 = Custom(DefaultBoolInfo1 as DBF1) {
			logic
				state: mutable uint32 cnt = 0;
				
				onTuple DBF1: {
					++cnt;
					
					DBF1 = {
						title = "Title" + (rstring)cnt,
						isbn = "ISBN" + (rstring)cnt,
						author= "Author" + (rstring)cnt,
						publisher = "Publisher" + (rstring)cnt,
						price= (float32)random()*(float32)100.0				
					};
					
					submit(DBF1, BookInfo1);
				} // End of onTuple DBF1	
		} // End of Custom(DefaultBoolInfo1)
	
		stream <bookInfo> BookInfo2 = Custom(BookInfo1) {
			logic
				state: 
					mutable uint32 cnt = 0u;
				
			onTuple BookInfo1: {
				// Submit once.
				submit(BookInfo1, BookInfo2);
				
				// We will duplicate every other tuple.
				if (++cnt%2u == 0u) {
					submit(BookInfo1, BookInfo2);
				} // End of if (++cnt%2u == 0)
			} // End of onTuple BookInfo1						
		} // End of BookInfo2 = Custom(BookInfo1)
		
		// Let us filter the duplicate tuples now.
		(stream <bookInfo> BookInfo3; stream <bookInfo> BookInfo4) = DeDuplicate(BookInfo2) {
			param
				// If you don't specifiy the timeOut parameter, it will deduplicate for 10 minutes by default.
				timeOut: 120.0;
				// If you don't specify the key parameter, then it will use the whole tuple for duplicate comparison algorithm.
				key: title, isbn, author, publisher, price;
		} // End of BookInfo3 = DeDuplicate(BookInfo2)
		
		// Now let us connect to the non-duplicate tuples sent by the Deduplicate operator.
		() as ScreenWriter1= Custom(BookInfo3) {
			logic
				state: 
					mutable int32 nonDuplicateTupleCnt = 0;
				
				onTuple BookInfo3: {
					if (nonDuplicateTupleCnt++ == 0) {
						printStringLn("\na)Non-Duplicate tuples sent by the Deduplicate operator:");
					} // End of if (nonDuplicateTupleCnt++ == 0)
					
					printStringLn ((rstring) nonDuplicateTupleCnt + "a)" + (rstring) BookInfo3);
				} // End of onTuple BookInfo3
		} // End of ScreenWriter1 = Custom(BookInfo3)
		
		// Now let us connect to the duplicate tuples sent by the Deduplicate operator.
		() as ScreenWriter2= Custom(BookInfo4) {
			logic
				state: 
					mutable int32 duplicateTupleCnt = 0;
				
				onTuple BookInfo4: {
					if (duplicateTupleCnt++ == 0) {
						printStringLn("\nb)Duplicate tuples sent by the Deduplicate operator:");
					} // End of if (duplicateTupleCnt++ == 0)
					
					printStringLn ((rstring) duplicateTupleCnt + "b)" + (rstring) BookInfo4);
				} // End of onTuple BookInfo4
		} // End of ScreenWriter2 = Custom(BookInfo4)
} // End of the main composite.

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/021_pair_at_work_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/023_union_at_work_my_sample_Main_spl/"> > </a>
</div>

