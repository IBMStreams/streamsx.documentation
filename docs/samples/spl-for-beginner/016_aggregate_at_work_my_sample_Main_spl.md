---
layout: samples
title: 016_aggregate_at_work
---

### 016_aggregate_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/015_join_at_work_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/017_filesource_filesink_at_work_my_sample_Main_spl/"> > </a>
</div>

~~~~~~
/*
This example shows off yet another powerful standard toolkit operator named
the Aggregate. It is very good in computing on the fly aggregate values by
collecting a set of tuples. Tuples are grouped based on tumbling and sliding
windows with partitioned variants. This example also shows how to use the
built-in assignment functions provided by this operator to compute regular
statistical calculations such as min, max, average, standard deviation etc.
*/
namespace my.sample;

composite Main {
	type
		cityData = tuple<rstring city, rstring country, uint32 population, uint32 medianAge, uint32 percentageEducated>;
		aggregatedCityData = tuple<uint32 maxPopulation, uint32 maxMedianAge, uint32 minMedianAge, uint32 minEducated>;
	
	graph
		stream <cityData> CityDataRecord = FileSource() {
			param
				file:	"Population.txt";
				format:	csv;
				hasDelayField: true;
				initDelay: 2.0;			
		} // End of CityDataRecord = FileSource()
		
		// Simple data aggregation using a tumbling time window.
		stream <aggregatedCityData> SimpleAggregationResult = Aggregate(CityDataRecord) {
			window
				CityDataRecord: tumbling, time(6);
			
			output
				SimpleAggregationResult:
					maxPopulation = Max(population),
					maxMedianAge = Max(medianAge),
					minMedianAge = Min(medianAge),
					minEducated = Min(percentageEducated);
		} // End of SimpleAggregationResult = Aggregate()
	
		// Data aggregation using group by clause.
		stream <aggregatedCityData, tuple<rstring city, rstring country>> GroupByAggregationResult = Aggregate(CityDataRecord) {
			window
				CityDataRecord: tumbling, time(6);

			param
				groupBy: city, country;				
			
			output
				GroupByAggregationResult:
					maxPopulation = Max(population),
					maxMedianAge = Max(medianAge),
					minMedianAge = Min(medianAge),
					minEducated = Min(percentageEducated);
		} // End of GroupByAggregationResult = Aggregate()		

		// Data aggregation using a sliding window.
		stream <aggregatedCityData, tuple<rstring city, rstring country>> SlidingWindowAggregationResult = Aggregate(CityDataRecord) {
			window
				CityDataRecord: sliding, count(5), count(2);
				
			param
				groupBy: country;				
			
			output
				SlidingWindowAggregationResult:
					maxPopulation = Max(population),
					maxMedianAge = Max(medianAge),
					minMedianAge = Min(medianAge),
					minEducated = Min(percentageEducated);
		} // End of SlidingWindowAggregationResult = Aggregate()				

		() as ScreenWriter1 = Custom(SimpleAggregationResult) {
			logic
				onTuple SimpleAggregationResult: {
					printStringLn("\na) Simple data aggregation result with tumbling time(6)");
					printStringLn ((rstring) SimpleAggregationResult);
				} // End of onTuple SimpleAggregationResult
		} // End of Custom(SimpleAggregationResult)		

		() as ScreenWriter2 = Custom(GroupByAggregationResult) {
			logic
				onTuple GroupByAggregationResult: {
					printStringLn("\nb) GroupBy aggregation result with tumbling time(6)");
					printStringLn ((rstring) GroupByAggregationResult);
				} // End of onTuple GroupByAggregationResult
		} // End of Custom(GroupByAggregationResult)

		() as ScreenWriter3 = Custom(SlidingWindowAggregationResult) {
			logic
				onTuple SlidingWindowAggregationResult: {
					printStringLn("\nc) Sliding Window aggregation result with sliding count(5), count(2)");
					printStringLn ((rstring) SlidingWindowAggregationResult);
				} // End of onTuple SlidingWindowAggregationResult
		} // End of Custom(SlidingWindowAggregationResult)			
		
} // End of composite Main.

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/015_join_at_work_my_sample_Main_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/017_filesource_filesink_at_work_my_sample_Main_spl/"> > </a>
</div>

