#! /usr/bin/python

__author__="Daniel Bauer <bauer@cs.columbia.edu>"
__date__ ="$Sep 12, 2011"

import sys
from collections import defaultdict
import math, re

"""
Count n-gram frequencies in a CoNLL NER data file and write counts to
stdout. 
"""

def simple_conll_corpus_iterator(corpus_file):
    """
    Get an iterator object over the corpus file. The elements of the
    iterator contain (word, ne_tag) tuples. Blank lines, indicating
    sentence boundaries return (None, None).
    """
    l = corpus_file.readline()
    while l:
        line = l.strip()
        if line: # Nonempty line
            # Extract information from line.
            # Each line has the format
            # word pos_tag phrase_tag ne_tag
            fields = line.split(" ")
            ne_tag = fields[-1]
            #phrase_tag = fields[-2] #Unused
            #pos_tag = fields[-3] #Unused
            word = " ".join(fields[:-1])
            yield word, ne_tag
        else: # Empty line
            yield (None, None)                        
        l = corpus_file.readline()

def sentence_iterator(corpus_iterator):
    """
    Return an iterator object that yields one sentence at a time.
    Sentences are represented as lists of (word, ne_tag) tuples.
    """
    current_sentence = [] #Buffer for the current sentence
    for l in corpus_iterator:        
            if l==(None, None):
                if current_sentence:  #Reached the end of a sentence
                    yield current_sentence
                    current_sentence = [] #Reset buffer
                else: # Got empty input stream
                    sys.stderr.write("WARNING: Got empty input file/stream.\n")
                    raise StopIteration
            else:
                current_sentence.append(l) #Add token to the buffer

    if current_sentence: # If the last line was blank, we're done
        yield current_sentence  #Otherwise when there is no more token
                                # in the stream return the last sentence.

def get_ngrams(sent_iterator, n):
    """
    Get a generator that returns n-grams over the entire corpus,
    respecting sentence boundaries and inserting boundary tokens.
    Sent_iterator is a generator object whose elements are lists
    of tokens.
    """
    for sent in sent_iterator:
         #Add boundary symbols to the sentence
         w_boundary = (n-1) * [(None, "*")]
         w_boundary.extend(sent)
         w_boundary.append((None, "STOP"))
         #Then extract n-grams
         ngrams = (tuple(w_boundary[i:i+n]) for i in xrange(len(w_boundary)-n+1))
         for n_gram in ngrams: #Return one n-gram at a time
            yield n_gram        


