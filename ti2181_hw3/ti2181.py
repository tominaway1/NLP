import sys, math

# handle main computations
def main(e,g):
	# implement IBM model 1
	english = []
	german = []

	# update arrays
	for word in e.read().split('\n'):
		english.append(word)
	for word in g.read().split('\n'):
		german.append(word)

	# calculate tag probabilities
	print "Calculating tag probabilities using IBM model 1"
	d, en = calc_trans_parem1(english,german)
	
	# write output for top ten possibilities for every word in the devwords.txt file
	devword = open('devwords.txt','r')
	write_dev_output(test_dicts(devword,d,en),'dev_output.txt')
	print "Wrote output of devwords to a file called dev_output1.txt"
	
	# find alignments for first 20 sentence pairs
	alignment = find_alignment1(english[0:20],german[0:20],d)
	write_alignment_output(english[0:20],german[0:20],alignment,'alignment_model1.txt')
	print "Wrote predicted tags to a file called alignment_model1.txt"

	# test for IBM model 2
	print "Calculating tag probabilities using IBM model 2"
	d,q,en = calc_trans_parem2(english,german,d)
	
	# write output for top ten possibilities for every word in the devwords.txt file
	devword = open('devwords.txt','r')
	write_dev_output(test_dicts(devword,d,en),'dev_output1.txt')
	print "Wrote output of devwords to a file called dev_output1.txt"

	# find alignments for first 20 sentence pairs
	alignment = find_alignment2(english[0:20],german[0:20],d,q)
	write_alignment_output(english[0:20],german[0:20],alignment,'alignment_model2.txt')
	print "Wrote predicted tags to a file called alignment_model2.txt"
	
	print "Creating unscrambled.en"
	find_translations(d,q)
	return

# writes results to output file
def write_alignment_output(e,g,d,fname):
	f = open(fname,'w')
	for i in range(len(e)):
		eng = e[i]
		germ = g[i]
		tag = d[i]
		f.write(eng+'\n')
		f.write(germ+'\n')
		f.write('[{0}]\n'.format(', '.join([str(x) for x in tag])))
		f.write('\n')


# Finds the alignment given corresponding sentences and the tag probability dictionary
def find_alignment1(e,g,d):
	ans = []
	# iterate through all sentences 
	for i in range(len(e)):
		arr = [] 
		english_sent = e[i].split()
		german_sent = g[i].split()
		english_sent.insert(0,None)
		# for every foreign word
		for j in range(len(german_sent)):
			# find arg with maximum tag in english sentence
			german_word = german_sent[j]
			maxim = float('-inf')
			max_arg = None
			for k in range(len(english_sent)):
				eng_word = english_sent[k]
				d.setdefault((german_word,eng_word),0)
				prob = d[(german_word,eng_word)]
				if prob >= maxim:
					maxim = prob
					max_arg = k
			arr.append(max_arg)
		ans.append(arr)
	return ans

# Finds the alignment given corresponding sentences and the tag probability dictionary
def find_alignment2(e,g,d,q):
	ans = []
	# iterate through all sentences 
	for i in range(len(e)):
		arr = [] 
		english_sent = e[i].split()
		german_sent = g[i].split()
		english_sent.insert(0,None)
		# for every foreign word
		for j in range(len(german_sent)):
			# find arg with maximum tag in english sentence
			german_word = german_sent[j]
			maxim = float('-inf')
			max_arg = None
			for k in range(len(english_sent)):
				eng_word = english_sent[k]
				d.setdefault((german_word,eng_word),0)
				q.setdefault((k,j,len(english_sent),len(german_sent)),0)
				prob = d[(german_word,eng_word)] * q[(k,j,len(english_sent),len(german_sent))]
				if prob >= maxim:
					maxim = prob
					max_arg = k
			arr.append(max_arg)
		ans.append(arr)
	return ans

def find_translations(d,q):
	e = open('scrambled.en','r')
	g = open('original.de','r')
	output = open('unscrambled.en','w')

	# get sentences
	english = []
	german = []

	# update arrays
	for word in e.read().split('\n'):
		english.append(word)
	for word in g.read().split('\n'):
		german.append(word)
	e.close()
	g.close()

	# calculate alignment
	# alignment = (english,german,d,g)

	for i in range(len(german)):
		german_sent1 = german[i]
		maxim = float('-inf')
		max_sentence = ''
		for english_sent in english:
			# find alignment
			alignment = find_alignment2([english_sent],[german_sent1],d,q)[0]

			# calculate probability
			probability = 0
			german_sent = german_sent1.split()
			english_sent1 = english_sent.split()
			english_sent1.insert(0,None)
			l = len(english_sent1)
			m = len(german_sent)
			for i in range(m):
				ai = alignment[i]
				q.setdefault(((ai,i,l,m),0))
				d.setdefault((german_sent[i],english_sent1[ai]),0)
				p = q[(ai,i,l,m)] * d[(german_sent[i],english_sent1[ai])]
				probability += p
			# compare probability to max
			if probability == 0 :
				continue
			if math.log(probability) > maxim:
				maxim = math.log(probability)
				max_sentence = english_sent
		output.write(max_sentence+'\n')
	output.close()

def write_dev_output(d,fname):
	f = open(fname,'w')
	for word in d:
		f.write("These are the top words for \"{}\"\n".format(word))
		for f_word, stat in d[word]:
			f.write('"{0}" with probability {1}\n'.format(f_word,stat))
		f.write('\n')
	f.close()

def test_dicts(dev,d,e):
	ans = {}
	for word in dev.read().split():
		if word not in e:
			temp = e[None]
		else:
			temp = e[word]
		temp.sort(key=lambda x: x[1],reverse=True)
		if len(temp)>10:
			ans[word] = temp[0:10]
		else:
			ans[word] = temp
	return ans


