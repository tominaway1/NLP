#! /usr/bin/python

__author__="Alexander Rush <srush@csail.mit.edu>"
__date__ ="$Sep 12, 2012"

import sys, json

"""
Count rule frequencies in a binarized CFG.
"""

class Counts:
  def __init__(self):

    #count dictionaries
    self.unary = {}
    self.binary = {}
    self.nonterm = {}
    self.term = {}

    #probabilities
    self.binary_probabilities = {}
    self.unary_probabilities = {}

    # other usefule information
    self.wordbank = {}
    self.binary_rules = {}


  def show(self):
    for symbol, count in self.nonterm.iteritems():
      print count, "NONTERMINAL", symbol

    for (sym, word), count in self.unary.iteritems():
      print count, "UNARYRULE", sym, word

    for (sym, y1, y2), count in self.binary.iteritems():
      print count, "BINARYRULE", sym, y1, y2

  def count(self, tree):
    """
    Count the frequencies of non-terminals and rules in the tree.
    """
    if isinstance(tree, basestring): return

    # Count the non-terminal symbol. 
    symbol = tree[0]
    self.nonterm.setdefault(symbol, 0)
    self.nonterm[symbol] += 1
    
    if len(tree) == 3:
      # It is a binary rule.
      y1, y2 = (tree[1][0], tree[2][0])
      key = (symbol, y1, y2)
      self.binary.setdefault(key, 0)
      self.binary[(symbol, y1, y2)] += 1
      if symbol not in self.binary_rules:
        self.binary_rules[symbol] = [(y1,y2)]
      else:
        temp = self.binary_rules[symbol]
        if (y1,y2) not in temp:
          temp.append((y1,y2))
          self.binary_rules[symbol] = temp
      
      # Recursively count the children.
      self.count(tree[1])
      self.count(tree[2])
    
    elif len(tree) == 2:
      # It is a unary rule.
      y1 = tree[1]
      key = (symbol, y1)
      self.unary.setdefault(key, 0)
      self.unary[key] += 1

  ## MY IMPLEMENTATIONS ##

  #counts the terminal symbols
  def counts(self):
    for (sym, word), count in self.unary.iteritems():
      self.term.setdefault(word, 0)
      self.term[word] += count

  #parses through terminal symbols and keeps everything more than 5
  def create_wordbank(self):
    for word in self.term:
      if self.term[word]>=5:
        self.wordbank[word] = 1

  # calculates unary and binary probabilities
  def calculate_probabilities(self):
    for (sym, y1, y2), count in self.binary.iteritems():
      if sym not in self.nonterm:
        continue 
      self.binary_probabilities[(sym, y1, y2)] = float(count) / float(self.nonterm[sym])
    
    for (sym, word), count in self.unary.iteritems():
      if word not in self.term:
        word = '__RARE__'
      self.unary_probabilities[(sym, str(word))] = float(count) / float(self.nonterm[sym])

  # writes tree to output file
  def write_tree(self,parse_file,outfile):
    outfile = open(outfile,'w')
    for l in open(parse_file):
      t = json.loads(l)
      self.update(t)
      json.dump(t,outfile)
      outfile.write('\n')

  # updates any terminals with __RARE__ if count less than 5
  def update(self,tree):
    if len(tree) == 3:      
      # Recursively count the children.
      self.update(tree[1])
      self.update(tree[2])
    
    elif len(tree) == 2:
      # It is a unary rule.
      y1 = tree[1]
      if self.term[y1]<5:
        tree[1] = '__RARE__'


def main(parse_file):
  counter = Counts() 
  for l in open(parse_file):
    t = json.loads(l)
    counter.count(t)
  counter.counts()
  counter.write_tree(parse_file,'modified_parse_train.dat')
  counter.show()

def usage():
    sys.stderr.write("""
    Usage: python count_cfg_freq.py [tree_file]
        Print the counts of a corpus of trees.\n""")

if __name__ == "__main__": 
  if len(sys.argv) != 2:
    usage()
    sys.exit(1)
  main(sys.argv[1])
  
