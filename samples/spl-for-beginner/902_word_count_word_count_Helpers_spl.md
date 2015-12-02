---
layout: samples
title: 902_word_count
---

### 902_word_count

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/901_cat_example_NumberedCat_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/902_word_count_word_count_WordCount_spl/"> > </a>
</div>

~~~~~~
namespace word.count;

type LineStat = tuple<int32 lines, int32 words>;

int32 countWords(rstring line) {
	return size(tokenize(line, " \t", false));
	
} // End of function countWords

void addStat(mutable LineStat x, LineStat y) {
	x.lines += y.lines;
	x.words += y.words;
} // End of function addStat

~~~~~~

<div class="sampleNav"><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/901_cat_example_NumberedCat_spl/"> < </a><a class="button" href="/streamsx.documentation/samples/spl-for-beginner/902_word_count_word_count_WordCount_spl/"> > </a>
</div>

