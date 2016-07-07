#!/bin/env python3.5
from nltk.tag.stanford import StanfordNERTagger
from nltk.internals import find_jars_within_path
from nltk.tokenize import sent_tokenize
import os

tagger = StanfordNERTagger('data/stanford-ner-2015-12-09/classifiers/english.all.3class.distsim.crf.ser.gz', 'data/stanford-ner-2015-12-09/stanford-ner.jar')
tagger._stanford_jar = ':'.join(find_jars_within_path(os.getcwd() + 'data/stanford-ner-2015-12-09'))
print(tagger.tag_sents([''.join([c for c in x if c not in '",:.?/!@#$%^&*()][{}~']).split() for x in sent_tokenize(input('Enter a sentence: '))]))
