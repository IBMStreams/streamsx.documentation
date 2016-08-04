---
layout: samples
title: 006_barrier_at_work
---

### 006_barrier_at_work

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/005_throttle_at_work_sample_throttle_at_work_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/007_split_at_work_sample_split_at_work_spl/"> > </a>
</div>

~~~~~~
/*
This example shows how to synchronize the incoming tuples using a 
Barrier operator. It uses a bank deposit/debit scenario to 
split the deposit/debit requests, perform that account activity,
and then combine the post-activity results with the incoming requests.
Barrier operator provides what is needed to accomplish that. 
*/
namespace sample;

composite barrier_at_work {
	type 
		BankTxSchema = uint32 accountNumber, rstring txType, float64 currentBalance, float64 txAmount;
		DepositInputSchema = uint32 accountNumber, float64 currentBalance, float64 depositAmount;
		DebitInputSchema = uint32 accountNumber, float64 currentBalance, float64 debitAmount;
		TxResultSchema = float64 newBalance;
		PostTxResultSchema = uint32 accountNumber, float64 currentBalance;

	graph
		// Read the bank transaction details one at a time.
		stream <BankTxSchema> TxData = FileSource() {
			param
				file : "bank_tasks.dat";
				format: csv;
		} // End of FileSource.
      
      	// Apply filter to pick the deposit requests.
		stream <DepositInputSchema> DepositRequest = Functor(TxData) {
			param 
				filter: txType == "Deposit";
				
			output 
				DepositRequest: depositAmount = txAmount;
		} // End of Functor(TxData)

		// Apply filter to pick the debit requests.
		stream <DebitInputSchema> DebitRequest = Functor(TxData) {
			param 
				filter: txType == "Debit";
				
			output 
				DebitRequest: debitAmount = txAmount;
		} // End of Functor(TxData)

		// Compute the new balance because of the deposit activity.
		stream <TxResultSchema> DepositResult = Functor(DepositRequest) {
			output 
				DepositResult: newBalance = currentBalance + depositAmount;
		} // End of Functor(DepositRequest)

		// Compute the new balance because of the debit activity.
		stream <TxResultSchema> DebitResult = Functor(DebitRequest) {
			output 
				DebitResult: newBalance = currentBalance - debitAmount;
		} // End of Functor(DebitRequest)

		// Use a barrier to synchronize the deposit request and result.
		stream <PostTxResultSchema> FinalDepositResult = Barrier(DepositRequest; DepositResult) {
			output 
				FinalDepositResult: accountNumber = DepositRequest.accountNumber, currentBalance = DepositResult.newBalance;
		} // End of Barrier(DepositRequest; DepositResult)

		// Use a barrier to synchronize the debit request and result.
		stream <PostTxResultSchema> FinalDebitResult = Barrier(DebitRequest; DebitResult) {
			output 
				FinalDebitResult: accountNumber = DebitRequest.accountNumber, currentBalance = DebitResult.newBalance;
		} // End of Barrier(DebitRequest; DebitResult)
		
		// Write the deposit results to a sink file.
		() as FileWriter1 = FileSink(FinalDepositResult) {
			param 
				file: "bank_tasks_deposit.result";
		} // End of FileSink(FinalDepositResult)

		// Write the debit results to a sink file.
		() as FileWriter2 = FileSink(FinalDebitResult) {
			param 
				file: "bank_tasks_debit.result";
		} // End of FileSink(FinalDebitResult)
} // End of composite barrier_at_work.

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/005_throttle_at_work_sample_throttle_at_work_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/007_split_at_work_sample_split_at_work_spl/"> > </a>
</div>

