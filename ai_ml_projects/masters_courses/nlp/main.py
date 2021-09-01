#!/bin/env python3.5
#Author: Saurabh Pathak
from nltk.internals import find_jars_within_path
from nltk.parse.stanford import StanfordParser
from nltk.tokenize import sent_tokenize
from nltk import download
from nltk.tree import ParentedTree
import os

#download('punkt', quiet=True)
#download('names', quiet=True)

os.environ['CLASSPATH'] = os.getenv('CLASSPATH', '') + os.getcwd() + 'data/stanford-parser-full-2015-12-09/stanford-parser.jar:' + os.getcwd() + 'data/stanford-parser-full-2015-12-09/stanford-parser-3.6.0-models.jar'

parser = StanfordParser(model_path='edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')
parser._classpath = find_jars_within_path(os.getcwd() + 'data/stanford-parser-full-2015-12-09')

text = input('Enter some text:')

tlist = [ParentedTree.fromstring(str(list(parsetree)[0])) for parsetree in parser.raw_parse_sents(sent_tokenize(text))]

tlist2 = [tree.copy(True) for tree in tlist]
from hobbs import *
from lappinleasse import *

print('Input text was:\n', text)
def resolve(ls, algo):
    print('\nResolving with', algo)
    i = -1
    for parsetree in ls:
        i += 1
        print("processing sentence {}...".format(i+1))
        if algo == "Hobb's algorithm": hobbs(parsetree, i, ls)
        else: lappinleasse(parsetree, i)

    print('\nAnaphora resolved sentences...')
    for parsetree in ls: print(" ".join(parsetree.leaves()))

resolve(tlist, "Hobb's algorithm")
resolve(tlist2, "Lappin and Leasse's algorithm")
