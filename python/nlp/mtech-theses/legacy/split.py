# coding=utf-8
import sys
import codecs

def eb_split(str):
	fr_db = codecs.open('data/DB/db_ebmt.txt', encoding='utf-8',mode='r');
	for line in fr_db:
		line=line[:-2];
		db=line.split('=');
		match=str.find(db[0]);
		if match!=-1:
			#Finding Start and End postion of Example
			start= match;
			end=start+len(db[0])+1;
			#Spliting the words
			temp=str[:start] +'=' + str[start:];
			temp2=temp[:end]+'='+temp[end:];

			words=temp2.split('=');
			if(start!=0):
				words[0]=words[0][:-1];
				full_split=words[0].split(' ');
				full_split.append(words[1]);
				if(end<len(str)-1):
					words[2]=words[2][1:];
					temp3=words[2].split(' ');
					for temp4 in temp3:
						full_split.append(temp4);
			else:
				full_split=list();
				full_split.append(words[1]);
				if(end<len(str)-1):
					words[2]=words[2][1:];
					temp3=words[2].split(' ');
					for temp4 in temp3:
						full_split.append(temp4);

			return full_split;

	return str.split(' ');
			
			
#Reading File Pointers
# input= codecs.open('Input/test1.txt', encoding='utf-8',mode='r');
# output = codecs.open('output/temp.txt', encoding='utf-8',mode='w');

# for str in input.readlines():
	# words=eb_split(str);
	# print len(words);
	# if words!=-1:
		# for word in words:
			# output.write(word+'\n');
	
# print "done";
