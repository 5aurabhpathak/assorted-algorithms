#!/bin/env python3.5
from nltk import RecursiveDescentParser, pos_tag, CFG, Tree
from nltk.parse.earleychart import EarleyChartParser
from nltk.draw import TreeView
from os import system, remove

grammar1  = CFG.fromstring("""S -> NP VP
    PP -> P | P NP | P VP
    NP -> Det NP PP1 | Adj N PP1 | N PP1 | N NP PP1
    PP1 -> PP PP1 | 
    VP -> V NP PP1 | V PP1
    Det -> 'DT'
    N -> 'NN' | 'NNS' | 'NNPS' | 'NNP' | 'PRP' | 'PRP$'
    V -> 'VBZ' | 'VBD' | 'VBP' | 'VBG'
    Adj -> 'JJ'
    P -> 'IN'""")

grammar2 = CFG.fromstring("""S -> NP VP
        PP -> P | PP NP | PP VP
        NP -> Det NP | Adj NP | N NP | NP PP | N
        VP -> VP NP | VP PP | V
        Det -> 'DT'
        N -> 'NN' | 'NNS' | 'NNPS' | 'NNP' | 'PRP' | 'PRP$'
        V -> 'VBZ' | 'VBD' | 'VBP' | 'VBG'
        Adj -> 'JJ'
        P -> 'IN'""")

grammar = grammar1

rdparser, earlyparser = RecursiveDescentParser(grammar), EarleyChartParser(grammar)

taggedsent = pos_tag(''.join(c for c in input('Enter a sentence:') if c not in ':,;."').split())
tags = [x[1] for x in taggedsent]

print('Trying to recognize using Recursive Descent...')
j = 1
try:
    for tree in rdparser.parse(tags):
        i = iter(taggedsent)
        for s in tree.subtrees():
            if len(s) == 1 and not isinstance(s[0], Tree): s[0] = next(i)[0]
        tv = TreeView(tree)
        tv._size.set(18)
        tv.resize()
        tv._cframe.canvas()['scrollregion'] = (0, 0, 1000,500)
        tv._cframe.print_to_file('rdout'+str(j)+'.ps')
        system('convert rdout'+str(j)+'.ps -alpha off rdout'+str(j)+'.png')
        remove('rdout'+str(j)+'.ps')
        j += 1
        print(tree)
except RecursionError: pass

print('Trying to recognize using Earley algorithm...')
j = 1
for tree in earlyparser.parse(tags):
    i = iter(taggedsent)
    for s in tree.subtrees():
        if len(s) == 1 and not isinstance(s[0], Tree): s[0] = next(i)[0]
    tv = TreeView(tree)
    tv._size.set(18)
    tv.resize()
    tv._cframe.canvas()['scrollregion'] = (0, 0, 1000,500)
    tv._cframe.print_to_file('earleyout'+str(j)+'.ps')
    system('convert earleyout'+str(j)+'.ps -alpha off earleyout'+str(j)+'.png')
    remove('earleyout'+str(j)+'.ps')
    j += 1
    print(tree)
