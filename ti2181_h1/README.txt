This is a report for assignment 1.

HOW TO RUN BASH SCRIPT
To run both scripts: bash run_script.sh 
To test just question 4 functions: bash run_emission.sh
To test viterbi functions: bash run_viterbi.sh

Question 4 analysis. 
Part 1: Generating the emission counts
What I did:
For this problem, I decided to write everything in count_freq.py because I believed that generating emission counts should be done in the HMM object. For the first part of the problem, I created a function calc_emissions inside the HMM object that parsed through the emission counts dictionary and generated a new dictionary where the keys are a tuple of a given word and one of its tags and the value is the probability associated to it. I stored all these values in a dictionary called emission_probability for I had a feeling it would be very helpful for future problems.

Part 2: Mapping infrequent words
What I did:
Yet again, I believed that this should yet again be a function within the HMM object so I created a function remove_infrequent which took in the minimum amount of words needed (which was in our case 5), before we map the word to _RARE_. This was tricky at first because some words had multiple tags so it was not as easy as just looking up the WORDTAGS for the count for each words. I realized that knowing the total counts of the words will be useful for number 5 so I decided that it should be useful to also put this value into a dictionary so before I did this function, I created a dictionary in the function create_taglist that had the word as the key and the value be an array where the first index is the count of the word and the second index is an array of all the tags that this word can take. Then I in remove_infrequent, I iterated through the taglist dictionary and if the count of the word was less than the 5, I updated the emission_counts with a new word _RARE_ and updated the corresponding tags with it. I also deleted the original word from the dictionary which was something I initially forgot to do but created a lot of problems for me in the future. 

Part 3: Implement simple names entity tagger
What I did:
To implement this, I first had the create a function that found the highest emission probability associated to a given word. So I created a function called find_max_emission which took in the HMM object and word as input and returned the tag and probability associated to it. I first checked to see if that word was ever encountered. If it was not in our dictionary, I assumed it was an infrequent word and mapped it to _RARE_. Then I iterated through all the tags associated to that word and return the tag with the highest probability and the log of the probability. Then I created a function called eval_emissions that read the file called "ner_dev.dat" and for every line, I figured out the highest emission probabilty and tag associated to that word and outputed it to a file called "output_e.dat". When I ran it, it compiled almost instantly and the scores are shown below. The scores are not bad at all and are on average around 50% for all 3 scores.

Output of eval_tagger.py for emissions
	 	 precision 	recall 		F1-Score
Total:	 0.579871	0.468218	0.518097
PER:	 0.435451	0.231230	0.302061
ORG:	 0.475936	0.399103	0.434146
LOC:	 0.811370	0.684842	0.742756
MISC:	 0.491689	0.610206	0.544574


Question 5 analysis:

For these problems, I created a seperate file ti2181.py and imported everything from count_freq.py. 

Part 1: Create a function that takes in a trigram and return the log probability 
What I did:
I decided that the input would be a space delimited string of three words. I first split that word and parsed it into trigram, bigram and unigram tuples. I thought that calculating the trigram, bigram and unigram probabilities every single time this function is called will be pretty heavy so I decided to create a dictionary for every tuple. So in my count_freq.py file, I created three functions,(compute_trigram_probabilities, compute_bigram_probabilities and compute_unigram_probabilities) that created the three dictionaries trigram_probabilities, bigram_probabilities and unigram_probabilities which stored the probability of every tuple. Then I multiplied them to the lambda values that I set and returned the sum of all 3. 

Part 2: Implementing Viterbi's algorithm
What I did:
I pretty much followed the psuedocode. I created two dictionaries, table_probabilities and back_pointer, which I filled out for every given sentence. Things to note was that I needed to seperate the first two words from the rest of the algorithm because "*" was not a tag. I also initially tried to implement the modified version of the algorithm in question 3 by creating a function that returned all the available tags for a given word. But I found that this heavily impacted my results and realized that since this is such a basic implementation of viterbi, it was better to just iterate through all the tags for now. Otherwise, I followed the psuedocode. Once I backtracked through my dictionary and found the given tag, I iterated through them to find the probabilities associated to them and returned an array of tuples where the first index is the tag and the second was the probability associated to it. 

Part 3: Implement basic tagger
What I did:
Similarly to the emission tagger, I yet again read "ner_dev.dat" but this time, I split the text by a "/n/n" which seperated every sentence in the file. Then I split each sentence by "/n" which gave me an array of tags and ran it into my viterbi function which returned to me my array of tag, probability tuples. Then I just ouputed the log of the probabilities to a file called "output_v.dat". 
The results take about 3-5 minutes to compile and the output varies on the lambda values. For some reason, Org is the only tag that I perform very poorly on and dramatically brings down the total scores. But overall, it did much better than the tagging by emission counts. I observed that putting a lot of weight on my trigrams seemed to increase my output the most so that is how my lambda values are set up for now. 

results: 
		 precision 	recall 		F1-Score
Total:	 0.664836	0.591974	0.626293
PER:	 0.712475	0.581066	0.640096
ORG:	 0.618768	0.473094	0.536213
LOC:	 0.644168	0.650491	0.647314
MISC:	 0.680265	0.669924	0.675055

Question 6:
Part 1: Improve how to handle low-frequency words
What I did:
I pretty much created different categories that these words fell into. I first looked for words where the first letter was capitalized and the rest were lowercase. This was a common trend among names and organizations. I also had a category for any words that were not alphanumeric. Then I checked for numbers. If all else failed, I gave it the _RARE_ tag. As you can see, this did increase the efficiency of the code as shown below. Every tag but ORG did very well. All my totals were greater than .7 which is great. 

Results:
		 precision 	recall 		F1-Score
Total:	 0.724875	0.708987	0.716843
PER:	 0.804533	0.772579	0.788232
ORG:	 0.573681	0.625561	0.598498
LOC:	 0.775439	0.723010	0.748307
MISC:	 0.717416	0.675353	0.695749


