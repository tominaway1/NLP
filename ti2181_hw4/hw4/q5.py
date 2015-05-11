import sys
from subprocess import Popen, PIPE

class Procserver:
    '''
    Launch a python process that reads from stdin and writes to stdout as a
    service. Taken from Piazza. Written by Mohammad Sadegh Rasooli
    '''
    def __init__(self, proc_args):
        '''
        Initializes the process using its arguments.
        '''
        self.proc = Popen(proc_args, stdout=PIPE, stdin=PIPE)

    def __del__(self):
        '''
        Terminates the process.
        '''
        self.proc.terminate()

    def communicate(self, string):
        '''
        Writes string to the process's stdin and blocks till the process writes
        to its stdout. Returns the contents from the process's stdout.
        '''
        self.proc.stdin.write(string.strip()+'\n\n')
        out = ''
        while True:
            line = self.proc.stdout.readline()
            if not line.strip(): break
            out += line
        return out.strip()


def main(training,output):
	# train a new model
	arr = trainNew(training)

	# write to output
	f = open(output,'w')
	for line in arr:
		f.write(line)
	

def trainNew(training):
	# initialize dictionaries
	model = {}
	g = {}
	t = {}

	# 5 iterations
	for i in range(5):
		print i
		
		# initialize servers
		gold_serv = Procserver(['python', 'tagger_history_generator.py', 'GOLD'])
		enum_serv = Procserver(['python', 'tagger_history_generator.py', 'ENUM'])
		history_serv = Procserver(['python', 'tagger_decoder.py', 'HISTORY'])

		# open output file
		f = open(training,'r')
		
		# initialize counter
		v = 0

		# iterate through all sentences
		for sentence in f.read().split('\n\n'):
			# initializing gold step 
			if i == 0:
				gold = gold_serv.communicate(sentence)
				t[v] = gold
				g[v] = calculate_weight(gold.split('\n'), sentence.split('\n'), {}, True)
			
			# get history 
			h = enum_serv.communicate(sentence)
			h = h.split('\n')

			# calculate weight
			weight = calculate_weight(h,sentence.split('\n'),model,False)
			
			# get tags
			tags = history_serv.communicate(weight)
			tags = tags.split('\n')
			
			# check to see if different from gold standard
			if tags != t[v]:
				features = calculate_weight(tags,sentence.split('\n'),{},True)
				for feature in g[v]:
					model.setdefault(feature,0)
					model[feature] += g[v][feature]

				for feature in features:
					model.setdefault(feature,0)
					model[feature] -= features[feature]
			v += 1
		# reinitialize servers
		del gold_serv
		del enum_serv
		del history_serv
	
	# return output
	arr = []
	for key in model:
		arr.append("{0} {1}\n".format(key,str(model[key])))
	return arr


def calculate_weight(h,s,m,boolean):
	answer = ''
	# iterate through history
	for line1 in h:
		# preprocessing
		line = line1.split()
		if len(line) < 1:
			continue
		if line[2] == 'STOP':
			continue

		# get index
		index = int(line[0]) - 1
		
		# get word
		temp = s[index]
		temp = temp.replace('\t',' ') 
		temp = temp.strip()
		word = s[index].split()[0]
		
		# get tag
		tag = line[2]

		# initialize weight
		weight = 0

		# generate all features
		bigram = "BIGRAM:{0}:{1}".format(line[1],tag)
		t = "TAG:{0}:{1}".format(word,tag)
		suffix =['SUFFIX:{0}:3:{1}'.format(word[-3:],tag),'SUFFIX:{0}:2:{1}'.format(word[-2:],tag),'SUFFIX:{0}:1:{1}'.format(word[-1:],tag)]
		features = [bigram,t] + suffix
		
		# calculate weight
		for item in features:
			# check to see if we want to calculate the weight
			if not boolean:
				if item in m:
					weight += m[item]
			else:
			# want to update the model
				if item in m:
					m[item] += 1
				else:
					m[item] = 1
		answer += "{0} {1}\n".format(line1, str(weight))

	# return proper output
	if not boolean:
		return answer
	return m


def usage():
	print "Proper usage: python q5.py [training] [output]"

if __name__ == '__main__':
	if len(sys.argv) != 3:
		usage()
		sys.exit(2)
	
	# run main
	main(sys.argv[1],sys.argv[2])



