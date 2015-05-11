from count_cfg_freq import *

def main(infile,outfile,counter):
	f_in = open(infile,'r')
	f_out = open(outfile,'w')
	for line in f_in:
		if not line:
			continue
		json.dump(cky(line,counter),f_out)
		f_out.write('\n')

#implements cky
def cky(sentence,counter):
	#initialize variables
	pi = {}
	bp = {}
	sentence = sentence.split()
	n = len(sentence)

	# run CKY main loop
	for l in range(1,n):
		for i in range(1,n-l+1):
			j = i + l
			for terminal in counter.binary_rules:
				maxim = 0
				best = None
				for s in range(i,j):
					for y1,y2 in counter.binary_rules[terminal]:
						q = counter.binary_probabilities[(terminal,y1,y2)]
						# check for base case for word 1
						if i == s:
							word = sentence[i-1]
							if word not in counter.wordbank:
								word = '__RARE__'
							counter.unary_probabilities.setdefault((y1,word),0)
							p1 = counter.unary_probabilities[(y1,word)]
						else:
							pi.setdefault((i,s,y1),0)
							p1 = pi[(i,s,y1)]
						# check for base case for word 2
						if s+1 == j:
							word = sentence[s]
							if word not in counter.wordbank:
								word = '__RARE__'
							counter.unary_probabilities.setdefault((y2,word),0)
							p2 = counter.unary_probabilities[(y2,word)]
						else:
							pi.setdefault((s+1,j,y2),0)
							p2 = pi[(s+1,j,y2)]
						p = p1 * p2 * q
						if p > maxim:
							maxim = p
							best = (terminal,y1,y2,s)
				pi[i,j,terminal] = maxim
				bp[i,j,terminal] = best
				
	# find the probability and backpointers
	pi.setdefault((1,n,unicode('S')),0)
	if pi[(1,n,unicode('S'))] > 0:
		tree = [unicode('S')]
		return make_tree(bp,sentence,unicode('S'),1,n)
	else:
		maxim = float('-inf')
		best = None
		for terminal in counter.binary_rules:
			if (1,n,terminal) in pi:
				p = pi[(1,n,terminal)]
				if p > maxim:
					maxim = p
					best = (1,n,terminal)
		return make_tree(bp,sentence,unicode(best[2]),1,n)

# makes the tree based off of backpointer
def make_tree(bp,sentence,current,start,end):
	# base case
	if start == end:
		return [str(current),str(sentence[start-1])]
	#create root
	root = [str(current)]
	t = bp[start,end,current]
	# call recursively on both children 
	left = make_tree(bp,sentence,t[1],start,t[3])
	right = make_tree(bp,sentence,t[2],t[3]+1,end)
	# append both children
	root.append(left)
	root.append(right)
	return root

# calculates the counts and initiates counter object
def calculate_counts(parse_file):
	counter = Counts() 
	for l in open(parse_file):
		t = json.loads(l)
		counter.count(t)
	return counter

def usage():
	sys.stderr.write("""
		Usage: python count_cfg_freq.py [tree_file] [parse_file]
	  Print the counts of a corpus of trees.\n""")

if __name__ == "__main__": 
	if len(sys.argv) != 3:
		usage()
		sys.exit(1)
	# initiate counter
	counter = calculate_counts(sys.argv[1])
	counter.counts()
	# calculate probabilities
	counter.calculate_probabilities()
	counter.create_wordbank()
	# run CKY algorithm
	main(sys.argv[2],'prediction_file',counter)

