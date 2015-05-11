from count_freqs import *
import sys

#This function will read in a file and output the results of viterbi
def eval_viterbi(HMM):
	#open dev file
	f_r = open("ner_dev.dat",'r')
	f = f_r.read().split('\n\n')
	#prepare file to write
	f_w = open('output_v.dat','w')

	#parse each line
	for line in f:
		#separate words by newline and remove empty strings
		str_list = line.split('\n')
		str_list = filter(None, str_list)
		
		#run viterbi. Tags is a array of tuples in form of (tag,probability)
		tags = viterbi_algorithm(HMM,str_list)

		#check to see if the line was empty
		if not tags:
			continue
		#write output to file in proper format
		for i in range(len(str_list)):
			f_w.write(" ".join([str_list[i],tags[i][0],str(math.log(tags[i][1]))+'\n']))
		f_w.write('\n')

	#close the files
	f_w.close()
	f_r.close()

#This function will take in a HMM and a space separated trigram 
#and return the probability of that trigram
def calculate_probability(HMM,line):
	#set lambda values
	lambda1 = .70
	lambda2 = .29
	lambda3 = .01

	#split the line. If length is not 3, it is not a trigram so return 0
	line = line.split()
	if len(line) != 3:
		return .0000000001

	#parse to trigram, bigram and unigram tuples
	trigram = (line[0],line[1],line[2])
	bigram = (line[1],line[2])
	unigram = (line[2],)

	#find probability for each. Set to 0 if not found in training
	if trigram in HMM.trigram_probabilities:
		trigramProbability = HMM.trigram_probabilities[trigram]
	else:
		trigramProbability = 0
	if bigram in HMM.bigram_probabilities:
		bigramProbability = HMM.bigram_probabilities[bigram]
	else:
		bigramProbability = 0
	if unigram in HMM.unigram_probabilities:
		unigramProbability = HMM.unigram_probabilities[unigram]
	else:
		unigramProbability = 0
	#calculate answer and make sure if zero, return very small decimal
	answer = lambda1 * trigramProbability + lambda2 * bigramProbability + lambda3 * unigramProbability
	if answer == 0:
		return .0000000000000000000001
	else:
		return answer

#Will return all possible tags
def find_possible_tags(HMM,word):
	tag = []
	for t in HMM.ngram_counts[0].keys():
		tag.append(t[0])
	return tag

def viterbi_algorithm(HMM,arr):
	#create dictionaries for probabilities and back pointers
	table_probability = {}
	back_pointer = {}

	#create empty array for answers
	finalTagArr = [None] * len(arr)

	#check size of array and return if empty
	sizeOfArr = len(arr)
	if sizeOfArr == 0:
		return None

	#Check to see if only one var
	if sizeOfArr == 1:
		maximum = float('-inf')
		maxTuple = None
		#find the tag with highest probability
		for tag_v in find_possible_tags(HMM,arr[-1]):
			line = " ".join(["*",tag_v,'STOP'])
			trigram_prob = calculate_probability(HMM,line)
			temp = trigram_prob
			if temp > maximum:
				maximum = temp
				maxTuple = tag_v
		# update the final tag array with tuple of tag and probability and return 
		finalTagArr[0] = (maxTuple,maximum)
		return finalTagArr

	#Main loop for viterbi
	for k in range(sizeOfArr):
		#choose v
		word = arr[k]
		v = find_possible_tags(HMM,word)
		#check to see if k is *
		if k >= 1:
			u = find_possible_tags(HMM,arr[k-1])
		else:
			u = ["*"]
		#loop through all tags of v
		for tag_v in v:
			#loop through all tags of u
			for tag_u in u:
				#create max value to keep track of largest prob and associated tag for backpointer
				max_w = None
				maximum = float('-inf')
				#check if u or w is *
				if k <= 1:
					#set pi(k-1,w,u)
					if k==0:
						prev_tag = 1
					else:
						prev_tag = table_probability[(0,'*',tag_u)]
					#find q(v|w,u)
					line = " ".join(["*",tag_u,tag_v])
					trigram_prob = calculate_probability(HMM,line)
					#find emission probability
					if arr[k] not in HMM.emission_probability:
						if tag_v in HMM.emission_probability[HMM.partition_to_category(arr[k])]:
							emmision = HMM.emission_probability[HMM.partition_to_category(arr[k])][tag_v]
						else:
							emission = 0
					else:
						if tag_v in HMM.emission_probability[arr[k]]:
							emmision = HMM.emission_probability[arr[k]][tag_v]
						else:
							emmision = 0
					#calculate probability and compare it to the maximum value
					temp = prev_tag * trigram_prob * emmision
					if temp > maximum:
						maximum = temp
						max_w = "*"
				else:
					#loop where u, v, w all have tags
					for tag_w in find_possible_tags(HMM,arr[k-2]):
						#find pi(k-1,w,u)
						prev_tag = table_probability[(k-1,tag_w,tag_u)]
						#find q(v|w,u)
						line = " ".join([tag_w,tag_u,tag_v])
						trigram_prob = calculate_probability(HMM,line)
						#find emmission probability
						if arr[k] not in HMM.emission_probability:
							if tag_v in HMM.emission_probability[HMM.partition_to_category(arr[k])]:
								emmision = HMM.emission_probability[HMM.partition_to_category(arr[k])][tag_v]
							else:
								emmision = 0
						else:
							if tag_v in HMM.emission_probability[arr[k]]:
								emmision = HMM.emission_probability[arr[k]][tag_v]
							else:
								emmision = 0
						#calculate probability and compare it to the maximum value
						temp =  prev_tag * trigram_prob * emmision
						if temp > maximum:
							if temp == 0:
								temp = float('-inf')
							maximum = temp
							max_w = tag_w
				table_probability[(k,tag_u,tag_v)] = maximum	
				back_pointer[(k,tag_u,tag_v)] = max_w
	
	#Set yn-1 and yn 
	maximum = float('-inf')
	maxTuple = None
	for tag_v in find_possible_tags(HMM,arr[-1]):
		for tag_u in find_possible_tags(HMM,arr[-2]):
			#find tag with highest probability
			prev_tag = table_probability[(sizeOfArr-1,tag_u,tag_v)]
			line = " ".join([tag_u,tag_v,'STOP'])
			trigram_prob = calculate_probability(HMM,line)
			temp = prev_tag * trigram_prob
			if temp > maximum:
				maximum = temp
				maxTuple = (tag_u,tag_v)
	#update the final tag array with tuple of tag for yn-1 and yn 
	finalTagArr[sizeOfArr-1] = maxTuple[1]
	finalTagArr[sizeOfArr-2] = maxTuple[0]
	
	#update tags by iterating backwards
	for i in range(3,sizeOfArr+1):
		finalTagArr[sizeOfArr-i] = back_pointer[(sizeOfArr-i+2,
			finalTagArr[sizeOfArr-i+1],finalTagArr[sizeOfArr-i+2])]
	
	#pair every tag with a probability
	for i in range(sizeOfArr):
		if i == 0:
			tag = finalTagArr[0]
			finalTagArr[0] = (finalTagArr[0],table_probability[(0,'*',tag)])
		else:
			finalTagArr[i] = (finalTagArr[i],table_probability[(i,finalTagArr[i-1][0],finalTagArr[i])])
	return finalTagArr
				

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
    #Evaluate Viterbi
    eval_viterbi(counter)
    
