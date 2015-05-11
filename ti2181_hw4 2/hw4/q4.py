import sys,re
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

def main(model,sentences,output):
	# generate dictionaries
	arr = create_tags(model,sentences)
	f = open(output,'w')
	for line in arr:
		f.write(line)

def create_tags(model,sentences):
	# initialize final array
	arr = []
	# initialize servers
	enum_serv = Procserver(['python', 'tagger_history_generator.py', 'ENUM'])
	history_serv = Procserver(['python', 'tagger_decoder.py', 'HISTORY'])

	# iterate through every sentence
	for sentence in sentences:
		if len(sentence) == 0:
			continue

		# get history
		h = enum_serv.communicate(sentence)
		h = h.split('\n')
		
		# calculate the weight
		weight = calculate_weight(h,sentence.split(),model)

		# find tag
		tag = history_serv.communicate(weight)
		tag = tag.split('\n')
		sentence1 = sentence.split('\n')

		# add to output arr
		for i in range(len(sentence1)):
			# get tag from output
			outTag = tag[i].split()
			outTag = outTag[2]
			# add to output array
			arr.append('{0} {1}\n'.format(sentence1[i],outTag))
		arr.append('\n')
	return arr

def calculate_weight(h,s,m):
	answer = ''
	for line1 in h:
		line = line1.split()
		if len(line) < 1:
			continue
		if line[2] == 'STOP':
			continue
		# get index
		index = int(line[0]) - 1
		# get word
		word = s[index]
		# get tag
		tag = line[2]

		# initialize weight
		weight = 0

		# generate all features
		bigram = "BIGRAM:{0}:{1}".format(line[1],tag)
		t = "TAG:{0}:{1}".format(word,tag)
		suffix =['SUFFIX:{0}:3:{1}'.format(word[-3:],tag),'SUFFIX:{0}:2:{1}'.format(word[-2:],tag),'SUFFIX:{0}:1:{1}'.format(word[-1:],tag)]
		
		# part 6 features
		lengthFeat = ['LENGTH:{0}:{1}'.format(str(len(word)),tag)]
		prefixFeat = ['PREFIX:{0}:3:{1}'.format(word[:3],tag),'PREFIX:{0}:2:{1}'.format(word[:2],tag),'PREFIX:{0}:1:{1}'.format(word[:1],tag)]
		formFeat = ['FORM:{0}:{1}'.format(identifyForm(word),tag)]

		# total features
		features = [bigram,t] + suffix + lengthFeat + prefixFeat + formFeat
		
		# calculate weight
		for item in features:
			if item in m:
				weight += m[item]
		answer += "{0} {1}\n".format(line1, str(weight))
	return answer

def make_dict(model):
	d = {}
	for line in model.read().split('\n'):
		line = line.split(' ')
		if len(line) == 2:
			d[line[0]] = float(line[1])
	# print d
	return d

def make_sentences(dev):
	arr = []
	for line in dev.read().split('\n\n'):
		# line = line.replace('\n',' ')
		arr.append(line)
	return arr

def identifyForm(word):
	if re.findall('[0-9]', word):
		if word.isdigit():
			form = "AllDigit"
		else:
		    form = 'HasDigit'

	# letters
	else:
		if re.match('^[A-Z]+$', word):
		    form = 'AllCaps'

		elif re.match('^[A-Z][^A-Z]*$', word):
		    form = 'Capitalized'
		elif re.match('^[a-z]+$', word):
		    form = 'Lowercase'
		elif word in [".",',']:
			form = 'Punctuation'
		else:
		    form = '_other_'
	return form


def usage():
	print "Proper usage: python q4.py [tag.model] [tag.dev] [output]"

if __name__ == '__main__':
	if len(sys.argv) != 4:
		usage()
		sys.exit(2)
	# open files
	model = open(sys.argv[1],'r')
	dev = open(sys.argv[2],'r')

	# generate model dictionary
	m = make_dict(model)
	sentences = make_sentences(dev)
	
	# close dicts
	dev.close()
	model.close()

	# run main
	main(m,sentences,sys.argv[3])