class Hmm(object):
    """
    Stores counts for n-grams and emissions. 
    """
    def __init__(self, n=3):
        assert n>=2, "Expecting n>=2."
        self.n = n
        self.emission_counts = defaultdict(int)
        self.ngram_counts = [defaultdict(int) for i in xrange(self.n)]
        self.all_states = set()
        
        #dictionaries I made
        self.emission_probability = defaultdict(int)
        self.trigram_probabilities = defaultdict(int)
        self.bigram_probabilities = defaultdict(int)
        self.unigram_probabilities = defaultdict(int)
        self.tag_list = defaultdict(int)
        self.categories = ['_CAPITALS_','_NUMBERS_','_SPECIALCHARACTERS_','_RARE_']

    def train(self, corpus_file):
        """
        Count n-gram frequencies and emission probabilities from a corpus file.
        """
        ngram_iterator = \
            get_ngrams(sentence_iterator(simple_conll_corpus_iterator(corpus_file)), self.n)

        for ngram in ngram_iterator:
            #Sanity check: n-gram we get from the corpus stream needs to have the right length
            assert len(ngram) == self.n, "ngram in stream is %i, expected %i" % (len(ngram, self.n))

            tagsonly = tuple([ne_tag for word, ne_tag in ngram]) #retrieve only the tags            
            for i in xrange(2, self.n+1): #Count NE-tag 2-grams..n-grams
                self.ngram_counts[i-1][tagsonly[-i:]] += 1
            
            if ngram[-1][0] is not None: # If this is not the last word in a sentence
                self.ngram_counts[0][tagsonly[-1:]] += 1 # count 1-gram
                self.emission_counts[ngram[-1]] += 1 # and emission frequencies

            # Need to count a single n-1-gram of sentence start symbols per sentence
            if ngram[-2][0] is None: # this is the first n-gram in a sentence
                self.ngram_counts[self.n - 2][tuple((self.n - 1) * ["*"])] += 1


    def write_counts(self, output, printngrams=[1,2,3]):
        """
        Writes counts to the output file object.
        Format:

        """
        # First write counts for emissions
        for word, ne_tag in self.emission_counts:            
            output.write("%i WORDTAG %s %s\n" % (self.emission_counts[(word, ne_tag)], ne_tag, word))


        # Then write counts for all ngrams
        for n in printngrams:            
            for ngram in self.ngram_counts[n-1]:
                ngramstr = " ".join(ngram)
                output.write("%i %i-GRAM %s\n" %(self.ngram_counts[n-1][ngram], n, ngramstr))

    def read_counts(self, corpusfile):
        self.n = 3
        self.emission_counts = defaultdict(int)
        self.ngram_counts = [defaultdict(int) for i in xrange(self.n)]
        self.all_states = set()

        for line in corpusfile:
            parts = line.strip().split(" ")
            count = float(parts[0])
            if parts[1] == "WORDTAG":
                ne_tag = parts[2]
                word = parts[3]
                self.emission_counts[(word, ne_tag)] = count
                self.all_states.add(ne_tag)
            elif parts[1].endswith("GRAM"):
                n = int(parts[1].replace("-GRAM",""))
                ngram = tuple(parts[2:])
                self.ngram_counts[n-1][ngram] = count
    
    #calculate emmision probability for every word
    def calc_emissions(self):
        #get unigram dictionary
        unigramDict = self.ngram_counts[0]

        #iterate through all the words in the dictionary
        for word, ne_tag in self.emission_counts:
            #get total times tag appears
            unigramCount = unigramDict[(ne_tag,)]
            #calculate probability
            if unigramCount == 0:
                p = .000000000000000001
            else:
                p = self.emission_counts[(word, ne_tag)] / float(unigramCount)

            #check if we already have a tag associated to word
            if word in self.emission_probability:
                self.emission_probability[word][ne_tag] = p
            else:
                self.emission_probability[word] = {}
                self.emission_probability[word][ne_tag] = p
    
    #create a list of tags for every word
    def create_taglist(self):
        #create new dictionary to keep track of number
        d = {}
        for word, ne_tag in self.emission_counts:
            if word in d:
                d[word][0] = d[word][0] + self.emission_counts[(word, ne_tag)]
                d[word][1].append(ne_tag)
            else:
                d[word] = [self.emission_counts[(word, ne_tag)],[ne_tag]]
        self.tag_list = d
    
    # a function that figures out what tag category a word falls into 
    def partition_to_category(self,tag):
        #check for special characters
        if re.match('^[\w-]+$', tag) is None:
            tagCategory = self.categories[2]
        #check for any capitals
        elif tag[0].isupper() and all(x.islower() for x in tag[1:]):
            tagCategory = self.categories[0]
        #check if it contains digits
        elif any(x.isdigit() for x in tag):
            tagCategory = self.categories[1]
        else:
            tagCategory = self.categories[-1]
        return tagCategory


    #replace infrequent words with _RARE_
    def remove_infrequent(self, minimum):
        if len(self.tag_list) == 0:
            self.create_taglist()
        d = self.tag_list
        #if the number of word is less than minimum, replace in dictionary
        arr = []
        #create categories in order of precedence
        for c in self.categories:
            d[c] = [0,[]]
        for word in d:
            if word in self.categories:
                continue
            if d[word][0] < minimum:
                for tag in d[word][1]:
                    # figure out what tag category the word falls into 
                    tagCategory = self.partition_to_category(word)
                    if tagCategory in d:
                        d[tagCategory][0] = d[tagCategory][0] + 1
                    else:
                        d[tagCategory] = 1
                    if tag not in d[tagCategory][1]:
                        d[tagCategory][1].append(tag)
                    if (tagCategory,tag) in self.emission_counts:
                        self.emission_counts[(tagCategory,tag)] = self.emission_counts[(tagCategory,tag)] + self.emission_counts[(word,tag)]
                    else:
                        self.emission_counts[(tagCategory,tag)] = self.emission_counts[(word,tag)]
                    del self.emission_counts[(word,tag)]

                arr.append(word)
        #update tag list
        for word in arr:
            del d[word]
        self.tag_list = d

    #compute trigram probabilities
    def compute_trigram_probabilities(self):
        for trigram in self.ngram_counts[2]:
            # parse the tuple to yi, yi-1, yi-2
            yi = trigram[2]
            yi_1 = trigram[1]
            yi_2 = trigram[0]

            #find counts for trigrams
            trigram_count = self.ngram_counts[2][trigram]
            bigram_count = self.ngram_counts[1][(yi_1,yi)]

            #calculate the probability for yi given yi-1 and yi-2
            self.trigram_probabilities[trigram] = trigram_count/float(bigram_count + .0000000000001)
    
    #compute bigram probabilities
    def compute_bigram_probabilities(self):
        for bigram in self.ngram_counts[1]:
            # parse the tuple to yi, yi-1
            yi_1 = bigram[1]

            #find counts for bigrams
            bigram_count = self.ngram_counts[1][bigram]

            #calculate the probability for yi given yi-1 
            if self.ngram_counts[0][(yi_1,)] == 0:
                #will only happen for when yi_1 is * meaning at the beginning of sentence
                return 1
            self.bigram_probabilities[bigram] = float(bigram_count)/(self.ngram_counts[0][(yi_1,)] + .0000000000001)

    #compute unigram probabilities
    def compute_unigram_probabilities(self):
        total = 0
        d = {}
        for unigram in self.ngram_counts[0]:
            yi = unigram[0]

            #find counts for unigrams
            unigram_count = self.ngram_counts[0][(yi,)]
            total += unigram_count
            d[unigram] = unigram_count
        for unigram in d:
            self.unigram_probabilities[unigram] = d[unigram] / float(total + .0000000000001)

