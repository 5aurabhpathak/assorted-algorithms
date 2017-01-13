# coding=utf-8
import sys
import codecs
import search

def is_Name(count,str_list):
	if count<len(str_list)-1:
		tmp=0;
		#for e in str_list[count+1]:
		if str_list[count+1][0] == 'न'.decode('utf-8') and str_list[count+1][1] == 'े'.decode('utf-8'):
			return 1;
		
		if str_list[count+1][0] == 'क'.decode('utf-8') and str_list[count+1][1] == 'ी'.decode('utf-8'):
			#print "ch11";
			return 2;
		
		if str_list[count+1][0] == 'क'.decode('utf-8') and str_list[count+1][1] == 'े'.decode('utf-8'):
			return 2;

		if str_list[count+1][0] == 'क'.decode('utf-8') and str_list[count+1][1] == 'ा'.decode('utf-8'):
			return 2;	
	return 0;
	
def join_word(str):
	tmp=0;
	for e in str:
		if (e=='औ'.decode('utf-8')):
			tmp=tmp+1;
		elif (e == 'र'.decode('utf-8')) and tmp==1:
			return 1;
		else:
			break;
	
	tmp=0;
	count=0;
	for e in str:
		if (e == 'य'.decode('utf-8'))and (count==0):
			tmp=tmp+1;
			
		elif (e == 'ा'.decode('utf-8')) and tmp==1:
			return 2;
	
		else:
			break;
	return 0;
	
def del_word(count,str_list):
	tmp=0;
	#for e in str_list[count]:
	if str_list[count][0] == 'न'.decode('utf-8') and str_list[count][1] == 'े'.decode('utf-8'):
		return 1;
	
	if str_list[count][0] == 'क'.decode('utf-8') and str_list[count][1] == 'ी'.decode('utf-8'):
		#print "ch2";
		return 2;
	
	if str_list[count][0] == 'क'.decode('utf-8') and str_list[count][1] == 'े'.decode('utf-8'):
		return 2;
	
	if str_list[count][0] == 'क'.decode('utf-8') and str_list[count][1] == 'ा'.decode('utf-8'):
		return 2;	
	
	return 0;