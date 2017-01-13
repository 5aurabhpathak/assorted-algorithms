# coding=utf-8
import codecs
	
def eb_hash():
	fr_db = codecs.open('data/DB/db_ebmt.txt', encoding='utf-8',mode='r');
	eb={};
	for temp in fr_db:
		line=temp[:-2];
		db=line.split('=');
		eb[db[0]]=db[1];
	
	return eb;
	
def dir_hash():
	fr = codecs.open('data/DB/dir.txt',  encoding='utf-8',mode='r')
	dir={};
	for line in fr:
		temp=line.split('=');
		try:
			b=dir[temp[0]];
			b.append(line);
			dir[temp[0]]=b;
		except KeyError, e:
			a=[];
			a.append(line);
			dir[temp[0]]=a;
			
	return dir;