# calculates translation parameters using IBM model 1
def calc_trans_parem1(english,german):
	#create dictionaries
	t_fe = {}
	c_ef = {}
	c_e = {}
	e_to_f = {}

	# find total german words
	total_german = find_total(german)
	for s in range(5):
		# print s
		# reset all counts
		for key in c_e:
			c_e[key] = 0
		for key in c_ef:
			c_ef[key] = 0
		
		# iterate through algorithm
		for k in range(len(english)):
			#get sentences
			e_sentence = english[k].split()
			e_sentence.insert(0,None)
			g_sentence = german[k].split()

			for i in range(len(g_sentence)):
				# calculate summation for sentence
				summation = 0
				for z in e_sentence[1:]:
					t_fe.setdefault((g_sentence[i],z),1.0/total_german)
					summation += t_fe[(g_sentence[i],z)]

				# iterate through every word in english sentence
				for j in range(len(e_sentence)):
					# calculate delta
					t_fe.setdefault((g_sentence[i],e_sentence[j]),1.0/total_german)
					delta = t_fe[(g_sentence[i],e_sentence[j])] / summation
					# set defaults
					c_ef.setdefault((e_sentence[j],g_sentence[i]),0)
					c_e.setdefault(e_sentence[j],0)
					# update c_ef
					c_ef[(e_sentence[j],g_sentence[i])] = c_ef[(e_sentence[j],g_sentence[i])] + delta				
					# update c_e
					c_e[e_sentence[j]] = c_e[e_sentence[j]] + delta
		# update t_fe
		for eng_word, germ_word in c_ef:
			if c_e[eng_word] == 0:
				t_fe[(germ_word,eng_word)] = 0
			else:
				t_fe[(germ_word,eng_word)] = c_ef[(eng_word,germ_word)] / c_e[eng_word]
	#update e_to_f dictionary
	for eng_word, germ_word in c_ef:
		e_to_f.setdefault(eng_word,[])
		e_to_f[eng_word].append((germ_word,t_fe[(germ_word,eng_word)]))
	return t_fe ,e_to_f

# finds every word in german dictionary
def find_total(german):
	total = 0
	for line in german:
		for word in line.split():
			total += 1
	return total


# extends IBM model 1 to IBM model 2
def calc_trans_parem2(english,german,t_fe):
	#create dictionaries
	c_ef = {}
	c_e = {}
	q_j_i_l_m = {}
	c_i_l_m = {}
	c_j_i_l_m = {}
	e_to_f = {}

	# find total german words
	total_german = find_total(german)
	for s in range(5):
		# print s
		# reset all counts
		for key in c_e:
			c_e[key] = 0
		for key in c_ef:
			c_ef[key] = 0
		
		# iterate through algorithm
		for k in range(len(english)):
			#get sentences
			e_sentence = english[k].split()
			e_sentence.insert(0,None)
			g_sentence = german[k].split()
			l = len(e_sentence)
			m = len(g_sentence)
			for i in range(m):
				# calculate summation for sentence
				summation = 0
				for j in range(l):
					t_fe.setdefault((g_sentence[i],e_sentence[j]),1.0/total_german)
					q_j_i_l_m.setdefault((j,i,l,m),1.0/(l+1))
					summation += t_fe[(g_sentence[i],e_sentence[j])] * q_j_i_l_m[(j,i,l,m)]

				# iterate through every word in english sentence
				for j in range(l):
					# set defaults
					c_ef.setdefault((e_sentence[j],g_sentence[i]),0)
					c_e.setdefault(e_sentence[j],0)
					c_i_l_m.setdefault((i,l,m),0)
					c_j_i_l_m.setdefault((j,i,l,m),0)
					# calculate delta
					delta = q_j_i_l_m[(j,i,l,m)] * t_fe[(g_sentence[i],e_sentence[j])] / summation
					# update c_ef
					c_ef[(e_sentence[j],g_sentence[i])] = c_ef[(e_sentence[j],g_sentence[i])] + delta				
					# update c_e
					c_e[e_sentence[j]] = c_e[e_sentence[j]] + delta
					# update c_j_i_l_m
					c_j_i_l_m[(j,i,l,m)] = c_i_l_m[(i,l,m)] + delta
					# update c_i_l_m
					c_i_l_m[(i,l,m)] = c_i_l_m[(i,l,m)] + delta
		# update t_fe
		for eng_word, germ_word in c_ef:
			if c_e[eng_word] == 0:
				t_fe[(germ_word,eng_word)] = 0
			else:
				t_fe[(germ_word,eng_word)] = c_ef[(eng_word,germ_word)] / c_e[eng_word]
		# update q_j_i_l_m
		for j,i,l,m in c_j_i_l_m:
			q_j_i_l_m[(j,i,l,m)] = c_j_i_l_m[(j,i,l,m)] / c_i_l_m[(i,l,m)]
	for eng_word, germ_word in c_ef:
		e_to_f.setdefault(eng_word,[])
		e_to_f[eng_word].append((germ_word,t_fe[(germ_word,eng_word)]))
	return t_fe, q_j_i_l_m, e_to_f

def usage():
    sys.stderr.write("Usage: python ibm_model_1.py [english_file] [german_file]\n")


if __name__ == '__main__':
	if len(sys.argv) != 3:
		usage()
		sys.exit(1)
	try:
		german_corp = open(sys.argv[2],'r')
	except:
		print "German corpus file invalid and cannot be found"
		sys.exit(1)
		
	try:
		english_corp = open(sys.argv[1],'r')
	except:
		print "English corpus file invalid and cannot be found"
		sys.exit(1)

	main(english_corp, german_corp)
	german_corp.close()
	english_corp.close()