#This function will read in a file and output the results of emission counts
def eval_emission(HMM):
    #open dev file
    f_r = open("ner_dev.dat",'r')
    f = f_r.read().split('\n\n')
    #prepare file to write
    f_w = open('output_e.dat','w')

    #parse each line
    for line in f:
        str_list = line.split('\n')
        str_list = filter(None, str_list)

        for word in str_list:
            tag, tag_prob = find_max_emission(HMM, word)
            f_w.write(" ".join([word,tag,str(tag_prob)+'\n']))
        f_w.write('\n')
        
    #close the files
    f_w.close()
    f_r.close()

def find_max_emission(HMM, word):
    if word in HMM.emission_probability:
        d = HMM.emission_probability[word]
    else:
        d = HMM.emission_probability['_RARE_']
    maxim = float('-inf')
    tag = None
    for key in d:
        if d[key] > maxim:
            maxim = d[key]
            tag = key
    return tag, math.log(maxim)



def usage():
    print """
    python count_freqs.py [input_file] > [output_file]
        Read in a named entity tagged training input file and produce counts.
    """

if __name__ == "__main__":

    if len(sys.argv)!=2: # Expect exactly one argument: the training data file
        usage()
        sys.exit(2)

    try:
        input = file(sys.argv[1],"r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile %s.\n" % arg)
        sys.exit(1)
    
    # Initialize a trigram counter
    counter = Hmm(3)
    # Collect counts
    counter.train(input)
    # Clean the counts
    counter.create_taglist()
    counter.remove_infrequent(5)
    # Update all tables
    counter.calc_emissions()
    counter.compute_trigram_probabilities()
    counter.compute_bigram_probabilities()
    counter.compute_unigram_probabilities()
    #evaluate emissions
    eval_emission(counter)


