---
layout: samples
title: 090_consistent_region_spl_01
---

### 090_consistent_region_spl_01

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/089_integrating_streams_apps_with_web_apps_com_acme_test_WebCalculator_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/091_consistent_region_spl_02_com_acme_test_ConsistentRegion2_spl/"> > </a>
</div>

~~~~~~
/* 
==========================================================================
Copyright (C) 2014-2015, International Business Machines Corporation
All Rights Reserved                                                 

This is one of many examples included in the "SPL Examples for
Beginners" collection to show the use of the consistent region feature
built into Streams 4.x and higher versions. This particular example was
written by my colleague Gabriela Jacques da Silva and full credit goes to her. 

This particular example shows how every single SPL based operator in an application
graph will take part in the consistent region. This example simulates the operator
failure by aborting that operator automatically when the application is
in the middle of executing the logic. By doing that, the core fault tolerance
feature of the consistent region will get triggered to recover from a
failure that occurred in an application graph. It will prove that the
tuples will not be missed and the local operator state will not be
compromised during the course of the unexpected operator failure and the
subsequent recovery/restoration. 


Initial Streams setup needed before running this example
---------------------------------------------------------
To use the consistent region feature, one must run the application in the
Distributed mode. Before that, certain configuration needs to be completed;
i.e. Streams checkpoint back-end related properties must be set. One can use
the file system or an external Redis infrastructure as a checkpoint back-end.
In this example, we will use the filesystem by setting the following
Streams instance properties:

streamtool setproperty instance.checkpointRepository=fileSystem -d <YOUR_DOMAIN_ID> -i <YOUR_INSTANCE_ID>
streamtool setproperty instance.checkpointRepositoryConfiguration={\"Dir\":\"/your/checkpoint/directory/here/\"}

Compile and Run
---------------
1) You can either compile this application inside the Streams Studio or from a Linux
   terminal window via the sc (Streams compiler) command.
 
2) While launching from Streams Studio or submitting via the streamtool command,
   you must provide the required application-specific submission time parameter called crash with
   a value of 0 (for no automatic crash of an operator) or 1 (to automatically crash an operator).

It is better to run it first with crash=0 (normal behavior) and then rename the result file created 
inside the data directory. After that, run it again with crash=1 (automatic fault injection) to
force a crash and recovery cycle. Now, compare the new result file in the data directory with
the result file from the previous run. If they are the same, then the consistent region feature
worked as expected.
==========================================================================
*/
namespace com.acme.test;

type 
  WordCountTuple = tuple<rstring word, uint32 count>;

// Sorts an input map according to its keys into a list
void sortMap(map<rstring, uint32> inMap, mutable list<WordCountTuple> orderedList) {
  mutable list<rstring> mapKeys = keys(inMap);
  sortM(mapKeys);
  for (rstring key in mapKeys) {
    appendM(orderedList, {word = key, count = inMap[key]});
  }
}

// This application counts words from the input file "loremIpsum.txt". Word count
// statistics is reported at every 25 tuples. The application can be configured
// at submission to inject faults, forcing tuples to be dropped. As the application
// uses the @consistent annotation, tuples are replayed after failure detection. 
composite ConsistentRegion1 {
  graph
    // JobControlPlane operator is mandatory in applications with consistent regions
    // Simply include it anywhere in your application graph.
    () as JCP = JobControlPlane() {}

    // FileSource is the start operator of a periodic consistent region. Consistent
    // state is reached at every second.
    // By using the @consistent annotation at the top of the FileSource, we are going to make this
    // entire application graph (i.e. all the operators in it) as fault tolerant or
    // as part of a consistent region.
    @consistent(trigger=periodic, period=1.0)
    stream<rstring line> Lines = FileSource() {
      param
        file: "loremIpsum.txt";
        format: line;
      config
        placement: partitionColocation("PE1");
    }

    // Given the input data file is a short file, the Throttle operator
    // gives the application the chance to establish consistent states
    // before fully processing the file. Throttle is fused with FileSource so that
    // its input stream is not filled up with all the lines of the file.
    stream<Lines> ThrottledLines = Throttle(Lines) {
      param
        rate: 20.0;
      config
        placement: partitionColocation("PE1");
    } 

    // Tokenize a line and eliminate punctuation from words
    stream<list<rstring> words> Words = Custom(ThrottledLines) {
      logic
        onTuple ThrottledLines: {
          list<rstring> originalWords = tokenize(ThrottledLines.line, " ", false);
          mutable list<rstring> trimmedWords = [];
          for (rstring word in originalWords) {
            rstring trimmedWord = rtrim(lower(word), ",.:;");
            appendM(trimmedWords, trimmedWord);
          }
          submit({words = trimmedWords}, Words);
        }
    }
    
    // Optionally crash operator when processing the 200th input tuple
    stream<Words> WordsAfterACrash = CrashAtTuple(Words) {
      param
        tupleNumber: 200u;
    }

    // Optionally crash operator when processing the 370th input tuple
    stream<Words> WordsAfterAnotherCrash = CrashAtTuple(WordsAfterACrash) {
      param
        tupleNumber: 370u;
      config
        placement: partitionColocation("PE2");
    }

    // Operator counts words and submits an ordered list of the current count values
    // at the specified submission interval. State of the operator is automatically 
    // checkpointed when establishing a consistent state.
    // Operator is fused with the the 'WordsAfterAnotherCrash' operator to illustrate
    // a stateful operator failure.  
    stream<list<WordCountTuple> wordCount> WordCount = Custom(WordsAfterAnotherCrash as I) {
      logic
        state: { mutable map<rstring, uint32> wordCountMap; 
                 mutable int32 tupCounter = 0; 
                 int32 submissionInterval = 25; }
        onTuple I: {
          for (rstring word in words) {
            if (word in wordCountMap) {
              wordCountMap[word] += 1u;
            } else {
              wordCountMap[word] = 1u;
            }
          }
          tupCounter++; 
          if (tupCounter % submissionInterval == 0) {
            mutable list<WordCountTuple> orderedList = [];
            // Sorts map to have a deterministic output
            sortMap(wordCountMap, orderedList);
            submit({wordCount = orderedList}, WordCount);
          } 
        }
      config
        placement: partitionColocation("PE2");
    }

    // FileSink operator automatically truncates its output when a failure
    // occurs in a consistent region. After a run with failures, the result
    // file has the same content as if the run had had no failures. 
    () as MySink1 = FileSink(WordCount) {
      param
        file: "result.txt";
    }
}

// Forwards input stream to the output stream. The operator
// optionally crashes itself when processing the specified tupleNumber.
// The crash occurs if the parameter "crash" is specified with a value
// greater than 0.
composite CrashAtTuple(output O; input I) {
  param
    expression<uint32> $tupleNumber;

  graph
    stream<I> O = Custom(I) {
      logic 
        state: { uint32 mustCrash = (uint32) strtoull(getSubmissionTimeValue("crash", "0"), 10);
                 mutable uint32 counter = 0u; }
        onTuple I : {
          counter++;
          // Force a crash only once when the tuple count reaches the user specified value.
          // In addition, do the check that this operator was not relaunched already to ensure that
          // we don't force a crash repeatedly.
          if (counter == $tupleNumber && mustCrash > 0u &&
              getRelaunchCount() == 0u) {
            // Force a crash now.
            abort();
          }
          
          // If no forced crash is needed, simply forward the incoming tuple.
          submit(I, O);
        }

    }    
}
~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/089_integrating_streams_apps_with_web_apps_com_acme_test_WebCalculator_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/091_consistent_region_spl_02_com_acme_test_ConsistentRegion2_spl/"> > </a>
</div>

