#!/bin/env python3.5
from nltk import RecursiveDescentParser, CFG, pos_tag, word_tokenize
from nltk.draw.tree import TreeView
from os import system, remove

rdparser = RecursiveDescentParser(CFG.fromstring("""S -> NP VP
    PP -> P | P NP | P VP
    NP -> Det NP PP1 | Adj N PP1 | N PP1 | N NP PP1
    PP1 -> PP PP1 | 
    VP -> V NP PP1 | V PP1
    Det -> 'DT'
    N -> 'NN' | 'NNS' | 'NNPS' | 'NNP' | 'PRP' | 'PRP$'
    V -> 'VBZ' | 'VBD' | 'VBP' | 'VBG'
    Adj -> 'JJ'
    P -> 'IN'"""))

taggedsent = pos_tag(word_tokenize(''.join(c for c in input('Enter a sentence:') if c not in ':,;."')))
j = 1
for tree in rdparser.parse([x[1] for x in taggedsent]):
    i = iter(taggedsent)
    for s in tree.subtrees():
        if len(s) == 1: s[0] = next(i)[0]
    tv = TreeView(tree)
    tv._size.set(18)
    tv.resize()
    tv._cframe.canvas()['scrollregion'] = (0, 0, 1000,500)
    tv._cframe.print_to_file('output'+str(j)+'.ps')
    if system('convert output'+str(j)+'.ps -alpha off output'+str(j)+'.png') != 0:
       print(tree)
    remove('output'+str(j)+'.ps')
    j += 1
