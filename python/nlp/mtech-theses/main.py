# coding=utf-8
import sys
import codecs
import split as split1
import tag
import rule
import search

#Reading File Pointers
input= codecs.open('data/input/test1.txt', encoding='utf-8',mode='r');

#Writeing File Pointers
#output = codecs.open('data/output/test1.txt', encoding='utf-8',mode='w');

count=0;
eb=search.eb_hash();
dir=search.dir_hash();

for str1 in input.readlines():	#for each sentence
	#print count+1;
	str=str1.split('.');
	#Spliting the words
	words=split1.eb_split(str[0]);
	#Example base Translation + Tagging and translation word by word
	tag_words=tag.tag1(words,eb,dir);	#0: Tagging 1: English Translation 2: Hindi Words
	#Rule Base approch 
	#print tag_words[1];
	result=rule.trans_rule(tag_words[1],tag_words[0]);
	count+=1;
